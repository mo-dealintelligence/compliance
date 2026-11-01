# Control descriptions — quality sweep change note (2026-10-31)

Input: `scratch/quality-sweep/data/controls.json` (136 controls as held in Comp).
Output: `scratch/quality-sweep/controls-v2.json` (same ids, same order, names untouched).
Script: `scratch/quality-sweep/rewrite_controls.py` — re-runnable; every requirement
edit is an exact-string replacement that is asserted to match, every `Evidence:`
reference is checked against the control's linked tasks, and a banned-term scan
(Humadroid, GuardDuty, AWS Config, WAF, Inspector, EC2, multi-region, size
language, "all employees", board meeting, 7-day, team member) must pass.

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
| Implementation note carries a CONFIRM | 17 |

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

## CONFIRM list (Implementation note could not be made specific, or a fact needs Mo)

| Control | What to confirm |
|---|---|
| A1.2.3, A1.3.1, A1.3.2, A1.3, CC7.5.2, CC9.1.3 | v1 calls the BCP test "Q1 2025" but says it was executed February 4, 2026. Notes now cite the execution date only. Confirm the correct label (Q1 2026?) and whether the Comp BCP record should be renamed. |
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
  tasks, re-run `rewrite_controls.py` after updating the `Evidence:` strings, or
  the checker will fail on the mismatch.
- CC1.3.2 / CC6.3.3 cite the R2 compensating-control set (PR + CI gate, CloudTrail,
  external auditor review). Confirm you want the auditor named as a control.
