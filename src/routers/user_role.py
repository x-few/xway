from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.user_role import UserRoleInCreate, \
    UserRoleListInResponse, \
    UserRoleInResponse, \
    UserRoleInUpdate
from db.crud.user_role import UserRole as UserRoleCRUD
from models.errors import HttpClientError, HttpNotFound

router = APIRouter()


@router.get("/user_roles", response_model=UserRoleListInResponse)
async def list_user_roles(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
) -> UserRoleListInResponse:
    _ = request.state.get_gettext
    offset = (page - 1) * pagesize
    user_role_crud = UserRoleCRUD(request.app.state.pgpool)
    user_roles, count = await user_role_crud.list_user_roles(offset, pagesize)

    return UserRoleListInResponse(data=user_roles, count=count)


@router.get("/user_role/{user_role_id}", response_model=UserRoleInResponse,)
async def get_user_role(
    request: Request,
    user_role_id: int = Path(..., title="The ID of the user_role"),
) -> UserRoleInResponse:
    _ = request.state.get_gettext
    user_role_crud = UserRoleCRUD(request.app.state.pgpool)
    target_user_role = await user_role_crud.get_user_role_by_id(user_role_id)
    if not target_user_role:
        raise HttpNotFound(_("user_role not found"))

    return target_user_role


@router.delete("/user_role/{user_role_id}",
               response_model=UserRoleInResponse,
               )
async def delete_user_role(
    request: Request,
    user_role_id: int = Path(..., title="The ID of the user_role"),
) -> UserRoleInResponse:
    _ = request.state.get_gettext
    user_role_crud = UserRoleCRUD(request.app.state.pgpool)
    target_user_role = await user_role_crud.get_user_role_by_id(user_role_id)
    if not target_user_role:
        raise HttpNotFound(_("user_role not found"))

    await user_role_crud.delete_user_role_by_id(user_role_id)
    return target_user_role


@router.post("/user_role",
             status_code=HTTP_201_CREATED,
             response_model=UserRoleInResponse,
             )
async def add_user_role(
    request: Request,
    info: UserRoleInCreate = Body(..., embed=True, alias="user_role"),
) -> UserRoleInResponse:
    _ = request.state.get_gettext
    if not info.user_id:
        raise HttpClientError(_("bad user_role user_id"))
    if not info.role_id:
        raise HttpClientError(_("bad user_role role_id"))

    user_role_crud = UserRoleCRUD(request.app.state.pgpool)
    return await user_role_crud.add_user_role(user_role=info)


@router.put("/user_role/{user_role_id}", response_model=UserRoleInResponse,)
async def update_user_role(
    request: Request,
    user_role_id: int = Path(..., title="The ID of the user_role"),
    info: UserRoleInUpdate = Body(..., embed=True, alias="user_role"),
) -> UserRoleInResponse:
    _ = request.state.get_gettext
    user_role_crud = UserRoleCRUD(request.app.state.pgpool)
    target_user_role = await user_role_crud.get_user_role_by_id(user_role_id)
    if not target_user_role:
        raise HttpNotFound(_("user_role not found"))

    target_user_role.user_id = info.user_id or target_user_role.user_id
    target_user_role.role_id = info.role_id or target_user_role.role_id

    updated = await user_role_crud.update_user_role_by_id(
        id=user_role_id,
        user_role=target_user_role,
    )

    target_user_role.updated = updated

    return target_user_role
