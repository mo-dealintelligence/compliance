# Control descriptions — quality sweep change note (2026-10-31)

Input: `scratch/quality-sweep/data/controls.json` (136 controls as held in Comp).
Output: `scratch/quality-sweep/controls-v2.json` (same ids, same order, names untouched).
Script: `scratch/quality-sweep/rewrite_controls.py` — re-runnable; every requirement
edit is an exact-string replacement that is asserted to match, every `Evidence:`
reference is checked against the control's linked tasks, and a banned-term scan
(Humadroid, GuardDuty, Security Hub/FSBP, AWS Config, WAF, Inspector, EC2, multi-region, size
language, "all employees", board meeting, 7-day, team member, device agent, Access
Analyzer, VPC endpoint, MFA-delete, anonymous) must pass.

## Counts

| Change type | Controls |
|---|---|
| Total controls | 136 |
| `changed: true` | 136 (every Implementation note was rewritten to the Q4 form: mechanism + `Evidence:` record list) |
| Names changed | 0 (truncated v1 names left as they are) |
| Requirement text edited | 53 |
| — R2 size language / role terms / "team members" → personnel | 51 |
| — R1 PI/Privacy TSC list → Security, Availability, Confidentiality (+ GDPR/CCPA) | 2 (CC3.1.1, CC3.1) |
| Implementation note: Humadroid → "the compliance platform" | 18 |
| Implementation note: R4 product removed or R4 compensating control cited (GuardDuty ×8, WAF/perimeter, MDM/device agent, Multi-AZ wording, single-region, metadata tagging, code-scanning stack) | 18 |
| Implementation note: R5/R3 stale number or cadence fixed (7-day backups → 90 days; CloudTrail 90 days → 7 years; annual access review → quarterly; PR "approval" → PR + CI gate + self-review; "PropelAuth MFA" → Google SSO/inherited MFA; risk count 6 → 7; vendor count 2 → 5; monthly Security Hub review; P1 4 business hours; 48-hour customer notice; 7-day critical CVE) | 30 |
| Implementation note: role wording only (board → management meeting, named person → CEO, contractor → Go-to-Market Contractor) | 13 |
| Implementation note: made specific from a generic v1 sentence using only v1 facts or rulebook-named mechanisms | 34 |
| Implementation note: no rule-driven content change (wording tightened, evidence list added) | 26 |
| Implementation note carries a CONFIRM | 11 (17 before D18 closed the six BCP-label rows) |
| Implementation note changed by a decision (D4, D15, D25) | 7 |
| Implementation note changed by D12 (Security Hub removed; round 2) | 25 (22 wording edits + 3 evidence-only renames) |

Tags are per control and overlap (a note can be both `humadroid` and `r5`); the
per-control tag list is in each record's `notes` field.

## What was done to the requirement text (before "Implementation:")

Only these kinds of edits, nothing else:
- Deleted or reworded size clauses: "Given the organization's size…", "small team
  size", "For a small remote team", "of this size", "2-5 employees", "Small
  companies can/should/might…" (AICPA guidance sentences deleted or recast).
- "all team members" / "each team member's" / "team member location" → personnel / role.
- "Employees shall be required…" (CC6.4.2) and "procedures for employees to…"
  (CC6.5.2) → personnel; "Train employees" (C1.1) → personnel.
- Role names: "the founder or designated lead" → "the CEO or a delegate approved by
  the CEO" (CC6.3.2); "a designated individual with appropriate authority" → "the
  CEO" (CC8.1.1); "peer review or secondary approval" → the R2 compensating control
  (CC8.1.3); "multiple team members" → "more than one person" (CC6.8.3, see CONFIRM).
- R1: the two lists of five Trust Services objectives (CC3.1.1, CC3.1).
- "Given the remote work environment…" clauses were **kept** (remote is a fact, not
  headcount).

Left in the requirement text on purpose (not in the allowed edit set — Mo to decide):
- CC6.6.2 and CC6.7.3 requirement wording says "authentication via PropelAuth with
  MFA" — conflicts with R5 ("never PropelAuth MFA"). Implementation notes use the
  R5 wording; the requirement sentences are unchanged.
- CC7.2.1 requirement mentions "VPN connections"; CC6.7.1 "VPN or zero-trust"; CC6.6
  AICPA text "VPNs". R4 removes VPN from the policy set; left here.
