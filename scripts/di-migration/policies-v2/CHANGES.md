# Policy set v2 — change log and open confirmations (2026-10-31)

Produced per RULEBOOK.md from the v1 markdown in data/markdown/ and data/nov2025/md/. Per-document notes are in changes/. Status: **drafts for Mo's review — not yet published to the compliance platform.** Lint: `python3 policies-v2/check.py`.

## Documents

| Document | v1 → v2 | Note |
|---|---|---|
| acceptable-use-policy | 2028 words | changes/acceptable-use-policy.md |
| access-control-and-authentication-policy | 1824 words | changes/access-control-and-authentication-policy.md |
| api-security-and-rate-limiting-standard | 2747 words | changes/api-security-and-rate-limiting-standard.md |
| business-continuity-plan | 1902 words | changes/business-continuity-plan.md |
| change-management-policy | 1639 words | changes/change-management-policy.md |
| cloud-infrastructure-security-policy | 2175 words | changes/cloud-infrastructure-security-policy.md |
| code-of-conduct | 922 words | changes/code-of-conduct.md |
| data-classification-and-handling-standard | 2138 words | changes/data-classification-and-handling-standard.md |
| data-classification-policy | merged | data-classification-policy.MERGED.md |
| data-retention-and-disposal-policy | 2747 words | changes/data-retention-and-disposal-policy.md |
| data-subject-rights-request-procedure | 1839 words | changes/data-subject-rights-request-procedure.md |
| encryption-and-cryptographic-controls-standard | 1923 words | changes/encryption-and-cryptographic-controls-standard.md |
| incident-response-procedure | 2112 words | changes/incident-response-procedure.md |
| information-security-policy | 1862 words | changes/information-security-policy.md |
| penetration-testing-and-security-assessment-procedure | 1775 words | changes/penetration-testing-and-security-assessment-procedure.md |
| privacy-notice-and-data-processing-agreement-template | 2097 words | changes/privacy-notice-and-data-processing-agreement-template.md |
| risk-assessment-procedure | 1724 words | changes/risk-assessment-procedure.md |
| secure-software-development-lifecycle-sdlc-standard | 1813 words | changes/secure-software-development-lifecycle-sdlc-standard.md |
| security-awareness-training-program | 545 words | changes/security-awareness-training-program.md |
| service-level-agreement-sla-management-policy | 1494 words | changes/service-level-agreement-sla-management-policy.md |
| system-description-v2 | 11055 words | changes/system-description.md |
| system-monitoring-and-logging-procedure | 2227 words | changes/system-monitoring-and-logging-procedure.md |
| third-party-integration-security-guidelines | merged | third-party-integration-security-guidelines.MERGED.md |
| vendor-management-policy | 1684 words | changes/vendor-management-policy.md |
| vulnerability-management-procedure | 1800 words | changes/vulnerability-management-procedure.md |

## Open CONFIRM items (consolidated from the change notes)

### acceptable-use-policy
- §16 Revision history: v1 export only shows version 1.1 dated November 13, 2025; the 1.0 row's date and the 1.1 summary ("Audited release") are placeholders — confirm or delete the 1.0 row.
- §3 "Authorized User … through PropelAuth authentication" kept from v1; internal personnel authenticate through Google Workspace, so confirm whether this definition should mention both.
- §7.1 "device agent of the compliance platform where deployed" — confirm the Comp device agent is actually deployed on the CEO's and the Contractor's machines; if not, drop the bullet.
- §11.1 "Anonymous reporting channels if available" kept from v1 — confirm whether any such channel exists; delete if not.
- §11.3 "Investigated within 24 hours of report" kept from v1 — not in R5; confirm this is consistent with the Incident Response Procedure's P1 4-business-hour acknowledgment.
- §12.1 "maximum 90 days" exception window kept from v1 — confirm it matches the Information Security Policy exception clause.
- R3 staging: separate account vs same account (not written into the policy).

### access-control-and-authentication-policy
- §6.3 "AWS Organizations SCPs limiting high-risk actions" kept verbatim (v1 claim). R3 says to say nothing about accounts; SCPs imply an AWS Organization. Confirm SCPs exist, or delete the bullet.
- §5.2.1 "Developer" and "Read-Only" RBAC roles kept as system roles even though only the CEO holds production access; confirm these roles exist in PropelAuth/IAM or collapse to Administrator + Customer.
- §5.3.3 "Service accounts rotated quarterly" kept; R3 describes Secrets Manager rotation on the DocumentDB credential and API-key rotation per calendar — confirm quarterly is the calendar value.
- §8.1 "Monthly review of security group rules and network ACLs" kept; confirm a monthly record exists in the compliance platform.
- §15 approval date: `[CONFIRM: date]`.

