variable "subscription_id" {
  type        = string
  description = "Azure subscription ID (from `az account show`)."
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "prefix" {
  type        = string
  default     = "cdfd"
  description = "Short name prefix for all resources (cloud-drone-fire-detection)."
}

variable "sql_admin_login" {
  type    = string
  default = "cdfdadmin"
}

variable "sql_admin_password" {
  type        = string
  sensitive   = true
  description = "Azure SQL admin password. Set via TF_VAR_sql_admin_password, do not commit."
}

variable "gemini_api_key" {
  type        = string
  sensitive   = true
  description = "Gemini API key to store in Key Vault. Set via TF_VAR_gemini_api_key."
}

variable "backend_image" {
  type        = string
  description = "Fully-qualified backend container image (e.g. <acr>.azurecr.io/cdfd-backend:latest)."
  default     = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" # placeholder until first push
}

variable "frontend_origin" {
  type        = string
  default     = ""
  description = "Deployed frontend URL, added to backend CORS once the Static Web App exists."
}
