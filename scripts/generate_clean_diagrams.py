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
# Diagram 1: Overall SOAM Architecture (Clear Boundary Separation)
# ==============================================================================
HTML_SOAM_ARCH = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 880px; padding: 30px; display: flex; flex-direction: column; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 22px; }
  .header h1 { font-size: 30px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 15px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .main-grid { display: grid; grid-template-columns: 280px 1fr 370px; gap: 20px; flex: 1; }
  
  .column { display: flex; flex-direction: column; gap: 16px; }
  
  .card { background: #ffffff; border-radius: 14px; border: 1.5px solid #e2e8f0; padding: 18px; box-shadow: 0 4px 16px -2px rgba(0,0,0,0.04); position: relative; }
  .card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
  .card-title { font-size: 16px; font-weight: 700; color: #0f172a; }
  .icon-badge { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
  
  .ingress-col .card { border-color: #bfdbfe; background: linear-gradient(180deg, #f8fafc 0%, #eff6ff 100%); }
  .ingress-badge { background: #dbeafe; color: #1d4ed8; }
  
  .center-col { display: flex; flex-direction: column; gap: 16px; }
  
  .mesh-card { border-color: #bbf7d0; background: #f0fdf4; border-width: 2px; }
  .mesh-badge { background: #dcfce7; color: #15803d; }
  
  .agent-box { background: #ffffff; border-radius: 10px; border: 1.5px solid #cbd5e1; padding: 14px; margin-bottom: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); }
  .agent-box.coordinator { border-left: 5px solid #2563eb; }
  .agent-box.worker { border-left: 5px solid #16a34a; }
  
  .agent-title { font-size: 15px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }
  .badge { font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 10px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  
  .agent-desc { font-size: 12px; color: #475569; margin-top: 5px; line-height: 1.35; }
  .agent-tags { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  
  .bus-card { border-color: #e9d5ff; background: #faf5ff; }
  .bus-badge { background: #f3e8ff; color: #7e22ce; }
  
  .topic-item { background: #ffffff; border: 1px solid #d8b4fe; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: 600; color: #581c87; font-family: ui-monospace, monospace; }
  
  .data-col .card { border-color: #fed7aa; background: #fff7ed; }
  .data-badge { background: #ffedd5; color: #c2410c; }
  
  .resource-item { background: #ffffff; border: 1px solid #fdba74; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; }
  .resource-name { font-size: 13px; font-weight: 700; color: #9a3412; display: flex; justify-content: space-between; align-items: center; }
  .resource-detail { font-size: 11.5px; color: #475569; margin-top: 3px; line-height: 1.3; }
  
  .footer-bar { margin-top: 14px; padding: 10px 16px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; display: flex; justify-content: space-around; font-size: 12px; font-weight: 600; color: #334155; }
  .footer-item { display: flex; align-items: center; gap: 6px; }
  .dot { width: 8px; height: 8px; border-radius: 50%; }
  .dot-blue { background: #2563eb; }
  .dot-green { background: #16a34a; }
  .dot-purple { background: #9333ea; }
  .dot-orange { background: #ea580c; }
</style>
</head>
<body>
  <div class="header">
    <h1>SOAM: Service-Oriented Agent Mesh on Google Cloud</h1>
    <p>Production-Grade 2-Agent Orchestration • Zero-Trust Ingress • Direct VPC Egress • Asynchronous Pub/Sub Backbone</p>
  </div>
  
  <div class="main-grid">
    <!-- Zone 1: Ingress Layer -->
    <div class="column ingress-col">
      <div class="card" style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div class="card-header">
            <div class="icon-badge ingress-badge">🌐</div>
            <div class="card-title">1. Ingress Layer</div>
          </div>
          
          <div style="background: #ffffff; border: 1.5px solid #93c5fd; border-radius: 10px; padding: 12px; margin-bottom: 12px;">
            <div style="font-weight: 700; font-size: 13px; color: #1e293b; display: flex; justify-content: space-between;">
              <span>External Client</span>
              <span class="badge badge-blue">HTTPS / REST</span>
            </div>
            <div style="font-size: 11.5px; color: #475569; margin-top: 4px;">
              Requests signed with Google IAM OIDC Bearer Token.
            </div>
          </div>
          
          <div style="text-align: center; color: #2563eb; font-weight: 700; font-size: 12px; margin: 8px 0;">
            ⬇️ Validates JWT
          </div>
          
          <div style="background: #ffffff; border: 1.5px solid #2563eb; border-radius: 10px; padding: 12px;">
            <div style="font-weight: 700; font-size: 13px; color: #1e40af; display: flex; justify-content: space-between;">
              <span>Cloud API Gateway</span>
              <span class="badge badge-blue">Managed URL</span>
            </div>
            <div style="font-size: 11.5px; color: #475569; margin-top: 4px; line-height: 1.35;">
              • Validates token via Google JWKS (accounts.google.com)<br>
              • Impersonates Gateway Service Account<br>
              • Routes internal request to Coordinator
            </div>
            <div style="margin-top: 8px; display: flex; gap: 4px;">
              <span class="badge badge-blue">OpenAPI 2.0</span>
              <span class="badge badge-indigo" style="background:#e0e7ff; color:#3730a3;">Google IAM OIDC</span>
            </div>
          </div>
        </div>
        
        <div style="background: #eff6ff; border: 1px dashed #3b82f6; border-radius: 8px; padding: 8px 10px; font-size: 11px; color: #1e40af;">
          🔒 <strong>Zero Public Ingress:</strong> Both Cloud Run agents reject direct internet traffic (INTERNAL_ONLY).
        </div>
      </div>
    </div>
    
    <!-- Zone 2 & 3: Compute Mesh & Message Bus -->
    <div class="column center-col">
      <!-- Zone 2: Serverless Compute Mesh -->
      <div class="card mesh-card">
        <div class="card-header">
          <div class="icon-badge mesh-badge">🤖</div>
          <div class="card-title">2. Serverless Compute Mesh (Cloud Run v2)</div>
        </div>
        
        <!-- Agent 1 -->
        <div class="agent-box coordinator">
          <div class="agent-title">
            <span style="color: #1e3a8a;">Agent 1: SOAM Coordinator</span>
            <span class="badge badge-blue">Gemini 1.5 Flash</span>
          </div>
          <div class="agent-desc">
            Ingress orchestrator, task classifier & context loader. Answers simple queries synchronously; dispatches complex tasks to Pub/Sub.
          </div>
          <div class="agent-tags">
            <span class="badge badge-blue">Direct VPC Egress</span>
            <span class="badge badge-green">Internal Only Ingress</span>
            <span class="badge badge-purple">sa-dev-agent-1</span>
          </div>
        </div>
        
        <!-- Agent 2 -->
        <div class="agent-box worker">
          <div class="agent-title">
            <span style="color: #14532d;">Agent 2: SOAM Specialist Worker</span>
            <span class="badge badge-green">Diagnostics / Reasoning</span>
          </div>
          <div class="agent-desc">
            Executes deep reasoning loops, queries private SQL database, updates Firestore session state, and invokes external tools.
          </div>
          <div class="agent-tags">
            <span class="badge badge-blue">Direct VPC Egress</span>
            <span class="badge badge-green">Internal Only Ingress</span>
            <span class="badge badge-purple">sa-dev-agent-2</span>
          </div>
        </div>
      </div>
      
      <!-- Zone 3: SOAM Message Bus -->
      <div class="card bus-card">
        <div class="card-header">
          <div class="icon-badge bus-badge">⚡</div>
          <div class="card-title">3. SOAM Message Bus (Google Cloud Pub/Sub)</div>
        </div>
        
        <div class="topic-item">
          <span>📨 agent-2-inbound-topic</span>
          <span class="badge badge-purple">OIDC Push Sub ➔ Agent 2</span>
        </div>
        <div class="topic-item">
          <span>📨 agent-1-inbound-topic</span>
          <span class="badge badge-purple">OIDC Push Sub ➔ Agent 1</span>
        </div>
        <div class="topic-item" style="border-color: #fca5a5; color: #991b1b;">
          <span>🧯 dap-dlq-topic (Dead Letter Queue)</span>
          <span class="badge badge-amber" style="background:#fee2e2; color:#991b1b;">5 Retries • 7-Day Hold</span>
        </div>
      </div>
    </div>
    
    <!-- Zone 4: Managed State & Private Egress -->
    <div class="column data-col">
      <div class="card" style="flex: 1;">
        <div class="card-header">
          <div class="icon-badge data-badge">💾</div>
          <div class="card-title">4. Managed State & Egress</div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Cloud SQL PostgreSQL 15</span>
            <span class="badge badge-amber">Google Tenant VPC</span>
          </div>
          <div class="resource-detail">
            100% Private IP (10.10.16.x) via <strong>Private Services Access (PSA)</strong> peering. Zero public IP exposure.
          </div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Cloud Firestore Native</span>
            <span class="badge badge-green">Private Google Access</span>
          </div>
          <div class="resource-detail">
            Multi-turn agent session memory & delegation results over internal Google SDN (PGA VIPs).
          </div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Secret Manager</span>
            <span class="badge badge-amber">Private Google Access</span>
          </div>
          <div class="resource-detail">
            Fine-grained IAM accessor for DB credentials and external LLM API keys.
          </div>
        </div>
        
        <div class="resource-item" style="border-color: #93c5fd;">
          <div class="resource-name">
            <span style="color: #1e40af;">Cloud NAT Gateway</span>
            <span class="badge badge-blue">Customer VPC Subnet</span>
          </div>
          <div class="resource-detail">
            Deterministic static outbound IP (<code>34.x.x.x</code>) for external LLM API allowlisting.
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="footer-bar">
    <div class="footer-item"><div class="dot dot-blue"></div> Client & API Gateway Ingress</div>
    <div class="footer-item"><div class="dot dot-green"></div> 2-Agent Serverless Compute Mesh</div>
    <div class="footer-item"><div class="dot dot-purple"></div> Asynchronous SOAM Pub/Sub Bus</div>
    <div class="footer-item"><div class="dot dot-orange"></div> PSA Peered DB, PGA PaaS & Secure NAT Egress</div>
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
  body { background: #ffffff; width: 1500px; height: 880px; padding: 30px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 16px; }
  .header h1 { font-size: 30px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 15px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .domains-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; flex: 1; margin-bottom: 12px; }
  
  .domain-card { background: #ffffff; border-radius: 14px; border: 2px solid #cbd5e1; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 3px 12px rgba(0,0,0,0.03); }
  
  .domain-title { font-size: 16px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  
  .inner-box { background: #f8fafc; border-radius: 10px; border: 1.5px solid #e2e8f0; padding: 12px; margin-bottom: 8px; }
  .inner-title { font-size: 13.5px; font-weight: 700; color: #0f172a; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center; }
  .inner-desc { font-size: 12px; color: #475569; line-height: 1.35; }
  
  .badge { font-size: 10.5px; font-weight: 600; padding: 2px 7px; border-radius: 8px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
  
  .footer-summary { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 18px; display: flex; justify-content: space-around; font-size: 12px; font-weight: 600; color: #334155; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Network Topology & Architectural Boundaries</h1>
    <p>Precise Boundary Separation: Customer VPC • Serverless Compute Plane • Google Tenant VPC • Private Google Access</p>
  </div>
  
  <div class="domains-grid">
    <!-- Domain 1: Customer VPC Network -->
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
            • Firewall Rule: <code>allow-internal</code> (TCP 443, 5432, 8080).<br>
            • Zero public IP addresses on this subnet.
          </div>
        </div>
        
        <div class="inner-box" style="border-color: #93c5fd; background: #ffffff;">
          <div class="inner-title">
            <span>Cloud Router & Cloud NAT Gateway</span>
            <span class="badge badge-blue">Static IP: 34.x.x.x</span>
          </div>
          <div class="inner-desc">
            • <code>dev-dap-router</code> + <code>dev-dap-nat</code> (MANUAL_ONLY allocation).<br>
            • Translates outbound agent calls to external LLM & SaaS APIs.
          </div>
        </div>
      </div>
      
      <div style="font-size: 11px; color: #1e40af; font-weight: 600; margin-top: 6px;">
        📍 Region: europe-west1 • Managed by Customer Terraform
      </div>
    </div>
    
    <!-- Domain 2: Serverless Compute Plane -->
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
            • Direct VPC Egress: Container attaches directly to <code>snet-private-workload</code>.<br>
            • Ingress: <code>INGRESS_TRAFFIC_INTERNAL_ONLY</code> (Protected from direct web).
          </div>
        </div>
        
        <div class="inner-box" style="border-color: #86efac; background: #ffffff;">
          <div class="inner-title">
            <span>Agent 2: SOAM Worker</span>
            <span class="badge badge-green">sa-dev-agent-2</span>
          </div>
          <div class="inner-desc">
            • Direct VPC Egress: Container attaches directly to <code>snet-private-workload</code>.<br>
            • Invoked exclusively via Pub/Sub Push Subscription (OIDC auth).
          </div>
        </div>
      </div>
      
      <div style="background: #dcfce7; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #166534; font-weight: 600;">
        ⚡ <strong>Direct VPC Egress:</strong> Sub-2ms container routing into Customer VPC without VM connector bottlenecks.
      </div>
    </div>
    
    <!-- Domain 3: Google-Managed Tenant VPC (Cloud SQL) -->
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
            • <code>ipv4_enabled = false</code> (No public IP address exists on this instance).<br>
            • Peered to Customer VPC via <strong>Private Services Access (PSA)</strong>.<br>
            • Reachable only from Cloud Run agents via Direct VPC Egress over peering.
          </div>
        </div>
      </div>
      
      <div style="background: #f3e8ff; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #6b21a8; font-weight: 600;">
        🔒 <strong>Database Isolation:</strong> Database lives in Google's Tenant VPC, completely isolated from internet.
      </div>
    </div>
    
    <!-- Domain 4: Google Cloud Multi-Tenant PaaS / APIs -->
    <div class="domain-card" style="border-color: #f59e0b; background: #fffbeb;">
      <div>
        <div class="domain-title" style="color: #92400e;">
          <span>☁️ Google Cloud Managed PaaS & APIs</span>
          <span class="badge badge-amber">Private Google Access (PGA)</span>
        </div>
        
        <div class="inner-box" style="border-color: #fde68a; background: #ffffff;">
          <div class="inner-title">
            <span>Cloud Firestore Native + Cloud Pub/Sub + Secret Manager</span>
            <span class="badge badge-amber">Google Global SDN VIPs</span>
          </div>
          <div class="inner-desc">
            • Reached over Google internal backbone (VIPs <code>199.36.153.8/30</code>).<br>
            • Traffic from Workload Subnet never traverses Cloud NAT or public internet.<br>
            • Zero egress NAT cost for Google PaaS API traffic.
          </div>
        </div>
      </div>
      
      <div style="background: #fef3c7; border-radius: 6px; padding: 6px 10px; font-size: 11px; color: #92400e; font-weight: 600;">
        ⚡ <strong>PGA Advantage:</strong> High-bandwidth, sub-millisecond access to Google PaaS APIs.
      </div>
    </div>
  </div>
  
  <div class="footer-summary">
    <span>🌐 <strong>Customer VPC:</strong> Only contains subnets, NAT router, and peering connections.</span>
    <span>🤖 <strong>Compute & State:</strong> Cloud Run is serverless, Cloud SQL is in Tenant VPC, and PaaS APIs are reached via PGA.</span>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 3: Hop-by-Hop Journey (Tight & Rich)
# ==============================================================================
HTML_HOP_BY_HOP = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 720px; padding: 25px 40px; display: flex; flex-direction: column; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 20px; }
  .header h1 { font-size: 30px; font-weight: 800; color: #0f172a; }
  .header p { font-size: 15px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .hops-container { display: flex; flex-direction: column; gap: 10px; flex: 1; }
  
  .hop-card { background: #ffffff; border-radius: 12px; border: 1.5px solid #e2e8f0; padding: 12px 18px; display: flex; align-items: center; gap: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
  
  .hop-num { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 800; color: #ffffff; flex-shrink: 0; }
  
  .hop-content { flex: 1; }
  .hop-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 3px; display: flex; justify-content: space-between; align-items: center; }
  .hop-desc { font-size: 12.5px; color: #475569; line-height: 1.35; }
  
  .badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-teal { background: #ccfbf1; color: #115e59; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — Hop-by-Hop Request & Packet Journey</h1>
    <p>Deterministic Lifecycle from Ingress JWT Validation to Database Query & Static NAT Egress</p>
  </div>
  
  <div class="hops-container">
    <div class="hop-card" style="border-left: 5px solid #2563eb; background: #f8fafc;">
      <div class="hop-num" style="background: #2563eb;">1</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 1: Edge Ingress (Client ➔ Cloud API Gateway)</span>
          <span class="badge badge-blue">HTTPS / Bearer Token</span>
        </div>
        <div class="hop-desc">Client initiates HTTPS call carrying a Google IAM OIDC Bearer Token signed by accounts.google.com.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #4f46e5; background: #f8fafc;">
      <div class="hop-num" style="background: #4f46e5;">2</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 2: JWT Validation & Internal Routing (API Gateway ➔ Agent 1)</span>
          <span class="badge badge-indigo">Google JWKS Validation</span>
        </div>
        <div class="hop-desc">Gateway validates JWT signature against Google public keys, impersonates <code>sa-dev-api-gateway</code> (roles/run.invoker), and proxies to Agent 1.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #0284c7; background: #f8fafc;">
      <div class="hop-num" style="background: #0284c7;">3</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 3: SOAM Dispatch Classification (Agent 1 Coordinator)</span>
          <span class="badge badge-blue">Gemini 1.5 Flash</span>
        </div>
        <div class="hop-desc">Agent 1 evaluates request complexity. Lightweight queries return synchronous HTTP responses; specialist tasks are published to Pub/Sub.</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #9333ea; background: #f8fafc;">
      <div class="hop-num" style="background: #9333ea;">4</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 4: SOAM Asynchronous Delivery (Pub/Sub ➔ Agent 2)</span>
          <span class="badge badge-purple">OIDC Push Subscription</span>
        </div>
        <div class="hop-desc">Pub/Sub push subscription invokes Agent 2 with OIDC token minted for <code>sa-dev-ps-invoker</code>. Failed tasks route to Dead-Letter Queue (DLQ).</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #16a34a; background: #f8fafc;">
      <div class="hop-num" style="background: #16a34a;">5</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 5: Context & Session State Access (Agent ➔ Firestore Native)</span>
          <span class="badge badge-green">Private Google Access (PGA)</span>
        </div>
        <div class="hop-desc">Agent retrieves conversation context and saves execution status to Firestore via Google's internal private VIPs (zero NAT cost).</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #0d9488; background: #f8fafc;">
      <div class="hop-num" style="background: #0d9488;">6</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 6: Relational Data Query (Agent ➔ Cloud SQL PostgreSQL)</span>
          <span class="badge badge-teal">PSA Peering 10.10.16.x</span>
        </div>
        <div class="hop-desc">Agent routes SQL query over Direct VPC Egress into PSA Peering. Database has <code>ipv4_enabled = false</code> (never internet-accessible).</div>
      </div>
    </div>
    
    <div class="hop-card" style="border-left: 5px solid #d97706; background: #f8fafc;">
      <div class="hop-num" style="background: #d97706;">7</div>
      <div class="hop-content">
        <div class="hop-title">
          <span>Hop 7: External Tool & LLM API Egress (Agent ➔ Cloud NAT)</span>
          <span class="badge badge-amber">Static Public IP (34.x.x.x)</span>
        </div>
        <div class="hop-desc">Outbound calls to external LLM APIs exit via Direct VPC Egress ➔ Cloud NAT with a deterministic static IP for enterprise firewall allowlisting.</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 4: Terragrunt Multi-Environment CI/CD (Tight & Balanced)
# ==============================================================================
HTML_TERRAGRUNT = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 720px; padding: 25px 40px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 15px; }
  .header h1 { font-size: 30px; font-weight: 800; color: #0f172a; }
  .header p { font-size: 15px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .section-card { background: #ffffff; border-radius: 14px; border: 1.5px solid #e2e8f0; padding: 18px; box-shadow: 0 3px 12px rgba(0,0,0,0.03); }
  
  .section-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
  
  .pipeline-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
  .pipeline-col { background: #f8fafc; border-radius: 10px; border: 1.5px solid #cbd5e1; padding: 12px 14px; }
  .col-header { font-size: 14px; font-weight: 700; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
  .step-item { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; margin-bottom: 6px; font-size: 12px; font-weight: 600; color: #334155; }
  
  .env-grid { display: grid; grid-template-columns: 260px 1fr; gap: 16px; }
  .root-hcl-box { background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 10px; padding: 14px; }
  .envs-subgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .env-item { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 12px; }
  
  .dag-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; }
  .dag-item { background: #ffffff; border: 1.5px solid #94a3b8; border-radius: 8px; padding: 8px; text-align: center; font-size: 12px; font-weight: 700; color: #1e293b; }
  .dag-num { font-size: 11px; color: #64748b; margin-bottom: 2px; }
  
  .badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-red { background: #fee2e2; color: #991b1b; }
</style>
</head>
<body>
  <div class="header">
    <h1>Terragrunt Multi-Environment GitOps CI/CD</h1>
    <p>Keyless Workload Identity Federation (WIF) • 3-Tier Promotion • 7-Module DAG Architecture</p>
  </div>
  
  <!-- CI/CD Pipeline -->
  <div class="section-card" style="border-color: #c084fc; background: #faf5ff;">
    <div class="section-title">
      <span>🚀 GitHub Actions GitOps Pipeline (.github/workflows/terragrunt-gcp.yml)</span>
      <span class="badge badge-purple">Keyless Auth via WIF</span>
    </div>
    <div class="pipeline-grid">
      <div class="pipeline-col">
        <div class="col-header">
          <span>🧪 Development (dev)</span>
          <span class="badge badge-blue">Branch: develop</span>
        </div>
        <div class="step-item">1. PR open ➔ terragrunt plan (dev)</div>
        <div class="step-item">2. Merge PR ➔ terragrunt apply (dev)</div>
      </div>
      
      <div class="pipeline-col">
        <div class="col-header">
          <span>🚀 Staging (staging)</span>
          <span class="badge badge-amber">Branch: staging</span>
        </div>
        <div class="step-item">1. PR open ➔ terragrunt plan (staging)</div>
        <div class="step-item">2. Merge PR ➔ terragrunt apply (staging)</div>
      </div>
      
      <div class="pipeline-col">
        <div class="col-header">
          <span>🛡️ Production (prod)</span>
          <span class="badge badge-red">Branch: main</span>
        </div>
        <div class="step-item">1. PR open ➔ terragrunt plan (prod)</div>
        <div class="step-item">2. Merge ➔ <strong>Manual Approval Gate</strong></div>
      </div>
    </div>
  </div>
  
  <!-- Terragrunt Hierarchy -->
  <div class="section-card" style="border-color: #93c5fd; background: #f0f9ff;">
    <div class="section-title">
      <span>📁 Terragrunt Directory & Environment Model (infra/environments/)</span>
      <span class="badge badge-blue">DRY Remote State</span>
    </div>
    <div class="env-grid">
      <div class="root-hcl-box">
        <div style="font-weight: 700; color: #1e40af; margin-bottom: 4px;">root.hcl (Root Config)</div>
        <div style="font-size: 11.5px; color: #334155; line-height: 1.35;">
          • Central GCS Backend generation<br>
          • Google Provider generation<br>
          • Dynamic environment variable loading
        </div>
      </div>
      <div class="envs-subgrid">
        <div class="env-item">
          <div style="font-weight: 700; color: #1e293b; font-size: 13px;">infra/environments/dev</div>
          <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">Subnet: 10.10.1.0/24<br>DB: db-f1-micro<br>Images: :latest</div>
        </div>
        <div class="env-item">
          <div style="font-weight: 700; color: #1e293b; font-size: 13px;">infra/environments/staging</div>
          <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">Subnet: 10.20.1.0/24<br>DB: db-custom-2-7680<br>Images: :staging</div>
        </div>
        <div class="env-item">
          <div style="font-weight: 700; color: #1e293b; font-size: 13px;">infra/environments/prod</div>
          <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">Subnet: 10.30.1.0/22 (HA)<br>DB: db-custom-4-15360<br>Images: :v1.0.0</div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 7 Terraform Modules DAG -->
  <div class="section-card" style="border-color: #86efac; background: #f0fdf4;">
    <div class="section-title">
      <span>⚙️ 7-Module Terraform DAG (infra/modules/)</span>
      <span class="badge badge-green">Strict Dependency Order</span>
    </div>
    <div class="dag-grid">
      <div class="dag-item" style="border-color: #3b82f6;">
        <div class="dag-num">01</div>
        <div>networking</div>
      </div>
      <div class="dag-item" style="border-color: #6366f1;">
        <div class="dag-num">02</div>
        <div>security_iam</div>
      </div>
      <div class="dag-item" style="border-color: #f59e0b;">
        <div class="dag-num">03</div>
        <div>data_state</div>
      </div>
      <div class="dag-item" style="border-color: #a855f7;">
        <div class="dag-num">04</div>
        <div>messaging</div>
      </div>
      <div class="dag-item" style="border-color: #10b981;">
        <div class="dag-num">05</div>
        <div>compute_services</div>
      </div>
      <div class="dag-item" style="border-color: #06b6d4;">
        <div class="dag-num">06</div>
        <div>ingress_gateway</div>
      </div>
      <div class="dag-item" style="border-color: #64748b;">
        <div class="dag-num">07</div>
        <div>observability</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 5: API Gateway Ingress (Horizontal Architecture Flow)
# ==============================================================================
HTML_GATEWAY = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 620px; padding: 30px 40px; display: flex; flex-direction: column; color: #1e293b; justify-content: space-between; }
  
  .header { text-align: center; margin-bottom: 20px; }
  .header h1 { font-size: 30px; font-weight: 800; color: #0f172a; }
  .header p { font-size: 15px; color: #64748b; margin-top: 4px; font-weight: 500; }
  
  .arch-row { display: flex; align-items: stretch; justify-content: space-between; gap: 16px; flex: 1; margin: 20px 0; }
  
  .node-box { flex: 1; background: #ffffff; border-radius: 14px; border: 2px solid #e2e8f0; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
  
  .node-header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
  .node-icon { width: 38px; height: 38px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .node-title { font-size: 16px; font-weight: 700; color: #0f172a; }
  
  .node-body { font-size: 12.5px; color: #475569; line-height: 1.45; flex: 1; }
  .node-body code { background: #f1f5f9; padding: 2px 5px; border-radius: 4px; font-size: 11px; color: #0f172a; }
  
  .node-footer { margin-top: 14px; display: flex; flex-wrap: wrap; gap: 6px; }
  
  .arrow-connector { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 40px; }
  .arrow-line { height: 3px; width: 100%; background: #94a3b8; position: relative; }
  .arrow-line::after { content: ''; position: absolute; right: 0; top: -5px; width: 0; height: 0; border-top: 6px solid transparent; border-bottom: 6px solid transparent; border-left: 10px solid #94a3b8; }
  .arrow-label { font-size: 10px; font-weight: 700; color: #64748b; margin-bottom: 6px; text-align: center; }
  
  .badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 8px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-indigo { background: #e0e7ff; color: #3730a3; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  
  .footer-summary { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 12px 20px; display: flex; justify-content: space-around; font-size: 12.5px; font-weight: 600; color: #475569; }
</style>
</head>
<body>
  <div class="header">
    <h1>Google Cloud API Gateway Ingress to Cloud Run Mesh</h1>
    <p>Zero-Trust Security • Google IAM OIDC JWT Validation • Internal-Only Ingress</p>
  </div>
  
  <div class="arch-row">
    <!-- Node 1: External Client -->
    <div class="node-box" style="border-color: #93c5fd; background: #f8fafc;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #dbeafe; color: #1d4ed8;">👤</div>
          <div class="node-title">1. External Client</div>
        </div>
        <div class="node-body">
          • Initiates HTTPS REST request.<br>
          • Acquires Google IAM OIDC Identity Token.<br>
          • Attaches token to <code>Authorization: Bearer &lt;JWT&gt;</code>.
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-blue">HTTPS / 443</span>
        <span class="badge badge-indigo">Google OIDC JWT</span>
      </div>
    </div>
    
    <div class="arrow-connector">
      <div class="arrow-label">JWT</div>
      <div class="arrow-line"></div>
    </div>
    
    <!-- Node 2: Cloud API Gateway -->
    <div class="node-box" style="border-color: #818cf8; background: #eef2ff;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #e0e7ff; color: #4338ca;">🌐</div>
          <div class="node-title">2. Cloud API Gateway</div>
        </div>
        <div class="node-body">
          • Intercepts edge HTTPS traffic.<br>
          • Validates JWT signature via Google JWKS.<br>
          • Enforces OpenAPI security definition.<br>
          • Impersonates <code>sa-dev-api-gateway</code>.
        </div>
      </div>
      <div class="node-footer">
        <span class="badge badge-indigo">Managed Gateway</span>
        <span class="badge badge-purple">OpenAPI 2.0</span>
      </div>
    </div>
    
    <div class="arrow-connector">
      <div class="arrow-label">Internal</div>
      <div class="arrow-line"></div>
    </div>
    
    <!-- Node 3: Agent 1 Coordinator -->
    <div class="node-box" style="border-color: #6ee7b7; background: #f0fdf4;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #dcfce7; color: #15803d;">🤖</div>
          <div class="node-title">3. Agent 1: Coordinator</div>
        </div>
        <div class="node-body">
          • Cloud Run v2 (Gemini 1.5 Flash).<br>
          • Rejects all direct public internet calls (<code>INTERNAL_ONLY</code>).<br>
          • Answers sync queries directly OR publishes specialist tasks to Pub/Sub.
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
    
    <!-- Node 4: Agent 2 Worker -->
    <div class="node-box" style="border-color: #c084fc; background: #faf5ff;">
      <div>
        <div class="node-header">
          <div class="node-icon" style="background: #f3e8ff; color: #7e22ce;">⚙️</div>
          <div class="node-title">4. Agent 2: Worker</div>
        </div>
        <div class="node-body">
          • Cloud Run v2 (Reasoning / Tools).<br>
          • Invoked by Pub/Sub Push Subscription with OIDC auth (<code>sa-dev-ps-invoker</code>).<br>
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
    <span>🔒 <strong>Zero Public Ingress:</strong> Agents cannot be reached directly without passing Gateway JWT verification.</span>
    <span>⚡ <strong>Sub-2ms Networking:</strong> Direct VPC Egress routes directly without VM Connector hops.</span>
  </div>
</body>
</html>
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    render_html_to_png(HTML_NETWORK_CERTS, os.path.join(OUTPUT_DIR, "network_connectivity_and_certs_diagram.png"), width=1500, height=1120)
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_architecture_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_minimal_architecture_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_VPC_NET, os.path.join(OUTPUT_DIR, "gcp_vpc_network_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_HOP_BY_HOP, os.path.join(OUTPUT_DIR, "gcp_hop_by_hop_diagram.png"), width=1500, height=720)
    render_html_to_png(HTML_TERRAGRUNT, os.path.join(OUTPUT_DIR, "terragrunt_multienv_cicd_diagram.png"), width=1500, height=720)
    render_html_to_png(HTML_GATEWAY, os.path.join(OUTPUT_DIR, "api_gateway_to_cloud_run_diagram.png"), width=1500, height=620)
    print("All diagrams regenerated with tight aspect ratios successfully!")

if __name__ == "__main__":
    main()
