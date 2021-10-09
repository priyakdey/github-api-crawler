import logging
from typing import Dict, Any

import requests

from crawler.exceptions import APIException

logger = logging.getLogger(__name__)


class RestClient:
    """Client which is capable of making Rest API calls"""

    @staticmethod
    def get(url: str, headers: Dict[str, Any] = None):
        """Makes a get call"""
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise APIException(response.status_code, "Issue with external api")  # TODO: err msg to be better
