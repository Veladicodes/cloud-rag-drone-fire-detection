"""Shared-secret auth for the ingestion API.

LOCAL STAND-IN FOR: Azure AD / Entra ID app registration + JWT validation.
A single API key is enough for a drone fleet + one dashboard; swap this
dependency for real JWT validation if/when multi-tenant auth is needed.
"""
from __future__ import annotations

from fastapi import Header, HTTPException, WebSocket, WebSocketException, status

from backend.core.config import get_settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.api_key:
        return  # auth disabled (local dev / CI default)
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing API key")


async def require_api_key_ws(ws: WebSocket) -> None:
    settings = get_settings()
    if not settings.api_key:
        return
    if ws.query_params.get("api_key") != settings.api_key:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
