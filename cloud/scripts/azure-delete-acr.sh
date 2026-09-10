#!/usr/bin/env bash
# ACR Basic is the only resource that bills 24/7 (~$0.17/day). Once the backend
# image is running in the Container App (which caches it), the registry is dead
# weight. This removes it from Azure AND from terraform state so a later `apply`
# doesn't recreate it. Re-add by `git checkout` on main.tf + `terraform apply`
# when you need to push a new image.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
require_rg

FULL_ACR="$("$AZ" acr list -g "$RG" --query "[0].name" -o tsv)"
[ -z "$FULL_ACR" ] && { echo "No ACR in $RG - nothing to do."; exit 0; }

echo "Deleting ACR $FULL_ACR ..."
"$AZ" acr delete -g "$RG" -n "$FULL_ACR" --yes -o none

echo "Dropping ACR-linked resources from terraform state so 'apply' won't recreate them..."
for addr in azurerm_container_registry.acr azurerm_role_assignment.backend_acr; do
  "$TF" -chdir="$TFDIR" state rm "$addr" 2>/dev/null || true
done
echo "Done. The Container App keeps running the cached image."
echo "To push a new image later: git checkout cloud/terraform/main.tf && terraform apply, then az acr build."
