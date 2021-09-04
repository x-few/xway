from datetime import datetime

from db.crud.base import Base
from utils.snowflake import get_id
from models.user_role import UserRoleInDB, \
    UserRoleInCreate, \
    UserRoleInUpdate


class UserRole(Base):
    async def list_user_roles(self, offset, limit) -> list:
        record = await self.exec("count_user_roles")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        user_roles = list()

        records = await self.exec("list_user_roles", offset=offset, limit=limit)
        if records:
            user_roles = [UserRoleInDB(**record) for record in records]

        return user_roles, count

    async def add_user_role(self, user_role: UserRoleInCreate
                            ) -> UserRoleInDB:
        record = await self.exec("add_user_role",
                                 id=get_id(),
                                 user_id=user_role.user_id,
                                 role_id=user_role.role_id,
                                 )

        return await self.get_user_role_by_id(record[0])

    async def get_user_role_by_id(self, id) -> UserRoleInDB:
        record = await self.exec("get_user_role_by_id", id)
        if record:
            return UserRoleInDB(**record)

        return None

    async def delete_user_role_by_id(self, id) -> None:
        return await self.exec("delete_user_role_by_id", id)

    async def update_user_role_by_id(self, id: int, user_role: UserRoleInUpdate
                                     ) -> datetime:
        record = await self.exec("update_user_role_by_id",
                                 id=id,
                                 user_id=user_role.user_id,
                                 role_id=user_role.role_id,
                                 )

        return record
