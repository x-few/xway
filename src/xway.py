import os
import uvicorn
import time
import routers

from config import config
from fastapi import FastAPI
from fastapi import Depends, Request, Header
# from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from handlers.app_start import handler as app_start_handler
from handlers.app_stop import handler as app_stop_handler
from handlers.http_error import handler as http_error_handler
from handlers.request_validation_error import handler as request_validation_error
from handlers.connection_refused_error import handler as connection_refused_error

def application() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_exception_handler(Exception, app_error_handler)

    app.add_event_handler("startup", app_start_handler(app))
    app.add_event_handler("shutdown", app_stop_handler(app))

    app.add_exception_handler(ConnectionRefusedError, connection_refused_error)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error)

    app.include_router(routers.router, prefix=config.ROUTER_PREFIX)

    return app


app = application()

if __name__ == "__main__":
    uvicorn.run("xway:app", **config.APP)