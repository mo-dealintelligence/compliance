#!/usr/bin/env python3
"""D27 (Mo, 2026-11-01): keep DocumentDB backups at 35 days; correct the D26 wording.

Run once from the compliance repo root after scratch/no-multi-az-2026-11-01/apply.py:
    python3 scripts/di-migration/scratch/backups-35-days-2026-11-01/apply.py

1. Backups: DocumentDB automated backups allow 1-35 days (AWS limit). Live cluster: 35.
   Every "90-day backups" claim becomes 35 days of point-in-time recovery.
2. AZ recovery (corrects D26): with no replica, DocumentDB re-creates a failed instance in
   the SAME availability zone, best effort (typically < 10 min, no committed data lost).
   During an outage of that zone the re-creation may not succeed; recovery is manual: add
   a db.serverless instance in us-east-1b to the same cluster (same endpoint).
   Point-in-time restore is for corruption/deletion, not for zone failures.
3. "Lambda in two AZs" is not counted as resilience: the database, the NAT instance and the
   Fargate subnet are all in us-east-1a.
4. The 2026-10-31 minutes are restored to their original text; D26 and D27 are recorded in
   a new dated decision record instead.

Exact-match replacements with expected counts: a re-run or a changed file fails loudly.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = "scripts/di-migration/policies-v2/"
Q = "scripts/di-migration/scratch/quality-sweep/"
D = "docs/dealintelligence/"

PITR35 = "continuous automated backups with 35-day point-in-time recovery"
INST = "automatic re-creation of the instance after an instance failure"
ZONE_RUNBOOK = ("if us-east-1a is unavailable, the CEO adds a db.serverless instance in us-east-1b to the "
                "same cluster, which takes over the same cluster endpoint")

EDITS = {
    P + "RULEBOOK.md": [
        ("- DocumentDB automated backups retained **90 days**, point-in-time recovery",
         "- DocumentDB automated backups retained **35 days** (the AWS maximum), point-in-time recovery (D27)", 1),
        ("- Backups: 90 days (R3).", "- Backups: 35 days, point-in-time recovery (R3, D27).", 1),
        ("a single `db.serverless` instance that DocumentDB re-provisions automatically on instance or AZ failure",
         "a single `db.serverless` instance that DocumentDB re-creates automatically after an instance failure "
         "(same AZ, best effort); after an AZ outage, recovery is manual (add an instance in us-east-1b)", 1),
    ],
    P + "business-continuity-plan.md": [
        ("(Lambda functions in two availability zones, DocumentDB storage replicated across three, automatic re-provisioning of the DocumentDB instance);",
         "(DocumentDB storage replicated across three availability zones, automatic re-creation of the DocumentDB instance after an instance failure, and manual recovery of the instance into us-east-1b after an outage of us-east-1a);", 1),
        ("are met with DocumentDB's automatic re-provisioning of its single serverless instance (cluster storage is replicated across three availability zones, so an instance or zone failure loses no committed data), point-in-time recovery, and 90-day automated backups described in section 5.2.",
         "are met with DocumentDB's automatic re-creation of its single serverless instance after an instance failure (typically within 10 minutes), manual recovery of the instance into another availability zone after a zone outage (section 7.2), and point-in-time recovery from 35 days of automated backups (section 5.2). Cluster storage is replicated across three availability zones, so neither failure loses committed data.", 1),
        ("the single serverless instance re-provisioned automatically by the service on instance or availability-zone failure",
         "the single serverless instance re-created automatically by the service after an instance failure; after an availability-zone outage the CEO adds an instance in another availability zone to the same cluster (section 7.2)", 1),
        ("- Daily automated backups with 90-day retention", "- Continuous automated backups with 35-day point-in-time recovery", 1),
        ("- An availability-zone outage stops the DocumentDB instance and the service has not re-provisioned it within the RTO",
         "- An availability-zone outage stops the DocumentDB instance (recovery is manual; section 7.2)", 1),
        ("- Daily automated backups at 02:00 UTC\n- 90-day retention for all production data",
         "- Continuous automated backups, with the daily backup window 03:00–04:00 UTC\n- 35-day retention for all production data (the DocumentDB maximum)", 1),
        ("- DocumentDB re-provisions its single serverless instance automatically; cluster storage, replicated across three availability zones, is unaffected\n"
         "- If the instance is not available again within the RTO, restore the cluster with point-in-time recovery (section 7.1)\n"
         "- Lambda functions distributed across availability zones\n",
         "- If the DocumentDB instance fails, the service re-creates it automatically in the same availability zone (typically within 10 minutes); cluster storage, replicated across three availability zones, is unaffected\n"
         "- If us-east-1a is unavailable, the CEO adds a `db.serverless` instance in us-east-1b to the same cluster (`aws docdb create-db-instance`); it takes over the same cluster endpoint, so no configuration change is needed\n"
         "- Point-in-time recovery (section 7.1) is used for data corruption or deletion, not for availability-zone failures\n"
         "- Lambda functions run in us-east-1a and us-east-1b; the NAT instance and the Fargate subnet are in us-east-1a, so outbound calls to customer CRMs and Slack and the data-collection jobs resume when us-east-1a recovers\n", 1),
        ("restated around DocumentDB storage replication with automatic instance recovery, point-in-time recovery, 90-day backups,",
         "restated around DocumentDB storage replication, automatic instance re-creation, manual availability-zone recovery, 35-day point-in-time recovery,", 1),
    ],
    P + "cloud-infrastructure-security-policy.md": [
        ("which DocumentDB re-provisions automatically if the instance or its availability zone fails (no committed data is lost; recovery within the RTO in the Business Continuity Plan)",
         "which DocumentDB re-creates automatically after an instance failure; after an availability-zone outage the instance is recovered manually into another availability zone (no committed data is lost in either case; recovery within the RTO in the Business Continuity Plan)", 1),
        ("- Daily automated DocumentDB backups with 90-day retention", "- Continuous automated DocumentDB backups with 35-day point-in-time recovery", 1),
        ("- Automatic re-provisioning of the DocumentDB instance by the service; point-in-time recovery from automated backups",
         "- Automatic re-creation of the DocumentDB instance after an instance failure; manual recovery into another availability zone after a zone outage; point-in-time recovery from automated backups for data corruption or deletion", 1),
    ],
    P + "information-security-policy.md": [
        ("managed through the availability-zone design (DocumentDB storage replicated across three availability zones with automatic instance recovery; Lambda functions in two availability zones), point-in-time recovery,",
         "managed through DocumentDB storage replicated across three availability zones with " + INST + " and manual recovery into another zone, 35-day point-in-time recovery,", 1),
        ("DocumentDB storage replicated across three availability zones with automatic instance recovery",
         "DocumentDB storage replicated across three availability zones with " + INST, 1),
        ("- Daily automated backups with 90-day retention", "- Continuous automated backups with 35-day point-in-time recovery", 1),
    ],
    P + "service-level-agreement-sla-management-policy.md": [
        ("|Lambda in two availability zones; DocumentDB storage replicated across three with automatic instance recovery; point-in-time recovery|",
         "|DocumentDB storage replicated across three availability zones with " + INST + "; 35-day point-in-time recovery|", 1),
    ],
    P + "risk-assessment-procedure.md": [
        ("DocumentDB storage replicated across three availability zones with automatic instance recovery, 99.9 % SLA, 90-day backups",
         "DocumentDB storage replicated across three availability zones with " + INST + ", 99.9 % SLA, 35-day point-in-time recovery", 1),
    ],
    P + "data-classification-and-handling-standard.md": [
        ("- **Backup storage**: Daily automated backups with 90-day retention",
         "- **Backup storage**: " + PITR35[0].upper() + PITR35[1:], 1),
    ],
    P + "data-retention-and-disposal-policy.md": [
        ("|**Database backups (DocumentDB)**|90 days|", "|**Database backups (DocumentDB)**|35 days|", 1),
        ("1. DocumentDB automated backups expire per the 90-day retention setting",
         "1. DocumentDB automated backups expire per the 35-day retention setting", 1),
        ("backups purge the data through normal rotation (90 days)", "backups purge the data through normal rotation (35 days)", 1),
        ("|DocumentDB backups|90 days|Automated backup retention|", "|DocumentDB backups|35 days|Automated backup retention|", 1),
    ],
    P + "data-subject-rights-request-procedure.md": [
        ("Backup copies expire under the 90-day backup retention cycle", "Backup copies expire under the 35-day backup retention cycle", 1),
        ("- Backup data follows a 90-day rotation cycle", "- Backup data follows a 35-day rotation cycle", 1),
    ],
    P + "system-description-v2.md": [
        ("with automatic re-provisioning of the single serverless instance; daily automated backups retained 90 days with point-in-time recovery;",
         "with automatic re-creation of the single serverless instance after an instance failure and manual recovery into another zone after a zone outage; " + PITR35 + ";", 1),
        ("instance re-provisioned automatically by the service on failure;",
         "instance re-created automatically by the service after an instance failure and recovered manually into another Availability Zone after a zone outage;", 1),
        ("daily automated backups retained 90 days, encrypted", "automated backups retained 35 days, encrypted", 1),
        ("with automatic instance recovery; backups retained 90 days with point-in-time recovery;",
         "with " + INST + " and manual recovery into another zone; backups retained 35 days with point-in-time recovery;", 1),
        ("staging environment, 90-day backups,", "staging environment, 35-day backups,", 1),
    ],
    P + "DECISIONS-2026-10-31.md": [
        ("the instance re-provisioned automatically on instance or AZ failure (no committed data lost; API unavailable until it recovers, within the BCP RTO of 2 hours for database services); point-in-time recovery and automated backups (90 days once the env-alignment branch deploys).",
         "the instance re-created automatically after an instance failure (same AZ, best effort; typically < 10 min); after an outage of us-east-1a, recovery is manual: add a db.serverless instance in us-east-1b to the same cluster (no committed data lost; API unavailable until then, within the BCP RTO of 2 hours for database services); point-in-time recovery from automated backups retained 35 days (D27).", 1),
    ],
    Q + "controls-v2.json": [
        ("DocumentDB automated daily snapshots are retained 90 days with point-in-time recovery enabled",
         "DocumentDB automated backups are retained 35 days with point-in-time recovery enabled", 1),
        ("with daily snapshots retained 90 days and point-in-time recovery enabled",
         "with automated backups retained 35 days and point-in-time recovery enabled", 1),
        ("7-day retention -> 90 days (R3/R5);", "7-day retention -> 35 days (R3/R5, D27);", 1),
        ("7-day retention -> 90 days.", "7-day retention -> 35 days (D27).", 1),
        ("the single serverless instance is re-provisioned automatically by the service;",
         "the single serverless instance is re-created automatically after an instance failure and recovered manually into another zone after a zone outage;", 1),
        ("backed by DocumentDB storage replicated across three availability zones with 90-day automated backups",
         "backed by DocumentDB storage replicated across three availability zones with 35-day point-in-time recovery", 1),
        ("runs a single serverless instance with storage replicated across three availability zones and automatic instance recovery,",
         "runs a single serverless instance with storage replicated across three availability zones, " + INST + " and manual zone recovery,", 1),
        ("with daily snapshots retained 90 days\"", "with automated backups retained 35 days\"", 0),
    ],
    Q + "records-v2/tasks-v2.json": [
        ("showing daily automated snapshots, 90-day retention, and point-in-time recovery enabled",
         "showing 35-day backup retention and point-in-time recovery enabled", 1),
    ],
    Q + "records-v2/risks-v2.json": [
        ("with automatic instance recovery", "with " + INST + " and manual zone recovery", 1),
        ("availability zones and automatic instance recovery;", "availability zones, " + INST + " and manual zone recovery;", 1),
    ],
    Q + "records-v2/context-v2.json": [
        ("DocumentDB (Multi-AZ, KMS encryption, daily backups retained 90 days with point-in-time recovery)",
         "DocumentDB (single serverless instance, storage replicated across three availability zones, KMS encryption, automated backups with 35-day point-in-time recovery)", 1),
    ],
    Q + "records-v2/policies-meta-v2.json": [
        ("Multi-AZ DocumentDB, 90-day backups with point-in-time recovery,",
         "DocumentDB storage replicated across three availability zones with instance re-creation and manual zone recovery, 35-day point-in-time recovery,", 1),
    ],
    Q + "records-v2/job-description-chief-executive-officer.md": [
        ("- Oversee daily automated backups with 90-day retention.", "- Oversee automated backups with 35-day point-in-time recovery.", 1),
    ],
    # D26 correction note inserted into dated minutes: removed (recorded in a new decision record instead)
    Q + "records-v2/management-meeting-minutes-2026-10-31.md": [
        ("Corrected 2026-11-01: the Multi-AZ row above is withdrawn — the single DocumentDB serverless instance is kept and the policies describe storage replication across three availability zones with automatic instance recovery instead (D26). The same correction applies to \"DocumentDB backup retention and Multi-AZ\" in the configuration-check checklist below (now: DocumentDB backup retention).\n\n", "", 1),
    ],
    D + "09-POLICY-QUALITY-CHECK.md": [
        ("| Backups 90 days | DocumentDB `BackupRetentionPeriod` 35 → 90 |",
         "| ~~Backups 90 days~~ — **withdrawn 2026-11-01 (D27)**: 35 days is the DocumentDB maximum and is kept | ~~DocumentDB `BackupRetentionPeriod` 35 → 90~~ |", 1),
    ],
}

CHANGE_NOTE_OLD = "a single serverless instance re-provisioned automatically on instance or AZ failure"
CHANGE_NOTE_NEW = ("a single serverless instance re-created automatically after an instance failure (same AZ, best effort), "
                   "recovered manually into us-east-1b after an outage of us-east-1a (corrected 2026-11-01, D27)")
CHANGE_NOTE_FILES = ["business-continuity-plan", "cloud-infrastructure-security-policy", "incident-response-procedure",
                     "information-security-policy", "risk-assessment-procedure", "service-level-agreement-sla-management-policy",
                     "system-monitoring-and-logging-procedure", "system-description-v2"]

CHECK_OLD = '# D26 (2026-11-01): no Multi-AZ DocumentDB\n'
CHECK_NEW = ('# D26 (2026-11-01): no Multi-AZ DocumentDB\n'
             '                   # D27 (2026-11-01): backups 35 days; no automatic recovery claimed for AZ outages\n'
             '                   r"\\b90[- ]day (automated )?backups?\\b", r"\\bbackups? retained 90\\b", r"\\bre-provision",\n'
             '                   r"\\bautomatic instance recovery\\b",\n')

DECISION = (
    "- D27 **DocumentDB backups 35 days** (Mo, 2026-11-01; supersedes the 90-day target in RULEBOOK R3 and the "
    "2026-10-31 minutes §4.4). 35 days is the DocumentDB maximum for automated backups and the live setting; no "
    "extra snapshots or AWS Backup plan. Also corrects D26: a failed instance is re-created automatically in the "
    "same AZ (best effort); an outage of us-east-1a is recovered manually by adding an instance in us-east-1b. "
    "Point-in-time restore is for corruption/deletion. \"Lambda in two AZs\" is not counted as resilience (DB, NAT "
    "and Fargate are in us-east-1a). Infra: `compliance/env-alignment` still sets BackupRetentionPeriod 90 "
    "(commit 989ad81) — revert to 35 before merging or the deploy fails.\n"
)

CHANGES_ENTRY = (
    "\n\n## 2026-11-01 — D27: backups 35 days; D26 wording corrected\n\n"
    "Applied by `scratch/backups-35-days-2026-11-01/apply.py`. 90-day backup claims → 35-day point-in-time recovery "
    "(BCP, Cloud Infra, InfoSec, Data Classification, Data Retention, DSR procedure, Risk Assessment, system description, "
    "RULEBOOK, controls, tasks, context, policy metadata, CEO job description). Availability-zone recovery restated: "
    "instance re-creation is automatic only for instance failures; zone outages are recovered manually (BCP §7.2 runbook "
    "added); point-in-time restore limited to corruption/deletion; Lambda-in-two-AZs no longer counted as resilience. "
    "Missed D26 spots fixed (context-v2.json, policies-meta-v2.json still said Multi-AZ). Correction note removed from "
    "the 2026-10-31 minutes; D26/D27 recorded in records-v2/decision-record-2026-11-01.md. check.py flags the old wording. "
    "Not edited (historical records): annual-performance-evaluation-ceo.md (2025).\n"
)

DECISION_RECORD = """---
title: Decision record — DocumentDB availability and backup retention
date: November 1, 2026
author: Mo Messidi, Chief Executive Officer
---

