"""Read endpoints for the dashboard: incidents, response plans, alerts."""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.db import get_db
from database.models import Alert, Incident, ResponsePlan

router = APIRouter(prefix="/api/v1", tags=["read"])


@router.get("/incidents")
def list_incidents(db: Session = Depends(get_db), limit: int = 50) -> list[dict]:
    rows = db.scalars(select(Incident).order_by(Incident.id.desc()).limit(limit)).all()
    return [
        {
            "id": r.id, "ts": r.ts, "lat": r.lat, "lon": r.lon,
            "detected_class": r.detected_class, "confidence": r.confidence,
            "status": r.status, "snapshot_key": r.snapshot_key,
            "has_plan": r.plan is not None,
        }
        for r in rows
    ]


@router.get("/plans/{incident_id}")
def get_plan(incident_id: int, db: Session = Depends(get_db)) -> dict:
    plan = db.scalar(select(ResponsePlan).where(ResponsePlan.incident_id == incident_id))
    if plan is None:
        raise HTTPException(status_code=404, detail="plan not ready")
    return {
        "incident_id": incident_id,
        "ts": plan.ts,
        "llm_mode": plan.llm_mode,
        "insufficient_context": plan.insufficient_context,
        "retrieved_sources": json.loads(plan.retrieved_sources or "[]"),
        "plan_markdown": plan.plan_markdown,
    }


@router.get("/alerts")
def list_alerts(db: Session = Depends(get_db), limit: int = 100) -> list[dict]:
    rows = db.scalars(select(Alert).order_by(Alert.id.desc()).limit(limit)).all()
    return [
        {
            "id": r.id, "ts": r.ts, "incident_id": r.incident_id,
            "alert_class": r.alert_class, "recipient_role": r.recipient_role,
            "channel": r.channel, "body": r.body,
        }
        for r in rows
    ]
