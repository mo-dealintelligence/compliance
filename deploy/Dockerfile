# =============================================================================
# Deal Intelligence self-hosted build of Comp AI Community Edition.
#
# One Dockerfile, four runnable targets:
#   --target api       NestJS API + better-auth            (port 3333)
#   --target app       Next.js admin app                   (port 3000)
#   --target portal    Next.js employee portal             (port 3000)
#   --target migrator  prisma migrate deploy + optional seed (one-shot)
#
# Build from the repo root:
#   docker build -f deploy/Dockerfile --target api -t comp-api .
#
# NEXT_PUBLIC_* values are inlined at build time; pass them as --build-arg.
# =============================================================================

ARG BUN_VERSION=1.4.4
ARG NODE_VERSION=22.23.4
# AWS Lambda Web Adapter lets the unmodified HTTP servers run on Lambda.
ARG LWA_VERSION=0.9.1

# -----------------------------------------------------------------------------
# deps: install the whole workspace once (cached by lockfile)
# -----------------------------------------------------------------------------
FROM oven/bun:${BUN_VERSION} AS deps
WORKDIR /app
COPY package.json bun.lock bunfig.toml ./
COPY packages/analytics/package.json ./packages/analytics/
COPY packages/auth/package.json ./packages/auth/
COPY packages/billing/package.json ./packages/billing/
COPY packages/company/package.json ./packages/company/
COPY packages/db/package.json ./packages/db/
COPY packages/email/package.json ./packages/email/
COPY packages/integration-platform/package.json ./packages/integration-platform/
COPY packages/integrations/package.json ./packages/integrations/
COPY packages/kv/package.json ./packages/kv/
COPY packages/tsconfig/package.json ./packages/tsconfig/
COPY packages/ui/package.json ./packages/ui/
COPY packages/utils/package.json ./packages/utils/
COPY apps/api/package.json ./apps/api/
COPY apps/app/package.json ./apps/app/
COPY apps/portal/package.json ./apps/portal/
RUN PRISMA_SKIP_POSTINSTALL_GENERATE=true bun install --frozen-lockfile --ignore-scripts

# -----------------------------------------------------------------------------
# workspace: source + built shared packages (db client generated here)
# -----------------------------------------------------------------------------
FROM deps AS workspace
COPY packages ./packages
COPY apps/api ./apps/api
COPY apps/app ./apps/app
COPY apps/portal ./apps/portal
RUN cd packages/db && bun run build
RUN cd packages/auth && bun run build \
 && cd ../kv && bun run build \
 && cd ../integration-platform && bun run build \
 && cd ../email && bun run build \
 && cd ../company && bun run build \
 && cd ../billing && bun run build

# -----------------------------------------------------------------------------
# migrator: prisma migrate deploy (+ seed when SEED=true)
# -----------------------------------------------------------------------------
FROM workspace AS migrator
WORKDIR /app/packages/db
COPY deploy/migrate.sh /usr/local/bin/migrate.sh
RUN chmod +x /usr/local/bin/migrate.sh
CMD ["/usr/local/bin/migrate.sh"]

# -----------------------------------------------------------------------------
# api
# -----------------------------------------------------------------------------
FROM workspace AS api-builder
RUN find /app/packages/db/prisma/schema -name '*.prisma' ! -name 'schema.prisma' \
      -exec cp {} /app/apps/api/prisma/schema/ \; \
 && cd /app/apps/api && bunx nest build

FROM node:${NODE_VERSION}-slim AS api
ARG LWA_VERSION
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
RUN groupadd --system nestjs && useradd --system --gid nestjs --create-home nestjs
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
      wget ca-certificates fontconfig fonts-dejavu-core openssl \
 && wget -q -O /usr/local/share/aws-rds-ca-bundle.pem \
      https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/aws-rds-ca-bundle.pem
