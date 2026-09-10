# Deploying to Azure (real)

The topology is designed in [`../docs/architecture/deployment-overview.md`](../docs/architecture/deployment-overview.md);
this file is the **runbook** to provision and deploy it. Terraform lives in
[`terraform/`](terraform/). Every step is credential-gated — run it yourself
after `az login`.

> **Status:** the local prototype (SQLite + filesystem Blob + `LLM_MODE=gemini`)
> is fully working. The steps below have **not** been executed from this repo —
> they are the exact commands to run once you have Azure for Students access.

## Prerequisites (one time)

```bash
# 1. Azure CLI + Terraform
winget install Microsoft.AzureCLI Hashicorp.Terraform      # (or brew / apt)
az login
az account show --query id -o tsv                          # -> your subscription_id

# 2. Register providers (first subscription use)
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights
```

## 1. Provision infrastructure

```bash
cd cloud/terraform
cp terraform.tfvars.example terraform.tfvars     # fill in subscription_id, prefix
export TF_VAR_sql_admin_password='<a strong password>'
export TF_VAR_gemini_api_key='<the same key from your .env>'

terraform init
terraform apply        # creates RG, VNet+subnets, Azure SQL Serverless, Storage,
                       # Key Vault, Container Apps env + backend app, Static Web App
```

`terraform output` then gives `backend_url`, `frontend_url`, `sql_server_fqdn`,
`storage_blob_endpoint`, `key_vault_uri`.

## 2. Database — run migrations against the real Azure SQL

```bash
# allow your IP through the SQL firewall for the one-off migration
az sql server firewall-rule create -g $(terraform output -raw resource_group) \
  -s $(terraform output -raw sql_server_fqdn | cut -d. -f1) \
  -n devbox --start-ip-address <your-ip> --end-ip-address <your-ip>

pip install "pyodbc"
export DATABASE_URL="$(az keyvault secret show --vault-name <kv-name> -n database-url --query value -o tsv)"
alembic upgrade head            # creates drones, telemetry, incidents, response_plans, alerts, alembic_version
python - <<'PY'
import sqlalchemy as sa, os
print(sorted(sa.inspect(sa.create_engine(os.environ["DATABASE_URL"])).get_table_names()))
PY
```

Expected: `['alembic_version', 'alerts', 'drones', 'incidents', 'response_plans', 'telemetry']`
— the same check Phase 2 ran against SQLite.

## 3. Backend image

```bash
az acr create -g $(terraform output -raw resource_group) -n <prefix>acr --sku Basic
az acr login -n <prefix>acr
docker build -f backend/Dockerfile -t <prefix>acr.azurecr.io/cdfd-backend:1 .
docker push <prefix>acr.azurecr.io/cdfd-backend:1

# point the container app at the real image and re-apply
terraform apply -var backend_image=<prefix>acr.azurecr.io/cdfd-backend:1
```

The backend runs with `STORAGE_MODE=azure`, `LLM_MODE=gemini`, and pulls
`GEMINI_API_KEY` / `DATABASE_URL` from Key Vault via its **system-assigned
Managed Identity** (Terraform already grants `Get`/`List` on the vault and
`Storage Blob Data Contributor` on the account).

Verify:

```bash
curl "$(terraform output -raw backend_url)/health"
# {"status":"ok","llm_mode":"gemini","storage_mode":"azure",...}
```

## 4. Frontend

```bash
cd frontend
echo "VITE_API_BASE=$(cd ../cloud/terraform && terraform output -raw backend_url)" > .env.production
npm ci && npm run build
npx @azure/static-web-apps-cli deploy ./dist \
  --deployment-token "$(az staticwebapp secrets list -n <prefix>-web --query properties.apiKey -o tsv)"
```

Then add the deployed origin to backend CORS:

```bash
cd ../cloud/terraform
terraform apply -var frontend_origin="$(terraform output -raw frontend_url)" \
                -var backend_image=<prefix>acr.azurecr.io/cdfd-backend:1
```

Open `frontend_url`, run `python testing/simulate_drone.py --api <backend_url>`,
and the deployed dashboard should show live telemetry, alerts, and Gemini plans.

## 5. Record the real names

After a successful deploy, fill the "Deployed resources" table in
[`README_LOCAL_MODE.md`](README_LOCAL_MODE.md) with the actual resource names and
endpoints (not secrets) from `terraform output`.

## Left mocked on purpose

**Azure Communication Services (SMS).** Provisioning a real SMS-capable phone
number needs extra identity verification and, in many regions, per-message cost
beyond the student credit. `backend/services/alert_service.py` keeps its mock
(console + `logs/alerts.log` + `alerts` table) even in the Azure deployment. This
is a deliberate, documented scope boundary — the alert *ordering* guarantee
(immediate before RAG, gate AL-1) is unchanged and still tested. To make it real
later: create an ACS resource + phone number and replace the two `send_*` bodies
with `azure.communication.sms.SmsClient` calls.
