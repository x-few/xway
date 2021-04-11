from fastapi import Depends, APIRouter
from . import login, user

def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1")
    router.include_router(user.router, prefix="/v1")

    app.include_router(router, prefix="/api")
