#!/usr/bin/env node
/**
 * Markdown -> TipTap JSON using the same TipTap schema the policy editor uses
 * (StarterKit incl. Link + Table + TextAlign), so imported policies are fully
 * editable in Comp.
 *
 *   node scripts/di-migration/md_to_tiptap.mjs data/markdown data/tiptap
 *
 * Emits <slug>.json = { frontMatter, content: <array of top-level nodes> }.
 * The policies API accepts `content` as an array of nodes (CreatePolicyDto).
 */
import { generateJSON } from '@tiptap/html';
import { Table, TableCell, TableHeader, TableRow } from '@tiptap/extension-table';
import TextAlign from '@tiptap/extension-text-align';
import StarterKit from '@tiptap/starter-kit';
import { readdirSync, readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, basename } from 'node:path';
import { marked } from 'marked';

const [, , srcDir, dstDir] = process.argv;
if (!srcDir || !dstDir) {
  console.error('usage: md_to_tiptap.mjs <markdown dir> <out dir>');
  process.exit(1);
}
mkdirSync(dstDir, { recursive: true });

const extensions = [
  StarterKit,
  TextAlign.configure({ types: ['heading', 'paragraph'] }),
  Table,
  TableRow,
  TableHeader,
  TableCell,
];

function splitFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n\n?/);
  if (!m) return { frontMatter: {}, body: text };
  const frontMatter = {};
  for (const line of m[1].split('\n')) {
    const i = line.indexOf(':');
    if (i > 0) frontMatter[line.slice(0, i).trim()] = JSON.parse(line.slice(i + 1).trim());
  }
  return { frontMatter, body: text.slice(m[0].length) };
}

for (const file of readdirSync(srcDir).filter((f) => f.endsWith('.md'))) {
  const { frontMatter, body } = splitFrontMatter(readFileSync(join(srcDir, file), 'utf8'));
  // Drop the leading H1: Comp renders the policy name as the page title.
  const withoutTitle = body.replace(/^# .+\n+/, '');
  const html = marked.parse(withoutTitle, { gfm: true, breaks: false });
  const doc = generateJSON(html, extensions);
  const slug = basename(file, '.md');
  writeFileSync(
    join(dstDir, `${slug}.json`),
    JSON.stringify({ frontMatter, content: doc.content ?? [] }, null, 2),
  );
  console.log(`${slug}: ${doc.content?.length ?? 0} top-level nodes`);
}
