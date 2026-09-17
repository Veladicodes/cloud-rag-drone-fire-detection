# Deploying to Azure (real, $100 student cap)

Runbook for the topology in [`../docs/architecture/deployment-overview.md`](../docs/architecture/deployment-overview.md),
tuned for **Azure for Students ($100, no card)**. Terraform: [`terraform/`](terraform/).
Cost model and the resources to avoid are in the last section of this file.

Everything is free-tier / serverless / scale-to-zero except **ACR Basic** (~$0.17/day),
which is deleted right after the image is built. Realistic cost: **deploy + a demo
day ≈ $1–3**; idle after `azure-stop.sh` ≈ **$0**; `azure-teardown.sh` → **$0**.

## Tools

```bash
AZ="/c/Program Files/Microsoft SDKs/Azure/CLI2/wbin/az.cmd"
TF="$HOME/AppData/Local/Microsoft/WinGet/Packages/Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe/terraform.exe"
"$AZ" login --tenant 62813970-e73c-4347-a7d2-5b5543893728   # MFA in browser
"$AZ" account set --subscription "Azure for Students"
```

## 1. Provision

```bash
cloud/scripts/azure-status.sh                 # baseline spend
"$AZ" provider register --namespace Microsoft.App --wait
"$AZ" provider register --namespace Microsoft.Web --wait
"$AZ" provider register --namespace Microsoft.OperationalInsights --wait
"$AZ" provider register --namespace Microsoft.Insights --wait

cd cloud/terraform
cp terraform.tfvars.example terraform.tfvars  # subscription_id, location, prefix, alert_email
export TF_VAR_sql_admin_password='<strong password>'
export TF_VAR_gemini_api_key='<same key as your .env>'
export TF_VAR_api_key="$(openssl rand -hex 32)"       # required: drone/dashboard shared secret, see backend/core/auth.py
# add your public IP so you can run the DB migration:
"$AZ" rest --method get --url https://api.ipify.org?format=json   # -> operator_ip in tfvars

"$TF" init
"$TF" plan -out tfplan     # REVIEW: ~22 resources, no private endpoint / gateway / premium
"$TF" apply tfplan
```

`terraform output` → `backend_url`, `frontend_url`, `sql_server_fqdn`,
`storage_blob_endpoint`, `acr_login_server`, `key_vault_name`, …

## 2. Database — migrate the real Azure SQL

```bash
pip install pyodbc
export DATABASE_URL="$("$AZ" keyvault secret show --vault-name $("$TF" -chdir=cloud/terraform output -raw key_vault_name) -n database-url --query value -o tsv)"
alembic upgrade head
python - <<'PY'
import sqlalchemy as sa, os
print(sorted(sa.inspect(sa.create_engine(os.environ["DATABASE_URL"])).get_table_names()))
PY
# expect: ['alembic_version','alerts','drones','incidents','response_plans','telemetry']
```

## 3. Backend image — built IN Azure (no local Docker)

```bash
ACR=$("$TF" -chdir=cloud/terraform output -raw acr_login_server); ACRNAME=${ACR%%.*}
"$AZ" acr build -r "$ACRNAME" -t cdfd-backend:1 -f backend/Dockerfile .
cd cloud/terraform && "$TF" apply -var backend_image="$ACR/cdfd-backend:1"
curl "$("$TF" output -raw backend_url)/health"
# {"status":"ok","llm_mode":"gemini","storage_mode":"azure","database":"azure-sql",...}

cloud/scripts/azure-delete-acr.sh             # <-- kill the only 24/7 cost now
```

## 4. Frontend → Static Web App

```bash
BACKEND=$("$TF" -chdir=cloud/terraform output -raw backend_url)
cd frontend && echo "VITE_API_BASE=$BACKEND" > .env.production
npm ci && npm run build
SWA=$("$TF" -chdir=../cloud/terraform output -raw static_web_app_name)
TOKEN=$("$AZ" staticwebapp secrets list -n "$SWA" --query properties.apiKey -o tsv)
npx -y @azure/static-web-apps-cli deploy ./dist --deployment-token "$TOKEN" --env production
# add the SWA origin to backend CORS:
FRONT=$("$TF" -chdir=../cloud/terraform output -raw frontend_url)
cd ../cloud/terraform && "$TF" apply -var frontend_origin="$FRONT" -var backend_image="$ACR/cdfd-backend:1"
```

