from crawler import main
from unittest.mock import patch

from crawler.exceptions import APIException, DatabaseException


def test_success(mocker):
    mocker.patch("crawler.api_client.get_all_categories", return_value=[])
    mocker.patch("crawler.api_client.get_details_for_all_categories", return_value=[])
    mocker.patch("crawler.db.insert_all", return_value=None)
    assert main.main() == 0


def test_api_error(mocker):
    def raise_exception(*args, **kwargs):
        raise APIException(503, "Service unavailable")

    mocker.patch("crawler.api_client.get_all_categories", side_effect=raise_exception)
    assert main.main() == 1


def test_db_error(mocker):
    def raise_exception(*args, **kwargs):
        raise DatabaseException(100, "Server not available")

    mocker.patch("crawler.api_client.get_all_categories", return_value=[])
    mocker.patch("crawler.api_client.get_details_for_all_categories", return_value=[])
    mocker.patch("crawler.db.insert_all", side_effect=raise_exception)
    assert main.main() == 2
