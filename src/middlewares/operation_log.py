

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.requests import HTTPConnection

# from fastapi_contrib.common.responses import UJSONResponse
from services.authentication import get_current_user
from models.errors import HttpForbidden

class OperationLog(BaseHTTPMiddleware):
    async def get_old_data(self, request):
        pass
        # check url and method

        # get data

        # save data to request ctx

    def is_change_method(self, method: str) -> bool:
        return method == "DELETE" or method == "PUT"

    def is_write_method(self, method: str) -> bool:
        return method == "POST" or self.is_change_method(method)


    async def log(self, request: Request):
        if not self.is_write_method(request.method):
            return

        # do log


    async def dispatch(self, request: Request, call_next):
        # user = await get_current_user(request)
        # if self.is_change_method(request.method):
        #     await self.get_old_data(request)
        response = await call_next(request)
        if response and response.status_code >= 200 and response.status_code < 300:
            await self.log(request)

        return response