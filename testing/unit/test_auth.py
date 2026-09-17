"""API_KEY gate on POST /incidents and WS /ws/telemetry.

conftest doesn't set API_KEY, so the default-empty-key/auth-off path is covered
implicitly by every other test in the suite; this file covers the enforced path.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def _client_with_key(rag_index, key: str):
    from backend.core.config import get_settings
    from backend.core.db import init_db
    from backend.main import app

    get_settings.cache_clear()

    import os

    os.environ["API_KEY"] = key
    get_settings.cache_clear()
    init_db()
    client = TestClient(app)
    yield client
    os.environ.pop("API_KEY", None)
    get_settings.cache_clear()


def test_post_incident_requires_api_key_when_set(rag_index):
    gen = _client_with_key(rag_index, "secret-123")
    client = next(gen)
    try:
        payload = {"lat": 1.0, "lon": 1.0, "confidence": 0.5}

        no_key = client.post("/api/v1/incidents", json=payload)
        assert no_key.status_code == 401

        wrong_key = client.post("/api/v1/incidents", json=payload, headers={"X-API-Key": "nope"})
        assert wrong_key.status_code == 401

        right_key = client.post("/api/v1/incidents", json=payload, headers={"X-API-Key": "secret-123"})
        assert right_key.status_code == 201
    finally:
        next(gen, None)


def test_ws_telemetry_requires_api_key_when_set(rag_index):
    gen = _client_with_key(rag_index, "secret-123")
    client = next(gen)
    try:
        try:
            with client.websocket_connect("/ws/telemetry"):
                assert False, "should have been rejected"
        except Exception:
            pass  # connection refused/closed as expected

        with client.websocket_connect("/ws/telemetry?api_key=secret-123") as ws:
            ws.send_json({"call_sign": "SIM-AUTH", "lat": 1.0, "lon": 1.0})
            echoed = ws.receive_json()
            assert echoed["call_sign"] == "SIM-AUTH"
    finally:
        next(gen, None)
