'use strict';
/**
 * Resolves a Lambda environment map at deploy time from a Secrets Manager
 * secret holding a flat JSON object (e.g. `comp/env/api`). Used by the
 * Serverless service files as:
 *
 *   environment: ${file(../env.js):api}
 *
 * The secret is the single source of truth; nothing is written to disk.
 * NEXT_PUBLIC_* keys are kept too (harmless at runtime, used by server code).
 */
const {
  SecretsManagerClient,
  GetSecretValueCommand,
} = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({
  region: process.env.AWS_REGION || 'us-east-1',
});

async function load(name) {
  const res = await client.send(
    new GetSecretValueCommand({ SecretId: `comp/env/${name}` }),
  );
  const parsed = JSON.parse(res.SecretString || '{}');
  const out = {};
  for (const [key, value] of Object.entries(parsed)) {
    if (value === null || value === undefined || value === '') continue;
    out[key] = String(value);
  }
  return out;
}

module.exports.api = () => load('api');
module.exports.app = () => load('app');
module.exports.portal = () => load('portal');
