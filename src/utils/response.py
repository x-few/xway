

from starlette.responses import JSONResponse
from starlette import status
from fastapi.encoders import jsonable_encoder

def Response(data, status=200) -> JSONResponse:
    json_data = jsonable_encoder(data)
    if not isinstance(data, list):
        json_data = [json_data]
    return JSONResponse({"data": json_data}, status_code=status)
