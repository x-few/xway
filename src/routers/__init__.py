from fastapi import Depends, APIRouter

from . import login, user, logout, language, operation_log
from services.authentication import get_current_user
from services.operation_log import init as init_oplog

def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1", tags=["login"])
    router.include_router(user.router, prefix="/v1", tags=["user"],
        dependencies=[Depends(get_current_user), Depends(init_oplog)],)
    router.include_router(language.router, prefix="/v1", tags=["language"],
        dependencies=[Depends(get_current_user)],)
    router.include_router(operation_log.router, prefix="/v1", tags=["operation_log"],
        dependencies=[Depends(get_current_user)],)
    router.include_router(logout.router, prefix="/v1", tags=["logout"],
        dependencies=[Depends(get_current_user)],)

    app.include_router(router, prefix="/api")
