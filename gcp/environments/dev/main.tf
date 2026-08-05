# ==============================================================================
# Enterprise Digital Agent Platform (DAP) - Dev Environment Deployment
# ==============================================================================

# 1. Module 01: Core Networking, Subnets, PSA & INT WAF
module "networking" {
  source             = "../../modules/01_networking"
  project_id         = var.project_id
  region             = var.region
  environment        = var.environment
  subnet_cidr        = var.subnet_cidr
  vpc_connector_cidr = var.vpc_connector_cidr
}

# 2. Module 02: IAM Service Accounts, Cloud KMS (CMEK) & Secret Manager
module "security_iam" {
  source      = "../../modules/02_security_iam"
  project_id  = var.project_id
  region      = var.region
  environment = var.environment
}

# 3. Module 03: Data & State (Cloud SQL, Firestore Native, CTT BigQuery)
module "data_state" {
  source              = "../../modules/03_data_state"
  project_id          = var.project_id
  region              = var.region
  environment         = var.environment
  vpc_id              = module.networking.vpc_id
  kms_cloudsql_key_id = module.security_iam.kms_keys["cloudsql"]
  kms_bigquery_key_id = module.security_iam.kms_keys["bigquery"]

  # Ensure Private Service Access peering is established prior to Cloud SQL
  depends_on = [module.networking.private_vpc_connection]
}

# 4. Module 04: Event-Driven Messaging (Pub/Sub Topics & Push Subscriptions)
module "messaging" {
  source            = "../../modules/04_messaging"
  project_id        = var.project_id
  environment       = var.environment
  kms_pubsub_key_id = module.security_iam.kms_keys["pubsub"]
}

# 5. Module 05: Serverless Microservices Compute (Cloud Run v2)
module "compute_services" {
  source                   = "../../modules/05_compute_services"
  project_id               = var.project_id
  region                   = var.region
  environment              = var.environment
  vpc_connector_id         = module.networking.vpc_connector_id
  service_account_emails   = module.security_iam.service_accounts
  container_images         = var.container_images
  firestore_database_name  = module.data_state.firestore_database_name
  agent_1_inbound_topic_id = module.messaging.agent_1_inbound_topic_id
  agent_2_inbound_topic_id = module.messaging.agent_2_inbound_topic_id
  gatekeeper_topic_id      = module.messaging.gatekeeper_topic_id
  registry_db_private_ip   = module.data_state.registry_db_private_ip
  gateway_db_private_ip    = module.data_state.gateway_db_private_ip
  bigquery_dataset_id      = module.data_state.bigquery_dataset_id

  depends_on = [module.data_state, module.messaging]
}

# 6. Module 06: Edge Ingress API Gateway with PingIdentity JWT Authentication
module "ingress_gateway" {
  source                     = "../../modules/06_ingress_gateway"
  project_id                 = var.project_id
  region                     = var.region
  environment                = var.environment
  agent_gateway_backend_url  = module.compute_services.agent_gateway_uri
  agent_registry_backend_url = module.compute_services.agent_registry_uri
  pingidentity_issuer_url    = var.pingidentity_issuer_url
  pingidentity_jwks_url      = var.pingidentity_jwks_url
  pingidentity_audience      = var.pingidentity_audience

  depends_on = [module.compute_services]
}

# 7. Module 07: Observability, Audit Logs & Dashboards
module "observability" {
  source      = "../../modules/07_observability"
  project_id  = var.project_id
  region      = var.region
  environment = var.environment
}
