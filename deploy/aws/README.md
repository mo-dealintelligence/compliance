# AWS deployment (Serverless Framework, scale-to-zero)

Topology (us-east-1, same account as `di-backend-api-prod`):

```
compliance.dealintelligence.io    -> HTTP API -> Lambda (container: comp-app)    Next.js admin
compliance-api.dealintelligence.io    -> HTTP API -> Lambda (container: comp-api)    NestJS + better-auth
compliance-portal.dealintelligence.io -> HTTP API -> Lambda (container: comp-portal) employee portal
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
export VPC_ID=vpc-xxxx SUBNET_IDS=subnet-a,subnet-b     # default VPC public subnets
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

- HTTP API request body limit is 10 MB; uploads larger than that go through
  presigned S3 URLs (the app does this for policies and task attachments).
- Lambda timeout is 29 s (API Gateway cap). Long work runs in Trigger.dev.
- Cold start for the Next.js app is a few seconds after idle.
