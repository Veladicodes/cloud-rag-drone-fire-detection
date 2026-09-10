variable "subscription_id" {
  type        = string
  description = "Azure subscription ID (from `az account show`)."
}

variable "location" {
  type    = string
  default = "centralindia"
}

variable "aca_location" {
  type        = string
  default     = "koreacentral"
  description = "Container App Environment region (Central India has 0 quota for these on student subs)."
}

variable "swa_location" {
  type        = string
  default     = "eastasia"
  description = "Static Web App region (limited list: westus2, centralus, eastus2, westeurope, eastasia)."
}

variable "prefix" {
  type        = string
  default     = "cdfd"
  description = "Short (<=6 lowercase) name prefix for every resource."
}

variable "alert_email" {
  type        = string
  description = "E-mail for the $100 budget alerts."
}

variable "operator_ip" {
  type        = string
  default     = ""
  description = "Public IP allowed through the SQL firewall for one-off `alembic upgrade head`."
}

variable "sql_admin_login" {
  type    = string
  default = "cdfdadmin"
}

variable "sql_admin_password" {
  type        = string
  sensitive   = true
  description = "Azure SQL admin password. Pass via TF_VAR_sql_admin_password; never commit."
}

variable "gemini_api_key" {
  type        = string
  sensitive   = true
  description = "Gemini API key -> Key Vault. Pass via TF_VAR_gemini_api_key."
}

variable "backend_image" {
  type        = string
  description = "Backend container image. Placeholder until the first ACR build; then <acr>.azurecr.io/cdfd-backend:<tag>."
  default     = "mcr.microsoft.com/k8se/quickstart:latest"
}

variable "recreate_db" {
  type        = string
  default     = "false"
  description = "Set to \"true\" for ONE deploy to drop+recreate the DB schema, then back to false."
}

variable "frontend_origin" {
  type        = string
  default     = ""
  description = "Deployed Static Web App URL, added to backend CORS after it exists."
}