COPY --from=api-builder --chown=nestjs:nestjs /app/apps/api/dist ./dist
COPY --from=api-builder --chown=nestjs:nestjs /app/apps/api/prisma ./prisma
COPY --from=api-builder --chown=nestjs:nestjs /app/apps/api/package.json ./package.json
COPY --from=api-builder --chown=nestjs:nestjs /app/packages ./packages
COPY --from=api-builder --chown=nestjs:nestjs /app/node_modules ./node_modules
ENV NODE_ENV=production PORT=3333 \
    AWS_LWA_PORT=3333 AWS_LWA_READINESS_CHECK_PATH=/v1/health AWS_LWA_ASYNC_INIT=true
USER nestjs
EXPOSE 3333
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3333/v1/health || exit 1
CMD ["node", "--report-on-fatalerror", "--report-compact", "dist/src/main.js"]

# -----------------------------------------------------------------------------
# app (Next.js admin)
# -----------------------------------------------------------------------------
FROM workspace AS app-builder
ARG NEXT_PUBLIC_BETTER_AUTH_URL
ARG NEXT_PUBLIC_APP_URL
ARG NEXT_PUBLIC_PORTAL_URL
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_TRUST_URL
ARG NEXT_PUBLIC_SELF_HOSTED=true
ARG NEXT_PUBLIC_APP_ENV=production
ARG NEXT_PUBLIC_BRAND_NAME
ARG NEXT_PUBLIC_BRAND_PRODUCT_NAME
ARG NEXT_PUBLIC_WEBSITE_URL
ARG NEXT_PUBLIC_SUPPORT_EMAIL
ARG NEXT_PUBLIC_TERMS_URL
ARG NEXT_PUBLIC_PRIVACY_URL
ARG NEXT_PUBLIC_BRAND_LOGO_URL
ARG NEXT_PUBLIC_LOGO_DEV_TOKEN
ARG NEXT_PUBLIC_POSTHOG_KEY
ARG NEXT_PUBLIC_POSTHOG_HOST
ARG NEXT_PUBLIC_SENTRY_DSN
ENV NEXT_PUBLIC_BETTER_AUTH_URL=$NEXT_PUBLIC_BETTER_AUTH_URL \
    NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL \
    NEXT_PUBLIC_PORTAL_URL=$NEXT_PUBLIC_PORTAL_URL \
    NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_PUBLIC_TRUST_URL=$NEXT_PUBLIC_TRUST_URL \
    NEXT_PUBLIC_SELF_HOSTED=$NEXT_PUBLIC_SELF_HOSTED \
    NEXT_PUBLIC_APP_ENV=$NEXT_PUBLIC_APP_ENV \
    NEXT_PUBLIC_BRAND_NAME=$NEXT_PUBLIC_BRAND_NAME \
    NEXT_PUBLIC_BRAND_PRODUCT_NAME=$NEXT_PUBLIC_BRAND_PRODUCT_NAME \
    NEXT_PUBLIC_WEBSITE_URL=$NEXT_PUBLIC_WEBSITE_URL \
    NEXT_PUBLIC_SUPPORT_EMAIL=$NEXT_PUBLIC_SUPPORT_EMAIL \
    NEXT_PUBLIC_TERMS_URL=$NEXT_PUBLIC_TERMS_URL \
    NEXT_PUBLIC_PRIVACY_URL=$NEXT_PUBLIC_PRIVACY_URL \
    NEXT_PUBLIC_BRAND_LOGO_URL=$NEXT_PUBLIC_BRAND_LOGO_URL \
    NEXT_PUBLIC_LOGO_DEV_TOKEN=$NEXT_PUBLIC_LOGO_DEV_TOKEN \
    NEXT_PUBLIC_POSTHOG_KEY=$NEXT_PUBLIC_POSTHOG_KEY \
    NEXT_PUBLIC_POSTHOG_HOST=$NEXT_PUBLIC_POSTHOG_HOST \
    NEXT_PUBLIC_SENTRY_DSN=$NEXT_PUBLIC_SENTRY_DSN \
    SELF_HOSTED=true \
    NEXT_TELEMETRY_DISABLED=1 NODE_ENV=production \
    NEXT_OUTPUT_STANDALONE=true \
    NODE_OPTIONS=--max_old_space_size=8192
