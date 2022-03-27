from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class UserGroupInCreate(Base):
    name: str
    creator: int
    description: str = ""
    creator: Optional[int] = None


class UserGroupInUpdate(Base):
    name: Optional[str] = None
    description: Optional[str] = None


class UserGroupInDB(UserGroupInCreate, IDModel, DateTimeModel):
    """UserGroupInDB"""


class UserGroupInResponse(UserGroupInDB):
    """UserGroupInResponse"""


class UserGroupListInResponse(Base):
    data: List[UserGroupInResponse]
    count: Optional[int] = None
