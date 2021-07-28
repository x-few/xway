from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.user import UserOut, UserInDB
from models.errors import EntityDoesNotExist

class Login(Base):
    async def get_all_login_record(self, uid, offset, limit) -> list:
        pass

    async def count_login_record(self, uid, offset, limit) -> list:
        pass

    async def add_login_record(self, uid, ip) -> None:
        pass
