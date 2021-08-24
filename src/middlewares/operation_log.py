

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# from fastapi_contrib.common.responses import UJSONResponse
from services.operation_log import record as record_operation_log


class OperationLog(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        await record_operation_log(request, response)

        return response
