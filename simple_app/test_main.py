from fastapi.testclient import TestClient
from main import app
import os
import json
import pytest

client = TestClient(app)

DATA_FILE = "data/cases.json"


def setup_module():
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)


def teardown_module():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)


def test_create_case():
    response = client.post(
        "/cases",
        json={"id": 10, "title": "Test Case", "status": "open"},
    )
    assert response.status_code == 200
    assert response.json()["case"]["id"] == 10


def test_get_cases():
    response = client.get("/cases")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_single_case():
    response = client.get("/cases/10")
    assert response.status_code == 200
    assert response.json()["id"] == 10


def test_update_case():
    response = client.put(
        "/cases/10",
        json={"id": 10, "title": "Updated Case", "status": "closed"},
    )
    assert response.status_code == 200
    assert response.json()["case"]["title"] == "Updated Case"


def test_delete_case():
    response = client.delete("/cases/10")
    assert response.status_code == 200
    assert response.json()["case"]["id"] == 10
