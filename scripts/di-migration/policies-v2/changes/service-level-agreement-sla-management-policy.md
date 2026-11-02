# Service Level Agreement (SLA) Management Policy — v1.0 → v2.0 change note

Source: `data/nov2025/md/service-level-agreement-sla-management-policy.md`
Output: `policies-v2/service-level-agreement-sla-management-policy.md`

## Frontmatter
- R0: `version` 1.0 → 2.0; `supersedes: "1.0"`; `effective_date` → `"<to be set at publication>"`; `review_date` → `"<one year after effective date>"`; dropped export-only `finalized_at` (R6). Kept `doc_type: Policy`, `author`, `source`, `acknowledgment`.
- R0: "## 3.1"-style sub-headings corrected to "### 3.1"; section numbers unchanged.

## Removals / rewordings / additions
- R1: §1 removed "PI1.1 (Processing Integrity)" from the TSC mapping (A1.1 and CC2.1 kept).
- R2: §11 "Technical Operations" and "Customer Success" → merged into §11.1 CEO (all bullets kept). Added §11.2 Go-to-Market Contractor (no production access or monitoring responsibilities; forwards customer SLA questions and feedback to the CEO).
- R2: §13.2 "Executive review for repeated SLA breaches" → "CEO review …"; "Customer advisory board review for systemic issues" → "Management review for systemic issues, recorded in the quarterly management meeting minutes".
- R3: §9.1 AWS row "Multi-AZ deployment" kept.
- R4 (Synthetics / status page / portal reports): §4.1 "CloudWatch Synthetics: canary tests every 5 minutes" → "CloudWatch Alarms: Alarms on API errors and latency (p95 > 2 seconds) with real-time SNS notification". §5.1 "Customer Reporting … generated automatically via Lambda … delivered through the customer portal" → "Availability Record and Customer Communication": monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform (v1's five content bullets kept as the record's contents); "Customers are notified of planned maintenance by email". §7.2 "Post-incident report published to status page" → "provided to affected customers by email". §8.1 notification "via email and status page" → "via email". §12.1 "Monthly availability reports from CloudWatch" → the monthly recorded availability figure.
- R4 (canary-style checks / circuit breakers): §4.1 "PropelAuth Status API … automated Lambda function checks" → "PropelAuth Service Status … provided by PropelAuth under its own SLA". §9.2 "Automated health checks every 5 minutes via EventBridge scheduled rules" → "AWS Health Dashboard and PropelAuth published service status monitored for dependency availability"; "Circuit breaker patterns implemented in Lambda functions" → "Lambda versioned deployments with reserved concurrency and rollback via `serverless rollback`".
- R4 (blue-green): §8.2 "Blue-green deployments for Lambda function updates" → "Lambda versioned deployments with rollback via `serverless rollback`".
- R4/R5 (15-minute 24/7 response): §7.1 "Response Time" column (15 min / 30 min / 2 h / 8 h) removed; sentence added: "Critical (P1) incidents are acknowledged by the CEO within 4 business hours, with Security Hub/SNS paging for critical findings. Response targets for other severities are defined in the Incident Response Procedure." Resolution targets kept as v1. §7.2 "Initial notification within 1 hour of critical incident detection" → "Initial notification by email following acknowledgment of a critical incident (see Section 7.1)". §13.2 "Escalation to Chief Executive Officer within 2 hours for critical issues" → "…who acknowledges critical issues within 4 business hours".
- R5 (99.9 % / no 99.95 % auth): §3.1 Authentication Service row "99.95% | Monthly | PropelAuth uptime monitoring" → "Provided by PropelAuth under its own SLA | Monthly | PropelAuth published service status". §9.1 PropelAuth "Their SLA" cell "99.95%" → "PropelAuth's own published SLA" (mitigation text kept).
- R5 (p95 > 2 s): §4.2 API Latency alert threshold "> 2000ms" → "p95 > 2 seconds".
- R5 (vendor reviews annual + availability record): §9.2 "Vendor performance tracked in the compliance platform Vendor Assessment workflow" → "Vendor performance reviewed annually in the compliance platform, supported by the continuous monthly availability record".
- R5 (policy review annual): §14 footer "subject to quarterly review" → "subject to annual review".
- R4 (reporting apparatus): §5.2 "Weekly internal SLA reviews" → "Monthly internal SLA reviews" to match the monthly availability figure that R4 names as the record (flagged in CONFIRM).
- R8: §8.1 Maintenance Tracking "Documented in the compliance platform Business Continuity Plans module" → "Recorded in the compliance platform".
- R8: restored real bullet lists (§2, §3.2, §8.2, §10.2, §12.2); split the §2 run-on "(PropelAuth authentication services) Internal operational processes…"; removed stray `<u>` fragments.
- R6: deleted the export junk footer "**Document Information Document Assignments (1)** mo@dealintelligence.io Pending"; §14 "Risk Assessment Procedure" made a proper list item.
- R0: added §15 Revision history.
- Kept verbatim (no rule applies): §3.1 Platform Availability, API Response Time, Data Processing Accuracy, Lead Delivery Time and Data Refresh rows; §3.2 exclusions; §4.2 other rows; §6 service-credit table and process; §7.1 resolution targets; §7.2 status updates every 2 hours and RCA within 48 hours; §8.1 standard window and emergency notice; §8.2 ECS rolling updates, migrations, cache warming; §10.1 quarterly SLA reviews; §10.2; §12.2; §13.1.

