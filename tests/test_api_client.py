from datetime import timedelta, datetime

import pytest

from crawler.api_client import RestClient, Token
from crawler import api_client
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


@pytest.mark.parametrize(
    "minutes,seconds,expected",
    [(4, 58, False), (4, 59, True), (5, 00, True)]
)
def test_token_is_expired(mocker, minutes, seconds, expected):
    # Clear cache FIXME : find a better way to contain test
    Token._token = None
    Token._tte = None

    def mock_token(*args, **kwargs):
        return MockResponse({"token": "some-random-token"}, 200)

    mocker.patch("requests.get", side_effect=mock_token)
    Token.get_token()

    mock_now = datetime.now() + timedelta(minutes=minutes, seconds=seconds)
    mocker.patch("crawler.api_client._now", return_value=mock_now)

    assert Token._is_expired() is expected


def test_get_token_when_not_expired(mocker):
    # Clear cache FIXME : find a better way to contain test
    Token._token = None
    Token._tte = None

    def first_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "first-token"}, 200)

    mocker.patch("requests.get", side_effect=first_mock_token_from_server)
    assert Token.get_token() == "first-token"

    # Let us mock a call 2 minutes before the expiration
    mock_current_time = Token._tte - timedelta(minutes=2)
    mocker.patch("crawler.api_client._now", return_value=mock_current_time)

    # a new  token should come from the server in case the actual call goes through
    def second_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "second-token"}, 200)

    mocker.patch("requests.get", side_effect=second_mock_token_from_server)
    assert Token.get_token() == "first-token"


def test_get_token_when_expired(mocker):
    # Clear cache FIXME : find a better way to contain test
    Token._token = None
    Token._tte = None

    def first_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "first-token"}, 200)

    mocker.patch("requests.get", side_effect=first_mock_token_from_server)
    assert Token.get_token() == "first-token"

    # Let us mock a call exactly 1 second after the expiration
    mock_current_time = Token._tte + timedelta(seconds=1)
    mocker.patch("crawler.api_client._now", return_value=mock_current_time)

    # a new  token should come from the server in case the actual call goes through
    def second_mock_token_from_server(*args, **kwargs):
        return MockResponse({"token": "second-token"}, 200)

    mocker.patch("requests.get", side_effect=second_mock_token_from_server)
    assert Token.get_token() == "second-token"


def test_get_details_for_category(mocker, animals_page_one, animals_page_two):
    def mock_data(*args, **kwargs):
        if args[0] == "https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=1&category=Animals":
            return MockResponse(animals_page_one, 200)
        elif args[0] == "https://public-apis-api.herokuapp.com/api/v1/apis/entry?page=2&category=Animals":
            return MockResponse(animals_page_two, 200)

    mocker.patch("requests.get", side_effect=mock_data)
    mocker.patch("crawler.api_client.Token.get_token", return_value="some-random-token")

    # Test for page 1
    count, data = api_client.get_details_for_category("Animals")
    assert count == 13
    assert len(data) == 10

    # Test for page 3
    count, data = api_client.get_details_for_category("Animals", 2)
    assert count == 13
    assert len(data) == 3


def test_get_all_categories(mocker, categories_page_one, categories_page_two):
    def mock_get_categories_from_server(*args, **kwargs):
        if args[0] == "https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=1":
            return MockResponse(categories_page_one, 200)
        elif args[0] == "https://public-apis-api.herokuapp.com/api/v1/apis/categories?page=2":
            return MockResponse(categories_page_two, 200)

    mocker.patch("requests.get", side_effect=mock_get_categories_from_server)
    mocker.patch("crawler.api_client.Token.get_token", return_value="some-random-token")

    mock_categories_list = categories_page_one["categories"] + categories_page_two["categories"]
    categories = api_client.get_all_categories()
    assert categories == mock_categories_list
