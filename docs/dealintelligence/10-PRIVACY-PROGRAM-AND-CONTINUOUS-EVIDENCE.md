# 10 — Lean GDPR/CCPA program and continuous evidence for a Type II (scoping, 2026-10-31)

Two questions from Mo: (1) add GDPR/CCPA "with some automation", cheaply;
(2) is a quarterly screenshot run enough for SOC 2 Type II, and how should
evidence be collected to match what the auditor samples.

Not legal advice; the data‑broker question in §1.2 needs ten minutes with a
privacy lawyer before you register or decide not to.

---

## 1. GDPR / CCPA — what actually applies to Deal Intelligence

Facts that drive scope: DI collects business contact data (name, business
email, LinkedIn URL, title, employer, competitor‑interaction signals) about
people it has **no direct relationship with**, from public/third‑party
sources, and sells it to customers. For that data DI is a **controller**
(GDPR) / a **business** and very likely a **data broker** (California). For
data customers push into DI (CRM sync, Slack), DI is a **processor**. The
Type I policies never settle this; the DPA template says "processor" and the
privacy notice behaves like a controller. Settling it is the first task.

### 1.1 Obligations that matter (and the cheap way to meet each)

| Obligation | Law | What it means for DI | Cheapest compliant implementation |
|---|---|---|---|
| Privacy notice to people whose data you hold (Art. 14 notice for data not collected from the subject) | GDPR 13/14; CCPA notice at collection | Must tell the individuals what you hold and why; Art. 14 allows "disproportionate effort" exception if you publish the notice | Public privacy notice page + a one‑line "where we got your data / how to opt out" link in any outreach that uses the data; document the Art. 14 exception reasoning once (LIA) |
| Lawful basis | GDPR 6(1)(f) | Legitimate interest for B2B contact data is the standard basis | One Legitimate Interest Assessment (LIA) document, ~2 pages, reviewed yearly |
| Records of processing (RoPA) | GDPR 30 | One table of processing activities | A single sheet in Comp (custom requirement + task); 8–10 rows |
| Data subject rights: access, deletion, correction, objection/opt‑out | GDPR 15–21; CCPA know/delete/correct/opt‑out of sale | Must handle within 30 days (GDPR) / 45 days (CCPA) | `privacy@dealintelligence.io` → Comp **access‑request / DSR record** (form exists); a **suppression collection** in DocumentDB checked by every ingestion and export path; deletion by the existing `dataRetentionEnforcement` Lambda extended with a "delete by email/LinkedIn URL" mode |
| Do Not Sell/Share + GPC signal | CCPA | Required if you sell PI; B2B exemption expired 2023 | "Do Not Sell or Share My Personal Information" link on the website → same suppression list; honour GPC header on the web app (one middleware line) |
| **Data broker registration + DROP** | Cal. Civ. Code 1798.99.80 (Delete Act, SB 362/361) | If DI is a data broker: register annually with CalPrivacy (fee), and **since Aug 1, 2026** pull the DROP deletion list at least every 45 days, delete/suppress matches, report status; $200/day/request penalties | Register (fee is a few hundred dollars/yr); a scheduled Lambda (EventBridge, every 30 days) that downloads the DROP list, matches on hashed email, writes to the suppression collection, deletes matches, and files a Comp evidence record — this is the one piece of real automation worth building |
| Retention limits | GDPR 5(1)(e); policy says 24 months | Already automated (`dataRetentionEnforcement` Lambda) | keep; add a monthly evidence record of rows purged |
| Vendor/sub‑processor contracts | GDPR 28; CCPA service‑provider terms | AWS, PropelAuth, Google Workspace, GitHub, Resend, Comp (self‑hosted = none) | DPAs are click‑through for all; store the links/PDFs on the vendor records in Comp |
| Breach notification | GDPR 33/34 (72 h to authority); CCPA | Already in the IR procedure (48 h customers, 72 h authority) | keep; fix the DPA's 24 h promise |
| Cookies/consent on the marketing site | ePrivacy; CCPA | Only if the site sets non‑essential cookies | check HubSpot tracking on dealintelligence.io; a banner only if needed |
| International transfers | GDPR Ch. V | Data in us‑east‑1; EU subjects' data processed in the US | rely on SCCs in the DPA template + EU‑US DPF only if DI certifies (don't); document transfer basis once |

### 1.2 Decision needed: are you a data broker?

The definition is a business that knowingly collects and sells to third
parties the personal information of consumers with whom it has no direct
relationship. DI's product is exactly that, for individuals who are
Californian in some share of records. Options:
- **Register** (cheap, ~2 hours + fee) and run the DROP sweep — the
  automation above makes the 45‑day cycle a Lambda, not a chore. Your
  "companies using X" pages are company‑level and unaffected; DROP affects
  individual contact rows only.
- **Argue you are not** (e.g. only business‑role data, no sale as defined) —
  needs counsel's opinion in writing; keep it in Comp.
I'd budget for the first option.

### 1.3 How to represent it in Comp (lean)

Not the 33 GDPR/CCPA template controls we removed. Instead a **custom
framework "Privacy (GDPR/CCPA)"** (`POST /frameworks/custom`) with ~10
requirements, each linked to existing SOC 2 Privacy‑category controls where
they overlap (P1–P8 already exist) plus 4–5 new controls:

