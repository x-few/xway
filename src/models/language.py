from pydantic import EmailStr, BaseConfig, BaseModel
from typing import Optional, List

class LanguageInDB(BaseModel):
    name: str
    code: str
    domain: str
    localedir: str

class LanguageInResponse(BaseModel):
    data: List[LanguageInDB]
