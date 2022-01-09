from pydantic import EmailStr, BaseConfig, BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenInResponse(BaseModel):
    data: Token
