from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security
from pydantic import EmailStr, BaseConfig, BaseModel

from db.crud.base import Base
from db.queries import queries
from models.users import UserInDB
from models.errors import EntityDoesNotExist

class User(Base):
    async def get_sub_users(self, uid, offset, limit) -> list:
        record = await self.exec("count_sub_users", uid=uid)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        users = list()

        records = await self.exec("get_sub_users", uid=uid, offset=offset, limit=limit)
        if records:
            users = [UserInDB(**record) for record in records]

        return users, count


    async def get_all_users(self, offset, limit) -> list:
        record = await self.exec("count_all_users", uid=uid)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        users = list()

        records = await self.exec("get_all_users", offset=offset, limit=limit)
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


    async def get_user_by_id_and_owner(self, id, owner) -> UserInDB:
        record = await self.exec("get_user_by_id_and_owner", id=id, owner=owner)
        if record:
            return UserInDB(**record)

        return None
        # raise EntityDoesNotExist("user does not exist, id: {0}, owner: {1}".format(id, owner))


    async def get_user_by_id(self, id) -> UserInDB:
        record = await self.exec("get_user_by_id", id)
        if record:
            return UserInDB(**record)

        return None
        # raise EntityDoesNotExist("user does not exist, id: {0}".format(id))


    async def get_user_by_username(self, username) -> UserInDB:
        record = await self.exec("get_user_by_username", username)
        if record:
            return UserInDB(**record)

        return None
        # raise EntityDoesNotExist("user does not exist, username: {0}".format(username))


    async def get_user_by_email(self, email) -> UserInDB:
        record = await self.exec("get_user_by_email", email)
        if record:
            return UserInDB(**record)

        return None
        # raise EntityDoesNotExist("user does not exist, email: {0}".format(email))


    async def delete_user_by_id(self, id) -> None:
        await self.exec("delete_user_by_id", id)


    async def update_user_by_id(self,
        id: int,
        user: UserInDB,
        # username: str,
        # password: str,
        # salt: str,
        # email: EmailStr,
        # status: int
    ) -> UserInDB:
        # user_in_db = await self.get_user_by_id(id=id)

        # user_in_db.username = username or user_in_db.username
        # user_in_db.email = email or user_in_db.email
        # user_in_db.status = status or user_in_db.status
        # if password:
        #     user_in_db.update_password(password)

        user.updated = await self.exec("update_user_by_id",
            id=id,
            username=user.username,
            email=user.email,
            salt=user.salt,
            password=user.password,
            status=user.status,
        )

        return user


