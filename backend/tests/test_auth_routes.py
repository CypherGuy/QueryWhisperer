# Run with: PYTHONPATH=$(pwd) pytest backend/tests/test_auth_routes.py -v

import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Fixed test user credentials
test_email = "test@example.com"
test_password = "password123"


def register_fixed_user():
    """Ensure that the fixed test user is registered.
       Accept 200 (newly created) or 409 (already exists) as success."""
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": test_email,
              "password": test_password}
    )
    if response.status_code not in [200, 409]:
        pytest.fail(
            f"User registration failed with status {response.status_code}")


def get_auth_token():
    """Logs in and returns an access token for the fixed test user.
       Ensures the user is registered first."""
    register_fixed_user()
    response = client.post(
        "/auth/login",
        json={"email": test_email, "password": test_password}
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def test_register_user():
    """Registers a new user with unique email and ensures successful registration."""
    unique_username = f"testuser_{uuid.uuid4().hex[:6]}"
    unique_email = f"{unique_username}@example.com"

    response = client.post(
        "/auth/register",
        json={"username": unique_username,
              "email": unique_email, "password": test_password}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_login_user():
    """Logs in the fixed user and retrieves an access token."""
    register_fixed_user()
    response = client.post(
        "/auth/login",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_access_protected_route():
    """Accesses a protected route using a valid token."""
    token = get_auth_token()
    assert token, "Failed to get access token"
    response = client.get(
        "/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "username" in data
    assert data["email"] == test_email


def test_invalid_login():
    """Tests login with incorrect credentials."""
    response = client.post(
        "/auth/login",
        json={"email": test_email, "password": "wrongpassword"}
    )
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json()["detail"] in [
        "Invalid credentials", "Could not validate credentials", "Not authenticated"]


def test_access_protected_route_without_token():
    """Attempts to access a protected route without authentication."""
    response = client.get("/auth/users/me")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json()["detail"] in [
        "Could not validate credentials", "Not authenticated"]


def test_cleanup_user():
    """Deletes the fixed test user if it exists."""
    token = get_auth_token()
    if token:
        response = client.get(
            "/users/", headers={"Authorization": f"Bearer {token}"})
        users = response.json()
        for user in users:
            if user["email"] == test_email:
                delete_response = client.delete(
                    f"/users/{user['id']}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                assert delete_response.status_code == 200, f"Failed to delete user with email {test_email}"


if __name__ == "__main__":
    pytest.main()
