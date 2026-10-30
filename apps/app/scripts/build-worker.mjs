#!/usr/bin/env node
/**
 * Bundles apps/app/src/trigger/worker.ts into worker/handler.js for Lambda.
 * App source is bundled (tsconfig paths resolved); node_modules stay external
 * and are shipped alongside, like the API image does.
 */
import { build } from 'esbuild';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
mkdirSync(resolve(root, 'worker'), { recursive: true });
// `server-only` throws outside React Server Components; stub it for the worker.
writeFileSync(resolve(root, 'worker/server-only.cjs'), 'module.exports = {};\n');

await build({
  entryPoints: [resolve(root, 'src/trigger/worker.ts')],
  outfile: resolve(root, 'worker/handler.cjs'),
  bundle: true,
  platform: 'node',
  target: 'node22',
  format: 'cjs',
  sourcemap: true,
  packages: 'external',
  tsconfig: resolve(root, 'tsconfig.json'),
  // Upstream imports the app by its own package name; bundle it instead of
  // leaving a node_modules symlink to .ts sources at runtime.
  alias: { 'server-only': resolve(root, 'worker/server-only.cjs'), '@trycompai/app': root },
  jsx: 'automatic',
  logLevel: 'info',
  define: { 'process.env.NEXT_RUNTIME': '"nodejs"' },
});
