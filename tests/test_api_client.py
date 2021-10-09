import pytest

from crawler.api_client import RestClient
from crawler.exceptions import APIException


class MockResponse:
    """Mock Response to be returned"""

    def __init__(self, json_date, status_code):
        self.json_data = json_date
        self.status_code = status_code

    def json(self):
        return self.json_data


def test_get_success(mocker):
    def mock_request_get(*args, **kwargs):
        """Mock function to be called instead of requests.get to return a Mock reponse"""
        return MockResponse({"key": "value"}, 200)

    mocker.patch("requests.get", side_effect=mock_request_get)
    data = RestClient.get("http://mock-url")
    assert data == {"key": "value"}


def test_get_exception(mocker):
    def mock_request_get(*args, **kwargs):
        return MockResponse(None, 404)

    mocker.patch("requests.get", side_effect=mock_request_get)
    with pytest.raises(APIException) as e:
        RestClient.get("http://mock-url")
    assert e.value.err_code == 404
    assert e.value.err_msg == "Issue with external api"
