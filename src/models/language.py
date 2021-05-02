from pydantic import EmailStr, BaseConfig, BaseModel
from typing import Optional


class LanguageInDB(BaseModel):
    name: str
    code: str
    domain: str
    localedir: str
