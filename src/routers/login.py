from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from models.user import UserIn, UserWithToken, UserWithTokenInResponse
from db.crud.users import Users as UserCRUD
from models.errors import HttpForbidden
from services.jwt import create_access_token

router = APIRouter()

@router.post("/login", response_model=UserWithTokenInResponse)
async def login(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user"),
) -> UserWithTokenInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)

    if info.username:
        user = await user_crud.get_user_by_username(username=info.username)

    if not user and info.email:
        user = await user_crud.get_user_by_email(email=info.email)

    if not user:
        raise HttpForbidden("invalid username or password")

    if user.is_disabled():
        raise HttpForbidden("this user has been disabled")

    if not user.check_password(info.password):
        raise HttpForbidden("invalid username or password")

    token = create_access_token(user, request.app.state.default_config)

    print("token: ", token)

    return UserWithTokenInResponse(
        data=UserWithToken(
            username=user.username,
            email=user.email,
            status=user.status,
            created=user.created,
            updated=user.updated,
            id=user.id,
            token=token,
        ),
    )
