import pytest
import warnings
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

pytestmark = pytest.mark.asyncio


async def test_get_all_user(
    app: FastAPI,
    authorized_client: AsyncClient,
    client: AsyncClient,
    pool: Pool
) -> None:
    response = await client.get("/api/v1/users")
    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()['errors'] != "Not authenticated"

    response = await authorized_client.get("/api/v1/users")
    # print("response: ", response.json())
    assert response.status_code == HTTP_200_OK
    assert response.json()['count'] == 2

    response = await authorized_client.post("/api/v1/users",
                                            json={"user":
                                                  {"username": "testuser",
                                                   "password": "pwd",
                                                   "email": "abc@bcd.com"}}
                                            )
    assert response.status_code == HTTP_201_CREATED

    user_id = response.json()['id']
    assert type(user_id) == int

    response = await authorized_client.get("/api/v1/users")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 3

    response = await authorized_client.get("/api/v1/users", params={"page": 1, "pagesize": 1})
    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 1
    assert response.json()['count'] == 3

    response = await authorized_client.get("/api/v1/users/{}".format(user_id))
    assert response.status_code == HTTP_200_OK
    assert response.json()['id'] == user_id

    response = await authorized_client.get("/api/v1/users/{}".format(1))
    assert response.status_code == HTTP_200_OK
    assert response.json()['id'] == 1

    response = await authorized_client.get("/api/v1/users/{}".format(10000))
    assert response.status_code == HTTP_404_NOT_FOUND

    response = await authorized_client.put("/api/v1/users/{}".format(user_id),
                                           json={"user": {"username": "bcd", "status": 2}})
    assert response.status_code == HTTP_200_OK
    assert response.json()['status'] == 2
    assert response.json()['username'] == "bcd"
    assert response.json()['email'] == "abc@bcd.com"

    response = await authorized_client.put("/api/v1/users/{}".format(1),
                                           json={"user": {"username": "bcd", "status": 2}})
    assert response.status_code == HTTP_400_BAD_REQUEST

    response = await authorized_client.put("/api/v1/users/{}".format(10000),
                                           json={"user": {"username": "bcd", "status": 2}})
    assert response.status_code == HTTP_404_NOT_FOUND

    response = await authorized_client.delete("/api/v1/users/{}".format(10000))
    assert response.status_code == HTTP_404_NOT_FOUND

    response = await authorized_client.delete("/api/v1/users/{}".format(user_id))
    assert response.status_code == HTTP_200_OK

    response = await authorized_client.get("/api/v1/users")
    assert response.status_code == HTTP_200_OK
    assert len(response.json()['data']) == 2
