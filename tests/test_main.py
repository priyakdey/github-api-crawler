from crawler import main


def test_main(mocker):
    mocker.patch("crawler.api_client.get_all_categories", return_value=[])
    assert main.main() == "Main function"
