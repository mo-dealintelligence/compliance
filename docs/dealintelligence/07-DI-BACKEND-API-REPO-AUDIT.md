# 07 — di-backend-api repository audit (read-only, 2026-10-31)

Scope: `~/dealintel/di-backend-api` (origin `dealintelligence/di-backend-api`),
HEAD 572f2b4 on `main`, in sync with origin. Nothing was changed, moved or
deleted. Findings are ordered by what matters for the audit window and for
handing the repo to another engineer/agent.

## 1. Must fix (security / audit)

| # | Finding | Detail | Suggested action |
|---|---------|--------|------------------|
| 1.1 | **Real secrets are in git history and on origin.** Commit `e0b7b57` (Nov 2025, "Fix Salesforce integration…") added `backups/secrets_backup_20251109_*` — Secrets Manager dumps including the staging secrets bundle (MongoDB Atlas user/password/connection string, DocumentDB user/password/connection string, PropelAuth API key, Apollo key, HubSpot client secret, Salesforce client id), the **prod DocumentDB password**, per-company HubSpot/Salesforce refresh tokens, the jobs Anthropic key, Clearbit and iScraper keys and the master-user-id. Removed from the tree in `61e1ed0` but every clone and GitHub still carry them. | Rotate every value in those files that is still live (prod DocumentDB password first, then PropelAuth, Apollo, HubSpot, Salesforce tokens, Anthropic/Clearbit/iScraper). Then purge with `git filter-repo --path backups --invert-paths`, force-push, and have anyone with a clone re-clone. Record both in Comp as an incident/finding (it is a CC6.1/CC7.3 event). |
| 1.2 | **CI is green-washed and red at the same time.** Every lint/scan/test step ends in `\|\| true` or `continue-on-error: true`, so nothing can fail — except the "Upload evidence to AWS Audit Manager" step, which `exit 1`s when it cannot parse test counts, which is why every push to `main` is red. TruffleHog runs with `base = default branch, head = HEAD` on push events (base == head → "won't scan anything"). | Make lint/tests real gates (drop `\|\| true`), make the Audit-Manager upload non-fatal or remove it (Comp is the evidence system now; that S3 bucket + Lambda were for the Humadroid era), give TruffleHog `fetch-depth: 0` and run it on PRs. Deploy only on green. |
| 1.3 | **No branch protection, direct pushes to `main`, one committer.** | Protect `main` (PR + status checks). Solo self-merge is fine for the auditor if CI gates. |
| 1.4 | `.secrets.baseline` has 692 entries. That many "known false positives" means detect-secrets is effectively disabled. | Regenerate the baseline after 1.1; review what is being whitelisted. |
| 1.5 | GitHub shows 198 open Security & quality alerts; 40 open Dependabot branches (May–Aug 2026) never merged. | Triage: merge the pip/npm bumps that pass, dismiss the rest with a reason. Vulnerability Management Procedure sets SLAs the auditor will sample. |
| 1.6 | `requirements.txt` pins two PropelAuth wheels from a personal GitHub raw URL (`mo-dealintelligence/propelauth-sdk-hosting`). Supply-chain risk and a build that breaks if the repo moves. | Vendor the wheels into the repo (or a private index) and pin by hash. |
| 1.7 | Dockerfiles pin `debian:bookworm-20241202-slim` (Dec 2024); two Dependabot bumps to 2026 images are open. | Merge the bump. |

## 2. Junk in the working tree (safe to delete; none of it is tracked)

