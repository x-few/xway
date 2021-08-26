from typing import AsyncIterator

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

# from fastapi_contrib.common.responses import UJSONResponse
from services.operation_log import record as record_operation_log


class OperationLog(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return await record_operation_log(request, response)
