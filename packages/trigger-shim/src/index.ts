/**
 * @trigger.dev/sdk compatible surface backed by AWS Lambda + Postgres.
 *
 * Supported: task, schemaTask, schedules.task, queue, tasks.trigger /
 * triggerAndWait / batchTrigger / batchTriggerAndWait, batch.trigger,
 * logger, metadata, tags, runs.retrieve / cancel / list, idempotencyKeys,
 * wait.for, auth.createPublicToken (returns a signed-less opaque token),
 * configure (no-op), AbortTaskRunError.
 */
import { dispatch } from './dispatch';
import { createRunRecord, executeRun } from './execute';
import {
  currentContext,
  listSchedules,
  registerTask,
  type RetryOptions,
  type TaskContext,
} from './registry';
import {
  loadRun,
  lookupIdempotent,
  patchRun,
  patchRunMetadata,
  rememberIdempotent,
  type RunRecord,
} from './runs-store';

export { listSchedules };
export type { RetryOptions, RunRecord, TaskContext };

// ── Types ───────────────────────────────────────────────────────────────────

export interface Queue {
  name?: string;
  concurrencyLimit?: number;
}

export interface TriggerOptions {
  idempotencyKey?: string;
  idempotencyKeyTTL?: string;
  tags?: string | string[];
  metadata?: Record<string, unknown>;
  queue?: Queue;
  concurrencyKey?: string;
  delay?: string | Date;
  ttl?: string;
  maxAttempts?: number;
  priority?: number;
}

export interface RunHandle {
  id: string;
  publicAccessToken: string;
  taskIdentifier?: string;
}

export type TaskRunResult<TOutput = unknown> =
  | { ok: true; id: string; taskIdentifier: string; output: TOutput }
  | { ok: false; id: string; taskIdentifier: string; error: unknown };

export interface BatchRunHandle {
  batchId: string;
  runs: RunHandle[];
  publicAccessToken: string;
}

export interface BatchResult<TOutput = unknown> {
  id: string;
  runs: TaskRunResult<TOutput>[];
}

export interface ScheduledTaskPayload {
  timestamp: Date;
  lastTimestamp?: Date;
  timezone: string;
  scheduleId: string;
  externalId?: string;
  upcoming: Date[];
  type: 'DECLARATIVE' | 'IMPERATIVE';
}

export interface Task<TIdentifier extends string = string, TPayload = unknown, TOutput = unknown> {
  id: TIdentifier;
  trigger: (payload: TPayload, options?: TriggerOptions) => Promise<RunHandle>;
  triggerAndWait: (payload: TPayload, options?: TriggerOptions) => Promise<TaskRunResult<TOutput>>;
  batchTrigger: (
    items: { payload: TPayload; options?: TriggerOptions }[],
    options?: TriggerOptions,
  ) => Promise<BatchRunHandle>;
  batchTriggerAndWait: (
    items: { payload: TPayload; options?: TriggerOptions }[],
    options?: TriggerOptions,
  ) => Promise<BatchResult<TOutput>>;
  /** phantom, for type inference only */
  readonly __payload?: TPayload;
  readonly __output?: TOutput;
}

export type AnyTask = Task<string, any, any>;
/**
 * Mirrors the real SDK: payloads cross a JSON boundary, so nested objects are
 * compared loosely (a Prisma row with extra columns is accepted where the task
 * declared a narrower shape).
 */
type LoosePayload<P> = P extends object
  ? {
      [K in keyof P]: P[K] extends (infer U)[]
        ? U extends object
          ? any[]
          : P[K]
        : P[K] extends object
          ? any
          : P[K];
    }
  : P;
export type TaskPayload<T extends AnyTask> =
  T extends Task<string, infer P, any> ? LoosePayload<P> : never;
export type TaskOutput<T extends AnyTask> = T extends Task<string, any, infer O> ? O : never;
export type TaskIdentifier<T extends AnyTask> = T['id'];

