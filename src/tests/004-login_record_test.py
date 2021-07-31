import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

pytestmark = pytest.mark.asyncio

async def test_login_record(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.post("/api/v1/login_record")
    print("response: ", response.json())
    assert response.status_code == 201
