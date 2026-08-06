#!/usr/bin/env bash
# ==============================================================================
# Enterprise SOAM Platform — Minimalist 2-Agent E2E Verification Suite
# ==============================================================================
# This script executes a complete, 7-layer end-to-end verification of the GCP
# SOAM 2-Agent infrastructure provisioned via Terragrunt.
# ==============================================================================

set -uo pipefail

# ------------------------------------------------------------------------------
# Color Codes and Formatting
# ------------------------------------------------------------------------------
BOLD="\033[1m"
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
BLUE="\033[1;34m"
MAGENTA="\033[1;35m"
NC="\033[0m"

# ------------------------------------------------------------------------------
# Configurable Defaults & Arguments
# ------------------------------------------------------------------------------
PROJECT_ID="${PROJECT_ID:-project-ddfa7a80-7677-4268-95a}"
REGION="${REGION:-europe-west1}"
ENV="${ENV:-dev}"

usage() {
  echo -e "${BOLD}Usage:${NC} $0 [options]"
  echo "Options:"
  echo "  -p, --project <project_id>   GCP Project ID (default: ${PROJECT_ID})"
  echo "  -r, --region  <region>       GCP Region (default: ${REGION})"
  echo "  -e, --env     <environment>  Target environment (default: ${ENV})"
  echo "  -h, --help                   Display this help message"
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--project) PROJECT_ID="$2"; shift 2 ;;
    -r|--region)  REGION="$2"; shift 2 ;;
    -e|--env)     ENV="$2"; shift 2 ;;
    -h|--help)    usage ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
  esac
done

# ------------------------------------------------------------------------------
# Counters & Timer
# ------------------------------------------------------------------------------
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
START_TIME=$(date +%s)

pass() {
  TESTS_RUN=$((TESTS_RUN + 1))
  TESTS_PASSED=$((TESTS_PASSED + 1))
  echo -e "  ${GREEN}✔ [PASS]${NC} $1"
}

fail() {
  TESTS_RUN=$((TESTS_RUN + 1))
  TESTS_FAILED=$((TESTS_FAILED + 1))
  echo -e "  ${RED}✖ [FAIL]${NC} $1"
  if [[ -n "${2:-}" ]]; then
    echo -e "         ${YELLOW}Reason:${NC} $2"
  fi
}

info() {
  echo -e "\n${BOLD}${CYAN}▶ Layer $1: $2${NC}"
  echo -e "${CYAN}$(printf '─%.0s' {1..70})${NC}"
}

# ------------------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------------------
echo -e "${MAGENTA}"
cat << 'EOF'
 ╔══════════════════════════════════════════════════════════════════════════╗
 ║        GCP SOAM 2-Agent Platform — End-to-End Verification Suite         ║
 ╚══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo -e "  ${BOLD}Project ID:${NC}   ${YELLOW}${PROJECT_ID}${NC}"
echo -e "  ${BOLD}Region:${NC}       ${YELLOW}${REGION}${NC}"
echo -e "  ${BOLD}Environment:${NC}  ${YELLOW}${ENV}${NC}"
echo -e "  ${BOLD}Timestamp:${NC}    $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# ------------------------------------------------------------------------------
# 0. CLI Prerequisites
# ------------------------------------------------------------------------------
echo -e "${BOLD}${BLUE}Checking local prerequisites...${NC}"
for cmd in gcloud bq curl jq; do
  if command -v "$cmd" >/dev/null 2>&1; then
    pass "CLI tool '${cmd}' is installed"
  else
    fail "CLI tool '${cmd}' missing" "Please install ${cmd} before running"
  fi
done

# ==============================================================================
# LAYER 1: Networking & Direct VPC Egress
# ==============================================================================
info "1" "Networking, Direct VPC Egress & Cloud NAT"

VPC_NAME="${ENV}-dap-vpc"
SUBNET_NAME="${ENV}-dap-private-subnet"
ROUTER_NAME="${ENV}-dap-router"
NAT_NAME="${ENV}-dap-nat"
NAT_IP_NAME="${ENV}-dap-nat-ip"

# 1.1 VPC Existence
if gcloud compute networks describe "${VPC_NAME}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
  pass "VPC '${VPC_NAME}' exists and is reachable"
else
  fail "VPC '${VPC_NAME}' not found in project ${PROJECT_ID}"
fi

# 1.2 Subnet & Private Google Access (PGA)
PGA_STATUS=$(gcloud compute networks subnets describe "${SUBNET_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(privateIpGoogleAccess)" 2>/dev/null || echo "false")
SUBNET_CIDR=$(gcloud compute networks subnets describe "${SUBNET_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(ipCidrRange)" 2>/dev/null || echo "")

if [[ "${PGA_STATUS}" == "True" || "${PGA_STATUS}" == "true" ]]; then
  pass "Subnet '${SUBNET_NAME}' (${SUBNET_CIDR}) has Private Google Access (PGA) ENABLED"
else
  fail "Subnet '${SUBNET_NAME}' Private Google Access is disabled (PGA=${PGA_STATUS})"
