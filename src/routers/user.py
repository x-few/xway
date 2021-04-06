from copy import deepcopy
from fastapi import APIRouter, Depends, Path, Query

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"hello": "users"}

@router.get("/user/{user_id}")
async def get_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "get user: {}".format(user_id)}

@router.post("/user/{user_id}")
async def add_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "post user: {}".format(user_id)}

@router.put("/user/{user_id}")
async def edit_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "put user: {}".format(user_id)}

@router.delete("/user/{user_id}")
async def del_user(user_id: int = Path(..., title="The ID of the user"),):
    return {"hello": "delete user: {}".format(user_id)}

