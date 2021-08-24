from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class RoleInCreate(Base):
    name: str
    description: str = ""


class RoleInUpdate(Base):
    name: Optional[str] = None
    description: Optional[str] = None


class RoleInDB(RoleInCreate, IDModel, DateTimeModel):
    """RoleInDB"""


class RoleInResponse(RoleInDB):
    """RoleInResponse"""


class RoleListInResponse(Base):
    data: List[RoleInResponse]
    count: Optional[int] = None
