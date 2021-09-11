from typing import Optional

from db.crud.base import Base
from utils.snowflake import get_id
from models.users import UserInDB
from models.errors import HttpClientError


class User(Base):
    async def list_user(self, offset, limit) -> list:
        count = await self.exec("count_user")
        if not count:
            return list(), 0

        users = list()

        records = await self.exec("list_user", offset=offset, limit=limit)
        if records:
            users = [UserInDB(**record) for record in records]

        return users, count

    async def add_user(self,
                       username: str,
                       password: str,
                       email: Optional[str] = None,
                       status: Optional[int] = 1,
                       creator: Optional[int] = 0,
                       ) -> UserInDB:
        if not password or not username:
            raise HttpClientError("bad username or password")

        user = UserInDB(username=username, email=email,
                        status=status, creator=creator)
        user.update_password(password)
        record = await self.exec("add_user",
                                 id=get_id(),
                                 username=user.username,
                                 email=user.email,
                                 salt=user.salt,
                                 password=user.password,
                                 status=user.status,
                                 creator=user.creator,
                                 )

        return user.copy(update=dict(record))

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
        return await self.exec("delete_user_by_id", id)

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
