"""Pytest fixtures — isolated temp DB + storage + FAISS index per session."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session", autouse=True)
def _env(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("cdfd")
    os.environ.update(
        DATABASE_URL=f"sqlite:///{tmp / 'test.db'}",
        STORAGE_PATH=str(tmp / "storage"),
        FAISS_INDEX_PATH=str(tmp / "faiss"),
        ALERT_LOG_PATH=str(tmp / "alerts.log"),
        LLM_MODE="mock",
        EMBED_MODE=os.environ.get("EMBED_MODE", "hash"),  # fast + offline for CI
        YOLO_MODE="stub",
        SYNC_RAG="true",
    )
    # settings are cached — clear so the test env wins
    from backend.core.config import get_settings

    get_settings.cache_clear()
    yield


@pytest.fixture(scope="session")
def rag_index(_env):
    from ai.rag.ingest import build_index

    return build_index()
