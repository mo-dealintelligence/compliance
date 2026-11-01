/**
 * Load the 2026-10-31 v2 content into the compliance platform.
 *
 * Policies (versioned + signed): for each policies-v2/<slug>.md, create a draft
 * version cloned from the current one, replace its content with the v2 TipTap
 * JSON, and submit it for approval to the CEO. Mo reviews and publishes in the
 * UI (publishing clears the signatures so everyone re-acknowledges). The two
 * merged documents (Data Classification Policy, Third-Party Integration
 * Security Guidelines) are left published until the v2 set is approved; a
 * follow-up `--archive-merged` step archives them.
 *
 * Everything else is not versioned or signed, so it is applied directly from
 * scratch/quality-sweep/: control names/descriptions (controls-v2.json, needs
 * the PATCH /controls/:id endpoint, deployed with 8f7aa1475), task
 * titles/descriptions (+ the new monthly availability task), risks, vendors,
 * people job titles, context answers (+ one deletion), policy metadata, and
 * the new management-meeting minutes as a board-meeting evidence submission.
 *
 * Idempotent through data/v2-publish-state.json. Dry-run by default.
 *
 *   COMP_API_URL=... COMP_API_KEY=... bun import/publish-v2.ts [--apply] \
 *     [--only policies,controls,tasks,risks,vendors,people,context,policy-meta,minutes] \
 *     [--archive-merged]
 */
