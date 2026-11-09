import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import { resolveSslConfig } from './ssl-config';

export type { SslConfig } from './ssl-config';
export { resolveSslConfig } from './ssl-config';

const globalForPrisma = global as unknown as { prisma?: PrismaClient };

function stripSslMode(connectionString: string): string {
  const url = new URL(connectionString);
  url.searchParams.delete('sslmode');
  return url.toString();
}

function createPrismaClient(): PrismaClient {
  const rawUrl = process.env.DATABASE_URL!;
  const ssl = resolveSslConfig(rawUrl);
  const url = ssl !== undefined ? stripSslMode(rawUrl) : rawUrl;
  // Small per-process pool: on Lambda every warm instance holds its own pool, and the
  // serverless Aurora cluster (max 2 ACU) refuses connections past its limit
  // (TooManyConnections). DB_POOL_MAX overrides; idle connections close quickly.
  const max = Number(process.env.DB_POOL_MAX ?? 2);
  const adapter = new PrismaPg({
    connectionString: url,
    ssl,
    max: Number.isFinite(max) && max > 0 ? max : 2,
    idleTimeoutMillis: 5_000,
    connectionTimeoutMillis: 60_000,
  });
  return new PrismaClient({
    adapter,
    transactionOptions: { timeout: 60000 },
  });
}

// Lazy initialization. Importing this module does NOT construct a Prisma client
// — that only happens on first property access on `db`. Critical so that
// Next.js `next build` (which imports every route handler to analyze it) does
// not trigger the strict TLS check at build time when no actual queries run.
function getClient(): PrismaClient {
  if (!globalForPrisma.prisma) {
    globalForPrisma.prisma = createPrismaClient();
  }
  return globalForPrisma.prisma;
}

export const db = new Proxy({} as PrismaClient, {
  get(_target, prop, _receiver) {
    const client = getClient();
    const value = Reflect.get(client, prop, client);
    return typeof value === 'function' ? value.bind(client) : value;
  },
});
