from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from models.login_record import LoginRecordInResponse
from db.crud.login_record import LoginRecord
from services.localization import get_gettext

router = APIRouter()

@router.post("/login_record", status_code=HTTP_201_CREATED,)
async def add_login_record(
    request: Request,
    _ = Depends(get_gettext),
) -> LoginRecordInResponse:
    user = request.state.current_user

    login_record_crud = LoginRecord(request.app.state.pgpool)
    record = await login_record_crud.add_login_record(uid=user.id, host=request.client.host)

    return record
