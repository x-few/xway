from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class LoginRecordInCreate(Base):
    user_id: int
    status: int
    host: str = ""
    type: int = 0


class LoginRecordInDB(LoginRecordInCreate, IDModel, DateTimeModel):
    """LoginRecordInDB"""


class LoginRecordInResponse(LoginRecordInDB):
    """LoginRecordInResponse"""


class LoginRecordListInResponse(Base):
    data: List[LoginRecordInResponse]
    count: Optional[int] = None
