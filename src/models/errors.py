from fastapi import HTTPException

class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""

class BaseException(Exception):
    def __init__(self, detail: str):
            self.detail = detail

class HttpServerError(BaseException):
    """Raised when Server Error"""

class HttpClientError(BaseException):
    """Raised when Client Error"""

class HttpUnauthorized(BaseException):
    """Raised when 401 Error"""

class HttpNotFound(BaseException):
    """Raised when 404 Error"""

class HttpForbidden(BaseException):
    """Raised when 403 Error"""

