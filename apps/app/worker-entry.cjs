/* eslint-disable @typescript-eslint/no-require-imports */
// Lambda handler module for the app background worker.
// `server-only` (pulled in by shared packages) throws outside React Server
// Components, so it is redirected to an empty module before anything loads.
const Module = require('node:module');
const path = require('node:path');

const originalResolve = Module._resolveFilename;
Module._resolveFilename = function patchedResolve(request, ...rest) {
  if (request === 'server-only' || request === 'client-only') {
    return path.join(__dirname, 'worker', 'server-only.cjs');
  }
  return originalResolve.call(this, request, ...rest);
};

module.exports = require('./worker/handler.cjs');
