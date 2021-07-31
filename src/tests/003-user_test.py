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
    response = await authorized_client.get("/api/v1/user")
    # print("response: "response.json())
    assert response.status_code == 200
    assert response.json()['count'] == 2

    response = await authorized_client.post("/api/v1/user", json={"user":{"username": "fdsafasfaea", "passwordd": "pwd"}})
    assert response.status_code == 201

    app_id = response.json()['id']
    assert type(app_id) == int

    response = await authorized_client.get("/api/v1/user")
    assert response.status_code == 200
    assert len(response.json()['data']) == 3

    response = await authorized_client.get("/api/v1/user/{}".format(app_id))
    assert response.status_code == 200
    assert response.json()['id'] == app_id

    response = await authorized_client.delete("/api/v1/user/{}".format(app_id))
    assert response.status_code == 204

    response = await authorized_client.get("/api/v1/user")
    assert response.status_code == 200
    assert len(response.json()['data']) == 2
