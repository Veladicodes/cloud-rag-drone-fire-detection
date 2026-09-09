"""Tiny in-memory WebSocket connection manager.

LOCAL STAND-IN FOR: Azure Web PubSub / SignalR fan-out. For a single-process
prototype an in-memory set of sockets is enough.
"""
from __future__ import annotations

import asyncio
import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._sockets: set[WebSocket] = set()
        self._loop: asyncio.AbstractEventLoop | None = None

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._sockets.add(ws)
        self._loop = asyncio.get_running_loop()

    def disconnect(self, ws: WebSocket) -> None:
        self._sockets.discard(ws)

    async def broadcast(self, message: dict) -> None:
        dead = []
        for ws in list(self._sockets):
            try:
                await ws.send_text(json.dumps(message, default=str))
            except Exception:  # noqa: BLE001
                dead.append(ws)
        for ws in dead:
            self._sockets.discard(ws)

    def broadcast_threadsafe(self, message: dict) -> None:
        """Callable from a sync context (e.g. a background task)."""
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast(message), self._loop)


manager = ConnectionManager()
