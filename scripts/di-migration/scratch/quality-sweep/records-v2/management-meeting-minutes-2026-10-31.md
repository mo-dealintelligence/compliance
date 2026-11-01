---
title: "Management Meeting Minutes - October 31, 2026"
doc_type: "Record"
version: "2.0"
supersedes: "1.0"
acknowledgment: "None"
effective_date: "October 31, 2026"
review_date: "N/A"
finalized_at: ""
author: "Mo Messidi"
source: "created 2026-10-31 per policies-v2/DECISIONS-2026-10-31.md D17; version 2.0 of the management meeting minutes record (1.0 = Q4 2025 minutes)"
---

# Management Meeting Minutes - October 31, 2026

## 1. Meeting information

| Field | Detail |
|---|---|
| Meeting type | Management meeting (SOC 2 program review) |
| Date | October 31, 2026 |
| Time | [CONFIRM] |
| Location | Video conference [CONFIRM] |
| Called by | Mo Messidi, Chief Executive Officer (CEO) |
| Purpose | Record the SOC 2 scope change, the policy set v2 program, the environment to-dos, the Security Hub decision, and the compliance platform cut-over |

## 2. Attendees

| Role | Name | Present |
|---|---|---|
| CEO | Mo Messidi | Yes |

Absent: none. Quorum: yes [CONFIRM].

## 3. Agenda

1. Scope change to Security, Availability, and Confidentiality
2. Descoping of Processing Integrity and Privacy controls
3. Policy set v2 program
4. Environment to-dos
5. Security Hub decision
6. Compliance platform cut-over
7. Action items

## 4. Minutes

### 4.1 Scope change to Security, Availability, and Confidentiality

The SOC 2 scope is Security, Availability, and Confidentiality. Objectives, policies, and control notes that listed five Trust Services Categories are restated to the three. GDPR and CCPA obligations remain as regulatory requirements outside the SOC 2 scope.

Decision: scope = Security, Availability, Confidentiality (DECISIONS D17; RULEBOOK R1).

### 4.2 Descoping of Processing Integrity and Privacy controls

Processing Integrity (PI1.x) and Privacy (P1.x–P8.x) criteria are removed from control mappings, task "Supports" lines, and the objectives text. Privacy obligations are carried by the Privacy Notice and Data Processing Agreement Template and the Data Subject Rights Request Procedure. Role model: Deal Intelligence is the controller for the business-contact data it compiles and the processor for data a customer uploads or holds in its account; the DPA carries processor terms for the latter and an independent-controllers clause for the former.

Decision: PI and Privacy criteria descoped; controller/processor roles as stated (D14, D17).

### 4.3 Policy set v2 program

The v2 policy set (policies-v2/) replaces the v1 policies under the rulebook (R0–R8) and the quality rubric. Key commitments recorded:

- Vendor breach notification: contractual terms that allow Deal Intelligence to meet its 48-hour customer commitment (D7).
- Remediation clocks: 24 hours for exploited or critical vulnerabilities, 7 days for critical dependency CVEs, 30 days for high, 90 days for medium; the 4-hour triage and 2-hour isolation clocks are deleted (D8).
- Change window: 07:00–11:00 UTC (02:00–06:00 ET) (D9).
- Incident communication: customer status updates every 2 hours for P1 (SLA policy); internal updates every 30 minutes (Incident Response Procedure); the two documents cross-reference each other (D10).
- Penetration test: annual, in Q3; no vendor insurance requirement (D11b).
- Availability: measured monthly over all minutes, excluding announced maintenance windows; a monthly compliance-platform task "Availability record (monthly)" (owner CEO) carries the record and is covered by the Monday reminder email (D13, D13b).
- Sub-processors: AWS and PropelAuth only; Google Workspace, GitHub, Resend, and HubSpot are vendors that do not process customer data (D15).
- Data subject rights: GDPR Article 18 restriction row restored, 30 days, with a manual step (D16).
- Endpoint control: FileVault full-disk encryption on personnel macOS devices plus browser SSO with MFA; no compliance-platform device agent (D4).
- Reporting: no anonymous channel exists; reports go to the CEO by email at compliance@dealintelligence.io (D5, D6).
- Staging: a staging stage of the same stack in the same AWS account (D1).
- Logging claims: VPC Flow Logs only; IAM Access Analyzer, DocumentDB audit logging, VPC endpoints, and S3 MFA-delete removed from all documents (D3).
- Records: job descriptions and the organizational structure move to version 2.0; historical minutes, certificates, and the ethics log keep their version with a "Corrected" note; author field "Mo Messidi" (D20, D22).
- The "86 % control automation" figure is struck from the CEO job description and the organizational structure; it stays as recorded in the Q4 2025 minutes and the 2025 CEO evaluation (D17).
- Cadences with no scheduled record in the compliance operating model are cut from policies, control notes, and records (D25).

Decision: the commitments above are adopted as stated (DECISIONS D1–D11, D11b, D13, D13b, D15–D16, D20, D22, D25). The controller/processor framing (D14) stays as applied in the Data Subject Rights Request Procedure and the DPA template but is open pending investigation [CONFIRM: D14 open — pending investigation]. Publication date of the v2 set: [CONFIRM].

### 4.4 Environment to-dos

Policy claims that run ahead of the deployed environment, to be closed before the Type II observation window (docs/05):

