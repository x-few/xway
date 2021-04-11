from typing import Optional, List
from pydantic import EmailStr, BaseConfig, BaseModel
from .common import IDModel, DateTimeModel
from .base import Base

class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    status: Optional[str] = "enable"


# from user
class UserIn(User):
    password: str = ""


# to user
class UserOut(User):
    """UserOut"""


class UserToDB(User):
    salt: str = ""
    password: str = ""


class UserFromDB(User, IDModel, DateTimeModel):
    """UserFromDB"""
    # salt: str = ""
    # password: str = ""

class ListOfUserInResponse(Base):
    data: List[UserFromDB]

class UserInResponse(Base):
    data: UserFromDB
