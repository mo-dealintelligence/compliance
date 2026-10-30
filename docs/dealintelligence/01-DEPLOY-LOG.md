# Deploy log and learnings — 2026-10-29 first deploy

Account `di-compliance` (775524235093, member of the DI Organization), stack
`comp-prod`, region us-east-1. Code lives at `~/dealintel/compliance` on Mo's
Mac (branch `di/self-host`, fork `mo-dealintelligence/compliance`).

## What finally worked (in order)

1. `deploy.sh infra` — VPC, NAT instance, private Aurora, S3, ECR, CodeBuild,
   Route 53 zone, ACM certs. The certs block until the zone is delegated.
2. NS record for `compliance.dealintelligence.io` in the prod zone
   (`Z0889255QBJMQ8IWV1X2`) pointing at the new zone's name servers.
3. `secrets.sh init` → `comp/env/{api,app,portal}`.
4. `SEED=true deploy.sh build` — CodeBuild builds six images, runs
   `prisma migrate deploy` (291 migrations) and the framework seed.
5. `deploy.sh functions` — five Lambdas, three function URLs, CloudFront, DNS.
6. `smoke.sh`.

## Problems hit, and the fix that stuck

| Symptom | Cause | Fix |
|---|---|---|
| CodeBuild `ecr get-login-password` hangs 195 s, no logs | Private subnets had no working egress: NAT instance booted without a masquerade rule | AL2023 minimal has no `nftables`/`iptables`; `dnf` is OOM-killed on t4g.**nano** (512 MB), even with swap. Use **t4g.micro** + `dnf install iptables-services` (same recipe as di-backend-api). |
| `docker buildx build requires 1 argument` | `NEXT_PUBLIC_*` build args with spaces word-split | bash + `mapfile` into an array, `--build-arg=K=V` |
| Next type check fails on `scripts/backfill-training-videos.ts` | trigger shim required a payload arg; real SDK makes it optional for payload-less tasks | `TriggerArgs<TPayload>` conditional tuple in the shim |
| Next type check fails on upstream `*.test.tsx` | upstream test drift | exclude `*.test.*` / `*.spec.*` in `apps/app/tsconfig.json` |
| Portal: `Module "@db" has no exported member 'Device'` | builder copied a merged `schema.prisma` next to the schema dir | sync `packages/db/prisma/schema/*.prisma` into the app's schema dir instead (same as the API stage) |
| Migrations: `P1001 can't reach database` | Aurora Serverless v2 auto-paused (0 ACU); Prisma gives up after 5 s | retry `migrate deploy` (10×20 s) + `connect_timeout=60` on every `DATABASE_URL` |
| Seed: `unable to get local issuer certificate` | direct Aurora endpoint chains to the regional RDS CA, not in Node/bun trust store | ship `global-bundle.pem` in every image, `NODE_EXTRA_CA_CERTS` + `DATABASE_SSL_CA_FILE` (seed and `resolveSslConfig` read it) |
| Lambda: `Ignoring extra certs … Permission denied` | `ADD <url>` creates the file 600/root; Lambda runs non-root | `ADD --chmod=644` |
| Function URL → 403 `Forbidden` with correct `InvokeFunctionUrl` policy | since Oct 2025 public function URLs also need `lambda:InvokeFunction`; Serverless v3 only adds the first | explicit `AWS::Lambda::Permission` ×3 in `resources-edge.yml` (`InvokedViaFunctionUrl: true`) |
| API: `Cannot find module '@db'` at runtime | Nest's path-alias rewrite didn't happen in the container build | `alias-register.cjs` loaded with `-r` / `NODE_OPTIONS` in both API images |
| API: `MacedClient: apiKey must start with mc_live_` | placeholder key for the pentest vendor SDK | module is inert without `MACED_API_KEY` (no client constructed) |

## Operating notes

- Cold start after >10 min idle: Aurora resumes in ~15–60 s; CloudFront waits 30 s.
  Decision (Mo): keep scale-to-zero; if it bites, add a client-side retry on the
  app's entry paths rather than raising min ACU.
- Cost: ~$10/mo idle, ~$20–30/mo in use (NAT micro ~$6, Aurora only while awake).
- Every `deploy.sh build` rebuilds whatever Dockerfile layers changed; a
  no-change rebuild is ~3 min thanks to ECR layer cache.
- The Mac's awscli is v1 (`pip --user`); `date -v` is BSD-only there — the
  helper scripts use `python3` for JSON and avoid GNU-only flags.
- Old attempts to delete once this is verified: `~/dealintel/di-compliance`
  (9.3 GB) and `~/dealintel/di-compliance-local` (2.4 GB).