import { execFileSync } from 'node:child_process';
import { existsSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const args = process.argv.slice(2);
const apply = args.includes('--apply');
const onlyIdx = args.indexOf('--only');
const only = new Set(onlyIdx >= 0 ? args[onlyIdx + 1].split(',') : ['policies', 'controls', 'tasks', 'risks', 'vendors', 'people', 'context', 'policy-meta', 'minutes']);
const archiveMerged = args.includes('--archive-merged');

const ROOT = new URL('../', import.meta.url);
const p = (rel: string) => new URL(rel, ROOT).pathname;
const readJson = <T,>(rel: string): T => JSON.parse(readFileSync(p(rel), 'utf8'));
const statePath = p('data/v2-publish-state.json');
type State = {
  policyVersions: Record<string, { policyId: string; versionId: string; submitted: boolean }>;
  controls: string[];
  tasks: string[];
  newTasks: Record<string, string>;
  risks: string[];
  vendors: string[];
  people: string[];
  context: string[];
  contextDeleted: string[];
  policyMeta: string[];
  minutes?: string;
  archived: string[];
};
const state: State = existsSync(statePath)
  ? JSON.parse(readFileSync(statePath, 'utf8'))
  : { policyVersions: {}, controls: [], tasks: [], newTasks: {}, risks: [], vendors: [], people: [], context: [], contextDeleted: [], policyMeta: [], archived: [] };
const save = () => writeFileSync(statePath, JSON.stringify(state, null, 2) + '\n');
const log = (s: string) => console.log(s);
const MERGED = ['data-classification-policy', 'third-party-integration-security-guidelines'];
const APPROVER = process.env.COMP_APPROVER_MEMBER_ID ?? 'mem_6ae4394866f20a057e95811c'; // Mo

// ---------- policies ----------
async function policies() {
  const importState = readJson<{ policies: Record<string, string> }>('data/import-state.json');
  const novState = readJson<Record<string, string>>('data/nov2025/state.json');
  const policyIdBySlug: Record<string, string> = { ...importState.policies, ...novState };
  const out = mkdtempSync(join(tmpdir(), 'v2-tiptap-'));
  execFileSync('node', [p('md_to_tiptap.mjs'), p('policies-v2'), out], { stdio: 'pipe' });
  const live = (await api.get<{ data: { id: string; name: string; status: string; currentVersionId?: string }[] }>('/policies', { summary: 'true' })).data;
  const liveById = new Map(live.map((x) => [x.id, x]));
  const slugs = Object.keys(policyIdBySlug).filter((s) => !MERGED.includes(s) && existsSync(p(`policies-v2/${s}.md`)));
  const missing = Object.keys(policyIdBySlug).filter((s) => !MERGED.includes(s) && !existsSync(p(`policies-v2/${s}.md`)));
  if (missing.length) log(`! no v2 markdown for: ${missing.join(', ')}`);
  for (const slug of slugs) {
    const policyId = policyIdBySlug[slug];
    const lv = liveById.get(policyId);
    if (!lv) { log(`! ${slug}: policy ${policyId} not found live`); continue; }
    const { content, frontMatter } = JSON.parse(readFileSync(join(out, `${slug}.json`), 'utf8'));
    const st = state.policyVersions[slug];
    log(`policy ${slug} (${lv.status}) → v${frontMatter.version} draft, ${content.length} nodes${st ? ` [version ${st.versionId}${st.submitted ? ', submitted' : ''}]` : ''}`);
    if (!apply) continue;
    let versionId = st?.versionId;
    if (!versionId) {
      const v = await api.post<{ id?: string; versionId?: string; data?: { id?: string; versionId?: string } }>(`/policies/${policyId}/versions`, {
        changelog: `v${frontMatter.version} (2026-10-31): scope Security/Availability/Confidentiality; roles; compensating controls; quality sweep. See repo policies-v2/changes/${slug}.md`,
      });
      versionId = v.versionId ?? v.data?.versionId ?? v.id ?? v.data?.id;
      if (!versionId) throw new Error(`${slug}: no version id in ${JSON.stringify(v).slice(0, 200)}`);
      state.policyVersions[slug] = { policyId, versionId, submitted: false };
      save();
    }
    await api.patch(`/policies/${policyId}/versions/${versionId}`, { content });
    if (!state.policyVersions[slug].submitted) {
      await api.post(`/policies/${policyId}/versions/${versionId}/submit-for-approval`, { approverId: APPROVER });
      state.policyVersions[slug].submitted = true;
      save();
    }
  }
  if (archiveMerged) {
    for (const slug of MERGED) {
      const id = policyIdBySlug[slug];
      if (!id || state.archived.includes(id)) continue;
      log(`archive merged policy ${slug} (${id})`);
      if (!apply) continue;
      await api.patch(`/policies/${id}`, { isArchived: true });
      state.archived.push(id); save();
    }
  }
}

// ---------- controls ----------
async function controls() {
  const v2 = readJson<{ id: string; name: string; description: string; changed: boolean }[]>('scratch/quality-sweep/controls-v2.json');
  const todo = v2.filter((c) => c.changed && !state.controls.includes(c.id));
  log(`controls: ${todo.length} to update (${state.controls.length} done)`);
  for (const c of todo) {
    if (!apply) continue;
    await api.patch(`/controls/${c.id}`, { name: c.name, description: c.description });
    state.controls.push(c.id); save();
  }
}

// ---------- generic field updates ----------
async function patchDiff(kind: keyof State & ('tasks' | 'risks' | 'vendors' | 'people' | 'context' | 'policyMeta'), orig: string, v2: string, path: string, fields: string[]) {
  const a = readJson<any[]>(orig); const b = readJson<any[]>(v2);
  const A = new Map(a.map((x) => [x.id, x]));
  const done = state[kind] as string[];
  let n = 0;
  for (const x of b) {
    if (!x.id || !A.has(x.id) || done.includes(x.id)) continue;
    const body: Record<string, unknown> = {};
    for (const f of fields) if (f in x && A.get(x.id)[f] !== x[f]) body[f] = x[f];
    if (!Object.keys(body).length) continue;
    n++;
    log(`  ${kind} ${x.id}: ${Object.keys(body).join(', ')}${x.title || x.name || x.question ? ` — ${(x.title ?? x.name ?? x.question).slice(0, 60)}` : ''}`);
    if (!apply) continue;
    await api.patch(`${path}/${x.id}`, body);
    done.push(x.id); save();
  }
  log(`${kind}: ${n} updated`);
}

async function tasks() {
  await patchDiff('tasks', 'scratch/quality-sweep/data/tasks.json', 'scratch/quality-sweep/records-v2/tasks-v2.json', '/tasks', ['title', 'description']);
  const v2 = readJson<any[]>('scratch/quality-sweep/records-v2/tasks-v2.json');
  for (const t of v2.filter((x) => x.new)) {
    if (state.newTasks[t.title]) continue;
    log(`  new task: ${t.title} (${t.frequency})`);
    if (!apply) continue;
    const created = await api.post<{ id: string }>('/tasks', {
      title: t.title, description: t.description, frequency: t.frequency ?? 'monthly', department: 'it',
      ...(APPROVER ? { assigneeId: APPROVER } : {}),
    });
    state.newTasks[t.title] = created.id; save();
  }
}

async function context() {
  await patchDiff('context', 'scratch/quality-sweep/data/context.json', 'scratch/quality-sweep/records-v2/context-v2.json', '/context', ['answer']);
  const a = readJson<any[]>('scratch/quality-sweep/data/context.json');
  const b = new Set(readJson<any[]>('scratch/quality-sweep/records-v2/context-v2.json').map((x) => x.id));
  for (const x of a) {
    if (b.has(x.id) || state.contextDeleted.includes(x.id)) continue;
    log(`  delete context ${x.id} — ${x.question} (duplicate)`);
    if (!apply) continue;
    await api.delete(`/context/${x.id}`);
    state.contextDeleted.push(x.id); save();
  }
}

// ---------- new minutes ----------
async function minutes() {
  if (state.minutes) { log(`minutes: already submitted (${state.minutes})`); return; }
  const md = readFileSync(p('scratch/quality-sweep/records-v2/management-meeting-minutes-2026-10-31.md'), 'utf8');
  const body = md.replace(/^---[\s\S]*?---\n/, '');
  log(`minutes: submit board-meeting record (${body.split(/\s+/).length} words) — contains ${(body.match(/\[CONFIRM/g) ?? []).length} CONFIRM markers`);
  if (!apply) return;
  const res = await api.post<{ id: string }>('/evidence-forms/board-meeting/submissions', {
    submissionDate: new Date().toISOString(),
    date: '2026-10-31',
    attendees: 'Chief Executive Officer (Mo Messidi)',
    meetingMinutes: body,
    meetingMinutesApprovedBy: 'Chief Executive Officer (Mo Messidi) — draft minutes, approval pending review',
    approvedDate: '2026-10-31',
  });
  state.minutes = res.id; save();
}

for (const [k, fn] of [
  ['policies', policies], ['controls', controls], ['tasks', tasks],
  ['risks', () => patchDiff('risks', 'scratch/quality-sweep/data/risks.json', 'scratch/quality-sweep/records-v2/risks-v2.json', '/risks', ['title', 'description', 'treatmentStrategyDescription'])],
  ['vendors', () => patchDiff('vendors', 'scratch/quality-sweep/data/vendors.json', 'scratch/quality-sweep/records-v2/vendors-v2.json', '/vendors', ['description', 'treatmentStrategyDescription'])],
  ['people', () => patchDiff('people', 'scratch/quality-sweep/data/people.json', 'scratch/quality-sweep/records-v2/people-v2.json', '/people', ['jobTitle', 'department'])],
  ['context', context],
  ['policy-meta', () => patchDiff('policyMeta', 'scratch/quality-sweep/data/policies-meta.json', 'scratch/quality-sweep/records-v2/policies-meta-v2.json', '/policies', ['description', 'frequency', 'department'])],
  ['minutes', minutes],
] as const) {
  if (!only.has(k)) continue;
  log(`\n== ${k}`);
  await fn();
}
if (!apply) log('\n(dry run — pass --apply to write)');
