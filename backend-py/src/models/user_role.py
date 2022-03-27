from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class UserRoleInCreate(Base):
    user_id: int
    role_id: int


class UserRoleInUpdate(Base):
    user_id: Optional[int] = None
    role_id: Optional[int] = None


class UserRoleInDB(UserRoleInCreate, IDModel, DateTimeModel):
    """UserRoleInDB"""


class UserRoleInResponse(UserRoleInDB):
    """UserRoleInResponse"""


class UserRoleListInResponse(Base):
    data: List[UserRoleInResponse]
    count: Optional[int] = None
