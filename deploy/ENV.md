# Environment reference (Deal Intelligence self-hosted Comp)

Secrets live in AWS Secrets Manager and are injected into ECS task definitions;
never commit real values. Build-time `NEXT_PUBLIC_*` values are baked into the
`app`/`portal` images via `--build-arg`.

## Shared (api, app, portal)

| Var                                                                                                                                          | Value / note                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `DATABASE_URL`                                                                                                                               | RDS Postgres, `?sslmode=require`                                                                                                       |
| `SELF_HOSTED`                                                                                                                                | `true` — turns on the self-hosted feature-flag map, disables vendor gates                                                              |
| `COOKIE_DOMAIN`                                                                                                                              | `.dealintelligence.io` — shares the session across app./api./portal.                                                                   |
| `AUTH_TRUSTED_ORIGINS`                                                                                                                       | `https://compliance.dealintelligence.io,https://compliance-portal.dealintelligence.io,https://compliance-api.dealintelligence.io,https://trust.dealintelligence.io` |
| `AUTH_TRUSTED_ORIGIN_SUFFIXES`                                                                                                               | `dealintelligence.io`                                                                                                                  |
| `RESEND_API_KEY`, `RESEND_FROM_SYSTEM`, `RESEND_FROM_DEFAULT`, `RESEND_FROM_TRUST_PORTAL`, `RESEND_DOMAIN`                                   | Resend on `mail.dealintelligence.io`                                                                                                   |
| `UNSUBSCRIBE_SECRET`                                                                                                                         | `openssl rand -base64 32` (same on api and app)                                                                                        |
| `INTERNAL_API_TOKEN`                                                                                                                         | shared secret api ↔ app/portal                                                                                                         |
| `SERVICE_TOKEN_TRIGGER`, `SERVICE_TOKEN_PORTAL`                                                                                              | per-service tokens the API accepts                                                                                                     |
| `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`                                                                                         | Upstash free tier                                                                                                                      |
| `APP_AWS_REGION`, `APP_AWS_BUCKET_NAME`, `APP_AWS_ORG_ASSETS_BUCKET`, `APP_AWS_QUESTIONNAIRE_UPLOAD_BUCKET`, `APP_AWS_KNOWLEDGE_BASE_BUCKET` | S3 buckets (task role creds preferred; `APP_AWS_ACCESS_KEY_ID/SECRET` only if not on ECS)                                              |
| `OPENAI_API_KEY`                                                                                                                             | optional; AI policy tailoring, chat, questionnaires                                                                                    |
| `NEXT_PUBLIC_BRAND_*`, `NEXT_PUBLIC_WEBSITE_URL`, `NEXT_PUBLIC_SUPPORT_EMAIL`, `NEXT_PUBLIC_TERMS_URL`, `NEXT_PUBLIC_PRIVACY_URL`            | see `packages/utils/src/brand.ts` defaults                                                                                             |

## api

| Var                                    | Value                                                       |
| -------------------------------------- | ----------------------------------------------------------- |
| `BASE_URL`                             | `https://compliance-api.dealintelligence.io`                           |
| `BETTER_AUTH_URL`                      | `https://compliance.dealintelligence.io`                           |
| `NEXT_PUBLIC_APP_URL`                  | `https://compliance.dealintelligence.io`                           |
| `PORTAL_URL`                           | `https://compliance-portal.dealintelligence.io`                        |
| `TRUST_APP_URL`                        | `https://trust.dealintelligence.io`                         |
| `SECRET_KEY`                           | ≥16 chars, `openssl rand -base64 32`                        |
| `AUTH_SECRET`                          | `openssl rand -base64 32`                                   |
| `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET` | Google OAuth client (Workspace)                             |
| `MACED_API_KEY`                        | unset (pentest module inert when `SELF_HOSTED=true`)        |
| `STRIPE_SECRET_KEY`                    | unset                                                       |

## app

| Var                                                | Value                                |
| -------------------------------------------------- | ------------------------------------ |
| `AUTH_SECRET`, `SECRET_KEY`, `REVALIDATION_SECRET` | random                               |
| `BETTER_AUTH_URL`                                  | `https://compliance.dealintelligence.io`    |
| `NEXT_PUBLIC_BETTER_AUTH_URL` (build)              | `https://compliance.dealintelligence.io`    |
| `NEXT_PUBLIC_API_URL` (build)                      | `https://compliance-api.dealintelligence.io`    |
| `NEXT_PUBLIC_PORTAL_URL` (build+run)               | `https://compliance-portal.dealintelligence.io` |
| `NEXT_PUBLIC_TRUST_URL` (build)                    | `https://trust.dealintelligence.io`  |
| `NEXT_PUBLIC_SELF_HOSTED` (build)                  | `true`                               |
| `NEXT_PUBLIC_LOGO_DEV_TOKEN` (build)               | logo.dev publishable key (optional)  |

## portal

| Var                                                          | Value                                        |
| ------------------------------------------------------------ | -------------------------------------------- |
| `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`                      | random; `https://compliance-portal.dealintelligence.io` |
| `NEXT_PUBLIC_BETTER_AUTH_URL`, `NEXT_PUBLIC_API_URL` (build) | portal / api URLs                            |
| `INTERNAL_API_TOKEN`                                         | same as api                                  |

## Background tasks (no Trigger.dev)

`@trigger.dev/sdk` resolves to `packages/trigger-shim`: `tasks.trigger()` does
an async `lambda:Invoke` of the service's `worker` function (`TASK_WORKER_FUNCTION`,
set by `deploy/aws/env.js`), runs are stored in the Postgres `kv_store`, and the
cron tasks are EventBridge schedules generated into `deploy/aws/{api,app}/schedules.yml`
by `node deploy/aws/gen-schedules.mjs <registry _schedules.json>` after
`node packages/trigger-shim/bin/gen-registry.mjs <trigger dir>`.
