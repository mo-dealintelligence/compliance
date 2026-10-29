/**
 * Task registry + execution context. Each process (web Lambda or worker
 * Lambda) registers every task module at startup by importing it; the worker
 * then executes by task id.
 */
import { AsyncLocalStorage } from 'node:async_hooks';

export interface RetryOptions {
  maxAttempts?: number;
  factor?: number;
  minTimeoutInMs?: number;
  maxTimeoutInMs?: number;
  randomize?: boolean;
}

export interface TaskContext {
  run: { id: string; tags: string[]; metadata: Record<string, unknown> };
  attempt: { number: number };
  task: { id: string };
}

export interface RegisteredTask {
  id: string;
  cron?: string;
  retry?: RetryOptions;
  maxDurationSeconds?: number;
  run: (payload: unknown, ctx: { ctx: TaskContext }) => Promise<unknown>;
  parse?: (payload: unknown) => unknown;
  onFailure?: (params: {
    payload: unknown;
    error: unknown;
    ctx: TaskContext;
  }) => Promise<unknown> | unknown;
}

// Process-global so the CJS and ESM builds (and any duplicate copies loaded
// by a bundler) share one registry and one run context.
type Globals = {
  __compTriggerRegistry?: Map<string, RegisteredTask>;
  __compTriggerRunContext?: AsyncLocalStorage<TaskContext>;
};
const g = globalThis as unknown as Globals;
const registry = (g.__compTriggerRegistry ??= new Map<string, RegisteredTask>());

export function registerTask(task: RegisteredTask): void {
  registry.set(task.id, task);
}

export function getTask(id: string): RegisteredTask | undefined {
  return registry.get(id);
}

export function listTasks(): RegisteredTask[] {
  return [...registry.values()];
}

export function listSchedules(): { id: string; cron: string }[] {
  return listTasks()
    .filter((t): t is RegisteredTask & { cron: string } => typeof t.cron === 'string')
    .map((t) => ({ id: t.id, cron: t.cron }));
}

/** Per-run async context so `metadata`, `tags` and `logger` know which run they belong to. */
export const runContext = (g.__compTriggerRunContext ??= new AsyncLocalStorage<TaskContext>());

export function currentContext(): TaskContext | undefined {
  return runContext.getStore();
}
