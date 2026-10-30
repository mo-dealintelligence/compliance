/**
 * Links the Nov‑2025 audited policies to the controls of the criteria they
 * primarily document. The Google Sheet only mapped the 10 Drive policies, so
 * these 14 would otherwise sit unlinked. Mapping is by criterion family (all
 * controls under e.g. CC9.2) — review in Comp and prune as needed.
 *
 *   COMP_API_URL=... COMP_API_KEY=... bun import/nov2025-policy-links.ts [--dry-run]
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const dryRun = process.argv.includes('--dry-run');
const D = join(import.meta.dirname, '..', 'data');
const policies = JSON.parse(readFileSync(join(D, 'nov2025', 'state.json'), 'utf8')) as Record<string, string>;
const controls = JSON.parse(readFileSync(join(D, 'import-state.json'), 'utf8')).controls as Record<string, string>;

const MAP: Record<string, string[]> = {
  'acceptable-use-policy': ['CC1.1', 'CC1.4', 'CC6.8'],
  'api-security-and-rate-limiting-standard': ['CC6.6', 'CC6.7', 'PI1.2'],
  'cloud-infrastructure-security-policy': ['CC6.1', 'CC6.6', 'CC6.7', 'A1.2'],
  'data-classification-and-handling-standard': ['C1.1', 'C1.2', 'CC6.5'],
  'data-subject-rights-request-procedure': ['P5.1', 'P5.2', 'P6.7', 'P8.1'],
  'encryption-and-cryptographic-controls-standard': ['CC6.1', 'CC6.7', 'C1.1'],
  'penetration-testing-and-security-assessment-procedure': ['CC4.1', 'CC7.1'],
  'secure-software-development-lifecycle-sdlc-standard': ['CC8.1', 'CC7.1', 'PI1.3'],
  'security-awareness-training-program': ['CC1.4', 'CC2.2', 'P8.1'],
  'service-level-agreement-sla-management-policy': ['A1.1', 'A1.2', 'CC2.3'],
  'system-monitoring-and-logging-procedure': ['CC7.2', 'CC7.3', 'CC4.1', 'A1.1'],
  'third-party-integration-security-guidelines': ['CC9.2', 'CC6.6', 'P6.1'],
  'vendor-management-policy': ['CC9.2', 'P6.1', 'CC3.4'],
  'vulnerability-management-procedure': ['CC7.1', 'CC7.2', 'CC8.1'],
};

for (const [slug, families] of Object.entries(MAP)) {
  const policyId = policies[slug];
  if (!policyId) throw new Error(`no policy id for ${slug}`);
  const idents = Object.keys(controls).filter((k) => families.some((f) => k === f || k.startsWith(`${f}.`)));
  const controlIds = idents.map((k) => controls[k]);
  console.log(`${slug} -> ${idents.length} controls [${families.join(', ')}]`);
  if (!dryRun) await api.post(`/policies/${policyId}/controls`, { controlIds });
}
console.log('done');
