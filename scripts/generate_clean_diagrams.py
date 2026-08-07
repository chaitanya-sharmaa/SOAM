import os
import subprocess
import tempfile

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "/Users/chasharm4/gcp-arch/docs"

def render_html_to_png(html_content, output_png_path, width=1600, height=1200):
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False) as f:
        f.write(html_content)
        temp_html = f.name

    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={output_png_path}",
        f"file://{temp_html}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.remove(temp_html)
    print(f"Rendered: {output_png_path}")

# ==============================================================================
# Diagram 0: Comprehensive Network Connectivity & PKI Certificate Architecture
# ==============================================================================
HTML_NETWORK_CERTS = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 1120px; padding: 28px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 16px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 14.5px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .channels-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
  
  .chan-card { background: #ffffff; border-radius: 12px; border: 1.5px solid #cbd5e1; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
  
  .chan-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .chan-title { font-size: 14.5px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
  
  .chan-body { font-size: 12px; color: #334155; line-height: 1.4; }
  .chan-body code { background: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-size: 11px; color: #0f172a; }
  
  .cert-box { margin-top: 8px; background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 8px; padding: 8px 10px; font-size: 11.5px; }
  .cert-title { font-weight: 700; color: #0f172a; margin-bottom: 2px; display: flex; justify-content: space-between; }
  
  .badge { font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 8px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  .badge-rose { background: #ffe4e6; color: #9f1239; }
  
  .table-container { background: #ffffff; border-radius: 12px; border: 1.5px solid #e2e8f0; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
  table { width: 100%; border-collapse: collapse; font-size: 11.5px; }
  th { background: #f1f5f9; color: #0f172a; font-weight: 700; text-align: left; padding: 8px 12px; border-bottom: 1.5px solid #cbd5e1; }
  td { padding: 7px 12px; border-bottom: 1px solid #f1f5f9; color: #334155; vertical-align: middle; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f8fafc; }
  
  .footer-summary { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 14px; display: flex; justify-content: space-around; font-size: 11.5px; font-weight: 600; color: #475569; margin-top: 8px; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Network Connectivity & PKI Certificate Architecture</h1>
    <p>Comprehensive Map of Resource Connections, Protocols, Ports, and Certificate Origins</p>
  </div>
  
  <div class="channels-grid">
    <!-- Channel 1: Client to API Gateway -->
    <div class="chan-card" style="border-color: #3b82f6;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #1d4ed8;"><span>🌐 1. Client ➔ Cloud API Gateway</span></div>
          <span class="badge badge-blue">HTTPS / 443</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> External client invokes <code>https://dev-dap-gateway-*.gateway.dev</code>.<br>
          • <strong>Auth:</strong> Google IAM OIDC Bearer Token in <code>Authorization</code> header.
        </div>
      </div>
      <div class="cert-box" style="border-color: #93c5fd; background: #eff6ff;">
        <div class="cert-title" style="color: #1e40af;">
          <span>🔒 TLS Cert Origin:</span>
          <span class="badge badge-blue">Google Trust Services (GTS CA 1C3)</span>
        </div>
        <div>• Managed SSL certificate automatically minted and rotated by Google on <code>*.gateway.dev</code>.<br>
        • JWT signature verified by fetching JWKS from <code>https://www.googleapis.com/oauth2/v3/certs</code>.</div>
      </div>
    </div>
    
    <!-- Channel 2: API Gateway to Cloud Run Agent 1 -->
    <div class="chan-card" style="border-color: #6366f1;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #4338ca;"><span>🛡️ 2. API Gateway ➔ Agent 1 (Coordinator)</span></div>
          <span class="badge badge-indigo">Internal mTLS / 443</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> Gateway forwards validated traffic to Cloud Run URL.<br>
          • <strong>Ingress:</strong> Agent 1 rejects direct public internet (<code>INTERNAL_ONLY</code>).
        </div>
      </div>
      <div class="cert-box" style="border-color: #c7d2fe; background: #eef2ff;">
        <div class="cert-title" style="color: #3730a3;">
          <span>🔒 TLS Cert Origin:</span>
          <span class="badge badge-purple">Google Borg ALTS / Internal CA</span>
        </div>
        <div>• Encrypted over Google's internal software-defined network via Application Layer Transport Security (ALTS).<br>
        • Auth: Gateway mints OIDC token for <code>sa-dev-api-gateway</code> (roles/run.invoker).</div>
      </div>
    </div>
    
    <!-- Channel 3: Pub/Sub Async Backbone to Agent 2 -->
    <div class="chan-card" style="border-color: #8b5cf6;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #6d28d9;"><span>⚡ 3. Pub/Sub Bus ➔ Agent 2 (Worker)</span></div>
          <span class="badge badge-purple">OIDC Push / 443</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> Push Subscription pushes task from <code>agent-2-inbound-topic</code> to Agent 2.<br>
          • <strong>Reliability:</strong> 300s ACK deadline, 5 retries, exponential backoff, DLQ hold.
        </div>
      </div>
      <div class="cert-box" style="border-color: #ddd6fe; background: #faf5ff;">
        <div class="cert-title" style="color: #5b21b6;">
          <span>🔒 TLS Cert Origin:</span>
          <span class="badge badge-purple">Google Internal Production CA</span>
        </div>
        <div>• Push payload encrypted in transit over Google internal TLS.<br>
        • Auth: Pub/Sub mints Google IAM OIDC token for <code>sa-dev-ps-invoker</code> (roles/run.invoker).</div>
      </div>
    </div>
    
    <!-- Channel 4: Direct VPC Egress into Customer Subnet -->
    <div class="chan-card" style="border-color: #10b981;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #047857;"><span>🔌 4. Cloud Run ➔ Customer VPC Subnet</span></div>
          <span class="badge badge-green">Direct VPC Egress</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> Containers attach directly to <code>snet-private-workload</code> (10.10.1.0/24).<br>
          • <strong>Zero VM Connectors:</strong> Eliminates e2-micro VMs, sub-2ms network routing.
        </div>
      </div>
      <div class="cert-box" style="border-color: #a7f3d0; background: #f0fdf4;">
        <div class="cert-title" style="color: #065f46;">
          <span>🔒 Network Security:</span>
          <span class="badge badge-green">VPC Subnet IP Leases</span>
        </div>
        <div>• Layer-3 packet encapsulation directly into customer VPC.<br>
        • Governed by VPC Firewall Rule <code>allow-internal</code> (TCP 443, 5432, 8080).</div>
      </div>
    </div>
    
    <!-- Channel 5: Cloud SQL over PSA Peering -->
    <div class="chan-card" style="border-color: #0d9488;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #0f766e;"><span>💾 5. Agents ➔ Cloud SQL PostgreSQL 15</span></div>
          <span class="badge badge-teal">PSA Peering / 5432</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> Agents connect to <code>10.10.16.x</code> in Google Tenant VPC over PSA.<br>
          • <strong>Zero Public IP:</strong> <code>ipv4_enabled = false</code> (No internet gateway exists on DB).
        </div>
      </div>
      <div class="cert-box" style="border-color: #99f6e4; background: #f0fdfa;">
        <div class="cert-title" style="color: #115e59;">
          <span>🔒 TLS Cert Origin:</span>
          <span class="badge badge-teal">Google Cloud SQL Managed Server CA</span>
        </div>
        <div>• Server TLS certificate issued by Google Cloud SQL Internal CA (<code>server-ca.pem</code>).<br>
        • Auth: IAM DB Authentication / Cloud SQL Auth Proxy mints ephemeral 60-min client TLS certs.</div>
      </div>
    </div>
    
    <!-- Channel 6: Private Google Access (PGA) -->
    <div class="chan-card" style="border-color: #f59e0b;">
      <div>
        <div class="chan-header">
          <div class="chan-title" style="color: #b45309;"><span>☁️ 6. Agents ➔ Firestore, Secrets & BigQuery</span></div>
          <span class="badge badge-amber">PGA VIPs / 443</span>
        </div>
        <div class="chan-body">
          • <strong>Connection:</strong> Workload subnet routes to <code>*.googleapis.com</code> via PGA.<br>
          • <strong>Route:</strong> Internal Google Private VIPs (<code>199.36.153.8/30</code>) bypassing Cloud NAT.
        </div>
      </div>
      <div class="cert-box" style="border-color: #fde68a; background: #fffbeb;">
        <div class="cert-title" style="color: #92400e;">
          <span>🔒 TLS Cert Origin:</span>
          <span class="badge badge-amber">Google Trust Services (GTS Root R1)</span>
        </div>
        <div>• Standard Google public CA certificates for <code>*.googleapis.com</code>.<br>
        • Verified against Linux system root CA bundle (<code>/etc/ssl/certs/ca-certificates.crt</code>).</div>
      </div>
    </div>
  </div>
  
  <!-- Master PKI & Connectivity Reference Table -->
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Connection Path</th>
          <th>Protocol & Port</th>
          <th>Transport Security</th>
          <th>Certificate Authority / Issuer</th>
          <th>Identity & Auth Mechanism</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Client ➔ Cloud API Gateway</strong></td>
          <td>HTTPS / 443</td>
          <td>TLS 1.3</td>
          <td><strong>Google Trust Services (GTS CA 1C3)</strong></td>
          <td>Google IAM OIDC Bearer Token (JWKS validated)</td>
        </tr>
        <tr>
          <td><strong>API Gateway ➔ Agent 1 Coordinator</strong></td>
          <td>HTTP/2 over mTLS</td>
          <td>Google ALTS / mTLS</td>
          <td><strong>Google Borg Production Internal CA</strong></td>
          <td>OIDC Token (<code>sa-dev-api-gateway</code>, roles/run.invoker)</td>
        </tr>
        <tr>
          <td><strong>Pub/Sub Push ➔ Agent 2 Worker</strong></td>
          <td>HTTPS / 443</td>
          <td>Google Internal TLS</td>
          <td><strong>Google Internal Production CA</strong></td>
          <td>OIDC Token (<code>sa-dev-ps-invoker</code>, roles/run.invoker)</td>
        </tr>
        <tr>
          <td><strong>Cloud Run ➔ Workload Subnet</strong></td>
          <td>Direct VPC Egress</td>
          <td>IP Encapsulation</td>
          <td><strong>VPC Subnet IP Allocation (10.10.1.0/24)</strong></td>
          <td>VPC Firewall Rule <code>allow-internal</code></td>
        </tr>
        <tr>
          <td><strong>Agents ➔ Cloud SQL PostgreSQL</strong></td>
          <td>TCP / 5432</td>
          <td>TLS (verify-full / mTLS)</td>
          <td><strong>Google Cloud SQL Managed Server CA</strong></td>
          <td>IAM DB Auth / Ephemeral certs (60-min rotation)</td>
        </tr>
        <tr>
          <td><strong>Agents ➔ Firestore / Secrets / BQ</strong></td>
          <td>HTTPS / 443 (PGA)</td>
          <td>TLS 1.3</td>
          <td><strong>Google Trust Services (GTS Root R1)</strong></td>
          <td>Google Workload Identity / Service Account IAM</td>
        </tr>
        <tr>
          <td><strong>Agents ➔ External LLMs / SaaS</strong></td>
          <td>HTTPS / 443 (Cloud NAT)</td>
          <td>TLS 1.3</td>
          <td><strong>Public Web PKI (DigiCert / Let's Encrypt)</strong></td>
          <td>API Keys from Secret Manager + Static NAT IP (34.x.x.x)</td>
        </tr>
      </tbody>
    </table>
  </div>
  
  <div class="footer-summary">
    <span>🔒 <strong>Edge & Public TLS:</strong> Google Trust Services (GTS)</span>
    <span>🛡️ <strong>Internal Mesh:</strong> Google Borg ALTS mTLS</span>
    <span>💾 <strong>Database:</strong> Cloud SQL Managed CA + Ephemeral IAM TLS</span>
    <span>☁️ <strong>Google PaaS:</strong> Private Google Access (PGA)</span>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 1: True Flow-Based Architecture Topology & Hop-by-Hop Journey
# ==============================================================================
HTML_SOAM_ARCH = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1600px; height: 1140px; padding: 24px 30px; position: relative; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 14px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 14px; color: #64748b; margin-top: 3px; font-weight: 500; }
  
  /* Stage Containers */
  .stage-box { position: absolute; border-radius: 14px; border: 1.5px solid #e2e8f0; background: #ffffff; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
  .stage-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; padding: 10px 16px 0; display: flex; justify-content: space-between; }
  
  /* Nodes */
  .node { position: absolute; border-radius: 12px; border: 1.5px solid #cbd5e1; background: #ffffff; padding: 12px 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); display: flex; flex-direction: column; justify-content: space-between; z-index: 10; }
  .node-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
  .node-title { font-size: 13.5px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 6px; }
  .node-desc { font-size: 11px; color: #475569; line-height: 1.38; }
  .node-desc code { background: #f1f5f9; padding: 1px 4px; border-radius: 4px; font-size: 10.5px; color: #0f172a; font-weight: 600; }
  .node-footer { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
  
  /* Badges */
  .badge { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  .badge-slate { background: #f1f5f9; color: #334155; }
  
  /* Hop Annotations */
  .hop-pill { position: absolute; background: #0f172a; color: #ffffff; font-size: 10.5px; font-weight: 800; border-radius: 12px; padding: 2px 8px; z-index: 20; box-shadow: 0 2px 6px rgba(0,0,0,0.15); transform: translate(-50%, -50%); text-align: center; }
  .hop-subtext { font-size: 9.5px; font-weight: 600; color: #475569; position: absolute; transform: translate(-50%, 0); white-space: nowrap; z-index: 20; text-align: center; }
  
  /* Footer */
  .footer-banner { position: absolute; bottom: 18px; left: 30px; width: 1540px; height: 46px; background: #0f172a; border-radius: 10px; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; color: #f8fafc; font-size: 11.5px; font-weight: 500; }
  .footer-banner strong { color: #38bdf8; }
</style>
</head>
<body>
  <div class="header">
    <h1>SOAM — End-to-End Request & Packet Flow Architecture</h1>
    <p>Deterministic Flow Pipeline: Edge Ingress ➔ 2-Agent Serverless Mesh ➔ Event Bus ➔ Direct VPC Egress ➔ State & SaaS APIs</p>
  </div>
  
  <div class="stage-box" style="top: 85px; left: 30px; width: 1540px; height: 320px; background: #fafbfc;">
    <div class="stage-title">
      <span>Stage 1 & 2: Edge Ingress & Serverless Multi-Agent Compute Mesh</span>
      <span style="color: #2563eb;">🔒 Zero Public Ingress (INTERNAL_ONLY on Agents)</span>
    </div>
  </div>
  
  <div class="node" style="top: 125px; left: 50px; width: 225px; height: 255px; border-color: #3b82f6; background: #eff6ff;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #1d4ed8;"><span>🌐 External Client</span></div>
        <span class="badge badge-blue">Caller</span>
      </div>
      <div class="node-desc">
        • Initiates HTTPS REST request.<br>
        • Obtains OIDC token from <code>accounts.google.com</code>.<br>
        • Passes token in <code>Authorization: Bearer</code> header.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-blue">TLS 1.3</span>
      <span class="badge badge-slate">Google IAM OIDC</span>
    </div>
  </div>
  
  <div class="node" style="top: 125px; left: 345px; width: 235px; height: 255px; border-color: #6366f1; background: #eef2ff;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #4338ca;"><span>🛡️ API Gateway</span></div>
        <span class="badge badge-indigo">Managed Edge</span>
      </div>
      <div class="node-desc">
        • Validates JWT with Google JWKS.<br>
        • Impersonates <code>sa-dev-api-gateway</code> (roles/run.invoker).<br>
        • <strong>Cert:</strong> Google Trust Services (GTS CA 1C3).<br>
        • Ingress URL: <code>*.gateway.dev</code>.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-indigo">OpenAPI 2.0</span>
      <span class="badge badge-purple">JWKS Signature</span>
    </div>
  </div>
  
  <div class="node" style="top: 125px; left: 655px; width: 250px; height: 255px; border-color: #2563eb; border-left: 5px solid #2563eb;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #1e40af;"><span>🤖 Agent 1: Coordinator</span></div>
        <span class="badge badge-blue">Cloud Run v2</span>
      </div>
      <div class="node-desc">
        • Identity: <code>sa-dev-agent-1</code>.<br>
        • Intent routing (Gemini 1.5 Flash).<br>
        • <em>Sync path:</em> direct JSON response.<br>
        • <em>Async path:</em> dispatches to Pub/Sub.<br>
        • Ingress: <code>INTERNAL_ONLY</code>.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-blue">Gemini 1.5 Flash</span>
      <span class="badge badge-green">Direct VPC Egress</span>
    </div>
  </div>
  
  <div class="node" style="top: 125px; left: 980px; width: 240px; height: 255px; border-color: #a855f7; background: #faf5ff;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #7e22ce;"><span>⚡ SOAM Message Bus</span></div>
        <span class="badge badge-purple">Pub/Sub</span>
      </div>
      <div class="node-desc">
        • <strong>Topic:</strong> <code>agent-2-inbound-topic</code>.<br>
        • <strong>Push Sub:</strong> mints OIDC with <code>sa-dev-ps-invoker</code>.<br>
        • <strong>DLQ:</strong> <code>dap-dlq-topic</code> (5 retries, 7-day retention hold).<br>
        • Decouples orchestration.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-purple">OIDC Push</span>
      <span class="badge badge-amber">DLQ Protected</span>
    </div>
  </div>
  
  <div class="node" style="top: 125px; left: 1295px; width: 255px; height: 255px; border-color: #16a34a; border-left: 5px solid #16a34a; background: #f0fdf4;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #15803d;"><span>🧠 Agent 2: Worker</span></div>
        <span class="badge badge-green">Cloud Run v2</span>
      </div>
      <div class="node-desc">
        • Identity: <code>sa-dev-agent-2</code>.<br>
        • Invoked by Pub/Sub Push over internal HTTPS.<br>
        • Executes complex SQL diagnostics, state persistence & tool calls.<br>
        • Ingress: <code>INTERNAL_ONLY</code>.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-green">Worker Loop</span>
      <span class="badge badge-teal">Direct VPC Egress</span>
    </div>
  </div>
  
  <div class="stage-box" style="top: 480px; left: 30px; width: 1540px; height: 575px; background: #f8fafc;">
    <div class="stage-title">
      <span>Stage 3: Customer VPC Boundary, Direct VPC Egress & Destination Isolation</span>
      <span style="color: #059669;">🛡️ dev-dap-vpc (10.10.0.0/16) • Zero Public IPs</span>
    </div>
  </div>
  
  <div class="node" style="top: 525px; left: 50px; width: 380px; height: 510px; border-color: #10b981; border-width: 2px;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #065f46; font-size: 15px;"><span>🔌 Customer VPC Workload Subnet</span></div>
        <span class="badge badge-green">10.10.1.0/24</span>
      </div>
      <div class="node-desc" style="font-size: 12px; line-height: 1.45; margin-top: 8px;">
        • <strong>Subnet Name:</strong> <code>snet-private-workload</code> in <code>europe-west1</code>.<br>
        • <strong>Direct VPC Egress:</strong> Cloud Run instances lease dynamic internal IPs directly from this subnet.<br>
        • <strong>Zero VM Connectors:</strong> Sub-2ms container networking without Serverless VPC Connector bottlenecks.<br>
        • <strong>Firewall Rule:</strong> <code>allow-internal</code> (TCP 443, 5432, 8080). Zero public IP assigned to subnet.<br>
        • <strong>Private Google Access (PGA):</strong> Enabled for private Google PaaS routing.
      </div>
      <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px; margin-top: 14px;">
        <div style="font-size: 11.5px; font-weight: 700; color: #166534; margin-bottom: 4px;">Subnet Routing Engine</div>
        <div style="font-size: 11px; color: #15803d; line-height: 1.35;">
          • PSA Peering ➔ routes <code>10.10.16.0/20</code> to Tenant VPC.<br>
          • PGA Route ➔ resolves <code>*.googleapis.com</code> to Private VIPs.<br>
          • Default 0.0.0.0/0 ➔ routed to Cloud NAT Gateway.
        </div>
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-green">Direct VPC Egress</span>
      <span class="badge badge-teal">PGA Enabled</span>
      <span class="badge badge-blue">Cloud NAT Attached</span>
    </div>
  </div>
  
  <div class="node" style="top: 525px; left: 740px; width: 810px; height: 150px; border-color: #0d9488; background: #f0fdfa;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #0f766e; font-size: 14.5px;"><span>💾 Cloud SQL PostgreSQL 15</span></div>
        <span class="badge badge-teal">Google Tenant VPC (10.10.16.x)</span>
      </div>
      <div class="node-desc" style="font-size: 11.5px; line-height: 1.4;">
        • <strong>Connection:</strong> Private Services Access (PSA) peering <code>10.10.16.0/20</code>. Port TCP <code>5432</code>.<br>
        • <strong>Network Isolation:</strong> <code>ipv4_enabled = false</code> (never internet-accessible). Zero public IP.<br>
        • <strong>Cert & Auth:</strong> Google Cloud SQL Managed CA (<code>server-ca.pem</code>) + IAM ephemeral 60-min client TLS certs.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-teal">PSA Peering</span>
      <span class="badge badge-slate">TCP 5432</span>
      <span class="badge badge-teal">Cloud SQL CA</span>
      <span class="badge badge-purple">IAM DB Auth</span>
    </div>
  </div>
  
  <div class="node" style="top: 705px; left: 740px; width: 810px; height: 150px; border-color: #f59e0b; background: #fffbeb;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #b45309; font-size: 14.5px;"><span>☁️ Cloud Firestore Native + Secret Manager + BigQuery</span></div>
        <span class="badge badge-amber">Private Google Access (PGA)</span>
      </div>
      <div class="node-desc" style="font-size: 11.5px; line-height: 1.4;">
        • <strong>Connection:</strong> Subnet resolves <code>*.googleapis.com</code> to Private VIPs (<code>199.36.153.8/30</code>). Port <code>443</code>.<br>
        • <strong>Transport:</strong> Google internal SDN bypasses the public internet with zero Cloud NAT egress cost.<br>
        • <strong>Cert & Auth:</strong> Google Trust Services (GTS Root R1) verified by container root CA bundle + IAM Workload Identity.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-amber">PGA VIPs (199.36.153.8/30)</span>
      <span class="badge badge-slate">HTTPS 443</span>
      <span class="badge badge-amber">GTS Root R1 CA</span>
      <span class="badge badge-green">Zero NAT Cost</span>
    </div>
  </div>
  
  <div class="node" style="top: 885px; left: 740px; width: 810px; height: 150px; border-color: #3b82f6; background: #eff6ff;">
    <div>
      <div class="node-header">
        <div class="node-title" style="color: #1e40af; font-size: 14.5px;"><span>🌍 External LLMs & SaaS APIs (OpenAI / Anthropic)</span></div>
        <span class="badge badge-blue">Cloud NAT Outbound</span>
      </div>
      <div class="node-desc" style="font-size: 11.5px; line-height: 1.4;">
        • <strong>Connection:</strong> Cloud Router & Cloud NAT translates outbound calls from <code>snet-private-workload</code>. Port <code>443</code>.<br>
        • <strong>Static Public IP:</strong> Dedicated IP (<code>34.x.x.x</code>) for deterministic enterprise firewall allowlisting.<br>
        • <strong>Cert & Security:</strong> Public Web PKI (DigiCert / Let's Encrypt TLS 1.3). API Keys securely fetched from Secret Manager.
      </div>
    </div>
    <div class="node-footer">
      <span class="badge badge-blue">Cloud NAT Gateway</span>
      <span class="badge badge-slate">HTTPS 443</span>
      <span class="badge badge-blue">Static Public IP (34.x.x.x)</span>
      <span class="badge badge-purple">Web PKI TLS</span>
    </div>
  </div>
  
  <svg style="position: absolute; top: 0; left: 0; width: 1600px; height: 1140px; pointer-events: none; z-index: 15;">
    <defs>
      <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
      </marker>
      <marker id="arrow-indigo" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#4f46e5" />
      </marker>
      <marker id="arrow-purple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#9333ea" />
      </marker>
      <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
      </marker>
      <marker id="arrow-teal" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#0d9488" />
      </marker>
      <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b" />
      </marker>
    </defs>
    
    <path d="M 275 250 L 340 250" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow-blue)" />
    <path d="M 580 250 L 650 250" fill="none" stroke="#4f46e5" stroke-width="3" marker-end="url(#arrow-indigo)" />
    <path d="M 905 220 L 975 220" fill="none" stroke="#9333ea" stroke-width="3" marker-end="url(#arrow-purple)" />
    <path d="M 1220 250 L 1290 250" fill="none" stroke="#16a34a" stroke-width="3" marker-end="url(#arrow-green)" />
    
    <path d="M 780 380 C 780 450, 240 440, 240 520" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="5,5" marker-end="url(#arrow-green)" />
    <path d="M 1420 380 C 1420 460, 320 440, 320 520" fill="none" stroke="#10b981" stroke-width="2.5" stroke-dasharray="5,5" marker-end="url(#arrow-green)" />
    
    <path d="M 430 600 C 580 600, 600 600, 735 600" fill="none" stroke="#0d9488" stroke-width="3" marker-end="url(#arrow-teal)" />
    <path d="M 430 780 C 580 780, 600 780, 735 780" fill="none" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrow-amber)" />
    <path d="M 430 960 C 580 960, 600 960, 735 960" fill="none" stroke="#2563eb" stroke-width="3" marker-end="url(#arrow-blue)" />
  </svg>
  
  <div class="hop-pill" style="top: 250px; left: 310px; background: #2563eb;">Hop 1</div>
  <div class="hop-subtext" style="top: 265px; left: 310px;">HTTPS 443</div>
  <div class="hop-pill" style="top: 250px; left: 615px; background: #4f46e5;">Hop 2</div>
  <div class="hop-subtext" style="top: 265px; left: 615px;">mTLS 443</div>
  <div class="hop-pill" style="top: 220px; left: 942px; background: #9333ea;">Hop 3</div>
  <div class="hop-subtext" style="top: 235px; left: 942px;">Publish Topic</div>
  <div class="hop-pill" style="top: 250px; left: 1255px; background: #16a34a;">Hop 4</div>
  <div class="hop-subtext" style="top: 265px; left: 1255px;">OIDC Push</div>
  <div class="hop-pill" style="top: 440px; left: 520px; background: #059669;">Hop 5: Direct VPC Egress</div>
  <div class="hop-subtext" style="top: 455px; left: 520px;">Sub-2ms • Zero VM Connectors</div>
  <div class="hop-pill" style="top: 600px; left: 585px; background: #0d9488;">Path 6A: PSA Peering</div>
  <div class="hop-subtext" style="top: 615px; left: 585px;">TCP 5432 • Cloud SQL CA</div>
  <div class="hop-pill" style="top: 780px; left: 585px; background: #d97706;">Path 6B: PGA VIPs</div>
  <div class="hop-subtext" style="top: 795px; left: 585px;">HTTPS 443 • GTS Root R1</div>
  <div class="hop-pill" style="top: 960px; left: 585px; background: #2563eb;">Path 6C: Cloud NAT</div>
  <div class="hop-subtext" style="top: 975px; left: 585px;">HTTPS 443 • Static IP 34.x.x.x</div>
  
  <div class="footer-banner">
    <div>🔒 <strong>Zero-Trust Ingress:</strong> API Gateway validates IAM OIDC JWTs at edge; Cloud Run containers reject all direct public traffic.</div>
    <div>⚡ <strong>Direct VPC Egress:</strong> Sub-2ms container networking with zero VM connector hops into Customer Subnet (10.10.1.0/24).</div>
    <div>🛡️ <strong>Private State Isolation:</strong> Cloud SQL (PSA) and Firestore (PGA) are never exposed to the public internet.</div>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 2: VPC Network Topology & True GCP Architecture Boundaries
# ==============================================================================
HTML_VPC_NET = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 880px; padding: 24px 30px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 14px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 14.5px; color: #64748b; margin-top: 3px; font-weight: 500; }
  
  .domains-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; flex: 1; margin-bottom: 14px; }
  
  .domain-card { background: #ffffff; border-radius: 12px; border: 2px solid #cbd5e1; padding: 14px 16px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
  
  .domain-title { font-size: 15px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  
  .inner-box { border-radius: 8px; border: 1.5px solid #e2e8f0; padding: 8px 12px; margin-top: 6px; }
  .inner-title { font-size: 12.5px; font-weight: 700; color: #0f172a; margin-bottom: 3px; display: flex; justify-content: space-between; }
  .inner-desc { font-size: 11.5px; color: #475569; line-height: 1.35; }
  .inner-desc code { background: #f1f5f9; padding: 1px 4px; border-radius: 4px; font-size: 10.5px; color: #0f172a; font-weight: 600; }
  
  .badge { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  .badge-slate { background: #f1f5f9; color: #334155; }
  
  .footer-summary { background: #0f172a; border-radius: 10px; padding: 10px 20px; display: flex; justify-content: space-around; font-size: 11.5px; font-weight: 600; color: #f8fafc; }
  .footer-summary strong { color: #38bdf8; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Network Topology & Architectural Boundaries</h1>
    <p>Precise Boundary Separation: Customer VPC • Serverless Compute Plane • Google Tenant VPC • Private Google Access</p>
  </div>
  
  <div class="domains-grid">
    <div class="domain-card" style="border-color: #3b82f6; background: #eff6ff;">
      <div>
        <div class="domain-title" style="color: #1e40af;">
          <span>🌐 Customer VPC Network (dev-dap-vpc)</span>
          <span class="badge badge-blue">CIDR: 10.10.0.0/16</span>
        </div>
        <div class="inner-box" style="border-color: #93c5fd; background: #ffffff;">
          <div class="inner-title">
            <span>Workload Subnet: snet-private-workload</span>
            <span class="badge badge-green">10.10.1.0/24 • PGA Enabled</span>
          </div>
          <div class="inner-desc">
            • Subnet hosting <strong>Direct VPC Egress</strong> container IP leases.<br>
            • Firewall: <code>allow-internal</code> (TCP 443, 5432, 8080). No public IP.
          </div>
        </div>
        <div class="inner-box" style="border-color: #93c5fd; background: #ffffff;">
          <div class="inner-title">
            <span>Cloud Router & Cloud NAT Gateway</span>
            <span class="badge badge-blue">Static IP: 34.x.x.x</span>
          </div>
          <div class="inner-desc">
            • <code>dev-dap-router</code> + <code>dev-dap-nat</code> (MANUAL_ONLY).<br>
            • Translates outbound calls to external LLM & SaaS APIs.
          </div>
        </div>
      </div>
      <div style="font-size: 11px; color: #1e40af; font-weight: 600; margin-top: 6px;">📍 Region: europe-west1</div>
    </div>
    
    <div class="domain-card" style="border-color: #10b981; background: #f0fdf4;">
      <div>
        <div class="domain-title" style="color: #065f46;">
          <span>🤖 Serverless Compute Plane (Cloud Run v2)</span>
          <span class="badge badge-green">Google Managed Serverless</span>
        </div>
        <div class="inner-box" style="border-color: #86efac; background: #ffffff;">
          <div class="inner-title">
            <span>Agent 1: SOAM Coordinator</span>
            <span class="badge badge-blue">sa-dev-agent-1</span>
          </div>
          <div class="inner-desc">
            • Direct VPC Egress: Container attaches to <code>snet-private-workload</code>.<br>
            • Ingress: <code>INTERNAL_ONLY</code>.
          </div>
        </div>
        <div class="inner-box" style="border-color: #86efac; background: #ffffff;">
          <div class="inner-title">
            <span>Agent 2: SOAM Worker</span>
            <span class="badge badge-green">sa-dev-agent-2</span>
          </div>
          <div class="inner-desc">
            • Direct VPC Egress: Container attaches to <code>snet-private-workload</code>.<br>
            • Invoked exclusively via Pub/Sub Push.
          </div>
        </div>
      </div>
      <div style="background: #dcfce7; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #166534; font-weight: 600;">
        ⚡ <strong>Direct VPC Egress:</strong> Sub-2ms container routing without VM connector bottlenecks.
      </div>
    </div>
    
    <div class="domain-card" style="border-color: #a855f7; background: #faf5ff;">
      <div>
        <div class="domain-title" style="color: #6b21a8;">
          <span>🏢 Google Tenant VPC (Service Producer Network)</span>
          <span class="badge badge-purple">PSA Peering (10.10.16.0/20)</span>
        </div>
        <div class="inner-box" style="border-color: #d8b4fe; background: #ffffff;">
          <div class="inner-title">
            <span>Cloud SQL PostgreSQL 15 Instance</span>
            <span class="badge badge-purple">Private IP: 10.10.16.x</span>
          </div>
          <div class="inner-desc">
            • <code>ipv4_enabled = false</code> (No public IP address).<br>
            • Peered to Customer VPC via <strong>Private Services Access (PSA)</strong>.
          </div>
        </div>
      </div>
      <div style="background: #f3e8ff; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #6b21a8; font-weight: 600;">
        🔒 <strong>Database Isolation:</strong> Never assigned a public IP; unreachable from public internet.
      </div>
    </div>
    
    <div class="domain-card" style="border-color: #f59e0b; background: #fffbeb;">
      <div>
        <div class="domain-title" style="color: #92400e;">
          <span>☁️ Google Cloud Managed PaaS & APIs</span>
          <span class="badge badge-amber">Private Google Access (PGA)</span>
        </div>
        <div class="inner-box" style="border-color: #fde68a; background: #ffffff;">
          <div class="inner-title">
            <span>Firestore, Pub/Sub, Secret Manager</span>
            <span class="badge badge-amber">Google Global SDN VIPs</span>
          </div>
          <div class="inner-desc">
            • Reached over Google internal backbone (VIPs <code>199.36.153.8/30</code>).<br>
            • Traffic never traverses public internet. Zero egress NAT cost.
          </div>
        </div>
      </div>
      <div style="background: #fef3c7; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #92400e; font-weight: 600;">
        ⚡ <strong>PGA Advantage:</strong> High-bandwidth, sub-millisecond access to Google PaaS.
      </div>
    </div>
  </div>
  
  <div class="footer-summary">
    <span>🌐 <strong>Customer VPC:</strong> Only contains subnets, NAT router, and peering connections.</span>
    <span>🤖 <strong>Compute & State:</strong> Cloud Run is serverless, SQL is Tenant-isolated, PaaS is internal.</span>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 3: Hop-by-Hop Journey (Visual Interconnected Pipeline)
# ==============================================================================
HTML_HOP_BY_HOP = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1600px; height: 960px; padding: 24px 30px; position: relative; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 16px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 14.5px; color: #64748b; margin-top: 3px; font-weight: 500; }
  
  /* Hop Grid */
  .hops-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 14px; }
  .hops-bottom-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  
  .hop-card { background: #ffffff; border-radius: 12px; border: 1.5px solid #cbd5e1; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 12px rgba(0,0,0,0.03); position: relative; min-height: 220px; }
  
  .hop-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
  .hop-num-badge { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; color: #ffffff; }
  .hop-title { font-size: 13.5px; font-weight: 700; color: #0f172a; }
  
  .hop-body { font-size: 11.5px; color: #334155; line-height: 1.42; }
  .hop-body code { background: #f1f5f9; padding: 1px 4px; border-radius: 4px; font-size: 10.5px; color: #0f172a; font-weight: 600; }
  
  .hop-cert-box { background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 6px; padding: 6px 8px; margin-top: 8px; font-size: 11px; }
  .hop-cert-title { font-weight: 700; color: #0f172a; margin-bottom: 2px; }
  
  .badge { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 6px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  .badge-slate { background: #f1f5f9; color: #334155; }
  
  .footer-summary { background: #0f172a; border-radius: 10px; padding: 10px 20px; display: flex; justify-content: space-around; font-size: 11.5px; font-weight: 600; color: #f8fafc; margin-top: 14px; }
  .footer-summary strong { color: #38bdf8; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Hop-by-Hop Request & Packet Journey</h1>
    <p>Complete Packet Lifecycle: Ingress Auth ➔ Agent Mesh ➔ Event Bus ➔ Direct VPC Egress ➔ Peered State & Egress</p>
  </div>
  
  <!-- Row 1: Hops 1, 2, 3, 4 -->
  <div class="hops-grid">
    <div class="hop-card" style="border-top: 4px solid #2563eb; background: #eff6ff;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #2563eb;">1</div>
            <div class="hop-title" style="color: #1e40af;">Edge Ingress</div>
          </div>
          <span class="badge badge-blue">HTTPS / 443</span>
        </div>
        <div class="hop-body">
          • <strong>Client ➔ Cloud API Gateway</strong> (<code>*.gateway.dev</code>).<br>
          • Client presents Google IAM OIDC Bearer Token in <code>Authorization</code> header.<br>
          • Ingress gateway terminates public TLS.
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #93c5fd; background: #ffffff;">
        <div class="hop-cert-title" style="color: #1e40af;">🔒 Cert: Google Trust Services (GTS CA 1C3)</div>
        <div>Managed SSL certificate rotated automatically by GCP.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-top: 4px solid #4f46e5; background: #eef2ff;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #4f46e5;">2</div>
            <div class="hop-title" style="color: #3730a3;">Internal Routing</div>
          </div>
          <span class="badge badge-indigo">Internal mTLS</span>
        </div>
        <div class="hop-body">
          • <strong>Gateway ➔ Agent 1 Coordinator</strong>.<br>
          • Gateway verifies JWT via Google JWKS.<br>
          • Gateway mints internal OIDC token using <code>sa-dev-api-gateway</code>.<br>
          • Agent 1 rejects direct public ingress (<code>INTERNAL_ONLY</code>).
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #c7d2fe; background: #ffffff;">
        <div class="hop-cert-title" style="color: #3730a3;">🔒 Cert: Google Borg Production Internal CA</div>
        <div>Application Layer Transport Security (ALTS) encrypted.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-top: 4px solid #9333ea; background: #faf5ff;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #9333ea;">3</div>
            <div class="hop-title" style="color: #6b21a8;">SOAM Event Dispatch</div>
          </div>
          <span class="badge badge-purple">Pub/Sub Bus</span>
        </div>
        <div class="hop-body">
          • <strong>Agent 1 ➔ agent-2-inbound-topic</strong>.<br>
          • Agent 1 evaluates task complexity using Gemini 1.5 Flash.<br>
          • Lightweight queries respond synchronously.<br>
          • Complex tasks are published as CMEK-encrypted Pub/Sub events.
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #d8b4fe; background: #ffffff;">
        <div class="hop-cert-title" style="color: #6b21a8;">🛡️ Reliability: Dead-Letter Queue (DLQ)</div>
        <div>5 retries with exponential backoff & 7-day retention hold.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-top: 4px solid #16a34a; background: #f0fdf4;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #16a34a;">4</div>
            <div class="hop-title" style="color: #15803d;">Push Invocation</div>
          </div>
          <span class="badge badge-green">OIDC Push / 443</span>
        </div>
        <div class="hop-body">
          • <strong>Pub/Sub Push ➔ Agent 2 Worker</strong>.<br>
          • Subscription authenticates with <code>sa-dev-ps-invoker</code>.<br>
          • Pushes task payload with 300s ACK deadline.<br>
          • Agent 2 executes worker reasoning loops.
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #86efac; background: #ffffff;">
        <div class="hop-cert-title" style="color: #15803d;">🔒 Cert: Google Internal TLS CA</div>
        <div>Encrypted payload delivery over internal Google SDN.</div>
      </div>
    </div>
  </div>
  
  <div class="hops-bottom-grid">
    <div class="hop-card" style="border-top: 4px solid #059669; background: #f0fdfa;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #059669;">5</div>
            <div class="hop-title" style="color: #065f46;">Direct VPC Egress</div>
          </div>
          <span class="badge badge-teal">Subnet 10.10.1.0/24</span>
        </div>
        <div class="hop-body">
          • <strong>Cloud Run ➔ Customer VPC Workload Subnet</strong>.<br>
          • Containers lease dynamic private IPs from <code>snet-private-workload</code>.<br>
          • Sub-2ms container networking with <strong>zero VM connectors</strong>.<br>
          • Firewall Rule: <code>allow-internal</code> (TCP 443, 5432, 8080).
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #5eead4; background: #ffffff;">
        <div class="hop-cert-title" style="color: #065f46;">⚡ Container Network Layer</div>
        <div>Sub-2ms latency • Zero connector VM bottleneck • Zero public IP.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-top: 4px solid #0d9488; background: #f0fdfa;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #0d9488;">6</div>
            <div class="hop-title" style="color: #0f766e;">Peered Database Query</div>
          </div>
          <span class="badge badge-teal">PSA Peering / 5432</span>
        </div>
        <div class="hop-body">
          • <strong>Agent ➔ Cloud SQL PostgreSQL 15</strong> (<code>10.10.16.x</code>).<br>
          • Routed across <strong>Private Services Access (PSA)</strong> peering.<br>
          • <code>ipv4_enabled = false</code> (Instance has no public IP address).<br>
          • Authenticates via IAM Database Authentication.
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #5eead4; background: #ffffff;">
        <div class="hop-cert-title" style="color: #0f766e;">🔒 Cert: Cloud SQL Managed CA (server-ca.pem)</div>
        <div>Encrypted TLS connection + Ephemeral 60-min IAM client certs.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-top: 4px solid #ea580c; background: #fff7ed;">
      <div>
        <div class="hop-top">
          <div style="display: flex; align-items: center; gap: 8px;">
            <div class="hop-num-badge" style="background: #ea580c;">7</div>
            <div class="hop-title" style="color: #c2410c;">PaaS (PGA) & Static NAT Egress</div>
          </div>
          <span class="badge badge-amber">PGA + Cloud NAT</span>
        </div>
        <div class="hop-body">
          • <strong>PaaS Path (PGA):</strong> Resolves <code>*.googleapis.com</code> to Private VIPs (<code>199.36.153.8/30</code>) for Firestore & Secrets (GTS Root R1 CA, zero NAT cost).<br>
          • <strong>LLM Egress Path (NAT):</strong> Exits via Cloud Router/NAT with dedicated Static IP (<code>34.x.x.x</code>) for enterprise firewall allowlisting.
        </div>
      </div>
      <div class="hop-cert-box" style="border-color: #fdba74; background: #ffffff;">
        <div class="hop-cert-title" style="color: #c2410c;">🔒 Cert: GTS Root R1 (PGA) & Public Web PKI (NAT)</div>
        <div>Validated against container CA bundle (/etc/ssl/certs/ca-certificates.crt).</div>
      </div>
    </div>
  </div>
  
  <div class="footer-summary">
    <div>🔒 <strong>End-to-End Zero Trust:</strong> Every hop is cryptographically authenticated with Google IAM OIDC or mTLS.</div>
    <div>💾 <strong>Complete Network Isolation:</strong> Cloud SQL is private via PSA; Cloud Run agents reject public internet.</div>
    <div>⚡ <strong>High-Performance Serverless:</strong> Direct VPC Egress removes VM bottlenecks across all agent calls.</div>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 4: Terragrunt Multi-Environment CI/CD
# ==============================================================================
HTML_TERRAGRUNT = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 720px; padding: 25px 35px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 16px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 14.5px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .main-row { display: grid; grid-template-columns: 320px 40px 1fr; gap: 16px; align-items: center; flex: 1; }
  
  .column { display: flex; flex-direction: column; gap: 12px; }
  
  .card { background: #ffffff; border-radius: 12px; border: 1.5px solid #e2e8f0; padding: 14px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); }
  .card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
  .card-title { font-size: 14.5px; font-weight: 700; color: #0f172a; }
  
  .env-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  
  .env-card { background: #ffffff; border-radius: 10px; border: 1.5px solid #cbd5e1; padding: 12px; }
  .env-title { font-size: 14px; font-weight: 700; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
  .env-item { font-size: 11.5px; color: #475569; margin-bottom: 4px; }
  
  .badge { font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 8px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  
  .arrow { display: flex; align-items: center; justify-content: center; font-size: 24px; color: #94a3b8; font-weight: 800; }
  
  .footer-bar { display: flex; justify-content: space-around; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 16px; font-size: 12px; font-weight: 600; color: #334155; margin-top: 12px; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Terragrunt Multi-Environment CI/CD Topology</h1>
    <p>Strict Isolation • Root Inheritance • GitHub Actions OIDC Workload Identity Federation</p>
  </div>
  
  <div class="main-row">
    <div class="column">
      <div class="card" style="border-color: #93c5fd; background: #eff6ff;">
        <div class="card-header">
          <div style="font-size: 18px;">🚀</div>
          <div class="card-title" style="color: #1e40af;">GitHub Actions CI/CD</div>
        </div>
        <div style="font-size: 12px; color: #334155; line-height: 1.45;">
          • <strong>Trigger:</strong> Push / PR to branch.<br>
          • <strong>Auth:</strong> Keyless Workload Identity Federation (WIF).<br>
          • <strong>Action:</strong> <code>terragrunt run-all plan/apply</code>.
        </div>
      </div>
      
      <div class="card" style="border-color: #c7d2fe; background: #eef2ff;">
        <div class="card-header">
          <div style="font-size: 18px;">🌳</div>
          <div class="card-title" style="color: #3730a3;">Root Configuration</div>
        </div>
        <div style="font-size: 12px; color: #334155; line-height: 1.45;">
          • <code>root.hcl</code>: Remote state GCS backend + Google provider generator.<br>
          • <code>env.hcl</code>: Environment variables & project IDs.
        </div>
      </div>
    </div>
    
    <div class="arrow">➔</div>
    
    <div class="env-grid">
      <div class="env-card" style="border-color: #60a5fa; background: #f8fafc;">
        <div class="env-title" style="color: #1d4ed8;">
          <span>🛠️ Dev Environment</span>
          <span class="badge badge-blue">dev</span>
        </div>
        <div class="env-item">• <strong>State:</strong> <code>dap-dev-tfstate</code></div>
        <div class="env-item">• <strong>VPC:</strong> <code>dev-dap-vpc</code></div>
        <div class="env-item">• <strong>SQL:</strong> <code>dev-dap-postgres-db</code></div>
        <div class="env-item">• <strong>Services:</strong> Agent 1 & Agent 2</div>
        <div class="env-item">• <strong>Min Replicas:</strong> 0</div>
      </div>
      
      <div class="env-card" style="border-color: #f59e0b; background: #f8fafc;">
        <div class="env-title" style="color: #b45309;">
          <span>🧪 Staging Environment</span>
          <span class="badge badge-amber">staging</span>
        </div>
        <div class="env-item">• <strong>State:</strong> <code>dap-staging-tfstate</code></div>
        <div class="env-item">• <strong>VPC:</strong> <code>staging-dap-vpc</code></div>
        <div class="env-item">• <strong>SQL:</strong> <code>staging-dap-postgres-db</code></div>
        <div class="env-item">• <strong>Services:</strong> Agent 1 & Agent 2</div>
        <div class="env-item">• <strong>Min Replicas:</strong> 1</div>
      </div>
      
      <div class="env-card" style="border-color: #10b981; background: #f8fafc;">
        <div class="env-title" style="color: #047857;">
          <span>🔒 Prod Environment</span>
          <span class="badge badge-green">prod</span>
        </div>
        <div class="env-item">• <strong>State:</strong> <code>dap-prod-tfstate</code></div>
        <div class="env-item">• <strong>VPC:</strong> <code>prod-dap-vpc</code></div>
        <div class="env-item">• <strong>SQL:</strong> HA (Regional)</div>
        <div class="env-item">• <strong>Services:</strong> Autoscaling</div>
        <div class="env-item">• <strong>Min Replicas:</strong> 2</div>
      </div>
    </div>
  </div>
  
  <div class="footer-bar">
    <span>🔒 <strong>WIF Authentication:</strong> No long-lived service account keys in CI/CD.</span>
    <span>⚡ <strong>Atomic Module Stacks:</strong> Networking ➔ Security ➔ DB ➔ Messaging ➔ Services ➔ Gateway.</span>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 5: API Gateway to Cloud Run Security
# ==============================================================================
HTML_GATEWAY = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 620px; padding: 25px 35px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 14px; }
  .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
  .header p { font-size: 14.5px; color: #64748b; margin-top: 3px; font-weight: 500; }
  
  .flow-row { display: grid; grid-template-columns: 260px 40px 300px 40px 300px 40px 300px; align-items: center; flex: 1; }
  
  .node-box { background: #ffffff; border-radius: 12px; border: 1.5px solid #cbd5e1; padding: 14px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: space-between; height: 380px; }
  
  .node-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
  .node-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
  .node-title { font-size: 14.5px; font-weight: 700; color: #0f172a; }
  
  .node-body { font-size: 11.5px; color: #475569; line-height: 1.4; }
  .node-body code { background: #f1f5f9; padding: 2px 4px; border-radius: 4px; font-size: 10.5px; color: #0f172a; font-weight: 600; }
  
  .node-footer { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  
  .badge { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 8px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  
  .arrow-connector { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
  .arrow-label { font-size: 10.5px; font-weight: 700; color: #64748b; margin-bottom: 4px; }
  .arrow-line { width: 100%; height: 2px; background: #94a3b8; position: relative; }
  .arrow-line::after { content: ''; position: absolute; right: -2px; top: -4px; width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-left: 6px solid #94a3b8; }
  
  .footer-summary { display: flex; justify-content: space-around; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 16px; font-size: 12px; font-weight: 600; color: #334155; }
</style>
</head>
<body>
  <div class="header">
    <h1>API Gateway ➔ Cloud Run Authentication & Ingress Security</h1>
    <p>Zero Public Ingress • JWT Verification • IAM Service Account Impersonation</p>
  </div>
  
  <div class="flow-row">
    <div class="node-box" style="border-color: #93c5fd; background: #eff6ff;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #dbeafe; color: #1e40af;">🌐</div>
          <div class="node-title">1. External Client</div>
        </div>
        <div class="node-body">
          • Requests <code>https://dev-dap-gateway-*.gateway.dev</code>.<br>
          • Supplies Google IAM OIDC Bearer Token.<br>
          • Encrypted via TLS 1.3.
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-blue">HTTPS REST</span>
        <span class="badge badge-blue">OIDC JWT</span>
      </div>
    </div>
    
    <div class="arrow-connector">
      <div class="arrow-label">Bearer Token</div>
      <div class="arrow-line"></div>
    </div>
    
    <div class="node-box" style="border-color: #a5b4fc; background: #eef2ff;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #e0e7ff; color: #3730a3;">🛡️</div>
          <div class="node-title">2. API Gateway</div>
        </div>
        <div class="node-body">
          • Validates JWT signature.<br>
          • Verifies audience & issuer claims.<br>
          • Impersonates <code>sa-dev-api-gateway</code>.<br>
          • Mints internal OIDC (roles/run.invoker).
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-indigo">OpenAPI 2.0</span>
        <span class="badge badge-indigo">JWKS Validated</span>
      </div>
    </div>
    
    <div class="arrow-connector">
      <div class="arrow-label">Internal OIDC</div>
      <div class="arrow-line"></div>
    </div>
    
    <div class="node-box" style="border-color: #6ee7b7; background: #f0fdf4;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #dcfce7; color: #15803d;">🤖</div>
          <div class="node-title">3. Agent 1: Coordinator</div>
        </div>
        <div class="node-body">
          • Cloud Run v2 (Gemini 1.5 Flash).<br>
          • Rejects public internet (<code>INTERNAL_ONLY</code>).<br>
          • Handles sync / async logic.
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-green">Direct VPC Egress</span>
        <span class="badge badge-green">Internal Only</span>
      </div>
    </div>
    
    <div class="arrow-connector">
      <div class="arrow-label">Pub/Sub</div>
      <div class="arrow-line"></div>
    </div>
    
    <div class="node-box" style="border-color: #c084fc; background: #faf5ff;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #f3e8ff; color: #7e22ce;">⚙️</div>
          <div class="node-title">4. Agent 2: Worker</div>
        </div>
        <div class="node-body">
          • Cloud Run v2 (Reasoning / Tools).<br>
          • Invoked by Pub/Sub Push (<code>sa-dev-ps-invoker</code>).<br>
          • Accesses Cloud SQL (PSA) and Firestore (PGA).
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-purple">Push Sub + OIDC</span>
        <span class="badge badge-amber">DLQ Protected</span>
      </div>
    </div>
  </div>
  
  <div class="footer-summary">
    <span>🔒 <strong>Zero Public Ingress:</strong> Agents unreachable without Gateway JWT verification.</span>
    <span>⚡ <strong>Sub-2ms Networking:</strong> Direct VPC Egress routes directly without VM Connector hops.</span>
  </div>
</body>
</html>
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    render_html_to_png(HTML_NETWORK_CERTS, os.path.join(OUTPUT_DIR, "network_connectivity_and_certs_diagram.png"), width=1500, height=1120)
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_architecture_diagram.png"), width=1600, height=1140)
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_minimal_architecture_diagram.png"), width=1600, height=1140)
    render_html_to_png(HTML_VPC_NET, os.path.join(OUTPUT_DIR, "gcp_vpc_network_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_HOP_BY_HOP, os.path.join(OUTPUT_DIR, "gcp_hop_by_hop_diagram.png"), width=1600, height=960)
    render_html_to_png(HTML_TERRAGRUNT, os.path.join(OUTPUT_DIR, "terragrunt_multienv_cicd_diagram.png"), width=1500, height=720)
    render_html_to_png(HTML_GATEWAY, os.path.join(OUTPUT_DIR, "api_gateway_to_cloud_run_diagram.png"), width=1500, height=620)
    print("All diagrams regenerated with tight aspect ratios successfully!")

if __name__ == "__main__":
    main()
