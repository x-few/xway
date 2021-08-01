# -*- coding: utf-8 -*-

from copy import deepcopy
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from typing import Optional

from models.users import UserInCreate, ListOfUserInResponse, UserInResponse, UserInUpdate
from models.response import Response
from db.crud.users import User as UserCRUD
from services.localization import get_gettext
from services.users import add_user as do_add_user, get_owner
from models.errors import HttpClientError, HttpForbidden, HttpServerError, HttpNotFound
from utils.const import is_system_maintainer, is_admin_user, is_normal_user, \
    get_user_type_normal_user, get_user_type_system_maintainer, get_user_type_admin_user

router = APIRouter()

# FIXME: add owner to these api

@router.get("/users", response_model=ListOfUserInResponse)
async def get_users(
    request: Request,
    skip: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _ = Depends(get_gettext),
) -> ListOfUserInResponse:
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    owner = await get_owner(current_user)
    user_type = current_user.type

    users = None
    count = 0

    user_crud = UserCRUD(request.app.state.pgpool)
    if is_admin_user(user_type) or is_normal_user(user_type):
        users, count = await user_crud.get_sub_users(owner, skip, limit)
    elif is_system_maintainer(user_type):
        # admin, can delete any user
        users, count = await user_crud.get_all_users(skip, limit)
    else:
        raise HttpServerError()

    return ListOfUserInResponse(data=users, count=count)


# curl localhost:9394/api/v1/users -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'
@router.post("/users",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
)
async def add_user(
    request: Request,
    info: UserInCreate = Body(..., embed=True, alias="user"),
    user_type: Optional[int] = get_user_type_normal_user(),
    _ = Depends(get_gettext),
) -> UserInResponse:
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    owner = await get_owner(current_user)
    current_user_type = current_user.type

    user = None

    user_crud = UserCRUD(request.app.state.pgpool)
    if is_admin_user(current_user_type) or is_normal_user(current_user_type):
        user = await do_add_user(request, info, get_user_type_normal_user(), _)
    elif is_system_maintainer(current_user_type):
        if is_normal_user(user_type):
            # admin, can not add sub-user
            raise HttpClientError(_("bad user type"))

        user = await do_add_user(request, info, user_type, _)
    else:
        raise HttpServerError()

    return user


@router.get("/users/{user_id}", response_model=UserInResponse,)
async def get_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
    _ = Depends(get_gettext),
) -> UserInResponse:
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    if current_user.id == user_id:
        return current_user

    user_crud = UserCRUD(request.app.state.pgpool)
    target_user = await user_crud.get_user_by_id(user_id)
    if not target_user:
        raise HttpNotFound(_("user not found"))

    user_type = current_user.type
    if not (is_system_maintainer(user_type) and is_admin_user(target_user.type)):
        current_owner = await get_owner(current_user)
        target_owner = await get_owner(target_user)
        if current_owner != target_owner:
            raise HttpNotFound(_("user not found"))

    return target_user



@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT,)
async def delete_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
    _ = Depends(get_gettext),
) -> None:
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    if user_id == current_user.id:
        # can not delete myself
        raise HttpForbidden(_("not allowed delete current user"))

    user_crud = UserCRUD(request.app.state.pgpool)
    target_user = await user_crud.get_user_by_id(user_id)
    if not target_user:
        raise HttpNotFound(_("user not found"))

    user_type = current_user.type
    if not (is_system_maintainer(user_type) and is_admin_user(target_user.type)):
        current_owner = await get_owner(current_user)
        target_owner = await get_owner(target_user)
        if current_owner != target_owner:
            raise HttpNotFound(_("user not found"))

    await user_crud.delete_user_by_id(user_id)
    return None


@router.put("/users/{user_id}", response_model=UserInResponse,)
async def update_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
    info: UserInUpdate = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
) -> UserInResponse:
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    user_crud = UserCRUD(request.app.state.pgpool)
    target_user = await user_crud.get_user_by_id(user_id)
    if not target_user:
        raise HttpNotFound(_("user not found"))

    user_type = current_user.type
    if not (is_system_maintainer(user_type) and is_admin_user(target_user.type)):
        current_owner = await get_owner(current_user)
        target_owner = await get_owner(target_user)
        if current_owner != target_owner:
            raise HttpNotFound(_("user not found"))

    password = target_user.password
    if info.password:
        # TODO Check if the password meets the requirements
        target_user.update_password(info.password)

    target_user.username = info.username or target_user.username
    target_user.email = info.email or target_user.email
    target_user.status = info.status or target_user.status
    # target_user.status = info.type,   # unsupported

    user = await user_crud.update_user_by_id(
        id=user_id,
        user=target_user,
    )

    return user
