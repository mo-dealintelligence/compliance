/**
 * Withdraw pending v2 policy versions whose markdown changed after submission, so
 * publish-v2.ts can create and submit fresh drafts (pending versions are immutable).
 *
 * For each slug: deny the pending version (as the assigned approver), delete it, and drop
 * its entry from data/v2-publish-state.json (recorded under `withdrawn`). For the record
 * files (controls, tasks, risks, context, policy metadata), ids whose JSON entry changed
 * since <base> are dropped from the state lists so publish-v2.ts patches them again.
 *
 *   COMP_API_URL=... COMP_API_KEY=... bun import/redraft-v2.ts --base <git-rev> --slugs a,b,c [--apply]
 *
 * Then: bun import/publish-v2.ts --apply --only policies,controls,tasks,risks,context,policy-meta
 * Used 2026-11-01 for D26/D27 (no Multi-AZ DocumentDB; 35-day backups).
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const args = process.argv.slice(2);
const apply = args.includes('--apply');
const arg = (k: string) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : undefined; };
const base = arg('--base');
const slugs = (arg('--slugs') ?? '').split(',').filter(Boolean);
if (!base || !slugs.length) throw new Error('usage: --base <rev> --slugs a,b [--apply]');
const APPROVER = process.env.COMP_APPROVER_MEMBER_ID ?? 'mem_6ae4394866f20a057e95811c';

const ROOT = new URL('../', import.meta.url);
const p = (rel: string) => new URL(rel, ROOT).pathname;
const statePath = p('data/v2-publish-state.json');
const state = JSON.parse(readFileSync(statePath, 'utf8'));
state.withdrawn ??= [];
const save = () => writeFileSync(statePath, JSON.stringify(state, null, 2) + '\n');

for (const slug of slugs) {
  const st = state.policyVersions[slug];
  if (!st) { console.log(`- ${slug}: no submitted version in state, nothing to withdraw`); continue; }
  const pol = (await api.get<{ data?: { pendingVersionId?: string | null }; pendingVersionId?: string | null }>(`/policies/${st.policyId}`));
  const pending = pol.data?.pendingVersionId ?? pol.pendingVersionId ?? null;
  console.log(`${slug}: state ${st.versionId}, pending ${pending}`);
  if (!apply) continue;
  if (pending === st.versionId) {
    await api.post(`/policies/${st.policyId}/deny-changes`, {
      approverId: APPROVER,
      comment: 'Withdrawn 2026-11-01: superseded by a corrected draft (D26/D27).',
    });
  }
  try {
    await api.delete(`/policies/${st.policyId}/versions/${st.versionId}`);
  } catch (e) {
    console.log(`  ! delete ${st.versionId}: ${(e as Error).message.slice(0, 160)}`);
  }
  state.withdrawn.push({ slug, ...st, at: new Date().toISOString() });
  delete state.policyVersions[slug];
  save();
}

// record files: drop changed ids so publish-v2 patches them again
const RECORDS: [string, string][] = [
  ['scratch/quality-sweep/controls-v2.json', 'controls'],
  ['scratch/quality-sweep/records-v2/tasks-v2.json', 'tasks'],
  ['scratch/quality-sweep/records-v2/risks-v2.json', 'risks'],
  ['scratch/quality-sweep/records-v2/context-v2.json', 'context'],
  ['scratch/quality-sweep/records-v2/policies-meta-v2.json', 'policyMeta'],
];
for (const [rel, key] of RECORDS) {
  const now: { id?: string }[] = JSON.parse(readFileSync(p(rel), 'utf8'));
  const then: { id?: string }[] = JSON.parse(
    execFileSync('git', ['show', `${base}:scripts/di-migration/${rel}`], { encoding: 'utf8', maxBuffer: 1 << 26 }),
  );
  const old = new Map(then.map((x) => [x.id, JSON.stringify(x)]));
  const changed = now.filter((x) => x.id && old.get(x.id) !== JSON.stringify(x)).map((x) => x.id!);
  console.log(`${key}: ${changed.length} changed since ${base}`);
  if (!apply) continue;
  state[key] = (state[key] as string[]).filter((id) => !changed.includes(id));
  save();
}
