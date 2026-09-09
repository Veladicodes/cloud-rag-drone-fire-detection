"""Storage dispatcher — picks the local stand-in or real Azure Blob at runtime.

`backend/services/pipeline.py` imports `save_blob` / `get_blob` from here, so the
call sites never change; only STORAGE_MODE (env) does.

    STORAGE_MODE=local   -> cloud.storage_local   (filesystem; default)
    STORAGE_MODE=azure   -> cloud.storage_azure   (azure-storage-blob)
"""
from __future__ import annotations

from backend.core.config import get_settings

_mode = get_settings().storage_mode.lower()

if _mode == "azure":
    from cloud.storage_azure import blob_path, get_blob, save_blob  # noqa: F401
else:
    from cloud.storage_local import blob_path, get_blob, save_blob  # noqa: F401

STORAGE_BACKEND = _mode
