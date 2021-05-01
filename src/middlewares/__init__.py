from fastapi import FastAPI

from middlewares.operation_log import OperationLog
from middlewares.authentication import AuthenticationMiddleware


def add_all_middleware(app: FastAPI):
    app.add_middleware(OperationLog)
    app.add_middleware(AuthenticationMiddleware)
