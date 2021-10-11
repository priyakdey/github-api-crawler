import logging
from typing import Dict, List, Any

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from crawler import constants as C
from crawler.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Wrapper class for MongoClient. This wrapper is to create a context manager,
    so clients do not need to handle opening, closing or handling error logic.

    Example:
        with DatabaseConnectionManager(conn_string) as conn_manager:
            # do something with the conn_manager (wrapper functions defined at module level)

    With clients using this context manager, they do not need to do resource handling.
    """

    def __init__(self, conn_string: str, timeout_ms: int = C.DB_TIMEOUT_IN_MS) -> None:  # pragma: no  cover
        self.conn_string = conn_string
        self.timeout_ms = timeout_ms

    def __enter__(self) -> MongoClient:  # pragma: no  cover
        self.conn = MongoClient(self.conn_string, serverSelectionTimeoutMS=self.timeout_ms)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # pragma: no  cover
        if self.conn is not None:
            logger.debug("Closing the database connection")
            self.conn.close()


def insert_all(api_details: List[Dict[str, Any]]):
    """Inserts all the api details into the DB"""
    logger.info("Dumping all api details into database")
    conn_string = C.DB_CONN_STRING
    with DatabaseConnectionManager(conn_string) as conn_manager:
        database = conn_manager["api-details-db"]
        collection = database["github-public-api-details"]
        try:
            collection.insert_many(api_details)
            logger.info("Dumping all api details into database completed")
        except PyMongoError as e:
            logger.error("Issue faced while trying to insert the data into db")
            raise DatabaseException(100, e.args[0])  # TODO: Need to check this
