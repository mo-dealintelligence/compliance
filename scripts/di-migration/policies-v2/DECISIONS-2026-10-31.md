# Mo's decisions on the v2 CONFIRM list (2026-10-31, late evening)

Apply these across policies-v2/, scratch/quality-sweep/controls-v2.json and
scratch/quality-sweep/records-v2/. Each is final unless marked OPEN.

## Environment facts
- D1 Staging: ~~same AWS account~~ **superseded by D1b below**.
- D2 KMS: production currently has **one customer-managed key**. Keep the Encryption Standard's key-separation design (data / backup / audit-log keys) as written, and record in docs/05 (environment to-do) that the AWS change is still to be made. Control notes and the system description describe the target design the same way.
- D3 Logging/telemetry claims: **keep VPC Flow Logs only**. Remove IAM Access Analyzer, DocumentDB audit logging, VPC endpoints and S3 MFA-delete wherever they appear.
- D4 Device controls: **drop the compliance-platform device-agent bullet** everywhere. Endpoint control = **FileVault full-disk encryption** (macOS) on personnel devices, plus browser SSO with MFA. State FileVault wherever endpoint encryption is discussed (AUP, Code of Conduct, Access Control, Data Classification, system description).
- D5 Anonymous reporting channel: **none exists** — remove from Code of Conduct, AUP, ethics log. Reporting goes to the CEO by email.
- D6 Ethics/compliance contact: `compliance@dealintelligence.io`.

