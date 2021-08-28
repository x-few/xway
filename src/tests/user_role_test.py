import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED

from .conftest import random_value

pytestmark = pytest.mark.asyncio


async def test_user_role(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.get("/api/v1/user_roles")
    assert response.status_code == 200
    assert response.json()['count'] == 0

    response = await authorized_client.post("/api/v1/user_role",
                                            json={"user_role":
                                                  {
                                                      "user_id": random_value("int"),
                                                      "role_id": random_value("int")
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    id = response.json()['id']
    assert type(id) == int

    response = await authorized_client.get("/api/v1/user_roles")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    response = await authorized_client.put("/api/v1/user_role/{}".format(id),
                                           json={"user_role":
                                                 {
                                                     "user_id": random_value("int"),
                                                     "role_id": random_value("int")
                                                 }
                                                 }
                                           )
    assert response.status_code == 200

    response = await authorized_client.get("/api/v1/user_role/{}".format(id))
    assert response.status_code == 200

    response = await authorized_client.delete("/api/v1/user_role/{}".format(id))
    assert response.status_code == 200

    response = await authorized_client.get("/api/v1/user_roles")
    assert response.status_code == 200
    assert len(response.json()['data']) == 0
    assert response.json()['count'] == 0
