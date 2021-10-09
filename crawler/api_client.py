import logging
from datetime import datetime, timedelta
from typing import Dict, Any

import requests

from crawler import constants as C
from crawler.exceptions import APIException

logger = logging.getLogger(__name__)


class RestClient:
    """Client which is capable of making Rest API calls"""

    @staticmethod
    def get(url: str, headers: Dict[str, Any] = None) -> Dict[str, Any]:
        """Makes a get call and returns a jsonified response.
        In case server returns non 200 code, raised APIException
        """
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(response.status_code, "Issue with external api")  # TODO: err msg to be better


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
            logger.info("Getting a token from the server")
            data = RestClient.get(C.GET_TOKEN_URL)
            cls._token = data["token"]
            cls._tte = _now() + timedelta(minutes=5)
        return cls._token

    @classmethod
    def _is_expired(cls) -> bool:
        """Checks if token has expired"""
        return True if cls._tte > _now() else False


# Cause this makes more sense than to use a third part lib to test
def _now() -> datetime:
    """Returns current timestamp"""
    return datetime.now()