### api-security-and-rate-limiting-standard
- API Gateway vs Lambda function URLs: v1 states token validation, JSON schema validation and configuration logging "at API Gateway level"; the R4 WAF row says origin access is restricted to "the Lambda function URLs". v1 API Gateway wording kept unchanged; confirm which front door is in production and whether API Gateway wording should become Lambda function URLs.
- Burst capacity of 200 (2x sustained) retained from v1 for the single tier; confirm the middleware actually implements a burst allowance, otherwise drop the Burst Capacity column and the "2x" bullet.
- "Provisioned concurrency for critical endpoints" (§4.2) and "Failover to cached JWT validation during PropelAuth outages" (§7.1) retained from v1 — not in the R4 removal list; confirm they exist.
- §13.1 SLO latency changed from 500 ms to 2 s to match the single R5 value; confirm the intended p95 objective.
- Section renumbering (new §8 pushes v1 §8–14 to §9–15): other v2 documents that cite this standard by section number should be checked.

### business-continuity-plan
- Appendix A: CEO phone and email for the emergency contact list (`[CONFIRM: phone]`, `[CONFIRM: email]`).
- §4.1 Authentication Services row (RTO 1 hour / RPO 30 minutes): kept from v1 but authentication is hosted by PropelAuth — confirm these values are meant to cover the platform's PropelAuth integration only.
- §6.2 "Activate CloudFront failover origins if configured" and §7.3 "Emergency bypass for critical operations (with audit logging)": v1 claims not covered by any rule; confirm they exist or strike.
- §8.1 "Failover Testing — Semi-annually — AZ failover procedures": kept from v1; confirm a DocumentDB failover test is actually performed semi-annually.

### change-management-policy
- §5.5 "Update configuration management database" kept verbatim; no CMDB is named anywhere in the rulebook. Confirm whether this should read "Confirm the CloudFormation stack reflects the deployed configuration" or be deleted.
- §5.2 Standard change "Automated dependency updates proposed by GitHub Dependabot that pass all required CI status checks" is my substitution for SSM patching; confirm Dependabot PRs are treated as pre-approved standard changes (otherwise move them to Normal).
- §3 Change Window "2:00 AM - 6:00 AM EST" and §5.4 "minimum 72 hours" customer notice kept verbatim; confirm these are still operated.
- Title/doc_type: brief said "PR + CI-gate standard"; kept title "Change Management Policy" and `doc_type: Policy` because cross-references use that name. Confirm if a rename to "Change Management Standard" is wanted (would require updating references in every other document).
- R3 note for CHANGES only: `[CONFIRM: separate account vs same account]` for the staging stage.

### cloud-infrastructure-security-policy
- [CONFIRM: API Gateway vs Lambda function URLs] — v1 §5.4.2 heading "API Gateway Security" and the R4-mandated WAF replacement text "origin access restricted to the Lambda function URLs" now sit in the same section. Heading kept as v1 (API Gateway itself is not in the R4 removal list). Confirm which is in the stack and align the heading/wording.
- [CONFIRM: separate account vs same account] — staging stage described without any account language per R3.
- [CONFIRM: VPC Flow Logs, DocumentDB audit logging, ECS network policies, AWS Well-Architected reviews] — kept verbatim from v1 because no rule removes them; worth checking they are actually enabled.

### code-of-conduct
- "Anonymous reporting channels when available" kept verbatim; confirm whether any anonymous channel exists or delete the bullet.
- "Suspension with or without pay" and "Performance improvement plans" kept as v1 disciplinary steps; confirm they are meaningful for a contractor relationship or trim to warnings / termination of contract / legal action.
- Revision history v1 date taken from the v1 `finalized_at` (November 30, 2025) because v1 `effective_date` was "N/A"; confirm.

