from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi import FastAPI
from models.errors import HttpServerError, HttpClientError, \
    HttpForbidden, HttpNotFound, HttpUnauthorized, EntityDoesNotExist
# from middlewares.operation_log import OperationLog
# from middlewares.authentication import AuthenticationMiddleware
from . import app_start, \
            app_stop, \
            http_error


def add_all_handler(app: FastAPI):
    app.add_event_handler("startup", app_start.handler(app))
    app.add_event_handler("shutdown", app_stop.handler(app))

    app.add_exception_handler(HTTPException, http_error.handler)
    app.add_exception_handler(HttpServerError, http_error.server)
    app.add_exception_handler(HttpClientError, http_error.client)
    app.add_exception_handler(HttpUnauthorized, http_error.notauth)
    app.add_exception_handler(HttpForbidden, http_error.forbidden)
    app.add_exception_handler(HttpNotFound, http_error.notfound)
    app.add_exception_handler(EntityDoesNotExist, http_error.entitynotfound)
    app.add_exception_handler(RequestValidationError, http_error.validation_error)
    app.add_exception_handler(ValidationError, http_error.validation_error)

    # app.add_middleware(OperationLog)
    # app.add_middleware(AuthenticationMiddleware)

