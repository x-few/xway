from pydantic import EmailStr, BaseConfig, BaseModel
from typing import Optional, List


class LanguageInDB(BaseModel):
    name: str
    code: str
    domain: str
    localedir: str


class LanguagesInResponse(BaseModel):
    data: List[LanguageInDB]
