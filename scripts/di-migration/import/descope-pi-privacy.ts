/**
 * Descope Processing Integrity (PI1.*) and Privacy (P1–P8) from the Comp SOC 2
 * program. Scope decision (2026-10-31): Type II = Security + Availability +
 * Confidentiality.
 *
 * What it removes (ids come from the verbatim export in
 * scratch/descoping-pi-privacy/removed-controls.json, which was archived to
 * Google Drive "Compliance / SOC 2 descoped — Processing Integrity and Privacy
 * (2026-10-31)" before anything is deleted):
 *   - the 75 PI/P controls (migrated from Humadroid, ids in import-state.json)
 *   - the evidence tasks that are linked ONLY to those controls (6 expected)
 * It never touches policies (none is linked only from PI/P) and never touches
 * the SOC 2 framework instance: the PI/P requirement definitions stay in the
 * seeded framework, simply unmapped (Comp has no out-of-scope flag).
 *
 * Safety: every control id is checked against Comp before deletion (exists and
 * its name starts with the expected identifier); every task is re-derived from
 * live control→task links and must be linked only to doomed controls.
 * The removed ids are moved in import-state.json from `controls` /
 * `evidenceTasks` to `descoped.controls` / `descoped.evidenceTasks` so run.ts
 * does not recreate them and the history stays in the repo.
 *
 * Dry-run by default; --apply deletes (final).
 *
 *   COMP_API_URL=https://api.compliance.dealintelligence.io COMP_API_KEY=... \
 *     bun import/descope-pi-privacy.ts [--apply]
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const apply = process.argv.includes('--apply');

const statePath = new URL('../data/import-state.json', import.meta.url);
const exportPath = new URL('../scratch/descoping-pi-privacy/removed-controls.json', import.meta.url);

type Export = {
  exported: string;
  reason: string;
  controls: { identifier: string; title: string; compId: string }[];
  evidenceTasksOnlyCitedHere: Record<string, string>;
};
type State = {
  controls: Record<string, string>;
  evidenceTasks: Record<string, string>;
  descoped?: { date: string; reason: string; controls: Record<string, string>; evidenceTasks: Record<string, string> };
  [k: string]: unknown;
};

const exp: Export = JSON.parse(readFileSync(exportPath, 'utf8'));
const state: State = JSON.parse(readFileSync(statePath, 'utf8'));

const isPiOrP = (id: string) => /^(PI\d|P\d)/.test(id);
const wanted = exp.controls.filter((c) => isPiOrP(c.identifier));
if (wanted.length !== exp.controls.length) throw new Error('export contains a non-PI/P identifier; refusing');
// Cross-check the export against the import state: same identifier -> same id.
for (const c of wanted) {
  const inState = state.controls[c.identifier];
  if (inState && inState !== c.compId) throw new Error(`${c.identifier}: export id ${c.compId} != state id ${inState}`);
}

type Control = { id: string; name: string; tasks?: { id: string; title?: string }[] };
const controls: Control[] = [];
for (let page = 1; ; page++) {
  const d = await api.get<{ data: Control[]; pageCount?: number }>('/controls', { limit: '50', page: String(page) });
  controls.push(...d.data);
  if (page >= (d.pageCount ?? 1)) break;
}
const byId = new Map(controls.map((c) => [c.id, c]));

const doomed: Control[] = [];
const alreadyGone: string[] = [];
for (const c of wanted) {
  const live = byId.get(c.compId);
  if (!live) { alreadyGone.push(c.identifier); continue; }
  if (!live.name.startsWith(c.identifier)) throw new Error(`${c.compId}: live name "${live.name}" does not start with ${c.identifier}`);
  doomed.push(live);
}
const doomedIds = new Set(doomed.map((c) => c.id));

// Tasks linked only to doomed controls, derived from live links.
const taskOwners = new Map<string, { title?: string; owners: Set<string> }>();
for (const c of controls)
  for (const t of c.tasks ?? []) {
    const e = taskOwners.get(t.id) ?? { title: t.title, owners: new Set<string>() };
    e.owners.add(c.id);
    taskOwners.set(t.id, e);
  }
const orphanTasks = [...taskOwners.entries()].filter(([, e]) => [...e.owners].every((o) => doomedIds.has(o)));
const orphanIds = new Set(orphanTasks.map(([id]) => id));
const expectedTaskIds = new Set(Object.values(exp.evidenceTasksOnlyCitedHere));
const unexpected = [...orphanIds].filter((id) => !expectedTaskIds.has(id));
const missing = [...expectedTaskIds].filter((id) => !orphanIds.has(id) && taskOwners.has(id));
const sharedKept = controls.filter((c) => !doomedIds.has(c.id) && (c.tasks ?? []).some((t) => expectedTaskIds.has(t.id)));

console.log(`${wanted.length} PI/P controls in export; ${doomed.length} live, ${alreadyGone.length} already gone`);
for (const c of doomed) console.log('  -', c.name.slice(0, 90));
console.log(`${orphanTasks.length} evidence tasks linked only to them:`);
for (const [id, e] of orphanTasks) console.log('  -', e.title, `(${id})`);
if (unexpected.length) console.log(`! ${unexpected.length} orphan task(s) not in the export list:`, unexpected.join(', '));
if (missing.length) console.log(`! ${missing.length} exported task(s) still linked to a kept control (will NOT be deleted):`, missing.join(', '));
for (const c of sharedKept) console.log('    kept control still citing one:', c.name.slice(0, 80));

if (!apply) {
  console.log('\n(dry run — pass --apply to delete)');
  process.exit(0);
}
if (unexpected.length) throw new Error('orphan task set differs from the archived export; re-export before applying');

let t = 0;
for (const [id] of orphanTasks) { await api.delete(`/tasks/${id}`); t++; }
let n = 0;
for (const c of doomed) { await api.delete(`/controls/${c.id}`); n++; }
console.log(`deleted ${t} tasks and ${n} controls`);

// Record in state so run.ts never recreates them.
const d = state.descoped ?? { date: exp.exported, reason: exp.reason, controls: {}, evidenceTasks: {} };
for (const c of wanted) {
  if (state.controls[c.identifier]) { d.controls[c.identifier] = state.controls[c.identifier]; delete state.controls[c.identifier]; }
}
for (const [file, id] of Object.entries(state.evidenceTasks)) {
  if (orphanIds.has(id)) { d.evidenceTasks[file] = id; delete state.evidenceTasks[file]; }
}
state.descoped = d;
writeFileSync(statePath, JSON.stringify(state, null, 2) + '\n');
console.log(`import-state.json: ${Object.keys(state.controls).length} controls remain, ${Object.keys(d.controls).length} recorded as descoped`);
