"""Coverage for the read endpoints in routes_plans.py not exercised elsewhere:
GET /incidents, GET /alerts, and the 404 path of GET /plans/{id}.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def _client(rag_index):
    from backend.core.db import init_db
    from backend.main import app

    init_db()
    return TestClient(app)


def test_get_plan_404_when_not_ready(rag_index):
    client = _client(rag_index)
    r = client.get("/api/v1/plans/999999")
    assert r.status_code == 404


def test_list_incidents_and_alerts_after_post(rag_index):
    client = _client(rag_index)
    payload = {"lat": 12.9, "lon": 77.6, "confidence": 0.7, "detected_class": "fire"}
    posted = client.post("/api/v1/incidents", json=payload)
    assert posted.status_code == 201
    incident_id = posted.json()["incident_id"]

    incidents = client.get("/api/v1/incidents")
    assert incidents.status_code == 200
    ids = [row["id"] for row in incidents.json()]
    assert incident_id in ids
    row = next(r for r in incidents.json() if r["id"] == incident_id)
    assert row["has_plan"] is True
    assert row["detected_class"] == "fire"

    alerts = client.get("/api/v1/alerts")
    assert alerts.status_code == 200
    assert any(a["incident_id"] == incident_id for a in alerts.json())


def test_list_incidents_respects_limit(rag_index):
    client = _client(rag_index)
    for _ in range(3):
        client.post("/api/v1/incidents", json={"lat": 1.0, "lon": 1.0, "confidence": 0.5})

    r = client.get("/api/v1/incidents", params={"limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1
