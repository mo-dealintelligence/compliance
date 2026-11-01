# Change note — information-security-policy (v1.0 → v2.0)

- R0: frontmatter `version` 1.0 → 2.0, `effective_date` / `review_date` set to publication placeholders, added `supersedes: "1.0"`; dropped the v1 `finalized_at` export stamp (it dated the v1 PDF, not this version).
- R0: added §10 Revision history.
- R0/R8: restored run-on bullets into real lists throughout (§5.1, §5.3, §5.4, §5.5, §5.6, §6.3, §8, §9); removed `<u>` underline artefacts from document names.
- R1: §2 "all five Trust Services Criteria ... Security (required), Availability, Processing Integrity, Confidentiality, and Privacy" → "Security, Availability and Confidentiality".
- R1: §3 TSC definition "Security, Availability, Processing Integrity, Confidentiality, and Privacy" → "Security, Availability and Confidentiality".
- R1: §9 removed the "PI1.1-PI1.5 : Processing Integrity" and "P1.0-P8.0 : Privacy" mapping rows; CC/A/C rows kept.
- R2: §4.1 Executive Leadership, §4.2 Security Lead and §4.3 System Owner merged into a single §4.1 Chief Executive Officer (CEO) with all v1 bullets retained, plus the R2 statements (owns every control, only role with production access, incident commander, exception approver, data protection contact).
- R2: added §4.2 Go-to-Market Contractor (no production access; onboarding, training, acknowledgments, acceptable use, confidentiality) and §4.4 External Parties (SOC 2 auditor, penetration-test vendor, sub-processors). §4.3 All Personnel kept verbatim.
- R2/R3: §5.4 "Branch protection rules requiring pull request reviews" → "Branch protection on `main` requiring a pull request with required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes"; "Staging deployment before production release" → "Deployment to a staging stage before production release"; "Manual approval for production deployments" → "Production deployments only from a green CI run".
- R2: §5.9 "Code reviews for security vulnerabilities" → "Logged self-review in the pull request, with automated security checks (Bandit, Trivy, TruffleHog) in CI".
- R4: §5.1 removed "leverages 86% automation of controls" → "administered in the compliance platform, which serves as the control register (controls, evidence, tasks)".
- R4: §6.1 removed "Quarterly automated control testing via Lambda functions" → "Controls, evidence and tasks tracked in the compliance platform as the control register".
- R4: §6.4 removed "86% control automation rate" (no replacement metric).
- R4: §5.12 removed "Phishing awareness and testing" → "Completion certificates recorded in the compliance platform portal".
- R5: §5.2 "PropelAuth JWT authentication with multi-factor authentication capability" → "PropelAuth JWT authentication, with customer MFA inherited from Google Workspace sign-in via PropelAuth (Google SSO only)"; added bullet "Multi-factor authentication for personnel enforced in Google Workspace, GitHub and AWS".
- R5: §5.5 Security Hub bullet extended with "critical findings alerted in real time via SNS and findings reviewed monthly".
- R5: §5.6 "Regular security assessments" → "Annual security assessments" (vendor reviews annual).
- R5: §6.4 "48-hour incident response time" → "48-hour breach notification to affected customers" (48 hours is the customer notification figure; incident response targets live in the IR procedure).
- R7: §3 Sub-processor definition "(currently limited to PropelAuth and AWS)" → "(the current list of sub-processors is maintained in the Vendor Management Policy)"; §5.6 "Current sub-processors limited to PropelAuth and AWS" → "Current sub-processors listed in the Vendor Management Policy" (list now AWS, PropelAuth, Google Workspace, GitHub, Resend, compliance platform hosting per R7).
- R7: §5.6 "Third-Party Integration Security Guidelines" → "Integration security section of the API Security and Rate Limiting Standard"; removed the Guidelines from §8 Related Documents.
- Kept verbatim (no rule applies): §1, §5.3 content, §5.7, §5.8, §5.10, §5.11, §5.13, §6.2, §7, 99.9 % SLA, 90-day logs, quarterly backup-restore test, multi-AZ.

## CONFIRM

- §5.3 "24-month retention period for active leads" kept verbatim. R5 sets customer account data retention at "relationship + 24 months"; confirm the lead-level 24-month figure is still what the retention Lambda enforces, or reword to the R5 phrasing.
- §5.5 "24/7 CloudWatch monitoring" kept (it describes automated monitoring, not a staffed response); confirm this is acceptable alongside the R5 "no 24/7 response" decision.
- §6.3 "Quarterly internal compliance assessments" kept verbatim; confirm a quarterly internal assessment is actually recorded in the compliance platform.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

## Quality sweep (2026-10-31)

- Voice: converted 14 "shall"/"shall be" constructions to present tense; removed filler ("comprehensive", "cornerstone document", "to reduce human error and ensure consistent enforcement"); rewrote §1 Purpose so the second paragraph no longer restates the first.
- Structure: merged §9 Compliance Mapping into §1 Purpose as a single sentence (all CC/A/C ranges kept, with their names); §8 Related Documents regrouped under bold labels (Policies / Standards / Procedures and plans / Other) instead of unnumbered `###` sub-headings, alphabetised, same 20 documents; revision history renumbered to §9.
- Formatting: removed blank lines between bullets in every list (≈110 lines); headings to sentence case after the number; bold-colon definitions normalised ("**Term**: …"); "99.9%" → "99.9 %"; Oxford comma applied ("Security, Availability, and Confidentiality" ×3, "Google Workspace, GitHub, and AWS").
- Consistency: "Chief Executive Officer (CEO)" on first use in §4.1, "the CEO" after; §4.2 / §4.3 given a lead-in sentence so bullets read as a list of duties; "48-hour breach notification" → "breach notification to affected customers within 48 hours" ×2; "multi-AZ" → "Multi-AZ"; "Ensures adequate resources" → "Provides the resources"; "24-month retention period for active leads" → "Active leads are retained for 24 months" (same figure).
- Parallel grammar: §6.1–6.2 bullets made full-sentence statements within each list; §5.x lists kept as fragments.
- Kept: 24/7 CloudWatch monitoring (existing CONFIRM), §6.3 quarterly internal compliance assessments (existing CONFIRM), all numbers, roles, and controls.

No new CONFIRM items.

## Decisions applied (2026-10-31)

- D25: cut §6.3 quarterly internal compliance assessments (bullet removed; section kept with annual SOC 2 audit, evidence collection, management review). Kept: §5.2 quarterly access reviews, §5.7 quarterly backup restoration testing, §6.1 annual security assessment, §6.2 annual policy review (all in the doc-11 calendar).
- D12: Security Hub wording in §5.5 and §6.1 unchanged.

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §5.7 security-monitoring list: the Security Hub bullet replaced by the CloudTrail-EventBridge → breach-detection Lambda → SNS real-time alert (folded into the CloudTrail bullet, event list named) and a monthly configuration-check Lambda bullet (checklist left to the Cloud Infrastructure Security Policy, which carries the full list); §6.1 "Continuous monitoring runs through CloudWatch and Security Hub" → CloudWatch and CloudTrail event alerting, with the monthly configuration-check record as the recurring evidence.
- D11b, D13b, D14: no insurance, availability-measurement or controller/processor text in this document; nothing to apply.

- D1 revised (Mo, 2026-10-31): staging moves to a **separate AWS account** in the same Organization; wording updated from "staging stage of the same stack" to a staging environment/account.
