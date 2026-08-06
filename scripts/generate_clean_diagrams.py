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
# Diagram 1: Overall SOAM Architecture
# ==============================================================================
HTML_SOAM_ARCH = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 880px; padding: 30px; display: flex; flex-direction: column; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 25px; }
  .header h1 { font-size: 32px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
  .header p { font-size: 16px; color: #64748b; margin-top: 6px; font-weight: 500; }
  
  .main-grid { display: grid; grid-template-columns: 280px 1fr 340px; gap: 24px; flex: 1; }
  
  .column { display: flex; flex-direction: column; gap: 20px; }
  
  .card { background: #ffffff; border-radius: 16px; border: 1.5px solid #e2e8f0; padding: 22px; box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05); position: relative; }
  .card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
  .card-title { font-size: 17px; font-weight: 700; color: #0f172a; }
  .icon-badge { width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  
  .ingress-col .card { border-color: #bfdbfe; background: linear-gradient(180deg, #f8fafc 0%, #eff6ff 100%); }
  .ingress-badge { background: #dbeafe; color: #1d4ed8; }
  
  .center-col { display: flex; flex-direction: column; gap: 20px; }
  
  .mesh-card { border-color: #bbf7d0; background: #f0fdf4; border-width: 2px; }
  .mesh-badge { background: #dcfce7; color: #15803d; }
  
  .agent-box { background: #ffffff; border-radius: 12px; border: 1.5px solid #cbd5e1; padding: 16px; margin-bottom: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
  .agent-box.coordinator { border-left: 5px solid #2563eb; }
  .agent-box.worker { border-left: 5px solid #16a34a; }
  
  .agent-title { font-size: 16px; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }
  .badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 12px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
  .badge-red { background: #fee2e2; color: #991b1b; }
  
  .agent-desc { font-size: 13px; color: #475569; margin-top: 6px; line-height: 1.4; }
  .agent-tags { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  
  .bus-card { border-color: #e9d5ff; background: #faf5ff; }
  .bus-badge { background: #f3e8ff; color: #7e22ce; }
  
  .topic-item { background: #ffffff; border: 1px solid #d8b4fe; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 600; color: #581c87; font-family: ui-monospace, monospace; }
  
  .data-col .card { border-color: #fed7aa; background: #fff7ed; }
  .data-badge { background: #ffedd5; color: #c2410c; }
  
  .resource-item { background: #ffffff; border: 1px solid #fdba74; border-radius: 10px; padding: 12px; margin-bottom: 10px; }
  .resource-name { font-size: 14px; font-weight: 700; color: #9a3412; display: flex; justify-content: space-between; align-items: center; }
  .resource-detail { font-size: 12px; color: #475569; margin-top: 4px; }
  
  .footer-bar { margin-top: 18px; padding: 14px 20px; background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; justify-content: space-around; font-size: 13px; font-weight: 600; color: #334155; }
  .footer-item { display: flex; align-items: center; gap: 8px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
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
    <!-- Ingress Layer -->
    <div class="column ingress-col">
      <div class="card" style="flex: 1;">
        <div class="card-header">
          <div class="icon-badge ingress-badge">🌐</div>
          <div class="card-title">1. Ingress Layer</div>
        </div>
        
        <div class="agent-box" style="border-left: 5px solid #0284c7;">
          <div class="agent-title">
            <span>External Client</span>
            <span class="badge badge-blue">HTTPS / REST</span>
          </div>
          <div class="agent-desc">Requests signed with Google IAM OIDC Bearer Token.</div>
        </div>
        
        <div style="text-align: center; color: #0284c7; font-weight: 700; margin: 12px 0;">⬇️ Validates JWT</div>
        
        <div class="agent-box" style="border-left: 5px solid #0284c7;">
          <div class="agent-title">
            <span>Cloud API Gateway</span>
            <span class="badge badge-blue">Managed URL</span>
          </div>
          <div class="agent-desc">
            • Validates token via Google JWKS (accounts.google.com)<br>
            • Impersonates Gateway Service Account<br>
            • Routes internal request to Coordinator
          </div>
          <div class="agent-tags">
            <span class="badge badge-blue">OpenAPI 2.0</span>
            <span class="badge badge-purple">Google IAM OIDC</span>
          </div>
        </div>
        
        <div style="margin-top: 20px; padding: 12px; background: #ffffff; border-radius: 10px; border: 1px dashed #93c5fd; font-size: 12px; color: #1e40af;">
          🔒 <strong>Zero Public Ingress:</strong> Both Cloud Run agents reject direct internet traffic (<code>INTERNAL_ONLY</code>).
        </div>
      </div>
    </div>
    
    <!-- Compute Mesh & Messaging Layer -->
    <div class="column center-col">
      <!-- 2-Agent Mesh -->
      <div class="card mesh-card">
        <div class="card-header">
          <div class="icon-badge mesh-badge">🤖</div>
          <div class="card-title">2. SOAM Compute Mesh (Cloud Run v2)</div>
        </div>
        
        <div class="agent-box coordinator">
          <div class="agent-title">
            <span>Agent 1: SOAM Coordinator</span>
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
        
        <div class="agent-box worker">
          <div class="agent-title">
            <span>Agent 2: SOAM Specialist Worker</span>
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
      
      <!-- Pub/Sub Backbone -->
      <div class="card bus-card">
        <div class="card-header">
          <div class="icon-badge bus-badge">⚡</div>
          <div class="card-title">3. SOAM Message Bus (Cloud Pub/Sub)</div>
        </div>
        
        <div class="topic-item">
          <span>📨 agent-2-inbound-topic</span>
          <span class="badge badge-purple">OIDC Push Sub ➔ Agent 2</span>
        </div>
        <div class="topic-item">
          <span>📨 agent-1-inbound-topic</span>
          <span class="badge badge-purple">OIDC Push Sub ➔ Agent 1</span>
        </div>
        <div class="topic-item" style="border-color: #fca5a5; background: #fff5f5; color: #991b1b;">
          <span>🛡️ dap-dlq-topic (Dead Letter Queue)</span>
          <span class="badge badge-red">5 Retries • 7-Day Hold</span>
        </div>
      </div>
    </div>
    
    <!-- State, Storage & Egress -->
    <div class="column data-col">
      <div class="card" style="flex: 1;">
        <div class="card-header">
          <div class="icon-badge data-badge">💾</div>
          <div class="card-title">4. Private State & Egress</div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Cloud SQL PostgreSQL 15</span>
            <span class="badge badge-amber">PSA 10.10.16.x</span>
          </div>
          <div class="resource-detail">100% Private IP via Peering. Zero public internet exposure.</div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Cloud Firestore Native</span>
            <span class="badge badge-amber">PGA Zero-NAT</span>
          </div>
          <div class="resource-detail">Multi-turn agent session memory & delegation results.</div>
        </div>
        
        <div class="resource-item">
          <div class="resource-name">
            <span>Secret Manager</span>
            <span class="badge badge-amber">Encrypted Vault</span>
          </div>
          <div class="resource-detail">Fine-grained IAM accessor for DB and LLM API keys.</div>
        </div>
        
        <div class="resource-item" style="border-color: #38bdf8; background: #f0f9ff;">
          <div class="resource-name" style="color: #0369a1;">
            <span>Cloud NAT (Static Outbound)</span>
            <span class="badge badge-blue">34.x.x.x Static IP</span>
          </div>
          <div class="resource-detail">Deterministic allowlistable IP for external LLM API calls.</div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="footer-bar">
    <div class="footer-item"><div class="dot dot-blue"></div> Client & API Gateway Ingress</div>
    <div class="footer-item"><div class="dot dot-green"></div> 2-Agent Serverless Compute Mesh</div>
    <div class="footer-item"><div class="dot dot-purple"></div> Asynchronous SOAM Pub/Sub Bus</div>
    <div class="footer-item"><div class="dot dot-orange"></div> 100% Private PSA/PGA State & Secure NAT Egress</div>
  </div>
</body>
</html>
"""

# ==============================================================================
# Diagram 2: VPC Network Topology
# ==============================================================================
HTML_VPC_NET = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  body { background: #ffffff; width: 1500px; height: 880px; padding: 30px; display: flex; flex-direction: column; color: #1e293b; }
  
  .header { text-align: center; margin-bottom: 25px; }
  .header h1 { font-size: 32px; font-weight: 800; color: #0f172a; }
  .header p { font-size: 16px; color: #64748b; margin-top: 6px; font-weight: 500; }
  
  .vpc-container { background: #f8fafc; border: 2.5px solid #3b82f6; border-radius: 20px; padding: 26px; flex: 1; display: flex; flex-direction: column; position: relative; box-shadow: 0 10px 30px rgba(59,130,246,0.08); }
  .vpc-title { font-size: 20px; font-weight: 800; color: #1d4ed8; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  
  .net-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; flex: 1; }
  
  .subnet-box { background: #ffffff; border-radius: 16px; border: 2px solid #22c55e; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
  .subnet-title { font-size: 17px; font-weight: 700; color: #15803d; margin-bottom: 14px; display: flex; justify-content: space-between; }
  
  .agents-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
  .agent-card { background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 16px; }
  .agent-card h4 { font-size: 15px; font-weight: 700; color: #166534; margin-bottom: 6px; }
  .agent-card p { font-size: 12px; color: #374151; line-height: 1.4; }
  
  .direct-egress-banner { background: #dbeafe; border: 1px dashed #3b82f6; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #1e40af; font-weight: 600; text-align: center; }
  
  .peering-box { background: #ffffff; border-radius: 16px; border: 2px solid #a855f7; padding: 20px; margin-top: 18px; }
  .peering-title { font-size: 16px; font-weight: 700; color: #7e22ce; margin-bottom: 10px; display: flex; justify-content: space-between; }
  
  .tenant-vpc { background: #faf5ff; border: 1.5px dashed #c084fc; border-radius: 12px; padding: 14px; display: flex; justify-content: space-between; align-items: center; }
  
  .right-col { display: flex; flex-direction: column; gap: 20px; }
  
  .nat-box { background: #ffffff; border-radius: 16px; border: 2px solid #0ea5e9; padding: 20px; }
  .pga-box { background: #ffffff; border-radius: 16px; border: 2px solid #f59e0b; padding: 20px; flex: 1; }
  
  .pga-service { display: flex; align-items: center; gap: 10px; padding: 8px 12px; background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; margin-bottom: 8px; font-size: 13px; font-weight: 600; color: #92400e; }
  
  .badge { font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 12px; }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }
  .badge-amber { background: #fef3c7; color: #92400e; }
</style>
</head>
<body>
  <div class="header">
    <h1>GCP DAP — VPC Network Topology & Direct VPC Egress</h1>
    <p>Strict Network Isolation • Zero Connector VMs • Private Services Access • Deterministic NAT Egress</p>
  </div>
  
  <div class="vpc-container">
    <div class="vpc-title">
      <span>🌐 Customer VPC Network: dev-dap-vpc (10.10.0.0/16)</span>
      <span class="badge badge-blue">Region: europe-west1</span>
    </div>
    
    <div class="net-grid">
      <!-- Left: Subnet & Peering -->
      <div>
        <div class="subnet-box">
          <div class="subnet-title">
            <span>Workload Subnet: snet-private-workload (10.10.1.0/24)</span>
            <span class="badge badge-green">Private Google Access (PGA) Enabled</span>
          </div>
          
          <div class="agents-row">
            <div class="agent-card">
              <h4>Agent 1: SOAM Coordinator</h4>
              <p>• Cloud Run v2 (2 vCPU, 2GB)<br>• Direct VPC Egress: IP from subnet<br>• Ingress: INTERNAL_ONLY</p>
            </div>
            <div class="agent-card">
              <h4>Agent 2: SOAM Worker</h4>
              <p>• Cloud Run v2 (2 vCPU, 2GB)<br>• Direct VPC Egress: IP from subnet<br>• Ingress: INTERNAL_ONLY</p>
            </div>
          </div>
          
          <div class="direct-egress-banner">
            ⚡ Direct VPC Egress: Container IPs allocated directly from snet-private-workload (Eliminates e2-micro Connector VMs & saves ~2ms per hop)
          </div>
        </div>
        
        <div class="peering-box">
          <div class="peering-title">
            <span>Private Services Access (PSA) Peering (10.10.16.0/20)</span>
            <span class="badge badge-purple">VPC Network Peering</span>
          </div>
          <div class="tenant-vpc">
            <div>
              <div style="font-weight: 700; color: #581c87;">Google Managed Tenant VPC</div>
              <div style="font-size: 12px; color: #6b21a8; margin-top: 2px;">Cloud SQL PostgreSQL 15 Instance (10.10.16.x)</div>
            </div>
            <span class="badge badge-purple" style="background: #e9d5ff;">100% Private IP (Zero Public IP)</span>
          </div>
        </div>
      </div>
      
      <!-- Right: Cloud NAT & PGA -->
      <div class="right-col">
        <div class="nat-box">
          <div style="font-size: 16px; font-weight: 700; color: #0369a1; margin-bottom: 8px;">
            Cloud Router & Cloud NAT
          </div>
          <p style="font-size: 12px; color: #475569; margin-bottom: 10px;">
            <code>dev-dap-router</code> + <code>dev-dap-nat</code> with <code>MANUAL_ONLY</code> IP allocation.
          </p>
          <div style="background: #e0f2fe; padding: 10px; border-radius: 8px; border: 1px solid #7dd3fc; font-size: 13px; font-weight: 700; color: #0369a1; text-align: center;">
            Static Outbound IP: 34.x.x.x
          </div>
          <div style="font-size: 11px; color: #64748b; margin-top: 6px; text-align: center;">
            Allowlisted by external LLM and enterprise SaaS APIs
          </div>
        </div>
        
        <div class="pga-box">
          <div style="font-size: 16px; font-weight: 700; color: #b45309; margin-bottom: 12px;">
            Private Google Access (PGA)
          </div>
          <div class="pga-service">💾 Cloud Firestore Native</div>
          <div class="pga-service">⚡ Cloud Pub/Sub Topics</div>
          <div class="pga-service">📊 BigQuery Telemetry Dataset</div>
          <div class="pga-service">🔐 Secret Manager Vault</div>
          <div style="font-size: 11px; color: #78350f; margin-top: 8px;">
            Traverses Google's internal SDN without hitting Cloud NAT or public internet.
          </div>
        </div>
      </div>
    </div>
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
    
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_architecture_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_SOAM_ARCH, os.path.join(OUTPUT_DIR, "soam_minimal_architecture_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_VPC_NET, os.path.join(OUTPUT_DIR, "gcp_vpc_network_diagram.png"), width=1500, height=880)
    render_html_to_png(HTML_HOP_BY_HOP, os.path.join(OUTPUT_DIR, "gcp_hop_by_hop_diagram.png"), width=1500, height=720)
    render_html_to_png(HTML_TERRAGRUNT, os.path.join(OUTPUT_DIR, "terragrunt_multienv_cicd_diagram.png"), width=1500, height=720)
    render_html_to_png(HTML_GATEWAY, os.path.join(OUTPUT_DIR, "api_gateway_to_cloud_run_diagram.png"), width=1500, height=620)
    print("All diagrams regenerated with tight aspect ratios successfully!")

if __name__ == "__main__":
    main()