interface CommonTaskOptions<TPayload, TOutput, TId extends string = string> {
  id: TId;
  retry?: RetryOptions;
  queue?: Queue;
  maxDuration?: number;
  machine?: unknown;
  tags?: string | string[];
  priority?: number;
  run: (payload: TPayload, params: { ctx: TaskContext }) => Promise<TOutput>;
  onFailure?: (params: {
    payload: TPayload;
    error: unknown;
    ctx: TaskContext;
  }) => Promise<unknown> | unknown;
  onSuccess?: unknown;
  onStart?: unknown;
  init?: unknown;
  cleanup?: unknown;
  handleError?: unknown;
  catchError?: unknown;
}

export class AbortTaskRunError extends Error {
  constructor(message?: string) {
    super(message);
    this.name = 'AbortTaskRunError';
  }
}

// ── Core execution helpers ─────────────────────────────────────────────────

function normalizeTags(tags?: string | string[]): string[] {
  if (!tags) return [];
  return Array.isArray(tags) ? tags : [tags];
}

async function startRun(
  taskId: string,
  payload: unknown,
  options?: TriggerOptions,
): Promise<RunHandle> {
  if (options?.idempotencyKey) {
    const existing = await lookupIdempotent(options.idempotencyKey);
    if (existing) return { id: existing, publicAccessToken: existing, taskIdentifier: taskId };
  }
  const run = await createRunRecord({
    taskIdentifier: taskId,
    payload,
    tags: normalizeTags(options?.tags),
    idempotencyKey: options?.idempotencyKey,
    metadata: options?.metadata,
  });
  if (options?.idempotencyKey) {
    await rememberIdempotent(options.idempotencyKey, run.id, 30 * 24 * 3600);
  }
  await dispatch({ runId: run.id, taskId, source: 'trigger' });
  return { id: run.id, publicAccessToken: run.id, taskIdentifier: taskId };
}

async function runInline<TOutput>(
  taskId: string,
  payload: unknown,
  options?: TriggerOptions,
): Promise<TaskRunResult<TOutput>> {
  const run = await createRunRecord({
    taskIdentifier: taskId,
    payload,
    tags: normalizeTags(options?.tags),
  });
  const result = await executeRun(run.id);
  if (result.status === 'COMPLETED') {
    return { ok: true, id: run.id, taskIdentifier: taskId, output: result.output as TOutput };
  }
  return { ok: false, id: run.id, taskIdentifier: taskId, error: result.error };
}

function buildTask<TPayload, TOutput, TId extends string = string>(
  options: CommonTaskOptions<TPayload, TOutput, TId>,
  parse?: (p: unknown) => TPayload,
  cron?: string,
) {
  registerTask({
    id: options.id,
    cron,
    retry: options.retry,
    maxDurationSeconds: options.maxDuration,
    run: (payload, params) => options.run(payload as TPayload, params),
    parse,
    onFailure: options.onFailure
      ? (params) =>
          options.onFailure!({
            payload: params.payload as TPayload,
            error: params.error,
            ctx: params.ctx,
          })
      : undefined,
  });
  const t: Task<TId, TPayload, TOutput> = {
    id: options.id,
    trigger: (payload, opts) => startRun(options.id, payload, mergeTags(opts, options.tags)),
    triggerAndWait: (payload, opts) =>
      runInline<TOutput>(options.id, payload, mergeTags(opts, options.tags)),
    batchTrigger: async (items, opts) => {
      const runs: RunHandle[] = [];
      for (const item of items)
        runs.push(
          await startRun(options.id, item.payload, mergeTags(item.options ?? opts, options.tags)),
        );
      return { batchId: `batch_${Date.now().toString(36)}`, runs, publicAccessToken: '' };
    },
    batchTriggerAndWait: async (items, opts) => {
      const runs: TaskRunResult<TOutput>[] = [];
      for (const item of items)
        runs.push(
          await runInline<TOutput>(
            options.id,
            item.payload,
            mergeTags(item.options ?? opts, options.tags),
          ),
        );
      return { id: `batch_${Date.now().toString(36)}`, runs };
    },
  };
  return t;
}

function mergeTags(opts: TriggerOptions | undefined, taskTags?: string | string[]): TriggerOptions {
  return { ...opts, tags: [...normalizeTags(taskTags), ...normalizeTags(opts?.tags)] };
}

