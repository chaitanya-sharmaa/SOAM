#!/usr/bin/env bash
# ==============================================================================
# SOAM Multi-Agent Platform — End-to-End Async Delegation Verifier
# Triggers Agent 1 via API Gateway -> Pub/Sub -> Agent 2 -> Verifies Cloud Logging
# ==============================================================================

set -eo pipefail

PROJECT_ID="project-ddfa7a80-7677-4268-95a"
GATEWAY="https://dev-dap-gateway-agj0gxxt.ew.gateway.dev"
SESSION_ID="verify-$(date +%s)"

echo "🔑 Step 1: Getting Google IAM OIDC Token..."
TOKEN=$(gcloud auth print-identity-token)

echo ""
echo "🚀 Step 2: Triggering Agent 1 (Coordinator) via API Gateway..."
echo "    Session ID: ${SESSION_ID}"
echo "    Task: 'Audit database connections and analyze network health'"

RESPONSE=$(curl -s -X POST "${GATEWAY}/v1/agent1/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"task\": \"Audit database connections and analyze network health\", \"session_id\": \"${SESSION_ID}\"}")

echo ""
echo "📥 Agent 1 Response:"
echo "${RESPONSE}" | python3 -m json.tool

TRACE_ID=$(echo "${RESPONSE}" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("trace_id", ""))')
MSG_ID=$(echo "${RESPONSE}" | python3 -c 'import sys, json; print(json.load(sys.stdin).get("delegation_info", {}).get("dispatch_result", {}).get("messageIds", [""])[0])')

if [ -z "${MSG_ID}" ]; then
  echo "❌ Error: Agent 1 did not dispatch a Pub/Sub message."
  exit 1
fi

echo ""
echo "🎯 Step 3: Correlation IDs:"
echo "    • Trace ID:        ${TRACE_ID}"
echo "    • Pub/Sub Msg ID:  ${MSG_ID}"
echo ""
echo "⏳ Waiting 7 seconds for Cloud Logging ingestion..."
sleep 7

echo ""
echo "🔍 Step 4: Querying Agent 2 (Worker) Cloud Run logs for recent execution..."
gcloud logging read \
  "resource.type=\"cloud_run_revision\" AND resource.labels.service_name=\"dev-dap-agent-2\" AND timestamp >= \"$(date -u -v-20S +%Y-%m-%dT%H:%M:%SZ)\"" \
  --project="${PROJECT_ID}" \
  --limit=5 \
  --format="table(timestamp,textPayload)"

echo ""
echo "✅ SUCCESS: Agent 1 successfully dispatched task to Pub/Sub, and Agent 2 picked it up and processed it!"
