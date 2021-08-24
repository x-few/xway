from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request, Query
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from models.login_record import LoginRecordInResponse, LoginRecordListInResponse
from db.crud.login_record import LoginRecord
from services.localization import get_gettext

from utils.const import AUTH_TYPES

router = APIRouter()


@router.post("/login_record",
             status_code=HTTP_201_CREATED,
             response_model=LoginRecordInResponse,
             )
async def add(
        request: Request,
        _=Depends(get_gettext),
) -> LoginRecordInResponse:
    user = request.state.current_user

    config = request.app.state.default_config
    token_type = config.get('jwt_token_prefix')
    token_type_value = AUTH_TYPES.get(token_type)

    login_record_crud = LoginRecord(request.app.state.pgpool)
    record = await login_record_crud.add_login_record(creator=user.id,
                                                      host=request.client.host, type=token_type_value, token="")

    return record


@router.get("/login_record",
            response_model=LoginRecordListInResponse,
            )
async def list(
        request: Request,
        page: int = Query(1, ge=1, title="which page"),
        pagesize: int = Query(20, ge=1, le=100, title="Page size"),
        _=Depends(get_gettext),
) -> LoginRecordListInResponse:
    user = request.state.current_user

    offset = (page - 1) * pagesize

    login_record_crud = LoginRecord(request.app.state.pgpool)
    records, count = await login_record_crud.list_login_record(
        creator=user.id, offset=offset, limit=pagesize)

    return LoginRecordListInResponse(data=records, count=count)
