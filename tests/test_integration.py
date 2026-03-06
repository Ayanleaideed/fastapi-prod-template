from fastapi.testclient import TestClient


def test_api_router_integration(client: TestClient) -> None:
    """Test API router is properly registered"""
    # Verify health endpoint exists
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200

    # Verify users endpoint exists
    response = client.post(
        "/api/v1/users",
        json={"email": "integration@example.com", "full_name": "Integration Test"},
    )
    assert response.status_code == 201


def test_error_handling_flow(client: TestClient) -> None:
    """Test complete error handling flow"""
    # Create a user
    create_response = client.post(
        "/api/v1/users",
        json={"email": "error@example.com", "full_name": "Error Test"},
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Try duplicate email
    dup_response = client.post(
        "/api/v1/users",
        json={"email": "error@example.com", "full_name": "Another User"},
    )
    assert dup_response.status_code == 409

    # Try invalid user ID
    invalid_response = client.get("/api/v1/users/0")
    assert invalid_response.status_code == 404

    # Try non-existent user
    nonexist_response = client.get(f"/api/v1/users/{user_id * 1000}")
    assert nonexist_response.status_code == 404


def test_data_persistence(client: TestClient) -> None:
    """Test that created data persists across requests"""
    # Create user
    create_response = client.post(
        "/api/v1/users",
        json={"email": "persistence@example.com", "full_name": "Persist Test"},
    )
    assert create_response.status_code == 201
    created_data = create_response.json()
    user_id = created_data["id"]
    created_at = created_data["created_at"]

    # Retrieve same user multiple times
    for _ in range(3):
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 200
        retrieved_data = get_response.json()

        # Verify data consistency
        assert retrieved_data["id"] == user_id
        assert retrieved_data["email"] == "persistence@example.com"
        assert retrieved_data["full_name"] == "Persist Test"
        assert retrieved_data["created_at"] == created_at
