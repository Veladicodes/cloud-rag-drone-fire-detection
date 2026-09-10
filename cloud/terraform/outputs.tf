output "resource_group" { value = azurerm_resource_group.rg.name }
output "location" { value = azurerm_resource_group.rg.location }

output "backend_url" { value = "https://${azurerm_container_app.backend.ingress[0].fqdn}" }
output "frontend_url" { value = "https://${azurerm_static_web_app.frontend.default_host_name}" }

output "sql_server_fqdn" { value = "${azurerm_mssql_server.sql.name}.database.windows.net" }
output "sql_database" { value = azurerm_mssql_database.db.name }

output "storage_account_name" { value = azurerm_storage_account.sa.name }
output "storage_blob_endpoint" { value = azurerm_storage_account.sa.primary_blob_endpoint }

output "acr_login_server" { value = azurerm_container_registry.acr.login_server }
output "key_vault_name" { value = azurerm_key_vault.kv.name }
output "key_vault_uri" { value = azurerm_key_vault.kv.vault_uri }

output "container_app_name" { value = azurerm_container_app.backend.name }
output "static_web_app_name" { value = azurerm_static_web_app.frontend.name }
output "app_insights_name" { value = azurerm_application_insights.ai.name }
