output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "backend_url" {
  value = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
}

output "frontend_url" {
  value = "https://${azurerm_static_web_app.frontend.default_host_name}"
}

output "sql_server_fqdn" {
  value = "${azurerm_mssql_server.sql.name}.database.windows.net"
}

output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}

output "storage_blob_endpoint" {
  value = azurerm_storage_account.sa.primary_blob_endpoint
}

output "key_vault_uri" {
  value = azurerm_key_vault.kv.vault_uri
}

output "database_url_secret" {
  value = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.db_conn.id})"
}
