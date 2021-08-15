from fastapi import FastAPI
from typing import Callable
from services.database import connect_to_db
from services.config import set_default_config
from services.localization import init_translation_object


def handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
        await set_default_config(app)
        await init_translation_object(app)
    return start_app
