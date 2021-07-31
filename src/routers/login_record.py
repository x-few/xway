from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request

from db.crud.login_record import LoginRecord
from services.localization import get_gettext

router = APIRouter()

@router.post("/add_login_record")
async def add_login_record(
    request: Request,
    _ = Depends(get_gettext),
) -> None:
    print("---isshe---: add_login_record --1--")
    user = request.state.current_user

    login_record_crud = LoginRecord(request.app.state.pgpool)
    await login_record_crud.add_login_record(uid=user.id, host=request.client.host)
