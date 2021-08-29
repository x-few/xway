from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class RolePermissionInCreate(Base):
    role_id: int
    permission_id: int


class RolePermissionInUpdate(Base):
    role_id: Optional[int] = None
    permission_id: Optional[int] = None


class RolePermissionInDB(RolePermissionInCreate, IDModel, DateTimeModel):
    """RolePermissionInDB"""


class RolePermissionInResponse(RolePermissionInDB):
    """RolePermissionInResponse"""


class RolePermissionListInResponse(Base):
    data: List[RolePermissionInResponse]
    count: Optional[int] = None
