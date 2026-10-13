"""Alert-recipient contact directory — who the Alert Service actually dispatches to.

Read is open (dashboard needs it); write is API-key protected like the other
ingestion/write endpoints (POST /incidents, WS /ws/telemetry).
"""
from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.auth import require_api_key
from backend.core.config import get_settings
from backend.core.db import get_db
from database.models import Recipient

router = APIRouter(prefix="/api/v1", tags=["recipients"])

ROLES = ["forest_ranger_on_duty", "fire_department_dispatch", "affected_zone_residents"]
_PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")


class RecipientUpdate(BaseModel):
    phone_number: str | None = None
    email: str | None = None
    channel_pref: str | None = None


def _ensure_seeded(db: Session) -> list[Recipient]:
    existing = {r.role: r for r in db.scalars(select(Recipient)).all()}
    settings = get_settings()
    changed = False
    for role in ROLES:
        if role not in existing:
            r = Recipient(role=role, phone_number=settings.default_alert_phone, email=settings.default_alert_email)
            db.add(r)
            existing[role] = r
            changed = True
    if changed:
        db.commit()
        for r in existing.values():
            db.refresh(r)
    return [existing[role] for role in ROLES]


@router.get("/recipients")
def list_recipients(db: Session = Depends(get_db)) -> list[dict]:
    rows = _ensure_seeded(db)
    return [
        {
            "role": r.role, "phone_number": r.phone_number, "email": r.email,
            "channel_pref": r.channel_pref, "updated_at": r.updated_at,
        }
        for r in rows
    ]


@router.put("/recipients/{role}", dependencies=[Depends(require_api_key)])
def update_recipient(role: str, body: RecipientUpdate, db: Session = Depends(get_db)) -> dict:
    if role not in ROLES:
        raise HTTPException(status_code=404, detail=f"unknown role '{role}'")
    r = db.scalar(select(Recipient).where(Recipient.role == role))
    if r is None:
        r = Recipient(role=role)
        db.add(r)

    if body.phone_number is not None:
        if body.phone_number and not _PHONE_RE.match(body.phone_number):
            raise HTTPException(status_code=422, detail="phone_number must be E.164-like, e.g. +919487038353")
        r.phone_number = body.phone_number
    if body.email is not None:
        r.email = body.email
    if body.channel_pref is not None:
        if body.channel_pref not in ("sms", "email"):
            raise HTTPException(status_code=422, detail="channel_pref must be 'sms' or 'email'")
        r.channel_pref = body.channel_pref

    db.commit()
    db.refresh(r)
    return {
        "role": r.role, "phone_number": r.phone_number, "email": r.email,
        "channel_pref": r.channel_pref, "updated_at": r.updated_at,
    }
