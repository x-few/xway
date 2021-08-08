from typing import Optional, List
from pydantic import EmailStr, BaseConfig, BaseModel
from .base import Base, IDModel, DateTimeModel
from .token import Token
from services import security
from utils.const import USER_STATUS_ENABLED

class User(Base):
    username: str
    email: Optional[EmailStr] = None
    status: Optional[int] = 1


# from user
class UserInCreate(User):
    password: str = ""


class UserInLogin(Base):
    username: Optional[str] = None
    password: Optional[str] = None


# to user
class UserInResponse(User, IDModel, DateTimeModel):
    """UserInResponse"""
    creator: int
    # salt: str = None
    # password: str = None


class UserInDB(UserInResponse):
    salt: str = ""
    password: str = ""  # hashed

    def update_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.password = security.get_password_hash(self.salt + password)

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.password)

    def is_disabled(self) -> bool:
        if self.status == USER_STATUS_ENABLED:
            return False
        return True

class UserListInResponse(Base):
    data: List[UserInResponse]
    count: int

class UserInJWT(Base):
    username: str

class UserWithToken(UserInResponse, Token):
    """UserWithToken"""

class UserWithTokenInResponse(UserWithToken):
    """"""

class UserInUpdate(Base):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[int] = None
