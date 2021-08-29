import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

pytestmark = pytest.mark.asyncio


async def test_login_record(
    app: FastAPI,
    # client: AsyncClient,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.post("/api/v1/login",
                                            json={"user": {"username": "test", "password": "pwd@test"}})
    assert response.status_code == HTTP_200_OK
    assert response.json()['access_token']

    response = await authorized_client.post("/api/v1/login_record")
    assert response.status_code == HTTP_201_CREATED

    response = await authorized_client.get("/api/v1/login_record")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["data"]) == 2
    assert response.json()["count"] == 2

    response = await authorized_client.get("/api/v1/login_record", params={"page": 1, "pagesize": 1})
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["count"] == 2

    response = await authorized_client.get("/api/v1/login_record", params={"page": 10, "pagesize": 1})
    assert response.status_code == HTTP_200_OK
    assert response.json()["data"] == []
    assert response.json()["count"] == 2
