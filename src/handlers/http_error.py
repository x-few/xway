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


async def server(request: Request, exc: HttpServerError) -> JSONResponse:
    traceback.print_exc()
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def client(request: Request, exc: HttpClientError) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]},
                        status_code=status.HTTP_400_BAD_REQUEST)


async def unauthorized(request: Request, exc: HttpUnauthorized) -> JSONResponse:
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
    traceback.print_exc()
    return JSONResponse({"errors": [exc.errors()]},
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def handler(request: Request, exc: HTTPException) -> JSONResponse:
    # set to default error detail
    _ = request.state.get_gettext
    if exc.status_code == status.HTTP_400_BAD_REQUEST:
        # TODO
        return await client(request, exc)
    elif exc.status_code == status.HTTP_401_UNAUTHORIZED:
        exc.detail = _("Not authenticated")
        return await unauthorized(request, exc)
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        # TODO
        return await forbidden(request, exc)
    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        # TODO
        return await notfound(request, exc)
    elif exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        # TODO
        return await validation_error(request, exc)
    elif exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        exc.detail = _("Internal Server Error")
        return await server(request, exc)

    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
