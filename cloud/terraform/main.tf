# Provisions the topology from docs/architecture/deployment-overview.md, tuned for a
# $100 Azure-for-Students cap (see cloud/DEPLOY.md "Cost model & guardrails").
# Everything here is free-tier, serverless, scale-to-zero, or (ACR) deleted right after use.
#
#   NO private endpoints / App Gateway / NAT / Firewall / OpenAI / premium SKUs.
#   Azure Communication Services (SMS) stays MOCKED (cloud/DEPLOY.md).

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

locals {
  name = "${var.prefix}${random_string.suffix.result}"
  tags = { project = "cloud-drone-fire-detection", managed_by = "terraform", budget = "students-100usd" }
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name}-rg"
  location = var.location
  tags     = local.tags
}

# ---------------------------------------------------------------- cost guard ---
# $100 subscription budget with e-mail alerts. Free.
resource "azurerm_consumption_budget_subscription" "cap" {
  name            = "${local.name}-budget"
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = 100
  time_grain      = "Annually"

  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00'Z'", timestamp())
  }

  dynamic "notification" {
    for_each = [50, 80, 100]
    content {
      enabled        = true
      threshold      = notification.value
      operator       = "GreaterThanOrEqualTo"
      threshold_type = "Actual"
      contact_emails = [var.alert_email]
    }
  }
  lifecycle { ignore_changes = [time_period] }
}

# ---------------------------------------------------------------- networking ---
resource "azurerm_virtual_network" "vnet" {
  name                = "${local.name}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.20.0.0/16"]
  tags                = local.tags
}

resource "azurerm_subnet" "frontend" {
  name                 = "frontend"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.20.1.0/24"]
}

