import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

pytestmark = pytest.mark.asyncio

async def test_get_all_user(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.get("/api/v1/users")
    # print("response: "response.json())
    assert response.status_code == 200
    assert response.json()['count'] == 2

    response = await authorized_client.post("/api/v1/user", json={"user":{"username": "fdsafasfaea", "passwordd": "pwd"}})
    assert response.status_code == 201

    response = await authorized_client.get("/api/v1/users")
    # print("response: "response.json())
    assert response.status_code == 200

