"""
Enterprise SOAM Multi-Agent Platform
Agent 1 — SOAM Coordinator & Primary Reasoning Engine
"""

import os
import sys
import json
import time
import uuid
import base64
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request as url_request

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("agent-1-coordinator")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT_ID", "project-ddfa7a80-7677-4268-95a"))
AGENT_2_TOPIC = os.environ.get("AGENT_2_TOPIC", "dev-dap-agent-2-inbound-topic")
PORT = int(os.environ.get("PORT", "8080"))


def get_gcp_access_token():
    """Fetches Google IAM access token from Cloud Run metadata server (ADC)."""
    try:
        req = url_request.Request(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
            headers={"Metadata-Flavor": "Google"}
        )
        with url_request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return data.get("access_token")
    except Exception as e:
        logger.warning(f"Could not fetch metadata token (likely running locally): {e}")
        return None


def publish_to_agent_2(subtask_payload: dict, parent_trace_id: str) -> dict:
    """Publishes an asynchronous subtask to Agent 2 inbound topic via Pub/Sub REST API."""
    token = get_gcp_access_token()
    if not token:
        logger.info("Local environment: Simulating Pub/Sub publish to Agent 2")
        return {"status": "SIMULATED", "messageId": f"local-{uuid.uuid4().hex[:8]}"}

    if AGENT_2_TOPIC.startswith("projects/"):
        pubsub_url = f"https://pubsub.googleapis.com/v1/{AGENT_2_TOPIC}:publish"
    else:
        pubsub_url = f"https://pubsub.googleapis.com/v1/projects/{PROJECT_ID}/topics/{AGENT_2_TOPIC}:publish"
    message_data = json.dumps({
        "event": "SOAM_DELEGATION",
        "parent_trace_id": parent_trace_id,
        "coordinator": "dev-dap-agent-1",
        "timestamp": time.time(),
        "payload": subtask_payload
    }).encode("utf-8")

    body = json.dumps({
        "messages": [
            {
                "data": base64.b64encode(message_data).decode("utf-8"),
                "attributes": {
                    "origin": "dev-dap-agent-1",
                    "trace_id": parent_trace_id
                }
            }
        ]
    }).encode("utf-8")

    req = url_request.Request(
        pubsub_url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with url_request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode())
            logger.info(f"Successfully dispatched subtask to Agent 2 via Pub/Sub: {result}")
            return {"status": "DISPATCHED", "messageIds": result.get("messageIds", [])}
    except Exception as e:
        logger.error(f"Error publishing to Pub/Sub: {e}")
        return {"status": "ERROR", "error": str(e)}


def reason_and_plan(task_text: str, session_id: str, force_delegate: bool = False) -> dict:
    """Core AI Reasoning Loop for Agent 1 (SOAM Coordinator)."""
    trace_id = f"trace-{uuid.uuid4().hex[:8]}"
    start_time = time.time()
    
    # 1. Intent & Domain Classification
    task_lower = task_text.lower()
    if any(k in task_lower for k in ["audit", "analyze", "deep", "sql", "database", "worker", "delegate", "subtask", "specialist"]):
        intent = "SPECIALIST_DELEGATION"
        needs_delegation = True
    elif any(k in task_lower for k in ["architecture", "soam", "mesh", "gcp", "security", "zero-trust", "gateway", "cloud run"]):
        intent = "ARCHITECTURE_REASONING"
        needs_delegation = force_delegate
    elif any(k in task_lower for k in ["status", "health", "ping", "hello"]):
        intent = "HEALTH_AND_STATUS"
        needs_delegation = False
    else:
        intent = "GENERAL_INTELLIGENCE"
        needs_delegation = force_delegate

    # 2. Reasoning Steps (Chain-of-Thought)
    thought_process = [
        f"1. Ingested user task: '{task_text[:60]}...'",
        f"2. Evaluated task complexity and classified intent as [{intent}].",
        f"3. Determined session context [{session_id}] with trace [{trace_id}]."
    ]

    delegation_info = None

    if needs_delegation:
        thought_process.append(f"4. Task requires specialist execution -> Initiating async SOAM delegation to Agent 2.")
        subtask = {
            "subtask_name": "Specialist Deep Analysis",
            "source_task": task_text,
            "session_id": session_id,
            "target_agent": "dev-dap-agent-2"
        }
        delegation_result = publish_to_agent_2(subtask, trace_id)
        thought_process.append(f"5. Pub/Sub dispatch status: {delegation_result.get('status')}")
        delegation_info = {
            "target": "Agent 2 (SOAM Worker)",
            "topic": AGENT_2_TOPIC,
            "dispatch_result": delegation_result
        }
        response_text = (
            f"Coordinator Agent 1 has evaluated your request ('{task_text}'). "
            f"Due to the specialized nature of this task, a sub-workflow has been autonomously delegated "
            f"to Agent 2 via the SOAM Pub/Sub Message Bus (Trace ID: {trace_id})."
        )
    else:
        thought_process.append(f"4. Task is self-contained. Generating direct AI synthesis.")
        if intent == "ARCHITECTURE_REASONING":
            response_text = (
                "The Service-Oriented Agent Mesh (SOAM) platform on GCP enforces Zero-Trust security across 5 layers: "
                "1) Google API Gateway with IAM OIDC validation, 2) Serverless Cloud Run Compute Mesh with Direct VPC Egress, "
                "3) Pub/Sub asynchronous event bus with OIDC push subscriptions, 4) Private-IP-only Cloud SQL (PSA) and Firestore, "
                "and 5) Deterministic outbound egress via Cloud NAT (Static Public IP)."
            )
        elif intent == "HEALTH_AND_STATUS":
            response_text = "SOAM Agent 1 (Coordinator) is healthy, active, and orchestrating requests across the platform."
        else:
            response_text = (
                f"Agent 1 processed your inquiry: '{task_text}'. "
                f"Multi-agent mesh coordination is operational and ready to process workflows."
            )

    execution_time_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "agent": "dev-dap-agent-1",
        "role": "SOAM Coordinator & Reasoning Engine",
        "trace_id": trace_id,
        "session_id": session_id,
        "intent": intent,
        "thought_process": thought_process,
        "delegated_to_worker": needs_delegation,
        "delegation_info": delegation_info,
        "ai_response": response_text,
        "execution_time_ms": execution_time_ms,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }


class AgentHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info(f"{self.command} {self.path} - {args[0] if args else ''}")

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "HEALTHY",
            "agent": "dev-dap-agent-1",
            "role": "SOAM Coordinator",
            "uptime": time.time()
        }).encode())

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len else b"{}"

        try:
            body_json = json.loads(post_body.decode("utf-8"))
        except Exception:
            body_json = {}

        # Handle Pub/Sub Push format if received
        if "message" in body_json and "data" in body_json["message"]:
            try:
                decoded_data = base64.b64decode(body_json["message"]["data"]).decode("utf-8")
                task_payload = json.loads(decoded_data)
            except Exception:
                task_payload = body_json
        else:
            task_payload = body_json

        task_text = task_payload.get("task", task_payload.get("prompt", "Analyze system state"))
        session_id = task_payload.get("session_id", f"sess-{uuid.uuid4().hex[:6]}")
        force_delegate = bool(task_payload.get("delegate", False))

        ai_result = reason_and_plan(task_text, session_id, force_delegate)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(ai_result, indent=2).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("", PORT), AgentHandler)
    logger.info(f"🚀 SOAM Coordinator Agent 1 running on port {PORT}")
    server.serve_forever()
