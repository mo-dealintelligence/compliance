/**
 * Builds the import plan from the Humadroid export:
 *   - data/Compliance/controls-list.csv   (TSC criteria + DI sub-controls + evidence refs)
 *   - data/markdown/_index.json + data/tiptap/*.json (converted documents)
 *   - data/manifest.json                   (downloaded evidence files)
 *
 * Output: data/import-plan.json (reviewed before running import/run.ts).
 */
import { parse } from 'csv-parse/sync';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, join } from 'node:path';

const DATA = join(import.meta.dir, '..', 'data');

export interface MatrixRow {
  Identifier: string;
  Section: string;
  Title: string;
  Description: string;
  'Implementation Notes': string;
  'Evidence files': string;
  'Evidence files desciptions': string;
}

export interface PlannedPolicy {
  slug: string;
  name: string;
  docType: string;
  requiredToSign: boolean;
  effectiveDate?: string;
  reviewDate?: string;
  sourcePdf: string;
  tiptapFile: string;
  department: string;
}

export interface PlannedEvidence {
  file: string; // filename as referenced in the matrix
  localPath?: string;
  mimeType?: string;
  title: string;
  description: string;
  criteria: string[]; // top-level TSC ids referencing it
  kind: 'screenshot' | 'log' | 'document' | 'record' | 'policy';
}

export interface PlannedControl {
  identifier: string; // e.g. CC6.1
  section: string;
  title: string;
  description: string; // criterion text + DI sub-controls + implementation notes
  evidenceFiles: string[];
  policySlugs: string[];
}

export interface ImportPlan {
  policies: PlannedPolicy[];
  controls: PlannedControl[];
  evidence: PlannedEvidence[];
  records: PlannedPolicy[]; // documents imported as evidence (not policies)
}

const RECORD_SLUGS =
  /^(annual-performance|board-management|ethics-.*-certificate|ethics-violation|job-description|organizational-structure)/;
const TITLE_OVERRIDES: Record<string, string> = {
  'board-management-meeting-minutes-q4-2025': 'Board / Management Meeting Minutes - Q4 2025',
  'ethics-and-privacy-training-completion-certificate-william-wickey':
    'Ethics and Privacy Training Completion Certificate - William Wickey',
  'ethics-and-security-training-completion-certificate-mo-messidi':
    'Ethics and Security Training Completion Certificate - Mo Messidi',
};
const DEPARTMENT_BY_SLUG: Record<string, string> = {
  'code-of-conduct': 'hr',
  'privacy-notice-and-data-processing-agreement-template': 'gov',
  'business-continuity-plan': 'it',
  'change-management-policy': 'it',
  'access-control-and-authentication-policy': 'it',
  'data-classification-policy': 'gov',
  'data-retention-and-disposal-policy': 'gov',
  'information-security-policy': 'gov',
  'incident-response-procedure': 'it',
  'risk-assessment-procedure': 'gov',
};

const DATE_RE = /^[A-Z][a-z]+ \d{1,2}, \d{4}$/;
const toIso = (s?: string) => (s && DATE_RE.test(s) ? new Date(s).toISOString() : undefined);

