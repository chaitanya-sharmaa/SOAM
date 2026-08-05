# Google Cloud Platform (GCP) Digital Agent Platform (DAP) Infrastructure

This repository contains production-grade, enterprise Terraform modules and **Terragrunt** live deployment configurations to provision the **Digital Agent Platform (DAP)** on **Google Cloud Platform (GCP)**.

---

## 📁 Repository Structure

```text
cloud-run/
├── .github/
│   └── workflows/
│       └── terraform-gcp.yml        # GCP GitHub Actions CI/CD Pipeline (WIF Keyless Auth)
│
├── gcp/                             # 🌐 Google Cloud Platform Implementation
│   ├── bootstrap/                   # One-time bootstrap for GCP WIF & Remote State Bucket
│   │
│   ├── live/                        # ⚡ Terragrunt Multi-Environment Deployments
│   │   ├── root.hcl                 # Global Root: GCS Remote State & Provider generation
│   │   └── dev/                     # Dev Environment DAG (Networking, Security, Compute, etc.)
│   │       ├── env.hcl              # Environment variables
│   │       ├── 01_networking/
│   │       ├── 02_security_iam/
│   │       ├── 03_data_state/
│   │       ├── 04_messaging/
│   │       ├── 05_compute_services/
│   │       ├── 06_ingress_gateway/
│   │       └── 07_observability/
│   │
│   ├── modules/                     # 📦 Reusable Terraform Modules
│   │   ├── 01_networking/           # VPC, Subnets, PSA, VPC Connector, Cloud Armor WAF
│   │   ├── 02_security_iam/         # Service Accounts, IAM Roles, Cloud KMS (CMEK), Secret Manager
│   │   ├── 03_data_state/           # Private Cloud SQL, Firestore Native DB, BigQuery (CTT Analytics)
│   │   ├── 04_messaging/            # Pub/Sub Inbound Topics & Push Subscriptions with DLQ
│   │   ├── 05_compute_services/     # Cloud Run v2 (Agents 1/2, Gateway, GateKeeper, MCP Gateway, Lens)
│   │   ├── 06_ingress_gateway/      # Google Cloud API Gateway & PingIdentity JWT Auth Specs
│   │   └── 07_observability/        # Immutable Audit Log Bucket, Sinks, Dashboards & Alerts
│   │
│   ├── environments/                # Standard Terraform Root Compositions
│   │   └── dev/
│   │
│   └── docs/
│       ├── ARCHITECTURE.md          # Architecture breakdown, network boundaries & data flows
│       ├── TERRAGRUNT.md            # Terragrunt execution guide, DAG graph & commands
│       └── RUNBOOK.md               # Deployment & operations runbook
│
├── .gitignore
└── README.md
```

---

## ⚡ Key Architectural Highlights

* **Compute**: Multi-Agent system on Cloud Run v2 sandboxes with Zero Public Ingress (`INGRESS_TRAFFIC_INTERNAL_ONLY`).
* **Ingress**: Google Cloud API Gateway with Cloud Armor edge security and PingIdentity JWT authentication.
* **Networking**: Custom VPC (`10.10.0.0/16`) with Serverless VPC Access Connector (`10.10.2.0/28`) and Private Services Access (PSA) Peering.
* **Storage & State**: Private Cloud SQL (PostgreSQL 15), Firestore Native Mode, and BigQuery Continuous Telemetry & Tracing (CTT).
* **Security & IAM**: Dedicated per-service Service Accounts, Cloud KMS Customer-Managed Encryption Keys (CMEK), and Workload Identity Federation (WIF).
* **IaC Orchestration**: Modular Terraform with **Terragrunt** to provide DRY multi-environment deployments with isolated per-module state.

---

## 🚀 Quick Navigation

- **Terragrunt Guide**: See [`gcp/docs/TERRAGRUNT.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/TERRAGRUNT.md).
- **Architecture & Network Flows**: See [`gcp/docs/ARCHITECTURE.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/ARCHITECTURE.md).
- **Deployment Runbook**: See [`gcp/docs/RUNBOOK.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/RUNBOOK.md).
