#!/usr/bin/env bash
# One-shot migration (and optional seed) task. Runs inside the `migrator`
# image from /app/packages/db. Requires DATABASE_URL.
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"

# Aurora Serverless v2 may be auto-paused (0 ACU); the first connection wakes
# it and can take ~30 s. Retry instead of failing the deploy.
echo "==> waiting for database"
for i in $(seq 1 20); do
  if bunx prisma db execute --schema=prisma/schema --stdin <<<'SELECT 1' >/dev/null 2>&1; then break; fi
  echo "   not reachable yet (attempt $i/20), retrying in 15s"; sleep 15
done

echo "==> prisma migrate deploy"
bunx prisma migrate deploy --schema=prisma/schema

# The generate_prefixed_cuid() helper is created by migrations, but older
# dumps may lack it. Re-applying is idempotent (CREATE OR REPLACE).
if [ -f prisma/functionDefinition.sql ]; then
  echo "==> ensuring generate_prefixed_cuid() exists"
  bunx prisma db execute --schema=prisma/schema --file prisma/functionDefinition.sql || true
fi

if [ "${SEED:-false}" = "true" ]; then
  echo "==> seeding framework templates"
  bun prisma/seed/seed.ts
fi

echo "==> done"
