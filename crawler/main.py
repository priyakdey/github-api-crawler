import logging

from crawler import api_client

FORMAT = "%(asctime)s %(levelname)9s %(process)d --- [%(name)25s] : %(message)s"
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main() -> str:
    logger.info("Hello")
    categories = api_client.get_all_categories()
    api_details = api_client.get_details_for_all_categories(categories)
    print(api_details)
    print(len(api_details))
    return "Main function"
