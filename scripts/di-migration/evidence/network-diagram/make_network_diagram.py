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
                      f'stroke="{color}" stroke-width="1.6" stroke-dasharray="8 5"/>')
        self.text(x + 16, y + 22 if at == "top" else y + h - 13, label, 12.5, "start", "bold", color)

    def arrow(self, pts, label=None, lx=None, ly=None, anchor="middle"):
        path = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.8" marker-end="url(#a)"/>')
        if label:
            self.text(lx, ly, label, 10.5, anchor, fill="#222")

    def header(self, title, sub):
        self.text(40, 46, title, 24, "start", "bold")
        self.text(40, 70, "Mo Messidi, Chief Executive Officer, Deal Intelligence", 12, "start", fill="#444")
        self.text(40, 91, sub, 12, "start", fill="#444")

    def save(self, stem):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
               f'<rect width="{self.w}" height="{self.h}" fill="#fff"/><defs><marker id="a" viewBox="0 0 10 10" refX="9" '
               'refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
               'fill="#1a1a1a"/></marker></defs>' + "".join(self.p) + "</svg>")
        (HERE / f"{stem}.svg").write_text(svg)
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / f"{stem}-{DATE}.png"),
                         output_width=self.w * 2, output_height=self.h * 2, background_color="white")
        print(f"  {stem}")


def build_internal():
    c = Canvas(1300, 1150)
    c.header("Deal Intelligence — Network Flow Diagram",
             f"Production, AWS account 164482277879, us-east-1 · {DATE}")

    c.boundary(50, 124, 1200, 118, "Internet")
    ey, eh, ew = 158, 64, 212
    c.node(72, ey, ew, eh, "Customers", "MCP · REST API · Clay", EXT, "Users")
    c.node(308, ey, ew, eh, "PropelAuth", "identity provider", EXT, "Client")
    c.node(544, ey, ew, eh, "Customer CRMs", "HubSpot · Salesforce", EXT, "Client")
    c.node(780, ey, ew, eh, "Google Workspace", None, EXT, "Client")
    c.node(1016, ey, ew, eh, "Data vendors", None, EXT, "Internetalt1")

    A = 330
    c.p.append(f'<rect x="50" y="{A}" width="1200" height="770" rx="4" ry="4" fill="none" stroke="#2b6cb0" '
               'stroke-width="1.7" stroke-dasharray="8 5"/>')
    c.text(66, A + 756, "AWS account 164482277879 — us-east-1", 12.5, "start", "bold", "#2b6cb0")

    c.node(100, A - 34, 560, 68, "CloudFront + WAF", "self-managed WAF · TLS 1.2+", BND, "AWSWAF")
    c.node(900, A - 34, 300, 68, "NAT", "self-managed instance · t3.micro · public subnet", BND, "AmazonVPCNATGateway")

    c.boundary(80, 410, 1140, 650, "VPC 10.0.0.0/16", "#2f855a")
    c.boundary(104, 440, 700, 520, "Private subnets — us-east-1a / 1b / 1f", "#555")
    c.node(128, 480, 300, 64, "Lambda app", "FastAPI", INT, "AWSLambda")
    c.node(448, 480, 330, 64, "Lambda mcp", "MCP server", INT, "AWSLambda")
    c.node(128, 580, 300, 64, "Lambda orchestrator", None, INT, "AWSLambda")
    c.node(448, 580, 330, 64, "Scheduled Lambdas", None, INT, "AWSLambda")
    c.cyl(200, 780, 500, 80, "DocumentDB", "di-backend-production-cluster", "AmazonDocumentDB")

    c.boundary(830, 440, 366, 520, "Public subnet", "#555")
    c.node(856, 480, 316, 64, "Fargate tasks", "di-jobs-production-cluster", INT, "AWSFargate")

    sw = 206
    for i, (ic, t) in enumerate([("AWSSecretsManager", "Secrets Manager"), ("AWSKeyManagementService", "KMS"),
                                 ("AmazonSimpleStorageService", "S3"), ("AWSCloudTrail", "CloudTrail"),
                                 ("AmazonElasticContainerRegistry", "ECR")]):
        c.node(104 + i * (sw + 16), 986, sw, 54, t, None, SUP, ic)

    # inbound
    c.arrow([(178, ey + eh), (230, A - 34)], "HTTPS 443", 150, 290, "start")
    c.arrow([(250, A + 34), (250, 480)], "HTTPS 443", 262, 430, "start")
    c.arrow([(600, A + 34), (600, 480)], "HTTPS 443", 588, 440, "end")
    # to the database
    c.arrow([(278, 544), (380, 780)], "TCP 27017", 318, 672, "end")
    c.arrow([(613, 544), (560, 780)], "TCP 27017", 598, 672, "start")
    c.arrow([(230, 644), (300, 780)], "TCP 27017", 180, 740, "start")
    c.arrow([(660, 644), (620, 780)], "TCP 27017", 650, 740, "start")
    # orchestrator launches Fargate
    c.arrow([(330, 644), (330, 700), (1014, 700), (1014, 544)], "ECS RunTask", 860, 692, "start")
    # Lambdas out through the NAT
    c.arrow([(778, 612), (1190, 612), (1190, A + 34)], "HTTPS 443", 1070, 604, "start")
    c.arrow([(970, A - 34), (414, ey + eh)], "HTTPS 443", 560, 300, "start")
    c.arrow([(1030, A - 34), (660, ey + eh)], "HTTPS 443", 760, 290, "start")
    c.arrow([(1090, A - 34), (900, ey + eh)], "HTTPS 443", 950, 280, "start")
    # Fargate: calls the API through CloudFront; reaches vendors directly
    c.arrow([(856, 500), (840, 500), (840, 420), (620, 420), (620, A + 34)], "HTTPS 443", 700, 403, "start")
    c.arrow([(1172, 500), (1236, 500), (1236, 250), (1130, 222)], "HTTPS 443", 1242, 390, "start")
    c.save("di-backend-network-internal")


