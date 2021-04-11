from copy import deepcopy
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from models.user import UserIn, UserFromDB
from db.crud.users import Users as UserCRUD
from utils.response import Response

router = APIRouter()

@router.get("/users")
async def get_users(request: Request,):
    user_crud = UserCRUD(request.app.state.pgpool)
    users = await user_crud.get_all_user()
    print(type(users), users)
    return Response(users)


# curl localhost:9394/api/v1/user -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'
@router.post("/user",
    status_code=HTTP_201_CREATED,
    # response_model=Response,
)
async def add_user(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user")
):
    user_crud = UserCRUD(request.app.state.pgpool)
    # TODO generate salt and hash pwd
    user = await user_crud.add_user(info.username, "salt", info.password, info.email, )
    print(type(user), user)
    return Response(user)

@router.get("/user/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "get user: {}".format(user_id)}

@router.put("/user/{user_id}")
async def edit_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "put user: {}".format(user_id)}

@router.delete("/user/{user_id}")
async def del_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "delete user: {}".format(user_id)}

