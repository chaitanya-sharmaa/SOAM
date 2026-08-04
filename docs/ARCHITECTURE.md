# Enterprise Digital Agent Platform (DAP) - Architecture Guide

## 1. Executive Summary

The **Digital Agent Platform (DAP)** is a cloud-native, event-driven, multi-agent AI execution platform hosted on **Google Cloud Platform (GCP)**. It decouples client requests, agent reasoning, tool execution, and security governance into dedicated, serverless microservices.

```
                                      GOOGLE CLOUD DAP (Data & Agent Platform)
+-------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                         |
|  +--------------------+   +------------------------------------------------------------------------------------------+  |
|  | SHARED FOUNDATION  |   | [1] GOVERNANCE & STATE                                                                   |  |
|  | - Cloud IAM        |   |     - Guardrails (Safety & Content Filter)  <-------> PingIdentity (OAuth2 / OIDC)       |  |
|  | - Secret Manager   |   |     - Firestore (Conversational / Agent State)                                           |  |
|  | - KMS (CMEK)       |   |     - Audit Logs (Cloud Logging 365-day Bucket)                                          |  |
|  | - Cloud Logging    |   +------------------------------------------------------------------------------------------+  |
|  | - Cloud Monitoring |   | [2] AGENT REGISTRY                 | [3] AGENT WORKSPACE (Project)                       |  |
|  |                    |   |     - Agent Registry Service       |     - Agent 1  <==>  Agent 1 Inbound Topic (Pub/Sub) |  |
|  |                    |   |     - Agent Registry (Cloud SQL)   |     - Agent 2  <==>  Agent 2 Inbound Topic (Pub/Sub) |  |
|  |                    |   +------------------------------------+-----------------------------------------------------+  |
|  |                    |   | [4] AGENT BACKBONE & ORCHESTRATION                                                       |  |
|  |                    |   |     - GateKeeper & GateKeeper Topic (Pub/Sub)  ==> CTT BigQuery (Analytics/Tracing)      |  |
|  |                    |   |     - MCP Gateway (Model Context Protocol)     ==> External Enterprise APIs              |  |
|  |                    |   |     - Agent Gateway & Topic (Cloud SQL / SOAM) ==> Routes to Agents & API Gateway        |  |
|  |                    |   |     - Grid Monitoring & Grid Lens (Observability & Dashboard UI)                         |  |
|  +--------------------+   +------------------------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------------------------------------------------+
                                              ^                                           |
                                              | Ingress via API Gateway                   | Egress Calls
                                              | (Cloud Armor WAF)                         v
                         +-----------------------------------+               +--------------------------+
                         | CLIENTS & CONSUMERS               |               | ENTERPRISE SERVICES      |
                         | - Internal Users & Admins         |               | - PingIdentity (IdP)     |
                         | - Business Application / BFF REST |               | - External Core APIs     |
                         |                                   |               | - LLM APIs (Vertex AI)   |
                         +-----------------------------------+               +--------------------------+
```

---

## 2. Module by Module Deep-Dive

### Module 1: Ingress & Perimeter Defense
* **Cloud Armor (INT WAF)**: Protects edge entrypoints with rate limiting, OWASP ModSecurity rule sets (SQLi, XSS, RCE), and IP filtering.
* **API Gateway**: Provides managed REST endpoints, rate limiting, and validates incoming JWT tokens issued by **PingIdentity**.
* **PingIdentity Integration**: Enterprise OIDC authority validating user authentication and authorization scopes.

### Module 2: Agent Registry Tier
* **Agent Registry (Cloud Run)**: Catalog service for discovering registered agents, versions, schemas, and allowed tools.
* **Agent Registry DB (Cloud SQL Postgres)**: Private IP relational store for catalog metadata.

### Module 3: Agent Execution Workspace
* **Agent 1 & Agent 2 (Cloud Run)**: Containerized agent reasoning runtimes.
* **Inbound Topics (Pub/Sub)**: Dedicated message queues for asynchronous task ingestion, retries, and workload smoothing.

### Module 4: Agent Backbone & Orchestration Core
* **Agent Gateway (Cloud Run + Cloud SQL)**: Central orchestration bus implementing **SOAM** (*Service Oriented Agent Messaging*).
* **GateKeeper & GateKeeper Topic (Pub/Sub + Cloud Run)**: Security enforcement proxy. Inspects prompts for prompt injection, sensitive PII leakage (DLP), and validates PingIdentity scopes.
* **MCP Gateway (Model Context Protocol)**: Secure tool execution proxy connecting Agents to **External APIs** without exposing raw credentials.
* **Grid Monitoring & Grid Lens**: Real-time OpenTelemetry trace collector and operational dashboard UI.

### Module 5: Governance & State
* **Guardrails**: Pre-execution and post-execution content moderation and safety policy engine.
* **Firestore (`Agent State`)**: Low-latency NoSQL document store for conversational memory and checkpoints.
* **CTT BigQuery**: Continuous Telemetry & Tracing data warehouse for token cost analytics, latency tracking, and audit trails.

### Module 6: Shared Foundation Security
* **Cloud IAM**: Least-privilege dedicated service accounts for every microservice.
* **Cloud KMS (CMEK)**: Customer-managed encryption keys for data at rest.
* **Secret Manager**: Secure vault for credentials, passwords, and external API keys.

---

## 3. End-to-End Workflow (Interview Talking Points)

1. **Request Ingestion**:
   * A client sends a request to the **API Gateway** through **Cloud Armor WAF**.
   * The API Gateway verifies the JWT against **PingIdentity's JWKS** endpoint and routes the request to **Agent Gateway**.

2. **Security Inspection**:
   * The **Agent Gateway** publishes the task to **GateKeeper Topic**.
   * **GateKeeper** validates payload safety with **Guardrails** and pushes clean tasks to the **Agent Inbound Topic**.

3. **Agent Reasoning & Execution**:
   * **Agent 1** pulls the message, loads conversation context from **Firestore**, and prompts the **LLM API (Vertex AI)**.
   * If a tool is required, Agent 1 calls **MCP Gateway**, which executes the tool against the **External API** using credentials from **Secret Manager**.

4. **Multi-Agent Collaboration**:
   * Agent 1 queries the **Agent Registry** to resolve **Agent 2**, and delegates subtasks via the Agent Gateway.

5. **Telemetry & Audit**:
   * Step latency and token consumption are pushed to **Grid Monitoring** and archived in **CTT BigQuery**.
   * Admins inspect live graphs in **Grid Lens**.