| Requirement | Control / evidence (Comp) |
|---|---|
| Role & basis documented | LIA + controller/processor memo (policy doc) |
| Privacy notice current | yearly task; screenshot of the live page |
| RoPA maintained | yearly task; the RoPA sheet attached |
| DSR handling | `access-request` form records; KPI: on‑time % |
| Suppression honoured | monthly automated record: suppression count, last sweep |
| DROP processed every 45 days | automated record per sweep (list size, matches, deleted) |
| Retention enforced | monthly automated record from the retention Lambda |
| Opt‑out link + GPC | yearly screenshot + code reference |
| Sub‑processor DPAs | vendor records with DPA attached |
| Breach notification | existing IR procedure |

Effort: custom framework + requirements via API — half a day. DROP/suppression
Lambda — 1–2 days in di‑backend‑api (fits next to `dataRetentionEnforcement`).
LIA/RoPA/notice edits — a day of writing. Cost: registration fee only.

---

## 2. Continuous evidence for a Type II

### 2.1 What the auditor actually does

A Type II covers a period (6–12 months). For each control the auditor
picks a test type:

| Control type | Example | What they ask for |
|---|---|---|
| Automated / configuration | CloudTrail on, KMS on, branch protection, log retention | the configuration **as of several dates across the period** — not one screenshot at the end |
| Recurring manual | quarterly access review, annual training, policy review, backup restore test | **every occurrence** in the period, dated, with who did it |
| Event‑driven | changes, incidents, new hires/terminations, vendor onboarding, DSRs | the **complete population** for the period, then a sample (e.g. 25 of 300 changes) with the evidence for each sampled item |
| Continuous monitoring | alerts reviewed, vulnerabilities remediated within SLA | the log of events **and** proof of review/remediation per sampled event |

So: a quarterly screenshot run covers only the first row, and only if it
runs every quarter without gaps. The population and recurring rows are
where solo‑operator Type IIs fail — "show me every change in March" has to
come from a system, not from memory.

### 2.2 Design — four layers, cheapest first

**Layer 1 — Populations come from systems of record (free, already there).**
- Changes: GitHub PRs into `main` (once branch protection is on, the PR list *is* the population; CI run per PR is the test evidence).
- Infra changes: CloudTrail `CreateStack/UpdateStack` + CodeBuild history.
- Access: PropelAuth user list, IAM users/roles (inventory script), Google Workspace users.
- Incidents / DSRs / access requests: Comp forms (findings, access‑request, whistleblower, DSR records).
- People: Comp People (onboard/offboard dates — fill them in).
- Vendors: Comp Vendors.
Requirement: logs must **cover the whole period**. CloudTrail is 90 days in CloudWatch → set the CloudTrail S3 bucket lifecycle to ≥ 400 days (Object Lock optional). Same for `di-backend-production-*` log groups: raise retention to 400 days or export monthly to S3 (CloudWatch → S3 export is pennies).

**Layer 2 — Automated daily configuration evidence (Comp integrations, ~1 hour each to connect).**
Reversing my earlier "skip": for a Type II the daily timestamped check is exactly what row 1 needs.
- AWS integration (read‑only role): CloudTrail, security groups, IAM, KMS rotation, S3 encryption/public access — daily.
- GitHub integration: branch protection, 2FA, Dependabot enabled, code scanning, Dependabot alert severity — daily. This alone evidences CC8.1/CC7.1 for the period.
- Google Workspace integration: 2‑step verification, employee list — daily.
Each run is stored with a timestamp and attached to the mapped controls; the auditor can pick any date.

**Layer 3 — Scheduled screenshot run (Chrome) for what has no API.**
Keep the shot list but change cadence by control: monthly for monitoring/alarms/Security Hub/ECR scan results; quarterly for the rest; and run it on a schedule, not by hand. Each run writes `runs/<date>.json` and attaches to tasks — that log is itself evidence of the control operating.

**Layer 4 — Recurring manual controls as Comp tasks with real completion.**
Tasks already have frequency + review dates; the task‑schedule cron flips them to `todo` and emails you. The evidence is the dated completion plus the artifact (access‑review export, training certificate, policy re‑publish, restore‑test record, tabletop form). The population of these is Comp's own task history.

### 2.3 Cadence answer

| Control | Minimum cadence that survives a Type II |
|---|---|
| Access review (PropelAuth, IAM, GitHub, Workspace) | quarterly, every quarter in the period, exported list + sign‑off |
| Vulnerability/alert review | continuous (integration daily) + a **monthly** review record |
| Backups restore test | quarterly (policy) — or change policy to semi‑annual, but then do it |
| Change management | per change (PR + CI); population = PRs |
| Policy review / acknowledgment / training | annual, within the period |
| Risk assessment | annual + quarterly register review (task) |
| Vendor review | annual |
| Incident/tabletop | annual tabletop; every incident recorded when it happens |
| Privacy: DSR / DROP / retention | per event + 45‑day / monthly automated records |

### 2.4 Build list (in order, all cheap)

1. CloudTrail bucket lifecycle ≥ 400 d; CloudWatch log retention 400 d or monthly S3 export (1 h).
2. Connect GitHub + AWS + Google Workspace integrations in Comp (3 h; AWS needs the CloudShell role).
3. Branch protection on `main` + the CI branch (already prepared).
4. Scheduled Chrome evidence run (monthly subset + quarterly full) using `evidence/shot-list.json` (needs one successful manual run first — AWS console sign‑in).
5. People onboard/offboard dates; quarterly access‑review task with an export script (`deploy/aws/inventory.sh` + PropelAuth user export) attached automatically.
6. Privacy: custom framework + DSR/suppression/DROP Lambda (§1.3).
7. Pick the Type II start date only after 1–5 are live for a month; the window should not begin before the evidence machinery does.
