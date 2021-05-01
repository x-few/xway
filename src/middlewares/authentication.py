

from starlette.middleware.base import BaseHTTPMiddleware
from models.errors import HttpForbidden
from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import HTTPConnection
from fastapi import Header, Security, Depends

# from fastapi_contrib.common.responses import UJSONResponse

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def authentication(self, request):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="test auth")
        # try:
        # except KeyError:
        #     raise HttpForbidden("X-Token header invalid")
        # # await get_token_header()
        pass

    async def dispatch(self, request, call_next):
        # await self.authentication(request)
        response = await call_next(request)
        return response