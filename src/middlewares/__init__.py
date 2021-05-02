from fastapi import FastAPI

from middlewares.localization import LocalizationMiddleware
from middlewares.operation_log import OperationLog
# from middlewares.authentication import AuthenticationMiddleware


def add_all_middleware(app: FastAPI):
    # app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(LocalizationMiddleware)
    app.add_middleware(OperationLog)
