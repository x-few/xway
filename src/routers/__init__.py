from fastapi import Depends, APIRouter

from . import login, users, logout, \
    language, operation_log, register, \
    login_record, permission
from services.authentication import get_current_user
from services.operation_log import init as init_oplog


def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1", tags=["login"])
    router.include_router(register.router, prefix="/v1", tags=["register"],
                          dependencies=[Depends(init_oplog)],)
    router.include_router(login_record.router, prefix="/v1", tags=["login_record"],
                          dependencies=[Depends(get_current_user)],)
    router.include_router(permission.router, prefix="/v1", tags=["permission"],
                          dependencies=[Depends(get_current_user)],)
    router.include_router(users.router, prefix="/v1", tags=["users"],
                          dependencies=[Depends(get_current_user), Depends(init_oplog)],)
    router.include_router(language.router, prefix="/v1", tags=["language"],)
    router.include_router(operation_log.router, prefix="/v1", tags=["operation_log"],
                          dependencies=[Depends(get_current_user)],)
    router.include_router(logout.router, prefix="/v1", tags=["logout"],
                          dependencies=[Depends(get_current_user)],)

    app.include_router(router, prefix="/api")
