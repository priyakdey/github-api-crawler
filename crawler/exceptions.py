class ApplicationException(Exception):
    """Base Exception class for all exceptions across the application"""

    def __init__(self, err_code: int, err_msg: str) -> None:
        super(ApplicationException, self).__init__(err_code, err_msg)
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):  # pragma: no cover
        return f"Error Code: {self.err_code}. Error Message: {self.err_msg}"

    def __repr__(self):  # pragma: no cover
        return self.__str__()


class APIException(ApplicationException):
    """Raised when and External API Call returns non 200 code"""
    pass


class DatabaseException(ApplicationException):
    """Raised when issue with database connection"""
    pass
