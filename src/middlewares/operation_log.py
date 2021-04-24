

from starlette.middleware.base import BaseHTTPMiddleware
from models.errors import HttpForbidden
from starlette.exceptions import HTTPException
from starlette import status

from starlette.requests import HTTPConnection

# from fastapi_contrib.common.responses import UJSONResponse

class OperationLog(BaseHTTPMiddleware):
    async def save_old_data(self, request):
        print("---isshe---: save_old_data ---")
        # check url and method

        # get data

        # save data to request ctx


    async def oplog(self, request):
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="test auth")
        print("---isshe---: oplog ---")
        # check method

    async def dispatch(self, request, call_next):
        print("---isshe---: oplog dispatch dispatch---")
        print("---isshe---: request = ", request)
        await self.save_old_data(request)
        response = await call_next(request)
        if response and response.status_code >= 200 and response.status_code < 300:
            await self.oplog(request)
        print("---isshe---: response = ", response)
        print("---isshe---: response.status_code = ", response.status_code)

        return response