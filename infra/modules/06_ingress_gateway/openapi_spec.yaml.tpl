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
  google_auth:
    type: "oauth2"
    authorizationUrl: ""
    flow: "implicit"
    x-google-issuer: "https://accounts.google.com"
    x-google-jwks_uri: "https://www.googleapis.com/oauth2/v3/certs"
    x-google-audiences: "${google_audiences}"

paths:
  /v1/agent1/tasks:
    post:
      summary: "Execute an Agent Task via Agent 1 (Primary Coordinator)"
      operationId: "executeAgent1Task"
      security:
        - google_auth: []
      x-google-backend:
        address: "${agent_1_backend_url}"
        path_translation: CONSTANT_ADDRESS
        jwt_audience: "${agent_1_backend_url}"
      responses:
        '200':
          description: "Task successfully processed"
          schema:
            type: "object"
        '401':
          description: "Unauthorized: Invalid or expired Google IAM OIDC token"

  /v1/agent2/tasks:
    post:
      summary: "Execute a Specialized Agent Task via Agent 2"
      operationId: "executeAgent2Task"
      security:
        - google_auth: []
      x-google-backend:
        address: "${agent_2_backend_url}"
        path_translation: CONSTANT_ADDRESS
        jwt_audience: "${agent_2_backend_url}"
      responses:
        '200':
          description: "Task successfully processed"
          schema:
            type: "object"
        '401':
          description: "Unauthorized: Invalid or expired Google IAM OIDC token"