- "employees, contractors, and business partners", "employee-owned devices",
  "employee errors", "staff" in AICPA guidance text — not the "all employees" form.
- CC1.2 criterion text "board of directors" (AICPA wording) and the AICPA guidance
  "if your board lacks…" — kept; implementation notes say "management meeting".
- CC8.1 AICPA guidance "developers shouldn't push their own code to production" — kept.

## What was done to the Implementation notes

- Form: one or two sentences naming the mechanism, then `Evidence: <task titles>`
  using the titles exactly as linked in `tasks` (so references survive a task
  retitle only if the task sweep keeps a mapping — see "Task titles" below).
- Humadroid → the compliance platform (18). Dashboard/register facts kept as
  recorded (0 open incidents, 100 % SLA compliance, 8 active plans, 8 processes /
  7 critical, RTO 2 h / 4 h / 4 h, Multi-Impact Assessment method, People Risk
  Mitigate).
- R4: GuardDuty replaced by Security Hub + CloudTrail + the breach-detection Lambda
  → SNS (CC3.3.2, CC4.1.2, CC4.1, CC5.1.2, CC5.1, CC6.6.3, CC7.1, CC7.5);
  "3 availability zones"/"geographic redundancy" → Multi-AZ, single region
  (A1.2.3, CC9.1.2); metadata tagging → handling rules by tier + CloudFormation
  tags (C1.1.2); perimeter → CloudFront + Shield Standard + Lambda function URLs
  (CC6.6.1); endpoint → compliance platform device agent where deployed (CC6.8.1);
  remote access → browser SSO + AWS console/CLI with MFA, no VPN (CC6.6.2);
  configuration baseline → CloudFormation drift + Security Hub checks (CC7.1.1).
- R3/R5 numbers as listed in the counts table. Password facts (14+ chars,
  complexity, 90-day rotation) kept from v1 per R5.
- Counts updated from the current platform export, not invented: risk register
  7 risks (v1 said 6), vendor register 5 vendors — AWS, PropelAuth, GitHub,
  Google Workspace, Resend (v1 said 2).
- Facts added only where the rulebook names them: compensating controls (R2),
  quarterly backup-restore test, annual pen test, Secrets Manager / API key
  rotation, staging stage, CI toolchain, emergency-change path, training in the
  compliance platform at onboarding and annually, acknowledgments in the portal,
  manual disposal entry, retention-enforcement and access-review Lambdas, p95 > 2 s,
  P1 within 4 business hours, 48-hour customer notice, 7-year incident evidence.
- Nothing else was added. Where v1 was generic and the rulebook names no
  mechanism, the note stays generic and the control is on the CONFIRM list.

## Decisions applied (policies-v2/DECISIONS-2026-10-31.md, applied 2026-10-31)

Applied by the `DECISIONS` table in `rewrite_controls.py` (exact-string edits to the
Implementation note, asserted to match; each control's `notes` field ends with
"Decisions applied: D…"). Requirement text (the AICPA/platform criterion wording
before "Implementation:") was not touched by any decision.

| Decision | Controls | Change |
|---|---|---|
| D3 (keep VPC Flow Logs only; drop IAM Access Analyzer, DocumentDB audit logging, VPC endpoints, S3 MFA-delete) | none | None of the 136 notes claimed any of the four; VPC Flow Logs mentions kept (CC6.6.3, CC6.7.4, CC7.2.1). The four terms are now in the banned-term scan so they cannot come back. |
| D4 (no device agent; endpoint control = FileVault) | CC6.8.1 | "with the compliance platform device agent where deployed" removed; note now reads "FileVault full-disk encryption, XProtect, and Gatekeeper protect personnel macOS devices". "device agent" added to the banned-term scan. FileVault already stated in C1.1.3, CC6.4.2, CC6.7.3. |
| D5 (no anonymous channel; reports go to the CEO by email) | none | No note claimed an anonymous channel (CC2.2.3 already says reports go to the CEO). "anonymous" added to the banned-term scan, with one allowance: the CC2.2 criterion guidance text says "(like anonymous hotlines)" — AICPA wording, left as is. |
| D8 (R5 remediation clocks only) | none | Notes carry only R5 values (24 h critical, 7 d critical dependency CVE — CC6.8.2). The P1 "acknowledged within 4 business hours" in CC7.3.2 is the rulebook R4 incident response target, not the vulnerability triage clock D8 deletes; left. |
| D12 (Security Hub — OPEN at round 1) | none | Superseded by round 2 below: Security Hub is removed. |
| D15 (sub-processors = AWS and PropelAuth only) | CC3.2.2, CC9.2 | Vendor-register sentence now distinguishes "AWS and PropelAuth as sub-processors, and GitHub, Google Workspace, and Resend as vendors that do not process customer data". |
| D18 (BCP test record renamed "BCP full test 2026-02-04") | A1.2.3, A1.3.1, A1.3.2, A1.3, CC7.5.2, CC9.1.3 | Notes already cite the execution date only; the "Q1 2025 label" CONFIRM is closed (tag removed; `notes` say "(D18)"). |
| D25 (cut cadences with no scheduled record in docs/11 §2) | A1.1.2, CC1.3.1, CC2.1.1, CC6.1.1 | A1.1.2: "capacity is reviewed annually in the quarterly management meeting" cut. CC1.3.1: organizational structure "reviewed annually" cut. CC2.1.1 and CC6.1.1: asset inventory "reviewed annually in the Q4 management meeting" → "refreshed annually" (the doc-11 annual inventory refresh). Every other cadence in the notes is on the doc-11 calendar: monthly Security Hub review; quarterly access review, management meeting, risk review, backup-restore test; annual policy review, training, risk assessment, vendor review, tabletop/BCP exercise, penetration test, performance evaluation, Code of Conduct acknowledgment. |

