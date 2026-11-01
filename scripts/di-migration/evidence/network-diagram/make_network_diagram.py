#!/usr/bin/env python3
"""
Deal Intelligence network diagram (designed version), drawn in the house style of
the 2025 Data Flow Diagram: dashed trust boundaries, rounded nodes, labelled flows.

CloudFront and the NAT instance sit *on* the account boundary: everything that
comes in crosses CloudFront, everything that goes out crosses the NAT (except the
Fargate tasks, which today leave from their own public IP - finding A of
docs/infra-edge-review-2026-11-01.md in di-backend-api).

Facts as verified 2026-11-01 (read-only) in di-backend-api docs:
infra-edge-review-2026-11-01.md and auth-hardening-2026-11-01.md.

    python3 make_network_diagram.py           # writes the .svg and .png next to this file
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
W, H = 1240, 1470

EXT = ("#ffe6cc", "#d79b00")      # outside the account
BND = ("#fff2cc", "#d6b656")      # devices on the boundary
INT = ("#dae8fc", "#6c8ebf")      # inside the account
DAT = ("#d5e8d4", "#82b366")      # data stores
SUP = ("#e1d5e7", "#9673a6")      # supporting services
FONT = "Helvetica, Arial, sans-serif"
p: list[str] = []


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, anchor="middle", weight="normal", fill="#1a1a1a", style=""):
    p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
             f'text-anchor="{anchor}" fill="{fill}" {style}>{esc(s)}</text>')


def lines(cx, cy, rows, size=12, lead=None, weight="normal", fill="#1a1a1a"):
    """Vertically centred block of lines; rows may be (text, size, weight)."""
    norm = [(r if isinstance(r, tuple) else (r, size, weight)) for r in rows]
    lead = lead or (size + 4)
    total = sum(r[1] + 4 for r in norm) - 4
    y = cy - total / 2
    for t, sz, wt in norm:
        y += sz
        text(cx, y, t, size=sz, weight=wt, fill=fill)
        y += 4


def box(x, y, w, h, rows, pal=INT, r=8, size=12, dash=None):
    f, s = pal
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{f}" '
             f'stroke="{s}" stroke-width="1.6"{d}/>')
    lines(x + w / 2, y + h / 2, rows, size=size)


def boundary(x, y, w, h, label, color="#444"):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="none" '
             f'stroke="{color}" stroke-width="1.6" stroke-dasharray="8 5"/>')
    text(x + 14, y + 22, label, size=13, anchor="start", weight="bold", fill=color)


def cyl(x, y, w, h, rows):
    f, s = DAT
    ry = 14
    p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 1 {w},0 v{h-2*ry} a{w/2},{ry} 0 0 1 {-w},0 z" '
             f'fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 0 {w},0" fill="none" stroke="{s}" stroke-width="1.6"/>')
    lines(x + w / 2, y + h / 2 + 6, rows, size=11.5)


def arrow(x1, y1, x2, y2, label=None, dashed=False, lx=None, ly=None, color="#1a1a1a", anchor="middle"):
    d = ' stroke-dasharray="6 4"' if dashed else ""
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.7" '
             f'marker-end="url(#a)"{d}/>')
    if label:
        text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6,
             label, size=10.5, fill="#333", anchor=anchor)


def elbow(pts, label=None, dashed=False, lx=None, ly=None, color="#1a1a1a"):
    d = ' stroke-dasharray="6 4"' if dashed else ""
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    p.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.7" '
             f'marker-end="url(#a)"{d}/>')
    if label:
        text(lx, ly, label, size=10.5, fill="#333")


# ---------------------------------------------------------------- header
text(40, 48, "Deal Intelligence — Network Diagram", size=26, anchor="start", weight="bold")
text(40, 74, "Mo Messidi, Chief Executive Officer, Deal Intelligence", size=12.5, anchor="start", fill="#444")
text(40, 96, "Production AWS account 164482277879 (us-east-1). Everything inbound crosses CloudFront; "
             "everything outbound crosses the NAT instance.", size=12.5, anchor="start", fill="#444")
text(40, 116, "Verified read-only against the live account, 2026-11-01.", size=11.5, anchor="start", fill="#777")

# ---------------------------------------------------------------- outside
boundary(60, 150, 1120, 150, "Outside the account — customers and third parties")
ext_y, ext_h = 192, 84
xs = [80, 300, 520, 740, 960]
box(xs[0], ext_y, 200, ext_h, [("Customers", 13, "bold"), "MCP clients · REST API",
                               "Clay · CRM · Slack"], pal=EXT)
box(xs[1], ext_y, 200, ext_h, [("PropelAuth", 13, "bold"), "Google SSO · JWT",
                               "API keys for MCP / li"], pal=EXT)
box(xs[2], ext_y, 200, ext_h, [("Customer CRMs", 13, "bold"), "HubSpot · Salesforce",
                               "OAuth tokens in Secrets Mgr"], pal=EXT)
box(xs[3], ext_y, 200, ext_h, [("Google Workspace", 13, "bold"), "identity · email",
                               "directory sync"], pal=EXT)
box(xs[4], ext_y, 200, ext_h, [("Data vendors", 13, "bold"), "enrichment · search",
                               "egress only"], pal=EXT)

# ---------------------------------------------------------------- account boundary
ACC_Y = 380
p.append(f'<rect x="60" y="{ACC_Y}" width="1120" height="1040" rx="4" ry="4" fill="none" '
         'stroke="#2b6cb0" stroke-width="1.6" stroke-dasharray="8 5"/>')
text(76, ACC_Y + 1026, "Deal Intelligence AWS account 164482277879 — us-east-1 (production)",
     size=13, anchor="start", weight="bold", fill="#2b6cb0")

# devices ON the boundary
box(150, ACC_Y - 42, 400, 84,
    [("CloudFront  E1QUZLMQLDUTYL", 12.5, "bold"),
     "api.dealintelligence.io · mcp.dealintelligence.io",
     "TLS 1.2+ · AWS Shield Standard · the only way in"], pal=BND)
box(700, ACC_Y - 42, 400, 84,
    [("NAT instance  t3.micro  52.70.24.151", 12.5, "bold"),
     "i-0c5a7ab0… · IMDSv2 · SSM · no key pair · no public ingress",
     "the only way out (lives in the public subnet below)"], pal=BND)

# inbound / outbound arrows across the boundary
arrow(180, ext_y + ext_h, 230, ACC_Y - 42, "HTTPS", lx=150, ly=345, anchor="start")
arrow(760, ACC_Y - 42, 470, ext_y + ext_h, "validate JWT / API key", lx=545, ly=316)
arrow(860, ACC_Y - 42, 650, ext_y + ext_h, "OAuth · CRM sync", lx=770, ly=322)
arrow(960, ACC_Y - 42, 848, ext_y + ext_h, "directory · mail", lx=925, ly=316)
arrow(1060, ACC_Y - 42, 1056, ext_y + ext_h, "enrichment", lx=1104, ly=322)

# ---------------------------------------------------------------- edge protection
box(150, 450, 400, 104,
    [("Edge protection — in code, no AWS WAF", 12.5, "bold"),
     "X-Origin-Verify header → OriginVerifyMiddleware",
     "(a direct hit on a function URL gets 403)",
     "rate limiting shared across Lambdas via DocumentDB",
     "keyed by credential, then IP · security headers · log redaction"], pal=BND, size=11)
arrow(350, ACC_Y + 42, 350, 450)

box(150, 584, 400, 78,
    [("Lambda function URLs", 12.5, "bold"),
     "app — origin-verified   ·   mcp — bearer token",
     "batchOrchestrator · documentdb-proxy — SigV4 (aws_iam)"], pal=INT, size=11)
arrow(350, 554, 350, 584)

# ---------------------------------------------------------------- VPC
boundary(90, 690, 1060, 610, "VPC di-backend-vpc 10.0.0.0/16", "#2f855a")

# private subnets
boundary(112, 724, 1016, 330, "Private subnets — us-east-1a / 1b / 1f", "#555")
box(136, 760, 470, 86, [("Lambda app — FastAPI", 12.5, "bold"),
                        "PropelAuth bearer · X-Internal-Key header",
                        "tenant taken from the token · 112 routes authenticated"], size=11)
box(630, 760, 474, 86, [("Lambda mcp — MCP server", 12.5, "bold"),
                        "PropelAuth API keys",
                        "own bearer auth on its function URL"], size=11)
box(136, 864, 300, 64, [("Lambda batchOrchestrator", 12, "bold"), "launches Fargate jobs"], size=10.5)
box(456, 864, 300, 64, [("Lambda documentdb-proxy", 12, "bold"), "SigV4 only"], size=10.5)
box(776, 864, 328, 64, [("Scheduled Lambdas", 12, "bold"),
                        "accessReview · dataRetention · breachDetection"], size=10.5)
cyl(390, 952, 460, 88, [("DocumentDB 5.0 — di-backend-production-cluster", 12, "bold"),
                        "private · TLS · KMS-encrypted · deletion protection · 35-day backups",
                        "port 27017 reachable only from the Lambda and NAT security groups"])

arrow(330, 662, 330, 760)
elbow([(520, 640), (880, 640), (880, 760)])
arrow(380, 846, 480, 952)
arrow(830, 846, 740, 952)
arrow(286, 928, 430, 952)
arrow(940, 928, 800, 952)
text(150, 944, "rate-limit counters", size=10, fill="#333", anchor="start")

# public subnet
boundary(112, 1076, 1016, 198, "Public subnet", "#555")
box(136, 1112, 420, 94, [("Fargate batch tasks — di-jobs-production-cluster", 12, "bold"),
                         "no ingress rules on the security group",
                         "egress leaves from the task's own public IP,",
                         "not through the NAT (finding A, 2026-11-01)"], size=10.5)
box(590, 1112, 280, 76, [("Bastion", 12, "bold"), "ECS task definition, on demand",
                         "no instance running"], size=10.5)
box(900, 1112, 204, 76, [("NAT instance", 12, "bold"), "shown on the boundary", "at the top of this diagram"],
    pal=BND, size=10.5)
elbow([(1002, 1112), (1002, 1066), (1136, 1066), (1136, 404), (1100, 404)], dashed=True)
arrow(1002, 928, 1002, 1112, "egress", lx=1010, ly=1030, anchor="start")
arrow(286, 928, 300, 1112, "RunTask", lx=306, ly=1066, anchor="start")

# Fargate egress straight out (not via NAT)
elbow([(346, 1206), (346, 1248), (1164, 1248), (1164, 318), (1074, 288)], dashed=True)
p.append('<text x="1158" y="800" font-family="%s" font-size="10" fill="#333" text-anchor="middle" '
         'transform="rotate(-90 1158 800)">Fargate egress — own public IP, not via the NAT</text>' % FONT)

# ---------------------------------------------------------------- supporting services
sx, sw = 96, 196
svc = [("Secrets Manager", "API keys · OAuth tokens", "5-minute TTL cache"),
       ("KMS", "customer-managed key", "annual rotation"),
       ("S3 × 5", "audit evidence · CloudTrail", "Block Public Access on"),
       ("CloudTrail", "multi-region · log-file validation", "CloudWatch Logs 90 days"),
       ("ECR", "container images", "scan on push")]
for i, (a, b, c) in enumerate(svc):
    box(sx + i * (sw + 16), 1316, sw, 72, [(a, 12, "bold"), b, c], pal=SUP, size=10)

text(1164, ACC_Y + 1026, "No security group in the account allows 0.0.0.0/0 · VPC flow logs on",
     size=11, anchor="end", fill="#555")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
       '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
       'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker></defs>'
       + "".join(p) + "</svg>")
(HERE / "di-backend-network-designed.svg").write_text(svg)
try:
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / "di-backend-network-designed-2026-11-01.png"),
                     output_width=W * 2, output_height=H * 2, background_color="white")
    print("wrote svg + png")
except ImportError:
    print("wrote svg (install cairosvg for the png)")
