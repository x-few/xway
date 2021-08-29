from fastapi import Depends, APIRouter

from . import login, users, logout, \
    language, operation_log, register, \
    login_log, permission
from . import role
from . import user_role
from . import role_permission
from . import login_log
# add import to here
from services.authentication import access_check
from services.operation_log import enable as enable_operation_log


def include_all_router(app):
    router = APIRouter()

    router.include_router(login.router, prefix="/v1", tags=["login"])
    router.include_router(language.router, prefix="/v1", tags=["language"],)
    router.include_router(register.router, prefix="/v1", tags=["register"],
                          dependencies=[Depends(enable_operation_log)],)
    router.include_router(login_log.router, prefix="/v1", tags=["login_log"],
                          dependencies=[Depends(access_check), ])
    router.include_router(permission.router, prefix="/v1", tags=["permission"],
                          dependencies=[Depends(access_check), ])
    router.include_router(operation_log.router, prefix="/v1", tags=["operation_log"],
                          dependencies=[Depends(access_check), ])
    router.include_router(logout.router, prefix="/v1", tags=["logout"],
                          dependencies=[Depends(access_check), ])
    router.include_router(users.router, prefix="/v1", tags=["users"],
                          dependencies=[Depends(access_check), Depends(enable_operation_log), ],)
    router.include_router(role.router, prefix="/v1", tags=["role"],
                          dependencies=[Depends(access_check), Depends(enable_operation_log), ],)
    router.include_router(user_role.router, prefix="/v1", tags=["user_role"],
                          dependencies=[Depends(access_check), Depends(enable_operation_log), ],)
    router.include_router(role_permission.router, prefix="/v1", tags=["role_permission"],
                          dependencies=[Depends(access_check), Depends(enable_operation_log), ],)
    # add router to here

    app.include_router(router, prefix="/api")