Not applicable to control notes: D1, D2, D6, D7, D9, D10, D11, D13, D14, D16, D17, D19–D24
(no note mentions staging accounts, KMS key separation, the compliance mailbox, vendor
breach-notice hours, the change window, status-update intervals, pentest quarter or
insurance, availability measurement, controller/processor roles, DSR rows, the 86 %
figure, record versioning, or author fields).

CONFIRM rows closed by a decision: the BCP "Q1 2025" label row (D18). Still open: the
rest of the list below.

## Decisions applied (2026-10-31, round 2)

Mo's second-round answers (DECISIONS-2026-10-31.md, 22:19). Applied by the same
`DECISIONS` table (D12 rows) plus the new `EVIDENCE_RENAMES` map; `notes` now end
"Decisions applied: … D12".

| Decision | Controls | Change |
|---|---|---|
| D12 (Security Hub removed) — wording | CC3.1.2, CC3.3.2, CC3.4.1, CC3.4, CC4.1.2, CC4.1, CC4.2.1, CC4.2.2, CC4.2, CC5.1.2, CC5.1, CC6.6.3, CC6.8.1, CC6.8, CC7.1.1, CC7.1.2, CC7.1, CC7.2.1, CC7.2.2, CC7.2.3, CC7.3, CC7.4 (22) | Every Security Hub mention in an Implementation note replaced, adapted to the sentence: the detection/monitoring mechanism is now "the monthly configuration-check Lambda" (dated pass/fail record in the compliance platform; CC7.1.1 lists the checklist items) and "the CloudTrail-EventBridge security-event rule → breach-detection Lambda → SNS alert to the CEO in real time". "Findings reviewed monthly" → "the configuration-check record is reviewed monthly" (CC4.2.1, CC4.2.2, CC7.1.2, CC7.2.3). Vulnerability awareness where Security Hub was listed as a scanner → ECR scan-on-push + Dependabot and code scanning + Trivy in CI (CC4.1.2, CC6.8.1, CC6.8, CC7.1). Monthly cadence kept everywhere. |
| D12 — evidence | the 19 controls that linked the two Security Hub screenshot tasks (CC3.1.2, CC3.1, CC3.2, CC3.3.2, CC3.3, CC3.4.1, CC3.4, CC4.1.2, CC4.1, CC4.2.1, CC4.2, CC5.1.2, CC6.8.1, CC6.8, CC7.1.1, CC7.1.2, CC7.1, CC7.3, CC7.4; CC3.4 linked both) | `Evidence:` "AWS Securityhub Findings" / "AWS Securityhub Overview" → "Configuration-check record (monthly)" (de-duplicated where a control linked both). The two v1 tasks are retitled in records-v2/tasks-v2.json; the apply step must relink by the v1 task id. CC3.1, CC3.2, CC3.3 are evidence-only changes (their note text never named Security Hub). |
| D12 — guard | all | "Security Hub", "Securityhub", "FSBP", "Foundational Security" added to the banned-term scan; the CC3.3.2 script note "GuardDuty -> Security Hub …" reworded. The historical `notes` strings "GuardDuty removed" are change history and stay. |
| D11b (no pentest-vendor insurance requirement) | none | No Implementation note ever mentioned insurance (CC4.1.2 says "an annual third-party penetration test is performed"). Nothing to remove. |
| D13b (monthly "Availability record (monthly)" task) | none | No control note is edited: the task does not exist yet in `data/controls.json` links, so it cannot be cited as `Evidence:` without failing the linked-task check. After the apply step creates the task (records-v2/tasks-v2.json, `"new": true`) and links it to A1.1.x / A1.2.x, add it to `Evidence:` and re-run. Logged here so it is not lost. |
| D14 (controller/processor — OPEN) | none | No Implementation note states a controller or processor role; nothing to mark. |

