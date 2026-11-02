# Business Continuity Plan — v1.0 → v2.0 change note

- R0: frontmatter — `version` 1.0 → 2.0, `supersedes: "1.0"`, `doc_type` Procedure → Plan, `effective_date`/`review_date` set to publication placeholders, `finalized_at` export field dropped; "Revision history" section added at the end.
- R0: fixed the Humadroid "#### 1." repeated-numbering artefacts in §6.2, §6.3, §6.4 to 1/2/3.
- R0/R8: restored collapsed bullets (§2 Geographic Scope, §3.3 "Ensures vendor SLA compliance … Maintains vendor contact information", §4.2 "DocumentDB cluster with KMS encryption / CloudFront CDN distribution", §6.3 "Restore EventBridge schedules", §6.4 "Schedule follow-up testing", §7.3 "Alternative authentication provider evaluation", Appendix C run-on, Appendix A split table merged into one).
- R6: "businessimpacting" → "business-impacting"; "useast-1a" → "us-east-1a"; `[Maintained Separately]` in Appendix A → `[CONFIRM: phone]` / `[CONFIRM: email]`.
- R4: §2 — added the statement that the platform is single-region (us-east-1) by design, with intra-region resilience via Multi-AZ and regional-outage recovery via CloudFormation redeployment.
- R2: §3 role holders "Mo Messidi, Chief Executive Officer" → "Chief Executive Officer (Mo Messidi)"; §3.1 "activates response teams" → "activates this plan"; §3.2 "Maintains technical recovery documentation and runbooks" → "Maintains the technical recovery procedures in this plan (Sections 6 and 7)" (also R4, no separate runbooks); §6.2 "Mo Messidi assesses" → "The CEO assesses"; §8.1 Responsible Party "Mo Messidi" → "CEO"; §8.2 step 5 "approval from Mo Messidi" → "approval from the CEO"; §10.2 "Annual effectiveness review presented to Mo Messidi" → "recorded in the management meeting minutes".
- R3: §4.1 — RTO/RPO table kept verbatim; added one sentence stating the values are met with Multi-AZ DocumentDB + PITR + 90-day backups, and (R5) that authentication availability is provided by PropelAuth under its own SLA.
- R3: §5.1 "Automated failover mechanisms for database services" now explicitly "(Multi-AZ DocumentDB with a second instance in another availability zone)".
- R4: §5.1 "Load balancing across multiple Lambda function instances" → "Lambda versioned deployments with rollback via `serverless rollback`".
- R3: §5.2 quarterly backup restoration test — added "recorded in the compliance platform"; §8.1 Backup Restoration scope now says "(automated, recorded in the compliance platform)".
- R4: §5.3 "Integration with incident detection Lambda functions" → "the breach-detection Lambda function that routes Security Hub findings to SNS".
- R4: §6.2 "Update status page with current service status" removed; §6.4 "Update status page to operational" removed, "Notify customers of service restoration" now "via email"; §9.3 Customers contact method "Email, Status Page" → "Email".
- R3: §6.3 "Reconcile any data gaps from transaction logs" → "using point-in-time recovery"; §7.1 "Incremental recovery using transaction logs" → "using point-in-time recovery" (DocumentDB exposes PITR, not transaction logs).
- R4: §7.1 "Cross-region backup replication for critical data" → "Point-in-time recovery enabled on the DocumentDB cluster" (R3 claim).
- R4: §7.2 "Database read replicas promoted to primary" → "Automatic failover of DocumentDB to the second instance in another availability zone"; "Load balancer health checks trigger failover" → "CloudWatch alarms on API errors and latency detect the failure".
- R3/R8: §7.2 "Automated deployment via CI/CD pipeline" → "via GitHub Actions (`serverless deploy`) from a green CI run".
- R4: §7.3 "Multi-region deployment consideration for critical services" → "Single-region deployment (us-east-1) by design; recovery from a regional outage relies on AWS service restoration".
- R4/R5: §8.3 "Technical recovery training for Mo Messidi quarterly" → "Technical recovery procedures exercised by the CEO through the quarterly backup restoration test".
- R8: §8.2 step 7 "the compliance platform's Business Continuity Plans module" → "the compliance platform".
- R4: Appendix B "Detailed technical runbooks maintained separately in secure documentation repository" → "Appendix B: Recovery Procedures" pointing to Sections 6 and 7 of this plan (same five topics, no separate runbooks).
- Kept verbatim (no rule applies): §4.1 numbers, §6.2 "Implement traffic rerouting", "Activate CloudFront failover origins if configured", "Scale unaffected resources"; §7.3 PropelAuth contingency bullets; §8.1 semi-annual failover test and quarterly communication test; §9 notification cadences.

## CONFIRM

