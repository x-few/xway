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
    # print("response: ", response.json())
    assert response.status_code == 200
    assert response.json()['count'] == 1

    # response = await authorized_client.post("/api/v1/users", json={"user":{"username": "testuser", "password": "pwd", "email": "abc@bcd.com"}})
    # assert response.status_code == 201

    # app_id = response.json()['id']
    # assert type(app_id) == int

    # response = await authorized_client.get("/api/v1/users")
    # assert response.status_code == 200
    # assert len(response.json()['data']) == 2

    # response = await authorized_client.get("/api/v1/users", params={"page": 1, "pagesize": 1})
    # assert response.status_code == 200
    # assert len(response.json()['data']) == 1
    # assert response.json()['count'] == 2

    # response = await authorized_client.get("/api/v1/users/{}".format(app_id))
    # assert response.status_code == 200
    # assert response.json()['id'] == app_id

    # response = await authorized_client.get("/api/v1/users/{}".format(1))
    # assert response.status_code == 404

    # response = await authorized_client.get("/api/v1/users/{}".format(10000))
    # assert response.status_code == 404

    # response = await authorized_client.put("/api/v1/users/{}".format(app_id),
    #     json={"user": {"username": "bcd", "status": 2}})
    # assert response.status_code == 200
    # assert response.json()['status'] == 2
    # assert response.json()['username'] == "bcd"
    # assert response.json()['email'] == "abc@bcd.com"

    # response = await authorized_client.put("/api/v1/users/{}".format(1),
    #     json={"user": {"username": "bcd", "status": 2}})
    # assert response.status_code == 404

    # response = await authorized_client.put("/api/v1/users/{}".format(10000),
    #     json={"user": {"username": "bcd", "status": 2}})
    # assert response.status_code == 404

    # response = await authorized_client.delete("/api/v1/users/{}".format(1))
    # assert response.status_code == 404

    # response = await authorized_client.delete("/api/v1/users/{}".format(10000))
    # assert response.status_code == 404

    # response = await authorized_client.delete("/api/v1/users/{}".format(app_id))
    # assert response.status_code == 204

    # response = await authorized_client.get("/api/v1/users")
    # assert response.status_code == 200
    # assert len(response.json()['data']) == 1
