/**
 * Lambda worker handler. The app/api worker entrypoint imports its task
 * registry (so every task registers) and re-exports `handler`.
 *
 * Events:
 *   { source: 'trigger',  runId }            — from tasks.trigger()
 *   { source: 'schedule', taskId, payload? } — from EventBridge rules
 *   { source: 'admin', action: 'set-run-status', runId, status, error? }
 *                                            — operator tool (self-hosted): resolve a
 *                                              run that died with the worker, e.g. an
 *                                              onboarding run stuck in EXECUTING
 */
import type { WorkerEvent } from './dispatch';
import { createRunRecord, executeRun } from './execute';
import { getTask, listSchedules } from './registry';
import { loadRun, patchRun } from './runs-store';

export { listSchedules };

export async function handler(
  event: WorkerEvent & {
    detail?: unknown;
    action?: string;
    status?: string;
    error?: string;
  },
): Promise<{ runId: string; status: string }> {
  if ((event.source as string) === 'admin') {
    if (event.action !== 'set-run-status' || !event.runId || !event.status)
      throw new Error('[trigger-shim] admin event needs action=set-run-status, runId, status');
    const run = await loadRun(event.runId);
    if (!run) throw new Error(`[trigger-shim] run ${event.runId} not found`);
    await patchRun(event.runId, {
      status: event.status as never,
      finishedAt: new Date().toISOString(),
      ...(event.error ? { error: { message: event.error } } : {}),
    } as never);
    return { runId: event.runId, status: event.status };
  }
  if (event.source === 'schedule' || (!event.runId && event.taskId)) {
    const taskId = event.taskId;
    if (!taskId || !getTask(taskId))
      throw new Error(`[trigger-shim] unknown scheduled task ${taskId}`);
    const run = await createRunRecord({
      taskIdentifier: taskId,
      payload: {
        timestamp: new Date().toISOString(),
        scheduleId: taskId,
        ...((event.payload as object) ?? {}),
      },
      tags: ['schedule'],
    });
    const result = await executeRun(run.id);
    return { runId: run.id, status: result.status };
  }
  if (!event.runId) throw new Error('[trigger-shim] event has neither runId nor taskId');
  // Task-level retries already ran inside executeRun; the Lambda async
  // retry policy is set to 0 in serverless.yml so failures are not doubled.
  const result = await executeRun(event.runId);
  return { runId: event.runId, status: result.status };
}
