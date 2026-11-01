#!/usr/bin/env python3
"""
Deal Intelligence network flow diagrams.

  internal  the production network as built: every system and every connection.
  customer  the same network with the customer's systems as the only outside party.

Nodes are systems; arrows are connections, pointing from the side that opens the
connection, labelled with protocol and port. Nothing else. Official AWS icons from
./aws-icons. The WAF and NAT are self-managed (application WAF, NAT instance).

    python3 make_network_diagram.py [internal|customer]
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
_icons = {}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def text(self, x, y, s, size=12, anchor="middle", weight="normal", fill="#1a1a1a"):
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.p.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
                      f'text-anchor="{anchor}" fill="{fill}">{s}</text>')

    def icon(self, name, x, y, size=30):
        if name not in _icons:
            raw = (ICONS / f"{name}.svg").read_text()
            inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
            inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
            _icons[name] = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
        self.p.append(f'<g transform="translate({x},{y}) scale({size/64:.4f})">{_icons[name]}</g>')

    def node(self, x, y, w, h, title, sub=None, pal=INT, ic=None):
        f, s = pal
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" ry="7" fill="{f}" '
                      f'stroke="{s}" stroke-width="1.6"/>')
        tx, ta = (x + 50, "start") if ic else (x + w / 2, "middle")
        if ic:
            self.icon(ic, x + 11, y + h / 2 - 15)
        if sub:
            self.text(tx, y + h / 2 - 2, title, 12.5, ta, "bold")
            self.text(tx, y + h / 2 + 14, sub, 10.5, ta, fill="#444")
        else:
            self.text(tx, y + h / 2 + 4.5, title, 12.5, ta, "bold")

    def cyl(self, x, y, w, h, title, sub=None, ic=None):
        f, s = DAT
        ry = 12
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 1 {w},0 v{h-2*ry} a{w/2},{ry} 0 0 1 {-w},0 z" '
                      f'fill="{f}" stroke="{s}" stroke-width="1.6"/>')
        self.p.append(f'<path d="M{x},{y+ry} a{w/2},{ry} 0 0 0 {w},0" fill="none" stroke="{s}" stroke-width="1.6"/>')
        tx, ta = (x + 52, "start") if ic else (x + w / 2, "middle")
        if ic:
            self.icon(ic, x + 13, y + h / 2 - 10)
        self.text(tx, y + h / 2 + 3, title, 12.5, ta, "bold")
        if sub:
            self.text(tx, y + h / 2 + 19, sub, 10.5, ta, fill="#444")

    def boundary(self, x, y, w, h, label, color="#444", at="top"):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" ry="4" fill="none" '
                      f'stroke="{color}" stroke-width="2.6" stroke-dasharray="12 6"/>')
        self.text(x + 16, y + 22 if at == "top" else y + h - 13, label, 12.5, "start", "bold", color)

    def arrow(self, pts, label=None, lx=None, ly=None, anchor="middle"):
        path = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#a)"/>')
        if label:
            self.text(lx, ly, label, 10.5, anchor, fill="#222")

    def header(self, title, sub):
        self.text(40, 46, title, 24, "start", "bold")
        self.text(40, 70, "Mo Messidi, Chief Executive Officer, Deal Intelligence", 12, "start", fill="#444")
        self.text(40, 91, sub, 12, "start", fill="#444")

    def save(self, stem):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#fff"/><defs><marker id="a" viewBox="0 0 10 10" refX="9" '
               'refY="5" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
               'fill="#1a1a1a"/></marker></defs>' + "".join(self.p) + "</svg>")
        (HERE / f"{stem}.svg").write_text(svg)
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / f"{stem}-{DATE}.png"),
                         output_width=self.w * 2, output_height=self.h * 2, background_color="white")
        print(f"  {stem}")


def legend(c, x, y):
    c.p.append(f'<line x1="{x}" y1="{y-4}" x2="{x+30}" y2="{y-4}" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#a)"/>')
    c.text(x + 38, y, "network connection — from the side that opens it, with protocol and port", 10.5, "start", fill="#333")
    c.p.append(f'<line x1="{x}" y1="{y+14}" x2="{x+30}" y2="{y+14}" stroke="#1a1a1a" stroke-width="1.1" '
               'stroke-dasharray="5 4" marker-end="url(#a)"/>')
    c.text(x + 38, y + 18, "administrative access", 10.5, "start", fill="#333")


def dashed(c, pts, label=None, lx=None, ly=None, anchor="middle"):
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    c.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.1" stroke-dasharray="5 4" marker-end="url(#a)"/>')
    if label:
        c.text(lx, ly, label, 10.5, anchor, fill="#222")


def build_internal():
    c = Canvas(1540, 1200)
    c.header("Deal Intelligence — Network Flow Diagram",
             f"Production · AWS account 164482277879 · us-east-1 · v2.0 · {DATE} · owner: CEO")

    c.boundary(50, 124, 1440, 118, "Internet")
    ey, eh, ew, gap = 158, 64, 226, 12
    xs = [72 + i * (ew + gap) for i in range(6)]
    c.node(xs[0], ey, ew, eh, "Web app", "browser · Netlify-hosted", EXT, "Client")
    c.node(xs[1], ey, ew, eh, "REST API clients", "Clay · integrations", EXT, "Client")
    c.node(xs[2], ey, ew, eh, "MCP clients", None, EXT, "Users")
    c.node(xs[3], ey, ew, eh, "Customer CRMs", "HubSpot · Salesforce", EXT, "Client")
    c.node(xs[4], ey, ew, eh, "Slack", None, EXT, "Client")
    c.node(xs[5], ey, ew, eh, "Operator", "console · CLI · SSM", EXT, "Users")

    A = 336
    c.p.append(f'<rect x="50" y="{A}" width="1440" height="770" rx="4" ry="4" fill="none" stroke="#2b6cb0" '
               'stroke-width="2.6" stroke-dasharray="12 6"/>')
    c.text(66, A + 756, "AWS account 164482277879 — us-east-1", 12.5, "start", "bold", "#2b6cb0")

    c.node(100, A - 34, 560, 68, "CloudFront + WAF", "api.dealintelligence.io · mcp.dealintelligence.io · self-managed WAF", BND, "AWSWAF")
    c.node(1100, A - 34, 330, 68, "NAT", "self-managed instance · t3.micro · 10.0.100.0/24", BND, "AmazonVPCNATGateway")

    c.boundary(80, 416, 1380, 650, "VPC 10.0.0.0/16", "#2f855a")
    c.boundary(104, 446, 760, 520, "Private subnets — 10.0.1.0/24 (us-east-1a) · 10.0.2.0/24 (us-east-1b)", "#555")
    c.node(128, 486, 310, 64, "Lambda app", "FastAPI", INT, "AWSLambda")
    c.node(508, 486, 330, 64, "Lambda mcp", "MCP server", INT, "AWSLambda")
    c.node(128, 586, 310, 64, "Lambda orchestrator", None, INT, "AWSLambda")
    c.cyl(230, 786, 500, 80, "DocumentDB", "di-backend-production-cluster", "AmazonDocumentDB")

    c.boundary(890, 446, 546, 520, "Public subnet — 10.0.100.0/24 (us-east-1a)", "#555")
    c.node(916, 486, 494, 64, "Fargate tasks", "di-jobs-production-cluster", INT, "AWSFargate")
    c.node(916, 700, 494, 64, "Bastion", "ECS task · started on demand", INT, "AmazonElasticContainerService")

    sw = 258
    for i, (ic, t) in enumerate([("AWSSecretsManager", "Secrets Manager"), ("AWSKeyManagementService", "KMS"),
                                 ("AmazonSimpleStorageService", "S3"), ("AWSCloudTrail", "CloudTrail"),
                                 ("AmazonElasticContainerRegistry", "ECR")]):
        c.node(104 + i * (sw + 16), 992, sw, 54, t, None, SUP, ic)

    # ingress
    c.arrow([(185, ey + eh), (185, A - 34)], "HTTPS 443", 193, 274, "start")
    c.arrow([(423, ey + eh), (423, A - 34)], "HTTPS 443", 431, 274, "start")
    c.arrow([(640, ey + eh), (640, A - 34)], "HTTPS 443", 648, 274, "start")
    c.arrow([(250, A + 34), (250, 486)], "HTTPS 443", 262, 440, "start")
    c.arrow([(640, A + 34), (640, 486)], "HTTPS 443", 652, 440, "start")
    # database
    c.arrow([(438, 518), (462, 518), (462, 786)], "TCP 27017", 455, 700, "end")
    c.arrow([(508, 530), (484, 530), (484, 786)], "TCP 27017", 492, 700, "start")
    c.arrow([(283, 650), (283, 786)], "TCP 27017", 295, 740, "start")
    # orchestrator -> Fargate
    c.arrow([(360, 650), (360, 672), (1163, 672), (1163, 550)], "ECS RunTask", 1000, 664, "start")
    # Lambda app + mcp out through the NAT (shared trunk)
    c.arrow([(420, 550), (420, 568), (1430, 568), (1430, A + 34)], "HTTPS 443", 1300, 560, "start")
    c.p.append('<path d="M760,550 L760,568" fill="none" stroke="#1a1a1a" stroke-width="1.1"/>')
    c.arrow([(1100, A - 16), (950, A - 16), (950, ey + eh)], "HTTPS 443", 958, 274, "start")
    c.arrow([(1137, A - 34), (1137, ey + eh)], "HTTPS 443", 1145, 274, "start")
    # Fargate: API calls back in through CloudFront
    c.arrow([(916, 506), (876, 506), (876, 400), (620, 400), (620, A + 34)], "HTTPS 443", 700, 394, "start")
    # administrative access
    dashed(c, [(xs[5] + 113, ey + eh), (xs[5] + 113, 282), (1478, 282), (1478, 732), (1410, 732)], "SSM · HTTPS 443", 1470, 690, "end")
    dashed(c, [(916, 748), (560, 748), (560, 786)], "TCP 27017", 800, 742, "middle")

    legend(c, 70, 1140)
    c.save("di-backend-network-internal")


def build_customer():
    c = Canvas(1200, 820)
    c.header("Deal Intelligence — Network Flow Diagram",
             f"Customer connections · v2.0 · {DATE}")

    c.boundary(50, 124, 1100, 118, "Customer systems")
    ey, eh = 158, 64
    c.node(76, ey, 200, eh, "Web app", "browser", EXT, "Client")
    c.node(300, ey, 200, eh, "REST API clients", "Clay · integrations", EXT, "Client")
    c.node(524, ey, 180, eh, "MCP clients", None, EXT, "Users")
    c.node(728, ey, 190, eh, "Customer CRM", "HubSpot · Salesforce", EXT, "Client")
    c.node(942, ey, 180, eh, "Customer Slack", None, EXT, "Client")

    A = 336
    c.p.append(f'<rect x="50" y="{A}" width="1100" height="400" rx="4" ry="4" fill="none" stroke="#2b6cb0" '
               'stroke-width="2.6" stroke-dasharray="12 6"/>')
    c.text(66, A + 386, "Deal Intelligence — AWS, us-east-1", 12.5, "start", "bold", "#2b6cb0")

    c.node(100, A - 34, 460, 68, "CloudFront + WAF", "api.dealintelligence.io · mcp.dealintelligence.io", BND, "AWSWAF")
    c.node(820, A - 34, 280, 68, "NAT", "outbound only", BND, "AmazonVPCNATGateway")

    c.boundary(80, 426, 1040, 260, "Private network", "#2f855a")
    c.node(150, 476, 300, 68, "API", "Lambda", INT, "AWSLambda")
    c.cyl(620, 468, 400, 84, "Customer data", "DocumentDB · encrypted · 35-day backups", "AmazonDocumentDB")

    c.arrow([(176, ey + eh), (176, A - 34)], "HTTPS 443", 184, 274, "start")
    c.arrow([(400, ey + eh), (400, A - 34)], "HTTPS 443", 408, 274, "start")
    c.arrow([(540, ey + eh), (540, A - 34)], "HTTPS 443", 548, 274, "start")
    c.arrow([(250, A + 34), (250, 476)], "HTTPS 443", 262, 446, "start")
    c.arrow([(450, 510), (620, 510)], "TCP 27017", 535, 502, "middle")
    c.arrow([(300, 544), (300, 606), (1080, 606), (1080, A + 34)], "HTTPS 443", 1072, 486, "end")
    c.arrow([(860, A - 34), (860, ey + eh)], "HTTPS 443", 868, 274, "start")
    c.arrow([(1032, A - 34), (1032, ey + eh)], "HTTPS 443", 1040, 274, "start")
    c.save("di-backend-network-customer")


B = {"internal": build_internal, "customer": build_customer}
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(B)):
        B[n]()
