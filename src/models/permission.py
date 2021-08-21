from typing import Optional, List

from .base import Base, IDModel, DateTimeModel
from utils.const import PERMISSIONS_METHOD_ALL, PERMISSIONS_STATUS_ENABLE


class PermissionInCreate(Base):
    name: str
    uri: str
    desc: Optional[str] = None
    method: Optional[int] = PERMISSIONS_METHOD_ALL
    status: Optional[int] = PERMISSIONS_STATUS_ENABLE


class PermissionInUpdate(PermissionInCreate):
    """PermissionInUpdate"""


class PermissionInDB(PermissionInCreate, IDModel, DateTimeModel):
    """PermissionInDB"""


class PermissionInResponse(PermissionInDB):
    """PermissionInResponse"""


class PermissionListInResponse(Base):
    data: List[PermissionInResponse]
    count: Optional[int] = None
