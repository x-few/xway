from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class PermissionInCreate(Base):
    name: str
    uri: str
    description: str = ""
    method: int = PERMISSIONS_METHOD_ALL
    status: int = PERMISSIONS_STATUS_ENABLE


class PermissionInUpdate(PermissionInCreate):
    """PermissionInUpdate"""


class PermissionInDB(PermissionInCreate, IDModel, DateTimeModel):
    """PermissionInDB"""


class PermissionInResponse(PermissionInDB):
    """PermissionInResponse"""


class PermissionListInResponse(Base):
    data: List[PermissionInResponse]
    count: Optional[int] = None
