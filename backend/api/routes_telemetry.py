"""WebSocket telemetry ingestion.

LOCAL STAND-IN FOR: Azure Container Apps WebSocket ingress + Azure SQL writes.
"""
from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.api.ws import manager
from backend.core.auth import require_api_key_ws
from backend.services.telemetry_ingest import persist_telemetry

router = APIRouter()


@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket) -> None:
    await require_api_key_ws(ws)
    await manager.connect(ws)
    try:
        while True:
            packet = await ws.receive_json()
            persist_telemetry(packet)
            await manager.broadcast({"type": "telemetry", **packet})
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception:  # noqa: BLE001
        manager.disconnect(ws)
        raise
