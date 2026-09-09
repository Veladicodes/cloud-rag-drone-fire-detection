"""Incident detection events.

POST /api/v1/incidents
  1. persist snapshot (Blob stand-in) + incidents row
  2. send_immediate_alert  <-- BEFORE any RAG work (ADR-002 addendum, gate AL-1)
  3. RAG plan + enriched alert  -- background task, or synchronous if SYNC_RAG=true
"""
from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.api.ws import manager
from backend.core.config import get_settings
from backend.core.db import SessionLocal, get_db
from backend.services.alert_service import send_immediate_alert
from backend.services.pipeline import create_incident, run_rag_and_notify

router = APIRouter(prefix="/api/v1", tags=["incidents"])


class IncidentIn(BaseModel):
    lat: float
    lon: float
    confidence: float = Field(ge=0.0, le=1.0)
    detected_class: str = "smoke"
    drone_id: int | None = None
    image_base64: str | None = None
    wind_speed_kmh: float | None = None
    wind_dir_deg: float | None = None
    temperature_c: float | None = None
    fuel_dryness: str | None = None


def _run_rag_bg(incident_id: int) -> None:
    db = SessionLocal()
    try:
        run_rag_and_notify(db, incident_id, broadcaster=manager.broadcast_threadsafe)
    finally:
        db.close()


@router.post("/incidents", status_code=201)
def post_incident(body: IncidentIn, bg: BackgroundTasks, db: Session = Depends(get_db)) -> dict:
    settings = get_settings()
    incident = create_incident(db, body.model_dump(exclude_none=True))

    # (2) immediate human alert — parallel with, and ahead of, RAG.
    immediate = send_immediate_alert(db, incident)

    # (3) RAG plan + enriched alert
    if settings.sync_rag:
        run_rag_and_notify(db, incident.id)
    else:
        bg.add_task(_run_rag_bg, incident.id)

    manager.broadcast_threadsafe({
        "type": "incident", "incident_id": incident.id,
        "lat": incident.lat, "lon": incident.lon,
        "confidence": incident.confidence, "detected_class": incident.detected_class,
    })

    return {
        "incident_id": incident.id,
        "snapshot_key": incident.snapshot_key,
        "immediate_alerts": [a.recipient_role for a in immediate],
        "rag": "synchronous" if settings.sync_rag else "queued",
    }
