# -*- coding: utf-8 -*-

import uuid
import warnings
import os
import sys
import random
import pytest
import alembic.config
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from typing import Any

# CURPATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.insert(0, CURPATH)

from models.users import UserInDB
from services.jwt import create_access_token
from db.crud.users import User as UserCRUD

DEFAULT_BASE_URL = "http://testxway.com"
DEFAULT_HEADERS = {"Content-Type": "application/json"}


def random_value(type) -> Any:
    if type == "int":
        return random.randint(1, 100000000)
    elif type == "str":
        return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6))
    else:
        return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6))


@pytest.fixture(autouse=True)
async def init_db() -> None:
    # before test, init db
    # clean
    alembic.config.main(argv=["downgrade", "base"])
    # init
    alembic.config.main(argv=["upgrade", "head"])
    yield
    # after test, clean db
    # clean
    # alembic.config.main(argv=["downgrade", "base"])
    # reinit for dev
    # alembic.config.main(argv=["upgrade", "head"])


@pytest.fixture
async def app(init_db: None) -> FastAPI:
    from xway import application  # local import for testing purpose

    app = application()
    async with LifespanManager(app):
        yield app
    # return application()


@pytest.fixture
def pool(app: FastAPI) -> Pool:
    return app.state.pgpool


@pytest.fixture
def default_config(app: FastAPI) -> Pool:
    return app.state.default_config


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url=DEFAULT_BASE_URL,
        headers=DEFAULT_HEADERS,
    ) as client:
        yield client


@pytest.fixture
def authorization_prefix(default_config) -> str:
    return default_config['jwt_token_prefix']


@pytest.fixture
async def test_user(pool: Pool) -> UserInDB:
    user_crud = UserCRUD(pool)
    return await user_crud.add_user(
        username="test", password="pwd@test",
        creator=0, email="admin@test.com")

# config = request.app.state.default_config


@pytest.fixture
async def token(test_user: UserInDB, default_config: dict) -> str:
    return create_access_token(test_user, default_config)


@pytest.fixture
async def authorized_client(
    app: FastAPI,
    client: AsyncClient,
    token: str,
    authorization_prefix: str,
    default_config: dict,
) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url=DEFAULT_BASE_URL,
        headers=DEFAULT_HEADERS,
    ) as client:
        client.headers[default_config['auth_header']
                       ] = f"{authorization_prefix} {token}"
        yield client
