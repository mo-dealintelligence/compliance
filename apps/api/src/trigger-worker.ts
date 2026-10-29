/**
 * Lambda entrypoint for background tasks (replaces the Trigger.dev worker).
 * Importing the generated registry registers every task with the
 * @trigger.dev/sdk shim; the handler executes runs / schedules by id.
 */
import './config/load-env';
import './trigger/_registry';

export { handler } from '@trigger.dev/sdk/worker';
