/**
 * Dump the non-policy content of the Comp org (controls, risks, vendors, people,
 * tasks, context answers, organization) to scratch/quality-sweep/data/*.json for
 * the 2026-10-31 quality/tone sweep. Read-only.
 *   COMP_API_URL=... COMP_API_KEY=... bun scratch/quality-sweep/dump.ts
 */
import { writeFileSync } from 'node:fs';
import { CompApi } from '../../import/api';
const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const out = new URL('./data/', import.meta.url);
const save = (n: string, d: unknown) => writeFileSync(new URL(n, out), JSON.stringify(d, null, 2) + '\n');
const controls: any[] = [];
for (let p = 1; ; p++) { const d = await api.get<any>('/controls', { limit: '50', page: String(p) }); controls.push(...d.data); if (p >= (d.pageCount ?? 1)) break; }
save('controls.json', controls.map((c) => ({ id: c.id, name: c.name, description: c.description, tasks: (c.tasks ?? []).map((t: any) => t.title), policies: (c.policies ?? []).map((p: any) => p.name) })));
for (const [n, p] of [['risks', '/risks'], ['vendors', '/vendors'], ['people', '/people'], ['tasks', '/tasks'], ['context', '/context']] as const) {
  const r = await api.get<any>(p); save(`${n}.json`, r.data ?? r);
}
save('organization.json', await api.get<any>('/organization'));
const pol = await api.get<any>('/policies');
save('policies-meta.json', pol.data.map((p: any) => ({ id: p.id, name: p.name, description: p.description, status: p.status, frequency: p.frequency, department: p.department, isRequiredToSign: p.isRequiredToSign, reviewDate: p.reviewDate })));
console.log('controls', controls.length, 'policies', pol.data.length);
