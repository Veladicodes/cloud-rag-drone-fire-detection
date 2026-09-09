# LOCAL MOCK FOR: Azure Communication Services (SMS) + Azure Notification Hubs (push).
# Swap the send_* function bodies for real Azure SDK calls when credentials exist
# (ACS SmsClient.send(...) / NotificationHubsClient.send_notification(...)).
# Recipients / channels / triggers are specified in
# docs/architecture/alert-recipients.md.
"""Public/Responder Alert Service (mocked delivery).

Two message classes:
  * send_immediate_alert  -> fired the instant an incident is logged, IN PARALLEL
                             with the RAG call (never gated on LLM latency).
  * send_enriched_plan    -> fired after the RAG plan is ready.

Every dispatch is (a) printed, (b) appended to logs/alerts.log, and (c) written
as an `alerts` row so the dashboard shows an audit trail even though no real
SMS/push leaves the machine.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.core.config import get_settings
from database.models import Alert, Incident

log = logging.getLogger("alert_service")

IMMEDIATE_RECIPIENTS = ["forest_ranger_on_duty", "fire_department_dispatch"]
ENRICHED_RECIPIENTS = ["forest_ranger_on_duty", "fire_department_dispatch", "affected_zone_residents"]


def _log_line(text: str) -> None:
    settings = get_settings()
    path = settings.abspath(settings.alert_log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{stamp} {text}\n")
    log.warning(text)


def send_immediate_alert(db: Session, incident: Incident) -> list[Alert]:
    """Raw alert — coordinates, confidence, timestamp, snapshot key. No RAG."""
    rows: list[Alert] = []
    body = (
        f"FIRE DETECTED at ({incident.lat:.4f}, {incident.lon:.4f}) | "
        f"class={incident.detected_class} conf={incident.confidence:.2f} | "
        f"t={incident.ts.isoformat(timespec='seconds') if incident.ts else 'now'} | "
        f"snapshot={incident.snapshot_key or 'n/a'}"
    )
    for role in IMMEDIATE_RECIPIENTS:
        _log_line(f"[MOCK SMS to {role}]: {body}")
        row = Alert(
            incident_id=incident.id, alert_class="immediate",
            recipient_role=role, channel="sms", body=body,
        )
        db.add(row)
        rows.append(row)
    db.commit()
    for r in rows:
        db.refresh(r)
    return rows


def send_enriched_plan(db: Session, incident: Incident, plan_markdown: str) -> list[Alert]:
    """Enriched notification — checklist summary + dashboard link, after RAG."""
    rows: list[Alert] = []
    summary = plan_markdown.strip().splitlines()
    headline = next((ln for ln in summary if ln.strip()), "response plan ready")
    body = (
        f"RESPONSE PLAN for incident #{incident.id} at ({incident.lat:.4f}, {incident.lon:.4f}): "
        f"{headline[:160]} | full plan: /incidents/{incident.id}"
    )
    for role in ENRICHED_RECIPIENTS:
        channel = "push" if role == "affected_zone_residents" else "sms"
        _log_line(f"[MOCK {channel.upper()} to {role}]: {body}")
        row = Alert(
            incident_id=incident.id, alert_class="enriched",
            recipient_role=role, channel=channel, body=body,
        )
        db.add(row)
        rows.append(row)
    db.commit()
    for r in rows:
        db.refresh(r)
    return rows
