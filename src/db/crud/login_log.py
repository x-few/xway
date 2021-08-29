from datetime import datetime

from db.crud.base import Base
from models.login_log import LoginRecordInDB, \
    LoginRecordInCreate


class LoginRecord(Base):
    async def list_login_logs(self, user_id: int, offset: int, limit: int) -> list:
        record = await self.exec("count_login_logs", user_id=user_id)
        if not record or not record[0] or record[0][0] == 0:
            return list(), 0

        count = record[0][0]
        login_logs = list()

        records = await self.exec("list_login_logs", user_id=user_id, offset=offset, limit=limit)
        if records:
            login_logs = [LoginRecordInDB(**record) for record in records]

        return login_logs, count

    async def add_login_log(self,
                            login_log: LoginRecordInCreate
                            ) -> LoginRecordInDB:
        record = await self.exec("add_login_log",
                                 user_id=login_log.user_id,
                                 host=login_log.host,
                                 type=login_log.type,
                                 status=login_log.status,
                                 )

        return await self.get_login_log_by_id(record[0])

    async def get_login_log_by_id(self, id: int) -> LoginRecordInDB:
        record = await self.exec("get_login_log_by_id", id)
        if record:
            return LoginRecordInDB(**record)

        return None

    async def delete_login_log_by_id(self, id: int) -> None:
        return await self.exec("delete_login_log_by_id", id)
