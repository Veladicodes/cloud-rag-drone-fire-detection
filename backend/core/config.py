"""Application settings.

Every field here is env-driven so that switching from the local prototype to a
real Azure deployment is a configuration change, not a code change. See
``.env.example`` for the local-vs-Azure meaning of each value.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root = two levels up from this file (backend/core/config.py -> repo root).
REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(REPO_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LOCAL STAND-IN FOR: Azure SQL Database.
    database_url: str = "sqlite:///./local.db"

    # LOCAL STAND-IN FOR: Azure Blob Storage.
    storage_path: str = "./storage"

    # Response-plan LLM.  mock | local | gemini
    #   mock   -> deterministic "[MOCK LLM OUTPUT]" (no key, CI/offline)
    #   local  -> small local transformers model, else mock
    #   gemini -> Google Gemini Flash via GEMINI_API_KEY (real generation)
    # (Azure OpenAI would be a fourth 'azure' branch once that key exists.)
    llm_mode: str = "mock"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Embedding backend.  auto (sentence-transformers) | hash (offline fallback)
    embed_mode: str = "auto"

    # Edge detector backend.  auto (ultralytics COCO placeholder) | finetuned | stub
    #   finetuned -> ai/models/weights/wildfire_yolov8n.pt (FireNet-trained)
    yolo_mode: str = "auto"
    finetuned_weights: str = "./ai/models/weights/wildfire_yolov8n.pt"

    # Blob backend.  local (filesystem stand-in) | azure (azure-storage-blob)
    storage_mode: str = "local"
    azure_storage_connection_string: str = ""
    azure_storage_account_url: str = ""  # for the Managed-Identity path
    azure_blob_container: str = "incident-snapshots"

    kb_path: str = "./data/knowledge-base/sample_sops"
    faiss_index_path: str = "./ai/rag/faiss_index"

    # LOCAL MOCK FOR: Azure Communication Services + Notification Hubs.
    alert_log_path: str = "./logs/alerts.log"

    confidence_threshold: float = 0.35
    sync_rag: bool = False
    recreate_db: bool = False  # one-shot: drop_all before create_all (schema reset)
    frontend_origin: str = "http://localhost:5173"

    # --- resolved absolute paths -------------------------------------------------
    def abspath(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else (REPO_ROOT / p)


@lru_cache
def get_settings() -> Settings:
    return Settings()
