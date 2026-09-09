# Alert Recipients & Delivery Specification

This document answers the human-alerting requirement directly: **how** alerts are delivered and **who** receives them. It is the single reference a reviewer can point to for the `Public/Responder Alert Service` described in [`architecture.md`](architecture.md).

Two message classes are defined:

- **Immediate raw alert** — dispatched the instant a YOLO detection is logged, **in parallel with** the RAG call (never gated on LLM latency). Measured by validation gate **AL-1** (`≤ 15 s` from detection to first SMS dispatch).
- **Enriched response-plan notification** — dispatched after the RAG pipeline returns a plan; carries the containment/evacuation checklist summary and a dashboard link.

---

## 1. Recipient / Channel / Trigger Matrix

| Recipient role | Channel | Trigger condition | Message content | Data source for contact info |
| :--- | :--- | :--- | :--- | :--- |
| Forest ranger on duty | SMS via Azure Communication Services | Any YOLO detection above the confidence threshold (immediate) | Incident coordinates, confidence score, timestamp, snapshot thumbnail link | On-duty roster — `drones_table` / operations roster. **TODO(verify):** confirm with team whether roster/contact data lives in Azure SQL or a separate directory service; not yet decided in ADR-002/003 — flagged as an open decision for Review-2. |
| Local fire department dispatch | SMS via Azure Communication Services | Same as above (immediate) | Same as above, plus nearest access route hint (future) | Static configured dispatch number per patrol region (config / Key Vault). **TODO(verify):** confirm per-region dispatch contact list ownership. |
| Forest ranger on duty + fire dispatch | SMS / push via Azure Notification Hubs | RAG pipeline has returned a response plan (enriched) | Generated containment/evacuation checklist summary + link to full plan on the dashboard | As above. |
| Affected-zone residents distribution list | Push via Azure Notification Hubs (SMS fallback) | RAG plan ready **and** incident location falls within a registered residential zone polygon | Plain-language evacuation guidance summary + dashboard link | Opt-in resident registry keyed by zone polygon. **TODO(verify):** registry storage and zone-polygon source not yet designed — open decision for Review-2. |
| Operator / ground commander | In-dashboard (WebSocket) — not part of the external Alert Service | Every incident (immediate) and every plan (enriched) | Full incident record + full plan | Azure SQL (`incidents`, `response_plans`). |

---

## 2. Delivery Rules

1. The **immediate raw alert** MUST be sent before the RAG call starts, not after it. The alert service call and the RAG trigger are issued in parallel by the FastAPI gateway.
2. If the Alert Service call fails, the failure is logged to the `alerts` record and retried with backoff; RAG processing is unaffected.
3. The **enriched notification** is best-effort and may be skipped if the RAG pipeline returns `INSUFFICIENT_CONTEXT` — in that case the immediate raw alert already stands, and the dashboard shows the fallback state.
4. Every dispatched message (immediate and enriched) is written to an `alerts` table row so the dashboard can display an "alerts sent" audit trail even when the underlying SMS/push provider is mocked.

---

## 3. Open Decisions (for Review-2)

- Where on-duty roster and resident-registry contact data is stored (Azure SQL vs. dedicated directory service).
- Zone-polygon definition and maintenance for the affected-zone residents list.
- Per-region fire-dispatch contact ownership and update process.
- Confidence-threshold value that qualifies a detection for an immediate public alert vs. an operator-only notification.
