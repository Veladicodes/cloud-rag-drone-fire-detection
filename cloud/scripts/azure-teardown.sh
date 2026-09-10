#!/usr/bin/env bash
# Full teardown -> $0. Destroys every resource in the RG. DB data is lost (demo
# only). Bring it all back with `terraform apply` (~10 min).
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"

echo "This will DESTROY every Azure resource for this project."
"$AZ" resource list -g "${RG:-<none>}" --query "[].name" -o table 2>/dev/null || true
read -r -p "Type 'destroy' to continue: " ans
[ "$ans" = "destroy" ] || { echo "aborted"; exit 1; }

"$TF" -chdir="$TFDIR" destroy -auto-approve

# Purge the soft-deleted Key Vault so the name can be reused immediately.
KV_NAME="$(tf_out key_vault_name)"
[ -n "$KV_NAME" ] && "$AZ" keyvault purge -n "$KV_NAME" -o none 2>/dev/null || true
echo "Teardown complete. Spend should return to ~\$0."