RUN cd apps/app && SKIP_ENV_VALIDATION=true bun run build:docker

FROM node:${NODE_VERSION}-alpine AS app
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=app-builder /app/apps/app/.next/standalone ./
COPY --from=app-builder /app/apps/app/.next/static ./apps/app/.next/static
COPY --from=app-builder /app/apps/app/public ./apps/app/public
COPY deploy/next-entrypoint.sh /usr/local/bin/next-entrypoint.sh
# Lambda's filesystem is read-only except /tmp; Next writes its runtime cache there.
RUN chmod +x /usr/local/bin/next-entrypoint.sh \
 && rm -rf apps/app/.next/cache && ln -s /tmp/next-cache apps/app/.next/cache
ENV NODE_ENV=production PORT=3000 HOSTNAME=0.0.0.0 NEXT_APP_DIR=apps/app \
    AWS_LWA_PORT=3000 AWS_LWA_READINESS_CHECK_PATH=/api/health AWS_LWA_ASYNC_INIT=true
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
CMD ["/usr/local/bin/next-entrypoint.sh"]

# -----------------------------------------------------------------------------
# portal (Next.js employee portal)
# -----------------------------------------------------------------------------
FROM workspace AS portal-builder
ARG NEXT_PUBLIC_BETTER_AUTH_URL
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_APP_URL
ARG NEXT_PUBLIC_PORTAL_URL
ARG NEXT_PUBLIC_BRAND_NAME
ARG NEXT_PUBLIC_WEBSITE_URL
ARG NEXT_PUBLIC_SUPPORT_EMAIL
ARG NEXT_PUBLIC_BRAND_LOGO_URL
ARG NEXT_PUBLIC_SENTRY_DSN
ENV NEXT_PUBLIC_BETTER_AUTH_URL=$NEXT_PUBLIC_BETTER_AUTH_URL \
    NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_PUBLIC_APP_URL=$NEXT_PUBLIC_APP_URL \
    NEXT_PUBLIC_PORTAL_URL=$NEXT_PUBLIC_PORTAL_URL \
    NEXT_PUBLIC_BRAND_NAME=$NEXT_PUBLIC_BRAND_NAME \
    NEXT_PUBLIC_WEBSITE_URL=$NEXT_PUBLIC_WEBSITE_URL \
    NEXT_PUBLIC_SUPPORT_EMAIL=$NEXT_PUBLIC_SUPPORT_EMAIL \
    NEXT_PUBLIC_BRAND_LOGO_URL=$NEXT_PUBLIC_BRAND_LOGO_URL \
    NEXT_PUBLIC_SENTRY_DSN=$NEXT_PUBLIC_SENTRY_DSN \
    NEXT_TELEMETRY_DISABLED=1 NODE_ENV=production \
    NEXT_OUTPUT_STANDALONE=true \
    NODE_OPTIONS=--max_old_space_size=6144
RUN cp packages/db/dist/schema.prisma apps/portal/prisma/schema.prisma \
 && cd apps/portal && SKIP_ENV_VALIDATION=true bun run build:docker

FROM node:${NODE_VERSION}-alpine AS portal
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
WORKDIR /app
RUN apk add --no-cache curl
COPY --from=portal-builder /app/apps/portal/.next/standalone ./
COPY --from=portal-builder /app/apps/portal/.next/static ./apps/portal/.next/static
COPY --from=portal-builder /app/apps/portal/public ./apps/portal/public
COPY deploy/next-entrypoint.sh /usr/local/bin/next-entrypoint.sh
RUN chmod +x /usr/local/bin/next-entrypoint.sh \
 && rm -rf apps/portal/.next/cache && ln -s /tmp/next-cache apps/portal/.next/cache
ENV NODE_ENV=production PORT=3000 HOSTNAME=0.0.0.0 NEXT_APP_DIR=apps/portal \
    AWS_LWA_PORT=3000 AWS_LWA_READINESS_CHECK_PATH=/ AWS_LWA_ASYNC_INIT=true
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1
CMD ["/usr/local/bin/next-entrypoint.sh"]