## Commitments
- D7 Vendor breach notification: "contractual terms that allow Deal Intelligence to meet its 48-hour customer commitment" (no 24 h).
- D8 Remediation clocks: **R5 values only** (24 h exploited/critical, 7 d critical dependency CVE, 30 d high, 90 d medium). Delete the 4-hour triage and 2-hour isolation clocks and the "High within 7 days" in the CEO JD.
- D9 Change window: **07:00–11:00 UTC (02:00–06:00 ET)**.
- D10 Incident communication: SLA policy (customer-facing) = status update every 2 hours for P1; IR procedure (internal) = every 30 minutes. Both stay; cross-reference each other.
- D11 Pentest: annual, "in Q3" kept. Vendor insurance requirement: **drop the $1 million figure**; require "professional liability insurance" without an amount. (Mo's question answered in chat: not a SOC 2 requirement.)
- D12 Security Hub: **OPEN** — Mo wants pros/cons before deciding whether to keep it. Until decided, leave the Security Hub wording as is (monthly reviewed record in the compliance platform; findings retained 90 days natively).
- D13 Availability: **measured monthly over all minutes, excluding announced maintenance windows**; delete "during standard business hours" from the system description.

## Privacy / contracts
- D14 Roles: controller for the business-contact data Deal Intelligence compiles; processor for data a customer uploads or holds in its account. DPA: processor terms for the latter, plus an **independent-controllers clause** for the former.
- D15 Sub-processors (customer-facing list): **AWS and PropelAuth only**. Google Workspace, GitHub, Resend and HubSpot do **not** process customer data and are listed as vendors, not sub-processors; Google sign-in for customers is via PropelAuth (already covered). Remove them from every sub-processor list (DPA, Vendor Management, Data Classification Standard, system description "other vendors" paragraph keeps them as non-subservice vendors).
- D16 DSR table: restore GDPR Art. 18 restriction row, 30 days, with a manual step.

## Records
- D17 "86 % control automation": strike from the CEO job description and the organizational structure. The Q4-2025 minutes and the 2025 CEO evaluation are historical records — **do not edit them**. Instead create a **new** management meeting minutes document dated at creation (not back-dated), version 2.0 of the minutes record for Mo's review, recording: scope change to Security/Availability/Confidentiality, descoping of PI/Privacy controls, policy set v2 program, environment to-dos (D2 KMS, 90-day backups, Multi-AZ, PR/branch protection, staging, secrets rotation, CloudTrail lock, ECR scan-on-push), Security Hub decision pending, compliance platform cut-over. File: scratch/quality-sweep/records-v2/management-meeting-minutes-2026-10-31.md. Attendee: CEO. Mark all dates/decisions `[CONFIRM]` where Mo has not stated them.
- D18 BCP test record: rename to "BCP full test 2026-02-04" (drop "Q1 2025").
- D19 Risk retitled: "OPERATIONAL_PEOPLE-001 Key-person dependency — CEO holds all production access".
- D20 Versioning of records: JDs and organizational structure → v2.0 with supersedes. Minutes (historical), certificates and the ethics log: no version bump; add a one-line "Corrected <date>: …" note instead. New minutes (D17) is its own document.
- D21 CEO named by title only in policies; name appears in signature/approval rows.
- D22 Author field: "Mo Messidi" everywhere.
- D23 Context answers: OPEN (Mo asked what this means — explained in chat). Apply nothing yet.
- D24 Humadroid screenshot on the BCP test record: leave as is.

## Cadences without evidence
- D25 Any review/assessment/audit cadence carried from v1 that has **no automated or scheduled record in docs/11 §2** (weekly performance trend analysis, monthly access-pattern review, quarterly security-posture assessment, monthly TLS scans, quarterly encryption audits, semi-annual key-rotation audit, quarterly Lambda-layer review, monthly consent-record review, monthly retention compliance report, weekly container-scan review, quarterly exception reviews, quarterly internal compliance assessments, monthly SG/NACL review, monthly contact-list update, etc.) is **cut**. What remains is the doc-11 calendar: monthly automated checks + Security Hub record + availability record; quarterly access review, management meeting, risk review, backup-restore test; semi-annual privileged-access audit; annual policy review, training, risk assessment, vendor review, tabletop, pentest, evaluation, inventory refresh. Where a cut leaves a section empty, delete the section. Log each cut in the document's change note.

## Mo's second-round answers (2026-10-31, 22:19)
- D11b Pentest vendor insurance: **remove the insurance requirement entirely** — no insurance claim or requirement anywhere.
- D12 **Security Hub is removed.** Replacement control, to be stated everywhere Security Hub was the mechanism (GuardDuty/AWS Config compensating rows in R4, monitoring, vulnerability management, incident detection, control notes, system description, docs/11 M1/M3):
  "A scheduled configuration-check Lambda runs **monthly** against a fixed checklist (CloudTrail enabled and log-file validation on; no public S3 buckets; no security groups open to 0.0.0.0/0 on administrative ports; root account MFA; IAM password policy; KMS key rotation; ECR scan-on-push; DocumentDB backup retention and Multi-AZ) and posts a dated pass/fail record to the compliance platform. Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time." Vulnerability awareness = ECR scan-on-push + GitHub Dependabot and code scanning + Trivy in CI (unchanged). Environment change: disable Security Hub in the account (Mo runs; saves $5.87/mo) — record in docs/05.
- D13b Availability: monthly, as decided; **a monthly compliance-platform task "Availability record (monthly)" must exist** with the Monday reminder email covering it (task frequency monthly, owner CEO).
- D14 **OPEN** — controller/processor framing needs a proper investigation before Mo decides. Keep the applied text but mark the DSR §1 framing and the DPA §4 preamble / §4.10 independent-controllers clause with `[CONFIRM: D14 open — pending investigation]`.
- D23 Context answers: delete the duplicate "How many employees" row; sign-in answer = "Google Workspace SSO and email/password, both with 2FA".

## Round 3 (2026-10-31, 23:22)
- D14 **closed**: two-flow framing adopted (independent controller for compiled data; processor for customer-uploaded data). CCPA: Deal Intelligence does not meet the business thresholds (Mo: well under the 50 %-of-revenue test for California personal information); no data-broker registration. Applied to the DSR procedure and the DPA template.
- D17/minutes: confirmed; markers resolved with the audited current-state facts, re-submitted.

## Round 4 (2026-10-31, 23:31)
- D1b Staging: **separate AWS account** in the same AWS Organization (supersedes D1). Reasons: hard isolation of prod data/keys/IAM from a single-operator deploy mistake; matches the "distinct accounts" claim the policies originally made and what an auditor expects for CC6.1/CC8.1; own KMS keys and secrets by construction; the NAT is a t3.micro and DocumentDB is serverless with a small synthetic dataset, so the cost is ~$15-25/mo rather than the ~$30-40 first estimated. The staging account is **outside the SOC 2 system boundary**; the monthly configuration-check Lambda runs in the production account only.
- Wording applied to 9 documents: "staging stage of the same stack" -> a staging environment in a separate AWS account. Environment work: create the member account, SSO/role, CloudTrail trail, cross-account ECR pull, parameterise the 11 hardcoded `*-production-*` names (docs/05).

## 2026-11-01
- D26 **No Multi-AZ DocumentDB** (supersedes the Multi-AZ item in RULEBOOK R3, the environment to-do in the 2026-10-31 minutes §4.4, and "and Multi-AZ" in the D12 configuration-check checklist). Production keeps one `db.serverless` instance in us-east-1a. Policies state what is true: cluster storage replicated six ways across three availability zones by the service; the instance re-created automatically after any failure including an AZ failure (typically < 10 min); fallback if not back within the RTO: add a db.serverless instance in us-east-1b to the same cluster (no committed data lost; API unavailable until then, within the BCP RTO of 2 hours for database services); point-in-time recovery from automated backups retained 35 days (D27). Never claim Multi-AZ, a second/standby instance, or failover to a replica. Infra: the second instance was removed from di-backend-api branch `compliance/env-alignment` (commit 404aeb5, not deployed). Lint: check.py now flags the old wording.
- D27 **DocumentDB backups 35 days** (Mo, 2026-11-01; supersedes the 90-day target in RULEBOOK R3 and the 2026-10-31 minutes §4.4). 35 days is the DocumentDB maximum for automated backups and the live setting; no extra snapshots or AWS Backup plan. Also corrects D26: a failed instance is re-created automatically after any failure including an AZ failure; adding an instance in us-east-1b is only the fallback if that has not completed within the RTO. Point-in-time restore is for corruption/deletion. Lambda runs across AZs automatically (corrected 2026-11-01). Infra: `compliance/env-alignment` still sets BackupRetentionPeriod 90 (commit 989ad81) — revert to 35 before merging or the deploy fails.
