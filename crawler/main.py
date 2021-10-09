import logging

from crawler import db

FORMAT = "%(asctime)s %(levelname)9s %(process)d --- [%(name)s] : %(message)s"
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main() -> str:
    logger.info("Hello")
    return "Main function"