## 5. Verify end-to-end + record

```bash
python testing/simulate_drone.py --api "$BACKEND"      # live telemetry + Gemini plans on the deployed dashboard
```
Fill the "Deployed resources" table in [`README_LOCAL_MODE.md`](README_LOCAL_MODE.md)
from `terraform output` (names/endpoints, **no secrets**), commit.

## 6. When you stop working

```bash
cloud/scripts/azure-stop.sh        # app -> 0 replicas, DB paused: ~$0
cloud/scripts/azure-status.sh      # confirm spend
# ... resume later:
cloud/scripts/azure-start.sh
# ... done for weeks / between milestones:
cloud/scripts/azure-teardown.sh    # terraform destroy -> $0 (DB data lost; demo only)
```

## Left mocked on purpose

**Azure Communication Services (SMS)** — a real sendable number needs extra
verification + per-message cost. `backend/services/alert_service.py` keeps its
mock (console + `logs/alerts.log` + `alerts` row) in the Azure deploy too. The
immediate-before-RAG ordering guarantee (gate **AL-1**) is unchanged and tested.

## Cost model & guardrails ($100 student cap)

Every service is free-tier, serverless, scale-to-zero, or deleted right after use.

| Service | Tier / setting | Cost |
| :--- | :--- | :--- |
| Resource Group, VNet + 3 subnets + NSG, Managed Identity, Budget | — | $0 (networking + IAM objects are free) |
| Azure SQL Database | Serverless `GP_S_Gen5_1`, auto-pause 60 min, min 0.5 vCore, `max_size_gb = 2` | ~$0 paused; a few cents per demo; storage ~$0.03–0.05/mo |
| Storage Account + Blob | Standard LRS, Hot, Hot→Cool @ 30 d lifecycle | < $0.05/mo (a few MB of snapshots) |
| Key Vault | Standard | < $0.01/mo ($0.03 / 10k ops) |
| Log Analytics | PerGB2018, `daily_quota_gb = 0.2`, 30-day retention | $0 (inside the ~5 GB/mo free grant; cap stops any overrun) |
| Application Insights | workspace-based, 20 % sampling | $0 (shares the Log Analytics grant) |
| Container Apps env + backend app | Consumption, `min_replicas = 0` | $0 idle; free grant ≈ 100 h/mo of active time |
| Static Web App (frontend) | Free | $0 |
| Container Registry | Basic | ~$0.17/day — **delete after the image is deployed** (`azure-delete-acr.sh`); the image is cached by Container Apps |

Realistic: deploy + a demo day ≈ **$1–3**; idle with ACR deleted ≈ **< $1/mo**;
`terraform destroy` ≈ **$0**.

### Never create these (each would drain the $100)

| Resource | Why |
| :--- | :--- |
| Private Endpoint / Private DNS Zone | ~$7.30/mo per endpoint. Use SQL firewall rules. |
| Application Gateway / Front Door / WAF | $125–300/mo. Container Apps has built-in HTTPS ingress. |
| NAT Gateway, Bastion, Azure Firewall | $30–900/mo. Not needed. |
| Azure OpenAI | needs approval + paid. The LLM is Google Gemini (free tier). |
| Any Premium / Provisioned / Dedicated tier, AKS, App Service Plan B1+, VMs | fixed hourly cost — serverless / Consumption only |
| Second region, geo-replication, zone-redundancy | multiplies cost |

### Rules
1. Always `terraform plan` and read it before `apply`. No `-auto-approve` on creates.
2. Serverless / Consumption / Free tiers only — no fixed hourly SKUs.
3. `min_replicas = 0` on the Container App; SQL auto-pause on; Log Analytics daily cap on.
4. One resource group (`<prefix>-rg`) so teardown is a single command.
5. No secrets in git — SQL password + Gemini key live in `terraform.tfvars` (git-ignored)
   and Key Vault only.
6. If the credit hits 80 %, `terraform destroy` and continue in local mode
   (`STORAGE_MODE=local`, SQLite).
