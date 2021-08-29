from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from services.authentication import get_current_user

URL_WHITE_LIST = {
    "/api/v1/login": True,
    "/api/v1/register": True,
    "/api/v1/language": True,
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
        print("---isshe---: path = ", path)
        if path not in URL_WHITE_LIST.keys():
            # get access user
            current_user = await get_current_user(request)

            # check if user has permission to access the uri
            # get user's roles

            # get role's permissions

            # check permissions

            pass

        return await call_next(request)
