swagger: "2.0"
info:
  title: "Enterprise Digital Agent Platform (DAP) API"
  description: "Edge REST API for Business Applications and Clients to trigger multi-agent workflows."
  version: "1.0.0"
schemes:
  - "https"
produces:
  - "application/json"
consumes:
  - "application/json"

securityDefinitions:
  pingidentity_auth:
    type: "oauth2"
    authorizationUrl: ""
    flow: "implicit"
    x-google-issuer: "${pingidentity_issuer_url}"
    x-google-jwks_uri: "${pingidentity_jwks_url}"
    x-google-audiences: "${pingidentity_audience}"

paths:
  /v1/agents/execute:
    post:
      summary: "Execute an Agent Task via Agent Gateway"
      operationId: "executeAgentTask"
      security:
        - pingidentity_auth: []
      x-google-backend:
        address: "${agent_gateway_backend_url}/v1/tasks"
        protocol: "h2"
      responses:
        '200':
          description: "Task successfully submitted or executed"
          schema:
            type: "object"
        '401':
          description: "Unauthorized: Invalid or expired PingIdentity JWT token"
        '429':
          description: "Too Many Requests: Cloud Armor rate limit triggered"

  /v1/agents/registry:
    get:
      summary: "Discover registered Agents and capabilities"
      operationId: "getAgentCatalog"
      security:
        - pingidentity_auth: []
      x-google-backend:
        address: "${agent_registry_backend_url}/v1/catalog"
        protocol: "h2"
      responses:
        '200':
          description: "List of registered agents"
          schema:
            type: "array"
