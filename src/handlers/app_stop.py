from fastapi import FastAPI
from typing import Callable
from utils.database import close_db_connection

def handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app