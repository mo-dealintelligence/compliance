#!/usr/bin/env python3
"""
Deal Intelligence data flow diagrams (Level 1), Gane-Sarson notation.

  internal  every process, store and outside party that customer data touches.
  customer  the same flows with the customer's systems as the only outside party.

Conventions (Gane-Sarson / Microsoft threat-modelling DFD):
  external entity  square-cornered rectangle, outside the system boundary
  process          rounded rectangle with an ID band (1.0, 2.0 ...), named by function
  data store       rectangle with an ID cell on the left (D1, D2), a LOGICAL store
  data flow        arrow in the direction the data moves, labelled with the data and
                   its classification: [C] Confidential, [R] Restricted
  trust boundary   dashed rectangle
Stores connect only to processes; no store-to-store or entity-to-store flows.
Lines are horizontal/vertical only.

Facts (2026-11-01, di-backend-api, after the roi_cache change): CRM accounts and
opportunities are pulled with the customer's OAuth token, matched against competitor
activity in Lambda memory and never written to a store; competitor activity signals are
written back to the CRM; Slack alerts go to the customer's incoming webhook (URL kept in
D1); OAuth tokens are in Secrets Manager; Fargate jobs submit collected activity through
the platform API; the operator reaches DocumentDB only through the bastion.

    python3 make_data_flow_diagram.py [internal|customer]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "network-diagram"))
import make_network_diagram as nd  # noqa: E402

nd.HERE = HERE
Canvas, EXT, INT, DATE = nd.Canvas, nd.EXT, nd.INT, nd.DATE
STORE = ("#d5e8d4", "#82b366")
VERSION = "v2.0"


def entity(c, x, y, w, h, title, sub=None, ic=None):
    f, s = EXT
    c.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    tx = x + 50 if ic else x + w / 2
    ta = "start" if ic else "middle"
    if ic:
        c.icon(ic, x + 11, y + h / 2 - 15)
    if sub:
        c.text(tx, y + h / 2 - 2, title, 12.5, ta, "bold")
        c.text(tx, y + h / 2 + 14, sub, 10.5, ta, fill="#444")
    else:
        c.text(tx, y + h / 2 + 4.5, title, 12.5, ta, "bold")


def process(c, x, y, w, h, pid, title, sub=None, ic=None):
    f, s = INT
    c.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" ry="14" fill="{f}" stroke="{s}" stroke-width="1.6"/>')
    c.p.append(f'<line x1="{x}" y1="{y+22}" x2="{x+w}" y2="{y+22}" stroke="{s}" stroke-width="1.2"/>')
    c.text(x + w / 2, y + 16, pid, 11, "middle", "bold", "#2b4a7a")
    body = y + 22 + (h - 22) / 2
    tx = x + 50 if ic else x + w / 2
    ta = "start" if ic else "middle"
    if ic:
        c.icon(ic, x + 11, body - 15)
    if sub:
        c.text(tx, body - 2, title, 12.5, ta, "bold")
        c.text(tx, body + 14, sub, 10.5, ta, fill="#444")
    else:
        c.text(tx, body + 4.5, title, 12.5, ta, "bold")


def store(c, x, y, w, h, sid, title, sub=None, ic=None):
    f, s = STORE
    c.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}" stroke="{s}" stroke-width="1.8"/>')
    c.p.append(f'<line x1="{x+46}" y1="{y}" x2="{x+46}" y2="{y+h}" stroke="{s}" stroke-width="1.4"/>')
    c.text(x + 23, y + h / 2 + 4.5, sid, 12, "middle", "bold", "#2f5d2a")
    tx = x + 96 if ic else x + 60
    if ic:
        c.icon(ic, x + 56, y + h / 2 - 15)
    if sub:
        c.text(tx, y + h / 2 - 2, title, 12.5, "start", "bold")
        c.text(tx, y + h / 2 + 14, sub, 10.5, "start", fill="#444")
    else:
        c.text(tx, y + h / 2 + 4.5, title, 12.5, "start", "bold")


def flow(c, pts, label=None, lx=None, ly=None, anchor="middle", both=False):
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    start = ' marker-start="url(#a)"' if both else ""
    c.p.append(f'<path d="{path}" fill="none" stroke="#1a1a1a" stroke-width="1.1"{start} marker-end="url(#a)"/>')
    if label:
        c.text(lx, ly, label, 10.5, anchor, fill="#222")


def key(c, x, y):
    c.text(x, y, "Key", 11, "start", "bold", "#333")
    entity(c, x + 34, y - 14, 46, 20, "")
    c.text(x + 86, y, "external entity", 10.5, "start", fill="#333")
    c.p.append(f'<rect x="{x+190}" y="{y-14}" width="46" height="20" rx="7" fill="{INT[0]}" stroke="{INT[1]}" stroke-width="1.4"/>')
    c.text(x + 242, y, "process", 10.5, "start", fill="#333")
    c.p.append(f'<rect x="{x+300}" y="{y-14}" width="46" height="20" fill="{STORE[0]}" stroke="{STORE[1]}" stroke-width="1.4"/>')
    c.p.append(f'<line x1="{x+312}" y1="{y-14}" x2="{x+312}" y2="{y+6}" stroke="{STORE[1]}" stroke-width="1.2"/>')
    c.text(x + 352, y, "data store", 10.5, "start", fill="#333")
    c.p.append(f'<line x1="{x+432}" y1="{y-4}" x2="{x+466}" y2="{y-4}" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#a)"/>')
    c.text(x + 474, y, "data flow", 10.5, "start", fill="#333")
    c.p.append(f'<rect x="{x+546}" y="{y-14}" width="46" height="20" fill="none" stroke="#444" stroke-width="2" stroke-dasharray="8 4"/>')
    c.text(x + 598, y, "trust boundary", 10.5, "start", fill="#333")
    c.text(x + 700, y, "[C] Confidential · [R] Restricted", 10.5, "start", fill="#333")


def build(variant):
    internal = variant == "internal"
    c = Canvas(1620, 930)
    sub = (f"Level 1 · production · AWS account 164482277879 · us-east-1 · {VERSION} · {DATE} · owner: CEO"
           if internal else f"Level 1 · customer data · {VERSION} · {DATE}")
    c.header("Deal Intelligence — Data Flow Diagram", sub)

    # outside the system boundary
    c.boundary(50, 124, 1520, 118, "Outside the system boundary" if internal else "Customer systems")
    ey, eh = 158, 64
    entity(c, 72, ey, 360, eh, "Customer users", "web app · REST API · MCP", "Users")
    entity(c, 560, ey, 320, eh, "Customer CRM", "HubSpot · Salesforce", "Client")
    entity(c, 1000, ey, 240, eh, "Customer Slack", None, "Client")
    if internal:
        entity(c, 1310, ey, 238, eh, "Operator", None, "Users")

    # system boundary
    c.boundary(50, 300, 1520, 560, "Deal Intelligence — AWS us-east-1", "#2b6cb0", at="bottom")
    py, ph = 390, 84
    process(c, 100, py, 340, ph, "1.0", "Serve platform requests", "Lambda app · Lambda mcp", "AWSLambda")
    process(c, 560, py, 320, ph, "2.0", "Match CRM records", "Lambda app · in memory only", "AWSLambda")
    process(c, 1000, py, 240, ph, "3.0", "Send alerts", "Lambda app", "AWSLambda")
    if internal:
        process(c, 1310, py, 238, ph, "5.0", "Administer database", "bastion", "AmazonElasticContainerService")
        process(c, 100, 560, 250, ph, "4.0", "Collect competitor activity", "Fargate jobs", "AWSFargate")
    store(c, 560, 570, 240, 56, "D2", "Integration credentials", "Secrets Manager [R]", "AWSSecretsManager")
    store(c, 100, 720, 1140, 60, "D1", "Platform database",
          "DocumentDB · competitor activity · customer accounts & settings · encrypted · 35-day backups · [C]",
          "AmazonDocumentDB")

    # entities <-> processes (crossing the system boundary)
    flow(c, [(170, ey + eh), (170, py)], "requests · settings [C]", 178, 282, "start")
    flow(c, [(360, py), (360, ey + eh)], "results · ROI [C]", 368, 350, "start")
    flow(c, [(620, ey + eh), (620, py)], "accounts · opportunities [C]", 628, 282, "start")
    flow(c, [(820, py), (820, ey + eh)], "activity signals [C]", 828, 350, "start")
    flow(c, [(1120, py), (1120, ey + eh)], "alerts [C]", 1128, 282, "start")
    if internal:
        flow(c, [(1429, ey + eh), (1429, py)], "queries · results [C]", 1437, 282, "start", both=True)

    # process <-> process
    flow(c, [(440, 420), (560, 420)], "ROI request", 500, 412, "middle")
    flow(c, [(560, 452), (440, 452)], "CRM matches [C]", 500, 444, "middle")
    if internal:
        flow(c, [(230, 560), (230, py + ph)], "collected activity [C]", 238, 520, "start")

    # processes <-> stores
    flow(c, [(380, py + ph), (380, 720)], "read · write [C]", 388, 690, "start", both=True)
    flow(c, [(430, py + ph), (430, 598), (560, 598)], "OAuth tokens [R]", 438, 590, "start")
    flow(c, [(700, 570), (700, py + ph)], "OAuth tokens [R]", 708, 530, "start")
    flow(c, [(840, 720), (840, py + ph)], None)
    c.text(848, 690, "competitor activity [C]", 10.5, "start", fill="#222")
    flow(c, [(1080, 720), (1080, py + ph)], "activity · webhook URL [C]", 1088, 600, "start")
    if internal:
        flow(c, [(1429, py + ph), (1429, 750), (1240, 750)], "queries · results [C]", 1437, 600, "start", both=True)

    key(c, 70, 900)
    c.save(f"di-backend-data-flow-{variant}")


B = {"internal": lambda: build("internal"), "customer": lambda: build("customer")}
if __name__ == "__main__":
    for n in (sys.argv[1:] or list(B)):
        B[n]()
