from copy import deepcopy
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, Request
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from models.user import UserIn, UserOut, UserInDB, ListOfUserInResponse, UserInResponse
from db.crud.users import Users as UserCRUD

router = APIRouter()

@router.get("/users", response_model=ListOfUserInResponse,)
async def get_users(
    request: Request,
    offset: int = Query(0, ge=0, title="which page"),
    limit: int = Query(20, gt=0, le=100, title="Page size"),
) -> ListOfUserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    users, count = await user_crud.get_all_user(offset, limit)
    print("len(users) = ", len(users))

    return ListOfUserInResponse(data=users, count=count)


# curl localhost:9394/api/v1/user -XPOST -d '{"user":{"username": "abc", "password": "pwd"}}'
@router.post("/user",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
)
async def add_user(
    request: Request,
    info: UserIn = Body(..., embed=True, alias="user")
) -> UserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    user = await user_crud.add_user(info.username, info.password, info.email)

    # Note: user is a UserInDB instance, we should return UserOut() to user
    return UserInResponse(data=user)


@router.get("/user/{user_id}")
async def get_user(
    request: Request,
    user_id: int = Path(..., title="The ID of the user"),
) -> UserInResponse:
    user_crud = UserCRUD(request.app.state.pgpool)
    user = await user_crud.get_user_by_id(user_id)

    # Note: user is a UserInDB instance, we should return UserOut() to user
    return UserInResponse(data=user)


@router.put("/user/{user_id}")
async def edit_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "put user: {}".format(user_id)}


@router.delete("/user/{user_id}")
async def del_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "delete user: {}".format(user_id)}

