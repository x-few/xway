
from fastapi import FastAPI, Depends
from starlette.requests import Request
from db.crud.config import Config as ConfigCRUD


async def set_default_config(app: FastAPI):
    pool = app.state.pgpool
    config_crud = ConfigCRUD(app.state.pgpool)
    app.state.default_config = await config_crud.get_all_default_config()
    # print(app.state.default_config)

async def get_default_config(request: Request):
    return request.app.state.default_config