### data-classification-and-handling-standard
- API keys moved to Restricted (v1 Standard had them Confidential; Policy had them Restricted). Confirm Restricted is the intended tier for customer-issued API keys as well as internal ones.
- §2.1.4 Restricted handling "Access limited to the CEO" — stated from R2 (only the CEO has production/secret access). Confirm no other access path to Secrets Manager/KMS exists (e.g. a CI deploy role) that should be described.
- §4.1 names the `di-backend-api-prod` stack as the location of Confidential/Restricted data (taken from the Policy §2.1.3). Confirm there is no second stack or bucket outside it holding Confidential data.
- §10.1 "Exceptions reviewed quarterly" kept verbatim; confirm a quarterly exception review is recorded in the compliance platform.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

### data-classification-policy
- Retire the Data Classification Policy record in the compliance platform and re-point any control/evidence that cites it to the Data Classification and Handling Standard v2.0.
- The Policy's §7.1 sub-processor table (AWS, PropelAuth only) is not carried into the Standard; the Standard now points to the Vendor Management Policy list (AWS, PropelAuth, Google Workspace, GitHub, Resend, compliance platform hosting). Confirm that list is final before the Standard is published.

### data-retention-and-disposal-policy
- §2.1 Security Hub Findings "7 years": Security Hub natively retains findings for 90 days; confirm how (or whether) findings are retained for 7 years, or change the row to 90 days with review records kept in the compliance platform. Marked `[CONFIRM: …]` in the table.
- §4.2 new "Customer Account Data Expiration" row: confirm the retention enforcement Lambda actually deletes customer account data at relationship end + 24 months (R5 says it does; the row was not in v1).
- §2.1 Authentication Records "2 years": kept from v1; these records live in PropelAuth — confirm the value and the mechanism.
- §2.1 Consent Records "Duration of processing + 7 years" and the monthly "Consent Record Review" EventBridge process in §4.2: kept from v1; confirm these exist (the Consent Management Procedure referenced elsewhere does not).
- §3.2.4 "Lambda function identifies and deletes expired manual snapshots": kept from v1; confirm this Lambda exists.
- §3.2.5 ECR "untagged images after 14 days": kept from v1; confirm the lifecycle policy value.
- §7.1 targets (">99%", "0 records") and §7.3 monthly retention compliance reports: kept from v1; confirm the monthly report is actually produced.
- Revision history: v1 body table dated the policy November 13, 2025 (1.0) and February 2, 2026 (2.0) while the frontmatter was 1.0 finalized February 2, 2026 — confirm the 1.0 date to show.

### data-subject-rights-request-procedure
- Controller/processor framing in §1 (inline `[CONFIRM]`): v1 only implied it via §6.2. Confirm the wording "controller for the business contact information it compiles and delivers; processor for data customers upload to or hold within their own accounts" and remove the marker.
- Article 18 (restriction of processing) now has no row in §3.1 and no procedure section, because the brief said to delete the 72-hour restriction row. GDPR still grants the right; if Mo wants it covered, add a "Restriction (Article 18) | 30 days" row and a manual step (CEO excludes the record from delivery until resolved).
- §4.1 "Secondary Channel: Authenticated customer portal via PropelAuth" kept verbatim — confirm a DSR submission path actually exists in the portal; otherwise delete the channel.
- §5.2 "Clear CloudWatch logs where permissible" kept — confirm log entries are ever cleared manually, or reword to "logs expire under the 90-day retention".
- HubSpot is named as a location of contact records (from the R4 runbook row) but is not in the R7 sub-processor list; confirm whether HubSpot should be added to the Vendor Management sub-processor list.
- §10.1 KPI targets (<20 days average, >95 % on-time, <5 % denial, <10 % extension; monthly/quarterly measurement) kept verbatim — confirm these are tracked in the compliance platform or drop the table.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

### encryption-and-cryptographic-controls-standard
- [CONFIRM: KMS key inventory] — §6.1 keeps v1's key list (Production Data key with DocumentDB/S3/Lambda sub-keys, Backup key, Audit Log key). Confirm which customer-managed keys actually exist in us-east-1 and whether backups use the DocumentDB key (as §4.1 states) rather than a separate Backup key.
- [CONFIRM: JWT signing key rotation 180 days] — v1 claim about PropelAuth; cannot be verified from the environment. Consider "Managed by PropelAuth" without a number.
- [CONFIRM: Lambda env-var secrets rotated quarterly] — §4.3 kept from v1; not among the R3/R5 rotation facts.
- [CONFIRM: monthly TLS configuration scans / quarterly encryption audit reports / semi-annual key rotation audits] — §11.1 and §16.1 kept from v1; confirm these are evidenced in the compliance platform.
- [CONFIRM: VPC endpoints] — §5.2 "VPC endpoints for AWS service communications" kept from v1; confirm endpoints exist in the stack.
- [CONFIRM: separate account vs same account] — staging described only as "the staging stage" per R3.

