# 05 — Open gaps and later work (hand-off list)

Status as of 2026-10-30. Items here are not blocking the Comp cut-over but
must be closed before a SOC 2 Type II observation window is clean. Each can
be handed to another agent independently; the context needed is in this
folder and in `scripts/di-migration/`.

## A. Findings from the 2026-10-30 evidence pass

| # | Finding | Where | Why it matters | Fix |
|---|---------|-------|----------------|-----|
| A1 | `dealintelligence/di-backend-api` CI Pipeline fails on every push to `main` (runs #289–#293, Oct 26–28). `lint-and-test` exits 1 in ~8s; `compliance-check` exits 1 (TruffleHog: "BASE and HEAD commits are the same" on direct pushes); `docker-build` never runs. | GitHub Actions | CC8.1 / SDLC standard say CI gates deploys. Auditor samples recent changes. | Fix lint job; TruffleHog step needs `fetch-depth: 0` and `base`/`head` on push (or run only on PRs); deploy only on green CI. |
| A2 | Commits go straight to `main` by one account; no PR trail. | GitHub | Change-management evidence (review/approval) is absent for the Type II window. | Branch protection on `main` (PR required, status checks), work on branches, self-merge is acceptable for a solo operator if CI gates. |
| A3 | 198 open "Security and quality" alerts (Dependabot/code scanning). | GitHub | Vulnerability Management Procedure sets remediation SLAs. | Triage: dismiss non-applicable, fix/upgrade the rest, record the triage. |
| A4 | GitHub 2FA relies on SMS (banner warning). | GitHub | Access Control policy; SMS is weak MFA. | Add TOTP/passkey on the `mo-dealintelligence` account. |
| A5 | ECR `serverless-di-backend-jobs-production` and `serverless-di-backend-api-production` have scan-on-push **off**. | AWS 164482277879 | Evaluation/minutes claim container scanning on all images. | Enable scan-on-push (or registry-level scanning) and record. |
| A6 | `HumadroidComplianceRole` IAM role + CloudFormation stack still in prod. | AWS | Orphaned third-party access path after Humadroid retirement. | Delete after Comp's AWS integration role is in place (Mo runs the delete). |
| A7 | PropelAuth: password login off (Google SSO only); "Require all users to set up 2FA" off (plan-gated). | PropelAuth | MFA is inherited from Google Workspace; say so in the system description instead of "PropelAuth MFA". | Update system description wording; optionally enforce 2-step verification in Google Admin and screenshot that. |
| A9 | Production uses **one** KMS customer-managed key; the Encryption Standard v2 (per Mo, 2026-10-31) keeps the key-separation design (data / backup / audit-log keys). | AWS 164482277879 | Policy claim ahead of the environment until the keys are split. | Create the backup and audit-log CMKs (annual rotation), re-point DocumentDB snapshot copies and the CloudTrail bucket; add to `compliance/env-alignment`. |
| A8 | Pentest: last report not yet attached; minutes committed to an annual test (Q1 2026 action item). | Comp | CC4.1 / Pentest procedure. | Attach report via the `penetration-test` evidence form (Mo to provide file). |
| A10 | Security Hub is still enabled in account 164482277879 ($5.87/mo) although the v2 policies, controls and records no longer cite it (D12, 2026-10-31). | AWS 164482277879 | Running a control the documentation does not claim is wasted spend and an auditor question; the replacement (monthly configuration-check Lambda + CloudTrail-EventBridge security-event rule → breach-detection Lambda → SNS) must be live first so there is no detection gap. | Mo disables Security Hub (and the FSBP standard) in us-east-1 **after** the configuration-check Lambda and the EventBridge rule are deployed and have posted their first record to Comp (docs/11 §4 step 5, M3b). |
| A11 | **Staging in a separate AWS account** (Mo, 2026-10-31, supersedes the same-account plan). | AWS Organization | Policies v2 state a staging environment in a separate account, outside the SOC 2 boundary. | Create the member account; SSO/role (`OrganizationAccountAccessRole`); own CloudTrail trail; cross-account ECR pull (or a staging ECR); parameterise the 11 hardcoded `*-production-*` names; deploy with scrubbed or synthetic data only. ~$15-25/mo (t3.micro NAT + serverless DocumentDB). Add to `compliance/env-alignment`. |
| A12 | **Remove the `documentdb-proxy` Lambda** (Mo, 2026-11-01). | di-backend-api `serverless.yml` | The function, its function URL, IAM role and DocumentDB SG rule are an unused path to the database. The v2.0 network flow diagram already omits it. | Delete the function + URL from `serverless.yml`, drop its SG ingress on the DocumentDB SG, redeploy, confirm no CloudWatch invocations in the last 30 days first. |

## B. Comp platform follow-ups

- Native evidence records (board meeting Q4‑2025, CEO evaluation 2025, BCP full test 2026‑02‑04, RBAC matrix, infra inventory) are scripted in `scripts/di-migration/evidence/native-records.ts`; they need the API build that includes commit 6c6719246 (API-key callers attributed to the acting member).
- Stuck onboarding job `run_ck0nptjgmvulz115` keeps the "AI is analyzing your organization" banner on the Risks page: `bash deploy/aws/ops.sh run-status app run_ck0nptjgmvulz115 COMPLETED` after the rebuild.
- 8 generic draft policies (`data/repo-policies/state.json`) still present: `bun scripts/di-migration/import/cleanup-templates.ts --apply`. 34 Comp seed-template drafts remain; optional.
- Evidence screenshots: GitHub (11) on hold until A1/A2; AWS (21) need Mo signed in to the console in Chrome; Comp (7) after the banner clears. Captured so far: PropelAuth 5/5 in `~/di-run-logs/comp-deploy/evidence-2026-10-30/` (to be uploaded with `evidence/upload.ts`).
- Scheduled evidence task (monthly/quarterly per `evidence/shot-list.json`) to be created once one full manual run has succeeded.
- M3 build list (docs/11 §4): M3a access-review + retention Lambdas post to Comp; **M3b configuration-check Lambda** (monthly EventBridge schedule → fixed checklist: CloudTrail on + log-file validation, no public S3, no SGs open to 0.0.0.0/0 on admin ports, root MFA, IAM password policy, KMS rotation, ECR scan-on-push, DocumentDB backup retention → dated pass/fail record to the Comp task "Configuration-check record (monthly)") plus the security-event EventBridge rule → breach-detection Lambda → SNS, and the availability record posted to the Comp task "Availability record (monthly)" (D12, D13b); M3c automated restore test. A10 (disable Security Hub) follows M3b.
- William: portal invite, policy acknowledgments, security-training videos (both people).
- Delete `~/dealintel/di-compliance` (9.3 GB) and `~/dealintel/di-compliance-local` (2.4 GB) once everything above is verified.
- Cold-start: if Aurora auto-pause causes failed first requests, add a 1–2× client-side retry on app entry paths (keep scale-to-zero).
- Optional: onboarding/policy-tailoring AI gateway → direct Anthropic.

## C. di-backend-api auth hardening (decided later, after Comp is done)

Mo is leaning to A + B + D from `/areas/di-backend-api-auth` analysis:
- A: stop accepting `master_user_id` / `user_id` as the auth principal in URL paths; require a bearer token (PropelAuth access token) and derive the principal server-side.
- B: per-customer API keys issued and stored hashed, scoped to the tenant, rotation + revocation, audit on use.
- D: a single internal "operator" credential for diagnostics/standalone scripts (e.g. `generate_user_slack_notification_standalone.py`), short-lived, logged.
- Also: remove `verify_user_or_master` case 3; update `di-platform-frontend` axios calls only where they currently send no token.
Risk notes and cost comparison are in the memory file / earlier analysis; re-confirm with Mo before starting.
