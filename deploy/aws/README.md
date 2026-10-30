# AWS deployment (Serverless Framework, scale-to-zero)

Topology (us-east-1, same account as `di-backend-api-prod`):

```
compliance.dealintelligence.io        -> CloudFront -> Lambda URL (comp-app)        Next.js admin
compliance-api.dealintelligence.io    -> CloudFront -> Lambda URL (comp-api)        NestJS + better-auth
compliance-portal.dealintelligence.io -> CloudFront -> Lambda URL (comp-portal)     employee portal
                                         +-> worker Lambdas (comp-app-worker, comp-api-worker) via async invoke + EventBridge crons
trust.dealintelligence.io  -> existing DI trust center (unchanged)
Aurora Serverless v2 Postgres 16 (0–2 ACU, auto-pause), public TLS endpoint
S3 comp-evidence-<acct> (SSE, versioned, private)
Trigger.dev Cloud (2 projects), Resend, Upstash Redis — SaaS
```

Why public DB endpoint: Trigger.dev Cloud workers (which send every email and
run schedules) must reach Postgres from outside AWS, so the Lambdas stay out of
the VPC as well and no NAT gateway is needed. Protection: `rds.force_ssl=1`,
32-char managed master password in Secrets Manager, security group, and the
cluster is only reachable by password. Revisit (VPC + NAT + self-hosted
Trigger) if the tool ever enters SOC 2 scope.

Costs at idle ≈ $0 for compute/API; Aurora pauses after 10 min idle
(storage only); S3 pennies.

## One-time

```
export AWS_PROFILE=... AWS_DEFAULT_REGION=us-east-1
deploy/aws/deploy.sh infra
deploy/aws/secrets.sh init        # writes comp/env/{api,app,portal} from a filled template
SEED=true deploy/aws/deploy.sh build      # builds images, migrates, seeds frameworks
export HOSTED_ZONE_ID=Z...
deploy/aws/deploy.sh functions
```

Then: deploy Trigger.dev tasks (`bunx trigger.dev deploy` in `apps/app` and
`apps/api` with `TRIGGER_PROJECT_REF`), add the Google OAuth redirect
`https://compliance-api.dealintelligence.io/api/auth/callback/google`, and sign in.

## Every release

```
deploy/aws/deploy.sh build && deploy/aws/deploy.sh functions
```

## Limits worth knowing

- Lambda function URLs cap request bodies at 6 MB; larger uploads go through
  presigned S3 URLs (the app does this for policies and task attachments).
- Web Lambdas time out at 120 s; background work runs on the worker Lambdas
  (15 min) and EventBridge crons. CloudFront fronts the function URLs only to
  provide the custom hostnames and TLS.
- Cold start for the Next.js app is a few seconds after idle.