## CONFIRM
- [CONFIRM: Data Processing Accuracy 99.5 % and Lead Delivery < 24 hours] — kept as customer commitments (R1 only strips the PI criteria mapping); confirm they are measured ("Validated records / Total processed records") or drop the row.
- [CONFIRM: weekly → monthly internal SLA review] — v1 said weekly; changed to monthly to align with the R4 monthly availability record. Revert if weekly reviews are actually performed and evidenced.
- [CONFIRM: status updates every 2 hours during active incidents] — kept from v1; sits uneasily with the 4-business-hour acknowledgment target.
- [CONFIRM: quarterly SLA reviews (§10.1, §11.1)] — kept from v1; R5 only prohibits quarterly *vendor* SLA reviews.
- [CONFIRM: error-rate thresholds] — §4.2 "> 1%" kept from v1 while the Monitoring Procedure alarm is ">5% for 5 minutes"; v1 inconsistency, no rule to resolve it.
- [CONFIRM: API Gateway] — §4.1/§4.2 "API Gateway latency/metrics" kept from v1; the Cloud Infrastructure v2 (per R4) refers to Lambda function URLs.
- [CONFIRM: Container Health retention 30 days] — §4.2 kept from v1 (other metrics 90 days).
- R5 (post-check): §10.1 and §11 "Quarterly SLA review" → annual SLA review with the monthly availability record as the continuous input (matches the operating-model calendar).

## Quality sweep (2026-10-31)

- Structure: Roles and responsibilities moved from §11 to §3; §12 Compliance and Audit reduced to §12 "Audit evidence" (§12.2 Regulatory Compliance deleted — three generic bullets with no control of their own); the closing italic line folded into §13.3 Review (keeps the annual review and "maintained in the compliance platform" statements); §8.2 "Zero-Downtime Deployments" retitled "Low-impact deployments" (the bullets minimize impact; they do not claim zero downtime). Sections renumbered 3–15; the §7.1 cross-reference updated to §8.1.
- §3.1 CEO duties: twelve bullets de-duplicated to nine (ownership + documentation merged; customer communication + feedback merged; credit approval + credit processing merged).
- Severity scale: §8.1 table labels "Critical/High/Medium/Low" → "P1 (Critical)/P2 (High)/P3 (Medium)/P4 (Low)", matching the Incident Response Procedure §3 scale (Q2: P1–P4 for incidents); targets unchanged.
- Voice: removed "ensures consistent delivery of services that meet customer expectations", "establishes the framework for"; passive credit-process steps given subjects (the customer, the CEO); "Chief Executive Officer" after first use → "the CEO" ×3; "(if applicable)" → "(where applicable)".
- Consistency: percentages spaced ("99.9 %", "> 1 %", "< 80 %"); "500ms" → "500 ms"; "02:00-06:00" → "02:00–06:00"; "Incident Reporting system" → "incident reporting module of the compliance platform"; headings and table labels to sentence case; blank lines between bullets removed (~75).
- Related documents: all 9 entries exist in the set; unchanged.
- Word count 1491 → 1417.

### New CONFIRM items

- §8.1 "Resolution target 4 hours" for P1 sits next to "acknowledged within 4 business hours" (R5). A 4-hour resolution target is stricter than the acknowledgment target; confirm the resolution column is intended (left unchanged).
- §8.2 "Status updates every 2 hours" (customer-facing) vs Incident Response Procedure "every 30 minutes for P1" (internal cadence). Confirm the two are meant to differ (left unchanged).
- §5.1/§5.2 reference "API Gateway" metrics; the Cloud Infrastructure Security Policy describes CloudFront in front of Lambda function URLs. Confirm the metric source name.

- R4/Q2 (post-sweep, settled from serverless.yml: 'API Gateway not used - using Lambda Function URL + CloudFront'): every 'API Gateway' reference replaced with CloudFront → Lambda function URL / middleware.

## Decisions applied (2026-10-31)

- D9: §9.1 standard maintenance window set to Sunday 07:00–11:00 UTC (02:00–06:00 ET), referencing the Change Management Policy change window
- D10: §8.2 customer status updates every 2 hours kept, with a cross-reference to the 30-minute internal cadence in the Incident Response Procedure
- D13: §4.1 availability calculation stated as measured over all minutes in the month, excluding announced maintenance windows (§4.2)
- D22: author set to "Mo Messidi" (frontmatter and revision history)
- D25: cut §6.2 monthly internal SLA review (section deleted; the monthly availability record in §6.1 remains)

## Decisions applied (2026-10-31, round 2)

- D13b: §6.1 states that the monthly availability record is the scheduled compliance-platform task "Availability record (monthly)" (owner CEO, monthly frequency, covered by the Monday reminder email)
- D12: Security Hub removed — §8.1 P1 paging "Security Hub/SNS paging for critical findings" → SNS paging to the CEO on security-relevant CloudTrail events and CloudWatch alarms

## Decision applied (2026-11-01)

- D26: no Multi-AZ DocumentDB (Mo, 2026-11-01; a standby instance is not worth the cost). Multi-AZ / second-instance / automatic-failover wording replaced by: DocumentDB cluster storage replicated six ways across three availability zones by the service; a single serverless instance re-created automatically after an instance failure (same AZ, best effort), recovered manually into us-east-1b after an outage of us-east-1a (corrected 2026-11-01, D27); point-in-time recovery and automated backups. "DocumentDB backup retention and Multi-AZ" in the configuration-check checklist → "DocumentDB backup retention".
