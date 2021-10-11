import logging
from datetime import datetime, timedelta
from math import ceil
from typing import Dict, Any, List, Tuple

import requests
from ratelimit import limits, sleep_and_retry

from crawler import constants as C
from crawler.exceptions import APIException

logger = logging.getLogger(__name__)


class RestClient:
    """Client which is capable of making Rest API calls"""

    @staticmethod
    @sleep_and_retry
    @limits(calls=10, period=timedelta(seconds=62).total_seconds())  # 2 seconds grace
    def get(url: str, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Makes a get call and returns a jsonified response.
        In case server returns non 200 code, raised APIException
        """
        logger.info("GET - %s", url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            # Because of how we are managing the rate limiter, there can be cases where
            # the token is not expired, but till thread comes alive, it is. So we then retry
            # Issue: https://github.com/priyakdey/github-api-crawler/issues/16
            return _retry(url)
        else:
            raise APIException(response.status_code, "Issue with external api")  # TODO: err msg to be better


def _retry(url: str) -> Dict[str, Any]:
    logger.info("The token has expired. Need to retry with a new token")
    token = Token.get_token()
    headers = {"Authorization": "Bearer " + token}
    return RestClient.get(url, headers)


class Token:
    """Class is responsible to cache a Authentication token and also expiration.
    Class has one class method get_token() which returns the cached token
    or else makes a call if token is null or expired.
    """

    _token = None
    _tte = None

    @classmethod
    def get_token(cls) -> str:
        if cls._token is None or cls._is_expired():
            # Make a call to get the token
            logger.info("Token cache is empty or expired. Getting a token from the server")
            data = RestClient.get(C.GET_TOKEN_URL)
            cls._token = data["token"]
            cls._tte = _now() + timedelta(minutes=4, seconds=59)  # keep 1 second grace
            logger.info("Token received from server. Token will expire at %s", cls._tte)
        return cls._token

    @classmethod
    def _is_expired(cls) -> bool:
        """Checks if token has expired"""
        return True if _now() >= cls._tte else False


def get_details_for_category(category: str, page: int = 1) -> Tuple[int, List[Dict[str, Any]]]:
    """Returns the API details for a category

    :param category The category for which details is requests
    :param page Page number for which details is requested. Default value is 1
    :returns (total count, list of api details)
    """
    logger.info("Getting api details for %s and page number %s", category, page)
    url = C.GET_DATA_FOR_CATEGORY_URL.substitute({"page": page, "category": category})
    token = Token.get_token()
    headers = {"Authorization": "Bearer " + token}
    data = RestClient.get(url, headers=headers)
    return data["count"], data["categories"]


def get_all_categories() -> List[str]:
    """Returns a list of all the categories returned by the API

    :returns List of categories
    """
    logger.info("Fetching all categories from api")
    categories = []

    data = _get_category_for_page(1)
    total_count = data["count"]
    logger.info("Total count of categories is %s", total_count)
    categories.extend(data["categories"])

    # Pagination for categories
    start_page = 2
    end_page = ceil(total_count / 10)

    for page in range(start_page, end_page + 1):
        data = _get_category_for_page(page)
        categories.extend(data["categories"])

    logger.info("Fetched all categories from api")
    logger.debug(categories)
    return categories


def get_details_for_all_categories(categories: List[str]) -> List[Dict[str, Any]]:
    """Get all api details for categories

    :param categories List of all categories returned from server
    :returns List of api details
    """
    api_details = []
    for category in categories:
        total_count, data = get_details_for_category(category, 1)
        api_details.extend(data)
        start_page = 2
        end_page = ceil(total_count / 10)

        for page in range(start_page, end_page + 1):
            _, data = get_details_for_category(category, page)
            api_details.extend(data)
    return api_details


def _get_category_for_page(page: int) -> Dict[str, Any]:
    url = C.GET_ALL_CATEGORIES_URL.substitute({"page": page})
    token = Token.get_token()
    headers = {"Authorization": "Bearer " + token}
    data = RestClient.get(url, headers=headers)
    return data


# Cause this makes more sense than to use a third part lib to test
def _now() -> datetime:
    """Returns current timestamp"""
    return datetime.now()
