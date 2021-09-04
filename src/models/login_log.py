from typing import Optional, List

from .base import Base, IDModel, DateTimeModel


class LoginLogInCreate(Base):
    user_id: int
    status: int
    host: str = ""
    type: int = 0


class LoginLogInDB(LoginLogInCreate, IDModel, DateTimeModel):
    """LoginLogInDB"""


class LoginLogInResponse(LoginLogInDB):
    """LoginLogInResponse"""


class LoginLogListInResponse(Base):
    data: List[LoginLogInResponse]
    count: Optional[int] = None
