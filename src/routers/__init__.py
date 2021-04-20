from fastapi import Depends, APIRouter
from . import login, user, logout
from dependencies.authentication import get_token_header

def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1", tags=["login"])
    router.include_router(user.router, prefix="/v1", tags=["user"], dependencies=[Depends(get_token_header)],)
    router.include_router(logout.router, prefix="/v1", tags=["logout"], dependencies=[Depends(get_token_header)],)

    app.include_router(router, prefix="/api")
