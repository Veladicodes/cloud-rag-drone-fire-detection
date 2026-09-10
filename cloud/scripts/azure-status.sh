#!/usr/bin/env bash
# Spend + resource snapshot. Run at the start and end of every Azure session.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"

echo "== Subscription =="
"$AZ" account show --query "{name:name, id:id, state:state}" -o table

echo; echo "== Cost this billing period (USD) =="
"$AZ" consumption usage list --query "[].{svc:instanceName, cost:pretaxCost, cur:currency}" -o table 2>/dev/null \
  | awk 'NR<=1{print;next}{s+=$2;print} END{printf "%-40s %10.2f\n","TOTAL", s}' || \
  echo "  (consumption API not ready yet - check the Cost Management + Budgets blade in the portal)"

if [ -n "${RG:-}" ]; then
  echo; echo "== Resources in $RG =="
  "$AZ" resource list -g "$RG" --query "[].{name:name, type:type, location:location}" -o table
  echo; echo "== SQL DB status =="
  "$AZ" sql db list -g "$RG" --query "[].{db:name, status:status}" -o table 2>/dev/null || true
  echo; echo "== Container App replicas =="
  "$AZ" containerapp replica list -g "$RG" -n "$APP" --query "length(@)" -o tsv 2>/dev/null | \
    sed 's/^/  running replicas: /' || true
else
  echo; echo "(no terraform state - nothing deployed)"
fi
