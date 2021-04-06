from copy import deepcopy
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/login")
async def login():
    return {"hello": "login"}

