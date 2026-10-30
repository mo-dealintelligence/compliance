/**
 * Creates Comp's native evidence-form records from the audited Humadroid
 * documents and links the matching form types to the controls that cite them.
 *
 *   COMP_API_URL=https://api.compliance.dealintelligence.io COMP_API_KEY=... \
 *   bun run scripts/di-migration/evidence/native-records.ts [--link-only] [--inventory <dir>]
 *
 * Records created (idempotent — keyed in data/native-records-state.json):
 *   board-meeting                   ← board-management-meeting-minutes-q4-2025-v1.0.pdf
 *   employee-performance-evaluation ← annual-performance-evaluation-ceo-v1.0.pdf
 *   tabletop-exercise               ← Humadroid "Q1 2025 BCP test" (full recovery test, 2026‑02‑04)
 *   rbac-matrix                     ← PropelAuth roles + live AWS IAM listing (inventory dir) + Comp/GitHub/Workspace
 *   infrastructure-inventory        ← live AWS listing produced by deploy/aws/inventory.sh
 *
 * Submissions require the API-key acting-member change (apps/api evidence-forms
 * controller) to be deployed; linking works on any build.
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { CompApi } from '../import/api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const args = process.argv.slice(2);
const linkOnly = args.includes('--link-only');
const invIdx = args.indexOf('--inventory');
const inventoryDir = invIdx >= 0 ? args[invIdx + 1] : undefined;

const dataDir = new URL('../data/', import.meta.url).pathname;
const statePath = join(dataDir, 'native-records-state.json');
const state: { submissions: Record<string, string>; links: Record<string, string[]> } = existsSync(statePath)
  ? JSON.parse(readFileSync(statePath, 'utf8'))
  : { submissions: {}, links: {} };
const save = () => writeFileSync(statePath, JSON.stringify(state, null, 1));

const importState = JSON.parse(readFileSync(join(dataDir, 'import-state.json'), 'utf8')) as {
  controls: Record<string, string>;
};
const plan = JSON.parse(readFileSync(join(dataDir, 'import-plan.json'), 'utf8')) as {
  controls: { identifier: string; evidenceFiles: string[] }[];
};

const OWNER = 'Mo Messidi';
const today = new Date().toISOString().slice(0, 10);

/** Markdown body of a converted audited document (frontmatter stripped). */
function docBody(slug: string) {
  const md = readFileSync(join(dataDir, 'markdown', `${slug}.md`), 'utf8');
  return md.replace(/^---[\s\S]*?---\s*/, '').trim();
}

function b64(path: string) {
  return readFileSync(path).toString('base64');
}

async function uploadFile(formType: string, filePath: string, fileType: string) {
  const fileName = filePath.split('/').pop()!;
  return api.post<{ fileName: string; fileKey: string; downloadUrl: string }>(
    '/evidence-forms/uploads',
    { formType, fileName, fileType, fileData: b64(filePath) },
  );
}

async function submit(key: string, formType: string, payload: Record<string, unknown>) {
  if (state.submissions[key]) {
    console.log(`= ${key} already created (${state.submissions[key]})`);
    return;
  }
  const res = await api.post<{ id: string }>(`/evidence-forms/${formType}/submissions`, payload);
  state.submissions[key] = res.id;
  save();
  console.log(`+ ${key} -> ${res.id}`);
}

// ---------------------------------------------------------------------------
// Form type ↔ controls (controls whose Humadroid evidence cited the document)
// ---------------------------------------------------------------------------
const formTypeByEvidence: Record<string, RegExp> = {
  board_meeting: /board-management-meeting-minutes/i,
  employee_performance_evaluation: /annual-performance-evaluation/i,
  tabletop_exercise: /humadroid_bcp_test_results/i,
  rbac_matrix: /propelauth_roles|aws_iam_(users|roles)/i,
  infrastructure_inventory: /aws_(lambda_functions|documentdb_cluster|vpc_list|s3_buckets|ecr_repositories)/i,
};

async function linkFormTypes() {
  for (const [formType, pattern] of Object.entries(formTypeByEvidence)) {
    const ids = plan.controls
      .filter((c) => c.evidenceFiles.some((f) => pattern.test(f)))
      .map((c) => c.identifier);
    const done = new Set(state.links[formType] ?? []);
    for (const ident of ids) {
      if (done.has(ident)) continue;
      const controlId = importState.controls[ident];
      if (!controlId) {
        console.warn(`! no control id for ${ident}`);
        continue;
      }
      await api.post(`/controls/${controlId}/document-types/link`, { formTypes: [formType] });
      done.add(ident);
      state.links[formType] = [...done];
      save();
    }
    console.log(`${formType}: linked to ${ids.length} controls (${ids.join(', ')})`);
  }
}

// ---------------------------------------------------------------------------
// Records
// ---------------------------------------------------------------------------
async function boardMeeting() {
  const minutes = docBody('board-management-meeting-minutes-q4-2025');
  await submit('board-meeting-q4-2025', 'board-meeting', {
    submissionDate: '2025-12-09T22:00:00.000Z',
    date: '2025-12-09',
    attendees: 'Mo Messidi (CEO); William Wickey (Head of GTM, contractor). Quorum established.',
    meetingMinutes:
      `Q4 2025 Quarterly Board/Management Meeting — Deal Intelligence LLC\n` +
      `Source: board-management-meeting-minutes-q4-2025-v1.0.pdf (audited record, finalized 2026-02-02)\n\n` +
      minutes,
    meetingMinutesApprovedBy: 'Mo Messidi (CEO, meeting recorder)',
    approvedDate: '2026-02-02',
  });
}

