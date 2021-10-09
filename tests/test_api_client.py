from datetime import timedelta

import pytest

from crawler.api_client import RestClient, Token
from crawler.exceptions import APIException


class MockResponse:
    """Class to mock server responses"""

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


def test_get_token_if_empty_cache(mocker):
    def mock_token(*args, **kwargs):
        return MockResponse({"token": "some-random-token"}, 200)

    mocker.patch("requests.get", side_effect=mock_token)
    token = Token.get_token()
    assert token == "some-random-token"
    assert Token._tte is not None


def test_get_token_when_not_expired(mocker):
    def first_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "first-token"}, 200)
    mocker.patch("requests.get", side_effect=first_mock_token_from_server)
    assert Token.get_token() == "first-token"

    # Let us mock a call 2 minutes before the expiration
    mock_current_time = Token._tte - timedelta(minutes=-2)
    mocker.patch("crawler.api_client._now", return_value=mock_current_time)

    # a new  token should come from the server in case the actual call goes through
    def second_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "second-token"}, 200)
    mocker.patch("requests.get", side_effect=second_mock_token_from_server)
    assert Token.get_token() == "first-token"


def test_get_token_when_expired(mocker):
    def first_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "first-token"}, 200)
    mocker.patch("requests.get", side_effect=first_mock_token_from_server)
    assert Token.get_token() == "first-token"

    # Let us mock a call exactly 5 minutes 1 second after the expiration
    mock_current_time = Token._tte - timedelta(minutes=5, seconds=1)
    mocker.patch("crawler.api_client._now", return_value=mock_current_time)

    # a new  token should come from the server in case the actual call goes through
    def second_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "second-token"}, 200)
    mocker.patch("requests.get", side_effect=second_mock_token_from_server)
    assert Token.get_token() == "second-token"
