

from typing import Optional

from db.queries import queries
from db.crud.base import Base
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound
from models.user import UserFromDB

class Users(Base):
    async def get_all_user(self):
        records = await self.exec("get_all_user")
        if records:
            return [UserFromDB(**record) for record in records]

        # empty
        return list()


    async def add_user(self,
        username: str,
        salt: str,
        password: str,
        email: Optional[str] = None,
        status: Optional[str] = "enable",
    ) -> UserFromDB:
        user = UserFromDB(username=username, email=email, status=status)
        record = await self.exec("add_user",
            username=username,
            email=email,
            salt=salt,
            password=password,
            status=status,
        )
        return user.copy(update=dict(record))

    async def get_user_by_id(self, id) -> UserFromDB:
        record = await self.exec("get_user_by_id", id)
        if record:
            return UserFromDB(**record)

        raise HttpNotFound("user does not exist, id: {0}".format(id))