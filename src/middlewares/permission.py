from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.exceptions import HTTPException

from models.errors import HttpUnauthorized, HttpForbidden
from services.authentication import get_current_user
from handlers.http_error import handler, unauthorized


URL_WHITE_LIST = {
    "/api/v1/login": True,
    "/api/v1/register": True,
    "/api/v1/languages": True,
}


class PermissionMiddleware(BaseHTTPMiddleware):
    """
    Check the user's access rights
    """

    async def dispatch(self, request: Request, call_next):
        # check if uri in whitelist
        path = request['path']
        if path != "/" and path.endswith("/"):
            path = path[:-2]
        if path not in URL_WHITE_LIST.keys():
            # get access user
            try:
                current_user = await get_current_user(request)
            except HTTPException as e:
                return await handler(request, e)
            except HttpUnauthorized as e:
                return await unauthorized(request, e)

            # check if user has permission to access the uri
            # get user's roles

            # get role's permissions

            # check permissions

            pass

        return await call_next(request)
