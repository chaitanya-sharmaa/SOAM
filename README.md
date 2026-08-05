# Multi-Cloud Enterprise Digital Agent Platform (DAP) Infrastructure

This repository contains production-grade, enterprise Terraform modules, architecture specifications, and GitHub Actions CI/CD pipelines to provision the **Digital Agent Platform (DAP)** across both **Google Cloud Platform (GCP)** and **Microsoft Azure**.

---

## 📁 Repository Structure

```
cloud-run/
├── .github/
│   └── workflows/
│       ├── terraform-gcp.yml        # GCP GitHub Actions CI/CD Pipeline (WIF Keyless Auth)
│       └── terraform-azure.yml      # Azure GitHub Actions CI/CD Pipeline (OIDC Keyless Auth)
│
├── gcp/                             # 🌐 Google Cloud Platform Implementation
│   ├── bootstrap/                   # One-time bootstrap for GCP WIF & Remote State Bucket
│   ├── environments/
│   │   ├── dev/                     # Dev environment root composition
│   │   ├── staging/                 # Staging environment
│   │   └── prod/                    # Production environment
│   ├── modules/
│   │   ├── 01_networking/           # VPC, Subnets, PSA, VPC Connector, Cloud Armor WAF
│   │   ├── 02_security_iam/         # Service Accounts, IAM Roles, Cloud KMS (CMEK), Secret Manager
│   │   ├── 03_data_state/           # Private Cloud SQL, Firestore Native DB, BigQuery (CTT Analytics)
│   │   ├── 04_messaging/            # Pub/Sub Inbound Topics & Push Subscriptions with DLQ
│   │   ├── 05_compute_services/     # Cloud Run v2 (Agents 1/2, Gateway, GateKeeper, MCP Gateway, Lens)
│   │   ├── 06_ingress_gateway/      # Google Cloud API Gateway & PingIdentity JWT Auth Specs
│   │   └── 07_observability/        # Immutable Audit Log Bucket, Sinks, Dashboards & Alerts
│   └── docs/
│       ├── ARCHITECTURE.md          # GCP Architecture breakdown & data flows
│       └── RUNBOOK.md               # GCP Deployment Runbook
│
├── azure/                           # ☁️ Microsoft Azure Implementation
│   ├── bootstrap/                   # One-time bootstrap for Azure Entra ID OIDC & State Storage
│   ├── environments/
│   │   ├── dev/                     # Dev environment root composition
│   │   ├── staging/                 # Staging environment
│   │   └── prod/                    # Production environment
│   ├── modules/
│   │   ├── 01_networking/           # VNet, Delegated Subnets, NAT Gateway, Front Door WAF
│   │   ├── 02_security_iam/         # Managed Identities, Azure Key Vault, CMEK Keys, Secrets
│   │   ├── 03_data_state/           # PostgreSQL Flexible Server, Cosmos DB, ADLS Gen2
│   │   ├── 04_messaging/            # Service Bus Topics & Subscriptions with DLQ
│   │   ├── 05_compute_services/     # Azure Container Apps (9 Multi-Agent Microservices)
│   │   ├── 06_ingress_gateway/      # Azure API Management (APIM) & PingIdentity JWT Policy
│   │   └── 07_observability/        # Log Analytics Workspace, App Insights, Immutable Audit Storage
│   └── docs/
│       ├── ARCHITECTURE.md          # Azure Architecture breakdown & 1-to-1 GCP mapping
│       └── RUNBOOK.md               # Azure Deployment Runbook
│
├── .gitignore
└── README.md
```

---

## ⚡ 1-to-1 Cloud Feature Comparison

| Architectural Domain | Google Cloud Platform (`gcp/`) | Microsoft Azure (`azure/`) |
| :--- | :--- | :--- |
| **Compute & Microservices** | Cloud Run v2 Services | **Azure Container Apps (ACA)** |
| **Edge WAF & DDoS Defense** | Cloud Armor Security Policy | **Azure Front Door + WAF (OWASP CRS 3.2)** |
| **Ingress API Gateway** | Cloud API Gateway + OpenID Connect | **Azure API Management (APIM) + JWT Policy** |
| **Relational Database** | Cloud SQL (PostgreSQL 16) | **Azure PostgreSQL Flexible Server (Private VNet)** |
| **Fast Session Store** | Cloud Firestore Native Mode | **Azure Cosmos DB (Serverless NoSQL)** |
| **Event-Driven Messaging** | Cloud Pub/Sub Topics & Subscriptions | **Azure Service Bus Topics & Subscriptions** |
| **Key & Secret Management** | Cloud KMS (CMEK) & Secret Manager | **Azure Key Vault (CMEK & RBAC Secrets)** |
| **Analytics & Telemetry** | Google BigQuery Dataset | **Azure Data Lake Storage Gen2 (ADLS)** |
| **Observability & Tracing** | Cloud Logging Sinks & Monitoring | **Log Analytics & Application Insights** |
| **CI/CD Authentication** | Workload Identity Federation (WIF) | **Entra ID Federated Credentials (OIDC)** |

---

## 🚀 Quick Navigation

- **Google Cloud Platform**: See [`gcp/docs/ARCHITECTURE.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/ARCHITECTURE.md) and [`gcp/docs/RUNBOOK.md`](file:///Users/chasharm4/gcp-arch/cloud-run/gcp/docs/RUNBOOK.md).
- **Microsoft Azure**: See [`azure/docs/ARCHITECTURE.md`](file:///Users/chasharm4/gcp-arch/cloud-run/azure/docs/ARCHITECTURE.md) and [`azure/docs/RUNBOOK.md`](file:///Users/chasharm4/gcp-arch/cloud-run/azure/docs/RUNBOOK.md).