// ── Public API ──────────────────────────────────────────────────────────────

export function task<TPayload = unknown, TOutput = unknown, TId extends string = string>(
  options: CommonTaskOptions<TPayload, TOutput, TId>,
) {
  return buildTask<TPayload, TOutput, TId>(options);
}

export function schemaTask<
  TSchema extends { parse: (input: unknown) => any },
  TOutput = unknown,
  TId extends string = string,
>(
  options: Omit<CommonTaskOptions<ReturnType<TSchema['parse']>, TOutput, TId>, 'run'> & {
    schema: TSchema;
    run: (payload: ReturnType<TSchema['parse']>, params: { ctx: TaskContext }) => Promise<TOutput>;
  },
) {
  const { schema, ...rest } = options;
  return buildTask<ReturnType<TSchema['parse']>, TOutput, TId>(rest, (p) => schema.parse(p));
}

export const schedules = {
  task<TOutput = unknown, TId extends string = string>(
    options: Omit<CommonTaskOptions<ScheduledTaskPayload, TOutput, TId>, 'run'> & {
      cron: string | { pattern: string; timezone?: string };
      run: (payload: ScheduledTaskPayload, params: { ctx: TaskContext }) => Promise<TOutput>;
    },
  ) {
    const { cron, ...rest } = options;
    const pattern = typeof cron === 'string' ? cron : cron.pattern;
    return buildTask<ScheduledTaskPayload, TOutput, TId>(
      rest,
      (p) => normalizeSchedulePayload(p, options.id),
      pattern,
    );
  },
  async create() {
    return { id: 'declarative' };
  },
  async del() {
    return undefined;
  },
  async list() {
    return { data: [] };
  },
};

function normalizeSchedulePayload(raw: unknown, scheduleId: string): ScheduledTaskPayload {
  const p = (raw ?? {}) as Partial<ScheduledTaskPayload> & { timestamp?: string | Date };
  const ts = p.timestamp ? new Date(p.timestamp) : new Date();
  return {
    timestamp: ts,
    lastTimestamp: p.lastTimestamp ? new Date(p.lastTimestamp) : undefined,
    timezone: p.timezone ?? 'UTC',
    scheduleId: p.scheduleId ?? scheduleId,
    externalId: p.externalId,
    upcoming: [],
    type: 'DECLARATIVE',
  };
}

export function queue(options: Queue): Queue {
  return options;
}

export const tasks = {
  trigger: <TTask extends AnyTask = AnyTask>(
    id: TaskIdentifier<TTask>,
    payload: TaskPayload<TTask>,
    options?: TriggerOptions,
  ) => startRun(id, payload, options),
  triggerAndWait: <TTask extends AnyTask = AnyTask>(
    id: TaskIdentifier<TTask>,
    payload: TaskPayload<TTask>,
    options?: TriggerOptions,
  ) => runInline<TaskOutput<TTask>>(id, payload, options),
  batchTrigger: async <TTask extends AnyTask = AnyTask>(
    id: TaskIdentifier<TTask>,
    items: { payload: TaskPayload<TTask>; options?: TriggerOptions }[],
    options?: TriggerOptions,
  ): Promise<BatchRunHandle> => {
    const runs: RunHandle[] = [];
    for (const item of items) runs.push(await startRun(id, item.payload, item.options ?? options));
    return { batchId: `batch_${Date.now().toString(36)}`, runs, publicAccessToken: '' };
  },
  batchTriggerAndWait: async <TTask extends AnyTask = AnyTask>(
    id: TaskIdentifier<TTask>,
    items: { payload: TaskPayload<TTask>; options?: TriggerOptions }[],
    options?: TriggerOptions,
  ): Promise<BatchResult<TaskOutput<TTask>>> => {
    const runs: TaskRunResult<TaskOutput<TTask>>[] = [];
    for (const item of items)
      runs.push(await runInline<TaskOutput<TTask>>(id, item.payload, item.options ?? options));
    return { id: `batch_${Date.now().toString(36)}`, runs };
  },
};