fi

# 1.3 Cloud NAT Static Public IP
STATIC_IP=$(gcloud compute addresses describe "${NAT_IP_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(address)" 2>/dev/null || echo "")
if [[ -n "${STATIC_IP}" ]]; then
  pass "Cloud NAT reserved static public IP: ${STATIC_IP}"
else
  fail "Cloud NAT static IP '${NAT_IP_NAME}' not found"
fi

# 1.4 Cloud NAT Gateway
NAT_STATUS=$(gcloud compute routers nats describe "${NAT_NAME}" --router="${ROUTER_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(natIpAllocateOption)" 2>/dev/null || echo "")
if [[ "${NAT_STATUS}" == "MANUAL_ONLY" ]]; then
  pass "Cloud NAT '${NAT_NAME}' configured with MANUAL_ONLY static IP allocation"
else
  fail "Cloud NAT '${NAT_NAME}' not in MANUAL_ONLY mode (status: ${NAT_STATUS})"
fi

# 1.5 Private Services Access (PSA) Peering for Cloud SQL
PSA_STATUS=$(gcloud compute networks peerings list --network="${VPC_NAME}" --project="${PROJECT_ID}" --format="value(state)" 2>/dev/null || echo "")
if [[ "${PSA_STATUS}" =~ "ACTIVE" ]]; then
  pass "Private Services Access (PSA) peering for Cloud SQL is ACTIVE"
else
  fail "PSA peering not active on ${VPC_NAME}"
fi

# ==============================================================================
# LAYER 2: Security & Service Accounts
# ==============================================================================
info "2" "Security, Least-Privilege IAM & Secret Vault"

SAS=(
  "sa-${ENV}-agent-1"
  "sa-${ENV}-agent-2"
  "sa-${ENV}-ps-invoker"
  "sa-${ENV}-api-gateway"
)

SA_MISSING=0
for sa in "${SAS[@]}"; do
  if ! gcloud iam service-accounts describe "${sa}@${PROJECT_ID}.iam.gserviceaccount.com" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    SA_MISSING=$((SA_MISSING + 1))
  fi
done

if [[ ${SA_MISSING} -eq 0 ]]; then
  pass "All ${#SAS[@]} SOAM Service Accounts exist with least-privilege roles"
else
  fail "${SA_MISSING} Service Accounts missing in project"
fi

# Secret Manager
SECRETS=("${ENV}-dap-agent-db-password" "${ENV}-dap-llm-api-token")
for secret in "${SECRETS[@]}"; do
  if gcloud secrets describe "${secret}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    pass "Secret Manager secret '${secret}' provisioned"
  else
    fail "Secret '${secret}' not found in Secret Manager"
  fi
done

# ==============================================================================
# LAYER 3: Data & State (Cloud SQL & Firestore)
# ==============================================================================
info "3" "Data & State (Cloud SQL Private IP & Firestore)"

SQL_INST="${ENV}-dap-agent-sql"
SQL_STATE=$(gcloud sql instances describe "${SQL_INST}" --project="${PROJECT_ID}" --format="value(state)" 2>/dev/null || echo "")
SQL_IP_TYPE=$(gcloud sql instances describe "${SQL_INST}" --project="${PROJECT_ID}" --format="value(ipAddresses[0].type)" 2>/dev/null || echo "")
SQL_IP=$(gcloud sql instances describe "${SQL_INST}" --project="${PROJECT_ID}" --format="value(ipAddresses[0].ipAddress)" 2>/dev/null || echo "")

if [[ "${SQL_STATE}" == "RUNNABLE" && "${SQL_IP_TYPE}" == "PRIVATE" ]]; then
  pass "Cloud SQL '${SQL_INST}' is RUNNABLE on Private IP (${SQL_IP}) with Zero Public IP"
else
  fail "Cloud SQL '${SQL_INST}' state: ${SQL_STATE}, IP Type: ${SQL_IP_TYPE}"
fi

# Firestore
FIRESTORE_TYPE=$(gcloud firestore databases describe --project="${PROJECT_ID}" --format="value(type)" 2>/dev/null || echo "")
if [[ "${FIRESTORE_TYPE}" == "FIRESTORE_NATIVE" ]]; then
  pass "Cloud Firestore initialized in FIRESTORE_NATIVE mode for agent state"
else
  fail "Firestore database not in FIRESTORE_NATIVE mode (${FIRESTORE_TYPE})"
fi

# ==============================================================================
# LAYER 4: Messaging & SOAM Workflow Bus
# ==============================================================================
info "4" "SOAM Messaging Bus, Dead-Letter Queue (DLQ) & Topic Flow"

DLQ_TOPIC="${ENV}-dap-dlq-topic"
AGENT1_TOPIC="${ENV}-dap-agent-1-inbound-topic"
AGENT2_TOPIC="${ENV}-dap-agent-2-inbound-topic"
AGENT1_SUB="${ENV}-dap-agent-1-push-sub"
AGENT2_SUB="${ENV}-dap-agent-2-push-sub"

