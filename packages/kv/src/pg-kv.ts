import { Pool } from 'pg';

/**
 * Postgres-backed key-value store with TTL semantics compatible with the
 * subset of the Upstash Redis client that this codebase uses
 * (get / set / getdel / del / exists / keys / expire / incr / ttl).
 *
 * Backed by the `kv_store` table (see packages/db/prisma/schema/kv-store.prisma).
 * Expired rows are ignored on read and lazily purged on write.
 */
export interface SetOptions {
  ex?: number; // seconds
  px?: number; // milliseconds
  nx?: boolean;
}

let pool: Pool | null = null;

function getPool(): Pool {
  if (!pool) {
    const connectionString = process.env.KV_DATABASE_URL || process.env.DATABASE_URL;
    if (!connectionString) {
      throw new Error('[kv] DATABASE_URL is required for the Postgres KV store');
    }
    pool = new Pool({ connectionString, max: 2, idleTimeoutMillis: 5_000 });
    // The server closes idle sessions (idle_session_timeout) held by frozen Lambda
    // instances; without a listener that 'error' would crash the process.
    pool.on('error', (err) => console.warn('[kv] idle pool client error:', err.message));
  }
  return pool;
}

const ALIVE = `("expires_at" IS NULL OR "expires_at" > NOW())`;
let lastPurge = 0;

async function purgeExpired(): Promise<void> {
  const now = Date.now();
  if (now - lastPurge < 60_000) return;
  lastPurge = now;
  await getPool().query(
    `DELETE FROM "kv_store" WHERE "expires_at" IS NOT NULL AND "expires_at" <= NOW()`,
  );
}

function expiresAtFrom(options?: SetOptions): Date | null {
  if (options?.px) return new Date(Date.now() + options.px);
  if (options?.ex) return new Date(Date.now() + options.ex * 1000);
  return null;
}

export class PgKv {
  async get<T = unknown>(key: string): Promise<T | null> {
    const { rows } = await getPool().query<{ value: T }>(
      `SELECT "value" FROM "kv_store" WHERE "key" = $1 AND ${ALIVE}`,
      [key],
    );
    return rows[0] ? rows[0].value : null;
  }

  async set<T = unknown>(key: string, value: T, options?: SetOptions): Promise<'OK' | null> {
    await purgeExpired();
    const expiresAt = expiresAtFrom(options);
    const conflict = options?.nx
      ? `DO NOTHING`
      : `DO UPDATE SET "value" = EXCLUDED."value", "expires_at" = EXCLUDED."expires_at", "updated_at" = NOW()`;
    const { rowCount } = await getPool().query(
      `INSERT INTO "kv_store" ("key", "value", "expires_at", "updated_at")
       VALUES ($1, $2::jsonb, $3, NOW()) ON CONFLICT ("key") ${conflict}`,
      [key, JSON.stringify(value ?? null), expiresAt],
    );
    return rowCount ? 'OK' : null;
  }

  async getdel<T = unknown>(key: string): Promise<T | null> {
    const { rows } = await getPool().query<{ value: T }>(
      `DELETE FROM "kv_store" WHERE "key" = $1 AND ${ALIVE} RETURNING "value"`,
      [key],
    );
    return rows[0] ? rows[0].value : null;
  }

  async del(...keys: string[]): Promise<number> {
    if (keys.length === 0) return 0;
    const { rowCount } = await getPool().query(`DELETE FROM "kv_store" WHERE "key" = ANY($1)`, [
      keys,
    ]);
    return rowCount ?? 0;
  }

  async exists(key: string): Promise<number> {
    const { rows } = await getPool().query(
      `SELECT 1 FROM "kv_store" WHERE "key" = $1 AND ${ALIVE}`,
      [key],
    );
    return rows.length;
  }

  async keys(pattern: string): Promise<string[]> {
    const like = pattern.replace(/[%_]/g, (m) => `\\${m}`).replace(/\*/g, '%');
    const { rows } = await getPool().query<{ key: string }>(
      `SELECT "key" FROM "kv_store" WHERE "key" LIKE $1 AND ${ALIVE}`,
      [like],
    );
    return rows.map((r) => r.key);
  }

  async expire(key: string, seconds: number): Promise<number> {
    const { rowCount } = await getPool().query(
      `UPDATE "kv_store" SET "expires_at" = NOW() + ($2 || ' seconds')::interval WHERE "key" = $1 AND ${ALIVE}`,
      [key, String(seconds)],
    );
    return rowCount ?? 0;
  }

  async ttl(key: string): Promise<number> {
    const { rows } = await getPool().query<{ secs: number | null }>(
      `SELECT EXTRACT(EPOCH FROM ("expires_at" - NOW()))::int AS secs FROM "kv_store" WHERE "key" = $1 AND ${ALIVE}`,
      [key],
    );
    if (!rows[0]) return -2;
    return rows[0].secs ?? -1;
  }

  async incr(key: string): Promise<number> {
    const { rows } = await getPool().query<{ value: number }>(
      `INSERT INTO "kv_store" ("key", "value", "updated_at") VALUES ($1, '1'::jsonb, NOW())
       ON CONFLICT ("key") DO UPDATE SET
         "value" = CASE WHEN ${ALIVE.replace(/"expires_at"/g, '"kv_store"."expires_at"')}
                        THEN to_jsonb((("kv_store"."value")::text)::bigint + 1) ELSE '1'::jsonb END,
         "expires_at" = CASE WHEN ${ALIVE.replace(/"expires_at"/g, '"kv_store"."expires_at"')}
                        THEN "kv_store"."expires_at" ELSE NULL END,
         "updated_at" = NOW()
       RETURNING ("value")::text::bigint AS value`,
      [key],
    );
    return Number(rows[0]?.value ?? 1);
  }
}

export const pgKv = new PgKv();
