# -*- coding: utf-8 -*-

from copy import deepcopy
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from models.user import UserInCreate, UserOut, ListOfUserInResponse, UserInResponse, UserInUpdate
from models.response import Response
from db.crud.user import User as UserCRUD
from services.localization import get_gettext
from services.user import add_user as do_add_user

SUB_USER = 2

router = APIRouter()

# FIXME: add owner to these api

@router.get("/users", response_model=ListOfUserInResponse)
async def get_all_users(
    request: Request,
    skip: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
    _ = Depends(get_gettext),
) -> ListOfUserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    users, count = await user_crud.get_all_user(skip, limit)

    return ListOfUserInResponse(data=users, count=count)


# @router.post("/owner_user",
#     status_code=HTTP_201_CREATED,
#     response_model=UserInResponse,
# )
# async def add_owner_user(
#     request: Request,
#     info: UserInCreate = Body(..., embed=True, alias="user")
# ) -> UserInResponse:
#     user = await do_add_user(request, info, 0)
#     return UserInResponse(
#         data=user
#     )


# curl localhost:9394/api/v1/user -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'
@router.post("/user",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
)
async def add_user(
    request: Request,
    info: UserInCreate = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
) -> UserInResponse:
    user = await do_add_user(request, info, SUB_USER, _)  # normal user, create by admin
    return UserInResponse(
        data=user
    )


@router.get("/user/{user_id}")
async def get_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
) -> UserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    user = await user_crud.get_user_by_id(user_id)

    # Note: user is a UserInDB instance, we should return UserOut() to user
    return UserInResponse(data=user)


@router.delete("/user/{user_id}", status_code=HTTP_204_NO_CONTENT,)
async def delele_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
) -> None:
    user_crud = UserCRUD(request.app.state.pgpool)
    await user_crud.delete_user_by_id(user_id)



@router.put("/user/{user_id}")
async def update_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
    info: UserInUpdate = Body(..., embed=True, alias="user")
) -> UserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    user = await user_crud.update_user_by_id(
        id=user_id,
        username=info.username,
        password=info.password,
        email=info.email,
        status=info.status,
    )

    return UserInResponse(data=user)
