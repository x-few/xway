from datetime import datetime

from db.crud.base import Base
from models.permission import PermissionInDB, \
    PermissionInCreate, \
    PermissionInUpdate


class Permission(Base):
    async def list_permissions(self, offset, limit) -> list:
        record = await self.exec("count_permissions")
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        permissions = list()

        records = await self.exec("get_permissions", offset=offset, limit=limit)
        if records:
            permissions = [PermissionInDB(**record) for record in records]

        return permissions, count

    async def add_permission(self, permission: PermissionInCreate
                             ) -> PermissionInDB:
        record = await self.exec("add_permission",
                                 name=permission.name,
                                 uri=permission.uri,
                                 description=permission.description,
                                 method=permission.method,
                                 status=permission.status,
                                 )

        return record[0][0]     # id

    async def get_permission_by_id(self, id) -> PermissionInDB:
        record = await self.exec("get_permission_by_id", id)
        if record:
            return PermissionInDB(**record)

        return None

    async def delete_permission_by_id(self, id) -> None:
        return await self.exec("delete_permission_by_id", id)

    async def update_permission_by_id(self, id: int, permission: PermissionInUpdate
                                      ) -> datetime:
        record = await self.exec("update_permission_by_id",
                                 id=id,
                                 name=permission.name,
                                 uri=permission.uri,
                                 description=permission.description,
                                 method=permission.method,
                                 status=permission.status,
                                 )

        return record[0][0]     # updated
