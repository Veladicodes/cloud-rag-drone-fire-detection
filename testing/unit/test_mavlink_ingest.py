"""Real-MAVLink bridge: sends genuine MAVLink wire-format packets over a real
UDP loopback socket via pymavlink and asserts they land in the telemetry
table with the right decoded values. No mocking of the protocol layer.
"""
from __future__ import annotations

import threading
import time


def _free_port() -> int:
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_mavlink_bridge_decodes_and_persists(rag_index):
    from pymavlink import mavutil

    from backend.core.db import init_db
    from backend.services.mavlink_ingest import run_bridge

    init_db()

    port = _free_port()
    received: list[dict] = []
    stop = threading.Event()
    t = threading.Thread(
        target=run_bridge,
        args=(f"udp:127.0.0.1:{port}", received.append, stop),
        daemon=True,
    )
    t.start()
    time.sleep(0.3)

    conn = mavutil.mavlink_connection(f"udpout:127.0.0.1:{port}", source_system=42)
    conn.mav.heartbeat_send(2, 0, 0, 0, 4)
    time.sleep(0.1)
    conn.mav.global_position_int_send(
        0, int(34.05 * 1e7), int(-118.24 * 1e7), 90000, 90000, 0, 0, 0, 1800,
    )
    time.sleep(0.1)
    conn.mav.sys_status_send(0, 0, 0, 0, 1200, -1, 77, 0, 0, 0, 0, 0, 0)

    deadline = time.time() + 5
    while time.time() < deadline and len(received) < 2:
        time.sleep(0.1)
    stop.set()

    assert len(received) >= 2, f"expected >=2 decoded packets, got {received}"
    assert received[0]["call_sign"] == "MAV-42"
    assert abs(received[0]["lat"] - 34.05) < 1e-4
    assert abs(received[0]["lon"] - (-118.24)) < 1e-4
    assert received[-1]["battery_pct"] == 77.0

    from backend.core.db import SessionLocal
    from database.models import Drone, Telemetry

    db = SessionLocal()
    try:
        drone = db.query(Drone).filter_by(call_sign="MAV-42").one()
        rows = db.query(Telemetry).filter_by(drone_id=drone.id).all()
    finally:
        db.close()
    assert len(rows) >= 2
    assert abs(rows[0].lat - 34.05) < 1e-4
