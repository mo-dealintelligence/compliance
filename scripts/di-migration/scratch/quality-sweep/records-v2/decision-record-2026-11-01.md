---
title: Decision record — DocumentDB availability and backup retention
date: November 1, 2026
author: Mo Messidi, Chief Executive Officer
---

# Decision record — November 1, 2026

Decisions taken by the CEO on November 1, 2026. They amend the targets recorded in the management meeting minutes of October 31, 2026 (section 4.4), which are left unchanged.

## D26 — No second DocumentDB instance

**Decision.** Production keeps one `db.serverless` DocumentDB instance in us-east-1a. No standby instance in a second availability zone is deployed.

**Basis.** DocumentDB cluster storage is replicated six ways across three availability zones, so an instance or zone failure loses no committed data. A standby instance only shortens recovery of the compute.

**Effect on recovery.**
- Instance or availability-zone failure: DocumentDB re-creates the instance automatically, typically within 10 minutes; no committed data is lost.
- Fallback if re-creation has not completed within the RTO: the CEO adds a `db.serverless` instance in us-east-1b to the same cluster; it takes over the cluster endpoint. Business Continuity Plan section 7.2.
- Data corruption or deletion: point-in-time restore.

**Withdrawn.** The October 31 target "DocumentDB Multi-AZ with automatic failover".

## D27 — DocumentDB backup retention 35 days

**Decision.** DocumentDB automated backups are retained 35 days with point-in-time recovery, the maximum the service supports and the current setting. No additional snapshots or backup service.

**Withdrawn.** The October 31 target "90-day retention with point-in-time recovery".

**Evidence.** Quarterly backup-restore test recorded in the compliance platform.

## Policies updated

Business Continuity Plan, Cloud Infrastructure Security Policy, Information Security Policy, Incident Response Procedure, Risk Assessment Procedure, Service Level Agreement (SLA) Management Policy, System Monitoring and Logging Procedure, Data Classification and Handling Standard, Data Retention and Disposal Policy, Data Subject Rights Request Procedure, Penetration Testing and Security Assessment Procedure, Vulnerability Management Procedure, and the system description.