def build_customer():
    c = Canvas(1200, 780)
    c.header("Deal Intelligence — Network Flow Diagram",
             f"How your systems connect to the Deal Intelligence platform · {DATE}")

    c.boundary(50, 124, 1100, 118, "Your systems")
    ey, eh = 158, 64
    c.node(76, ey, 250, eh, "Your users", "MCP · REST API · Clay", EXT, "Users")
    c.node(350, ey, 250, eh, "Your CRM", "HubSpot · Salesforce", EXT, "Client")
    c.node(624, ey, 230, eh, "Your Slack", None, EXT, "Client")
    c.node(878, ey, 250, eh, "PropelAuth", "sign-in", EXT, "Client")

    A = 330
    c.p.append(f'<rect x="50" y="{A}" width="1100" height="400" rx="4" ry="4" fill="none" stroke="#2b6cb0" '
               'stroke-width="1.7" stroke-dasharray="8 5"/>')
    c.text(66, A + 386, "Deal Intelligence — AWS, us-east-1", 12.5, "start", "bold", "#2b6cb0")

    c.node(100, A - 34, 300, 68, "CloudFront + WAF", "TLS 1.2+", BND, "AWSWAF")
    c.node(800, A - 34, 300, 68, "NAT", "outbound only", BND, "AmazonVPCNATGateway")

    c.boundary(80, 420, 1040, 260, "Private network", "#2f855a")
    c.node(150, 470, 300, 68, "API", "Lambda", INT, "AWSLambda")
    c.cyl(620, 462, 400, 84, "Your data", "DocumentDB · encrypted · 35-day backups", "AmazonDocumentDB")

    c.arrow([(200, ey + eh), (230, A - 34)], "HTTPS 443", 150, 290, "start")
    c.arrow([(250, A + 34), (250, 470)], "HTTPS 443", 262, 440, "start")
    c.arrow([(450, 504), (620, 504)], "TCP 27017", 535, 496, "middle")
    c.arrow([(300, 538), (300, 600), (1080, 600), (1080, A + 34)], "HTTPS 443", 1090, 480, "start")
    c.arrow([(880, A - 34), (520, ey + eh)], "HTTPS 443", 640, 300, "start")
    c.arrow([(940, A - 34), (760, ey + eh)], "HTTPS 443", 870, 280, "start")
    c.arrow([(1010, A - 34), (1000, ey + eh)], "HTTPS 443", 1020, 300, "start")
    c.save("di-backend-network-customer")


B = {"internal": build_internal, "customer": build_customer}
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(B)):
        B[n]()
