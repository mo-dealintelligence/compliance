
- D1 revised (Mo, 2026-10-31): staging moves to a **separate AWS account** in the same Organization; wording updated from "staging stage of the same stack" to a staging environment/account.

## Decision applied (2026-11-01)

- D26: no Multi-AZ DocumentDB (Mo, 2026-11-01; a standby instance is not worth the cost). Multi-AZ / second-instance / automatic-failover wording replaced by: DocumentDB cluster storage replicated six ways across three availability zones by the service; a single serverless instance re-created automatically after any failure including an AZ failure; fallback: add an instance in us-east-1b (corrected 2026-11-01, D27); point-in-time recovery and automated backups. "DocumentDB backup retention and Multi-AZ" in the configuration-check checklist → "DocumentDB backup retention".