### incident-response-procedure
- §7.1 acknowledgement targets for P2 (1 business day), P3 (5 business days) and P4 (monthly review): only the P1 value (4 business hours) is given by the rulebook; the others are chosen to sit below P1 and need Mo's confirmation.
- §10.1 MTTC "< 2 hours from acknowledgement": v1 said "< 2 hours" with no reference point; confirm the measurement basis.
- §8.3 "S3 bucket with versioning and MFA delete": v1 claim not covered by any rule; confirm the evidence bucket actually has MFA delete enabled.
- §9.2 "Monthly update of contact lists and escalation paths": v1 cadence kept; confirm this is actually performed monthly.

### information-security-policy
- §5.3 "24-month retention period for active leads" kept verbatim. R5 sets customer account data retention at "relationship + 24 months"; confirm the lead-level 24-month figure is still what the retention Lambda enforces, or reword to the R5 phrasing.
- §5.5 "24/7 CloudWatch monitoring" kept (it describes automated monitoring, not a staffed response); confirm this is acceptable alongside the R5 "no 24/7 response" decision.
- §6.3 "Quarterly internal compliance assessments" kept verbatim; confirm a quarterly internal assessment is actually recorded in the compliance platform.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

### penetration-testing-and-security-assessment-procedure
- §2 "Quarterly automated security assessments" and §5.2 heading kept from v1 — confirm a quarterly assessment record exists in the compliance platform alongside the monthly Security Hub review.
- §5.1 "Conducted annually in Q3" — confirm Q3 is still the intended window.
- §6.1 "Professional liability insurance minimum $1 million coverage" kept from v1 — confirm this vendor requirement is still wanted.
- §7.1 "IAM access analyzer findings" kept from v1 — confirm IAM Access Analyzer is enabled.
- §8 "Findings logged in GitHub Issues with security labels" kept from v1 — confirm pentest findings are logged in GitHub Issues rather than only in the compliance platform.
- §10.3 "Annual attestation of security assessment completion" kept from v1 — confirm an attestation is produced.
- R3 staging: separate account vs same account (not written into the policy).

### privacy-notice-and-data-processing-agreement-template
- §3.1.4 / §4.1.5 sub-processor purposes (Google Workspace = email/documents/sign-in, GitHub = code hosting/CI, Resend = transactional email) are inferred from the rulebook (R4, R7, R8), not from v1. Confirm each one actually touches customer personal data before it goes into a customer-facing DPA; GitHub in particular may not process personal data at all.
- §4.1.7 "Quarterly security assessments" and "Third-party security certifications" kept verbatim — confirm Deal Intelligence is willing to offer a quarterly assessment to customers (R5 sets vendor reviews annual) and whether any certification beyond the SOC 2 report exists; otherwise delete both bullets.
- §4.1.3 and §10.2 "Quarterly risk/privacy assessments via the compliance platform Risk Assessment module" kept verbatim — confirm quarterly is what is recorded.
- §10.2 "Semi-annual consent audit" kept verbatim — confirm it is performed.
- §4.1 DPA parties keep v1's "Deal Intelligence LLC ('Processor') and [Customer Name] ('Controller')". This is correct for customer-uploaded data; for compiled business-contact data Deal Intelligence is a controller (see DSR Procedure §1). Confirm whether a controller-to-controller clause (SCC Module 1 is already listed in §7.1) should be added to the DPA body.
- §3.1.1 "[Company Address]" and §5.2 "[Name] / [Number]" left as template fields by design.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

### risk-assessment-procedure
- §5.3 key-risk table scores (inherent/residual values) are carried over from v1 unchanged; confirm they match the current register in the compliance platform.
- §6.1 seven-week annual assessment timeline kept from v1; confirm it reflects how the annual assessment is actually run.
- §6.2 "Weekly: CloudWatch metrics analysis" kept from v1 (not a daily review, so not struck by R5); confirm it is performed weekly.

