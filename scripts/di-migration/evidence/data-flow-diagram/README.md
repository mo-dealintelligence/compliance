# Data flow diagrams — di-backend-api production

| File | Audience |
|---|---|
| `di-backend-data-flow-internal-2026-11-01.png` | Engineering, auditor. Every process, store and outside party customer data touches. |
| `di-backend-data-flow-customer-2026-11-01.png` | Customers. Customer systems are the only outside parties. |

Companion to `../network-diagram/` (which shows connections and ports). Here boxes are
processes, cylinders are data stores (with collection names and classification from the
Data Classification and Handling Standard), dashed boxes are trust boundaries, and arrows
point the way the data moves, labelled with what moves.

Facts as of 2026-11-01 from di-backend-api:
- CRM accounts and opportunities are pulled with the customer's OAuth token and matched
  in memory. The match result is cached in DocumentDB `roi_cache`, removed by a 1-hour
  TTL index; DocumentDB snapshots (35 days) can capture rows present at snapshot time.
- Competitor activity signals are written to the customer's CRM; alerts go to the
  customer's Slack incoming webhook. Neither CRM nor Slack sends data to the platform
  on its own initiative.
- OAuth tokens are stored in Secrets Manager, not DocumentDB.
- Fargate jobs write collected data through the platform API.

Source: `make_data_flow_diagram.py` (reuses the helpers and AWS icons in `../network-diagram`).
