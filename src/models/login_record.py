from typing import Optional, List
from .base import Base, IDModel, DateTimeModel

# class LoginRecordToDB(Base):
#     uid: int
#     ip: Optional[str] = None


class LoginRecordInDB(DateTimeModel, IDModel):
    id: Optional[int] = None
    uid: int
    host: Optional[str] = None


class LoginRecordInResponse(LoginRecordInDB):
    """"""