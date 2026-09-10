#!/usr/bin/env bash
# "Stop" for this deployment is mostly automatic:
#   * the Container App is min-replicas 0 -> scales to 0 after ~5 min of no
#     traffic ($0 while idle). Nothing to do.
#   * the Serverless SQL DB auto-pauses after 60 min idle ($0 while paused).
#     (This CLI build has no `az sql db pause`; auto-pause is the only lever.)
# So this script just reports state and reminds you what still trickles.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
require_rg

echo "Container App replicas (idle target = 0):"
"$AZ" containerapp replica list -g "$RG" -n "$APP" --query "length(@)" -o tsv 2>/dev/null | sed 's/^/  /' || true

echo "SQL DB status (auto-pauses after 60 min idle):"
"$AZ" sql db list -g "$RG" --query "[].{db:name,status:status}" -o table 2>/dev/null || true

cat <<'NOTE'

Idle cost after this: ~$0/day (Log Analytics + App Insights ingestion is minutes
of data; Storage + Key Vault are pennies; ACR was deleted). Nothing to stop
manually. For a hard $0 between milestones use cloud/scripts/azure-teardown.sh.
NOTE
