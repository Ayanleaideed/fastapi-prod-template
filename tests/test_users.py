import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_create_user_success(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "full_name": "Test User"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client: TestClient) -> None:
    # Create first user
    client.post(
        "/api/v1/users",
        json={"email": "duplicate@example.com", "full_name": "First User"},
    )
    # Try to create user with same email
    response = client.post(
        "/api/v1/users",
        json={"email": "duplicate@example.com", "full_name": "Second User"},
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_get_user_success(client: TestClient) -> None:
    # Create a user first
    create_response = client.post(
        "/api/v1/users",
        json={"email": "gettest@example.com", "full_name": "Get Test User"},
    )
    user_id = create_response.json()["id"]
    
    # Retrieve the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "gettest@example.com"
    assert data["full_name"] == "Get Test User"


def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/users/999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_user_invalid_email(client: TestClient) -> None:
    response = client.post(
        "/api/v1/users",
        json={"email": "invalid-email", "full_name": "Invalid User"},
    )
    assert response.status_code == 422


def test_get_user_multiple_users(client: TestClient) -> None:
    user1 = client.post(
        "/api/v1/users",
        json={"email": "user1@example.com", "full_name": "User One"},
    ).json()
    user2 = client.post(
        "/api/v1/users",
        json={"email": "user2@example.com", "full_name": "User Two"},
    ).json()
    
    response1 = client.get(f"/api/v1/users/{user1['id']}")
    assert response1.status_code == 200
    assert response1.json()["email"] == "user1@example.com"
    
    response2 = client.get(f"/api/v1/users/{user2['id']}")
    assert response2.status_code == 200
    assert response2.json()["email"] == "user2@example.com"