resource "azurerm_subnet" "backend" {
  name                 = "backend"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.20.2.0/23"] # Container Apps Consumption env needs a /23
  delegation {
    name = "aca"
    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

resource "azurerm_subnet" "database" {
  name                 = "database"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.20.4.0/24"]
}

# NSG documents the intent (DB tier reachable only from the backend subnet).
resource "azurerm_network_security_group" "database" {
  name                = "${local.name}-db-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  security_rule {
    name                       = "allow-backend-subnet"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "10.20.2.0/23"
    source_port_range          = "*"
    destination_address_prefix = "10.20.4.0/24"
    destination_port_ranges    = ["1433"]
  }
  tags = local.tags
}

resource "azurerm_subnet_network_security_group_association" "database" {
  subnet_id                 = azurerm_subnet.database.id
  network_security_group_id = azurerm_network_security_group.database.id
}

# -------------------------------------------------------------- Azure SQL -------
resource "azurerm_mssql_server" "sql" {
  name                          = "${local.name}-sql"
  resource_group_name           = azurerm_resource_group.rg.name
  location                      = azurerm_resource_group.rg.location
  version                       = "12.0"
  administrator_login           = var.sql_admin_login
  administrator_login_password  = var.sql_admin_password
  public_network_access_enabled = true # no private endpoint on this budget; firewall-gated below
  minimum_tls_version           = "1.2"
  tags                          = local.tags
}

resource "azurerm_mssql_database" "db" {
  name                        = "cdfd"
  server_id                   = azurerm_mssql_server.sql.id
  sku_name                    = "GP_S_Gen5_1" # Serverless, GP, 1 vCore
  auto_pause_delay_in_minutes = 60            # pauses -> ~$0 when idle
  min_capacity                = 0.5
  max_size_gb                 = 2             # demo data is tiny; storage is billed per GB
  storage_account_type        = "Local"
  tags                        = local.tags
}

# Allow other Azure services (the Container App) + the operator's IP for migrations.
resource "azurerm_mssql_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_mssql_firewall_rule" "operator" {
  count            = var.operator_ip == "" ? 0 : 1
  name             = "operator"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = var.operator_ip
  end_ip_address   = var.operator_ip
}

# --------------------------------------------------------- Blob storage ---------
resource "azurerm_storage_account" "sa" {
  name                     = replace("${local.name}sa", "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  access_tier              = "Hot"
  min_tls_version          = "TLS1_2"
  tags                     = local.tags
}

resource "azurerm_storage_container" "snapshots" {
  name                  = "incident-snapshots"
  storage_account_id    = azurerm_storage_account.sa.id
  container_access_type = "private"
}

resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.sa.id
  rule {
    name    = "snapshots-hot-to-cool"
    enabled = true
    filters {
      prefix_match = ["incident-snapshots/"]
      blob_types   = ["blockBlob"]
    }
    actions {
      base_blob {
        tier_to_cool_after_days_since_modification_greater_than = 30
      }
    }
  }
}

# ------------------------------------------------ Log Analytics + App Insights --
resource "azurerm_log_analytics_workspace" "law" {
  name                = "${local.name}-law"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  daily_quota_gb      = 0.2 # hard cap so Container Apps logs cannot run up a bill
}

resource "azurerm_application_insights" "ai" {
  name                = "${local.name}-ai"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  workspace_id        = azurerm_log_analytics_workspace.law.id
  application_type    = "web"
  sampling_percentage = 20
  tags                = local.tags
}

# ------------------------------------------------------------- Key Vault --------
resource "azurerm_key_vault" "kv" {
  name                       = "${local.name}-kv"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  rbac_authorization_enabled = false
  tags                       = local.tags
}

resource "azurerm_key_vault_access_policy" "deployer" {
  key_vault_id       = azurerm_key_vault.kv.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = data.azurerm_client_config.current.object_id
  secret_permissions = ["Get", "List", "Set", "Delete", "Purge", "Recover"]
}

resource "azurerm_key_vault_secret" "gemini" {
  name         = "gemini-api-key"
  value        = var.gemini_api_key
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

resource "azurerm_key_vault_secret" "db_conn" {
  name = "database-url"
  value = format(
    "mssql+pyodbc://%s:%s@%s.database.windows.net:1433/%s?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no",
    var.sql_admin_login, var.sql_admin_password,
    azurerm_mssql_server.sql.name, azurerm_mssql_database.db.name
  )
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

# -------------------------------------------------- Container Registry (Basic) --
# The ONLY resource that bills 24/7 (~$0.17/day). Delete it right after the image
# is pushed (cloud/scripts/azure-delete-acr.sh); Container Apps caches the image.
resource "azurerm_container_registry" "acr" {
  name                = replace("${local.name}acr", "-", "")
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true  # express Container App envs can't use MI for ACR pull
  tags                = local.tags
}

# ------------------------------------------------------- Container Apps ---------
# Central India has a 0 quota for Container App Environments on this student sub,
# so the environment (and only the environment) lives in var.aca_location. A VNet
# is single-region, so this Consumption environment runs public - SQL/Storage/KV
# stay reachable via firewall rules + Managed Identity, and the VNet/NSG remain as
# the documented network design. (Recorded in cloud/README_LOCAL_MODE.md.)
resource "azurerm_container_app_environment" "cae" {
  name                       = "${local.name}-cae"
  location                   = var.aca_location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

resource "azurerm_container_app" "backend" {
  name                         = "${local.name}-backend"
  container_app_environment_id = azurerm_container_app_environment.cae.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity { type = "SystemAssigned" }

  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }

  secret {
    name  = "gemini-api-key"
    value = var.gemini_api_key
  }

  secret {
    name = "database-url"
    value = format(
      "mssql+pyodbc://%s:%s@%s.database.windows.net:1433/%s?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no",
      var.sql_admin_login, var.sql_admin_password,
      azurerm_mssql_server.sql.name, azurerm_mssql_database.db.name
    )
  }

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = 0 # scale-to-zero: $0 when idle
    max_replicas = 1
    container {
      name   = "backend"
      image  = var.backend_image
      cpu    = 0.5
      memory = "1Gi"
      env {
        name  = "STORAGE_MODE"
        value = "azure"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "GEMINI_API_KEY"
        secret_name = "gemini-api-key"
      }
      env {
        name  = "RECREATE_DB"
        value = var.recreate_db
      }
      env {
        name  = "AZURE_STORAGE_ACCOUNT_URL"
        value = azurerm_storage_account.sa.primary_blob_endpoint
      }
      env {
        name  = "LLM_MODE"
        value = "gemini"
      }
      env {
        name  = "KEY_VAULT_URI"
        value = azurerm_key_vault.kv.vault_uri
      }
      env {
        name  = "APPLICATIONINSIGHTS_CONNECTION_STRING"
        value = azurerm_application_insights.ai.connection_string
      }
      env {
        name  = "FRONTEND_ORIGIN"
        value = var.frontend_origin
      }
    }
  }
  tags = local.tags
}

# backend identity: read KV secrets, write blobs, pull from ACR
resource "azurerm_key_vault_access_policy" "backend" {
  key_vault_id       = azurerm_key_vault.kv.id
  tenant_id          = data.azurerm_client_config.current.tenant_id
  object_id          = azurerm_container_app.backend.identity[0].principal_id
  secret_permissions = ["Get", "List"]
}

resource "azurerm_role_assignment" "backend_blob" {
  scope                = azurerm_storage_account.sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_container_app.backend.identity[0].principal_id
}

# --------------------------------------------------------- Frontend ------------
resource "azurerm_static_web_app" "frontend" {
  name                = "${local.name}-web"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.swa_location # SWA has a short region list
  sku_tier            = "Free"
  sku_size            = "Free"
  tags                = local.tags
}
