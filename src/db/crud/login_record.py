from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.login_record import LoginRecordInDB
from models.errors import EntityDoesNotExist


class LoginRecord(Base):
    async def list(self, creator: int, offset: int, limit: int) -> list:
        record = await self.exec("count_login_record", creator=creator)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        res = list()

        records = await self.exec("list_login_record", creator=creator, offset=offset, limit=limit)
        if records:
            res = [LoginRecordInDB(**record) for record in records]

        return res, count

    async def count(self, creator: int) -> list:
        record = await self.exec("count_login_record", creator=creator)
        if not record or not record[0] or record[0][0] == 0:
            return 0

        return record[0][0]

    async def add(self, creator: int, host: str, type: int, token: str) -> int:
        record = await self.exec("add_login_record",
                                 creator=creator, host=host, type=type, token=token)

        # return id
        return LoginRecordInDB(id=record[0], creator=creator, host=host)
