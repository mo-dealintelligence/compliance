/**
 * Attach captured evidence files to their Comp tasks and mark the tasks done.
 *
 *   COMP_API_URL=https://api.compliance.dealintelligence.io/v1 COMP_API_KEY=... \
 *     bun evidence/upload.ts <capture dir>
 *
 * The capture dir holds files named exactly like the `file` field in
 * shot-list.json, optionally with a date suffix before the extension
 * (aws_kms_keys.png or aws_kms_keys_2026-11-01.png). Each file is uploaded to
 * the task listed for it; a run log (evidence/runs/<date>.json) records what
 * was attached. Re-running skips files already logged for that day.
 */
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { basename, extname, join } from 'node:path';
import { CompApi } from '../import/api';

const api = new CompApi(process.env.COMP_API_URL!, process.env.COMP_API_KEY!);
const dir = process.argv[2];
if (!dir) throw new Error('usage: bun evidence/upload.ts <capture dir>');
const list = JSON.parse(readFileSync(new URL('./shot-list.json', import.meta.url), 'utf8')) as {
  shots: { file: string; taskId: string; source: string }[];
};
const byStem = new Map(list.shots.map((s) => [s.file.replace(extname(s.file), ''), s]));
const today = new Date().toISOString().slice(0, 10);
const runsDir = new URL('./runs/', import.meta.url);
mkdirSync(runsDir, { recursive: true });
const logFile = join(runsDir.pathname, `${today}.json`);
const log: { file: string; taskId: string; attachmentId?: string; at: string }[] = existsSync(logFile)
  ? JSON.parse(readFileSync(logFile, 'utf8'))
  : [];
const mime: Record<string, string> = { '.png': 'image/png', '.jpg': 'image/jpeg', '.json': 'application/json', '.pdf': 'application/pdf' };

let n = 0;
for (const name of readdirSync(dir)) {
  const ext = extname(name);
  const stem = name.replace(ext, '').replace(/_\d{4}-\d{2}-\d{2}$/, '');
  const shot = byStem.get(stem);
  if (!shot) {
    console.log(`skip ${name}: not in shot-list`);
    continue;
  }
  if (log.some((l) => l.file === name)) continue;
  const data = readFileSync(join(dir, name));
  const res = await api.post<{ id?: string }>(`/tasks/${shot.taskId}/attachments`, {
    fileName: `${stem}_${today}${ext}`,
    fileType: mime[ext] ?? 'application/octet-stream',
    fileData: data.toString('base64'),
    description: `Evidence capture ${today} (${shot.source})`,
    userId: process.env.COMP_USER_ID,
  });
  await api.patch(`/tasks/${shot.taskId}`, { status: 'done' });
  log.push({ file: name, taskId: shot.taskId, attachmentId: res?.id, at: new Date().toISOString() });
  writeFileSync(logFile, JSON.stringify(log, null, 2));
  console.log(`attached ${name} -> ${shot.taskId}`);
  n++;
}
console.log(`${n} files attached; log: ${logFile}`);
