from typing import Optional
from pydantic import EmailStr, BaseConfig, BaseModel


class Config(BaseModel):
    key: str
    value: str
    comment: Optional[str] = None