async function performanceEvaluation() {
  const body = docBody('annual-performance-evaluation-ceo');
  const summary = body.match(/\*\*Summary\*\* : ([\s\S]*?)\n\n## 8\./)?.[1]?.trim() ?? '';
  await submit('performance-evaluation-ceo-2025', 'employee-performance-evaluation', {
    submissionDate: '2025-12-09T22:00:00.000Z',
    employeeName: 'Mo Messidi (CEO)',
    manager: 'Self-evaluation — CEO / sole owner (reports to Board of Directors)',
    reviewPeriodTo: '2025-12-09',
    overallRating: 'exceeds-expectations',
    managerComments:
      `Annual Performance Evaluation — CEO, period 2025-01-01 to 2025-12-09. Composite rating 4.95/5 (Exceptional).\n\n` +
      summary +
      `\n\nAreas for improvement: control automation 86% → 95% (Q2 2026); 2 remaining SOC 2 controls (Q1–Q2 2026); ` +
      `penetration testing cadence (Q2 2026). Full record: annual-performance-evaluation-ceo-v1.0.pdf.`,
    managerSignature: 'Mo Messidi',
    managerSignatureDate: '2025-12-09',
  });
}

async function tabletopExercise() {
  const shot = join(dataDir, 'Compliance/evidence/screenshots/humadroid/humadroid_bcp_test_results.png');
  const evidenceFile = await uploadFile('tabletop-exercise', shot, 'image/png');
  await submit('bcp-full-test-2026-02', 'tabletop-exercise', {
    submissionDate: '2026-02-04T08:25:00.000Z',
    exerciseDate: '2026-02-04',
    facilitator: 'Mo Messidi (CEO, exercise coordinator)',
    scenarioType: 'custom',
    scenarioDescription:
      'AWS service disruption — full systems recovery from backups using infrastructure-as-code ' +
      '(serverless.yml deployment). Plan: "AWS Service Disruption Recovery" (process: AWS Infrastructure Operations). ' +
      'Type: full test (not a discussion-only tabletop).',
    attendees: [{ name: 'Mo Messidi', roleTitle: 'CEO', department: 'Executive' }],
    sessionNotes:
      'Scheduled 2026-03-04, executed early on 2026-02-04 (started 00:24, completed 00:25 PST). ' +
      'Recovered all AWS infrastructure from backups via the serverless.yml deployment. Result: system recovered successfully; ' +
      'plan success rate 100% (1/1 exercises). Recorded in the Humadroid Business Continuity module (screenshot attached).',
    actionItems: [
      {
        finding: 'Full recovery succeeded; no gaps identified in the restore path.',
        improvementAction:
          'Repeat the restoration test quarterly per the Business Continuity Plan and record RTO/RPO achieved.',
        assignedOwner: OWNER,
        dueDate: '2026-05-04',
      },
    ],
    evidenceFile,
  });
}

async function rbacMatrix() {
  const rows: { system: string; roleName: string; permissionsScope: string; approvedBy: string; lastReviewed: string }[] = [
    { system: 'PropelAuth (Deal Intelligence platform auth)', roleName: 'Owner', permissionsScope: 'Full organization administration in the DI platform; manage members and billing', approvedBy: OWNER, lastReviewed: today },
    { system: 'PropelAuth (Deal Intelligence platform auth)', roleName: 'Admin', permissionsScope: 'Organization administration; manage members and settings', approvedBy: OWNER, lastReviewed: today },
    { system: 'PropelAuth (Deal Intelligence platform auth)', roleName: 'Member (default role)', permissionsScope: 'Standard product access to the organization’s data; no member/billing management', approvedBy: OWNER, lastReviewed: today },
    { system: 'Comp (compliance platform, self-hosted)', roleName: 'owner — Mo Messidi', permissionsScope: 'Full administration of the compliance program (policies, controls, evidence, people, settings)', approvedBy: OWNER, lastReviewed: today },
    { system: 'Comp (compliance platform, self-hosted)', roleName: 'employee — William Wickey', permissionsScope: 'Employee portal only: policy acknowledgment and security training', approvedBy: OWNER, lastReviewed: today },
    { system: 'GitHub (mo-dealintelligence)', roleName: 'Organization owner — Mo Messidi', permissionsScope: 'All repositories, branch protection, secrets, Actions; MFA enforced', approvedBy: OWNER, lastReviewed: today },
    { system: 'Google Workspace (dealintelligence.io)', roleName: 'Super Admin — Mo Messidi', permissionsScope: 'Workspace administration, user lifecycle, security settings', approvedBy: OWNER, lastReviewed: today },
  ];
  if (inventoryDir) {
    const aws = JSON.parse(readFileSync(join(inventoryDir, 'rbac-aws-rows.json'), 'utf8')) as { awsRows: typeof rows };
    rows.push(...aws.awsRows);
  } else {
    console.warn('! --inventory not given: AWS IAM rows omitted from the RBAC matrix');
  }
  await submit(`rbac-matrix-${today}`, 'rbac-matrix', { submissionDate: new Date().toISOString(), matrixRows: rows });
}

async function infrastructureInventory() {
  if (!inventoryDir) {
    console.warn('! --inventory not given: skipping infrastructure inventory');
    return;
  }
  const inv = JSON.parse(readFileSync(join(inventoryDir, 'infrastructure-inventory.json'), 'utf8')) as {
    inventoryRows: unknown[];
  };
  await submit(`infrastructure-inventory-${today}`, 'infrastructure-inventory', {
    submissionDate: new Date().toISOString(),
    inventoryRows: inv.inventoryRows,
  });
}

await linkFormTypes();
if (!linkOnly) {
  await boardMeeting();
  await performanceEvaluation();
  await tabletopExercise();
  await rbacMatrix();
  await infrastructureInventory();
}
console.log('done');
