/**
 * Imports the audited Nov‑2025 policy set that was not in the Google Drive
 * export (the SOC 2 Type I evidence package, soc2-compliance-documents-5q2p-
 * 20251114). Content is verbatim (PDF -> markdown -> TipTap), published,
 * editable in Comp, same metadata the first 10 Drive policies got.
 *
 *   python3 -I pdf_to_md.py data/nov2025/new-pdf data/nov2025/md
 *   node md_to_tiptap.mjs data/nov2025/md data/nov2025/tiptap
 *   COMP_API_URL=... COMP_API_KEY=... COMP_MEMBER_ID=... bun import/nov2025-policies.ts [--dry-run]
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { CompApi } from './api';

const DATA = join(import.meta.dirname, '..', 'data', 'nov2025');
const STATE = join(DATA, 'state.json');
const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const memberId = process.env.COMP_MEMBER_ID;
const dryRun = process.argv.includes('--dry-run');

const DEPARTMENT: Record<string, string> = {
  'acceptable-use-policy': 'hr',
  'security-awareness-training-program': 'hr',
  'data-subject-rights-request-procedure': 'gov',
  'vendor-management-policy': 'gov',
};

type Index = {
  slug: string;
  title: string;
  doc_type: string;
  version: string;
  acknowledgment: string;
  effective_date: string;
  review_date: string;
  source: string;
};

const toIso = (d: string) => {
  const t = Date.parse(d);
  return Number.isNaN(t) ? undefined : new Date(t).toISOString();
};

const index = JSON.parse(readFileSync(join(DATA, 'md', '_index.json'), 'utf8')) as Index[];
const state: Record<string, string> = existsSync(STATE) ? JSON.parse(readFileSync(STATE, 'utf8')) : {};

for (const p of index) {
  if (state[p.slug]) continue;
  const doc = JSON.parse(readFileSync(join(DATA, 'tiptap', `${p.slug}.json`), 'utf8')) as { content: unknown[] };
  const requiredToSign = /explicit/i.test(p.acknowledgment);
  console.log(`policy: ${p.title} v${p.version} (${p.source}) sign=${requiredToSign}`);
  if (dryRun) continue;
  const created = await api.post<{ id: string }>('/policies', {
    name: p.title,
    description: `${p.doc_type} v${p.version} imported from the Deal Intelligence SOC 2 Type I program (source: ${p.source}, effective ${p.effective_date}).`,
    content: doc.content,
    status: 'published',
    frequency: 'yearly',
    department: DEPARTMENT[p.slug] ?? 'it',
    isRequiredToSign: requiredToSign,
    reviewDate: toIso(p.review_date),
    ...(memberId ? { assigneeId: memberId, signedBy: requiredToSign ? [memberId] : [] } : {}),
  });
  state[p.slug] = created.id;
  writeFileSync(STATE, JSON.stringify(state, null, 2));
}
console.log('done');
