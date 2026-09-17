"""Shared telemetry persistence — used by both the JSON WebSocket ingestion
(routes_telemetry.py) and the real-MAVLink bridge (mavlink_ingest.py) so a
drone's transport doesn't change what lands in the `telemetry` table.
"""
from __future__ import annotations

from backend.core.db import SessionLocal
from database.models import Drone, Telemetry


def persist_telemetry(packet: dict) -> None:
    db = SessionLocal()
    try:
        call_sign = packet.get("call_sign", "SIM-1")
        drone = db.query(Drone).filter_by(call_sign=call_sign).one_or_none()
        if drone is None:
            drone = Drone(call_sign=call_sign)
            db.add(drone)
            db.commit()
            db.refresh(drone)
        db.add(Telemetry(
            drone_id=drone.id,
            lat=float(packet["lat"]), lon=float(packet["lon"]),
            altitude_m=float(packet.get("altitude_m", 90.0)),
            battery_pct=float(packet.get("battery_pct", 100.0)),
            bearing_deg=float(packet.get("bearing_deg", 0.0)),
        ))
        drone.battery_pct = float(packet.get("battery_pct", drone.battery_pct))
        db.commit()
    finally:
        db.close()
