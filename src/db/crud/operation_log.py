from typing import Optional

from db.crud.base import Base
from db.queries import queries
from models.operation_log import OperationLogInDB
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound

class OperationLog(Base):

    async def get_oplog_by_owner(self, owner: int, offset: int, limit: int) -> list:
        record = await self.exec("count_oplog_by_owner", owner=owner)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        oplogs = list()

        records = await self.exec("get_oplog_by_owner", owner=owner, offset=offset, limit=limit)
        if record:
            oplogs = [OperationLogInDB(**record) for record in records]

        return oplogs, count

    async def add_oplog(self, op: str, path: str, new: dict, old: dict, owner: int, creator: int):
        # oplog = OperationLogInDB()
        record = await self.exec("add_oplog",
            op=op,
            path=path,
            new=new,
            old=old,
            owner=owner,
            creator=creator,
        )
        print("---add-oplog---: result = ", record)