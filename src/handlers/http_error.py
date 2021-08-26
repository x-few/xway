import traceback
from typing import Union
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette import status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from models.errors import HttpServerError, HttpClientError, \
    HttpForbidden, HttpNotFound, HttpUnauthorized, \
    EntityDoesNotExist, UnprocessableEntity


async def handler(request: Request, exc: HTTPException) -> JSONResponse:
    # print("exc.status_code = ", exc.status_code)
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def server(request: Request, exc: HttpServerError) -> JSONResponse:
    traceback.print_exc()
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def client(request: Request, exc: HttpClientError) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_400_BAD_REQUEST)


async def notauth(request: Request, exc: HttpUnauthorized) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_401_UNAUTHORIZED)


async def forbidden(request: Request, exc: HttpForbidden) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_403_FORBIDDEN)


async def notfound(request: Request, exc: HttpNotFound) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_404_NOT_FOUND)


async def entitynotfound(request: Request, exc: EntityDoesNotExist) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_404_NOT_FOUND)


async def unprocessable_entity(request: Request, exc: UnprocessableEntity) -> JSONResponse:
    traceback.print_exc()
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def validation_error(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    return JSONResponse({"errors": [exc.errors()]},
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
