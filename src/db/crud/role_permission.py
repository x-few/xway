from datetime import datetime

from db.crud.base import Base
from utils.snowflake import get_id
from models.role_permission import RolePermissionInDB, \
    RolePermissionInCreate, \
    RolePermissionInUpdate


class RolePermission(Base):
    async def list_role_permissions(self, offset: int, limit: int) -> list:
        record = await self.exec("count_role_permissions")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        role_permissions = list()

        records = await self.exec("list_role_permissions", offset=offset, limit=limit)
        if records:
            role_permissions = [RolePermissionInDB(
                **record) for record in records]

        return role_permissions, count

    async def add_role_permission(self,
                                  role_permission: RolePermissionInCreate
                                  ) -> RolePermissionInDB:
        record = await self.exec("add_role_permission",
                                 id=get_id(),
                                 role_id=role_permission.role_id,
                                 permission_id=role_permission.permission_id,
                                 )

        return await self.get_role_permission_by_id(record[0])

    async def get_role_permission_by_id(self, id: int) -> RolePermissionInDB:
        record = await self.exec("get_role_permission_by_id", id)
        if record:
            return RolePermissionInDB(**record)

        return None

    async def delete_role_permission_by_id(self, id: int) -> None:
        return await self.exec("delete_role_permission_by_id", id)

    async def update_role_permission_by_id(self,
                                           id: int,
                                           role_permission: RolePermissionInUpdate
                                           ) -> datetime:
        record = await self.exec("update_role_permission_by_id",
                                 id=id,
                                 role_id=role_permission.role_id,
                                 permission_id=role_permission.permission_id,
                                 )

        return record