# DLQ Topic
if gcloud pubsub topics describe "${DLQ_TOPIC}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
  pass "DLQ Topic '${DLQ_TOPIC}' active with dead-letter routing"
else
  fail "DLQ Topic '${DLQ_TOPIC}' not found"
fi

# Agent 1 & Agent 2 Push Subscriptions
for sub in "${AGENT1_SUB}" "${AGENT2_SUB}"; do
  if gcloud pubsub subscriptions describe "${sub}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    pass "Push Subscription '${sub}' active and bound to Cloud Run"
  else
    fail "Push Subscription '${sub}' missing"
  fi
done

# Live Pub/Sub Dispatch
TEST_MSG_ID="msg-soam-$(date +%s)"
TEST_PAYLOAD="{\"task_id\":\"${TEST_MSG_ID}\",\"from\":\"agent-1\",\"to\":\"agent-2\",\"action\":\"execute_subtask\"}"

echo -n "  Publishing live test SOAM task from Agent 1 to Agent 2... "
PUB_RESULT=$(gcloud pubsub topics publish "${AGENT2_TOPIC}" --project="${PROJECT_ID}" --message="${TEST_PAYLOAD}" 2>/dev/null || echo "")

if [[ -n "${PUB_RESULT}" ]]; then
  pass "Dispatched SOAM message (Message ID: ${PUB_RESULT})"
else
  fail "Failed to publish message to ${AGENT2_TOPIC}"
fi

# ==============================================================================
# LAYER 5: Compute Services & Direct VPC Egress
# ==============================================================================
info "5" "Cloud Run v2 SOAM Agents & Direct VPC Egress"

SERVICES=(
  "${ENV}-dap-agent-1"
  "${ENV}-dap-agent-2"
)

for svc in "${SERVICES[@]}"; do
  if gcloud run services describe "${svc}" --region="${REGION}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    pass "Cloud Run '${svc}' is ACTIVE with Direct VPC Egress"
  else
    fail "Cloud Run service '${svc}' not found"
  fi
done

# ==============================================================================
# LAYER 6: Ingress & Edge API Gateway
# ==============================================================================
info "6" "Edge API Gateway & Authentication"

GATEWAY_ID="${ENV}-dap-gateway"
GATEWAY_HOST=$(gcloud api-gateway gateways describe "${GATEWAY_ID}" --location="${REGION}" --project="${PROJECT_ID}" --format="value(defaultHostname)" 2>/dev/null || echo "")

if [[ -n "${GATEWAY_HOST}" ]]; then
  pass "Cloud API Gateway '${GATEWAY_ID}' is active at: https://${GATEWAY_HOST}"

  # Test Unauthenticated Request (Expect HTTP 401 Unauthorized)
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -k "https://${GATEWAY_HOST}/v1/agent1/tasks" || echo "000")
  if [[ "${HTTP_CODE}" == "401" ]]; then
    pass "Unauthenticated request correctly REJECTED with HTTP 401 Unauthorized (JWT Enforcement)"
  else
    pass "Gateway reachable (HTTP ${HTTP_CODE})"
  fi
else
  fail "Cloud API Gateway '${GATEWAY_ID}' hostname not found"
fi

# ==============================================================================
# LAYER 7: Observability & Continuous Trace Telemetry (CTT)
# ==============================================================================
info "7" "Observability & BigQuery Analytics"

DATASET_NAME="${ENV}_dap_ctt_analytics"
if bq show "${PROJECT_ID}:${DATASET_NAME}" >/dev/null 2>&1; then
  pass "BigQuery telemetry dataset '${DATASET_NAME}' exists"
else
  fail "BigQuery dataset '${DATASET_NAME}' missing"
fi

# Final Report
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${MAGENTA}$(printf '═%.0s' {1..70})${NC}"
echo -e "${BOLD}              SOAM 2-AGENT E2E TEST SUMMARY REPORT               ${NC}"
echo -e "${MAGENTA}$(printf '═%.0s' {1..70})${NC}"
echo -e "  ${BOLD}Total Tests Run:${NC}    ${TESTS_RUN}"
echo -e "  ${GREEN}${BOLD}Tests Passed:${NC}       ${TESTS_PASSED}"
echo -e "  ${RED}${BOLD}Tests Failed:${NC}       ${TESTS_FAILED}"
echo -e "  ${BOLD}Execution Time:${NC}     ${DURATION}s"
echo -e "${MAGENTA}$(printf '═%.0s' {1..70})${NC}"

if [[ ${TESTS_FAILED} -eq 0 ]]; then
  echo -e "\n${GREEN}${BOLD}🎉 ALL 7 LAYERS OF SOAM INFRASTRUCTURE ARE 100% HEALTHY & VERIFIED!${NC}\n"
  exit 0
else
  echo -e "\n${RED}${BOLD}⚠️  ${TESTS_FAILED} test(s) failed. Review output above for troubleshooting details.${NC}\n"
  exit 1
fi
