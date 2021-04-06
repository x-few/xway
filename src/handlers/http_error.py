from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

async def handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)