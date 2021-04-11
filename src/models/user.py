from typing import Optional, List
from pydantic import EmailStr, BaseConfig, BaseModel
from .common import IDModel, DateTimeModel
from .base import Base
from utils import security

class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    status: Optional[str] = "enable"


# from user
class UserIn(User):
    password: str = ""


# to user
class UserOut(User, IDModel, DateTimeModel):
    """UserOut"""


class UserInDB(User, IDModel, DateTimeModel):
    salt: str = ""
    password: str = ""

    def update_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.password = security.get_password_hash(self.salt + password)

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.password)


class ListOfUserInResponse(Base):
    data: List[UserOut]

class UserInResponse(Base):
    data: UserOut