function humanize(file: string): string {
  return basename(file)
    .replace(/\.(png|json|pdf)$/i, '')
    .replace(/-v\d+\.\d+$/, '')
    .replace(/_\d{8}_\d{6}$/, '')
    .replace(/^\d+_/, '')
    .replace(/[_-]+/g, ' ')
    .replace(/\baws\b/i, 'AWS')
    .replace(/\bgithub\b/i, 'GitHub')
    .replace(/\biam\b/i, 'IAM')
    .replace(/\bvpc\b/i, 'VPC')
    .replace(/\bs3\b/i, 'S3')
    .replace(/\bkms\b/i, 'KMS')
    .replace(/\becr\b/i, 'ECR')
    .replace(/\bsns\b/i, 'SNS')
    .replace(/\bci\b/i, 'CI')
    .replace(/\bmacos\b/i, 'macOS')
    .replace(/\bfilevault\b/i, 'FileVault')
    .replace(/\bcloudtrail\b/i, 'CloudTrail')
    .replace(/\bcloudwatch\b/i, 'CloudWatch')
    .replace(/\bdocumentdb\b/i, 'DocumentDB')
    .replace(/\bpropelauth\b/i, 'PropelAuth')
    .replace(/\bhumadroid\b/i, 'compliance platform')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function buildPlan(): ImportPlan {
  const rows = parse(readFileSync(join(DATA, 'Compliance', 'controls-list.csv')), {
    columns: true,
    skip_empty_lines: true,
  }) as MatrixRow[];
  const docIndex = JSON.parse(readFileSync(join(DATA, 'markdown', '_index.json'), 'utf8')) as {
    slug: string;
    title: string;
    doc_type: string;
    acknowledgment: string;
    effective_date: string;
    review_date: string;
    source: string;
  }[];
  const manifest = JSON.parse(readFileSync(join(DATA, 'manifest.json'), 'utf8')) as {
    title: string;
    localPath: string;
    mimeType: string;
    ok: boolean;
  }[];
  const byFile = new Map(manifest.filter((m) => m.ok).map((m) => [m.title, m]));

  const policies: PlannedPolicy[] = [];
  const records: PlannedPolicy[] = [];
  for (const d of docIndex) {
    const planned: PlannedPolicy = {
      slug: d.slug,
      name: TITLE_OVERRIDES[d.slug] ?? d.title,
      docType: d.doc_type,
      requiredToSign: d.acknowledgment === 'Explicit',
      effectiveDate: toIso(d.effective_date),
      reviewDate: toIso(d.review_date),
      sourcePdf: d.source,
      tiptapFile: join(DATA, 'tiptap', `${d.slug}.json`),
      department: DEPARTMENT_BY_SLUG[d.slug] ?? 'none',
    };
    (RECORD_SLUGS.test(d.slug) ? records : policies).push(planned);
  }
  const policyBySource = new Map(policies.map((p) => [p.sourcePdf, p.slug]));

  // Group matrix rows by top-level criterion (e.g. CC6.1); sub-controls are CC6.1.1, ...
  const groups = new Map<string, MatrixRow[]>();
  for (const r of rows) {
    const top = r.Identifier.split('.').slice(0, 2).join('.');
    if (!groups.has(top)) groups.set(top, []);
    groups.get(top)!.push(r);
  }

  const evidence = new Map<string, PlannedEvidence>();
  const controls: PlannedControl[] = [];
  for (const [identifier, group] of groups) {
    const head = group.find((r) => r.Identifier === identifier) ?? group[0];
    const subs = group.filter((r) => r.Identifier !== identifier);
    const files = new Set<string>();
    const policySlugs = new Set<string>();
    const lines: string[] = [];
    lines.push(`Criterion ${identifier} (${head.Section}): ${head.Title.trim()}`);
    if (head['Implementation Notes'])
      lines.push('', `Implementation: ${head['Implementation Notes'].trim()}`);
    if (subs.length) {
      lines.push('', 'Deal Intelligence controls:');
      for (const s of subs) {
        lines.push(
          `- ${s.Identifier} ${s.Title.trim()}: ${s.Description.trim()}${s['Implementation Notes'] ? ` (Implementation: ${s['Implementation Notes'].trim()})` : ''}`,
        );
      }
    }
    for (const r of group) {
      const refs = r['Evidence files']
        .split(',')
        .map((f) => f.trim())
        .filter(Boolean);
      const descs = r['Evidence files desciptions']
        .split(/\.\s+(?=[A-Z])/)
        .map((d) => d.trim())
        .filter(Boolean);
      refs.forEach((f, i) => {
        if (policyBySource.has(f)) policySlugs.add(policyBySource.get(f)!);
        files.add(f);
        const m = byFile.get(f);
        const existing = evidence.get(f);
        const desc = descs[i] ?? descs[0] ?? '';
        const kind: PlannedEvidence['kind'] = f.endsWith('.png')
          ? 'screenshot'
          : f.endsWith('.json')
            ? 'log'
            : policyBySource.has(f)
              ? 'policy'
              : docIndex.some((d) => d.source === f)
                ? 'record'
                : 'document';
        if (!existing) {
          evidence.set(f, {
            file: f,
            localPath: m?.localPath,
            mimeType: m?.mimeType,
            title: humanize(f),
            description: desc,
            criteria: [identifier],
            kind,
          });
        } else if (!existing.criteria.includes(identifier)) {
          existing.criteria.push(identifier);
          if (desc && !existing.description.includes(desc)) existing.description += ` ${desc}`;
        }
      });
    }
    controls.push({
      identifier,
      section: head.Section,
      title: `${identifier} ${head.Title.trim().slice(0, 110)}`,
      description: lines.join('\n'),
      evidenceFiles: [...files],
      policySlugs: [...policySlugs],
    });
  }

  return {
    policies,
    controls,
    evidence: [...evidence.values()].sort((a, b) => a.file.localeCompare(b.file)),
    records,
  };
}

if (import.meta.main) {
  const plan = buildPlan();
  writeFileSync(join(DATA, 'import-plan.json'), JSON.stringify(plan, null, 2));
  const missing = plan.evidence.filter((e) => !e.localPath);
  console.log(
    `policies=${plan.policies.length} records=${plan.records.length} controls=${plan.controls.length} evidence=${plan.evidence.length} (missing files: ${missing.map((m) => m.file).join(', ') || 'none'})`,
  );
  if (!existsSync(join(DATA, 'tiptap'))) console.warn('run md_to_tiptap.mjs first');
}
