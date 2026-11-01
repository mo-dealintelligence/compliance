#!/usr/bin/env python3
"""
Deal Intelligence network diagrams — three audiences, one set of facts.

  internal  full engineering / auditor view: every component, third parties and
            data vendors included.
  boundary  security view: what crosses the account boundary and the control at
            each hop. WAF in, NAT out.
  customer  customer-facing: the customer's own systems are the only outside
            party. No data vendors, no other third parties.

Drawn in the house style of the 2025 Data Flow Diagram (dashed trust boundaries,
rounded nodes, labelled flows) with the official AWS architecture icons in
./aws-icons (AWS Architecture Icons, see aws-icons/LICENSE).

The WAF and the NAT are both self-managed rather than the AWS managed services —
a NAT instance instead of a NAT Gateway, and the WAF's job (origin verification,
rate limiting, header and payload rules) in the application instead of AWS WAF.
They are drawn and named as what they are, with "self-managed" on the node.

Facts verified read-only against account 164482277879 on 2026-11-01, from
di-backend-api/docs/infra-edge-review-2026-11-01.md and
di-backend-api/docs/auth-hardening-2026-11-01.md.

    python3 make_network_diagram.py            # all three
    python3 make_network_diagram.py internal   # just one
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ICONS = HERE / "aws-icons"
DATE = "2026-11-01"

EXT = ("#ffe6cc", "#d79b00")
BND = ("#fff2cc", "#d6b656")
INT = ("#dae8fc", "#6c8ebf")
DAT = ("#d5e8d4", "#82b366")
SUP = ("#e1d5e7", "#9673a6")
FONT = "Helvetica, Arial, sans-serif"

_icon_cache: dict[str, str] = {}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    # ---------- primitives ----------
    def esc(self, s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=12, anchor="middle", weight="normal", fill="#1a1a1a"):
        self.p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
                      f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{self.esc(s)}</text>')

    def icon(self, name, x, y, size=34):
        if name not in _icon_cache:
            raw = (ICONS / f"{name}.svg").read_text()
            inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
            inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
            inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
            _icon_cache[name] = inner
        s = size / 64
        self.p.append(f'<g transform="translate({x},{y}) scale({s:.4f})">{_icon_cache[name]}</g>')

    def node(self, x, y, w, h, rows, pal=INT, ic=None, size=11.5, r=8):
        """Rounded node; icon on the left, text block beside it."""
        f, s = pal
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{f}" '
                      f'stroke="{s}" stroke-width="1.6"/>')
        tx, ta = x + w / 2, "middle"
        if ic:
            self.icon(ic, x + 12, y + h / 2 - 17)
            tx, ta = x + 58, "start"
        norm = [(t if isinstance(t, tuple) else (t, size, "normal")) for t in rows]
        total = sum(t[1] + 3.5 for t in norm) - 3.5
        yy = y + h / 2 - total / 2
        for t, sz, wt in norm:
            yy += sz
            self.text(tx, yy, t, size=sz, weight=wt, anchor=ta)
            yy += 3.5

    def cyl(self, x, y, w, h, rows, ic=None):
        f, s = DAT
        ry = 13
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 1 {w},0 v{h-2*ry} a{w/2},{ry} 0 0 1 {-w},0 z" '
                      f'fill="{f}" stroke="{s}" stroke-width="1.6"/>')
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 0 {w},0" fill="none" stroke="{s}" stroke-width="1.6"/>')
        tx, ta = x + w / 2, "middle"
        if ic:
            self.icon(ic, x + 14, y + h / 2 - 12)
            tx, ta = x + 60, "start"
        norm = [(t if isinstance(t, tuple) else (t, 11.5, "normal")) for t in rows]
        total = sum(t[1] + 3.5 for t in norm) - 3.5
        yy = y + h / 2 - total / 2 + 6
        for t, sz, wt in norm:
            yy += sz
            self.text(tx, yy, t, size=sz, weight=wt, anchor=ta)
            yy += 3.5

    def boundary(self, x, y, w, h, label, color="#444", label_at="top"):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="none" '
                      f'stroke="{color}" stroke-width="1.6" stroke-dasharray="8 5"/>')
        ly = y + 22 if label_at == "top" else y + h - 14
        self.text(x + 16, ly, label, size=13, anchor="start", weight="bold", fill=color)

    def arrow(self, x1, y1, x2, y2, label=None, dashed=False, lx=None, ly=None, anchor="middle"):
        d = ' stroke-dasharray="6 4"' if dashed else ""
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1a1a1a" stroke-width="1.7" '
                      f'marker-end="url(#a)"{d}/>')
        if label:
            self.text(lx if lx is not None else (x1 + x2) / 2,
                      ly if ly is not None else (y1 + y2) / 2 - 6, label, size=10.5,
                      fill="#333", anchor=anchor)

    def elbow(self, pts, label=None, dashed=False, lx=None, ly=None, anchor="middle"):
        d = ' stroke-dasharray="6 4"' if dashed else ""
        path = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.7" '
                      f'marker-end="url(#a)"{d}/>')
        if label:
            self.text(lx, ly, label, size=10.5, fill="#333", anchor=anchor)

    def header(self, title, subtitle, note):
        self.text(40, 48, title, size=25, anchor="start", weight="bold")
        self.text(40, 73, "Mo Messidi, Chief Executive Officer, Deal Intelligence", size=12.5,
                  anchor="start", fill="#444")
        self.text(40, 95, subtitle, size=12.5, anchor="start", fill="#444")
        self.text(40, 115, note, size=11.5, anchor="start", fill="#777")

    def save(self, stem):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}"><rect width="{self.w}" height="{self.h}" fill="#fff"/>'
               '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
               'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1a1a1a"/></marker></defs>'
               + "".join(self.p) + "</svg>")
        (HERE / f"{stem}.svg").write_text(svg)
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / f"{stem}-{DATE}.png"),
                             output_width=self.w * 2, output_height=self.h * 2, background_color="white")
        except ImportError:
            print("  (cairosvg missing — svg only)")
        print(f"  {stem}")


WAF_ROWS = [("WAF — self-managed", 12.5, "bold"),
            "origin verification: X-Origin-Verify header checked in",
            "middleware, a direct hit on a function URL gets 403",
            "rate limiting shared across Lambdas via DocumentDB,",
            "keyed by credential then IP · security headers · redaction"]
NAT_ROWS = [("NAT — self-managed instance  t3.micro", 12.5, "bold"),
            "52.70.24.151 · IMDSv2 · SSM · no key pair",
            "no public ingress (10.0.1.0/24, 10.0.2.0/24 only)",
            "the only route out of the private subnets"]


# ------------------------------------------------------------------ internal
def build_internal():
    c = Canvas(1260, 1500)
    c.header("Deal Intelligence — Network Diagram (internal)",
             "Production AWS account 164482277879, us-east-1. Everything inbound crosses CloudFront and the WAF; "
             "everything outbound crosses the NAT.",
             f"Verified read-only against the live account, {DATE}.")

    c.boundary(60, 150, 1140, 150, "Outside the account — customers and third parties")
    ey, eh = 192, 84
    for x, ic, rows in [
        (80, "Users", [("Customers", 12.5, "bold"), "MCP clients · REST API", "Clay · CRM · Slack"]),
        (304, "Client", [("PropelAuth", 12.5, "bold"), "Google SSO · JWT", "API keys"]),
        (528, "Client", [("Customer CRMs", 12.5, "bold"), "HubSpot · Salesforce", "OAuth tokens"]),
        (752, "Client", [("Google Workspace", 12.5, "bold"), "identity · email", "directory sync"]),
        (976, "Internetalt1", [("Data vendors", 12.5, "bold"), "enrichment · search", "egress only"]),
    ]:
        c.node(x, ey, 204, eh, rows, pal=EXT, ic=ic, size=11)

    ACC = 380
    c.p.append(f'<rect x="60" y="{ACC}" width="1140" height="1060" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.6" stroke-dasharray="8 5"/>')
    c.text(76, ACC + 1046, "Deal Intelligence AWS account 164482277879 — us-east-1 (production)",
           size=13, anchor="start", weight="bold", fill="#2b6cb0")
    c.text(1184, ACC + 1046, "No security group allows 0.0.0.0/0 · VPC flow logs on",
           size=11, anchor="end", fill="#555")

    c.node(140, ACC - 44, 420, 88,
           [("CloudFront  E1QUZLMQLDUTYL", 12.5, "bold"),
            "api.dealintelligence.io · mcp.dealintelligence.io",
            "TLS 1.2+ · AWS Shield Standard · the only way in"], pal=BND, ic="AmazonCloudFront", size=11)
    c.node(700, ACC - 44, 440, 88, NAT_ROWS, pal=BND, ic="AmazonVPCNATGateway", size=10.5)

    c.arrow(182, ey + eh, 240, ACC - 44, "HTTPS", lx=150, ly=345, anchor="start")
    c.arrow(760, ACC - 44, 470, ey + eh, "validate JWT / API key", lx=545, ly=316)
    c.arrow(860, ACC - 44, 650, ey + eh, "OAuth · CRM sync", lx=772, ly=330)
    c.arrow(960, ACC - 44, 854, ey + eh, "directory · mail", lx=930, ly=316)
    c.arrow(1070, ACC - 44, 1070, ey + eh, "enrichment", lx=1110, ly=330)

    c.node(140, 452, 420, 110, WAF_ROWS, pal=BND, ic="AWSWAF", size=10.5)
    c.arrow(350, ACC + 44, 350, 452)
    c.node(140, 592, 420, 76,
           [("Lambda function URLs", 12.5, "bold"),
            "app — origin-verified · mcp — bearer",
            "batchOrchestrator · documentdb-proxy — SigV4"], ic="AWSLambda", size=10.5)
    c.arrow(350, 562, 350, 592)

    c.boundary(90, 700, 1080, 620, "VPC di-backend-vpc 10.0.0.0/16", "#2f855a")
    c.boundary(112, 734, 1036, 332, "Private subnets — us-east-1a / 1b / 1f", "#555")
    c.node(136, 770, 476, 86, [("Lambda app — FastAPI", 12.5, "bold"),
                               "PropelAuth bearer · X-Internal-Key header",
                               "tenant from the token · 112 routes authenticated"],
           ic="AWSLambda", size=10.5)
    c.node(636, 770, 490, 86, [("Lambda mcp — MCP server", 12.5, "bold"),
                               "PropelAuth API keys",
                               "own bearer auth on its function URL"], ic="AWSLambda", size=10.5)
    c.node(136, 876, 308, 62, [("batchOrchestrator", 12, "bold"), "launches Fargate jobs"],
           ic="AWSLambda", size=10)
    c.node(464, 876, 300, 62, [("documentdb-proxy", 12, "bold"), "SigV4 only"], ic="AWSLambda", size=10)
    c.node(784, 876, 342, 62, [("Scheduled Lambdas", 12, "bold"),
                               "accessReview · retention · breachDetection"], ic="AWSLambda", size=10)
    c.cyl(392, 962, 470, 90, [("DocumentDB 5.0 — di-backend-production-cluster", 11.5, "bold"),
                              "private · TLS · KMS-encrypted · deletion protection · 35-day backups",
                              "port 27017 only from the Lambda and NAT security groups"],
          ic="AmazonDocumentDB")
    c.arrow(420, 668, 420, 770)
    c.elbow([(520, 648), (890, 648), (890, 770)])
    c.arrow(380, 856, 490, 962)
    c.arrow(840, 856, 760, 962)
    c.arrow(290, 938, 440, 962)
    c.arrow(950, 938, 810, 962)
    c.text(150, 956, "rate-limit counters", size=10, fill="#333", anchor="start")

    c.boundary(112, 1090, 1036, 200, "Public subnet", "#555")
    c.node(136, 1126, 430, 96, [("Fargate batch tasks — di-jobs-production-cluster", 11.5, "bold"),
                                "no ingress rules on the security group",
                                "egress leaves from the task's own public IP,",
                                "not through the NAT (finding A, 2026-11-01)"], ic="AWSFargate", size=10)
    c.node(596, 1126, 272, 76, [("Bastion", 12, "bold"), "ECS task definition, on demand",
                                "no instance running"], ic="AmazonElasticContainerService", size=10)
    c.node(900, 1126, 226, 76, [("NAT instance", 12, "bold"), "drawn on the boundary",
                                "at the top of this diagram"], pal=BND, ic="AmazonEC2Instance", size=10)
    c.elbow([(1013, 1126), (1013, 1080), (1156, 1080), (1156, 404), (1140, 404)], dashed=True)
    c.arrow(1013, 938, 1013, 1126, "egress", lx=1021, ly=1040, anchor="start")
    c.arrow(290, 938, 300, 1126, "RunTask", lx=306, ly=1080, anchor="start")
    c.elbow([(351, 1222), (351, 1266), (1180, 1266), (1180, 318), (1086, 288)], dashed=True)
    c.p.append(f'<text x="1192" y="820" font-family="{FONT}" font-size="10" fill="#333" '
               'text-anchor="middle" transform="rotate(-90 1192 820)">Fargate egress — own public IP</text>')

    sw = 200
    for i, (ic, a, b, d) in enumerate([
        ("AWSSecretsManager", "Secrets Manager", "API keys · OAuth tokens", "5-minute TTL cache"),
        ("AWSKeyManagementService", "KMS", "customer-managed key", "annual rotation"),
        ("AmazonSimpleStorageService", "S3 × 5", "audit evidence · CloudTrail", "Block Public Access on"),
        ("AWSCloudTrail", "CloudTrail", "multi-region · validated", "CloudWatch Logs 90 days"),
        ("AmazonElasticContainerRegistry", "ECR", "container images", "scan on push")]):
        c.node(96 + i * (sw + 14), 1336, sw, 74, [(a, 11.5, "bold"), b, d], pal=SUP, ic=ic, size=9.5)
    c.save("di-backend-network-internal")


# ------------------------------------------------------------------ boundary
def build_boundary():
    c = Canvas(1260, 940)
    c.header("Deal Intelligence — Trust Boundary and Controls",
             "What crosses the production account boundary, and the control applied at each crossing. "
             "In through the WAF, out through the NAT.",
             f"Verified read-only against the live account, {DATE}.")

    c.boundary(60, 150, 1140, 132, "Outside the account")
    c.node(90, 186, 290, 78, [("Customers", 12.5, "bold"), "MCP clients · REST API · Clay",
                              "authenticated on every route"], pal=EXT, ic="Users", size=11)
    c.node(416, 186, 300, 78, [("PropelAuth", 12.5, "bold"), "Google SSO · JWT · API keys",
                               "identity provider (sub-processor)"], pal=EXT, ic="Client", size=11)
    c.node(752, 186, 418, 78, [("Third parties — egress only", 12.5, "bold"),
                               "customer CRMs · Google Workspace · data vendors",
                               "no inbound path into the account"], pal=EXT, ic="Internetalt1", size=11)

    ACC = 372
    c.p.append(f'<rect x="60" y="{ACC}" width="1140" height="502" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.6" stroke-dasharray="8 5"/>')
    c.text(76, ACC + 488, "Deal Intelligence AWS account 164482277879 — us-east-1 (production)",
           size=13, anchor="start", weight="bold", fill="#2b6cb0")

    c.node(120, ACC - 46, 450, 92,
           [("CloudFront + WAF — the only way in", 12.5, "bold"),
            "TLS 1.2+ · AWS Shield Standard (DDoS)",
            "self-managed WAF: origin verification (direct function-URL hits 403),",
            "shared rate limiting per credential then IP, security headers"],
           pal=BND, ic="AWSWAF", size=10.5)
    c.node(700, ACC - 46, 440, 92,
           [("NAT instance — the only way out", 12.5, "bold"),
            "t3.micro 52.70.24.151 · IMDSv2 · SSM · no key pair",
            "no public ingress; accepts 10.0.1.0/24 and 10.0.2.0/24 only",
            "egress NAT for the private subnets"], pal=BND, ic="AmazonVPCNATGateway", size=10.5)

    c.arrow(200, 264, 250, ACC - 46, "HTTPS", lx=170, ly=340, anchor="start")
    c.arrow(830, ACC - 46, 600, 264, "JWT / API key validation", lx=690, ly=318)
    c.arrow(980, ACC - 46, 940, 264, "OAuth · directory · enrichment", lx=1038, ly=316)

    c.node(300, 470, 660, 86, [("Authentication and tenancy", 12.5, "bold"),
                               "PropelAuth bearer for app users · PropelAuth API keys for MCP and /v1/li",
                               "X-Internal-Key header for internal callers — no credential in a URL path",
                               "tenant taken from the token; company writes are allow-listed"],
           ic="AWSLambda", size=10.5)
    c.arrow(345, ACC + 46, 400, 470)

    c.node(120, 596, 480, 84, [("Private subnets — compute", 12.5, "bold"),
                               "Lambda app · mcp · batchOrchestrator · documentdb-proxy",
                               "scheduled jobs · no inbound path except through CloudFront"],
           ic="AWSLambda", size=10.5)
    c.cyl(660, 592, 480, 92, [("DocumentDB — customer and research data", 11.5, "bold"),
                              "private subnets · TLS · KMS-encrypted · deletion protection",
                              "35-day automated backups · 27017 from the Lambda and NAT SGs only"],
          ic="AmazonDocumentDB")
    c.arrow(500, 556, 400, 596)
    c.arrow(760, 556, 860, 592)
    c.arrow(600, 636, 660, 636)
    c.elbow([(600, 696), (1172, 696), (1172, 440), (1140, 418)], label="egress", lx=1166, ly=560, anchor="end")

    c.node(120, 724, 1020, 72, [("Logging and evidence", 12.5, "bold"),
                                "CloudTrail multi-region with log-file validation · VPC flow logs · "
                                "CloudWatch Logs 90 days · S3 with Block Public Access · KMS · "
                                "Secrets Manager (no secrets in Lambda environments)"],
           pal=SUP, ic="AWSCloudTrail", size=10.5)
    c.text(630, 834, "No security group in the account allows 0.0.0.0/0 or ::/0. Private subnets do not map public IPs.",
           size=11.5, fill="#555")
    c.save("di-backend-network-boundary")


# ------------------------------------------------------------------ customer
def build_customer():
    c = Canvas(1260, 920)
    c.header("Deal Intelligence — How Your Data Is Connected",
             "The path your data takes between your systems and the Deal Intelligence platform, and the "
             "controls protecting it.",
             f"Production environment as at {DATE}. AWS account in us-east-1.")

    c.boundary(60, 150, 1140, 140, "Your systems")
    c.node(100, 190, 320, 84, [("Your users", 12.5, "bold"), "MCP client · REST API · Clay",
                               "signed in through your Google account"], pal=EXT, ic="Users", size=11)
    c.node(460, 190, 330, 84, [("Your CRM", 12.5, "bold"), "HubSpot · Salesforce",
                               "connected by you with OAuth"], pal=EXT, ic="Client", size=11)
    c.node(830, 190, 330, 84, [("Your Slack workspace", 12.5, "bold"), "alerts and digests",
                               "delivered to the channels you pick"], pal=EXT, ic="Client", size=11)

    ACC = 378
    c.p.append(f'<rect x="60" y="{ACC}" width="1140" height="472" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.6" stroke-dasharray="8 5"/>')
    c.text(76, ACC + 458, "Deal Intelligence — private AWS environment (us-east-1)",
           size=13, anchor="start", weight="bold", fill="#2b6cb0")

    c.node(130, ACC - 46, 460, 92,
           [("CloudFront + WAF", 12.5, "bold"),
            "TLS 1.2 or better on every connection · DDoS protection",
            "web application firewall: request filtering and rate limiting",
            "the single entry point — nothing else is reachable"],
           pal=BND, ic="AWSWAF", size=10.5)
    c.node(720, ACC - 46, 420, 92,
           [("NAT — outbound only", 12.5, "bold"),
            "one controlled exit for calls back to your CRM and Slack",
            "accepts no inbound connection from the internet"],
           pal=BND, ic="AmazonVPCNATGateway", size=10.5)

    c.arrow(230, 274, 290, ACC - 46, "HTTPS", lx=186, ly=312, anchor="end")
    c.arrow(860, ACC - 46, 640, 274, "your CRM, with your OAuth grant", lx=742, ly=324)
    c.arrow(1000, ACC - 46, 980, 274, "your Slack alerts", lx=1070, ly=338)

    c.node(300, 486, 660, 80, [("Authenticated API", 12.5, "bold"),
                               "every route requires your token or your API key",
                               "your data is scoped to your account — the tenant comes from the token"],
           ic="AWSLambda", size=11)
    c.arrow(360, ACC + 46, 430, 486)

    c.cyl(340, 606, 580, 94, [("Your data — encrypted database", 12, "bold"),
                              "private network only, never reachable from the internet",
                              "encrypted at rest with AWS KMS and in transit with TLS",
                              "35-day automated backups · deletion protection"], ic="AmazonDocumentDB")
    c.arrow(630, 566, 630, 606)

    c.node(100, 720, 480, 70, [("Access and retention", 12, "bold"),
                               "access limited to the CEO, reviewed quarterly",
                               "contact data kept 24 months, then deleted automatically"],
           pal=SUP, ic="AWSSecretsManager", size=10.5)
    c.node(680, 720, 480, 70, [("Monitoring and audit", 12, "bold"),
                               "every API call logged and retained",
                               "SOC 2 Type I report available under NDA"],
           pal=SUP, ic="AWSCloudTrail", size=10.5)
    c.save("di-backend-network-customer")


BUILDERS = {"internal": build_internal, "boundary": build_boundary, "customer": build_customer}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for name in want:
        if name not in BUILDERS:
            sys.exit(f"unknown variant {name!r}; pick from {', '.join(BUILDERS)}")
        BUILDERS[name]()
