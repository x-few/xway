from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.user import UserOut, UserInDB
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound

class Users(Base):
    async def get_all_user(self, offset, limit) -> list:
        record = await self.exec("count_users")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        users = list()

        records = await self.exec("get_all_user", offset=offset, limit=limit)
        print("records = ", records)
        if records:
            users = [UserOut(**record) for record in records]

        return users, count


    async def add_user(self,
        username: str,
        password: str,
        email: Optional[str] = None,
        status: Optional[str] = "enable",
    ) -> UserInDB:
        user = UserInDB(username=username, email=email, status=status)
        user.update_password(password)
        record = await self.exec("add_user",
            username=user.username,
            email=user.email,
            salt=user.salt,
            password=user.password,
            status=user.status,
        )

        return user.copy(update=dict(record))


    async def get_user_by_id(self, id) -> UserInDB:
        record = await self.exec("get_user_by_id", id)
        if record:
            return UserInDB(**record)

        raise HttpNotFound("user does not exist, id: {0}".format(id))


    async def get_user_by_username(self, username) -> UserInDB:
        record = await self.exec("get_user_by_username", username)
        if record:
            return UserInDB(**record)

        raise HttpNotFound("user does not exist, username: {0}".format(username))


    async def get_user_by_email(self, email) -> UserInDB:
        record = await self.exec("get_user_by_email", email)
        if record:
            return UserInDB(**record)

        raise HttpNotFound("user does not exist, email: {0}".format(email))
