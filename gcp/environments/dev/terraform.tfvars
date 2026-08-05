project_id  = "project-ddfa7a80-7677-4268-95a"
region      = "europe-west1"
environment = "dev"

subnet_cidr        = "10.10.0.0/20"
vpc_connector_cidr = "10.10.16.0/28"

pingidentity_issuer_url = "https://auth.enterprise.com"
pingidentity_jwks_url   = "https://auth.enterprise.com/.well-known/jwks.json"
pingidentity_audience   = "dap-platform-api"
