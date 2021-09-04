from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.user_group import UserGroupInCreate, \
    UserGroupListInResponse, \
    UserGroupInResponse, \
    UserGroupInUpdate
from db.crud.user_group import UserGroup as UserGroupCRUD
from models.errors import HttpClientError, HttpNotFound

router = APIRouter()


@router.get("/user_groups", response_model=UserGroupListInResponse)
async def list_user_groups(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
) -> UserGroupListInResponse:
    _ = request.state.get_gettext
    offset = (page - 1) * pagesize
    user_group_crud = UserGroupCRUD(request.app.state.pgpool)
    user_groups, count = await user_group_crud.list_user_groups(offset, pagesize)

    return UserGroupListInResponse(data=user_groups, count=count)


@router.get("/user_group/{user_group_id}", response_model=UserGroupInResponse,)
async def get_user_group(
    request: Request,
    user_group_id: int = Path(..., title="The ID of the user_group"),
) -> UserGroupInResponse:
    _ = request.state.get_gettext
    user_group_crud = UserGroupCRUD(request.app.state.pgpool)
    target_user_group = await user_group_crud.get_user_group_by_id(user_group_id)
    if not target_user_group:
        raise HttpNotFound(_("user_group not found"))

    return target_user_group


@router.delete("/user_group/{user_group_id}",
               response_model=UserGroupInResponse,
               )
async def delete_user_group(
    request: Request,
    user_group_id: int = Path(..., title="The ID of the user_group"),
) -> UserGroupInResponse:
    _ = request.state.get_gettext
    user_group_crud = UserGroupCRUD(request.app.state.pgpool)
    target_user_group = await user_group_crud.get_user_group_by_id(user_group_id)
    if not target_user_group:
        raise HttpNotFound(_("user_group not found"))

    await user_group_crud.delete_user_group_by_id(user_group_id)
    return target_user_group


@router.post("/user_group",
             status_code=HTTP_201_CREATED,
             response_model=UserGroupInResponse,
             )
async def add_user_group(
    request: Request,
    info: UserGroupInCreate = Body(..., embed=True, alias="user_group"),
) -> UserGroupInResponse:
    _ = request.state.get_gettext
    if not info.name:
        raise HttpClientError(_("bad user_group name"))
    if not info.creator:
        raise HttpClientError(_("bad user_group creator"))
    info.creator = request.state.current_user.id
    user_group_crud = UserGroupCRUD(request.app.state.pgpool)
    return await user_group_crud.add_user_group(user_group=info)


@router.put("/user_group/{user_group_id}", response_model=UserGroupInResponse,)
async def update_user_group(
    request: Request,
    user_group_id: int = Path(..., title="The ID of the user_group"),
    info: UserGroupInUpdate = Body(..., embed=True, alias="user_group"),
) -> UserGroupInResponse:
    _ = request.state.get_gettext
    user_group_crud = UserGroupCRUD(request.app.state.pgpool)
    target_user_group = await user_group_crud.get_user_group_by_id(user_group_id)
    if not target_user_group:
        raise HttpNotFound(_("user_group not found"))

    target_user_group.name = info.name or target_user_group.name
    target_user_group.description = info.description or target_user_group.description

    updated = await user_group_crud.update_user_group_by_id(
        id=user_group_id,
        user_group=target_user_group,
    )

    target_user_group.updated = updated

    return target_user_group
