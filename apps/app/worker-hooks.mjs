// ESM resolve hook: redirect `server-only`/`client-only` (which throw outside
// React Server Components) to an empty module. Loaded on the worker Lambda via
// NODE_OPTIONS="--import /var/task/worker-register.mjs".
export async function resolve(specifier, context, nextResolve) {
  if (specifier === 'server-only' || specifier === 'client-only') {
    return { url: new URL('./worker/server-only.cjs', import.meta.url).href, shortCircuit: true };
  }
  return nextResolve(specifier, context);
}
