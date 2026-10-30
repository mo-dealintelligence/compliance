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
export AWS_PROFILE=<management account> AWS_DEFAULT_REGION=us-east-1
export COMP_ACCOUNT_ID=<di-compliance account id>   # deploy.sh assumes OrganizationAccountAccessRole
deploy/aws/deploy.sh infra                            # ~15 min (Aurora); prints the zone's name servers
PROD_ZONE_ID=Z0889255QBJMQ8IWV1X2 deploy/aws/deploy.sh delegate   # NS record in dealintelligence.io (prod creds)
SECRETS_INPUT=~/comp-input.json deploy/aws/secrets.sh init        # writes comp/env/{api,app,portal}
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
