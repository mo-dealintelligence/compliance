#!/usr/bin/env python3
"""
Deal Intelligence network flow diagrams — three audiences, one set of facts.

  internal  engineering / auditor: every node, every flow, blocked paths shown.
  boundary  what crosses the account boundary, in which direction, under what control.
  customer  the customer's own systems are the only outside party.

These are network flow diagrams, not illustrations: every edge is directed, carries
protocol and port, is numbered, and is listed in the flow table underneath with its
initiator and the control applied. Nodes carry identifiers, not prose.

The WAF and the NAT are self-managed rather than the AWS managed services (a t3.micro
NAT instance instead of a NAT Gateway; the firewall's job in the application instead of
AWS WAF). They are named for what they do, marked "self-managed".

Facts verified read-only against account 164482277879 on 2026-11-01, from
di-backend-api/docs/infra-edge-review-2026-11-01.md and auth-hardening-2026-11-01.md.

    python3 make_network_diagram.py [internal|boundary|customer ...]
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
BLOCK = "#c0392b"
MGMT = "#7f8c8d"
_icons: dict[str, str] = {}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def esc(self, s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def text(self, x, y, s, size=12, anchor="middle", weight="normal", fill="#1a1a1a", family=FONT):
        self.p.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
                      f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{self.esc(s)}</text>')

    def icon(self, name, x, y, size=30):
        if name not in _icons:
            raw = (ICONS / f"{name}.svg").read_text()
            inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
            inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
            _icons[name] = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
        self.p.append(f'<g transform="translate({x},{y}) scale({size/64:.4f})">{_icons[name]}</g>')

    def node(self, x, y, w, h, title, meta=(), pal=INT, ic=None, r=7):
        """Terse node: bold name, then identifier/placement lines. No prose."""
        f, s = pal
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" fill="{f}" '
                      f'stroke="{s}" stroke-width="1.6"/>')
        tx = x + (52 if ic else w / 2)
        ta = "start" if ic else "middle"
        if ic:
            self.icon(ic, x + 11, y + h / 2 - 15)
        rows = [(title, 12.5, "bold")] + [(m, 10.5, "normal") for m in meta]
        total = sum(r0[1] + 3 for r0 in rows) - 3
        yy = y + h / 2 - total / 2
        for t, sz, wt in rows:
            yy += sz
            self.text(tx, yy, t, size=sz, weight=wt, anchor=ta,
                      fill="#1a1a1a" if wt == "bold" else "#444")
            yy += 3

    def cyl(self, x, y, w, h, title, meta=(), ic=None):
        f, s = DAT
        ry = 12
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 1 {w},0 v{h-2*ry} a{w/2},{ry} 0 0 1 {-w},0 z" '
                      f'fill="{f}" stroke="{s}" stroke-width="1.6"/>')
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 0 {w},0" fill="none" stroke="{s}" stroke-width="1.6"/>')
        tx = x + (54 if ic else w / 2)
        ta = "start" if ic else "middle"
        if ic:
            self.icon(ic, x + 13, y + h / 2 - 10)
        rows = [(title, 12, "bold")] + [(m, 10.5, "normal") for m in meta]
        total = sum(r0[1] + 3 for r0 in rows) - 3
        yy = y + h / 2 - total / 2 + 5
        for t, sz, wt in rows:
            yy += sz
            self.text(tx, yy, t, size=sz, weight=wt, anchor=ta,
                      fill="#1a1a1a" if wt == "bold" else "#444")
            yy += 3

    def boundary(self, x, y, w, h, label, color="#444", at="top"):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="none" '
                      f'stroke="{color}" stroke-width="1.6" stroke-dasharray="8 5"/>')
        self.text(x + 16, y + 22 if at == "top" else y + h - 13, label, size=12.5,
                  anchor="start", weight="bold", fill=color)

    # ---------- flows ----------
    def flow(self, n, pts, label, lx=None, ly=None, anchor="middle", color="#1a1a1a",
             dashed=False, badge=True, both=False):
        d = ' stroke-dasharray="6 4"' if dashed else ""
        mid = f' marker-start="url(#as)"' if both else ""
        path = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.9" '
                      f'marker-end="url(#a)"{mid}{d}/>')
        if badge and n:
            bx, by = pts[len(pts) // 2] if len(pts) % 2 else (
                (pts[len(pts) // 2 - 1][0] + pts[len(pts) // 2][0]) / 2,
                (pts[len(pts) // 2 - 1][1] + pts[len(pts) // 2][1]) / 2)
            self.p.append(f'<circle cx="{bx}" cy="{by}" r="10" fill="#fff" stroke="{color}" stroke-width="1.6"/>')
            self.text(bx, by + 3.8, str(n), size=11, weight="bold", fill=color)
        if label:
            self.text(lx, ly, label, size=10, fill=color if color != "#1a1a1a" else "#222",
                      anchor=anchor, family="Helvetica, Arial, sans-serif")

    def blocked(self, pts, label, lx, ly, anchor="middle"):
        path = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{path}" fill="none" stroke="{BLOCK}" stroke-width="1.7" '
                      'stroke-dasharray="5 4"/>')
        mx, my = pts[-1]
        px, py = pts[-2]
        cx, cy = (mx + px) / 2, (my + py) / 2
        self.p.append(f'<g stroke="{BLOCK}" stroke-width="2.4"><line x1="{cx-7}" y1="{cy-7}" x2="{cx+7}" '
                      f'y2="{cy+7}"/><line x1="{cx+7}" y1="{cy-7}" x2="{cx-7}" y2="{cy+7}"/></g>')
        self.text(lx, ly, label, size=10, fill=BLOCK, anchor=anchor)

    def legend(self, x, y, items):
        self.text(x, y, "Legend", size=11.5, anchor="start", weight="bold", fill="#333")
        yy = y + 16
        for style, lab in items:
            if style == "flow":
                self.p.append(f'<line x1="{x}" y1="{yy-4}" x2="{x+34}" y2="{yy-4}" stroke="#1a1a1a" '
                              'stroke-width="1.9" marker-end="url(#a)"/>')
            elif style == "mgmt":
                self.p.append(f'<line x1="{x}" y1="{yy-4}" x2="{x+34}" y2="{yy-4}" stroke="{MGMT}" '
                              'stroke-width="1.9" stroke-dasharray="6 4" marker-end="url(#a)"/>')
            elif style == "blocked":
                self.p.append(f'<line x1="{x}" y1="{yy-4}" x2="{x+34}" y2="{yy-4}" stroke="{BLOCK}" '
                              'stroke-width="1.7" stroke-dasharray="5 4"/>')
                self.p.append(f'<g stroke="{BLOCK}" stroke-width="2.2"><line x1="{x+13}" y1="{yy-11}" '
                              f'x2="{x+23}" y2="{yy+3}"/><line x1="{x+23}" y1="{yy-11}" x2="{x+13}" y2="{yy+3}"/></g>')
            elif style == "bnd":
                self.p.append(f'<rect x="{x}" y="{yy-11}" width="34" height="14" fill="none" stroke="#444" '
                              'stroke-width="1.5" stroke-dasharray="6 4"/>')
            self.text(x + 44, yy, lab, size=10.5, anchor="start", fill="#333")
            yy += 19

    def flow_table(self, x, y, w, rows, title="Network flows"):
        self.text(x, y, title, size=13, anchor="start", weight="bold")
        cols = [52, 300, 150, 110, 999]
        heads = ["#", "Source → destination (arrow shows who initiates)", "Protocol / port",
                 "Direction", "Control enforced"]
        yy = y + 24
        cx = x
        for i, hd in enumerate(heads):
            self.text(cx + 4, yy, hd, size=10.5, anchor="start", weight="bold", fill="#333")
            cx += cols[i]
        yy += 6
        self.p.append(f'<line x1="{x}" y1="{yy}" x2="{x+w}" y2="{yy}" stroke="#bbb" stroke-width="1"/>')
        for r in rows:
            yy += 20
            cx = x
            colr = BLOCK if r[0] == "DENY" else ("#555" if r[0] == "LOG" else "#222")
            for i, cell in enumerate(r):
                self.text(cx + 4, yy, cell, size=10.2, anchor="start",
                          fill=colr if i == 0 else "#333",
                          weight="bold" if i == 0 else "normal")
                cx += cols[i]
            self.p.append(f'<line x1="{x}" y1="{yy+6}" x2="{x+w}" y2="{yy+6}" stroke="#eee" stroke-width="1"/>')
        return yy + 6

    def header(self, title, subtitle, note):
        self.text(40, 46, title, size=24, anchor="start", weight="bold")
        self.text(40, 70, "Mo Messidi, Chief Executive Officer, Deal Intelligence", size=12,
                  anchor="start", fill="#444")
        self.text(40, 91, subtitle, size=12, anchor="start", fill="#444")
        self.text(40, 110, note, size=11, anchor="start", fill="#777")

    def save(self, stem):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}"><rect width="{self.w}" height="{self.h}" fill="#fff"/>'
               '<defs>'
               '<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
               'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>'
               '<marker id="as" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" '
               'orient="auto-start-reverse"><path d="M10,0 L0,5 L10,10 z" fill="context-stroke"/></marker>'
               '</defs>' + "".join(self.p) + "</svg>")
        (HERE / f"{stem}.svg").write_text(svg)
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / f"{stem}-{DATE}.png"),
                             output_width=self.w * 2, output_height=self.h * 2, background_color="white")
        except ImportError:
            print("  (cairosvg missing — svg only)")
        print(f"  {stem}")


# ===================================================================== internal
def build_internal():
    c = Canvas(1460, 2200)
    c.header("Deal Intelligence — Network Flow Diagram (internal)",
             "Production AWS account 164482277879, us-east-1. Arrows point from the party that opens the "
             "connection to the party that accepts it.",
             f"Verified read-only against the live account, {DATE}. Flows are numbered to the table below.")

    # ---- outside
    c.boundary(50, 146, 1360, 132, "Internet — outside the account")
    ey, eh = 182, 76
    c.node(70, ey, 236, eh, "Customers", ["MCP clients · REST · Clay", "unauthenticated internet"], EXT, "Users")
    c.node(330, ey, 236, eh, "PropelAuth", ["identity provider", "auth.dealintelligence.co"], EXT, "Client")
    c.node(590, ey, 236, eh, "Customer CRMs", ["HubSpot · Salesforce", "customer tenants"], EXT, "Client")
    c.node(850, ey, 236, eh, "Google Workspace", ["identity · mail"], EXT, "Client")
    c.node(1110, ey, 280, eh, "Data vendors", ["enrichment · search APIs"], EXT, "Internetalt1")

    # ---- account boundary, with the two chokepoints straddling it
    ACC = 372
    c.p.append(f'<rect x="50" y="{ACC}" width="1360" height="1140" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.7" stroke-dasharray="8 5"/>')
    c.text(66, ACC + 1126, "AWS account 164482277879 — us-east-1 (production)", size=12.5,
           anchor="start", weight="bold", fill="#2b6cb0")

    c.node(110, ACC - 38, 330, 76, "CloudFront + WAF (self-managed)",
           ["E1QUZLMQLDUTYL · TLS 1.2+ · Shield Std", "api· / mcp·dealintelligence.io"], BND, "AWSWAF")
    c.node(1000, ACC - 38, 330, 76, "NAT (self-managed instance)",
           ["t3.micro · 52.70.24.151 · public subnet", "egress only — accepts no internet ingress"],
           BND, "AmazonVPCNATGateway")

    # ---- inside: function URLs
    c.node(110, 470, 330, 72, "Lambda function URLs",
           ["app — origin-verified · mcp — bearer", "orchestrator · proxy — SigV4"], INT, "AWSLambda")

    # ---- VPC
    c.boundary(80, 580, 1300, 880, "VPC di-backend-vpc 10.0.0.0/16", "#2f855a")
    c.boundary(104, 614, 1252, 470, "Private subnets — us-east-1a / 1b / 1f (no public IPs)", "#555")
    c.node(128, 650, 400, 76, "Lambda app (FastAPI)",
           ["112 routes · PropelAuth bearer", "X-Internal-Key · tenant from token"], INT, "AWSLambda")
    c.node(560, 650, 360, 76, "Lambda mcp", ["MCP server · PropelAuth API keys"], INT, "AWSLambda")
    c.node(952, 650, 380, 76, "Scheduled Lambdas",
           ["accessReview · retention", "breachDetection · workspace"], INT, "AWSLambda")
    c.node(128, 758, 400, 68, "Lambda batchOrchestrator", ["launches Fargate jobs"], INT, "AWSLambda")
    c.node(560, 758, 360, 68, "Lambda documentdb-proxy", ["SigV4 only"], INT, "AWSLambda")
    c.cyl(430, 880, 520, 86, "DocumentDB 5.0 — di-backend-production-cluster",
          ["private subnets · TLS · KMS · deletion protection · 35-day backups",
           "security group: 27017 from the Lambda and NAT SGs only"], "AmazonDocumentDB")

    c.boundary(104, 1104, 1252, 330, "Public subnet", "#555")
    c.node(128, 1140, 400, 84, "Fargate batch tasks",
           ["di-jobs-production-cluster", "own public IP · SG has no ingress rules"], INT, "AWSFargate")
    c.node(560, 1140, 300, 76, "Bastion", ["ECS task definition", "no instance running"],
           INT, "AmazonElasticContainerService")
    c.node(900, 1140, 300, 76, "NAT instance", ["drawn on the boundary above"], BND, "AmazonEC2Instance")
    c.p.append('<path d="M1050,1140 L1050,1098 L1362,1098 L1362,406 L1330,406" fill="none" '
               f'stroke="{MGMT}" stroke-width="1.5" stroke-dasharray="4 4"/>')

    sw = 246
    for i, (ic, t, m) in enumerate([
            ("AWSSecretsManager", "Secrets Manager", "API keys · OAuth tokens"),
            ("AWSKeyManagementService", "KMS", "customer-managed key"),
            ("AmazonSimpleStorageService", "S3 × 5", "Block Public Access on"),
            ("AWSCloudTrail", "CloudTrail", "multi-region · validated"),
            ("AmazonElasticContainerRegistry", "ECR", "scan on push")]):
        c.node(128 + i * (sw + 10), 1270, sw, 60, t, [m], SUP, ic)
    c.text(128, 1356, "AWS service endpoints reached over HTTPS 443 through the NAT — there are no VPC endpoints.",
           size=10.5, anchor="start", fill="#555")

    # ---- flows
    c.flow(1, [(165, ey + eh), (200, ACC - 38)], "HTTPS 443", lx=120, ly=330, anchor="start")
    c.flow(2, [(275, ACC + 38), (275, 470)], "HTTPS 443 + X-Origin-Verify", lx=292, ly=440, anchor="start")
    c.flow(3, [(275, 542), (275, 650)], "invoke", lx=292, ly=600, anchor="start")
    c.flow(4, [(440, 506), (660, 506), (660, 650)], "invoke", lx=676, ly=600, anchor="start")
    c.flow(5, [(528, 700), (544, 700), (544, 880)], "TCP 27017 TLS", lx=552, ly=836, anchor="start")
    c.flow(6, [(700, 726), (760, 880)], "TCP 27017 TLS", lx=770, ly=800, anchor="start")
    c.flow(7, [(1100, 726), (900, 880)], "TCP 27017 TLS", lx=1010, ly=790, anchor="start")
    c.flow(8, [(300, 826), (440, 884)], "TCP 27017 TLS", lx=150, ly=874, anchor="start")
    c.flow(9, [(330, 826), (330, 1140)], "ECS RunTask (HTTPS 443 via NAT)", lx=344, ly=1038, anchor="start")
    c.flow(10, [(1240, 726), (1240, 1000), (1300, 1000)], "HTTPS 443 via NAT →", lx=1150, ly=1022, anchor="start")
    c.flow(11, [(1300, 1000), (1336, 1000), (1336, 452), (1200, 420)], "", badge=False)
    c.flow(12, [(1120, ACC - 38), (960, ey + eh)], "HTTPS 443 — JWT / API-key validation", lx=905, ly=330, anchor="start")
    c.flow(13, [(1180, ACC - 38), (1180, ey + eh)], "HTTPS 443 — OAuth, mail, enrichment",
           lx=1196, ly=330, anchor="start")
    c.flow(14, [(528, 1182), (1396, 1182), (1396, 300), (1300, 262)], "HTTPS 443 — own public IP,", lx=1388, ly=1210, anchor="end")
    c.text(1388, 1224, "not via the NAT", size=10, fill="#222", anchor="end")
    c.flow(15, [(300, 1140), (300, 1096), (28, 1096), (28, 420), (110, 396)],
           "", badge=True)
    c.text(36, 316, "15 — Fargate jobs call the public API: HTTPS 443 + X-Internal-Key", size=10, fill="#222", anchor="start")

    # blocked
    c.blocked([(700, 300), (560, 440), (420, 470)], "direct hit on a function URL → 403 (origin verification)",
              lx=600, ly=430, anchor="start")
    c.blocked([(936, 300), (936, 600), (936, 872)], "no route from the internet to DocumentDB",
              lx=948, ly=548, anchor="start")

    c.legend(60, 1552, [("flow", "network flow — arrow points to the party accepting the connection"),
                        ("blocked", "path that is denied, and what denies it"),
                        ("mgmt", "same host / management relationship, not a network flow"),
                        ("bnd", "trust boundary")])

    rows = [
        ("1", "Customer client → CloudFront", "HTTPS 443 (TLS 1.2+)", "inbound", "Shield Standard; WAF rate limit per credential then IP"),
        ("2", "CloudFront → Lambda function URL", "HTTPS 443", "inbound", "X-Origin-Verify header; direct hits rejected 403"),
        ("3", "Function URL → Lambda app", "AWS invoke", "internal", "PropelAuth bearer or X-Internal-Key on every route"),
        ("4", "Function URL → Lambda mcp", "AWS invoke", "internal", "PropelAuth API key; bearer on the function URL"),
        ("5", "Lambda app → DocumentDB", "TCP 27017 (TLS)", "internal", "SG: 27017 from the Lambda SG only; KMS at rest"),
        ("6", "Lambda documentdb-proxy → DocumentDB", "TCP 27017 (TLS)", "internal", "SigV4 on the function URL; same SG rule"),
        ("7", "Scheduled Lambdas → DocumentDB", "TCP 27017 (TLS)", "internal", "same SG rule; EventBridge schedules only"),
        ("8", "batchOrchestrator → DocumentDB", "TCP 27017 (TLS)", "internal", "same SG rule; also holds the shared WAF rate-limit counters"),
        ("9", "batchOrchestrator → ECS RunTask", "HTTPS 443 via NAT", "outbound", "task role scoped to the jobs cluster"),
        ("10", "Lambdas → Secrets Manager / AWS APIs", "HTTPS 443 via NAT", "outbound", "no VPC endpoints; IAM-scoped; 5-minute cache"),
        ("12", "Lambdas → NAT → PropelAuth", "HTTPS 443", "outbound", "egress through the NAT; no inbound path"),
        ("13", "Lambdas → NAT → CRM / Workspace / vendors", "HTTPS 443", "outbound", "OAuth tokens held in Secrets Manager"),
        ("14", "Fargate task → data vendors", "HTTPS 443", "outbound", "leaves on the task's own public IP, not the NAT (finding A)"),
        ("15", "Fargate task → CloudFront → API", "HTTPS 443", "out and back in", "X-Internal-Key header; same WAF path as a customer"),
        ("DENY", "Internet → Lambda function URL (direct)", "HTTPS 443", "inbound", "denied — origin verification returns 403"),
        ("DENY", "Internet → DocumentDB", "TCP 27017", "inbound", "denied — private subnets, no public IP, SG denies"),
        ("DENY", "Internet → NAT instance", "any", "inbound", "denied — SG accepts 10.0.1.0/24 and 10.0.2.0/24 only"),
        ("DENY", "Internet → Fargate task", "any", "inbound", "denied — security group has no ingress rules"),
        ("LOG", "CloudTrail → S3; VPC flow logs and Lambda logs → CloudWatch", "AWS internal", "logging", "multi-region, log-file validation, 90-day retention"),
    ]
    c.flow_table(60, 1672, 1340, rows)
    c.save("di-backend-network-internal")


# ===================================================================== boundary
def build_boundary():
    c = Canvas(1460, 1400)
    c.header("Deal Intelligence — Account Boundary Crossings",
             "Every flow that crosses the production account boundary, its direction, and the control that "
             "governs it. Three crossing points: in through CloudFront, out through the NAT, and the Fargate "
             "tasks' own egress.",
             f"Verified read-only against the live account, {DATE}.")

    c.boundary(50, 150, 1360, 124, "Internet — outside the account")
    c.node(80, 182, 380, 72, "Customers", ["MCP clients · REST · Clay"], EXT, "Users")
    c.node(500, 182, 380, 72, "PropelAuth", ["identity provider · sub-processor"], EXT, "Client")
    c.node(920, 182, 460, 72, "Third parties", ["customer CRMs · Google Workspace · data vendors"],
           EXT, "Internetalt1")

    ACC = 384
    c.p.append(f'<rect x="50" y="{ACC}" width="1360" height="452" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.7" stroke-dasharray="8 5"/>')
    c.text(66, ACC + 438, "AWS account 164482277879 — us-east-1 (production)", size=12.5,
           anchor="start", weight="bold", fill="#2b6cb0")

    c.node(90, ACC - 38, 340, 76, "CloudFront + WAF (self-managed)",
           ["ingress chokepoint · TLS 1.2+ · Shield Std"], BND, "AWSWAF")
    c.node(560, ACC - 38, 320, 76, "NAT (self-managed instance)",
           ["egress chokepoint · t3.micro"], BND, "AmazonVPCNATGateway")
    c.node(1010, ACC - 38, 370, 76, "Fargate task public IP",
           ["second egress path — not the NAT"], BND, "AWSFargate")

    c.boundary(80, 500, 1300, 288, "VPC di-backend-vpc 10.0.0.0/16", "#2f855a")
    c.node(110, 548, 420, 84, "Private subnets — compute",
           ["Lambda app · mcp · orchestrator · proxy", "scheduled jobs · no public IPs"], INT, "AWSLambda")
    c.cyl(600, 544, 460, 92, "DocumentDB",
          ["private subnets · TLS · KMS · 35-day backups",
           "27017 from the Lambda and NAT SGs only"], "AmazonDocumentDB")
    c.node(110, 672, 420, 80, "Public subnet — Fargate tasks",
          ["di-jobs-production-cluster", "SG has no ingress rules"], INT, "AWSFargate")
    c.node(1120, 548, 240, 80, "Account services",
           ["Secrets Manager · KMS", "S3 · CloudTrail · ECR"], SUP, "AWSSecretsManager")

    c.flow(1, [(200, 254), (200, ACC - 38)], "HTTPS 443 inbound", lx=212, ly=330, anchor="start")
    c.flow(2, [(260, ACC + 38), (260, 548)], "HTTPS 443 + X-Origin-Verify", lx=272, ly=476, anchor="start")
    c.flow(3, [(530, 586), (600, 586)], "27017 TLS", lx=512, ly=612, anchor="middle")
    c.flow(4, [(640, 548), (640, ACC + 38)], "HTTPS 443 outbound via NAT", lx=652, ly=470, anchor="start")
    c.flow(5, [(680, ACC - 38), (680, 254)], "HTTPS 443 — JWT / API-key validation, OAuth, mail, enrichment",
           lx=694, ly=330, anchor="start")
    c.flow(6, [(530, 712), (1195, 712), (1195, ACC + 38)], "HTTPS 443 outbound on the task's own public IP",
           lx=1185, ly=700, anchor="end")
    c.flow(7, [(1195, ACC - 38), (1195, 254)], "", badge=False)
    c.flow(8, [(1120, 588), (1060, 588)], "HTTPS 443 via NAT", lx=1180, ly=640, anchor="middle")

    c.blocked([(430, 300), (430, 420), (430, 540)], "direct hit on a function URL → 403", lx=440, ly=350,
              anchor="start")
    c.blocked([(940, 300), (940, 440), (940, 536)], "no inbound route to DocumentDB", lx=950, ly=350,
              anchor="start")

    c.legend(60, 890, [("flow", "network flow — arrow points to the party accepting the connection"),
                       ("blocked", "path that is denied, and what denies it"),
                       ("bnd", "trust boundary")])

    rows = [
        ("1", "Internet (customer) → CloudFront", "HTTPS 443 (TLS 1.2+)", "inbound", "Shield Standard; self-managed WAF: origin check, rate limit, headers"),
        ("2", "CloudFront → Lambda function URL", "HTTPS 443", "inbound", "X-Origin-Verify header; every route authenticated"),
        ("3", "Compute → DocumentDB", "TCP 27017 (TLS)", "internal", "SG 27017 from the Lambda SG only; KMS at rest"),
        ("4", "Compute → NAT", "HTTPS 443", "internal", "NAT SG accepts 10.0.1.0/24 and 10.0.2.0/24 only"),
        ("5", "NAT → PropelAuth / CRM / Workspace / vendors", "HTTPS 443", "outbound", "egress only; credentials from Secrets Manager"),
        ("6", "Fargate task → internet", "HTTPS 443", "outbound", "task's own public IP, bypasses the NAT (finding A, open)"),
        ("8", "Compute → AWS service endpoints", "HTTPS 443 via NAT", "outbound", "no VPC endpoints; IAM-scoped"),
        ("DENY", "Internet → Lambda function URL (direct)", "HTTPS 443", "inbound", "origin verification returns 403"),
        ("DENY", "Internet → DocumentDB", "TCP 27017", "inbound", "private subnets, no public IP, SG denies"),
        ("DENY", "Internet → NAT instance", "any", "inbound", "SG accepts 10.0.1.0/24 and 10.0.2.0/24 only"),
        ("DENY", "Internet → Fargate task", "any", "inbound", "security group has no ingress rules"),
        ("LOG", "CloudTrail → S3; flow logs and Lambda logs → CloudWatch", "AWS internal", "stays in account", "multi-region, log-file validation, 90-day retention"),
    ]
    c.flow_table(60, 1000, 1340, rows, "Boundary crossings")
    c.save("di-backend-network-boundary")


# ===================================================================== customer
def build_customer():
    c = Canvas(1400, 1100)
    c.header("Deal Intelligence — How Your Data Is Connected",
             "The network path between your systems and the Deal Intelligence platform. Arrows point from "
             "the party that opens the connection to the party that accepts it.",
             f"Production environment as at {DATE}. Single AWS account in us-east-1.")

    c.boundary(50, 150, 1300, 124, "Your systems and your identity provider")
    c.node(80, 182, 300, 72, "Your users", ["MCP client · REST API · Clay"], EXT, "Users")
    c.node(410, 182, 300, 72, "Your CRM", ["HubSpot · Salesforce"], EXT, "Client")
    c.node(740, 182, 280, 72, "Your Slack", ["alerts and digests"], EXT, "Client")
    c.node(1050, 182, 270, 72, "PropelAuth", ["sign-in · sub-processor"], EXT, "Client")

    ACC = 384
    c.p.append(f'<rect x="50" y="{ACC}" width="1300" height="290" rx="4" ry="4" fill="none" '
               'stroke="#2b6cb0" stroke-width="1.7" stroke-dasharray="8 5"/>')
    c.text(66, ACC + 276, "Deal Intelligence — private AWS environment (us-east-1)", size=12.5,
           anchor="start", weight="bold", fill="#2b6cb0")

    c.node(90, ACC - 38, 360, 76, "CloudFront + WAF",
           ["the only way in · TLS 1.2+ · DDoS protection"], BND, "AWSWAF")
    c.node(900, ACC - 38, 380, 76, "NAT — outbound only",
           ["accepts no inbound connection"], BND, "AmazonVPCNATGateway")

    c.node(230, 520, 460, 84, "Authenticated API",
           ["every route requires your token or API key", "your tenant is taken from the token"],
           INT, "AWSLambda")
    c.cyl(760, 516, 500, 92, "Your data",
          ["private network only · encrypted with AWS KMS",
           "TLS in transit · 35-day backups · deletion protection"], "AmazonDocumentDB")

    c.flow(1, [(170, 254), (170, ACC - 38)], "HTTPS 443", lx=182, ly=330, anchor="start")
    c.flow(2, [(270, ACC + 38), (270, 520)], "HTTPS 443, origin-verified", lx=282, ly=490, anchor="start")
    c.flow(3, [(690, 560), (760, 560)], "TCP 27017, TLS", lx=726, ly=620, anchor="middle")
    c.flow(4, [(620, 520), (1010, 470), (1010, ACC + 38)], "HTTPS 443 outbound", lx=1024, ly=498, anchor="start")
    c.flow(5, [(1020, ACC - 38), (620, 254)], "HTTPS 443 — your CRM, with the OAuth grant you gave us",
           lx=640, ly=324, anchor="start")
    c.flow(6, [(1120, ACC - 38), (900, 254)], "", badge=False)
    c.flow(7, [(1200, ACC - 38), (1180, 254)], "HTTPS 443 — sign-in", lx=1216, ly=324, anchor="start")

    c.blocked([(470, 300), (470, 400), (470, 508)], "the API cannot be reached except through CloudFront",
              lx=482, ly=352, anchor="start")
    c.blocked([(820, 300), (820, 400), (820, 504)], "your data is not reachable from the internet",
              lx=832, ly=352, anchor="start")

    c.legend(60, 742, [("flow", "network flow — arrow points to the party accepting the connection"),
                       ("blocked", "path that is denied, and what denies it"),
                       ("bnd", "trust boundary")])

    rows = [
        ("1", "Your users → CloudFront", "HTTPS 443 (TLS 1.2+)", "inbound", "DDoS protection; web application firewall; rate limiting"),
        ("2", "CloudFront → Deal Intelligence API", "HTTPS 443", "inbound", "origin verification; no other route reaches the API"),
        ("3", "API → your data", "TCP 27017 (TLS)", "internal", "private network only; encrypted at rest with AWS KMS"),
        ("4", "API → NAT", "HTTPS 443", "internal", "single controlled exit for outbound calls"),
        ("5", "NAT → your CRM", "HTTPS 443", "outbound", "uses the OAuth grant you issued; token held in AWS Secrets Manager"),
        ("6", "NAT → your Slack", "HTTPS 443", "outbound", "posts only to the channels you configure"),
        ("7", "NAT → PropelAuth", "HTTPS 443", "outbound", "sign-in and token validation"),
        ("DENY", "Internet → the API directly", "HTTPS 443", "inbound", "rejected; CloudFront is the only entry point"),
        ("DENY", "Internet → your data", "TCP 27017", "inbound", "no public address and no route; firewall denies"),
        ("LOG", "All API calls logged and retained", "—", "internal", "90-day log retention; SOC 2 Type I report available under NDA"),
    ]
    c.flow_table(60, 852, 1280, rows, "Data flows")
    c.save("di-backend-network-customer")


BUILDERS = {"internal": build_internal, "boundary": build_boundary, "customer": build_customer}

if __name__ == "__main__":
    want = sys.argv[1:] or list(BUILDERS)
    for name in want:
        if name not in BUILDERS:
            sys.exit(f"unknown variant {name!r}; pick from {', '.join(BUILDERS)}")
        BUILDERS[name]()
