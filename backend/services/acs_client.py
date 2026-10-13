# REAL COUNTERPART OF: the mock `_log_line` SMS/push sends in alert_service.py.
# Selected at runtime when ALERT_MODE=acs (see backend/core/config.py).
"""Azure Communication Services client — real SMS (primary) and Email (fallback).

NOTE: ACS SMS does not currently support India (+91) as a destination country
(confirmed via Microsoft Q&A / Messaging Connect docs, Oct 2026). SMS sends to
+91 numbers will raise/return a failure; callers should treat that as expected
and fall back to send_email(), not as a bug. See
docs/architecture/acs-sms-india-risk.md.
"""
from __future__ import annotations

import functools
import logging

from backend.core.config import get_settings

log = logging.getLogger("acs_client")


@functools.lru_cache(maxsize=1)
def _sms_client():
    from azure.communication.sms import SmsClient

    return SmsClient.from_connection_string(get_settings().acs_connection_string)


@functools.lru_cache(maxsize=1)
def _email_client():
    from azure.communication.email import EmailClient

    return EmailClient.from_connection_string(get_settings().acs_connection_string)


def send_sms(to: str, body: str) -> tuple[bool, str]:
    """Returns (success, detail). Does not raise on provider-level failure —
    the caller decides whether to fall back to email."""
    settings = get_settings()
    if not settings.acs_sms_sender:
        return False, "ACS_SMS_SENDER not configured"
    try:
        result = _sms_client().send(from_=settings.acs_sms_sender, to=[to], message=body)
        r = result[0] if isinstance(result, list) else result
        success = bool(getattr(r, "successful", False))
        detail = str(getattr(r, "error_message", None) or getattr(r, "http_status_code", ""))
        return success, detail or "sent"
    except Exception as exc:  # noqa: BLE001 — provider/network errors are expected (e.g. unsupported country)
        log.warning("ACS SMS send failed for %s: %s", to, exc)
        return False, str(exc)


def send_email(to: str, subject: str, body_text: str) -> tuple[bool, str]:
    settings = get_settings()
    if not settings.acs_email_sender:
        return False, "ACS_EMAIL_SENDER not configured"
    try:
        message = {
            "senderAddress": settings.acs_email_sender,
            "recipients": {"to": [{"address": to}]},
            "content": {"subject": subject, "plainText": body_text},
        }
        poller = _email_client().begin_send(message)
        result = poller.result()
        status = str(getattr(result, "status", "") or (result.get("status", "") if isinstance(result, dict) else ""))
        return True, status or "sent"
    except Exception as exc:  # noqa: BLE001
        log.warning("ACS Email send failed for %s: %s", to, exc)
        return False, str(exc)
