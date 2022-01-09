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

    # create user
    response = await authorized_client.post("/api/v1/users",
                                            json={
                                                "user":
                                                {
                                                    "username": random_value("str"),
                                                    "password": random_value("str"),
                                                    "email": random_value("str") + "@test.com"}
                                            })
    assert response.status_code == 201
    user_id = response.json()['id']
    assert type(user_id) == int

    # create role
    response = await authorized_client.post("/api/v1/role",
                                            json={"role":
                                                  {
                                                      "name": random_value("str"),
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    role_id = response.json()['id']
    assert type(role_id) == int

    response = await authorized_client.post("/api/v1/user_role",
                                            json={"user_role":
                                                  {
                                                      "user_id": user_id,
                                                      "role_id": role_id,
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    id = response.json()['id']
    assert type(id) == int

    response = await authorized_client.get("/api/v1/user_roles")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    # create role
    response = await authorized_client.post("/api/v1/role",
                                            json={"role":
                                                  {
                                                      "name": random_value("str"),
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    role_id = response.json()['id']
    assert type(role_id) == int

    response = await authorized_client.put("/api/v1/user_role/{}".format(id),
                                           json={"user_role":
                                                 {
                                                     "user_id": user_id,
                                                     "role_id": role_id
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
