"""End-to-end proof: POST an incident -> an `alerts` row AND a `response_plans`
row are created, and the immediate alert lands before the plan.

conftest pins SYNC_RAG=true so the background RAG task runs inside the request.
"""
from __future__ import annotations

import base64

from fastapi.testclient import TestClient


def _client(rag_index):
    from backend.core.db import init_db
    from backend.main import app

    init_db()
    return TestClient(app)


def test_incident_creates_alert_and_plan_rows(rag_index):
    client = _client(rag_index)
    payload = {
        "lat": 34.05, "lon": -118.24, "confidence": 0.91, "detected_class": "smoke",
        "image_base64": base64.b64encode(b"synthetic-test-frame").decode(),
        "wind_speed_kmh": 22, "wind_dir_deg": 200, "temperature_c": 33, "fuel_dryness": "high",
    }
    r = client.post("/api/v1/incidents", json=payload)
    assert r.status_code == 201, r.text
    incident_id = r.json()["incident_id"]
    assert r.json()["immediate_alerts"]  # immediate alert dispatched in-request

    from backend.core.db import SessionLocal
    from database.models import Alert, ResponsePlan

    db = SessionLocal()
    try:
        alerts = db.query(Alert).filter_by(incident_id=incident_id).all()
        plan = db.query(ResponsePlan).filter_by(incident_id=incident_id).one_or_none()
    finally:
        db.close()

    assert plan is not None, "response_plans row must be created"
    classes = {a.alert_class for a in alerts}
    assert "immediate" in classes, "immediate alert row must exist"
    assert "enriched" in classes, "enriched alert row must exist after the plan"

    # the immediate alert must be timestamped no later than the enriched one
    immediate_ts = min(a.ts for a in alerts if a.alert_class == "immediate")
    enriched_ts = min(a.ts for a in alerts if a.alert_class == "enriched")
    assert immediate_ts <= enriched_ts


def test_plan_endpoint_returns_markdown(rag_index):
    client = _client(rag_index)
    r = client.post("/api/v1/incidents", json={"lat": 34.0, "lon": -118.2, "confidence": 0.8})
    inc = r.json()["incident_id"]
    p = client.get(f"/api/v1/plans/{inc}")
    assert p.status_code == 200
    assert "plan_markdown" in p.json()
    assert p.json()["llm_mode"].startswith("mock")
