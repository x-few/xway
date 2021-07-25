import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

pytestmark = pytest.mark.asyncio

async def test_register(
    app: FastAPI,
    client: AsyncClient,
    pool: Pool
) -> None:
    response = await client.post("/api/v1/register", json={"user":{"username": "abc", "password": "pwd"}})
    body = response.json()
    assert response.status_code == 201
    assert body['data']
    assert body['data']['username'] == 'abc'
