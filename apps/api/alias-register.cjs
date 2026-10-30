// Runtime resolver for the tsconfig path aliases used by the API ("@/..." and
// "@db"). Nest's build normally rewrites them to relative paths; this hook makes
// the compiled output work even when it hasn't (e.g. some container builds).
// Load with `node -r ./alias-register.cjs dist/src/main.js` or NODE_OPTIONS.
const Module = require('node:module');
const path = require('node:path');
const distRoot = path.join(__dirname, 'dist');
const aliases = [
  ['@db', () => path.join(distRoot, 'prisma', 'index')],
  ['@/', (req) => path.join(distRoot, 'src', req.slice(2))],
];
const orig = Module._resolveFilename;
Module._resolveFilename = function (request, parent, isMain, options) {
  for (const [prefix, map] of aliases) {
    if (request === prefix || (prefix.endsWith('/') && request.startsWith(prefix))) {
      return orig.call(this, map(request), parent, isMain, options);
    }
  }
  return orig.call(this, request, parent, isMain, options);
};
