from fastapi import FastAPI
from typing import Callable
from utils.database import connect_to_db


def handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
    return start_app