# Decision record — November 1, 2026

Decisions taken by the CEO on November 1, 2026. They amend the targets recorded in the management meeting minutes of October 31, 2026 (section 4.4), which are left unchanged.

## D26 — No second DocumentDB instance

**Decision.** Production keeps one `db.serverless` DocumentDB instance in us-east-1a. No standby instance in a second availability zone is deployed.

**Basis.** DocumentDB cluster storage is replicated six ways across three availability zones, so an instance or zone failure loses no committed data. A standby instance only shortens recovery of the compute.

**Effect on recovery.**
- Instance failure: DocumentDB re-creates the instance automatically in the same availability zone, typically within 10 minutes.
- Outage of us-east-1a: re-creation in that zone may not succeed. The CEO adds a `db.serverless` instance in us-east-1b to the same cluster; it takes over the cluster endpoint. Business Continuity Plan section 7.2.
- Data corruption or deletion: point-in-time restore.

**Withdrawn.** The October 31 target "DocumentDB Multi-AZ with automatic failover".

## D27 — DocumentDB backup retention 35 days

**Decision.** DocumentDB automated backups are retained 35 days with point-in-time recovery, the maximum the service supports and the current setting. No additional snapshots or backup service.

**Withdrawn.** The October 31 target "90-day retention with point-in-time recovery".

