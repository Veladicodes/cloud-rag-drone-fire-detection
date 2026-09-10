#!/usr/bin/env bash
# Resume after azure-stop.sh: wake the SQL DB, let the Container App scale on demand.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
require_rg

DB_SRV="$("$AZ" sql server list -g "$RG" --query "[0].name" -o tsv)"
echo "Resuming SQL database cdfd on $DB_SRV..."
"$AZ" sql db resume -g "$RG" -s "$DB_SRV" -n cdfd -o none 2>/dev/null \
  || echo "  (already running)"

echo "Container App $APP stays at min-replicas 0 - it wakes on the first request (a few seconds cold start)."
BACKEND="$(tf_out backend_url)"
echo "Backend: $BACKEND/health"
echo "Frontend: $(tf_out frontend_url)"
