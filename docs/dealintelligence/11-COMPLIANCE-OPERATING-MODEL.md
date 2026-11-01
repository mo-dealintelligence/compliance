# 11 — Compliance operating model: automate everything, batch the rest (2026-10-31)

Goal set by Mo: stay compliant for a SOC 2 Type II with the least recurring
effort — automated evidence wherever possible, screenshots where there is no
API, manual controls pushed to the longest cadence the criteria allow, and
the manual ones batched so they are done in one sitting.

Target steady state: **~1 hour per quarter + ~2 days per year of Mo's time.**
Everything else runs on its own and lands in Comp with a timestamp.

## 1. The four mechanisms (build once)

| # | Mechanism | What it produces | Cost | Build effort |
|---|---|---|---|---|
| M1 | **Comp integrations** — GitHub, AWS (read‑only role), Google Workspace | daily pass/fail per check, attached to controls (branch protection, 2FA, Dependabot, code scanning; CloudTrail, SGs, IAM, KMS rotation, S3 encryption/public access; Workspace 2‑step, user list) | $0 | ~3 h total; AWS needs the CloudShell role (you) |
| M2 | **Scheduled Chrome evidence run** (Claude scheduled task on the Mac, signed‑in browser) | screenshots from `evidence/shot-list.json` uploaded to the right Comp task, run log `runs/<date>.json` | $0 | shot list + uploader exist; needs one successful manual run with AWS console signed in, then schedule |
| M3 | **Evidence‑poster Lambdas** in di‑backend‑api (EventBridge → Lambda → Comp API) | structured records in Comp forms/tasks: access‑review export (IAM + PropelAuth + Workspace users), retention purge count, backup‑restore test result, Security Hub summary, monthly availability % | cents | 1–2 days once; reuses the existing `accessReview` and `dataRetentionEnforcement` Lambdas (add a "post to Comp" step) |
| M4 | **Comp task schedule** (already running: 12‑hourly cron flips due tasks to `todo`, Monday reminder email) | the manual calendar below, with dated completion as evidence | $0 | set frequencies/review dates once (script) |

## 2. Control calendar — cadence chosen to minimise your work

Cadences below are the longest an auditor will accept for a one‑person
company given what the policies say; where a policy says something shorter,
the policy line to amend is noted.

### Continuous / daily — zero touch (M1, M3)
CloudTrail on, SGs not open, IAM password policy/MFA, KMS rotation, S3
encryption + block public access, branch protection, 2FA, Dependabot, code
scanning, Workspace 2‑step, employee list sync, ECR scan results, Security
Hub findings.

### Monthly — zero touch (M2 screenshots + M3 records)
| Control | Evidence | Who |
|---|---|---|
| Monitoring & alerting in place | screenshots: CloudWatch alarms, log groups/retention, Security Hub summary + findings, SNS topics | M2 |
| Vulnerability status | screenshots: ECR repos/scan results, Dependabot alerts page, Security & quality tab | M2 |
| Retention enforced | record: rows purged by `dataRetentionEnforcement` | M3 |
| Availability | record: monthly uptime % from CloudWatch (API 5xx / invocations) | M3 |
| Security Hub review | record: open findings by severity + "reviewed" flag — **this is the one monthly click**: approve the record (2 min) | M3 → you |

### Quarterly — ~1 hour, one sitting
| Control | Evidence | Mechanism |
|---|---|---|
| Access review (IAM, PropelAuth, GitHub, Workspace) | auto‑generated RBAC‑matrix/access‑review record; you review and approve (15 min) | M3 + approve |
| Management review / meeting minutes (CC1.2, CC4.1) | Comp `board-meeting` form **prefilled** by M3 with the quarter's numbers (uptime, incidents, vulns, access changes, risks); you add decisions and submit (20 min) | M3 prefill + you |
| Risk register review | task: open Risks page, confirm or edit, mark done (10 min) | M4 |
| Full screenshot sweep | all 48 shots (M2 handles; you only sign into AWS console if the session expired) | M2 |
| Backup restore test | **automated**: Lambda restores latest snapshot to a temp cluster, runs a document count, deletes the cluster, posts a `tabletop-exercise`/record with timings (RTO achieved) — a few dollars of DocumentDB per run | M3 |

### Semi‑annual — 30 min
| Control | Evidence |
|---|---|
| Privileged‑access audit (Access Control policy says semi‑annual) | same auto record as the quarterly review, filtered to admin roles; approve |

### Annual — "compliance week": ~2 days, batched in the same month every year
| Control | What you do | Prep I automate |
|---|---|---|
| Policy review | open each policy, confirm or edit, re‑publish (v+0.1), re‑acknowledge; William acknowledges in portal | script flips all 24 to `needs_review` on the anniversary; changelog line template |
| Security awareness training | you + William watch Comp's 5 videos; certificate auto‑generated | reminder task |
| Risk assessment | annual pass over the 7 risks + add/remove; residual scores | Comp risk form |
| Vendor review | confirm SOC 2 reports/DPAs for AWS, PropelAuth, Google, GitHub, Resend; attach | task with links to each vendor's trust page |
| Tabletop exercise (incident) | 45‑minute scenario walk‑through recorded in the `tabletop-exercise` form | scenario template prefilled |
| Penetration test | engage vendor; attach report to `penetration-test` form | vendor shortlist |
| Performance evaluation (CEO self‑eval) + contractor review | `employee-performance-evaluation` form | prefilled with the year's metrics |
| Privacy: LIA, RoPA, privacy notice, "not a CCPA business" memo | confirm still true; re‑date | template docs in Comp |
| Code of Conduct / AUP acknowledgment | portal click for both of you | M4 |
| Inventory & network diagram refresh | regenerate from `inventory.sh` + Mermaid; submit forms | script |

### Per event — only when it happens
Incident → `findings`/IR record; new hire/contractor → People + onboarding
checklist; offboarding → checklist (access revocation); new vendor → vendor
record; DSR → DSR record; emergency change → PR with "emergency" label.

## 3. Policy lines to amend to match this calendar
- Incident Response: "quarterly tabletop + annual simulation" → annual tabletop.
- Security Awareness: training within 5 days / quizzes / phishing → onboarding + annual videos.
- BCP: quarterly restore test stays (automated); failover test semi‑annual → covered by the same automated restore (reword).
- Monitoring: "daily security alert review" → automated daily checks + monthly reviewed record.
- Change Mgmt: 48‑h CAB review → PR + CI gate, self‑approval allowed for sole operator, emergency label.
- Vendor: quarterly performance/SLA reviews → annual review + continuous availability record.

## 4. Build order (all cheap; ~1 week of my time, ~3 h of yours)

1. **M4 now**: set task frequencies/review dates to the calendar above (script; 1 h).
2. **M1**: connect GitHub + Google Workspace (you authorise, 10 min each); AWS role via CloudShell (you, 10 min).
3. **M2**: one manual run with AWS console signed in → create the scheduled task (monthly subset, quarterly full).
4. **M3a**: `accessReview` and `dataRetentionEnforcement` Lambdas post a record to Comp (API key in Secrets Manager) — half a day.
5. **M3b**: monthly Security Hub + availability record; quarterly minutes prefill — half a day.
6. **M3c**: automated restore test — 1 day (restore → count → delete → record); protects the BCP claim.
7. Annual pack: policy `needs_review` flip script, prefilled annual forms, vendor links — half a day, before the first anniversary (Nov 13).

After step 3 the Type II evidence machine is running; start the observation window one month later.