| Path | Size | What it is |
|------|------|------------|
| `node_modules/` | 345 MB | Serverless Framework + 2 plugins. Needed only to deploy; keep but it is 55 % of the folder. |
| `.local-docs/` | 143 MB | 90 run artifacts: CSV exports, `cc_cleanup_*` folders, JSON dumps, `REPORT.txt`, a patch. Working data, not source. |
| `.claude/worktrees/` | 17 MB | Two agent worktrees; `agent-a56dcdb7…` is already *prunable*, `agent-a36c…` is locked with 2 unmerged commits (d576425). |
| `anthropic-reviewer-package/` | 19 MB | Screenshots/assets for the MCP connector review submission (git-ignored). Keep if the review is still open, else archive. |
| `.local-backups/` | 7 MB | Pre-change snapshots incl. **`secret-20261023-210822.json`, `secret-all-20261023-210936.json`** — Secrets Manager dumps sitting unencrypted on disk. |
| `.local-secrets/` | 8 KB | `cc_api_keys_2026-10-25.md`, `rep_piatt_rutherford.md` — plaintext keys. |
| `.serverless/` | 4 MB | Packaging cache. |
| `jobs/competitor_customers/_cc_snapshot.tgz`, `_cc_snapshot2.tgz`, `aisearch/`, `baseline/`, `proptech/`, `universes/*.csv`, `glean_lifecycle.csv`, `toloka_dates.csv` | — | Run outputs and ad-hoc data under the source tree. |
| `jobs/di-gdrive-auth-client-0469afbf977c.json` | — | Google service-account key on disk inside the repo folder (ignored, but a `git add -A` away from history). |
| `jobs/.env`, `jobs/.env.bak`, `.env` | — | Fine as ignored files; `.env.bak` is a stale copy. |
| `*.pyc`, `__pycache__/`, `.pytest_cache/`, `.coverage`, `.DS_Store` (tracked once: `app/server/.DS_Store`) | — | Build/OS noise. |
| `ws.pdf` (0 bytes), `convert_to_csv.py` (root), `jobs/apis/remove_me_now` (420 KB tracked Python dict dump of Attention's company record, incl. competitor lists) | — | `remove_me_now` is **tracked** and contains customer data — delete and purge. |

## 3. Tracked files that should not be, or should move

- `jobs/apis/remove_me_now` — see above.
- `jobs/competitor_reachout/*_standalone_old.py` (4 files) — superseded copies kept as `_old`.
- `jobs/scraping_jobs/run_nodriver_v2.py` (416 KB) — a `_v2` beside the original; decide which is live.
- `app/server/.DS_Store`.
- Untracked but sitting in source dirs: `collectors/name_guess.py.pre-2026-10-29`, `supplier_crawl.py.pre-2026-10-29`, `web.py.pre-2026-10-29`, `web.py.pre-2026-10-29b`, `jobs/apis/*.bak` — git already has history; these are manual backups.
- `legal/` (5 design/legal docs) and `jobs/competitor_customers/REVIEW_2026-10-29_*.md` are untracked — either commit them (they look like real docs) or move them to `.local-docs`.
- `.local-scripts/` (18 one-off scripts, e.g. `delete_mo_messidi_lead_events_2026-10-28.py`) — these are the "scratch scripts" that should live in a tracked `scripts/scratch/` folder with a README, per your own rule; today they are invisible to git.

## 4. Uncommitted work

- 20 modified files, +7110/−5700 lines, mostly `jobs/competitor_customers/**` (collectors, lifecycle, methods, schema, profiles) plus `jobs/apis/slack.py`, `subprocessors/__init__.py`, and two staged files (`app/server/database.py`, a test) — a large in-flight change with no commit. Risky to leave: one bad `git checkout` loses it.
- 14 untracked new modules in the same area (`certainty.py`, `disclosure_sweep.py`, `tenant_identify.py`, `subprocessors/{deploygraph,subprocessor_org,venpo}.py`, 4 new profiles, a new test).
- 1 stash (`WIP on main: 6c7ae32 MCP: competitor_customers tool…`).
- Local branches `betterenrich-email-finder` and `disqualify-same-company-and-competitor-leads` are fully merged (0 ahead) — delete; `worktree-agent-a36c…` has 2 unmerged commits — review or drop.

## 5. Structure / hygiene

- **Duplicate module names across `app/server` and `jobs/apis`**: `apollo.py`, `hubspot.py`, `hubspot_with_deals.py`, `slack.py`, `internal.py`, `auth.py`, `env_vars.py`, `telemetry.py`, `onboarding.py`, `v1.py`… Two copies of CRM clients drift independently (e.g. `hubspot_with_deals.py` exists in both). Worth a `packages/`-style shared lib or at least an explicit "which is canonical" note in CLAUDE.md.
- `serverless.yml` is 2,500 lines with ~1,750 lines of raw CloudFormation `Resources`; the 8 functions + Fargate tasks + VPC/DocDB/NAT are all in one file. Splitting into `resources/*.yml` (as the compliance repo does) makes reviews and the IaC evidence legible.
- `app/server/salesforce.py` has 153 `print(` calls, `hubspot*.py` 43 each, `database.py` 38 — logs go to CloudWatch as unstructured stdout, and the PII-sanitising logger the System Monitoring procedure describes is bypassed wherever `print` is used.
- 44 `TODO/FIXME/HACK` markers; 12 unpinned requirements (`>=`) in an otherwise pinned file.
- `deploy.yml` is `workflow_dispatch` only and its ECR build steps are commented out — the documented "CI/CD with staging validation" (CEO evaluation, SDLC standard) is not what the workflow does. Either restore the pipeline or update the policy text.
- `compliance/` (3 monitors) and `scripts/seed_reviewer_org.py` are the only non-jobs scripts; `compliance/google_workspace_manager.py` etc. are the Lambdas cited as evidence — fine, but they deserve tests (none).
- 81 test files exist; with CI never failing, nobody knows the pass rate. Running `pytest` locally once and fixing the red ones is the first step before CI can gate.

## 6. Suggested order

1. Rotate the leaked secrets (1.1), then purge history and force-push; delete `.local-backups/secret-*.json`, `.local-secrets/`, `jobs/di-gdrive-auth-client-*.json` from disk (move keys to the password manager / Secrets Manager).
2. Commit or stash the in-flight competitor_customers work; prune merged branches and the stale worktree.
3. Fix CI (1.2) and protect `main` (1.3); merge the Dependabot bumps.
4. Delete the junk in §2 and §3; add `scripts/scratch/` for one-offs; regenerate `.secrets.baseline`.
5. Structural items in §5 as time allows (serverless split, shared CRM clients, print → logger).
