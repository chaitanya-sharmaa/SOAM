"""
Enterprise SOAM Multi-Agent Platform
Agent 1 — SOAM Coordinator & Primary Reasoning Engine (Powered by Google Vertex AI Gemini 1.5 Flash)
"""

import os
import sys
import json
import time
import uuid
import base64
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request as url_request, error as url_error

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s")
logger = logging.getLogger("agent-1-coordinator")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("PROJECT_ID", "project-ddfa7a80-7677-4268-95a"))
REGION = os.environ.get("REGION", "europe-west1")
AGENT_2_TOPIC = os.environ.get("AGENT_2_TOPIC", "dev-dap-agent-2-inbound-topic")
PORT = int(os.environ.get("PORT", "8080"))
GEMINI_MODEL = "gemini-1.5-flash"


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


def call_vertex_gemini(prompt: str, system_instruction: str = None, temperature: float = 0.2) -> dict:
    """Invokes Google Vertex AI Gemini 1.5 Flash via Native REST API with ADC."""
    token = get_gcp_access_token()
    if not token:
        logger.info("Local environment: Simulating Gemini LLM inference")
        return {
            "status": "SIMULATED",
            "model": f"{GEMINI_MODEL} (Local Simulation)",
            "text": "Simulated local LLM response."
        }

    vertex_url = f"https://{REGION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{GEMINI_MODEL}:generateContent"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 1024,
            "responseMimeType": "application/json"
        }
    }

    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    req = url_request.Request(
        vertex_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with url_request.urlopen(req, timeout=12) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            candidates = resp_data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts and "text" in parts[0]:
                    raw_text = parts[0]["text"]
                    logger.info("Successfully received live response from Vertex AI Gemini 1.5 Flash")
                    return {
                        "status": "SUCCESS",
                        "model": GEMINI_MODEL,
                        "raw_text": raw_text
                    }
            return {"status": "NO_CONTENT", "model": GEMINI_MODEL, "raw_text": "{}"}
    except Exception as e:
        logger.warning(f"Vertex AI Gemini call failed, falling back to heuristic engine: {e}")
        return {"status": "FALLBACK", "model": "heuristic-engine", "error": str(e)}


def publish_to_agent_2(subtask_payload: dict, parent_trace_id: str) -> dict:
    """Publishes an asynchronous subtask to Agent 2 inbound topic via Pub/Sub REST API."""
    token = get_gcp_access_token()
    if not token:
        logger.info("Local environment: Simulating Pub/Sub publish to Agent 2")
        return {"status": "SIMULATED", "messageIds": [f"local-{uuid.uuid4().hex[:8]}"]}

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
    """Core AI Reasoning Loop for Agent 1 using Vertex AI Gemini 1.5 Flash."""
    trace_id = f"trace-{uuid.uuid4().hex[:8]}"
    start_time = time.time()

    system_prompt = (
        "You are Agent 1 (Primary Coordinator & Reasoning Engine) of the Service-Oriented Agent Mesh (SOAM) on GCP. "
        "Your role is to evaluate user requests, formulate multi-step chain-of-thought plans, and decide whether a task "
        "can be synthesized directly or requires delegating specialist subtasks to Agent 2 (Worker Specialist for database/network/infra audits).\n"
        "Always output strict JSON with these keys:\n"
        "- intent: string ('SPECIALIST_DELEGATION' | 'ARCHITECTURE_REASONING' | 'GENERAL_SYNTHESIS' | 'HEALTH_AND_STATUS')\n"
        "- needs_delegation: boolean (true if database audit, deep specialist work, or complex multi-agent analysis is needed)\n"
        "- thought_steps: array of strings describing your chain-of-thought reasoning\n"
        "- subtask_name: string (if delegating, concise name of the delegated routine)\n"
        "- subtask_instructions: string (if delegating, detailed instructions for Agent 2)\n"
        "- response_synthesis: string (your comprehensive, professional AI answer to the user)"
    )

    user_prompt = f"User Request: {task_text}\nSession ID: {session_id}\nForce Delegate: {force_delegate}"

    llm_result = call_vertex_gemini(user_prompt, system_prompt, temperature=0.2)
    
    # Parse LLM response or fallback
    parsed_llm = None
    if llm_result.get("status") == "SUCCESS" and "raw_text" in llm_result:
        try:
            parsed_llm = json.loads(llm_result["raw_text"])
        except Exception as pe:
            logger.warning(f"Could not parse Gemini JSON output: {pe}")

    if parsed_llm:
        intent = parsed_llm.get("intent", "GENERAL_SYNTHESIS")
        needs_delegation = force_delegate or bool(parsed_llm.get("needs_delegation", False))
        thought_process = parsed_llm.get("thought_steps", [
            f"1. Ingested user task: '{task_text[:60]}...'",
            f"2. Vertex AI Gemini classified intent as [{intent}].",
            f"3. Determined session context [{session_id}] with trace [{trace_id}]."
        ])
        subtask_name = parsed_llm.get("subtask_name", "Specialist Deep Analysis")
        subtask_instructions = parsed_llm.get("subtask_instructions", task_text)
        ai_response_text = parsed_llm.get("response_synthesis", "")
    else:
        # Heuristic Fail-Safe Fallback
        task_lower = task_text.lower()
        if any(k in task_lower for k in ["audit", "analyze", "deep", "sql", "database", "worker", "delegate", "subtask", "specialist"]):
            intent = "SPECIALIST_DELEGATION"
            needs_delegation = True
        elif any(k in task_lower for k in ["architecture", "soam", "mesh", "gcp", "security", "zero-trust", "gateway", "cloud run"]):
            intent = "ARCHITECTURE_REASONING"
            needs_delegation = force_delegate
        else:
            intent = "GENERAL_SYNTHESIS"
            needs_delegation = force_delegate

        thought_process = [
            f"1. Ingested user task: '{task_text[:60]}...'",
            f"2. Evaluated task complexity and classified intent as [{intent}].",
            f"3. Determined session context [{session_id}] with trace [{trace_id}]."
        ]
        subtask_name = "Specialist Deep Analysis"
        subtask_instructions = task_text
        ai_response_text = (
            "The Service-Oriented Agent Mesh (SOAM) platform on GCP enforces Zero-Trust security across 5 layers: "
            "1) Google API Gateway with IAM OIDC validation, 2) Serverless Cloud Run Compute Mesh with Direct VPC Egress, "
            "3) Pub/Sub asynchronous event bus with OIDC push subscriptions, 4) Private-IP-only Cloud SQL (PSA) and Firestore, "
            "and 5) Deterministic outbound egress via Cloud NAT (Static Public IP)."
        )

    delegation_info = None

    if needs_delegation:
        thought_process.append("4. Task requires specialist execution -> Initiating async SOAM delegation to Agent 2.")
        subtask = {
            "subtask_name": subtask_name,
            "instructions": subtask_instructions,
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
        if not ai_response_text:
            ai_response_text = (
                f"Coordinator Agent 1 has evaluated your request ('{task_text}'). "
                f"Due to the specialized nature of this task, a sub-workflow has been autonomously delegated "
                f"to Agent 2 via the SOAM Pub/Sub Message Bus (Trace ID: {trace_id})."
            )
    else:
        thought_process.append("4. Task is self-contained. Generating direct AI synthesis.")

    execution_time_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "agent": "dev-dap-agent-1",
        "role": "SOAM Coordinator & Reasoning Engine",
        "llm_engine": llm_result.get("model", GEMINI_MODEL),
        "trace_id": trace_id,
        "session_id": session_id,
        "intent": intent,
        "thought_process": thought_process,
        "delegated_to_worker": needs_delegation,
        "delegation_info": delegation_info,
        "ai_response": ai_response_text,
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
            "llm_model": GEMINI_MODEL,
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
    logger.info(f"🚀 SOAM Coordinator Agent 1 running on port {PORT} with {GEMINI_MODEL}")
    server.serve_forever()
