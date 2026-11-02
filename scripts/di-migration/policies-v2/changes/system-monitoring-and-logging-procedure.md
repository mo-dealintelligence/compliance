# System Monitoring and Logging Procedure — v1.0 → v2.0 change note

Source: `data/nov2025/md/system-monitoring-and-logging-procedure.md`
Output: `policies-v2/system-monitoring-and-logging-procedure.md`

## Frontmatter
- R0: `version` 1.0 → 2.0; `supersedes: "1.0"`; `effective_date` → `"<to be set at publication>"`; `review_date` → `"<one year after effective date>"`; `doc_type` "Policy" → "Procedure" (honest type); dropped export-only `finalized_at` (R6). Kept `author`, `source`, `acknowledgment`.
- R0: sub-headings "## 3.1" etc. corrected to "### 3.1" (numbering artefact); section numbers unchanged.

## Removals / rewordings / additions
- R1: §1 removed "Processing Integrity (PI1.4)" from the TSC mapping (CC6.1, CC7.1, A1.2, C1.1 kept).
- R2: §14 "Chief Information Security Officer", "System Administrator", "Development Team" → single §14.1 CEO (bullets merged; "Support troubleshooting activities" dropped as it only made sense between teams). §14.4 "All Personnel" → §14.2 "All Personnel (including the Go-to-Market Contractor)", reporting to the CEO.
- R2: §8.1 Critical "SNS notification to on-call personnel" → "to the CEO".
- R2: §10.1 "Restricted to authorized security and operations personnel" → "Restricted to the CEO".
- R2: §10.2 removed "Development team for troubleshooting (with approval)"; "Compliance auditors during assessments" → "The external SOC 2 auditor during assessments".
- R2/R5: §15 exception approver "Chief Information Security Officer" → CEO.
- R3/R5: §3.1 CloudTrail row 90 days → 7 years; storage "S3 bucket with KMS encryption, lifecycle to Glacier, Object Lock". All other rows unchanged (CloudWatch 90 d, PropelAuth 30 d).
- R3/R5: §12.3 "SOC 2 requirements (90-day minimum)" → "(90-day minimum for CloudWatch Logs; 7 years for CloudTrail)".
- R4 (EC2/CloudWatch Agent): §5.1 removed "**CloudWatch Agent**: System and application logs from EC2 instances"; lead sentence now "Workloads run on Lambda and Fargate."
- R4 (Route 53 health checks / multi-region): §6.1 "Multi-region health checks via Route 53" → "Route 53 is used for DNS only; the platform runs in a single region (us-east-1) by design, as stated in the Business Continuity Plan".
- R4 (Synthetics): §6.1 "CloudWatch Synthetics canaries shall execute every 5 minutes" → "CloudWatch alarms on API errors and latency (p95 > 2 seconds)"; "Third-party uptime monitoring integration" → "Monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform". §9.2 Availability Reports → same monthly CloudWatch figure. §13.2 "CloudWatch Synthetics: Availability monitoring" → "CloudWatch Alarms: Availability and latency monitoring".
- R4 (cross-account): §5.2 removed "Cross-account log aggregation where applicable".
- R4 (auto-scaling): §4.2 Database CPU action "Auto-scaling trigger" → "SNS notification".
- R4 (Config): §7.3 "AWS Config rules for configuration compliance" → CloudFormation (`serverless deploy`) as the only change path reporting drift + Security Hub configuration checks + scheduled Lambda checks (access review, retention enforcement). §13.1 "AWS Config: Configuration compliance monitoring" → "AWS CloudFormation: Configuration drift reporting via `serverless deploy`". §4.3 removed "Automated remediation workflows for critical findings".
- R4 ("quarterly control testing" / reports): §7.3 "Quarterly compliance reports via the compliance platform" → "The compliance platform as the control register (controls, evidence, tasks), with the monthly recorded review of Security Hub findings".
- R4 (breach-detection Lambda scope): §7.2 trimmed to what the Lambda does per R4 — process Security Hub findings in real time, route to SNS; removed "Correlate security events across multiple sources" and "Initiate automated containment actions where appropriate"; "Generate incident tickets in the compliance platform" → "Support the recording of resulting incidents … by the CEO". §13.3 Lambda Functions → "Breach detection and scheduled checks (access review, retention enforcement)".
- R4 (S3 security-log archive): §5.3 "Log forwarding to immutable storage for compliance retention" → "CloudTrail bucket lifecycle policy and S3 Object Lock for 7-year compliance retention"; §13.3 S3 Buckets → "Long-term CloudTrail log archival (7 years, Object Lock)".
- R4 (runbooks, 15-minute response): §8.3 "Escalation Procedures" (escalate after 15 min / 1 h / 4 h; "paths documented in runbooks") → "Response Targets": real-time SNS, P1 acknowledged by the CEO within 4 business hours per the Incident Response Procedure, CEO as incident commander, medium/low in the monthly review. §4.2 "Escalation" column (Immediate / 15 minutes / 30 minutes / 1 hour) removed; replaced by a sentence pointing to §8.3. The two broken alarm tables merged into one.
- R5 (no daily reviews): §9.1 "Daily review of security alerts and anomalies" → "Real-time SNS alerting on critical security alerts and anomalies, with a monthly recorded review of all security findings". §14 "Perform daily log reviews" → "Perform the monthly recorded review of security findings and alerts". §8.1 Medium "Daily digest of events" and Low "Weekly summary reports" → "Included in the monthly recorded review"; High "Email notification within 15 minutes" → "SNS notification to the CEO".
- R5 (Security Hub monthly + real-time): §4.3 added "Critical findings alert in real time; all Security Hub findings are reviewed monthly and the review is recorded in the compliance platform".
- R5 (p95 > 2 s): §4.2 added an "API Latency | p95 > 2 seconds | SNS notification" row (the alarm R4/R5 require; v1 had no latency alarm in this table).
- R5 (incident evidence 7 years): §9.3 "Extended log retention for security incidents (up to 1 year)" → "Retention of logs and evidence relating to security incidents for 7 years".
- R5 (MFA wording): §10.1 "Authenticated via PropelAuth with MFA enforcement" → "Authenticated to the AWS console and CLI with MFA enforced" (monitoring systems are AWS; never "PropelAuth MFA").
- R8: restored real bullet lists where v1 collapsed them (§2, §3.2, §5.2, §6.3, §9.3, §12.1); split run-ons in §5.3 ("…Standard IAM policies…") and §11.1 ("…change requests Validate…"); removed stray `<u>` fragments.
- R6: §16 split the merged "SLA Management Policy Data Retention and Disposal Policy" item into two.
- R0: added §18 Revision history.
- Kept verbatim (no rule applies): §3.2, §3.3, §4.1, §4.2 thresholds, §6.2, §6.3 (quarterly capacity reviews), §7.1, §8.2, §9.1 weekly/monthly/quarterly items, §9.2 Executive Dashboard and Compliance Reports, §11.x, §12.1–12.2, §13.2 X-Ray/Container Insights, §13.3 EventBridge, §17.

