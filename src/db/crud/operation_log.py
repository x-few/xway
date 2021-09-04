from typing import Optional

from utils.snowflake import get_id
from db.crud.base import Base
from models.operation_log import OperationLogInDB


class OperationLog(Base):
    async def list_operation_log(self, offset: int, limit: int) -> list:
        res = await self.exec("count_operation_log")
        if not res or not res[0] or res[0][0] == 0:
            return list(), 0

        count = res[0][0]
        operation_logs = list()

        records = await self.exec("list_operation_log",
                                  offset=offset, limit=limit)
        if records:
            operation_logs = [OperationLogInDB(**record) for record in records]

        return operation_logs, count

    async def add_operation_log(self, op: str, path: str,
                                new: str, old: str, creator: int):
        # oplog = OperationLogInDB()
        await self.exec("add_operation_log",
                        id=get_id(),
                        op=op,
                        path=path,
                        new=new,
                        old=old,
                        creator=creator,
                        )
