import logging

from crawler import api_client, db

FORMAT = "%(asctime)s %(levelname)9s %(process)d --- [%(name)25s] : %(message)s"
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main() -> str:
    logger.info("Hello")
    api_client.get_all_categories()
    return "Main function"
