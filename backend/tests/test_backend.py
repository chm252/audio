import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}

def test_transcriptions():
    res = client.get("/transcriptions")
    assert res.status_code == 200
    assert "data" in res.json()
    assert isinstance(res.json()["data"], list)

def test_search():
    query = "Sample 1"
    res = client.get("/search", params={"query": query})

    assert res.status_code == 200
    assert "results" in res.json()
    assert isinstance(res.json()["results"], list)