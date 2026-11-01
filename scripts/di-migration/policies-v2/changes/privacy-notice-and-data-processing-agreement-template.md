# Change note — privacy-notice-and-data-processing-agreement-template (v1.0 → v2.0)

- R0/R6: frontmatter `doc_type` "Policy" → "Template", `acknowledgment` "Explicit" → "None", `version` 1.0 → 2.0, `effective_date` / `review_date` set to publication placeholders, added `supersedes: "1.0"`; dropped the v1 `finalized_at` export stamp. Title already says "Template"; `[Customer Name]`-style fields kept.
- R0: added §14 Revision history.
- R0/R8: restored run-on bullets into real lists (§2, §3.1.2, §3.1.4, §3.1.5, §3.1.7, §4.1.2, §8.1); removed `<u>` artefacts; §8.1 consent checkboxes split onto separate lines.
- R1: §1 "ensures compliance with the GDPR, CCPA, and SOC 2 Trust Services Criteria for Privacy (P1.1-P8.1)" → "ensures compliance with the GDPR and the CCPA".
- R1: §3.1.7 "Technical and organizational measures per SOC 2 certification" → "covered by our SOC 2 report (Security, Availability and Confidentiality)".
- R1/brief: §4.1.7 "Annual SOC 2 Type II audit reports" → "The Processor's SOC 2 report (Security, Availability and Confidentiality), available on request under NDA".
- R2: §3.1.1 "Data Protection Officer: [Email Address]" → "Data protection contact: Chief Executive Officer"; §5.1 "Contact our Data Protection Officer" → "Contact our Chief Executive Officer"; §5.1 sign-off "Deal Intelligence Security Team" → "Chief Executive Officer, Deal Intelligence LLC"; §5.2 "Data Protection Officer: [Name]" → "Chief Executive Officer: [Name]".
- R5: §3.1.3 Customer Account Management retention "Duration of contract + 7 years" → "Duration of the relationship + 24 months".
- R5: §3.1.5 "Multi-factor authentication" → "Multi-factor authentication for personnel enforced in Google Workspace, GitHub and AWS; customer sign-in through Google Workspace via PropelAuth"; "24/7 security monitoring" → "Security monitoring through CloudWatch alarms and Security Hub, with real-time alerting for critical findings".
- R5: §3.1.6 added "within 30 days (GDPR) or 45 days (CCPA)" to the DSR sentence.
- R5: §3.1.8 "notify affected individuals within 72 hours of discovery" → "notify affected customers within 48 hours of discovery, and the supervisory authority within 72 hours where GDPR applies".
- R5: §4.1.4 "Assist the Controller in responding to data subject requests within 10 business days" → "within the statutory timelines (30 days under GDPR / 45 days under CCPA)".
- R4: §4.1.4 "Enable data deletion and rectification through API endpoints" → "Perform data deletion and rectification per the Data Subject Rights Request Procedure" (manual runbook; no DSR API/automation claim).
- R5: §4.1.6 deleted "Notify the Controller within 24 hours"; "Provide detailed incident information within 48 hours" → "Notify the Controller within 48 hours, with the incident information confirmed at that time"; added "Support the Controller's notification to the supervisory authority within 72 hours where GDPR applies".
- R4: §4.1.9 removed "Insurance requirements per SOC 2 standards" (cyber-insurance claim; SOC 2 has no insurance requirement).
- R7: §2 "Sub-processor agreements with PropelAuth and AWS" → "with the sub-processors listed in the Vendor Management Policy"; §3.1.4 and §4.1.5 sub-processor lists expanded from AWS + PropelAuth to AWS (us-east-1), PropelAuth, Google Workspace (email, documents and personnel sign-in), GitHub (source code hosting and CI), Resend (transactional email delivery), compliance platform (self-hosted on AWS).
- R7: §3.1.4 and §12 "Third-Party Integration Security Guidelines" → "the Integration security section of the API Security and Rate Limiting Standard" / "API Security and Rate Limiting Standard".
- R5: §10.2 "Monthly breach readiness testing" → "Annual tabletop exercise recorded in the compliance platform".
- Kept verbatim (no rule applies): §3.1.2 data lists, §3.1.3 other rows, §3.1.6 rights list, §4.1.1, §4.1.2, §4.1.3 (incl. quarterly risk assessments), §4.1.5 change-notice terms, §4.1.7 other bullets, §4.1.8, §5.1 body, §5.2 fields, §6, §7, §8, §9, §10.1, §10.2 other rows, §11, §13.

## CONFIRM

- §3.1.4 / §4.1.5 sub-processor purposes (Google Workspace = email/documents/sign-in, GitHub = code hosting/CI, Resend = transactional email) are inferred from the rulebook (R4, R7, R8), not from v1. Confirm each one actually touches customer personal data before it goes into a customer-facing DPA; GitHub in particular may not process personal data at all.
- §4.1.7 "Quarterly security assessments" and "Third-party security certifications" kept verbatim — confirm Deal Intelligence is willing to offer a quarterly assessment to customers (R5 sets vendor reviews annual) and whether any certification beyond the SOC 2 report exists; otherwise delete both bullets.
- §4.1.3 and §10.2 "Quarterly risk/privacy assessments via the compliance platform Risk Assessment module" kept verbatim — confirm quarterly is what is recorded.
- §10.2 "Semi-annual consent audit" kept verbatim — confirm it is performed.
- §4.1 DPA parties keep v1's "Deal Intelligence LLC ('Processor') and [Customer Name] ('Controller')". This is correct for customer-uploaded data; for compiled business-contact data Deal Intelligence is a controller (see DSR Procedure §1). Confirm whether a controller-to-controller clause (SCC Module 1 is already listed in §7.1) should be added to the DPA body.
- §3.1.1 "[Company Address]" and §5.2 "[Name] / [Number]" left as template fields by design.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.
