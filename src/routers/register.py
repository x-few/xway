# -*- coding: utf-8 -*-

from fastapi import APIRouter, Body, Request
from starlette.status import HTTP_201_CREATED

from models.users import UserInCreate, UserInResponse
from services.users import add_user as do_add_user
from services.authentication import check_username_is_taken, check_email_is_taken
from models.errors import HttpClientError

router = APIRouter()

# curl localhost:9394/api/v1/register -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'


@router.post("/register",
             status_code=HTTP_201_CREATED,
             response_model=UserInResponse,
             )
async def register(
    request: Request,
    info: UserInCreate = Body(..., embed=True, alias="user"),
) -> UserInResponse:
    _ = request.state.get_gettext
    if await check_username_is_taken(request.app.state.pgpool, info.username):
        raise HttpClientError(_("user with this username already exists"))

    if await check_email_is_taken(request.app.state.pgpool, info.email):
        raise HttpClientError(_("user with this email already exists"))

    request.state.current_user = None
    user = await do_add_user(request, info)

    return user

    # token = create_access_token(user, request.app.state.default_config)
    # return UserWithTokenInResponse(
    #     data=UserWithToken(
    #         username=user.username,
    #         email=user.email,
    #         status=user.status,
    #         created=user.created,
    #         updated=user.updated,
    #         creator=user.creator,
    #         owner=user.owner,
    #         id=user.id,
    #         access_token=token,
    #         token_type="bearer",
    #         type=ADMIN_USER,
    #     ),
    # )
