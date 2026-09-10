# CLAUDE.md — Azure operating manual for `cloud-drone-fire-detection`

This file governs **every Azure action** taken in this repo. Read it before running
any `az` / `terraform` command. It exists because the project runs on an **Azure
for Students** subscription with a **hard $100 credit cap and no card on file** —
when the credit is gone, everything stops.

Subscription: `Azure for Students` · `8fb3faa8-4e94-4e42-8a36-5b559e3618a4`
Tenant: `62813970-e73c-4347-a7d2-5b5543893728` · MFA required (`az login --tenant <tenant>`)

---

## 1. The two goals, in tension

1. **Breadth for marks** — the rubric rewards using *more* distinct Azure services.
2. **$100 total** — so every service must be free-tier, serverless, scale-to-zero,
   or deleted immediately after use.

The design below maximises (1) inside (2). Do not add a service that is not on the
"USE" list without re-checking its price and updating this file.

---

## 2. Services we USE (and why they're safe on $100)

| # | Service | Tier / setting | Idle cost | Why it's safe |
| :- | :--- | :--- | :--- | :--- |
| 1 | Resource Group | — | $0 | container only |
| 2 | Virtual Network + 3 subnets + NSG | — | $0 | networking objects are free |
| 3 | Azure SQL Database | **Serverless** `GP_S_Gen5_1`, auto-pause 60 min, min 0.5 vCore | ~$0 when paused; ~$0.10/hr active; storage ~$0.12/GB/mo | pauses itself after 1 h idle; demo bursts are cents |
| 4 | Storage Account + Blob container | Standard **LRS**, Hot, lifecycle → Cool @ 30 d | < $0.05/mo at demo scale | a few MB of snapshots |
| 5 | Key Vault | Standard | ~$0 | $0.03 per 10k ops |
| 6 | Managed Identity (system-assigned) | — | $0 | free |
| 7 | Log Analytics Workspace | PerGB2018, **daily cap 0.2 GB**, 30-day retention | first ~5 GB/mo effectively free; cap stops overrun | required by Container Apps |
| 8 | Application Insights | workspace-based, sampling on | ~$0 within the LA free grant | adds an observability service for marks, ~free |
| 9 | Container Apps Environment + 1 Container App (backend) | **Consumption**, `min_replicas = 0` | **$0 when idle** | monthly free grant 180k vCPU-s + 360k GiB-s; scales to zero |
| 10 | Static Web App (frontend) | **Free** | $0 | free tier, 100 GB bandwidth/mo |
| 11 | Azure Container Registry | **Basic** | ~$0.167/day (~$5/mo) | the ONLY always-on cost — **delete it after the image is built** (see §5) |
| 12 | Azure Budget + alert | $100, alerts at 50/80/100 % | $0 | the safety net |
| 13 | Cost Management queries | `az consumption` / `az costmanagement` | $0 | check spend before/after every session |

**Realistic run cost:** deploy + a demo afternoon ≈ **$1–3**. Idle with ACR kept ≈
**$5/mo**. Idle with ACR deleted ≈ **< $1/mo**. Full `terraform destroy` ≈ **$0**.

---

## 3. Services we must NEVER create (they will drain the $100)

| Service | Why forbidden |
| :--- | :--- |
| **Private Endpoint / Private DNS Zone** | $0.01/hr each (~$7.30/mo/endpoint) + DNS zone. Use SQL firewall rules instead. |
| **Application Gateway / Front Door / WAF** | $125–300/mo. Container Apps has built-in HTTPS ingress. |
| **NAT Gateway, Azure Bastion, Azure Firewall** | $30–900/mo. Not needed. |
| **Azure OpenAI** | needs approval + paid. We use **Gemini free tier** for the LLM. |
| **Any "Premium" / "Provisioned" / "Dedicated" tier** | fixed hourly cost. Serverless/Consumption only. |
| **AKS, App Service Plan (B1+), VMs, Cosmos DB provisioned** | fixed cost. |
| **Second region / geo-replication / zone-redundancy** | multiplies cost. Single region: `centralindia`. |

If Terraform tries to create any of these, stop and fix the config.

---

## 4. Golden rules

1. **Plan before apply.** Always `terraform plan` and read it. Never `apply` an
   unreviewed plan. Never `apply -auto-approve` for creates.
2. **Serverless / Consumption / Free only.** Every compute or data resource must be
   one of these. No fixed hourly SKUs.
3. **Scale to zero.** `min_replicas = 0` on the Container App. SQL auto-pause on.
4. **Cap the logs.** Log Analytics `daily_quota_gb = 0.2`. Container Apps is the
   noisy one.
5. **Stop when idle.** After a work/demo session run `cloud/scripts/azure-stop.sh`
   (scales app to 0, the DB pauses itself). Full teardown between milestones:
   `cloud/scripts/azure-teardown.sh` (= `terraform destroy`).
6. **Delete the ACR** once the backend image is in the Container App
   (`cloud/scripts/azure-delete-acr.sh`) — the image is cached by Container Apps,
   and ACR Basic is the only thing that bills 24/7.
7. **Check spend every session.** Start and end with
   `cloud/scripts/azure-status.sh` (shows budget + current cost).
8. **One resource group.** Everything in `<prefix>-rg` so teardown is one command.
9. **No secrets in git.** SQL password + Gemini key live in `terraform.tfvars`
   (git-ignored) and Key Vault. Never echo them into a committed file or the
   transcript.
10. **If credit hits 80 %**, `terraform destroy` immediately and continue the
    project in local mode (`STORAGE_MODE=local`, `LLM_MODE=gemini`, SQLite).

---

## 5. Standard procedures

```bash
# tools (Bash tool can't rely on PATH — use full paths)
AZ="/c/Program Files/Microsoft SDKs/Azure/CLI2/wbin/az.cmd"
TF=~/AppData/Local/Microsoft/WinGet/Packages/Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe/terraform.exe

# --- provision (once) ---
cloud/scripts/azure-status.sh          # baseline spend
cd cloud/terraform && "$TF" init && "$TF" plan -out tfplan
# ... review plan ...
"$TF" apply tfplan

# --- after image build ---
cloud/scripts/azure-delete-acr.sh      # stop the only 24/7 cost

# --- end of every session ---
cloud/scripts/azure-stop.sh            # app -> 0 replicas; DB auto-pauses
cloud/scripts/azure-status.sh          # confirm spend

# --- between milestones / when done for weeks ---
cloud/scripts/azure-teardown.sh        # terraform destroy -> $0

# --- resume after teardown ---
cd cloud/terraform && "$TF" apply       # ~10 min; DB data is lost (demo only)
```

## 6. What "using Azure properly" means for the report

We can legitimately claim, with resources actually deployed:
VNet + subnet isolation, NSG, **Serverless Azure SQL**, **Blob Storage with a
lifecycle policy**, **Key Vault + system-assigned Managed Identity** (zero secrets
in code), **Container Apps** (scale-to-zero microservice), **Static Web App**,
**Container Registry**, **Log Analytics + Application Insights** (observability),
and **Azure Budget** cost governance — all provisioned via **Terraform IaC**, all
inside a $100 student cap. Screenshot `az resource list -o table` and the Budget
blade for evidence.
