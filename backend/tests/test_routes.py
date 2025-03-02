# Run with: PYTHONPATH=$(pwd) pytest backend/tests/test_routes.py -v

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

user_id = None


def test_create_user():
    global user_id
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com",
              "password": "password123"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"
    user_id = data["id"]


def test_get_all_users():
    response = client.get("/users/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_user():
    global user_id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"


def test_update_user():
    global user_id
    response = client.put(
        f"/users/{user_id}",
        json={"username": "updateduser"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "updateduser"


def test_delete_user():
    global user_id
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["id"] == user_id


def test_get_deleted_user():
    global user_id
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert response.json()["detail"] == "User not found"


if __name__ == "__main__":
    pytest.main()
