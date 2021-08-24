from typing import AsyncIterator

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

# from fastapi_contrib.common.responses import UJSONResponse
from services.operation_log import record as record_operation_log


async def read_bytes(generator: AsyncIterator[bytes]) -> bytes:
    body = b""
    async for data in generator:
        body += data
    return body


async def get_body_from_streaming_response(streaming: StreamingResponse):
    return await read_bytes(streaming.body_iterator)


class OperationLog(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        method = request.method
        if method == "PUT" or method == "POST":
            if response.headers['content-type'] != "application/json" \
                    and response.media_type != "application/json":
                # TODO warning log
                pass

            content = await get_body_from_streaming_response(response)
            response = Response(
                content,
                response.status_code,
                response.headers,
                response.media_type,
                response.background
            )

        await record_operation_log(request, response)

        return response
