"""Incident pipeline: detection event -> storage + DB -> immediate alert ->
RAG plan -> enriched alert -> dashboard broadcast.

The ordering here is a real requirement (professor's brief / ADR-002 addendum):
`send_immediate_alert` is called BEFORE the RAG pipeline starts, so human
notification never waits on LLM latency.
"""
from __future__ import annotations

import base64
import json
import logging

from sqlalchemy.orm import Session

from ai.rag.orchestrate import generate_plan
from backend.services.alert_service import send_enriched_plan, send_immediate_alert
from cloud.storage import save_blob  # local stand-in or real Azure Blob per STORAGE_MODE
from database.models import Incident, ResponsePlan

log = logging.getLogger("pipeline")


def create_incident(db: Session, payload: dict) -> Incident:
    snapshot_key = None
    img_b64 = payload.get("image_base64")
    if img_b64:
        raw = base64.b64decode(img_b64)
        # container "incident-snapshots" -> LOCAL STAND-IN FOR: Azure Blob container
        snapshot_key = save_blob("incident-snapshots", f"pending-{payload['lat']:.4f}_{payload['lon']:.4f}.jpg", raw)

    incident = Incident(
        drone_id=payload.get("drone_id"),
        lat=float(payload["lat"]),
        lon=float(payload["lon"]),
        detected_class=payload.get("detected_class", "smoke"),
        confidence=float(payload["confidence"]),
        snapshot_key=snapshot_key,
        wind_speed_kmh=float(payload.get("wind_speed_kmh", 12.0)),
        wind_dir_deg=float(payload.get("wind_dir_deg", 210.0)),
        temperature_c=float(payload.get("temperature_c", 31.0)),
        fuel_dryness=payload.get("fuel_dryness", "high"),
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)

    if snapshot_key:  # rename now that we have an id
        incident.snapshot_key = save_blob(
            "incident-snapshots", f"incident-{incident.id}.jpg", base64.b64decode(img_b64)
        )
        db.commit()
    return incident


def run_rag_and_notify(db: Session, incident_id: int, broadcaster=None) -> ResponsePlan:
    incident = db.get(Incident, incident_id)
    result = generate_plan(
        {
            "lat": incident.lat, "lon": incident.lon,
            "detected_class": incident.detected_class, "confidence": incident.confidence,
            "wind_speed_kmh": incident.wind_speed_kmh, "wind_dir_deg": incident.wind_dir_deg,
            "temperature_c": incident.temperature_c, "fuel_dryness": incident.fuel_dryness,
        }
    )
    plan = ResponsePlan(
        incident_id=incident.id,
        plan_markdown=result["plan_markdown"],
        llm_mode=result["llm_mode"],
        retrieved_sources=result["retrieved_sources"],
        insufficient_context=result["insufficient_context"],
    )
    db.add(plan)
    incident.status = "planned"
    db.commit()
    db.refresh(plan)

    send_enriched_plan(db, incident, result["plan_markdown"])

    if broadcaster is not None:
        broadcaster({
            "type": "plan_ready",
            "incident_id": incident.id,
            "llm_mode": plan.llm_mode,
            "insufficient_context": plan.insufficient_context,
        })
    log.info("incident %s planned (llm_mode=%s)", incident.id, plan.llm_mode)
    return plan
