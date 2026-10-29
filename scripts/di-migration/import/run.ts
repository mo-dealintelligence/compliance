/**
 * Idempotent importer: loads data/import-plan.json into a Comp organization
 * through the API. Progress is recorded in data/import-state.json so reruns
 * skip what already exists.
 *
 *   COMP_API_URL=https://compliance-api.dealintelligence.io \
 *   COMP_API_KEY=comp_... COMP_USER_ID=usr_... COMP_MEMBER_ID=mem_... \
 *   bun import/run.ts [--dry-run] [--only policies,controls,evidence,records,vendors,people,context]
 *
 * Prerequisites (UI): organization created with the SOC 2 framework enabled,
 * an API key with full access, evidence approval disabled.
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { CompApi } from './api';
import type { ImportPlan, PlannedEvidence } from './plan';
import { CONTEXT, PEOPLE, RISKS, VENDORS } from './seed-data';

const DATA = join(import.meta.dir, '..', 'data');
const STATE_FILE = join(DATA, 'import-state.json');

interface State {
  frameworkInstanceId?: string;
  requirementIds: Record<string, string>; // 'CC6.1' -> req id
  policies: Record<string, string>; // slug -> policy id
  controls: Record<string, string>; // identifier -> control id
  evidenceTasks: Record<string, string>; // file -> task id
  evidenceUploaded: Record<string, boolean>;
  links: Record<string, boolean>;
  vendors: Record<string, string>;
  risks: Record<string, string>;
  people: Record<string, boolean>;
  context: Record<string, string>;
}

const env = (k: string) => {
  const v = process.env[k];
  if (!v) throw new Error(`${k} is required`);
  return v;
};
const dryRun = process.argv.includes('--dry-run');
const onlyArg = process.argv.find((a) => a.startsWith('--only='));
const only = new Set(
  onlyArg
    ? onlyArg.slice(7).split(',')
    : ['policies', 'controls', 'evidence', 'records', 'vendors', 'risks', 'people', 'context'],
);

const api = new CompApi(env('COMP_API_URL'), env('COMP_API_KEY'));
const userId = env('COMP_USER_ID');
const memberId = process.env.COMP_MEMBER_ID;
const plan = JSON.parse(readFileSync(join(DATA, 'import-plan.json'), 'utf8')) as ImportPlan;
const state: State = existsSync(STATE_FILE)
  ? JSON.parse(readFileSync(STATE_FILE, 'utf8'))
  : {
      requirementIds: {},
      policies: {},
      controls: {},
      evidenceTasks: {},
      evidenceUploaded: {},
      links: {},
      vendors: {},
      risks: {},
      people: {},
      context: {},
    };
const save = () => writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
const log = (...a: unknown[]) => console.log(new Date().toISOString().slice(11, 19), ...a);

const MIME: Record<string, string> = {
  png: 'image/png',
  pdf: 'application/pdf',
  json: 'application/json',
};
const mimeFor = (f: string) =>
  MIME[f.split('.').pop()!.toLowerCase()] ?? 'application/octet-stream';

async function resolveFramework() {
  if (state.frameworkInstanceId && Object.keys(state.requirementIds).length) return;
  const list = await api.get<{ data: { id: string; framework: { name: string } }[] }>(
    '/frameworks',
  );
  const soc2 = list.data.find((f) => /soc ?2/i.test(f.framework?.name ?? ''));
  if (!soc2) throw new Error('SOC 2 framework instance not found; enable it in the UI first');
  state.frameworkInstanceId = soc2.id;
  const detail = await api.get<{ requirementDefinitions: { id: string; identifier: string }[] }>(
    `/frameworks/${soc2.id}`,
  );
  for (const r of detail.requirementDefinitions)
    state.requirementIds[r.identifier.toUpperCase().replace(/-/g, '.')] = r.id;
  log(`framework ${soc2.id}: ${detail.requirementDefinitions.length} requirements`);
  save();
}

async function importPolicies() {
  for (const p of plan.policies) {
    if (state.policies[p.slug]) continue;
    const doc = JSON.parse(readFileSync(p.tiptapFile, 'utf8')) as { content: unknown[] };
    log(`policy: ${p.name}`);
    if (dryRun) continue;
    const created = await api.post<{ id: string }>('/policies', {
      name: p.name,
      description: `${p.docType} imported from the Deal Intelligence SOC 2 Type I program (source: ${p.sourcePdf}).`,
      content: doc.content,
      status: 'published',
      frequency: 'yearly',
      department: p.department,
      isRequiredToSign: p.requiredToSign,
      reviewDate: p.reviewDate,
      ...(memberId ? { assigneeId: memberId, signedBy: p.requiredToSign ? [memberId] : [] } : {}),
    });
    state.policies[p.slug] = created.id;
    save();
  }
}

async function importControls() {
  await resolveFramework();
  const fi = state.frameworkInstanceId!;
  for (const c of plan.controls) {
    if (!state.controls[c.identifier]) {
      const reqId = state.requirementIds[c.identifier];
      if (!reqId) log(`  ! no Comp requirement for ${c.identifier}; creating control unmapped`);
      log(`control: ${c.title}`);
      if (dryRun) continue;
      const created = await api.post<{ id: string }>('/controls', {
        name: c.title,
        description: c.description,
        requirementMappings: reqId ? [{ requirementId: reqId, frameworkInstanceId: fi }] : [],
      });
      state.controls[c.identifier] = created.id;
      save();
    }
    const controlId = state.controls[c.identifier];
    const policyIds = c.policySlugs.map((s) => state.policies[s]).filter(Boolean);
    const key = `policies:${c.identifier}`;
    if (policyIds.length && !state.links[key] && !dryRun) {
      await api.post(`/controls/${controlId}/policies/link`, { policyIds });
      await api.post(
        `/controls/${controlId}/policies/link`,
        { policyIds },
        { frameworkInstanceId: fi },
      );
      state.links[key] = true;
      save();
    }
  }
}

async function uploadEvidence(e: PlannedEvidence, taskId: string) {
  if (!e.localPath || state.evidenceUploaded[e.file]) return;
  const path = e.localPath.startsWith('/') ? e.localPath : join(DATA, '..', e.localPath);
  if (!existsSync(path)) {
    log(`  ! missing file ${path}`);
    return;
  }
  const bytes = readFileSync(path);
  await api.post(`/tasks/${taskId}/attachments`, {
    fileName: basename(e.file),
    fileType: e.mimeType ?? mimeFor(e.file),
    fileData: bytes.toString('base64'),
    description: e.description.slice(0, 490),
    userId,
  });
  state.evidenceUploaded[e.file] = true;
  save();
}

async function importEvidence() {
  await resolveFramework();
  const fi = state.frameworkInstanceId!;
  const controlIdByFile = new Map<string, string[]>();
  for (const c of plan.controls)
    for (const f of c.evidenceFiles)
      controlIdByFile.set(
        f,
        [...(controlIdByFile.get(f) ?? []), state.controls[c.identifier]].filter(Boolean),
      );

  for (const e of plan.evidence) {
    if (e.kind === 'policy') continue; // policies are linked, not uploaded as evidence
    if (!state.evidenceTasks[e.file]) {
      log(`evidence: ${e.title} (${e.criteria.join(', ')})`);
      if (dryRun) continue;
      const created = await api.post<{ id: string }>('/tasks', {
        title: e.title,
        description: `${e.description || 'Evidence from the SOC 2 Type I program.'}\n\nSupports: ${e.criteria.join(', ')}\nSource file: ${e.file}`,
        frequency: e.kind === 'screenshot' || e.kind === 'log' ? 'quarterly' : 'yearly',
        department: 'it',
        ...(memberId ? { assigneeId: memberId } : {}),
      });
      state.evidenceTasks[e.file] = created.id;
      save();
    }
    const taskId = state.evidenceTasks[e.file];
    if (dryRun) continue;
    await uploadEvidence(e, taskId);
    const controlIds = controlIdByFile.get(e.file) ?? [];
    for (const controlId of controlIds) {
      const key = `task:${e.file}:${controlId}`;
      if (state.links[key]) continue;
      await api.post(`/controls/${controlId}/tasks/link`, { taskIds: [taskId] });
      await api.post(
        `/controls/${controlId}/tasks/link`,
        { taskIds: [taskId] },
        { frameworkInstanceId: fi },
      );
      state.links[key] = true;
      save();
    }
    if (!state.links[`done:${e.file}`]) {
      await api.patch(`/tasks/${taskId}`, { status: 'done' });
      state.links[`done:${e.file}`] = true;
      save();
    }
  }
}

async function importRecords() {
  // Records (minutes, certificates, evaluations, JDs) that the matrix does not
  // reference directly still get an evidence task with the PDF attached.
  for (const r of plan.records) {
    if (state.evidenceTasks[r.sourcePdf]) continue;
    log(`record: ${r.name}`);
    if (dryRun) continue;
    const created = await api.post<{ id: string }>('/tasks', {
      title: r.name,
      description: `${r.docType} imported from the SOC 2 Type I program (source: ${r.sourcePdf}).`,
      frequency: 'yearly',
      department: 'hr',
      ...(memberId ? { assigneeId: memberId } : {}),
    });
    state.evidenceTasks[r.sourcePdf] = created.id;
    save();
    await uploadEvidence(
      {
        file: r.sourcePdf,
        localPath: join('data', 'Compliance', 'evidence', 'policies-procedures', r.sourcePdf),
        title: r.name,
        description: r.docType,
        criteria: [],
        kind: 'record',
      },
      created.id,
    );
    await api.patch(`/tasks/${created.id}`, { status: 'done' });
  }
}

async function importVendors() {
  for (const v of VENDORS) {
    if (state.vendors[v.name]) continue;
    log(`vendor: ${v.name}`);
    if (dryRun) continue;
    const created = await api.post<{ id: string }>('/vendors', v);
    state.vendors[v.name] = created.id;
    save();
  }
}

async function importRisks() {
  for (const r of RISKS) {
    if (state.risks[r.title]) continue;
    log(`risk: ${r.title}`);
    if (dryRun) continue;
    const created = await api.post<{ id: string }>('/risks', {
      ...r,
      ...(memberId ? { assigneeId: memberId } : {}),
    });
    state.risks[r.title] = created.id;
    save();
  }
}

async function importPeople() {
  for (const p of PEOPLE) {
    if (state.people[p.email]) continue;
    log(`person: ${p.email} (${p.roles.join(',')})`);
    if (dryRun) continue;
    await api.post('/people/invite', {
      invites: [{ email: p.email, roles: p.roles, sendPortalEmail: false }],
    });
    state.people[p.email] = true;
    save();
  }
}

async function importContext() {
  for (const c of CONTEXT) {
    if (state.context[c.question]) continue;
    log(`context: ${c.question}`);
    if (dryRun) continue;
    const created = await api.post<{ id: string }>('/context', c);
    state.context[c.question] = created.id;
    save();
  }
}

const steps: [string, () => Promise<void>][] = [
  ['policies', importPolicies],
  ['controls', importControls],
  ['evidence', importEvidence],
  ['records', importRecords],
  ['vendors', importVendors],
  ['risks', importRisks],
  ['people', importPeople],
  ['context', importContext],
];
for (const [name, fn] of steps) {
  if (!only.has(name)) continue;
  log(`== ${name}${dryRun ? ' (dry run)' : ''}`);
  await fn();
}
log('done');
