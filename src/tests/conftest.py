import uuid
import warnings
from os import environ, getenv

import pytest
import alembic.config
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(autouse=True)
async def init_db() -> None:
    # clean
    alembic.config.main(argv=["downgrade", "base"])
    # init
    alembic.config.main(argv=["upgrade", "head"])
    yield
    # clean
    alembic.config.main(argv=["downgrade", "base"])
    # reinit for dev
    alembic.config.main(argv=["upgrade", "head"])


@pytest.fixture
def app(init_db: None) -> FastAPI:
    from xway import application  # local import for testing purpose

    return application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app
    # return app


@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pgpool


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client

@pytest.fixture
def authorization_prefix() -> str:
    from app.core.config import JWT_TOKEN_PREFIX

    return JWT_TOKEN_PREFIX

@pytest.fixture
async def test_user(pool: Pool) -> UserInDB:
    async with pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            email="test@test.com", password="password", username="username"
        )

# config = request.app.state.default_config
@pytest.fixture
def token(test_user: UserInDB) -> str:
    return jwt.create_access_token_for_user(test_user, environ["SECRET_KEY"])


@pytest.fixture
def authorized_client(
    client: AsyncClient, token: str, authorization_prefix: str
) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }
    return client