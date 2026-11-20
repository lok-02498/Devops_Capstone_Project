import pytest
import os
import sys

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from main import app, init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    os.environ["DATABASE_PATH"] = ":memory:"
    init_db()
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test dashboard UI loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"SecureOps Automation Platform" in response.data

def test_liveness_probe(client):
    """Test Kubernetes liveness probe endpoint"""
    response = client.get("/health/live")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "UP"
    assert json_data["probe"] == "liveness"

def test_readiness_probe(client):
    """Test Kubernetes readiness probe endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "READY"
    assert json_data["database"] == "connected"

def test_task_creation_and_retrieval(client):
    """Test REST API for task management"""
    # Create task
    post_res = client.post("/api/v1/tasks", json={"title": "Deploy to Kubernetes"})
    assert post_res.status_code == 201

    # Fetch tasks
    get_res = client.get("/api/v1/tasks")
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert data["count"] >= 1
    assert data["tasks"][0]["title"] == "Deploy to Kubernetes"

def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint format"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data
