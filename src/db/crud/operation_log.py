from typing import Optional

from db.crud.base import Base
from db.queries import queries
from models.operation_log import OperationLogInDB
from models.errors import HttpServerError, HttpClientError, HttpForbidden, HttpNotFound


class OperationLog(Base):

    async def get_all(self, offset: int, limit: int) -> list:
        dbres = await self.exec("count_all_oplog")
        if not dbres or not dbres[0] or dbres[0][0] == 0:
            return list(), 0

        count = dbres[0][0]
        oplogs = list()

        records = await self.exec("get_all_oplog", offset=offset, limit=limit)
        if records:
            oplogs = [OperationLogInDB(**record) for record in records]

        return oplogs, count

    async def add_oplog(self, op: str, path: str, new: str, old: str, creator: int):
        # oplog = OperationLogInDB()
        await self.exec("add_oplog",
                        op=op,
                        path=path,
                        new=new,
                        old=old,
                        creator=creator,
                        )

    async def rollback(self, id: int, creator: int):
        # do rollback
        try:
            async with self._pool.acquire() as conn:
                async with conn.transaction():
                    records = await queries.get_oplog_gt_id(conn, id=id)
                    for record in records:
                        # do rollback
                        op = record[1]
                        if op == "PUT":
                            # update old
                            # TODO map queries method
                            pass
                        elif op == "POST":
                            # delete new
                            pass
                        elif op == "DELETE":
                            # add old
                            pass
                        else:
                            # error !
                            pass

                        # add op log

        except Exception as e:
            raise HttpServerError(str(e))
