import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

pytestmark = pytest.mark.asyncio


async def test_languages(
    client: AsyncClient,
) -> None:
    response = await client.get("/api/v1/languages")
    assert response.status_code == HTTP_200_OK
    assert type(len(response.json()["data"])) == int
