/**
 * Remove the generic Comp template controls that onboarding generated for SOC 2
 * (they duplicate the audited Deal Intelligence control matrix imported by
 * run.ts) and the template tasks linked only to them. GDPR/CCPA template
 * controls are kept. Dry-run by default; pass --apply to delete.
 *
 *   COMP_API_URL=https://api.compliance.dealintelligence.io/v1 COMP_API_KEY=... \
 *     bun import/cleanup-templates.ts [--apply]
 */
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const apply = process.argv.includes('--apply');

type Control = {
  id: string;
  name: string;
  controlTemplateId: string | null;
  tasks?: { id: string; title?: string }[];
  requirementsMapped?: { frameworkInstance?: { framework?: { name?: string } } }[];
};

const controls: Control[] = [];
for (let page = 1; ; page++) {
  const d = await api.get<{ data: Control[]; pageCount?: number }>('/controls', {
    limit: '50',
    page: String(page),
  });
  controls.push(...d.data);
  if (page >= (d.pageCount ?? 1)) break;
}
const isSoc2Template = (c: Control) =>
  !!c.controlTemplateId &&
  (c.requirementsMapped ?? []).every(
    (m) => (m.frameworkInstance?.framework?.name ?? 'SOC 2') === 'SOC 2',
  );
const doomed = controls.filter(isSoc2Template);
const doomedIds = new Set(doomed.map((c) => c.id));
const owners = new Map<string, { title?: string; owners: Set<string> }>();
for (const c of controls)
  for (const t of c.tasks ?? []) {
    const e = owners.get(t.id) ?? { title: t.title, owners: new Set<string>() };
    e.owners.add(c.id);
    owners.set(t.id, e);
  }
const orphanTasks = [...owners.entries()].filter(([, e]) => [...e.owners].every((o) => doomedIds.has(o)));

console.log(`${doomed.length} SOC 2 template controls:`);
for (const c of doomed) console.log('  -', c.name);
console.log(`${orphanTasks.length} tasks linked only to them:`);
for (const [, e] of orphanTasks) console.log('  -', e.title);
if (!apply) {
  console.log('\n(dry run — pass --apply to delete)');
  process.exit(0);
}
let n = 0;
for (const c of doomed) {
  await api.delete(`/controls/${c.id}`);
  n++;
}
let m = 0;
for (const [id] of orphanTasks) {
  await api.delete(`/tasks/${id}`);
  m++;
}
console.log(`deleted ${n} controls and ${m} tasks`);
