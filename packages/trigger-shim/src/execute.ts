/**
 * Executes a registered task for a run record: retries per the task's retry
 * options, persists status/output, and runs the task inside its async context.
 */
import { getTask, runContext, type RegisteredTask, type TaskContext } from './registry';
import { loadRun, newRunId, patchRun, saveRun, type RunRecord } from './runs-store';

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

function backoff(task: RegisteredTask, attempt: number): number {
  const { factor = 2, minTimeoutInMs = 1000, maxTimeoutInMs = 10000 } = task.retry ?? {};
  return Math.min(maxTimeoutInMs, minTimeoutInMs * factor ** (attempt - 1));
}

function describeError(error: unknown): RunRecord['error'] {
  if (error instanceof Error)
    return { message: error.message, name: error.name, stack: error.stack };
  return { message: String(error) };
}

export async function createRunRecord(params: {
  taskIdentifier: string;
  payload: unknown;
  tags?: string[];
  idempotencyKey?: string;
  metadata?: Record<string, unknown>;
}): Promise<RunRecord> {
  const run: RunRecord = {
    id: newRunId(),
    taskIdentifier: params.taskIdentifier,
    status: 'QUEUED',
    payload: params.payload,
    metadata: params.metadata ?? {},
    tags: params.tags ?? [],
    attempts: 0,
    createdAt: new Date().toISOString(),
    idempotencyKey: params.idempotencyKey,
  };
  await saveRun(run);
  return run;
}

/** Runs a task to completion in this process. Returns the final run record. */
export async function executeRun(runId: string): Promise<RunRecord> {
  const run = await loadRun(runId);
  if (!run) throw new Error(`[trigger-shim] run ${runId} not found`);
  const task = getTask(run.taskIdentifier);
  if (!task) {
    const failed = await patchRun(runId, {
      status: 'FAILED',
      error: { message: `task ${run.taskIdentifier} is not registered in this worker` },
      finishedAt: new Date().toISOString(),
    });
    return failed ?? run;
  }

  const maxAttempts = Math.max(1, task.retry?.maxAttempts ?? 1);
  let payload = run.payload;
  try {
    payload = task.parse ? task.parse(run.payload) : run.payload;
  } catch (error) {
    const failed = await patchRun(runId, {
      status: 'FAILED',
      error: describeError(error),
      finishedAt: new Date().toISOString(),
    });
    return failed ?? run;
  }

  await patchRun(runId, { status: 'EXECUTING', startedAt: new Date().toISOString() });

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const ctx: TaskContext = {
      run: { id: runId, tags: run.tags, metadata: run.metadata },
      attempt: { number: attempt },
      task: { id: task.id },
    };
    try {
      const output = await runContext.run(ctx, () => task.run(payload, { ctx }));
      const done = await patchRun(runId, {
        status: 'COMPLETED',
        output,
        attempts: attempt,
        finishedAt: new Date().toISOString(),
      });
      return done ?? run;
    } catch (error) {
      console.error(`[trigger-shim] ${task.id} attempt ${attempt}/${maxAttempts} failed`, error);
      await patchRun(runId, { attempts: attempt, error: describeError(error) });
      if (attempt < maxAttempts) {
        await sleep(backoff(task, attempt));
        continue;
      }
      if (task.onFailure) {
        try {
          await runContext.run(ctx, () => task.onFailure!({ payload, error, ctx }));
        } catch (hookError) {
          console.error(`[trigger-shim] ${task.id} onFailure hook failed`, hookError);
        }
      }
      const failed = await patchRun(runId, {
        status: 'FAILED',
        finishedAt: new Date().toISOString(),
      });
      return failed ?? run;
    }
  }
  return run;
}
