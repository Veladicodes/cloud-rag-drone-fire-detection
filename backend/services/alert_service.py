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
from database.models import Alert, Incident, Recipient

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


def _get_or_seed_recipient(db: Session, role: str) -> Recipient:
    r = db.query(Recipient).filter_by(role=role).one_or_none()
    if r is None:
        settings = get_settings()
        r = Recipient(role=role, phone_number=settings.default_alert_phone, email=settings.default_alert_email)
        db.add(r)
        db.commit()
        db.refresh(r)
    return r


def _dispatch(recipient: Recipient, channel: str, body: str) -> tuple[str, bool]:
    """Real-vs-mock dispatch for one recipient/channel. Returns (channel_used, delivered)."""
    settings = get_settings()
    if settings.alert_mode != "acs":
        _log_line(f"[MOCK {channel.upper()} to {recipient.role}]: {body}")
        return channel, True

    from backend.services.acs_client import send_email, send_sms

    if channel in ("sms", "push") and recipient.phone_number:
        ok, detail = send_sms(recipient.phone_number, body)
        if ok:
            log.info("ACS SMS delivered to %s (%s): %s", recipient.role, recipient.phone_number, detail)
            return "sms", True
        log.warning(
            "ACS SMS failed for %s (%s): %s — falling back to email",
            recipient.role, recipient.phone_number, detail,
        )
    if recipient.email:
        ok, detail = send_email(recipient.email, "FireWatch Alert", body)
        return "email", ok
    _log_line(f"[UNDELIVERABLE — no working channel for {recipient.role}]: {body}")
    return channel, False


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
        recipient = _get_or_seed_recipient(db, role)
        channel_used, delivered = _dispatch(recipient, "sms", body)
        row = Alert(
            incident_id=incident.id, alert_class="immediate",
            recipient_role=role, channel=channel_used, body=body, delivered=delivered,
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
        preferred = "push" if role == "affected_zone_residents" else "sms"
        recipient = _get_or_seed_recipient(db, role)
        channel_used, delivered = _dispatch(recipient, preferred, body)
        row = Alert(
            incident_id=incident.id, alert_class="enriched",
            recipient_role=role, channel=channel_used, body=body, delivered=delivered,
        )
        db.add(row)
        rows.append(row)
    db.commit()
    for r in rows:
        db.refresh(r)
    return rows
