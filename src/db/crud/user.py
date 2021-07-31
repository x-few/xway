from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.user import UserInDB
from models.errors import EntityDoesNotExist

class User(Base):
    async def get_all_user(self, offset, limit) -> list:
        record = await self.exec("count_users")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        users = list()

        records = await self.exec("get_all_user", offset=offset, limit=limit)
        # print("records = ", records)
        if records:
            users = [UserInDB(**record) for record in records]

        return users, count


    async def add_user(self,
        username: str,
        password: str,
        creator: int,
        owner: int,
        type: int,
        email: Optional[str] = None,
        status: Optional[int] = 1,
    ) -> UserInDB:

        user = UserInDB(username=username, email=email, status=status, creator=creator, owner=owner, type=type)
        user.update_password(password)
        record = await self.exec("add_user",
            username=user.username,
            email=user.email,
            salt=user.salt,
            password=user.password,
            status=user.status,
            creator=user.creator,
            owner=user.owner,
            type=user.type
        )

        return user.copy(update=dict(record))


    async def get_user_by_id(self, id) -> UserInDB:
        record = await self.exec("get_user_by_id", id)
        if record:
            return UserInDB(**record)

        raise EntityDoesNotExist("user does not exist, id: {0}".format(id))


    async def get_user_by_username(self, username) -> UserInDB:
        record = await self.exec("get_user_by_username", username)
        if record:
            return UserInDB(**record)

        raise EntityDoesNotExist("user does not exist, username: {0}".format(username))


    async def get_user_by_email(self, email) -> UserInDB:
        record = await self.exec("get_user_by_email", email)
        if record:
            return UserInDB(**record)

        raise EntityDoesNotExist("user does not exist, email: {0}".format(email))


    async def delete_user_by_id(self, id) -> None:
        await self.exec("delete_user_by_id", id)


    async def update_user_by_id(self,
        id: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[str] = None,
    ) -> UserInDB:
        user_in_db = await self.get_user_by_id(id=id)

        user_in_db.username = username or user_in_db.username
        user_in_db.email = email or user_in_db.email
        user_in_db.status = status or user_in_db.status
        if password:
            user_in_db.update_password(password)

        user_in_db.updated = await self.exec("update_user_by_id",
            id=id,
            username=user_in_db.username,
            email=user_in_db.email,
            salt=user_in_db.salt,
            password=user_in_db.password,
            status=user_in_db.status,
        )

        return user_in_db


