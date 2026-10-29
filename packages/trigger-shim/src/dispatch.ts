/**
 * Dispatches a run for background execution.
 *
 * - TASK_WORKER_FUNCTION set (Lambda): async `lambda:Invoke` of the worker.
 * - otherwise (local dev, tests): execute in-process without awaiting.
 */
import { InvokeCommand, LambdaClient } from '@aws-sdk/client-lambda';
import { executeRun } from './execute';

let lambda: LambdaClient | null = null;

export interface WorkerEvent {
  runId?: string;
  taskId?: string;
  payload?: unknown;
  source: 'trigger' | 'schedule';
}

export async function dispatch(event: WorkerEvent): Promise<void> {
  const fn = process.env.TASK_WORKER_FUNCTION;
  if (fn) {
    lambda ??= new LambdaClient({
      region: process.env.AWS_REGION || process.env.APP_AWS_REGION || 'us-east-1',
    });
    await lambda.send(
      new InvokeCommand({
        FunctionName: fn,
        InvocationType: 'Event',
        Payload: Buffer.from(JSON.stringify(event)),
      }),
    );
    return;
  }
  if (event.runId) {
    const runId = event.runId;
    setImmediate(() => {
      executeRun(runId).catch((error) =>
        console.error('[trigger-shim] in-process run failed', error),
      );
    });
  }
}