| Item | Current state | Target | Owner | Due |
|---|---|---|---|---|
| KMS key separation | One customer-managed key in production | Data, backup, and audit-log keys as designed in the Encryption and Cryptographic Controls Standard (D2) | CEO | [CONFIRM] |
| DocumentDB backups | [CONFIRM: current retention] | 90-day retention with point-in-time recovery | CEO | [CONFIRM] |
| Multi-AZ | [CONFIRM: current instance layout] | Multi-AZ DocumentDB (us-east-1a, us-east-1b) | CEO | [CONFIRM] |
| Pull requests and branch protection | Direct pushes to main | Branch protection on main: pull request required, CI status checks required, no direct pushes | CEO | [CONFIRM] |
| Staging | [CONFIRM: current state] | Staging stage of the same stack in the same AWS account (D1) | CEO | [CONFIRM] |
| Secrets rotation | [CONFIRM: current state] | DocumentDB credential rotated by Secrets Manager; API keys per the rotation calendar | CEO | [CONFIRM] |
| CloudTrail lock | [CONFIRM: current state] | CloudTrail bucket with Object Lock and 7-year retention | CEO | [CONFIRM] |
| ECR scan-on-push | Off on the two production repositories | Scan-on-push enabled and recorded | CEO | [CONFIRM] |
| Configuration-check Lambda and security-event rule | Not deployed | Scheduled configuration-check Lambda (monthly) posting a pass/fail record to the compliance platform; EventBridge rule on security-relevant CloudTrail events to the breach-detection Lambda and SNS (D12) | CEO | [CONFIRM] |
| Security Hub | Enabled | Disabled after the configuration-check Lambda and the security-event rule are deployed (D12) | CEO | [CONFIRM] |

Decision: KMS key-separation design is kept in the standard and the AWS change is recorded as a to-do (D2). Other rows: targets as stated in the v2 policies; dates [CONFIRM].

### 4.5 Security Hub decision

AWS Security Hub is removed as a control mechanism. The replacement control, stated in every policy, control note, and record where Security Hub was the mechanism, is: a scheduled configuration-check Lambda that runs monthly against a fixed checklist (CloudTrail enabled and log-file validation on; no public S3 buckets; no security groups open to 0.0.0.0/0 on administrative ports; root account MFA; IAM password policy; KMS key rotation; ECR scan-on-push; DocumentDB backup retention and Multi-AZ) and posts a dated pass/fail record to the compliance platform (task "Configuration-check record (monthly)"); and an EventBridge rule on security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) that triggers the breach-detection Lambda and an SNS alert to the CEO in real time. Vulnerability awareness is unchanged: ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI. Security Hub is disabled in the AWS account once the Lambda and the rule are deployed (environment to-do in 4.4).

Decision: Security Hub removed; replacement control as stated (D12). Decision date: October 31, 2026.

### 4.6 Compliance platform cut-over

The self-hosted compliance platform replaces the previous platform as the control register and evidence store. Native records scripted for import: Q4 2025 management meeting minutes, 2025 CEO performance evaluation, BCP full test 2026-02-04 (renamed from the "Q1 2025" label, D18), RBAC matrix, infrastructure inventory. Risk "OPERATIONAL_PEOPLE-001 Key-person dependency — CEO holds all production access" retitled (D19).

Cut-over date: [CONFIRM]. Remaining platform follow-ups (orphaned previous-platform IAM role, generic draft policies, evidence screenshots, portal invite and training for the Go-to-Market Contractor): [CONFIRM].

## 5. Decisions

| # | Decision | Source |
|---|---|---|
| 1 | SOC 2 scope is Security, Availability, and Confidentiality; PI and Privacy criteria descoped | D17, R1 |
| 2 | Policy set v2 commitments adopted as listed in 4.3; controller/processor framing (D14) open pending investigation | D1–D11, D11b, D13, D13b, D15–D16, D20, D22, D25 |
| 3 | KMS key-separation design kept; AWS change recorded as an environment to-do | D2 |
| 4 | Security Hub removed; replaced by the monthly configuration-check Lambda record and the CloudTrail-EventBridge security-event rule to the breach-detection Lambda and SNS | D12 |
| 5 | BCP test record renamed "BCP full test 2026-02-04"; key-person risk retitled | D18, D19 |
| 6 | Historical records (Q4 2025 minutes, 2025 CEO evaluation) not edited; corrections carried as a dated note | D17, D20 |

## 6. Action items

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Publish the v2 policy set and re-acknowledge in the compliance platform portal | CEO | [CONFIRM] |
| 2 | Close the environment to-dos in 4.4 and attach evidence | CEO | [CONFIRM] |
| 3 | Deploy the configuration-check Lambda and the security-event EventBridge rule, then disable Security Hub in the AWS account | CEO | [CONFIRM] |
| 4 | Complete the compliance platform cut-over follow-ups in 4.6 | CEO | [CONFIRM] |
| 5 | Confirm every [CONFIRM] item in these minutes and finalize | CEO | [CONFIRM] |

## 7. Next meeting

[CONFIRM: date] — quarterly management meeting per the compliance operating model.

## 8. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| CEO (meeting recorder) | Mo Messidi | _________________ | [CONFIRM] |

## 9. Revision history

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | February 2, 2026 | Mo Messidi | Q4 2025 management meeting minutes (historical record, unchanged) |
| 2.0 | October 31, 2026 | Mo Messidi | New minutes recording the scope change, policy set v2, environment to-dos, the Security Hub decision (removed; replacement control stated), and the compliance platform cut-over |
