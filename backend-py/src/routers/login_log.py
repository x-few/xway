from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.login_log import LoginLogInCreate, \
    LoginLogListInResponse, \
    LoginLogInResponse
from db.crud.login_log import LoginLog as LoginLogCRUD
from models.errors import HttpClientError, HttpNotFound

router = APIRouter()


@router.get("/login_logs", response_model=LoginLogListInResponse)
async def list_login_logs(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
) -> LoginLogListInResponse:
    _ = request.state.get_gettext
    current_user = request.state.current_user
    offset = (page - 1) * pagesize
    login_log_crud = LoginLogCRUD(request.app.state.pgpool)
    login_logs, count = await login_log_crud.list_login_logs(
        current_user.id, offset, pagesize)

    return LoginLogListInResponse(data=login_logs, count=count)


@router.get("/login_log/{login_log_id}", response_model=LoginLogInResponse,)
async def get_login_log(
    request: Request,
    login_log_id: int = Path(..., title="The ID of the login_log"),
) -> LoginLogInResponse:
    _ = request.state.get_gettext
    login_log_crud = LoginLogCRUD(request.app.state.pgpool)
    target_login_log = await login_log_crud.get_login_log_by_id(login_log_id)
    if not target_login_log:
        raise HttpNotFound(_("login_log not found"))

    return target_login_log


@router.delete("/login_log/{login_log_id}",
               response_model=LoginLogInResponse,
               )
async def delete_login_log(
    request: Request,
    login_log_id: int = Path(..., title="The ID of the login_log"),
) -> LoginLogInResponse:
    _ = request.state.get_gettext
    login_log_crud = LoginLogCRUD(request.app.state.pgpool)
    target_login_log = await login_log_crud.get_login_log_by_id(login_log_id)
    if not target_login_log:
        raise HttpNotFound(_("login_log not found"))

    await login_log_crud.delete_login_log_by_id(login_log_id)
    return target_login_log


@router.post("/login_log",
             status_code=HTTP_201_CREATED,
             response_model=LoginLogInResponse,
             )
async def add_login_log(
    request: Request,
    info: LoginLogInCreate = Body(..., embed=True, alias="login_log"),
) -> LoginLogInResponse:
    _ = request.state.get_gettext
    if not info.user_id:
        raise HttpClientError(_("bad login_log user_id"))
    if not info.status:
        raise HttpClientError(_("bad login_log status"))

    login_log_crud = LoginLogCRUD(request.app.state.pgpool)
    return await login_log_crud.add_login_log(login_log=info)
