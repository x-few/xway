from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2

from models.user import UserIn, UserWithToken, UserWithTokenInResponse
from db.crud.users import Users as UserCRUD
from models.errors import HttpForbidden
from services.jwt import create_access_token
from models.token import Token

router = APIRouter()

async def authenticate_user(pgpool, info):
    user_crud = UserCRUD(pgpool)

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

    return user

@router.post("/login", response_model=UserWithTokenInResponse)
async def login(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user"),
) -> UserWithTokenInResponse:

    user = authenticate_user(request.app.state.pgpool, info)
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

# curl "localhost/api/v1/token" -d 'username=username&password=password'
@router.post("/token", response_model=Token)
async def login_access_token(
    request: Request,
    info: OAuth2PasswordRequestForm = Depends()
):
    print("info = ", info)
    print("info.usrname = ", info.username)
    user = await authenticate_user(request.app.state.pgpool, info)
    token = create_access_token(user, request.app.state.default_config)
    return {"access_token": token, "token_type": "bearer"}
