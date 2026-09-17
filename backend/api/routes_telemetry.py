"""WebSocket telemetry ingestion.

LOCAL STAND-IN FOR: Azure Container Apps WebSocket ingress + Azure SQL writes.
"""
from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.api.ws import manager
from backend.core.auth import require_api_key_ws
from backend.core.db import SessionLocal
from database.models import Drone, Telemetry

router = APIRouter()


@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket) -> None:
    await require_api_key_ws(ws)
    await manager.connect(ws)
    try:
        while True:
            packet = await ws.receive_json()
            _persist(packet)
            await manager.broadcast({"type": "telemetry", **packet})
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception:  # noqa: BLE001
        manager.disconnect(ws)
        raise


def _persist(packet: dict) -> None:
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
