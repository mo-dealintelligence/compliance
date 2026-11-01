# Data flow diagrams — di-backend-api production (Level 1)

| File | Audience |
|---|---|
| `di-backend-data-flow-internal-2026-11-01.png` | Engineering, auditor. Every process, store and outside party customer data touches. |
| `di-backend-data-flow-customer-2026-11-01.png` | Customers. Customer systems are the only outside parties. |

Companion to `../network-diagram/` (connections and ports). Drawn in Gane-Sarson notation,
the convention used for security DFDs (Microsoft threat modelling, PCI DSS 1.2.4):

- External entities: square rectangles, outside the system boundary.
- Processes: rounded rectangles with an ID (1.0 ...), named by what they do with the data.
- Data stores: rectangles with an ID cell on the left (D1, D2). These are logical stores:
  D1 is the one DocumentDB cluster, D2 is Secrets Manager.
- Data flows: arrows in the direction the data moves, labelled with the data and its
  classification ([C] Confidential, [R] Restricted, per the Data Classification and
  Handling Standard). Stores connect only to processes.
- Trust boundaries: dashed rectangles.

Facts as of 2026-11-01 from di-backend-api (with the roi_cache change applied):
- 2.0 pulls CRM accounts and opportunities with the customer's OAuth token, matches them
  against competitor activity in Lambda memory (15-minute in-process cache) and returns
  the result to 1.0. No flow from 2.0 to any store: CRM data is never written to D1, D2
  or backups. DocumentDB `roi_cache` holds a build-status marker only (no CRM content).
- 2.0 writes competitor activity signals into the customer's CRM.
- 3.0 posts alerts to the customer's Slack incoming webhook (URL stored in D1).
- OAuth tokens are written by 1.0 at connect time and read by 2.0; they live in D2.
- 4.0 (Fargate jobs) submits collected activity through 1.0.
- 5.0: the operator reaches D1 only through the bastion.

Source: `make_data_flow_diagram.py` (reuses the helpers and AWS icons in `../network-diagram`).
