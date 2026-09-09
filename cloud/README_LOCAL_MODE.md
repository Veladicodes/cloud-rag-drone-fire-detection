# Local Mode — Azure Service Stand-in Map

The Phase-2 prototype runs entirely on local processes. Nothing in this pass
touches a real Azure account. This file is the single place that records **what
each local stand-in becomes in production**.

| Architecture component (Azure) | Local stand-in (this repo) | How to switch to real Azure |
| :--- | :--- | :--- |
| **Azure SQL Database** | SQLite file `local.db` via SQLAlchemy (`backend/core/db.py`) | Set `DATABASE_URL` to an Azure SQL connection string (`mssql+pyodbc://…`). Models use portable types only — no schema change. |
| **Azure Blob Storage** | `storage/` folder on disk (`cloud/storage_local.py`, `save_blob`/`get_blob`) | Replace the two function bodies with `azure-storage-blob` `BlobClient` calls; set `AZURE_STORAGE_CONNECTION_STRING`. Call sites unchanged. |
| **Azure OpenAI (GPT-4o)** | `LLM_MODE=mock` deterministic `[MOCK LLM OUTPUT]`, or `LLM_MODE=local` small transformers model (`ai/rag/orchestrate.py`) | Set `LLM_MODE=azure` and add an `AzureOpenAI` client branch in `orchestrate.py`; supply endpoint + key via Key Vault. |
| **Embedding model** (`text-embedding-3-small`) | `sentence-transformers/all-mpnet-base-v2` (768-dim) locally, hash fallback for offline CI (`ai/rag/embeddings.py`) | Swap `_SentenceTransformerEmbedder` for an Azure OpenAI embeddings client; keep the 768/1536-dim contract. |
| **FAISS Vector Index** | Local `IndexFlatL2` written to `ai/rag/faiss_index/` | Same FAISS index, mounted from Azure Files or rebuilt in the container on deploy. |
| **Azure Communication Services (SMS) + Notification Hubs (push)** | `backend/services/alert_service.py` — logs `[MOCK SMS …]` to console + `logs/alerts.log` + an `alerts` DB row | Replace `send_immediate_alert` / `send_enriched_plan` bodies with the ACS `SmsClient` / Notification Hubs SDK; recipients from the roster (see `docs/architecture/alert-recipients.md`). |
| **Azure Container Apps** | `uvicorn` (backend) + `vite` dev server (frontend), plain processes, no Docker | Build the two containers, push to ACR, deploy to Container Apps in the VNet described in `docs/architecture/deployment-overview.md`. |
| **Managed Identity / Key Vault** | `.env` file | Replace `.env` values with Key Vault references; grant the Container App a System-Assigned Managed Identity. |

## Rule
Every file that names an Azure service carries a `# LOCAL STAND-IN FOR: Azure X`
header comment. If you add a new Azure-named module, add that header and a row here.
