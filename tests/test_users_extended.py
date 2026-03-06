from fastapi.testclient import TestClient


def test_create_user_with_missing_fields(client: TestClient) -> None:
    """Test creating user without required fields"""
    response = client.post(
        "/api/v1/users",
        json={"email": "missing@example.com"},
    )
    assert response.status_code == 422


def test_create_user_with_empty_payload(client: TestClient) -> None:
    """Test creating user with empty payload"""
    response = client.post("/api/v1/users", json={})
    assert response.status_code == 422


def test_create_user_with_extra_fields(client: TestClient) -> None:
    """Test creating user with extra fields (should ignore them)"""
    response = client.post(
        "/api/v1/users",
        json={
            "email": "extra@example.com",
            "full_name": "Extra Fields",
            "extra_field": "should be ignored",
        },
    )
    assert response.status_code == 201


def test_create_and_retrieve_multiple_operations(client: TestClient) -> None:
    """Test common workflow of creating and retrieving users"""
    # Create first user
    response1 = client.post(
        "/api/v1/users",
        json={"email": "workflow1@example.com", "full_name": "Workflow User 1"},
    )
    assert response1.status_code == 201
    user1_id = response1.json()["id"]

    # Create second user
    response2 = client.post(
        "/api/v1/users",
        json={"email": "workflow2@example.com", "full_name": "Workflow User 2"},
    )
    assert response2.status_code == 201
    user2_id = response2.json()["id"]

    # Retrieve first user
    get_response1 = client.get(f"/api/v1/users/{user1_id}")
    assert get_response1.status_code == 200
    assert get_response1.json()["email"] == "workflow1@example.com"

    # Retrieve second user
    get_response2 = client.get(f"/api/v1/users/{user2_id}")
    assert get_response2.status_code == 200
    assert get_response2.json()["email"] == "workflow2@example.com"

    # Try to retrieve non-existent user
    get_response3 = client.get(f"/api/v1/users/{user1_id + user2_id + 999}")
    assert get_response3.status_code == 404
