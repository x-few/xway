import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from .conftest import random_value

pytestmark = pytest.mark.asyncio


async def test_login_log(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.get("/api/v1/login_logs")
    assert response.status_code == HTTP_200_OK
    assert response.json()['count'] == 0

    # not supported foreign key yet
    response = await authorized_client.post("/api/v1/login_log",
                                            json={"login_log":
                                                  {
                                                      "user_id": random_value("int"),
                                                      "status": random_value("int")
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    id = response.json()['id']
    assert type(id) == int

    response = await authorized_client.get("/api/v1/login_logs")
    assert response.status_code == HTTP_200_OK
    # added record, but not for test user
    assert len(response.json()['data']) == 0

    response = await authorized_client.get("/api/v1/login_log/{}".format(id))
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.delete("/api/v1/login_log/{}".format(id))
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.get("/api/v1/login_logs")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 0
    assert response.json()['count'] == 0

    response = await authorized_client.post("/api/v1/login",
                                            json={"user": {"username": "test", "password": "pwd@test"}})
    assert response.status_code == HTTP_200_OK
    assert response.json()['access_token']

    response = await authorized_client.post("/api/v1/login",
                                            json={"user": {"username": "test", "password": "pwd@test"}})
    assert response.status_code == HTTP_200_OK
    assert response.json()['access_token']

    response = await authorized_client.get("/api/v1/login_logs")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["data"]) == 2
    assert response.json()["count"] == 2

    response = await authorized_client.get("/api/v1/login_logs", params={"page": 1, "pagesize": 1})
    assert response.status_code == HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["count"] == 2

    response = await authorized_client.get("/api/v1/login_logs", params={"page": 10, "pagesize": 1})
    assert response.status_code == HTTP_200_OK
    assert response.json()["data"] == []
    assert response.json()["count"] == 2
