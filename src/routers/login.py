from copy import deepcopy
from fastapi import APIRouter, Depends, Body, Request
from models.user import UserIn, UserOut, UserInDB, UserInResponse
from db.crud.users import Users as UserCRUD
from models.errors import HttpForbidden

router = APIRouter()

@router.post("/login", response_model=UserInResponse)
async def login(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user"),
) -> UserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)

    if info.username:
        user = await user_crud.get_user_by_username(username=info.username)

    if not user and info.email:
        user = await user_crud.get_user_by_email(email=info.email)

    if not user.check_password(info.password):
        raise HttpForbidden("invalid username or password")

    # TODO: create access token

    return UserInResponse(data=user)
