from datetime import datetime

from db.crud.base import Base
from utils.snowflake import get_id
from models.role import RoleInDB, \
    RoleInCreate, \
    RoleInUpdate


class Role(Base):
    async def list_roles(self, offset, limit) -> list:
        record = await self.exec("count_roles")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        roles = list()

        records = await self.exec("list_roles", offset=offset, limit=limit)
        if records:
            roles = [RoleInDB(**record) for record in records]

        return roles, count

    async def add_role(self, role: RoleInCreate
                       ) -> RoleInDB:
        record = await self.exec("add_role",
                                 id=get_id(),
                                 name=role.name,
                                 description=role.description,
                                 )

        return await self.get_role_by_id(record[0])

    async def get_role_by_id(self, id) -> RoleInDB:
        record = await self.exec("get_role_by_id", id)
        if record:
            return RoleInDB(**record)

        return None

    async def delete_role_by_id(self, id) -> None:
        return await self.exec("delete_role_by_id", id)

    async def update_role_by_id(self, id: int, role: RoleInUpdate
                                ) -> datetime:
        record = await self.exec("update_role_by_id",
                                 id=id,
                                 name=role.name,
                                 description=role.description,
                                 )

        return record
