from typing import Optional, List
from .base import Base, IDModel, DateTimeModel
from pydantic import BaseModel

class OperationLog(BaseModel):
    op: str
    path: str
    new: Optional[str] = None
    old: Optional[str] = None
    creator: int


class OperationLogInDB(OperationLog, IDModel, DateTimeModel):
    """OperationLogInDB"""


class ListOfOperationLogInResponse(Base):
    data: List[OperationLogInDB]
    count: int
