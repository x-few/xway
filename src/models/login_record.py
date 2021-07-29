from typing import Optional, List
from .base import Base, IDModel, DateTimeModel

# class LoginRecordToDB(Base):
#     uid: int
#     ip: Optional[str] = None


class LoginRecordInDB(DateTimeModel, IDModel):
    uid: int
    host: Optional[str] = None


class LoginRecordInResponse(Base):
    data: LoginRecordInDB