// Lambda handler module for the app background worker (ESM).
// `server-only`/`client-only` are redirected by worker-hooks.mjs, loaded via
// NODE_OPTIONS="--import /var/task/apps/app/worker-register.mjs".
export { handler } from './worker/handler.mjs';
