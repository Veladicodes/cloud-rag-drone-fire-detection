# Azure Service Stand-in Map

The prototype runs entirely on local processes by default. Every "cloud"
component has a local stand-in **and** a real Azure implementation selected by a
config flag — this file records the mapping. Provisioning is in
[`DEPLOY.md`](DEPLOY.md); IaC is in [`terraform/`](terraform/).

| Architecture component (Azure) | Local stand-in | Real Azure path | Switch |
| :--- | :--- | :--- | :--- |
| **Azure SQL Database** | SQLite `local.db` via SQLAlchemy (`backend/core/db.py`) | Terraform `azurerm_mssql_database` (Serverless, auto-pause); Alembic migrations apply unchanged (portable column types) | `DATABASE_URL=mssql+pyodbc://…` (Key Vault secret `database-url`) |
| **Azure Blob Storage** | `storage/` folder (`cloud/storage_local.py`) | `cloud/storage_azure.py` — same `save_blob`/`get_blob` signatures via `azure-storage-blob`; Terraform storage account + `incident-snapshots` container + Hot→Cool-after-30-days lifecycle | `STORAGE_MODE=azure` (+ `AZURE_STORAGE_ACCOUNT_URL` / Managed Identity). Dispatcher: `cloud/storage.py` |
| **Azure OpenAI / LLM** | `LLM_MODE=mock` `[MOCK LLM OUTPUT]`, or `local` flan-t5 | `LLM_MODE=gemini` — real Google Gemini Flash (`ai/rag/orchestrate.py`, `google-genai` SDK). An `azure` branch would slot in the same way once an Azure OpenAI key exists. | `LLM_MODE=gemini` + `GEMINI_API_KEY` (Key Vault secret `gemini-api-key`) |
| **Embedding model** | `sentence-transformers/all-mpnet-base-v2` (768-dim), hash fallback | same model in the container, or an Azure OpenAI embeddings client (keep the dim contract) | `EMBED_MODE` |
| **FAISS Vector Index** | local `IndexFlatL2` in `ai/rag/faiss_index/` | same index, built in the container image or mounted from Azure Files | (none) |
| **Azure Communication Services (SMS) + Notification Hubs** | `backend/services/alert_service.py` — console + `logs/alerts.log` + `alerts` row | **kept mocked on purpose** even in the Azure deployment (see `DEPLOY.md` → "Left mocked"). To make real: ACS `SmsClient` in the two `send_*` bodies. | — |
| **Azure Container Apps** | `uvicorn` process | Terraform `azurerm_container_app` (backend, system-assigned identity, scale-to-zero) from `backend/Dockerfile` | `terraform apply` + image push |
| **Frontend host** | `vite` dev server | Terraform `azurerm_static_web_app`; `npm run build` → SWA CLI deploy | see `DEPLOY.md` §4 |
| **Key Vault / Managed Identity** | `.env` file | Terraform `azurerm_key_vault` + secrets `gemini-api-key`, `database-url`; backend MI granted `Get`/`List` + `Storage Blob Data Contributor` | automatic once deployed |

## Deployed resources (live — `terraform apply` on 2026-09-10)

29 resources in resource group **`cdfdzupn5-rg`** (`centralindia`, except the
Container App environment in `eastasia` — Central India has 0 quota for those on
this student sub; Static Web App in `eastasia`).

| Output | Value |
| :--- | :--- |
| `resource_group` | `cdfdzupn5-rg` |
| `backend_url` | `https://cdfdzupn5-backend.bluewater-83023317.eastasia.azurecontainerapps.io` |
| `frontend_url` | `https://lively-meadow-05cf7d800.6.azurestaticapps.net` |
| `sql_server_fqdn` | `cdfdzupn5-sql.database.windows.net` (db `cdfd`, Serverless GP_S_Gen5_1, auto-pause 60 min) |
| `storage_blob_endpoint` | `https://cdfdzupn5sa.blob.core.windows.net/` (container `incident-snapshots`, Hot→Cool @30d) |
| `key_vault_name` | `cdfdzupn5-kv` (secrets: `gemini-api-key`, `database-url`) |
| `acr_login_server` | `cdfdzupn5acr.azurecr.io` (Basic; delete after the image is in the app) |
| `app_insights_name` | `cdfdzupn5-ai` (workspace-based, 20% sampling) |
| `log_analytics` | `cdfdzupn5-law` (daily cap 0.2 GB) |
| Budget | `cdfdzupn5-budget` — $100, alerts 50 / 80 / 100 % → `adithya.a2023@vitstudent.ac.in` |

**Backend image status:** the Container App currently runs the placeholder
`mcr.microsoft.com/k8se/quickstart` image. The student subscription blocks **ACR
Tasks** (`TasksOperationsNotAllowed`), so `az acr build` cannot be used — the real
`backend/Dockerfile` image must be built via GitHub Actions
(`.github/workflows/deploy-backend.yml`) or a local Docker build, then
`terraform apply -var backend_image=cdfdzupn5acr.azurecr.io/cdfd-backend:<tag>`.

## Rule
Every file that names an Azure service carries a `# LOCAL STAND-IN FOR:` or
`# REAL COUNTERPART OF:` header. Add a row here for any new Azure-named module.
