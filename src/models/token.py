from pydantic import EmailStr, BaseConfig, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str