**Evidence.** Quarterly backup-restore test recorded in the compliance platform.

## Policies updated

Business Continuity Plan, Cloud Infrastructure Security Policy, Information Security Policy, Incident Response Procedure, Risk Assessment Procedure, Service Level Agreement (SLA) Management Policy, System Monitoring and Logging Procedure, Data Classification and Handling Standard, Data Retention and Disposal Policy, Data Subject Rights Request Procedure, Penetration Testing and Security Assessment Procedure, Vulnerability Management Procedure, and the system description.
"""


def main() -> int:
    errors = []
    for rel, edits in EDITS.items():
        path = ROOT / rel
        text = path.read_text()
        for old, new, n in edits:
            found = text.count(old)
            if found != n:
                errors.append(f"{rel}: expected {n} of {old[:80]!r}, found {found}")
                continue
            text = text.replace(old, new)
        path.write_text(text)
    for name in CHANGE_NOTE_FILES:
        path = ROOT / P / "changes" / f"{name}.md"
        text = path.read_text()
        if text.count(CHANGE_NOTE_OLD) != 1:
            errors.append(f"changes/{name}.md: change note not found once")
            continue
        path.write_text(text.replace(CHANGE_NOTE_OLD, CHANGE_NOTE_NEW))
    chk = ROOT / P / "check.py"
    t = chk.read_text()
    if t.count(CHECK_OLD) != 1:
        errors.append("check.py: D26 anchor not found once")
    else:
        chk.write_text(t.replace(CHECK_OLD, CHECK_NEW))
    dec = ROOT / P / "DECISIONS-2026-10-31.md"
    dec.write_text(dec.read_text().rstrip("\n") + "\n" + DECISION)
    ch = ROOT / P / "CHANGES.md"
    ch.write_text(ch.read_text().rstrip("\n") + CHANGES_ENTRY)
    rec = ROOT / Q / "records-v2" / "decision-record-2026-11-01.md"
    rec.write_text(DECISION_RECORD)
    if errors:
        print("\n".join(errors))
        return 1
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Follow-up edits applied by hand after the run above (2026-11-01), recorded here:
# - business-continuity-plan.md: "35-day retention for all production data" -> "35-day backup retention covering all production data".
#
# - check.py: removed r"\b35[- ]day" from "R5 numbers" (it banned the old value when the target was 90).
# - system-description-v2.md: "90-day backup retention" dropped from the list of changes adopted in the period.
# - risks-v2.json: two "retained 90 days" backup mentions -> 35 days.
# - job-description-chief-executive-officer.md, organizational-structure.md: "Multi-AZ deployment" lines (missed by D26) reworded / removed.
# - Not edited (historical records): annual-performance-evaluation-ceo.md, board-management-meeting-minutes-q4-2025.md,
#   management-meeting-minutes-2026-10-31.md tables (superseded by records-v2/decision-record-2026-11-01.md).
