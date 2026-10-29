/**
 * Lambda entrypoint for the app's background tasks (replaces the Trigger.dev
 * worker). Bundled by scripts/build-worker.mjs; see deploy/Dockerfile
 * target `app-worker`.
 */
import './tasks/_registry';

export { handler } from '@trigger.dev/sdk/worker';
