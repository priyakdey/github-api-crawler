import logging

from crawler import api_client, banner, db
from crawler.exceptions import APIException, DatabaseException

FORMAT = "%(asctime)s %(levelname)9s %(process)d --- [%(name)25s] : %(message)s"
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("------------------------------------------------")
    logger.info(banner.APP_BANNER)
    logger.info("Starting crawling process")
    try:
        categories = api_client.get_all_categories()
        logger.info("Total categories fetched = %s", len(categories))
        api_details = api_client.get_details_for_all_categories(categories)
        logger.info("Total api data fetched = %s", len(api_details))
        db.insert_all(api_details)
        logger.info("Exiting application successfully")
        return 0
    except APIException:
        logger.info("Exiting application with error")
        return 1  # TODO: Logging and proper exit codes
    except DatabaseException:
        logger.info("Exiting application with error")
        return 2  # TODO: Logging and proper exit codes
