from typing import Optional, List

from .base import Base, IDModel, DateTimeModel
from utils.const import PERMISSIONS_METHOD_ALL, PERMISSIONS_STATUS_ENABLE


class PermissionInCreate(Base):
    name: str
    uri: str
    description: str = ""
    method: int = PERMISSIONS_METHOD_ALL
    status: int = PERMISSIONS_STATUS_ENABLE
    creator: Optional[int] = None


class PermissionInUpdate(Base):
    name: Optional[str] = None
    uri: Optional[str] = None
    description: Optional[str] = None
    method: Optional[int] = None
    status: Optional[int] = None


class PermissionInDB(PermissionInCreate, IDModel, DateTimeModel):
    """PermissionInDB"""


class PermissionInResponse(PermissionInDB):
    """PermissionInResponse"""


class PermissionListInResponse(Base):
    data: List[PermissionInResponse]
    count: Optional[int] = None
