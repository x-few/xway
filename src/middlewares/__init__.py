from fastapi import FastAPI

from middlewares.localization import LocalizationMiddleware
from middlewares.operation_log import OperationLogMiddleware
from middlewares.permission import PermissionMiddleware
# from middlewares.authentication import AuthenticationMiddleware


def add_all_middleware(app: FastAPI):
    app.add_middleware(LocalizationMiddleware)
    app.add_middleware(PermissionMiddleware)
    app.add_middleware(OperationLogMiddleware)
