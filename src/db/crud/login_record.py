from typing import Optional
from starlette import status as slstatus
from fastapi import Depends, HTTPException, Security

from db.crud.base import Base
from db.queries import queries
from models.login_record import LoginRecordInDB
from models.errors import EntityDoesNotExist

class LoginRecord(Base):
    async def get_user_login_record(self, uid: int, offset: int, limit: int) -> list:
        record = await self.exec("count_user_login_record", uid=uid)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        res = list()

        records = await self.exec("get_all_login_record", offset=offset, limit=limit)
        if records:
            res = [LoginRecordInDB(**record) for record in records]

        return res, count


    async def count_user_login_record(self, uid: int) -> list:
        record = await self.exec("count_user_login_record", uid=uid)
        if not record or not record[0] or record[0][0] == 0:
            return 0

        return record[0][0]


    async def add_login_record(self, uid: int, host: str) -> int:
        record = await self.exec("add_login_record", uid=uid, host=host)

        # return id
        return record[0]
