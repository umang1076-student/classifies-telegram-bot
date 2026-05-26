import sys
import os

# Fix Python path - add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend'))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Classifieds API", "docs": "/docs"}


def test_create_ad():
    response = client.post("/ads", json={
        "title": "Test Ad",
        "price": 100,
        "description": "Test description",
        "category": "Test",
        "contact": "@test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Ad"
    assert data["price"] == 100


def test_get_ads():
    response = client.get("/ads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_ad():
    # First create an ad
    create_response = client.post("/ads", json={
        "title": "Single Test",
        "price": 50,
        "description": "Single test description",
        "category": "Test",
        "contact": "@single"
    })
    ad_id = create_response.json()["id"]

    # Then get it
    get_response = client.get(f"/ads/{ad_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == ad_id


def test_delete_ad():
    # Create ad to delete
    create_response = client.post("/ads", json={
        "title": "To Delete",
        "price": 1,
        "description": "Will be deleted",
        "category": "Test",
        "contact": "@delete"
    })
    ad_id = create_response.json()["id"]

    # Delete it
    delete_response = client.delete(f"/ads/{ad_id}")
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/ads/{ad_id}")
    assert get_response.status_code == 404