## CONFIRM list (Implementation note could not be made specific, or a fact needs Mo)

| Control | What to confirm |
|---|---|
| ~~A1.2.3, A1.3.1, A1.3.2, A1.3, CC7.5.2, CC9.1.3~~ | Closed by D18: the record is "BCP full test 2026-02-04"; notes cite the execution date only. |
| CC1.2.1 | "External advisor" consultation and the basis for oversight independence are v1 claims with no named record. Confirm the advisor arrangement exists (and is minuted) or drop it. |
| CC1.5.1 | Only linked evidence is "PropelAuth Security Settings", which does not evidence security responsibilities in role definitions. Link the job descriptions / performance evaluation instead. |
| CC2.2.1 | v1 "security updates via regular team communications" is generic; note now cites portal acknowledgments and the quarterly management meeting (rulebook-named). Confirm that is the actual channel. |
| CC2.3.2 | v1 names no external security contact. Note says "the security contact published in the privacy notice". Confirm the address (security@dealintelligence.io?) and that the privacy notice publishes it. |
| CC3.2 | v1 example "probability/impact 4/3 = score 32" dropped — the arithmetic does not match. Confirm the scoring formula used in the compliance platform. |
| CC6.4.2, CC6.7.3 | Lost/stolen device reporting: v1 says within 24 hours; Acceptable Use Policy v2 says "immediately". Pick one and align. |
| CC6.8, CC7.1 | v1 says "code scanning via AWS not GitHub"; the R4 table says "GitHub Dependabot and code scanning, Trivy in CI". Notes follow R4. Confirm where code scanning actually runs. |
| CC6.8.3 | Requirement now says "more than one person can execute response procedures"; with one production-access role this may not be true. Confirm or delete the sentence. |
| CC7.4.2 | Requirement asks for primary and backup incident commanders; only the CEO is named. Confirm whether a backup (external?) exists or accept the gap. |
| CC9.1.1 | BCP dashboard labels a process "MongoDB"; note says DocumentDB per Q2. Rename the process in the compliance platform or revert the note. |

## Other things for Mo to decide

- `changed: true` on all 136 because every note was reformatted; 26 of them had
  no rule-driven content change. If you only want to push rule-driven changes,
  filter on `notes` not containing "Implementation: none".
- Point-in-time counts kept from v1 will go stale: 8 KMS keys (CC6.1.4), 8 Lambda
  functions (CC2.1.1), 21 Dependabot alerts (CC4.1.2, CC6.8), 8 BCP plans /
  processes, 7 risks, 5 vendors. Consider dropping counts from control notes and
  leaving them to the evidence.
- Policy linkages (not edited): several controls still link "Data Classification
  Policy" (merged into the Standard per R7) and "Third-Party Integration Security
  Guidelines" (merged per R7). Relink to Data Classification and Handling Standard /
  API Security Standard / Vendor Management when the policy set is loaded.
- Task "AWS S3 Bucket Encryption" says "Supports: … PI1.5.1" — for the task sweep (R1).
- Task titles: notes cite task titles verbatim ("Board Management Meeting Minutes
  Q4 2025", "Compliance Platform Bcp Dashboard"). If the task sweep retitles
  tasks, add the v1 → v2 title to `EVIDENCE_RENAMES` in `rewrite_controls.py`
  (the check validates the v1 title against the control's linked tasks and
  prints the v2 title) and re-run; otherwise the checker fails on the mismatch.
- CC1.3.2 / CC6.3.3 cite the R2 compensating-control set (PR + CI gate, CloudTrail,
  external auditor review). Confirm you want the auditor named as a control.
