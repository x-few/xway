from asyncpg.connection import Connection
from asyncpg.pool import Pool
from db.queries import queries
from models.errors import HttpServerError

class Base:
    def __init__(self, pool: Pool) -> None:
        self._pool = pool

    @property
    def pool(self) -> Pool:
        return self._pool

    async def exec(self, name, *args, **kwargs):
        try:
            async with self._pool.acquire() as conn:
                async with conn.transaction():
                    func = getattr(queries, name)
                    return await func(conn, *args, **kwargs)
        except Exception as e:
            func = getattr(queries, name)
            print(func.sql)
            raise HttpServerError(str(e))
