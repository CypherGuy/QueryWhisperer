import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Example user credentials
test_email = "test@example.com"
test_password = "password123"


def register_fixed_user():
    """
    Ensure that the fixed test user is registered.
    Accept 200 (newly created) or 409 (already exists) as success.
    """
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": test_email,
              "password": test_password}
    )
    if response.status_code not in [200, 409]:
        pytest.fail(
            f"User registration failed with status {response.status_code}")


def get_auth_token() -> str:
    """
    Logs in and returns an access token for the fixed test user.
    Ensures the user is registered first.
    """
    register_fixed_user()
    response = client.post(
        "/auth/login",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code == 200, f"Login failed with status {response.status_code}"
    token = response.json().get("access_token")
    assert isinstance(token, str), "Token is not a string."
    # Ensure no extra whitespace
    assert token == token.strip(), "Token has unexpected whitespace."
    return token


def get_current_user_id(token: str) -> int:
    """
    Retrieve the current authenticated user's ID by querying the /auth/users/me endpoint.
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 200, f"Expected 200 when getting current user, got {response.status_code}"
    user = response.json()
    return user["id"]


def test_get_auth_token_returns_raw_token():
    """Ensure get_auth_token() returns a string without extra whitespace."""
    token = get_auth_token()
    assert token.startswith("eyJ"), "Token does not appear to be a valid JWT."


def test_register_user():
    """Registers a new user with a unique email and ensures successful registration."""
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
    assert "access_token" in data, f"Token not found in response: {data}"
    assert data["token_type"] == "bearer"


def test_access_protected_route():
    """Accesses a protected route using a valid token."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "username" in data
    assert data["email"] == test_email


def test_access_protected_route_without_token():
    """Attempts to access a protected route without authentication.
       Expecting 403 Forbidden.
    """
    response = client.get("/auth/users/me")
    assert response.status_code == 403, f"Expected 403, got {response.status_code}"


def test_update_user():
    """Updates the fixed user with a valid token."""
    token = get_auth_token()
    user_id = get_current_user_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        f"/users/{user_id}",
        json={"username": "updateduser"},
        headers=headers
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_delete_user():
    """Deletes the fixed test user with a valid token."""
    token = get_auth_token()
    user_id = get_current_user_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_get_deleted_user():
    """After deletion, attempting to get the deleted user should result in a 404 Not Found."""
    token = get_auth_token()
    user_id = get_current_user_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    # Delete first, then check it's actually deleted
    del_response = client.delete(f"/users/{user_id}", headers=headers)
    assert del_response.status_code == 200, f"Deletion failed: got {del_response.status_code}"
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