### secure-software-development-lifecycle-sdlc-standard
- §5.2.1 Node.js/TypeScript row: is there any Node/TypeScript code in `di-backend-api` or the frontend, and is ESLint run anywhere? If not, delete the row.
- §5.2.1 CloudFormation row: v1 cited cfn-lint / cfn-nag; replaced with CloudFormation + Security Hub checks. Confirm neither tool is actually in CI.
- §4.1 keeps the name "Mo Messidi" as in v1; confirm whether v2 documents should name the CEO or use the title only.
- §5.4.1 "approved via the GitHub Actions workflow": confirm a manual approval gate (environment protection rule) exists on the production deploy job; otherwise reduce to "deployed from a green CI run on `main`".
- §5.5.2 "Container vulnerability scans shall be reviewed weekly" kept from v1 — confirm this cadence is actually recorded.
- R3 staging: separate account vs same account (not written into the policy).

### security-awareness-training-program
- The compliance platform issues a completion certificate for the security-awareness training (used as the evidence statement in §4).
- Contractor acknowledgment cadence: v2 says "at onboarding and annually" for the AUP/confidentiality acknowledgment; confirm this matches the Acceptable Use Policy v2 and the Code of Conduct annual acknowledgment (R6).
- Onboarding training "before being granted access to company data" — v1 allowed 5 business days after provisioning; confirm the stricter gating is the intended practice.

### service-level-agreement-sla-management-policy
- [CONFIRM: Data Processing Accuracy 99.5 % and Lead Delivery < 24 hours] — kept as customer commitments (R1 only strips the PI criteria mapping); confirm they are measured ("Validated records / Total processed records") or drop the row.
- [CONFIRM: weekly → monthly internal SLA review] — v1 said weekly; changed to monthly to align with the R4 monthly availability record. Revert if weekly reviews are actually performed and evidenced.
- [CONFIRM: status updates every 2 hours during active incidents] — kept from v1; sits uneasily with the 4-business-hour acknowledgment target.
- [CONFIRM: quarterly SLA reviews (§10.1, §11.1)] — kept from v1; R5 only prohibits quarterly *vendor* SLA reviews.
- [CONFIRM: error-rate thresholds] — §4.2 "> 1%" kept from v1 while the Monitoring Procedure alarm is ">5% for 5 minutes"; v1 inconsistency, no rule to resolve it.
- [CONFIRM: API Gateway] — §4.1/§4.2 "API Gateway latency/metrics" kept from v1; the Cloud Infrastructure v2 (per R4) refers to Lambda function URLs.
- [CONFIRM: Container Health retention 30 days] — §4.2 kept from v1 (other metrics 90 days).
- R5 (post-check): §10.1 and §11 "Quarterly SLA review" → annual SLA review with the monthly availability record as the continuous input (matches the operating-model calendar).

### system-description
- `[CONFIRM: as-of date]`, `[CONFIRM: period start]`, `[CONFIRM: period end]` — header, Section 7, Management's Assertion (a, b, c).
- `[CONFIRM: name, title, date]` — Management's Assertion signatory.
- `[CONFIRM: no significant incidents in the period]` — Section 7.
- `[CONFIRM: that Resend sends only transactional notifications and that no lead records are included in message bodies]` — Section 3, Other vendors.
- `[CONFIRM: that the compliance platform deployment holds no customer data and that its hosting is within the in-scope AWS account]` — Section 3, Other vendors.
- `[CONFIRM: whether any CRM or notification vendor receives customer data in a way that would require listing as a sub-processor]` — Section 3 (HubSpot / Slack).
- `[CONFIRM: whether pre-commit hooks are also configured locally]` — Section 5, Software.
- `[CONFIRM: field-level encryption for sensitive attributes, as stated in v1]` — Section 5, Data; and `[CONFIRM: field-level encryption for sensitive personal information]` — Section 6, Control activities. If not implemented, delete both.
- `[CONFIRM: final v2 document inventory and count at publication]` — Section 5, In-scope documents table.
- `[CONFIRM: separate account vs same account]` for the staging stage — tracked in this note only (R3); the document makes no account claim.
- Figure 1 — the network diagram must be exported from the compliance platform and inserted at the Figure 1 placeholder in Section 5 before publication.

