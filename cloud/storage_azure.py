# REAL COUNTERPART OF: cloud/storage_local.py
# Same save_blob / get_blob / blob_path signatures, backed by Azure Blob Storage.
# Selected at runtime when STORAGE_MODE=azure (see cloud/storage.py).
"""Azure Blob Storage implementation.

Requires `azure-storage-blob` and one of:
  * AZURE_STORAGE_CONNECTION_STRING  (simple; used during initial setup), or
  * a Managed Identity + AZURE_STORAGE_ACCOUNT_URL (preferred in the deployed app)
"""
from __future__ import annotations

import functools
from pathlib import Path

from backend.core.config import get_settings

_settings = get_settings()


@functools.lru_cache(maxsize=1)
def _service_client():
    from azure.storage.blob import BlobServiceClient

    conn = _settings.azure_storage_connection_string
    if conn:
        return BlobServiceClient.from_connection_string(conn)
    # Managed-identity path
    from azure.identity import DefaultAzureCredential

    acct_url = _settings.azure_storage_account_url
    if not acct_url:
        raise RuntimeError(
            "STORAGE_MODE=azure but neither AZURE_STORAGE_CONNECTION_STRING nor "
            "AZURE_STORAGE_ACCOUNT_URL is set"
        )
    return BlobServiceClient(account_url=acct_url, credential=DefaultAzureCredential())


def _ensure_container(name: str):
    svc = _service_client()
    cc = svc.get_container_client(name)
    try:
        cc.create_container()
    except Exception:  # already exists
        pass
    return cc


def save_blob(container: str, key: str, data: bytes) -> str:
    _ensure_container(container).upload_blob(name=key, data=data, overwrite=True)
    return f"{container}/{key}"


def get_blob(container: str, key: str) -> bytes:
    return _service_client().get_blob_client(container, key).download_blob().readall()


def blob_path(container: str, key: str) -> Path:  # no true Azure equivalent
    raise NotImplementedError("blob_path() is local-only; use a SAS URL in Azure mode")
