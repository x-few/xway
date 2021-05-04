from typing import Optional, List
from pydantic import EmailStr, BaseConfig, BaseModel
from .base import Base, IDModel, DateTimeModel
from services import security

class User(Base):
    username: str
    email: Optional[EmailStr] = None
    status: Optional[str] = "enable"


# from user
class UserInCreate(User):
    owner: Optional[int] = None
    password: str = ""


class UserInLogin(User):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# to user
class UserOut(User, IDModel, DateTimeModel):
    """UserOut"""
    creator: int
    owner: int


class UserInDB(UserOut):
    salt: str = ""
    password: str = ""

    def update_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.password = security.get_password_hash(self.salt + password)

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.password)

    def is_disabled(self) -> bool:
        if self.status == "enable":
            return False
        return True

class ListOfUserInResponse(Base):
    data: List[UserOut]
    count: int

class UserInResponse(Base):
    data: UserOut

class UserInJWT(Base):
    username: str

class UserWithToken(User):
    token: Optional[str] = None

class UserWithTokenInResponse(Base):
    data: UserWithToken

class UserInUpdate(Base):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    status: Optional[str] = None
