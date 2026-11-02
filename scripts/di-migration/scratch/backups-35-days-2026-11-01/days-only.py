#!/usr/bin/env python3
"""D27 (Mo, 2026-11-01): DocumentDB backups 35 days. Days only — every other word stays as
scratch/no-multi-az-2026-11-01/apply.py left it (Mo: "go back to the previous phrasing for all
except the days of backup").

Supersedes apply.py and fix-recovery-wording.py in this folder (both reverted). Run from the
compliance repo root on top of commit 2607d7ca1's files. Exact matches with expected counts.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = "scripts/di-migration/policies-v2/"
Q = "scripts/di-migration/scratch/quality-sweep/"
D = "docs/dealintelligence/"

EDITS = {
    P + "RULEBOOK.md": [
        ("- DocumentDB automated backups retained **90 days**,", "- DocumentDB automated backups retained **35 days**,", 1),
        ("- Backups: 90 days (R3).", "- Backups: 35 days (R3).", 1),
    ],
    P + "DECISIONS-2026-10-31.md": [
        ("automated backups (90 days once the env-alignment branch deploys)", "automated backups (35 days, D27)", 1),
    ],
    P + "business-continuity-plan.md": [
        ("and 90-day automated backups described in section 5.2", "and 35-day automated backups described in section 5.2", 1),
        ("- Daily automated backups with 90-day retention", "- Daily automated backups with 35-day retention", 1),
        ("- 90-day retention for all production data", "- 35-day retention for all production data", 1),
        ("point-in-time recovery, 90-day backups,", "point-in-time recovery, 35-day backups,", 1),
    ],
    P + "cloud-infrastructure-security-policy.md": [
        ("- Daily automated DocumentDB backups with 90-day retention", "- Daily automated DocumentDB backups with 35-day retention", 1),
    ],
    P + "information-security-policy.md": [
        ("- Daily automated backups with 90-day retention", "- Daily automated backups with 35-day retention", 1),
    ],
    P + "data-classification-and-handling-standard.md": [
        ("Daily automated backups with 90-day retention", "Daily automated backups with 35-day retention", 1),
    ],
    P + "data-retention-and-disposal-policy.md": [
        ("|**Database backups (DocumentDB)**|90 days|", "|**Database backups (DocumentDB)**|35 days|", 1),
        ("DocumentDB automated backups expire per the 90-day retention setting", "DocumentDB automated backups expire per the 35-day retention setting", 1),
        ("backups purge the data through normal rotation (90 days)", "backups purge the data through normal rotation (35 days)", 1),
        ("|DocumentDB backups|90 days|", "|DocumentDB backups|35 days|", 1),
    ],
    P + "data-subject-rights-request-procedure.md": [
        ("under the 90-day backup retention cycle", "under the 35-day backup retention cycle", 1),
        ("- Backup data follows a 90-day rotation cycle", "- Backup data follows a 35-day rotation cycle", 1),
    ],
    P + "risk-assessment-procedure.md": [
        ("99.9 % SLA, 90-day backups", "99.9 % SLA, 35-day backups", 1),
    ],
    P + "system-description-v2.md": [
        ("daily automated backups retained 90 days with point-in-time recovery", "daily automated backups retained 35 days with point-in-time recovery", 1),
        ("daily automated backups retained 90 days, encrypted", "daily automated backups retained 35 days, encrypted", 1),
        ("backups retained 90 days with point-in-time recovery;", "backups retained 35 days with point-in-time recovery;", 1),
        ("staging environment, 90-day backups,", "staging environment, 35-day backups,", 1),
        ("the staging environment, 90-day backup retention, 7-year", "the staging environment, 35-day backup retention, 7-year", 1),
    ],
    Q + "controls-v2.json": [
        ("snapshots are retained 90 days", "snapshots are retained 35 days", 1),
        ("daily snapshots retained 90 days", "daily snapshots retained 35 days", 1),
        ("7-day retention -> 90 days (R3/R5)", "7-day retention -> 35 days (R3/R5, D27)", 1),
        ("7-day retention -> 90 days.", "7-day retention -> 35 days (D27).", 1),
        ("with 90-day automated backups", "with 35-day automated backups", 1),
    ],
    Q + "records-v2/tasks-v2.json": [
        ("daily automated snapshots, 90-day retention,", "daily automated snapshots, 35-day retention,", 1),
    ],
    Q + "records-v2/risks-v2.json": [
        ("retained 90 days", "retained 35 days", 2),
    ],
    Q + "records-v2/context-v2.json": [
        ("daily backups retained 90 days", "daily backups retained 35 days", 1),
    ],
    Q + "records-v2/policies-meta-v2.json": [
        ("90-day backups with point-in-time recovery", "35-day backups with point-in-time recovery", 1),
    ],
    Q + "records-v2/job-description-chief-executive-officer.md": [
        ("- Oversee daily automated backups with 90-day retention.", "- Oversee daily automated backups with 35-day retention.", 1),
    ],
    D + "09-POLICY-QUALITY-CHECK.md": [
        ("| Backups 90 days | DocumentDB `BackupRetentionPeriod` 35 → 90 |",
         "| ~~Backups 90 days~~ — **withdrawn 2026-11-01 (D27)**: 35 days kept | ~~DocumentDB `BackupRetentionPeriod` 35 → 90~~ |", 1),
    ],
    # lint: 35-day was banned while the target was 90
    P + "check.py": [
        ('r"\\b35[- ]day", ', '', 1),
    ],
}

DECISION = ("- D27 **DocumentDB backups 35 days** (Mo, 2026-11-01). Supersedes the 90-day target (RULEBOOK R3, "
            "2026-10-31 minutes §4.4). 35 days is the DocumentDB maximum and the live setting. Days only; all other "
            "wording as D26 left it. Infra: revert BackupRetentionPeriod 90 → 35 on di-backend-api "
            "`compliance/env-alignment` (commit 989ad81) before merging.\n")
CHANGES = ("\n\n## 2026-11-01 — D27: backups 35 days\n\n"
           "Applied by `scratch/backups-35-days-2026-11-01/days-only.py`: every DocumentDB backup retention of 90 days "
           "→ 35 days; no other wording changed.\n")


def main() -> int:
    errs = []
    for rel, edits in EDITS.items():
        f = ROOT / rel
        t = f.read_text()
        for old, new, n in edits:
            c = t.count(old)
            if c != n:
                errs.append(f"{rel}: expected {n} of {old[:70]!r}, found {c}")
                continue
            t = t.replace(old, new)
        f.write_text(t)
    if errs:
        print("\n".join(errs))
        return 1
    dec = ROOT / P / "DECISIONS-2026-10-31.md"
    dec.write_text(dec.read_text().rstrip("\n") + "\n" + DECISION)
    ch = ROOT / P / "CHANGES.md"
    ch.write_text(ch.read_text().rstrip("\n") + CHANGES)
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
