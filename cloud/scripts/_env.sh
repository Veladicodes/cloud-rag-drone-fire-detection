#!/usr/bin/env bash
# Shared helpers for the azure-*.sh scripts. Source this.
set -euo pipefail

AZ="${AZ:-/c/Program Files/Microsoft SDKs/Azure/CLI2/wbin/az.cmd}"
TF="${TF:-$HOME/AppData/Local/Microsoft/WinGet/Packages/Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe/terraform.exe}"
TFDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../terraform" && pwd)"

tf_out() { "$TF" -chdir="$TFDIR" output -raw "$1" 2>/dev/null || true; }

RG="$(tf_out resource_group)"
APP="$(tf_out container_app_name)"
ACR="$(tf_out acr_login_server)"; ACR="${ACR%%.*}"
SUB="$("$AZ" account show --query id -o tsv 2>/dev/null || true)"

require_rg() {
  if [ -z "${RG:-}" ]; then
    echo "No terraform state / resource group found. Nothing deployed?" >&2
    exit 1
  fi
}
