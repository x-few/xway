from fastapi import Depends, APIRouter
from . import login, user, logout
from services.authentication import get_current_user

def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1", tags=["login"])
    router.include_router(user.router, prefix="/v1", tags=["user"],
        dependencies=[Depends(get_current_user)],)
    router.include_router(logout.router, prefix="/v1", tags=["logout"],
        dependencies=[Depends(get_current_user)],)

    app.include_router(router, prefix="/api")
