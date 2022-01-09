from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class JWT(BaseModel):
    exp: datetime
    sub: str
    # alg: Optional[str] = "HS256"
    # iss: Optional[str] = None
    # iat: Optional[str] = None
    # nbf: Optional[str] = None
    # jti: Optional[str] = None
