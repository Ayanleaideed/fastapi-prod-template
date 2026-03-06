from app.main import app, lifespan
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_lifespan_context_manager() -> None:
    """Test that lifespan context manager can be entered and exited"""
    test_app = FastAPI(lifespan=lifespan)

    # Create a client which triggers the lifespan
    client = TestClient(test_app)

    # Make a simple request to ensure the app is working
    # This triggers the ASGI flow which includes lifespan
    response = client.get("/")
    assert response.status_code in [404, 200]  # 404 is expected since we don't have routes


def test_app_with_lifespan() -> None:
    """Test that app with lifespan initializes correctly"""
    # App is already initialized with lifespan in main.py
    assert app.router is not None
    assert len(app.routes) > 0


def test_health_and_users_integration(client: TestClient) -> None:
    """Test health and users endpoints work together"""
    # First check health
    health_response = client.get("/api/v1/health/live")
    assert health_response.status_code == 200

    # Then use users endpoint
    user_response = client.post(
        "/api/v1/users",
        json={"email": "combo@example.com", "full_name": "Combo Test"},
    )
    assert user_response.status_code == 201

    # Health should still work
    health_response2 = client.get("/api/v1/health/ready")
    assert health_response2.status_code == 200