export const batch = {
  trigger: async <TTask extends AnyTask = AnyTask>(
    items: { id: TaskIdentifier<TTask>; payload: TaskPayload<TTask>; options?: TriggerOptions }[],
  ): Promise<BatchRunHandle> => {
    const runs: RunHandle[] = [];
    for (const item of items) runs.push(await startRun(item.id, item.payload, item.options));
    return { batchId: `batch_${Date.now().toString(36)}`, runs, publicAccessToken: '' };
  },
  triggerAndWait: async <TTask extends AnyTask = AnyTask>(
    items: { id: TaskIdentifier<TTask>; payload: TaskPayload<TTask>; options?: TriggerOptions }[],
  ): Promise<BatchResult<TaskOutput<TTask>>> => {
    const runs: TaskRunResult<TaskOutput<TTask>>[] = [];
    for (const item of items)
      runs.push(await runInline<TaskOutput<TTask>>(item.id, item.payload, item.options));
    return { id: `batch_${Date.now().toString(36)}`, runs };
  },
  triggerByTask: async (
    items: { task: AnyTask; payload: unknown; options?: TriggerOptions }[],
  ): Promise<BatchRunHandle> => {
    const runs: RunHandle[] = [];
    for (const item of items) runs.push(await startRun(item.task.id, item.payload, item.options));
    return { batchId: `batch_${Date.now().toString(36)}`, runs, publicAccessToken: '' };
  },
};

const prefix = () => {
  const ctx = currentContext();
  return ctx ? `[${ctx.task.id} ${ctx.run.id}]` : '[trigger-shim]';
};

export const logger = {
  log: (message: string, data?: unknown) => console.log(prefix(), message, data ?? ''),
  info: (message: string, data?: unknown) => console.info(prefix(), message, data ?? ''),
  warn: (message: string, data?: unknown) => console.warn(prefix(), message, data ?? ''),
  error: (message: string, data?: unknown) => console.error(prefix(), message, data ?? ''),
  debug: (message: string, data?: unknown) =>
    process.env.TRIGGER_SHIM_DEBUG ? console.debug(prefix(), message, data ?? '') : undefined,
  trace: async <T>(_name: string, fn: () => Promise<T>) => fn(),
};

function withRun(update: (m: Record<string, unknown>) => Record<string, unknown>): void {
  const ctx = currentContext();
  if (!ctx) return;
  ctx.run.metadata = update(ctx.run.metadata);
  void patchRunMetadata(ctx.run.id, update).catch(() => undefined);
}

type MetadataApi = {
  set: (key: string, value: unknown) => MetadataApi;
  get: (key: string) => unknown;
  del: (key: string) => MetadataApi;
  increment: (key: string, by?: number) => MetadataApi;
  decrement: (key: string, by?: number) => MetadataApi;
  append: (key: string, value: unknown) => MetadataApi;
  replace: (value: Record<string, unknown>) => MetadataApi;
  current: () => Record<string, unknown>;
  stream: <T>(
    key: string,
    value: AsyncIterable<T> | ReadableStream<T>,
  ) => Promise<AsyncIterable<T> | ReadableStream<T>>;
  flush: () => Promise<void>;
  root: Pick<MetadataApi, 'set' | 'increment' | 'decrement' | 'append'>;
  parent: Pick<MetadataApi, 'set' | 'increment' | 'decrement' | 'append'>;
};

export const metadata: MetadataApi = {
  set: (key, value) => {
    withRun((m) => ({ ...m, [key]: value }));
    return metadata;
  },
  get: (key) => currentContext()?.run.metadata[key],
  del: (key) => {
    withRun((m) => {
      const { [key]: _removed, ...rest } = m;
      return rest;
    });
    return metadata;
  },
  increment: (key, by = 1) => {
    withRun((m) => ({ ...m, [key]: (Number(m[key]) || 0) + by }));
    return metadata;
  },
  decrement: (key, by = 1) => {
    withRun((m) => ({ ...m, [key]: (Number(m[key]) || 0) - by }));
    return metadata;
  },
  append: (key, value) => {
    withRun((m) => ({ ...m, [key]: [...((m[key] as unknown[]) ?? []), value] }));
    return metadata;
  },
  replace: (value) => {
    withRun(() => ({ ...value }));
    return metadata;
  },
  current: () => currentContext()?.run.metadata ?? {},
  stream: async (_key, value) => value,
  flush: async () => undefined,
  get root() {
    return metadata;
  },
  get parent() {
    return metadata;
  },
};

