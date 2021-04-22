from fastapi import FastAPI
from typing import Callable
from services.database import connect_to_db
from services.config import get_default_config

def handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
        await get_default_config(app)
    return start_app