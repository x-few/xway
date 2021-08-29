# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Path, Query, Body, Request
from starlette.status import HTTP_201_CREATED

from models.users import UserInCreate, \
    UserListInResponse, \
    UserInResponse, UserInUpdate
from db.crud.users import User as UserCRUD
from services.users import add_user as do_add_user
from models.errors import HttpClientError, HttpForbidden, HttpNotFound

router = APIRouter()


@router.get("/users", response_model=UserListInResponse)
async def list_user(
    request: Request,
    page: int = Query(1, ge=1, title="which page"),
    pagesize: int = Query(20, ge=1, le=100, title="Page size"),
) -> UserListInResponse:
    _ = request.state.get_gettext
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    offset = (page - 1) * pagesize
    user_crud = UserCRUD(request.app.state.pgpool)
    users, count = await user_crud.list_user(offset, pagesize)

    return UserListInResponse(data=users, count=count)


# curl localhost:9394/api/v1/users -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'
@router.post("/users",
             status_code=HTTP_201_CREATED,
             response_model=UserInResponse,
             )
async def add_user(
    request: Request,
    info: UserInCreate = Body(..., embed=True, alias="user"),
) -> UserInResponse:
    return await do_add_user(request, info)


@router.get("/users/{user_id}", response_model=UserInResponse,)
async def get_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
) -> UserInResponse:
    _ = request.state.get_gettext
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    if current_user.id == user_id:
        return current_user

    user_crud = UserCRUD(request.app.state.pgpool)
    target_user = await user_crud.get_user_by_id(user_id)
    if not target_user:
        raise HttpNotFound(_("user not found"))

    return target_user


@router.delete("/users/{user_id}",
               response_model=UserInResponse,
               )
async def delete_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
) -> UserInResponse:
    _ = request.state.get_gettext
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

    await user_crud.delete_user_by_id(user_id)
    return target_user


@router.put("/users/{user_id}", response_model=UserInResponse,)
async def update_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
    info: UserInUpdate = Body(..., embed=True, alias="user"),
) -> UserInResponse:
    _ = request.state.get_gettext
    current_user = request.state.current_user
    if not current_user:
        raise HttpNotFound(_("current user not found"))

    user_crud = UserCRUD(request.app.state.pgpool)
    target_user = await user_crud.get_user_by_id(user_id)
    if not target_user:
        raise HttpNotFound(_("user not found"))

    if info.username:
        temp_user = await user_crud.get_user_by_username(info.username)
        if temp_user and temp_user.id != target_user.id:
            raise HttpClientError(_("username already exists"))

    # password = target_user.password
    if info.password:
        # TODO Check if the password meets the requirements
        target_user.update_password(info.password)

    target_user.username = info.username or target_user.username
    target_user.email = info.email or target_user.email
    target_user.status = info.status or target_user.status

    user = await user_crud.update_user_by_id(
        id=user_id,
        user=target_user,
    )

    return user
