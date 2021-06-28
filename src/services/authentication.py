from fastapi import Header, Security, Depends
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.requests import Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from models.errors import HttpForbidden
from services.config import get_default_config
from models.errors import HttpUnauthorized, EntityDoesNotExist
from db.crud.user import User as UserCRUD
from models.user import UserInDB
from services.localization import get_gettext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# curl "localhost:9394/api/v1/users" -H "Authorization: bearer <jwt-token>"
async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    _ = Depends(get_gettext),
) -> UserInDB:
    try:
        config = request.app.state.default_config
        pgpool = request.app.state.pgpool
        payload = jwt.decode(token, config['secret_key'], algorithms=[config['jwt_algorithm']])
        username: str = payload.get("username")
        if username is None:
            raise HttpUnauthorized(_("invalid access token"))
    except (jwt.JWTError, ValidationError):
        raise HttpUnauthorized(_("invalid access token"))

    user_crud = UserCRUD(pgpool)
    user = await user_crud.get_user_by_username(username=username)
    if user is None:
        raise HttpUnauthorized(_("invalid access token"))

    # set user to request context
    request.state.current_user = user

    return user


async def authenticate_user(pgpool, info, _):
    user_crud = UserCRUD(pgpool)

    user = None
    try:
        if info.username:
            user = await user_crud.get_user_by_username(username=info.username)

        if not user and info.email:
            user = await user_crud.get_user_by_email(email=info.email)
    except:
        pass

    if not user:
        raise HttpForbidden(_("invalid username or password"))

    if user.is_disabled():
        raise HttpForbidden(_("this user has been disabled"))

    if not user.check_password(info.password):
        raise HttpForbidden(_("invalid username or password"))

    return user


async def check_username_is_taken(pgpool, username: str) -> bool:
    user_crud = UserCRUD(pgpool)
    try:
        await user_crud.get_user_by_username(username=username)
    except EntityDoesNotExist:
        return False

    return True


async def check_email_is_taken(pgpool, email: str) -> bool:
    user_crud = UserCRUD(pgpool)

    try:
        await user_crud.get_user_by_email(email=email)
    except EntityDoesNotExist:
        return False

    return True