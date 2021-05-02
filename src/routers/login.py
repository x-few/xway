from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2

from models.user import UserIn
from db.crud.user import Users as UserCRUD
from models.errors import HttpForbidden
from services.jwt import create_access_token
from models.token import Token, TokenInResponse, \
    TokenWithUser, TokenWithUserInResponse
from services.authentication import authenticate_user
from services.localization import get_gettext

router = APIRouter()

@router.post("/login", response_model=TokenWithUserInResponse)
async def login(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
    # info: OAuth2PasswordRequestForm = Depends(),  # Use json instead
) -> TokenWithUserInResponse:

    user = await authenticate_user(request.app.state.pgpool, info, _)
    token = create_access_token(user, request.app.state.default_config)
    # print("token: ", token)

    return TokenWithUserInResponse(
        data=TokenWithUser(
            username=user.username,
            email=user.email,
            status=user.status,
            created=user.created,
            updated=user.updated,
            id=user.id,
            access_token=token,
            token_type="bearer",
        ),
    )


# curl "localhost/api/v1/token" -d 'username=username&password=password'
# curl "localhost/api/v1/token" -d '{"user":{"username":"username", "password": "password"}}'
@router.post("/token", response_model=TokenInResponse)
async def login_access_token(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user"),
    _ = Depends(get_gettext),
    # info: OAuth2PasswordRequestForm = Depends()   # Use json instead
) -> TokenInResponse:
    user = await authenticate_user(request.app.state.pgpool, info, _)
    token = create_access_token(user, request.app.state.default_config)
    return TokenInResponse(
        data=Token(
            access_token=token,
            token_type="bearer",
        ),
    )