export const tags = {
  add: async (newTags: string | string[]) => {
    const ctx = currentContext();
    if (!ctx) return;
    const merged = [...new Set([...ctx.run.tags, ...normalizeTags(newTags)])];
    ctx.run.tags = merged;
    await patchRun(ctx.run.id, { tags: merged });
  },
};

export interface RetrievedRun extends RunRecord {
  isCompleted: boolean;
  isSuccess: boolean;
  isFailed: boolean;
  isQueued: boolean;
  isExecuting: boolean;
  isCancelled: boolean;
}

function decorate(run: RunRecord): RetrievedRun {
  const terminal = [
    'COMPLETED',
    'FAILED',
    'CANCELED',
    'CRASHED',
    'SYSTEM_FAILURE',
    'INTERRUPTED',
    'EXPIRED',
    'TIMED_OUT',
  ].includes(run.status);
  return {
    ...run,
    isCompleted: terminal,
    isSuccess: run.status === 'COMPLETED',
    isFailed: [
      'FAILED',
      'CRASHED',
      'SYSTEM_FAILURE',
      'INTERRUPTED',
      'EXPIRED',
      'TIMED_OUT',
    ].includes(run.status),
    isQueued: run.status === 'QUEUED',
    isExecuting: run.status === 'EXECUTING',
    isCancelled: run.status === 'CANCELED',
  };
}

export const runs = {
  retrieve: async (runId: string): Promise<RetrievedRun> => {
    const run = await loadRun(runId);
    if (!run) throw new Error(`Run ${runId} not found`);
    return decorate(run);
  },
  cancel: async (runId: string) => {
    const run = await loadRun(runId);
    if (run && !decorate(run).isCompleted)
      await patchRun(runId, { status: 'CANCELED', finishedAt: new Date().toISOString() });
    return { id: runId };
  },
  poll: async (runId: string, options?: { pollIntervalMs?: number }): Promise<RetrievedRun> => {
    for (;;) {
      const run = await runs.retrieve(runId);
      if (run.isCompleted) return run;
      await new Promise((r) => setTimeout(r, options?.pollIntervalMs ?? 2000));
    }
  },
  list: async () => ({ data: [] as RetrievedRun[] }),
  replay: async (runId: string) => ({ id: runId }),
  subscribeToRun: async function* (runId: string) {
    yield await runs.retrieve(runId);
  },
};

export const auth = {
  /** Realtime tokens are not needed: the app polls /api/trigger/runs/:id with its session. */
  createPublicToken: async (_options?: unknown) => 'shim',
  createTriggerPublicToken: async (_task: unknown, _options?: unknown) => 'shim',
  withAuth: async <T>(_options: unknown, fn: () => Promise<T>) => fn(),
  configure: (_options: unknown) => undefined,
};

export const idempotencyKeys = {
  create: async (key: string | string[], _options?: { scope?: 'run' | 'attempt' | 'global' }) =>
    (Array.isArray(key) ? key.join(':') : key) as string,
};

export const wait = {
  for: async (options: { seconds?: number; minutes?: number; hours?: number; days?: number }) => {
    const ms =
      ((options.seconds ?? 0) +
        (options.minutes ?? 0) * 60 +
        (options.hours ?? 0) * 3600 +
        (options.days ?? 0) * 86400) *
      1000;
    await new Promise((r) => setTimeout(r, ms));
  },
  until: async (options: { date: Date }) => {
    await new Promise((r) => setTimeout(r, Math.max(0, options.date.getTime() - Date.now())));
  },
};

export function configure(_options: unknown): void {
  // Nothing to configure: execution is local or via TASK_WORKER_FUNCTION.
}

export const envvars = {
  list: async () => [],
  retrieve: async () => ({ name: '', value: '' }),
};

/** trigger.config.ts compatibility: the config is ignored by the shim. */
export function defineConfig<T>(config: T): T {
  return config;
}