## CONFIRM
- [CONFIRM: API Gateway] — §3.1 row "API Gateway | Request/response logs" and §6.2 "API Gateway request rates and throttling" kept from v1; the Cloud Infrastructure v2 (per R4) says origins are Lambda function URLs. Confirm which is deployed and align.
- [CONFIRM: Security Hub standards] — §4.3 "CIS AWS Foundations Benchmark adherence" and "Custom security standards for SOC 2 requirements" kept from v1; R4 only cites Foundational Security Best Practices. Confirm CIS is enabled and whether any custom standard exists.
- [CONFIRM: S3 MFA delete] — §5.3 "S3 bucket versioning and MFA delete protection" kept from v1; confirm MFA delete is actually enabled on the CloudTrail bucket.
- [CONFIRM: Security Hub finding retention] — §3.1 "90 days | Security Hub console" kept (native retention); confirm acceptable given the 7-year incident-evidence rule (findings tied to incidents are exported to the compliance platform).
- [CONFIRM: EventBridge] — §13.3 "EventBridge: Event-driven automation" kept verbatim; confirm it is what schedules the Lambda checks.

## Quality sweep (2026-10-31)

- Structure: Roles and responsibilities moved from §14 to §3 (Q3 order); §12 Compliance and Audit Support dissolved — §12.1 Evidence Collection and §12.2 Audit Trail Requirements deleted (generic, no control of their own), §12.3 Retention Compliance reduced to one sentence (§12.3) pointing to the Data Retention and Disposal Policy with the three retention values already stated in §4.1; §11.2 Incident Response Integration deleted (restated §8–§10); §11.1 Change Management Integration condensed to one paragraph; §15 Exceptions and §17 Review and Updates merged into §14 "Exceptions and review" so Related documents precedes Revision history. Sections renumbered 3–16; the §8.3 cross-reference updated to §9.3.
- §3.1 CEO duties: eleven bullets de-duplicated to eight ("Ensure compliance with SOC 2 requirements" merged into "maintains the SOC 2 evidence"; "Implement application-level logging" and "Maintain logging standards in code" merged).
- Voice: removed "shall" ×24; removed "comprehensive" ×3; "Reference: X for detailed …" ×6 → plain sentences; "Monitor and track:" / "Maintain forensic readiness through:" imperative lead-ins → declarative with a subject; "where applicable" → "where one exists"; §11.2 "Temporary access with automatic expiration" (a condition listed as a grantee) folded into the lead sentence.
- Consistency: "AWS CloudWatch/CloudTrail/Security Hub/CloudFormation" → bare service names; "real-time" (adverb) → "real time"; "5%/1%/80%/20%/99.9%" → spaced percent; "Incident Reporting system" → "incident reporting module of the compliance platform"; "Risk Assessment module" → "risk assessment module"; headings to sentence case; blank lines between bullets removed (~120).
- Related documents: added API Security and Rate Limiting Standard (referenced in §4.3); all entries exist in the set.
- Word count 2227 → 1980.

