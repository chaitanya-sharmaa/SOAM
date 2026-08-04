# Enterprise Digital Agent Platform (DAP) Infrastructure

This repository contains production-grade, enterprise Terraform modules and CI/CD pipelines to provision the **Google Cloud Digital Agent Platform (DAP)**.

## 📁 Repository Structure

```
├── .github/
│   └── workflows/
│       └── terraform.yml          # GitHub Actions CI/CD Pipeline (WIF Keyless Auth)
├── bootstrap/                     # One-time bootstrap for WIF & GCS State Bucket
├── environments/
│   ├── dev/                       # Development environment configuration
│   ├── staging/                   # Staging environment
│   └── prod/                      # Production environment
├── modules/
│   ├── 01_networking/             # VPC, Subnets, PSA, Serverless VPC Connector, Cloud Armor WAF
│   ├── 02_security_iam/           # Service Accounts, IAM Roles, Cloud KMS (CMEK), Secret Manager
│   ├── 03_data_state/             # Private Cloud SQL, Firestore Native DB, BigQuery (CTT Analytics)
│   ├── 04_messaging/              # Pub/Sub Inbound Topics & Push Subscriptions with DLQ
│   ├── 05_compute_services/       # Cloud Run v2 (Agents 1/2, Gateway, GateKeeper, MCP Gateway, Lens)
│   ├── 06_ingress_gateway/        # Google Cloud API Gateway & PingIdentity JWT Auth Specs
│   └── 07_observability/          # Immutable Audit Log Bucket, Sinks, Dashboards & Alerts
├── docs/
│   ├── ARCHITECTURE.md            # Complete architecture breakdown & interview talking points
│   └── RUNBOOK.md                 # Step-by-step deployment guide
└── README.md
```

## 🚀 Getting Started

1. Read the [Architecture Guide](file:///Users/chasharm4/gcp-arch/docs/ARCHITECTURE.md) to understand the platform design and data flows.
2. Follow the [Deployment Runbook](file:///Users/chasharm4/gcp-arch/docs/RUNBOOK.md) to bootstrap WIF and deploy via GitHub Actions.
