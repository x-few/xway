import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

pytestmark = pytest.mark.asyncio

async def test_get_all_user(
    app: FastAPI,
    client: AsyncClient,
    pool: Pool
) -> None:
    response = await client.get("/api/v1/users")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'data': []}

    response = await client.post("/api/v1/user", json={"user":{"username": "fdsafasfaea", "passwordd": "pwd"}})
    assert response.status_code == 201

    response = await client.get("/api/v1/users")
    print(response.json())
    assert response.status_code == 200

