from datetime import datetime

from db.crud.base import Base
from utils.snowflake import get_id
from models.user_group import UserGroupInDB, \
    UserGroupInCreate, \
    UserGroupInUpdate


class UserGroup(Base):
    async def list_user_groups(self, offset: int, limit: int) -> list:
        record = await self.exec("count_user_groups")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        user_groups = list()

        records = await self.exec("list_user_groups", offset=offset, limit=limit)
        if records:
            user_groups = [UserGroupInDB(**record) for record in records]

        return user_groups, count

    async def add_user_group(self,
                             user_group: UserGroupInCreate
                             ) -> UserGroupInDB:
        record = await self.exec("add_user_group",
                                 id=get_id(),
                                 name=user_group.name,
                                 description=user_group.description,
                                 creator=user_group.creator,
                                 )

        return await self.get_user_group_by_id(record[0])

    async def get_user_group_by_id(self, id: int) -> UserGroupInDB:
        record = await self.exec("get_user_group_by_id", id)
        if record:
            return UserGroupInDB(**record)

        return None

    async def delete_user_group_by_id(self, id: int) -> None:
        return await self.exec("delete_user_group_by_id", id)

    async def update_user_group_by_id(self,
                                      id: int,
                                      user_group: UserGroupInUpdate
                                      ) -> datetime:
        record = await self.exec("update_user_group_by_id",
                                 id=id,
                                 name=user_group.name,
                                 description=user_group.description,
                                 )

        return record
