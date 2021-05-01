from fastapi import Header, Security, Depends
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.requests import Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError

from services.config import get_default_config
from models.errors import HttpForbidden
from db.crud.users import Users as UserCRUD
from models.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme)
) -> UserInDB:
    try:
        config = request.app.state.default_config
        pgpool = request.app.state.pgpool
        payload = jwt.decode(token, config['secret_key'], algorithms=[config['jwt_algorithm']])
        username: str = payload.get("username")
        if username is None:
            raise HttpForbidden("username not found")
    except (jwt.JWTError, ValidationError):
        raise HttpForbidden("access token error")

    user_crud = UserCRUD(pgpool)
    user = await user_crud.get_user_by_username(username=username)
    if user is None:
        raise HttpForbidden("username not found")

    return user


async def get_token_header(request: Request):
    print("---get_token_header: request.method = ", request.method)
    # if x_token != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_token_header2(x_token: str = Header(...)):
    print("---get_token_header2---")
    # if x_token != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def get_query_token(token: str):
#     if token != "jessica":
#         raise HTTPException(status_code=400, detail="No Jessica token provided")