### New CONFIRM items

- §4.1 lists "API Gateway" as a log source and §7.2 monitors "API Gateway request rates and throttling", while the Cloud Infrastructure Security Policy describes CloudFront with origin access restricted to Lambda function URLs. Confirm whether API Gateway is in the architecture; if not, these rows should name the Lambda function URL / CloudFront logs.
- §4.1 Security Hub findings retained "90 days" here; the Data Retention and Disposal Policy §5.1 says 7 years (already a CONFIRM there). The two should agree once the mechanism is confirmed.
- §13.2 "AWS X-Ray: distributed tracing (when implemented)" is a hedge carried from v1; confirm whether X-Ray is in use, otherwise drop the line.
- §10.1 weekly performance trend analysis, monthly access pattern review, and quarterly security posture assessment are cadences carried from v1; confirm a record exists for each.

- R4/Q2 (post-sweep, settled from serverless.yml: 'API Gateway not used - using Lambda Function URL + CloudFront'): every 'API Gateway' reference replaced with CloudFront → Lambda function URL / middleware.

## Decisions applied (2026-10-31)

- D3: removed §4.1 DocumentDB database audit logs row; §6.3 "S3 bucket versioning and MFA delete protection" reduced to "S3 bucket versioning"
- D22: author set to "Mo Messidi" (frontmatter and revision history)
- D25: cut §7.3 quarterly capacity review (section deleted); cut §10.1 weekly performance trend analysis, §10.1 monthly access-pattern review, §10.1 quarterly security-posture assessment; cut §10.2 monthly executive dashboard and quarterly SOC 2 evidence-collection reports; cut §14.1 quarterly exception review

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed — §1 scope names the configuration-check and breach-detection Lambda functions instead of Security Hub; §4.1 retention table row "Security Hub findings, 90 days, console" → configuration-check records, 7 years, compliance platform (matches the Data Retention and Disposal Policy); §5.3 retitled "Configuration checks and security event alerting" and rewritten as the monthly configuration-check Lambda with the fixed checklist and dated pass/fail record, plus the CloudTrail → EventBridge → breach-detection Lambda → SNS real-time path (FSBP / CIS Benchmark / custom standards claims dropped); §3 CEO duty and §10.1 monthly review now name the configuration-check record and security alerts; §8.2 breach-detection Lambda triggered by EventBridge on CloudTrail events; §8.3 "Security Hub configuration checks and compliance scores" folded into the scheduled Lambda checks and the compliance-platform line now holds the monthly configuration-check record; §13.1 stack lists the configuration-check and breach-detection Lambdas; §13.3 Lambda list adds the monthly configuration check

## Decision applied (2026-11-01)

- D26: no Multi-AZ DocumentDB (Mo, 2026-11-01; a standby instance is not worth the cost). Multi-AZ / second-instance / automatic-failover wording replaced by: DocumentDB cluster storage replicated six ways across three availability zones by the service; a single serverless instance re-created automatically after an instance failure (same AZ, best effort), recovered manually into us-east-1b after an outage of us-east-1a (corrected 2026-11-01, D27); point-in-time recovery and automated backups. "DocumentDB backup retention and Multi-AZ" in the configuration-check checklist → "DocumentDB backup retention".
