from fastapi.testclient import TestClient

from xway import app

client = TestClient(app)


def test_get_all_user():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}