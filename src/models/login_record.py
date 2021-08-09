from typing import Optional, List
from .base import Base, IDModel, DateTimeModel

# class LoginRecordToDB(Base):
#     uid: int
#     ip: Optional[str] = None


class LoginRecordInDB(DateTimeModel, IDModel):
    id: Optional[int] = None
    host: Optional[str] = None
    type: Optional[int] = None
    token: Optional[str] = None
    creator: int


class LoginRecordInResponse(LoginRecordInDB):
    """"""

class LoginRecordListInResponse(Base):
    data: List[LoginRecordInDB]
    count: int
