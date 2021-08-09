from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2

from models.users import UserInLogin, UserWithToken, UserWithTokenInResponse
from models.login_record import LoginRecordInDB
from db.crud.login_record import LoginRecord
from models.errors import HttpForbidden
from services.jwt import create_access_token
from models.token import Token, TokenInResponse
from services.authentication import authenticate_user
from services.localization import get_gettext
from utils.const import AUTH_TYPES

router = APIRouter()


async def do_login(request, info, _):
    pgpool = request.app.state.pgpool

    # TODO: support admin level config
    config = request.app.state.default_config

    user = await authenticate_user(pgpool, info, _)
    token = create_access_token(user, config)

    token_type = config.get('jwt_token_prefix')
    token_type_value = AUTH_TYPES.get(token_type)

    host = request.client.host

    login_record_crud = LoginRecord(pgpool)
    await login_record_crud.add(creator=user.id,
        host=host, type=token_type_value, token=token)

    return user, token, token_type


# TODO limit login rate
@router.post("/login", response_model=UserWithTokenInResponse)
async def login(
    request: Request,
    info: UserInLogin = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
    # info: OAuth2PasswordRequestForm = Depends(),  # Use json instead
) -> UserWithTokenInResponse:

    user, token, token_type = await do_login(request, info, _)

    return UserWithTokenInResponse(
        username=user.username,
        email=user.email,
        status=user.status,
        created=user.created,
        updated=user.updated,
        creator=user.creator,
        id=user.id,
        access_token=token,
        token_type=token_type,
    )


# curl "localhost/api/v1/token" -d 'username=username&password=password'
# curl "localhost/api/v1/token" -d '{"user":{"username":"username", "password": "password"}}'
@router.post("/token", response_model=Token)
async def login_access_token(
    request: Request,
    # info: UserInLogin = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
    info: OAuth2PasswordRequestForm = Depends()   # Use json instead
) -> Token:
    user, token, token_type = await do_login(request, info, _)

    return Token(
        access_token=token,
        token_type=token_type_key,
    )
