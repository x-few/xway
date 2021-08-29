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
    assert len(response.json()['data']) == 1

    response = await authorized_client.put("/api/v1/login_log/{}".format(id),
                                           json={"login_log":
                                                 {
                                                     "user_id": random_value("int"),
                                                     "status": random_value("int")
                                                 }
                                                 }
                                           )
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.get("/api/v1/login_log/{}".format(id))
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.delete("/api/v1/login_log/{}".format(id))
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.get("/api/v1/login_logs")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 0
    assert response.json()['count'] == 0
