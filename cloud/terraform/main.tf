# Provisions the topology designed in docs/architecture/deployment-overview.md:
#   VNet (frontend / backend / database subnets) · Azure SQL Serverless ·
#   Storage Account + Blob (Hot -> Cool after 30 days) · Container Apps env +
#   backend app · Static Web App (frontend) · Key Vault · system-assigned
#   Managed Identity wired to Key Vault.  SMS (Azure Communication Services) is
#   intentionally NOT provisioned — see cloud/DEPLOY.md section "left mocked".

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 5
  upper   = false
  special = false
}

locals {
  name = "${var.prefix}${random_string.suffix.result}"
  tags = { project = "cloud-drone-fire-detection", managed_by = "terraform" }
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.name}-rg"
  location = var.location
  tags     = local.tags
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
  address_prefixes     = ["10.20.2.0/23"] # Container Apps needs a /23
  delegation {
    name = "aca"
    service_delegation {
      name    = "Microsoft.App/environments"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    }
  }
}

resource "azurerm_subnet" "database" {
  name                              = "database"
  resource_group_name               = azurerm_resource_group.rg.name
  virtual_network_name              = azurerm_virtual_network.vnet.name
  address_prefixes                  = ["10.20.4.0/24"]
  private_endpoint_network_policies  = "Enabled"
}

resource "azurerm_network_security_group" "database" {
  name                = "${local.name}-db-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  # Database subnet only accepts traffic from the backend subnet.
  security_rule {
    name                       = "allow-backend-only"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "10.20.2.0/23"
    source_port_range          = "*"
    destination_address_prefix = "10.20.4.0/24"
    destination_port_ranges    = ["1433", "443"]
  }
  security_rule {
    name                       = "deny-all-inbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_address_prefix      = "*"
    source_port_range          = "*"
    destination_address_prefix = "*"
    destination_port_range     = "*"
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
  public_network_access_enabled = true # keep true for first migration; flip to false once the private endpoint is verified
  minimum_tls_version           = "1.2"
  tags                          = local.tags
}

resource "azurerm_mssql_database" "db" {
  name                        = "cdfd"
  server_id                   = azurerm_mssql_server.sql.id
  sku_name                    = "GP_S_Gen5_1" # Serverless, General Purpose, 1 vCore
  auto_pause_delay_in_minutes = 60
  min_capacity                = 0.5
  max_size_gb                 = 32
  storage_account_type        = "Local"
  tags                        = local.tags
}

resource "azurerm_private_endpoint" "sql" {
  name                = "${local.name}-sql-pe"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.database.id
  private_service_connection {
    name                           = "sql"
    private_connection_resource_id = azurerm_mssql_server.sql.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }
  tags = local.tags
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

# ------------------------------------------------------------- Key Vault --------
resource "azurerm_key_vault" "kv" {
  name                       = "${local.name}-kv"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false
  soft_delete_retention_days = 7
  tags                       = local.tags
}

resource "azurerm_key_vault_access_policy" "deployer" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  secret_permissions = ["Get", "List", "Set", "Delete", "Purge"]
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
    "mssql+pyodbc://%s:%s@%s.database.windows.net:1433/%s?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes",
    var.sql_admin_login, var.sql_admin_password,
    azurerm_mssql_server.sql.name, azurerm_mssql_database.db.name
  )
  key_vault_id = azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.deployer]
}

# ------------------------------------------------------- Container Apps ---------
resource "azurerm_log_analytics_workspace" "law" {
  name                = "${local.name}-law"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "cae" {
  name                       = "${local.name}-cae"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
  infrastructure_subnet_id   = azurerm_subnet.backend.id
}

resource "azurerm_container_app" "backend" {
  name                         = "${local.name}-backend"
  container_app_environment_id = azurerm_container_app_environment.cae.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity { type = "SystemAssigned" }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  template {
    min_replicas = 0
    max_replicas = 2
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
        name  = "FRONTEND_ORIGIN"
        value = var.frontend_origin
      }
    }
  }
  tags = local.tags
}

# The backend's managed identity may read Key Vault secrets and write blobs.
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
  location            = "eastus2" # SWA has a limited region list
  sku_tier            = "Free"
  sku_size            = "Free"
  tags                = local.tags
}
