"""WebSocket telemetry ingestion + Blob-storage stand-in."""
from __future__ import annotations

from fastapi.testclient import TestClient


def _client(rag_index):
    from backend.core.db import init_db
    from backend.main import app

    init_db()
    return TestClient(app)


def test_ws_telemetry_persists_and_echoes(rag_index):
    client = _client(rag_index)
    with client.websocket_connect("/ws/telemetry") as ws:
        ws.send_json({"call_sign": "SIM-TEST", "lat": 34.1, "lon": -118.2, "battery_pct": 77.0})
        echoed = ws.receive_json()
    assert echoed["type"] == "telemetry"
    assert echoed["call_sign"] == "SIM-TEST"

    from backend.core.db import SessionLocal
    from database.models import Drone, Telemetry

    db = SessionLocal()
    try:
        drone = db.query(Drone).filter_by(call_sign="SIM-TEST").one()
        rows = db.query(Telemetry).filter_by(drone_id=drone.id).count()
    finally:
        db.close()
    assert rows >= 1


def test_storage_local_roundtrip(rag_index):
    from cloud.storage_local import get_blob, save_blob

    key = save_blob("unit-test", "hello.txt", b"payload-123")
    assert key == "unit-test/hello.txt"
    assert get_blob("unit-test", "hello.txt") == b"payload-123"
