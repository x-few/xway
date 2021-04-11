

from typing import Optional

from db.queries import queries
from db.crud.base import Base
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound
from models.user import UserFromDB

class Users(Base):
    async def get_all_user(self):
        try:
            records = await self.exec("get_all_user")
            return [UserFromDB(**record) for record in records]
        except Exception as e:
            raise HttpServerError(str(e))


    async def add_user(self,
        username: str,
        salt: str,
        password: str,
        email: Optional[str] = None,
        status: Optional[str] = "enable",
    ) -> UserFromDB:
        try:
            user = UserFromDB(username=username, email=email, status=status)
            record = await self.exec("add_user",
                username=username,
                email=email,
                salt=salt,
                password=password,
                status=status,
            )
            return user.copy(update=dict(record))
        except Exception as e:
            raise HttpServerError(str(e))
