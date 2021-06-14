

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# from fastapi_contrib.common.responses import UJSONResponse
from services.operation_log import record as record_oplog

class OperationLog(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # print("---isshe---: OperationLog---")
        # try:
        await record_oplog(request, response)
        # except (KeyError, AttributeError):
        #     # TODO warning...
        #     print("---isshe--- AttributeError")
        #     pass

        return response