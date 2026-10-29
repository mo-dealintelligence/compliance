/**
 * Run records live in the Postgres kv_store (via @trycompai/kv/pg) under
 * `run:<id>` with a 7-day TTL. Enough for `runs.retrieve`, progress metadata
 * and idempotency keys; no Trigger.dev dashboard is involved.
 */
import { pgKv } from '@trycompai/kv/pg';

export type RunStatus =
  | 'QUEUED'
  | 'EXECUTING'
  | 'COMPLETED'
  | 'FAILED'
  | 'CANCELED'
  | 'CRASHED'
  | 'SYSTEM_FAILURE'
  | 'INTERRUPTED'
  | 'EXPIRED'
  | 'TIMED_OUT';

export interface RunRecord {
  id: string;
  taskIdentifier: string;
  status: RunStatus;
  payload: unknown;
  output?: unknown;
  error?: { message: string; name?: string; stack?: string };
  metadata: Record<string, unknown>;
  tags: string[];
  attempts: number;
  createdAt: string;
  startedAt?: string;
  finishedAt?: string;
  idempotencyKey?: string;
}

const RUN_TTL_SECONDS = 7 * 24 * 3600;

const keyFor = (id: string) => `run:${id}`;

export function newRunId(): string {
  const rand = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  return `run_${rand}`;
}

export async function saveRun(run: RunRecord): Promise<void> {
  await pgKv.set(keyFor(run.id), run, { ex: RUN_TTL_SECONDS });
}

export async function loadRun(id: string): Promise<RunRecord | null> {
  return pgKv.get<RunRecord>(keyFor(id));
}

export async function patchRun(id: string, patch: Partial<RunRecord>): Promise<RunRecord | null> {
  const current = await loadRun(id);
  if (!current) return null;
  const next = { ...current, ...patch };
  await saveRun(next);
  return next;
}

export async function patchRunMetadata(
  id: string,
  update: (metadata: Record<string, unknown>) => Record<string, unknown>,
): Promise<void> {
  const current = await loadRun(id);
  if (!current) return;
  current.metadata = update(current.metadata ?? {});
  await saveRun(current);
}

export async function lookupIdempotent(key: string): Promise<string | null> {
  return pgKv.get<string>(`idem:${key}`);
}

export async function rememberIdempotent(
  key: string,
  runId: string,
  ttlSeconds: number,
): Promise<void> {
  await pgKv.set(`idem:${key}`, runId, { ex: ttlSeconds });
}
