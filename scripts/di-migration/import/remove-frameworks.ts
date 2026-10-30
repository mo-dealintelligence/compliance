/**
 * Remove framework instances that are not part of the audited program (GDPR and
 * CCPA were enabled during onboarding) together with the Comp template controls
 * that exist only for them and the template tasks linked only to those
 * controls. The 211 migrated SOC 2 controls are never touched: a migrated
 * control that happens to map to a GDPR/CCPA requirement just loses that
 * mapping when the instance goes.
 *
 * Dry-run by default; pass --apply to delete. Deletion is final.
 *
 *   COMP_API_URL=https://api.compliance.dealintelligence.io COMP_API_KEY=... \
 *     bun import/remove-frameworks.ts [--apply] [--frameworks GDPR,CCPA]
 */
import { readFileSync } from 'node:fs';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const args = process.argv.slice(2);
const apply = args.includes('--apply');
const fwIdx = args.indexOf('--frameworks');
const targetNames = new Set((fwIdx >= 0 ? args[fwIdx + 1] : 'GDPR,CCPA').split(',').map((s) => s.trim()));

const migrated = new Set<string>(
  Object.values(
    JSON.parse(readFileSync(new URL('../data/import-state.json', import.meta.url), 'utf8')).controls as Record<string, string>,
  ),
);

type Instance = { id: string; framework?: { name?: string }; customFramework?: { name?: string } | null };
const instances = (await api.get<{ data: Instance[] }>('/frameworks')).data;
const targets = instances.filter((i) => targetNames.has(i.framework?.name ?? i.customFramework?.name ?? ''));
const targetIds = new Set(targets.map((i) => i.id));
if (targets.length === 0) {
  console.log(`no framework instance named ${[...targetNames].join(', ')}; nothing to do`);
  process.exit(0);
}

type Control = {
  id: string;
  name: string;
  controlTemplateId: string | null;
  tasks?: { id: string; title?: string }[];
  requirementsMapped?: { frameworkInstanceId?: string; frameworkInstance?: { id?: string } }[];
};
const controls: Control[] = [];
for (let page = 1; ; page++) {
  const d = await api.get<{ data: Control[]; pageCount?: number }>('/controls', { limit: '50', page: String(page) });
  controls.push(...d.data);
  if (page >= (d.pageCount ?? 1)) break;
}
const instanceOf = (m: NonNullable<Control['requirementsMapped']>[number]) => m.frameworkInstanceId ?? m.frameworkInstance?.id ?? '';
// Template controls whose every requirement mapping points at a target instance.
const doomed = controls.filter(
  (c) =>
    !migrated.has(c.id) &&
    !!c.controlTemplateId &&
    (c.requirementsMapped ?? []).length > 0 &&
    (c.requirementsMapped ?? []).every((m) => targetIds.has(instanceOf(m))),
);
const doomedIds = new Set(doomed.map((c) => c.id));
const owners = new Map<string, { title?: string; owners: Set<string> }>();
for (const c of controls)
  for (const t of c.tasks ?? []) {
    const e = owners.get(t.id) ?? { title: t.title, owners: new Set<string>() };
    e.owners.add(c.id);
    owners.set(t.id, e);
  }
const orphanTasks = [...owners.entries()].filter(([, e]) => [...e.owners].every((o) => doomedIds.has(o)));

console.log(`${targets.length} framework instance(s) to remove:`);
for (const i of targets) console.log('  -', i.framework?.name ?? i.customFramework?.name, `(${i.id})`);
console.log(`${doomed.length} template controls mapped only to them:`);
for (const c of doomed) console.log('  -', c.name);
console.log(`${orphanTasks.length} tasks linked only to those controls:`);
for (const [, e] of orphanTasks) console.log('  -', e.title);
const migratedTouched = controls.filter((c) => migrated.has(c.id) && (c.requirementsMapped ?? []).some((m) => targetIds.has(instanceOf(m))));
console.log(`${migratedTouched.length} migrated SOC 2 controls also mapped to these frameworks (kept; mapping removed by cascade)`);

if (!apply) {
  console.log('\n(dry run — pass --apply to delete)');
  process.exit(0);
}
let m = 0;
for (const [id] of orphanTasks) { await api.delete(`/tasks/${id}`); m++; }
let n = 0;
for (const c of doomed) { await api.delete(`/controls/${c.id}`); n++; }
let f = 0;
for (const i of targets) { await api.delete(`/frameworks/${i.id}`); f++; }
console.log(`deleted ${m} tasks, ${n} controls and ${f} framework instance(s)`);
