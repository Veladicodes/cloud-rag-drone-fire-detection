#!/usr/bin/env bash
# Idle the deployment: Container App -> 0 replicas, SQL DB paused now (don't wait
# for the 60-min auto-pause). Keeps all resources + data; costs ~$0 while stopped.
# Resume with azure-start.sh.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
require_rg

echo "Scaling $APP to 0 replicas..."
"$AZ" containerapp update -g "$RG" -n "$APP" --min-replicas 0 --max-replicas 1 -o none

DB_SRV="$("$AZ" sql server list -g "$RG" --query "[0].name" -o tsv)"
echo "Pausing SQL database cdfd on $DB_SRV..."
"$AZ" sql db pause -g "$RG" -s "$DB_SRV" -n cdfd -o none 2>/dev/null \
  || echo "  (already paused or not pausable right now - it auto-pauses after 60 min anyway)"

echo "Stopped. Run cloud/scripts/azure-status.sh to confirm, azure-start.sh to resume."
