# Digital Agent Platform (DAP) — GCP Infrastructure

> Production-grade, enterprise multi-agent AI platform on **Google Cloud Platform** using **Terraform**, **Terragrunt**, and **GitHub Actions (WIF Keyless CI/CD)**.

---

## 🏗️ Platform Architecture

### VPC Network Topology & Connectivity

![GCP DAP — VPC Network Topology & Connectivity](https://raw.githubusercontent.com/chaitanya-sharmaa/SOAM/grunt/gcp/docs/gcp_vpc_network_diagram.png)

### SOAM — Service Oriented Agent Messaging

![SOAM — Service Oriented Agent Messaging](https://raw.githubusercontent.com/chaitanya-sharmaa/SOAM/grunt/gcp/docs/soam_architecture_diagram.png)

### Hop-by-Hop Packet & Connection Lifecycle

![GCP DAP — Hop-by-Hop Packet Lifecycle](https://raw.githubusercontent.com/chaitanya-sharmaa/SOAM/grunt/gcp/docs/gcp_hop_by_hop_diagram.png)

### Terragrunt Multi-Environment IaC & GitOps CI/CD

![GCP DAP — Terragrunt CI/CD Pipeline](https://raw.githubusercontent.com/chaitanya-sharmaa/SOAM/grunt/gcp/docs/terragrunt_multienv_cicd_diagram.png)

---

## ⚡ Key Architectural Highlights

| Area | Design Decision | Benefit |
| :--- | :--- | :--- |
| **SOAM Orchestration** | Async Pub/Sub dispatch + sync fallback via Agent Gateway | Decoupled, fault-tolerant multi-agent task routing |
| **Zero Trust Ingress** | All Cloud Run: `INGRESS_TRAFFIC_INTERNAL_ONLY` | No direct public exposure to any microservice |
| **Direct VPC Egress** | `network_interfaces` block — Cloud Run IPs from `snet-private-workload` | Eliminates e2-micro connector VMs, removes ~2ms latency per hop |
| **Static NAT Egress** | Cloud NAT `MANUAL_ONLY` with reserved static IP | Deterministic allowlistable IP for enterprise firewall rules |
| **Private DB Access** | Cloud SQL `ipv4_enabled = false` via PSA Peering | Database never reachable from public internet |
| **PGA Zero NAT** | `private_ip_google_access = true` on subnet | BigQuery, Firestore, Pub/Sub, KMS all via Google internal SDN |
| **CMEK Everywhere** | KMS keys for SQL, Pub/Sub, BigQuery, GCS, Secrets | Customer-controlled encryption across all data stores |
| **Keyless CI/CD** | GitHub Actions WIF — no long-lived service account keys | Zero key management risk in CI/CD pipeline |
| **Idempotent Messaging** | Pub/Sub: 300s ACK, 5-retry DLQ, 10s–600s backoff | No silent task loss — failed tasks go to forensic DLQ |
| **Multi-Agent Collaboration** | Agents delegate sub-tasks back through SOAM bus | Horizontal scale without point-to-point coupling |

---

## 📁 Repository Structure

```text
SOAM/
├── .github/
│   └── workflows/
│       └── terragrunt-gcp.yml        # GitOps CI/CD: WIF auth, plan/apply/destroy per env
│
├── apps/                             # Application Microservices & AI Agent Logic
│   ├── coordinator/                  # Agent 1: Coordinator & Reasoning Engine (Gemini 1.5 Flash)
│   │   ├── Dockerfile
│   │   └── main.py
│   └── worker/                       # Agent 2: Specialist Worker & Diagnostics Engine
│       ├── Dockerfile
│       └── main.py
│
├── infra/                            # Infrastructure as Code (Terraform + Terragrunt)
│   ├── bootstrap/                    # One-time: WIF setup & GCS remote state bucket
│   │
│   ├── live/                         # Terragrunt live environments
│   │   ├── root.hcl                  # Global: GCS remote state, provider, WIF
│   │   ├── dev/                      # 🧪 Dev  — project: dev-dap    | subnet: 10.10.1.0/24
│   │   ├── staging/                  # 🚀 Staging — project: staging-dap | subnet: 10.20.1.0/24
│   │   └── prod/                     # 🛡️  Prod  — project: prod-dap  | subnet: 10.30.1.0/22 (HA)
│   │       └── [01..07]/terragrunt.hcl
│   │
│   └── modules/                      # Reusable Terraform modules (source of truth)
│       ├── 01_networking/            # VPC, snet-private-workload, PSA, Cloud NAT (static IP)
│       ├── 02_security_iam/          # Service Accounts, IAM roles, Secret Manager
│       ├── 03_data_state/            # Cloud SQL (Private IP), Firestore, BigQuery
│       ├── 04_messaging/             # SOAM Pub/Sub topics, DLQ, push subscriptions
│       ├── 05_compute_services/      # Cloud Run v2 (2-Agent Mesh), Direct VPC Egress
│       ├── 06_ingress_gateway/       # Cloud API Gateway + Google IAM OIDC OpenAPI spec
│       └── 07_observability/         # BigQuery telemetry dataset, Logging sinks, Alerts
│
├── scripts/                          # Operational & Validation Tooling
│   ├── live_platform_deep_test.sh    # Deep-dive 8-layer test with live log streaming
│   ├── test_e2e.sh                   # Comprehensive regression validation
│   └── verify_agent_delegation.sh    # Pub/Sub delegation verification
│
├── docs/                             # Architecture Specs, Blueprints & Runbooks
│   ├── ARCHITECTURE.md               # Full architecture: SOAM, VPC, hops, module map
│   ├── TERRAGRUNT.md                 # Terragrunt guide, DAG, CLI cheat sheet
│   └── RUNBOOK.md                    # Step-by-step deployment & operational runbook
│
└── README.md
```

---

## 🤖 SOAM — Service Oriented Agent Messaging

SOAM is the core orchestration pattern of this platform — an **async-first, event-driven** architecture that enables scalable and auditable multi-agent task routing.

```text
Client
  └─→ Cloud API Gateway (Google IAM / OIDC JWT)
        └─→ Agent 1 (Coordinator Powered by Gemini 1.5 Flash)
              │
              ├─ Direct Synthesis? ─────────────────────────→ Sync HTTP response
              │
              └─ Specialist Task? ──→ [agent-2-inbound-topic]
                                        │
                               [Agent 2 (Worker Powered by Gemini)]
                                        │
                               Agent 2 (Cloud Run)
                                 ├─→ Cloud SQL  (100% Private PSA Peering)
                                 ├─→ Firestore  (PGA — Zero NAT)
                                 ├─→ Cloud NAT  (Static Outbound IP)
                                 └─→ BigQuery   (Telemetry Dataset)
```

---

## 🚀 CI/CD GitOps Workflow

| Git Event | Environment | Action |
| :--- | :--- | :--- |
| PR to `develop` | dev | `terragrunt plan` (plan only) |
| Merge to `develop` | dev | `terragrunt apply` (auto) |
| PR to `staging` | staging | `terragrunt plan` (plan only) |
| Merge to `staging` | staging | `terragrunt apply` (auto) |
| PR to `main` | prod | `terragrunt plan` (plan only) |
| Merge to `main` + **Reviewer Approval** | prod | `terragrunt apply` (gated) |
| `workflow_dispatch` | any | manual plan/apply/destroy |

**Auth**: All runs use **Workload Identity Federation (WIF)** — zero service account key files.

---

## 💻 Quick Start

```bash
# Plan the full dev environment (topological order, all 7 modules)
cd infra/live/dev
terragrunt run --all plan

# Apply dev end-to-end
terragrunt run --all apply

# Run the live 8-layer deep platform verification suite
cd scripts
./live_platform_deep_test.sh

# View module dependency graph
cd infra/live/dev
terragrunt dag graph
```

---

## 📖 Documentation

| Document | Description |
| :--- | :--- |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Full architecture: SOAM, VPC topology, hop-by-hop lifecycle, module map |
| [`docs/TERRAGRUNT.md`](docs/TERRAGRUNT.md) | Terragrunt deep-dive, DAG, CLI cheat sheet |
| [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | Step-by-step deployment & operational runbook |
