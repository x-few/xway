import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED

from .conftest import random_value

pytestmark = pytest.mark.asyncio


async def test_role_permission(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None:
    response = await authorized_client.get("/api/v1/role_permissions/?a=a")
    assert response.status_code == 200
    assert response.json()['count'] == 0

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

    response = await authorized_client.post("/api/v1/permission",
                                            json={"permission":
                                                  {
                                                      "name": random_value("str"),
                                                      "uri": random_value("str"),
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    permission_id = response.json()['id']
    assert type(permission_id) == int

    # not supported foreign key yet
    response = await authorized_client.post("/api/v1/role_permission",
                                            json={"role_permission":
                                                  {
                                                      "role_id": role_id,
                                                      "permission_id": permission_id,
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    id = response.json()['id']
    assert type(id) == int

    response = await authorized_client.get("/api/v1/role_permissions")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    response = await authorized_client.post("/api/v1/permission",
                                            json={"permission":
                                                  {
                                                      "name": random_value("str"),
                                                      "uri": random_value("str"),
                                                  }
                                                  }
                                            )

    assert response.status_code == HTTP_201_CREATED
    permission_id = response.json()['id']
    assert type(permission_id) == int

    response = await authorized_client.put("/api/v1/role_permission/{}".format(id),
                                           json={"role_permission":
                                                 {
                                                     "role_id": role_id,
                                                     "permission_id": permission_id,
                                                 }
                                                 }
                                           )
    assert response.status_code == 200

    response = await authorized_client.get("/api/v1/role_permission/{}".format(id))
    assert response.status_code == 200

    response = await authorized_client.delete("/api/v1/role_permission/{}".format(id))
    assert response.status_code == 200

    response = await authorized_client.get("/api/v1/role_permissions")
    assert response.status_code == 200
    assert len(response.json()['data']) == 0
    assert response.json()['count'] == 0
