/**
 * Import Deal Intelligence's internal policy docs (from the `docs/` mkdocs
 * site in the dealintel monorepo) that cover audited policies missing from the
 * Google Drive export. Content is verbatim (markdown -> TipTap); the
 * description records which audited policy name each doc satisfies.
 *
 *   node md_to_tiptap.mjs data/repo-policies/md data/repo-policies/tiptap
 *   COMP_API_URL=... COMP_API_KEY=... COMP_MEMBER_ID=... bun import/repo-policies.ts [--dry-run]
 */
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { CompApi } from './api';

const DATA = join(import.meta.dirname, '..', 'data', 'repo-policies');
const STATE = join(DATA, 'state.json');
const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const memberId = process.env.COMP_MEMBER_ID;
const dryRun = process.argv.includes('--dry-run');

// slug -> [audited policy names it satisfies], department
const DOCS: Record<string, { audited: string[]; department: string }> = {
  'employee-handbook': { audited: ['Acceptable Use Policy'], department: 'hr' },
  vendor: { audited: ['Vendor Management Policy'], department: 'gov' },
  'data-protection': { audited: ['Encryption and Cryptographic Controls Standard'], department: 'it' },
  'system-audit': {
    audited: ['System Monitoring and Logging Procedure', 'Penetration Testing and Security Assessment Procedure'],
    department: 'it',
  },
  'vuln-mgmt': { audited: ['Vulnerability Management Procedure'], department: 'it' },
  model: { audited: ['Cloud Infrastructure Security Policy'], department: 'it' },
  rar: { audited: ['Security Awareness Training Program'], department: 'hr' },
  sdlc: { audited: ['Secure Software Development Lifecycle (SDLC) Standard'], department: 'it' },
};

const state: Record<string, string> = existsSync(STATE) ? JSON.parse(readFileSync(STATE, 'utf8')) : {};
for (const [slug, meta] of Object.entries(DOCS)) {
  if (state[slug]) continue;
  const doc = JSON.parse(readFileSync(join(DATA, 'tiptap', `${slug}.json`), 'utf8')) as {
    content: { type: string; attrs?: { level?: number }; content?: { text?: string }[] }[];
  };
  // The converter drops the leading H1 (Comp shows the name as the title); take it from the markdown.
  const md = readFileSync(join(DATA, 'md', `${slug}.md`), 'utf8');
  const name = md.match(/^#{1,2}\s+(.+)$/m)?.[1]?.trim() || slug;
  console.log(`policy: ${name}  (satisfies: ${meta.audited.join('; ')})`);
  if (dryRun) continue;
  const created = await api.post<{ id: string }>('/policies', {
    name,
    description: `Deal Intelligence internal policy (docs/${slug}.md, v2023.1). Satisfies audited inventory item(s): ${meta.audited.join('; ')}.`,
    content: doc.content,
    status: 'published',
    frequency: 'yearly',
    department: meta.department,
    isRequiredToSign: true,
    ...(memberId ? { assigneeId: memberId } : {}),
  });
  state[slug] = created.id;
  writeFileSync(STATE, JSON.stringify(state, null, 2));
}
console.log('done');
