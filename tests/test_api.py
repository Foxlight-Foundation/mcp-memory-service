import os
from pathlib import Path

from fastapi.testclient import TestClient

# isolate test DB
os.environ["MEMORY_DB_PATH"] = str(Path("data/test-memory.db"))

from memory_service.app import app  # noqa: E402


client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_add_and_search_memory():
    add = client.post(
        "/api/memories",
        json={"text": "Foxlight builds embodied AI companions", "metadata": {"tag": "mission"}},
    )
    assert add.status_code == 200
    mid = add.json()["id"]
    assert mid > 0

    search = client.post("/api/memories/search", json={"query": "embodied companions", "limit": 3})
    assert search.status_code == 200
    matches = search.json()["matches"]
    assert len(matches) >= 1
    assert matches[0]["score"] <= 1.0
