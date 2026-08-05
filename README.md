# Google Cloud Platform (GCP) Digital Agent Platform (DAP) Infrastructure

Production-grade, enterprise Infrastructure-as-Code (IaC) repository orchestrating the **Digital Agent Platform (DAP)** on **Google Cloud Platform (GCP)** using **Terraform modules**, **Terragrunt multi-environment live state**, and **GitHub Actions Keyless CI/CD (Workload Identity Federation)**.

---

## 🎨 Platform Architecture & CI/CD Orchestration

![Terragrunt Multi-Environment CI/CD Orchestration](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/terragrunt_multienv_cicd_diagram.png)

---

## 📁 Repository Structure

```text
cloud-run/
├── .github/
│   └── workflows/
│       └── terragrunt-gcp.yml       # Branch-aware multi-env CI/CD Pipeline (WIF Keyless Auth)
│
├── gcp/                             # 🌐 Google Cloud Platform Implementation
│   ├── bootstrap/                   # One-time bootstrap for GCP WIF & Remote State Bucket
│   │
│   ├── live/                        # ⚡ Terragrunt Multi-Environment Deployments
│   │   ├── root.hcl                 # 🌐 Global Root: Auto GCS Remote State & Provider generation
│   │   │
│   │   ├── dev/                     # 🧪 Development Environment (my-dap-gcp-dev)
│   │   │   ├── env.hcl              # CIDR: 10.10.1.0/24, DB: 2 vCPU, :latest tags
│   │   │   ├── 01_networking/
│   │   │   ├── 02_security_iam/
│   │   │   ├── 03_data_state/
│   │   │   ├── 04_messaging/
│   │   │   ├── 05_compute_services/
│   │   │   ├── 06_ingress_gateway/
│   │   │   └── 07_observability/
│   │   │
│   │   ├── staging/                 # 🚀 Staging Environment (my-dap-gcp-staging)
│   │   │   ├── env.hcl              # CIDR: 10.20.1.0/24, DB: 4 vCPU, :staging tags
│   │   │   └── ... (01 through 07)
│   │   │
│   │   └── prod/                    # 🛡️ Production Environment (my-dap-gcp-prod)
│   │       ├── env.hcl              # CIDR: 10.30.1.0/24, DB: 8 vCPU (HA), :v1.0.0 tags
│   │       └── ... (01 through 07)
│   │
│   ├── modules/                     # 📦 Reusable Terraform Modules (Source of Truth)
│   │   ├── 01_networking/           # VPC, Subnets, PSA Peering, VPC Connector, Cloud Armor WAF
│   │   ├── 02_security_iam/         # Service Accounts, IAM Roles, Cloud KMS (CMEK), Secret Manager
│   │   ├── 03_data_state/           # Private Cloud SQL (PostgreSQL 15), Firestore Native, BigQuery CTT
│   │   ├── 04_messaging/            # Pub/Sub Inbound Topics & Push Subscriptions with DLQ
│   │   ├── 05_compute_services/     # Cloud Run v2 (Agents 1/2, Gateway, GateKeeper, MCP Gateway, Lens)
│   │   ├── 06_ingress_gateway/      # Google Cloud API Gateway & PingIdentity JWT Auth Specs
│   │   └── 07_observability/        # Immutable Audit Log Bucket, Sinks, Dashboards & Alerts
│   │
│   └── docs/
│       ├── ARCHITECTURE.md          # Network boundaries, packet lifecycles & data flow diagrams
│       ├── TERRAGRUNT.md            # In-depth Terragrunt guide, DAG dependency graph & CLI cheat sheet
│       └── RUNBOOK.md               # Step-by-step deployment and operational runbook
│
├── .gitignore
└── README.md
```

---

## ⚡ Key Architectural Highlights

* **Multi-Agent Compute**: Microservices on Cloud Run v2 with Zero Public Ingress (`INGRESS_TRAFFIC_INTERNAL_ONLY`) communicating securely over Google internal service meshes.
* **Edge Ingress**: Google Cloud API Gateway with Cloud Armor WAF and PingIdentity JWT authentication.
* **Network Isolation**: Custom VPC with Serverless VPC Access Connector and Private Services Access (PSA) Peering.
* **Enterprise State & Data**: Private Cloud SQL (PostgreSQL 15), Firestore Native Mode, and BigQuery Continuous Telemetry & Tracing (CTT) analytics via Private Google Access (PGA).
* **Keyless Security**: Cloud KMS Customer-Managed Encryption Keys (CMEK), per-service least-privilege IAM, and GitHub Actions Workload Identity Federation (WIF).
* **DRY Multi-Environment Orchestration**: **Terragrunt** eliminates boilerplate and orchestrates `dev`, `staging`, and `prod` with isolated state and automated dependency resolution (DAG).

---

## 💻 Quick Start with Terragrunt

### 1. View Dependency Graph
```bash
cd gcp/live/dev
terragrunt dag graph
```

### 2. Plan and Deploy Dev
```bash
cd gcp/live/dev

# Topological plan across all 7 units
terragrunt run --all plan

# Deploy the entire environment
terragrunt run --all apply
```

### 3. Target a Single Module
```bash
cd gcp/live/dev/05_compute_services
terragrunt apply
```

---

## 🚀 CI/CD GitOps Workflow

The repository includes an automated GitHub Actions pipeline at [`.github/workflows/terragrunt-gcp.yml`](file:///Users/chasharm4/gcp-arch/cloud-run/.github/workflows/terragrunt-gcp.yml):

* **Pull Request to `develop`** ➔ Dynamically plans only **`dev`**
* **Pull Request to `staging`** ➔ Dynamically plans only **`staging`**
* **Pull Request to `main`** ➔ Dynamically plans only **`prod`**
* **Merge to `develop`** ➔ Auto-applies to **`dev`**
* **Merge to `staging`** ➔ Auto-applies to **`staging`**
* **Merge to `main`** ➔ Auto-applies to **`prod`**

---

## 📖 Documentation Index

- **Terragrunt Deep Dive**: [`gcp/docs/TERRAGRUNT.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/TERRAGRUNT.md)
- **GCP Architecture & Network Flows**: [`gcp/docs/ARCHITECTURE.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/ARCHITECTURE.md)
- **Deployment Runbook**: [`gcp/docs/RUNBOOK.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/RUNBOOK.md)
