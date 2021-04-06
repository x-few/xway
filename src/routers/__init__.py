from fastapi import Depends, APIRouter
from . import login, user
router = APIRouter()

router.include_router(login.router, prefix="/v1")
router.include_router(user.router, prefix="/v1")

# from ..depends import jwt_required
# from ..factory import app

# app.include_router(site.router)
# app.include_router(other.router, dependencies=[Depends(jwt_required)])
# app.include_router(rest.router, dependencies=[Depends(jwt_required)], prefix="/rest")
