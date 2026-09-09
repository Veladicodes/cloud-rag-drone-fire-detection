# LOCAL STAND-IN FOR: Azure Blob Storage.
# Swap the body of save_blob / get_blob for azure-storage-blob calls
# (BlobServiceClient.from_connection_string(...).get_blob_client(container, key))
# when AZURE_STORAGE_CONNECTION_STRING exists. The signatures deliberately match
# a thin wrapper around that SDK, so call sites do not change.
"""Filesystem-backed blob store.

Layout:  <STORAGE_PATH>/<container>/<key>
"""
from __future__ import annotations

from pathlib import Path

from backend.core.config import get_settings

_settings = get_settings()


def _root() -> Path:
    root = _settings.abspath(_settings.storage_path)
    root.mkdir(parents=True, exist_ok=True)
    return root


def save_blob(container: str, key: str, data: bytes) -> str:
    """Persist ``data`` and return the storage key (``container/key``)."""
    dest = _root() / container / key
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return f"{container}/{key}"


def get_blob(container: str, key: str) -> bytes:
    src = _root() / container / key
    return src.read_bytes()


def blob_path(container: str, key: str) -> Path:
    """Local-only helper (no Azure equivalent) — used by the dashboard to serve thumbnails."""
    return _root() / container / key
