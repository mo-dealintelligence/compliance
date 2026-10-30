# Disaster recovery runbook — Comp (compliance.dealintelligence.io)

Everything needed to rebuild is in three places: this repo, the Aurora
backups/snapshots in the `di-compliance` account, and one secrets backup file
kept outside the repo. Nothing lives only on a laptop.

## What is backed up, and where

| Thing | Where | Retention |
|---|---|---|
| Database (all compliance content) | Aurora automated backups (`comp-db`) | 14 days, point-in-time |
| Database, manual | `deploy.sh snapshot` → `comp-prod-db-<date>`; cluster deletion also snapshots | until deleted |
| Evidence files, policy PDFs | S3 `comp-evidence-775524235093`, versioned | until deleted |
| App secrets (`SECRET_KEY`, `AUTH_SECRET`, OAuth, Resend…) | Secrets Manager `comp/env/{api,app,portal}` **and** `~/di-run-logs/comp-deploy/secrets-backup.json` (written by `bootstrap`, refresh with `secrets.sh backup`) | keep the file in a password manager / encrypted drive |
| Infra | this repo (`deploy/aws`) | git |
| Third-party inputs (Google OAuth client, Resend key) | `~/di-run-logs/comp-deploy/secrets-input.json` | keep with the backup above |

`ENCRYPTION_KEY` matters most: it encrypts integration credentials stored in
the database (`SECRET_KEY`/`AUTH_SECRET` sign sessions). A restored database
with a regenerated `ENCRYPTION_KEY` loses every connected integration.
That is why `secrets.sh init` refuses to run over existing secrets.

## Scenarios

### A. A deploy failed halfway
Re-run the step that failed; every step is idempotent (`infra`, `build`,
`functions`, `bootstrap`). Nothing needs cleaning up first.

### B. Bad data / need yesterday's database (same stack)
1. `deploy.sh snapshot` (keep the current state too).
2. Restore point-in-time in the RDS console to a new cluster
   `comp-db-restored`, or use `aws rds restore-db-cluster-to-point-in-time`.
3. Point the apps at it: `secrets.sh set api DATABASE_URL …` (×3), then
   `deploy.sh functions` to roll the Lambdas.
   Or swap by renaming clusters so the endpoint stays `comp-db`.

### C. The whole account/stack is gone (or we move accounts)
Prereqs: repo, `deploy/aws/.env` (prod keys + `COMP_ACCOUNT_ID` of the new
account), `secrets-backup.json`, a shared or copied DB snapshot (share the
snapshot with the new account if it is a different one).

```
cd ~/dealintel/compliance/deploy/aws
deploy.sh restore <snapshot-id>      # infra from snapshot → delegate → secrets (restored) → build → functions → smoke
```
With no snapshot at all (start over): `deploy.sh bootstrap` — same flow with
`secrets.sh init` and the framework seed; content is re-imported with
`scripts/di-migration` from the Google Drive export.

Afterwards: re-add the three hostnames + callback in the Google OAuth client
only if the hostnames changed; Resend DNS lives in the prod zone and survives.

### D. Lost the secrets backup but the account is fine
`secrets.sh backup` right now. (If both the account and the file are lost, the
integration credentials are gone — reconnect AWS/GitHub/Google Workspace in
the UI; everything else is rebuilt by `bootstrap`.)

## Quarterly check (put on the Comp task list)
- `deploy.sh snapshot` and `secrets.sh backup`; copy the file to the vault.
- Confirm the Aurora automated backup window shows restorable points.
- Dry run: `serverless print --stage prod --param=phase=infra` must resolve.
