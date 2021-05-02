from pydantic import EmailStr, BaseConfig, BaseModel
from typing import Optional

from .user import UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenWithUser(Token, UserOut):
    """Token with User"""


class TokenWithUserInResponse(BaseModel):
    data: TokenWithUser

class TokenInResponse(BaseModel):
    data: Token