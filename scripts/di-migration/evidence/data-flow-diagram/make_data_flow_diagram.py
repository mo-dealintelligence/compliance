#!/usr/bin/env python3
"""
Deal Intelligence data flow diagrams.

  internal  every process, data store and outside party that customer data touches.
  customer  the same flows with the customer's systems as the only outside party.

Processes are boxes, data stores are cylinders, outside parties sit in the top band.
Arrows point the way the data moves and are labelled with what moves. Dashed boxes are
trust boundaries. Reuses the drawing helpers and AWS icons of ../network-diagram.

Facts (2026-11-01, di-backend-api): CRM records are pulled with the customer's OAuth
token and matched in memory; the match result is cached in DocumentDB `roi_cache` with a
1-hour TTL index. Competitor activity signals are written into the customer's CRM.
Slack receives alerts through the customer's incoming webhook. OAuth tokens live in
Secrets Manager. Fargate jobs write collected data through the platform API.

    python3 make_data_flow_diagram.py [internal|customer]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "network-diagram"))
import make_network_diagram as nd  # noqa: E402

nd.HERE = HERE  # write outputs next to this script
Canvas, EXT, INT, SUP, DATE = nd.Canvas, nd.EXT, nd.INT, nd.SUP, nd.DATE


def both(c, pts, label=None, lx=None, ly=None, anchor="middle"):
    """Data moving in both directions (read and write)."""
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    c.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.1" '
               'marker-start="url(#a)" marker-end="url(#a)"/>')
    if label:
        c.text(lx, ly, label, 10.5, anchor, fill="#222")


def dashed(c, pts, label=None, lx=None, ly=None, anchor="middle"):
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    c.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.1" stroke-dasharray="5 4" '
               'marker-start="url(#a)" marker-end="url(#a)"/>')
    if label:
        c.text(lx, ly, label, 10.5, anchor, fill="#222")


def legend(c, x, y, admin=True):
    c.p.append(f'<line x1="{x}" y1="{y-4}" x2="{x+30}" y2="{y-4}" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#a)"/>')
    c.text(x + 38, y, "data flow — arrow points the way the data moves", 10.5, "start", fill="#333")
    if admin:
        c.p.append(f'<line x1="{x}" y1="{y+14}" x2="{x+30}" y2="{y+14}" stroke="#1a1a1a" stroke-width="1.1" '
                   'stroke-dasharray="5 4" marker-end="url(#a)"/>')
        c.text(x + 38, y + 18, "administrative access", 10.5, "start", fill="#333")


def build(variant):
    internal = variant == "internal"
    c = Canvas(1620, 1060)
    if internal:
        c.header("Deal Intelligence — Data Flow Diagram",
                 f"Production · AWS account 164482277879 · us-east-1 · v1.0 · {DATE} · owner: CEO")
    else:
        c.header("Deal Intelligence — Data Flow Diagram", f"Customer data · v1.0 · {DATE}")

    # outside parties
    c.boundary(50, 124, 1520, 118, "Outside the system boundary" if internal else "Customer systems")
    ey, eh = 158, 64
    c.node(72, ey, 320, eh, "Customer users", "web app · REST API · MCP", EXT, "Users")
    c.node(640, ey, 280, eh, "Customer CRM", "HubSpot · Salesforce", EXT, "Client")
    c.node(960, ey, 240, eh, "Customer Slack", None, EXT, "Client")
    if internal:
        c.node(1300, ey, 248, eh, "Operator", "CEO", EXT, "Users")

    # platform
    A = 300
    c.boundary(50, A, 1520, 690, "Deal Intelligence — AWS us-east-1", "#2b6cb0", at="bottom")
    c.node(100, 400, 900, 70, "Platform API", "Lambda app · Lambda mcp", INT, "AWSLambda")
    if internal:
        c.node(1150, 400, 340, 70, "Data collection", "Fargate jobs", INT, "AWSFargate")

    c.boundary(84, 580, 1022, 160, "DocumentDB — encrypted with KMS", "#2f855a")
    c.cyl(104, 620, 330, 84, "Competitor activity data", "events · accounts · contacts · Confidential", "AmazonDocumentDB")
    c.cyl(454, 620, 316, 84, "Customer accounts", "users · companies · settings · Confidential", "AmazonDocumentDB")
    c.cyl(790, 620, 296, 84, "CRM match cache", "roi_cache · deleted after 1 h · Confidential", "AmazonDocumentDB")
    c.cyl(1150, 620, 340, 84, "Integration credentials", "Secrets Manager · OAuth tokens · Restricted", "AWSSecretsManager")
    c.cyl(310, 850, 570, 84, "DocumentDB backups", "automated snapshots · 35 days · encrypted", "AmazonDocumentDB")

    # customer users <-> API
    c.arrow([(180, ey + eh), (180, 400)], "requests · settings", 188, 280, "start")
    c.arrow([(300, 400), (300, ey + eh)], "competitor activity results", 308, 340, "start")
    # CRM <-> API
    c.arrow([(700, ey + eh), (700, 400)], "accounts · opportunities", 692, 280, "end")
    c.arrow([(860, 400), (860, ey + eh)], "competitor activity signals", 852, 340, "end")
    # API -> Slack
    c.arrow([(985, 400), (985, ey + eh)], "alerts", 993, 280, "start")
    # Fargate -> API
    if internal:
        c.arrow([(1150, 435), (1000, 435)], "collected activity", 1075, 427, "middle")

    # API <-> stores
    both(c, [(380, 470), (380, 620)], "read · write", 388, 545, "start")
    both(c, [(612, 470), (612, 620)], "read · write", 620, 545, "start")
    both(c, [(900, 470), (900, 620)], "CRM matches", 908, 600, "start")
    both(c, [(1320, 620), (1320, 530), (960, 530), (960, 470)], "OAuth tokens", 1200, 522, "middle")
    # stores -> backups
    c.arrow([(595, 740), (595, 850)], "daily snapshot · all collections", 603, 800, "start")

    if internal:
        dashed(c, [(1424, ey + eh), (1424, 270), (1540, 270), (1540, 790), (1000, 790), (1000, 740)],
               "admin queries · bastion", 1270, 782, "middle")

    legend(c, 70, 1022, admin=internal)
    c.save(f"di-backend-data-flow-{variant}")


B = {"internal": lambda: build("internal"), "customer": lambda: build("customer")}
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(B)):
        B[n]()
