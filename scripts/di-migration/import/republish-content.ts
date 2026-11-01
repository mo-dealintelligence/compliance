/**
 * Re-publish policy CONTENT only (name/status/signatures untouched) from the
 * reconverted markdown → TipTap files, for every policy created by run.ts
 * (Drive set) and nov2025-policies.ts. Used after converter fixes.
 *
 *   COMP_API_URL=... COMP_API_KEY=... bun import/republish-content.ts [--dry-run]
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { CompApi } from './api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const dry = process.argv.includes('--dry-run');
const D = join(import.meta.dirname, '..', 'data');
const drive = JSON.parse(readFileSync(join(D, 'import-state.json'), 'utf8')).policies as Record<string, string>;
const nov = JSON.parse(readFileSync(join(D, 'nov2025', 'state.json'), 'utf8')) as Record<string, string>;
const sets: [Record<string, string>, string][] = [[drive, join(D, 'tiptap')], [nov, join(D, 'nov2025', 'tiptap')]];
for (const [state, dir] of sets)
  for (const [slug, id] of Object.entries(state)) {
    const content = JSON.parse(readFileSync(join(dir, `${slug}.json`), 'utf8')).content;
    console.log(`${dry ? 'would update' : 'updating'} ${slug} (${id}) ${content.length} nodes`);
    if (!dry) await api.patch(`/policies/${id}`, { content });
  }
console.log('done');
