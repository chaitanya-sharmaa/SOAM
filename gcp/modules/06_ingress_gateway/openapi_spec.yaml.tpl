swagger: "2.0"
info:
  title: "Enterprise SOAM Multi-Agent Platform API"
  description: "Edge REST API for Business Applications and Clients to trigger Agent 1 and Agent 2 workflows."
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
  /v1/agent1/tasks:
    post:
      summary: "Execute an Agent Task via Agent 1 (Primary Coordinator)"
      operationId: "executeAgent1Task"
      security:
        - pingidentity_auth: []
      x-google-backend:
        address: "${agent_1_backend_url}/v1/tasks/process"
        protocol: "h2"
      responses:
        '200':
          description: "Task successfully processed"
          schema:
            type: "object"
        '401':
          description: "Unauthorized: Invalid or expired PingIdentity JWT token"

  /v1/agent2/tasks:
    post:
      summary: "Execute a Specialized Agent Task via Agent 2"
      operationId: "executeAgent2Task"
      security:
        - pingidentity_auth: []
      x-google-backend:
        address: "${agent_2_backend_url}/v1/tasks/process"
        protocol: "h2"
      responses:
        '200':
          description: "Task successfully processed"
          schema:
            type: "object"
        '401':
          description: "Unauthorized: Invalid or expired PingIdentity JWT token"
