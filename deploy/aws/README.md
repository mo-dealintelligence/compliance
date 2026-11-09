# AWS deployment (single Serverless Framework stack, scale-to-zero)

Account: `di-compliance` (member of the dealintelligence Organization; nothing
shared with the production account). Treated as a self-hosted vendor tool,
outside the SOC 2 system boundary.

```
compliance.dealintelligence.io         -> CloudFront -> Lambda URL (comp-app)     Next.js admin
api.compliance.dealintelligence.io     -> CloudFront -> Lambda URL (comp-api)     NestJS + better-auth
portal.compliance.dealintelligence.io  -> CloudFront -> Lambda URL (comp-portal)  employee portal
                                          +-> comp-prod-apiWorker / comp-prod-appWorker (async invoke + EventBridge crons)
VPC 10.42.0.0/24: 1 public subnet (t4g.micro NAT instance), 2 private subnets (Lambdas, Aurora, CodeBuild)
Aurora Serverless v2 Postgres 16, private, 0-2 ACU, auto-pause 10 min, force SSL
S3 evidence bucket (SSE, versioned, private) via gateway endpoint; S3 source bucket for CodeBuild
Route 53 zone compliance.dealintelligence.io (delegated by one NS record in the prod zone)
Outside AWS: Resend (email), Google Workspace (sign-in). Trust center stays on SafeBase.
```

## One-time

```
cp deploy/aws/.env.example deploy/aws/.env            # fill in the prod keys; git-ignored, scripts source it
deploy/aws/deploy.sh infra                            # ~15 min (Aurora); prints the zone's name servers
deploy/aws/deploy.sh delegate                         # NS record in dealintelligence.io (prod creds)
deploy/aws/secrets.sh init                            # writes comp/env/{api,app,portal}
SEED=true deploy/aws/deploy.sh build                  # CodeBuild: images -> ECR, migrate, seed frameworks
deploy/aws/deploy.sh functions                        # lambdas + cloudfront + dns
deploy/aws/smoke.sh                                   # hits the three hostnames
```

Then add the Google OAuth redirect `https://api.compliance.dealintelligence.io/api/auth/callback/google`
and the JS origins for the three hostnames, and sign in.

## Every release

```
deploy/aws/deploy.sh build && deploy/aws/deploy.sh functions
```

Cron tasks: after changing `schedules.task` definitions, regenerate
`apps/*/src/trigger/**/_registry.ts` + `_schedules.json`
(`node packages/trigger-shim/bin/gen-registry.mjs <dir>`) and
`deploy/aws/schedules-{api,app}.yml` (`node deploy/aws/gen-schedules.mjs <json>`).

## Limits worth knowing

- Lambda function URLs cap request bodies at 6 MB; larger uploads use presigned S3 URLs.
- Web Lambdas: 120 s; workers: 15 min. CloudFront exists only for hostnames + TLS.
- The NAT instance is the single egress path for private subnets (t4g.micro, ~$6/mo).

## Database password rotation (off since 2026-11-09)

The Aurora master password is an RDS-managed secret (`ManageMasterUserPassword: true`). RDS
enables 7-day rotation on it by default, but the functions get `DATABASE_URL` baked into their
environment at deploy time (`env.js`), so every rotation broke the app (AuthenticationFailed,
pages timing out) until `secrets.sh refresh-db-url` + a functions deploy. Rotation was
cancelled on 2026-11-09 (`aws secretsmanager cancel-rotate-secret` on the `rds!cluster-…`
secret). If it is ever re-enabled, the apps must read the password from that secret at runtime
first. Comp is outside the SOC 2 system boundary, so no policy depends on this rotation.

Recovery if the password changes anyway: `bash secrets.sh refresh-db-url && bash deploy.sh functions`.
