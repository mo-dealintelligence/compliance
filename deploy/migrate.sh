#!/usr/bin/env bash
# One-shot migration (and optional seed) task. Runs inside the `migrator`
# image from /app/packages/db. Requires DATABASE_URL.
set -euo pipefail

: "${DATABASE_URL:?DATABASE_URL is required}"

# Aurora Serverless v2 may be auto-paused (0 ACU). The first connection wakes
# it, which can take ~30-60 s, so retry the migration itself.
echo "==> prisma migrate deploy"
for i in $(seq 1 10); do
  if bunx prisma migrate deploy --schema=prisma/schema; then break; fi
  [ "$i" = 10 ] && { echo "database still unreachable after 10 attempts"; exit 1; }
  echo "   attempt $i failed (database waking up?), retrying in 20s"; sleep 20
done

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
