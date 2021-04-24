

from starlette.middleware.base import BaseHTTPMiddleware
from models.errors import HttpForbidden
from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import HTTPConnection

# from fastapi_contrib.common.responses import UJSONResponse

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def authentication(self, request):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="test auth")
        print("---isshe---: AuthenticationMiddleware authentication---")

    async def dispatch(self, request, call_next):
        print("---isshe---: AuthenticationMiddleware dispatch---")
        await self.authentication(request)
        response = await call_next(request)
        return response