
from fastapi import FastAPI, Depends

from db.crud.config import Config as ConfigCRUD

async def get_default_config(app: FastAPI):
    pool = app.state.pgpool
    config_crud = ConfigCRUD(app.state.pgpool)
    app.state.default_config = await config_crud.get_all_default_config()
    print(app.state.default_config)
