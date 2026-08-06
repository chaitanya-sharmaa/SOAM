import os, json
from http.server import BaseHTTPRequestHandler, HTTPServer

class AgentHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress default logging

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "healthy",
            "message": "Hello World from SOAM Agent!"
        }).encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        agent_name = os.environ.get("AGENT_NAME", "agent")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "message": f"Hello World from {agent_name}!",
            "received": payload,
            "soam": "Service-Oriented Agent Mesh"
        }).encode())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting SOAM agent on port {port}")
    HTTPServer(("", port), AgentHandler).serve_forever()