### system-monitoring-and-logging-procedure
- [CONFIRM: API Gateway] — §3.1 row "API Gateway | Request/response logs" and §6.2 "API Gateway request rates and throttling" kept from v1; the Cloud Infrastructure v2 (per R4) says origins are Lambda function URLs. Confirm which is deployed and align.
- [CONFIRM: Security Hub standards] — §4.3 "CIS AWS Foundations Benchmark adherence" and "Custom security standards for SOC 2 requirements" kept from v1; R4 only cites Foundational Security Best Practices. Confirm CIS is enabled and whether any custom standard exists.
- [CONFIRM: S3 MFA delete] — §5.3 "S3 bucket versioning and MFA delete protection" kept from v1; confirm MFA delete is actually enabled on the CloudTrail bucket.
- [CONFIRM: Security Hub finding retention] — §3.1 "90 days | Security Hub console" kept (native retention); confirm acceptable given the 7-year incident-evidence rule (findings tied to incidents are exported to the compliance platform).
- [CONFIRM: EventBridge] — §13.3 "EventBridge: Event-driven automation" kept verbatim; confirm it is what schedules the Lambda checks.

### third-party-integration-security-guidelines
- Other v2 documents that still list "Third-Party Integration Security Guidelines" in their Related Documents (v1 Security Awareness Training Program, Vendor Management Policy, API Security Standard did; others may) need the reference repointed to API Security and Rate Limiting Standard §8 or Vendor Management Policy.

### vendor-management-policy
- Approval date for the CEO signature row.
- Vendor-inbound breach notification: v1 required vendors to notify within 24 hours (§5.3 table, §6.1, §9.1). Reworded to "contractual breach notification terms that allow Deal Intelligence to meet its 48-hour customer commitment" because the R5 breach-notification values are 48 h/72 h and the hyperscale sub-processors' DPAs do not commit to 24 h. Confirm wording, or restore 24 h if the DPAs actually say so.
- Sub-processor service descriptions (Google Workspace = email/SSO/documents; GitHub = source hosting and CI; Resend = transactional email) are inferred from the rulebook and the other policies; confirm they match the customer-facing sub-processor list.
- §7.3 vendor risk review changed from quarterly to annual to match R5; confirm the Risk Assessment Procedure v2 does not still say quarterly for vendor risks.
- §13 "Reviewed quarterly for continued necessity" (exception review cadence) kept from v1 — not addressed by R5; confirm.

### vulnerability-management-procedure
- §4.1.1 v1 claimed "weekly re-scans of production images" and automatic reporting to Security Hub. Both dropped; confirm ECR continuous scanning is not enabled (if it is, restore the re-scan claim).
- §4.1.3 "Lambda Layer Analysis: Quarterly review of Lambda layer dependencies" kept from v1 — confirm Lambda layers are in use and the quarterly review is recorded.
- §6.1 step 2 "severity assignment within 4 hours" and §6.2 "isolated within 2 hours" kept from v1 — not in R5; confirm these clocks are intended.
- §9.1 "Builds fail if Critical vulnerabilities detected" — confirm the Trivy step in CI is configured to fail on CRITICAL.
- §9.2 "Container Isolation: Network policies enforce container segmentation" kept from v1 — confirm this maps to security groups on the Fargate tasks.
- §15 "Regular briefings on emerging vulnerability trends" kept from v1 — borderline under R4 (newsletters removed); delete if no evidence exists.
- R3 staging: separate account vs same account (not written into the policy).

## 2026-11-01 — D26: no Multi-AZ DocumentDB

Applied by `scratch/no-multi-az-2026-11-01/apply.py`. Edited: business-continuity-plan, cloud-infrastructure-security-policy, incident-response-procedure, information-security-policy, risk-assessment-procedure, service-level-agreement-sla-management-policy, system-monitoring-and-logging-procedure, penetration-testing-and-security-assessment-procedure, vulnerability-management-procedure, system-description-v2; RULEBOOK (R3 bullet removed, R4 row added), check.py (new R4 patterns); controls-v2.json (5 control notes), risks-v2.json (2 treatments), tasks-v2.json (2 evidence descriptions), management-meeting-minutes-2026-10-31 (correction note, row kept); docs/05, docs/09 (§H1 row withdrawn, §H2 row added). The earlier open items on BCP "AZ failover testing" are moot: there is no failover to test; the quarterly restore test covers recovery.
