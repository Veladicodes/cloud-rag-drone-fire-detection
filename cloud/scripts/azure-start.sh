#!/usr/bin/env bash
# "Resume" is automatic too: the first HTTP request to the backend wakes the
# Container App (a few-second cold start) and that query wakes the Serverless SQL
# DB. This script just warms both and prints the URLs.
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
require_rg

BACKEND="$(tf_out backend_url)"
echo "Warming $BACKEND/health ..."
curl -s -m 90 "$BACKEND/health" ; echo
echo
echo "Backend : $BACKEND"
echo "Frontend: $(tf_out frontend_url)"
echo "Run a live demo:  python testing/simulate_drone.py --api $BACKEND"