- Appendix A: CEO phone and email for the emergency contact list (`[CONFIRM: phone]`, `[CONFIRM: email]`).
- §4.1 Authentication Services row (RTO 1 hour / RPO 30 minutes): kept from v1 but authentication is hosted by PropelAuth — confirm these values are meant to cover the platform's PropelAuth integration only.
- §6.2 "Activate CloudFront failover origins if configured" and §7.3 "Emergency bypass for critical operations (with audit logging)": v1 claims not covered by any rule; confirm they exist or strike.
- §8.1 "Failover Testing — Semi-annually — AZ failover procedures": kept from v1; confirm a DocumentDB failover test is actually performed semi-annually.

## Quality sweep (2026-10-31)

- Structure: fixed 12 `####` leftovers (`#### 1. Detection and Assessment` … `#### 3. Post-Incident Activities`) into 6.2.1–6.4.3; the colon-suffixed `#### Backup Architecture:`-style pseudo-headings (12) turned into lead-in lines under their `###`; §3 three role sub-sections (Business Continuity Coordinator / Technical Recovery Lead / Vendor Liaison, each "Role Holder: CEO") merged into §3.1 Chief Executive Officer (CEO) with the three role labels and all bullets kept; Appendix C renamed "Related documents" and expanded to the documents cited in the body (Data Classification and Handling Standard, Information Security Policy, Security Awareness Training Program, System Monitoring and Logging Procedure); revision history numbered §12.
- Voice: removed "ensures systematic", "ensuring business resilience across all operational contexts", "comprehensive health checks"; "Ensures vendor SLA compliance" → "Tracks vendor SLA compliance"; §6.2.1 mixed subjects ("Automated monitoring alerts trigger / The CEO assesses / Determine if …") made parallel; §6.2.2 made declarative.
- Formatting: removed blank lines between bullets (≈150 lines); tables: bold header cells removed, "N/A" → "—", "AWS Lambda" → "Lambda", "AWS Fargate" → "Fargate", "CloudFront CDN distribution" → "CloudFront distribution", "900s" → "900 s", "multi-availability zone" → "Multi-AZ" ×3, "99.9%" → "99.9 %", en dashes in ranges; Oxford comma applied.
- Consistency: "Section 5" → "section 5" cross-references; "Parameter store" → "Parameter Store"; "AWS support" → "AWS Support".
- Kept: all RTO/RPO/MTD values, 02:00 UTC backup time, test schedule, notification timings, contact placeholders, Appendix A "24/7" for AWS Support (whitelisted vendor fact).

No new CONFIRM items.

## Decisions applied (2026-10-31)

- D10: §9.2 customer updates "every 4 hours" → cross-referenced to the SLA Management Policy cadence (every 2 hours for P1 incidents); §9.1 internal 30-minute updates kept (matches the IR procedure).
- D21: §3.1 "The Chief Executive Officer (CEO), Mo Messidi, holds all three BCP roles" → title only. Appendix A emergency contact list left with the name (contact directory, not policy prose).
- D25: cut §8.1 semi-annual failover testing, quarterly communication test, annual vendor coordination test (table now: quarterly backup restoration, annual full BCP exercise); cut §8.3 semi-annual vendor coordination procedure review; cut §10.2 quarterly metrics on recovery objectives. Kept: quarterly backup restoration test, annual full BCP exercise, annual plan review, annual effectiveness review in the management meeting minutes, annual BCP awareness training.
- D2: §7.1 "customer-managed KMS keys" kept (target key design per the Encryption Standard).
- D18/D24: concern the BCP test record, not this plan; nothing changed here.

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §5.3 Monitoring and early warning: "Security Hub findings for threat detection" and "breach-detection Lambda function that routes Security Hub findings to SNS" replaced by the CloudTrail-EventBridge → breach-detection Lambda → SNS real-time alert and the monthly configuration-check Lambda record (checklist includes DocumentDB backup retention and Multi-AZ, which is the BCP-relevant part).
- D13b: the BCP states the 99.9 % SLA but does not define its measurement or record; measurement and the monthly "Availability record (monthly)" task live in the SLA Management Policy. Nothing to apply here.
- D11b, D14: no insurance or controller/processor text in this document; nothing to apply.

## Decision applied (2026-11-01)

- D26: no Multi-AZ DocumentDB (Mo, 2026-11-01; a standby instance is not worth the cost). Multi-AZ / second-instance / automatic-failover wording replaced by: DocumentDB cluster storage replicated six ways across three availability zones by the service; a single serverless instance re-created automatically after an instance failure (same AZ, best effort), recovered manually into us-east-1b after an outage of us-east-1a (corrected 2026-11-01, D27); point-in-time recovery and automated backups. "DocumentDB backup retention and Multi-AZ" in the configuration-check checklist → "DocumentDB backup retention".
