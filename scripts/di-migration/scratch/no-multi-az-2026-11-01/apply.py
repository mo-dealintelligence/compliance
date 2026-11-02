#!/usr/bin/env python3
"""D26 (Mo, 2026-11-01): no Multi-AZ DocumentDB. Amend the policies to the environment.

Production keeps ONE db.serverless instance (us-east-1a). DocumentDB cluster storage is
replicated six ways across three Availability Zones by the service; on instance or AZ
failure the service re-provisions the instance (no committed data lost; API unavailable
until it is back, within the BCP RTO). Point-in-time recovery + automated backups unchanged.

Every replacement is exact-match and must hit exactly the expected number of times, so a
re-run (or a file that changed underneath) fails loudly instead of half-applying.
Run from the compliance repo root:  python3 scripts/di-migration/scratch/no-multi-az-2026-11-01/apply.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = "scripts/di-migration/policies-v2/"
Q = "scripts/di-migration/scratch/quality-sweep/"
D = "docs/dealintelligence/"

STORAGE = "DocumentDB cluster storage replicated six ways across three availability zones"
RECOVER = "the single serverless instance re-provisioned automatically by the service on instance or availability-zone failure"

EDITS = {
    # ---------------- policies ----------------
    P + "cloud-infrastructure-security-policy.md": [
        ("- **Multi-AZ deployment**: distribution of resources across multiple availability zones for high availability",
         "- **Availability zone (AZ)**: an isolated location within an AWS region; the production VPC has private subnets in us-east-1a and us-east-1b"),
        ("- DocumentDB clusters are Multi-AZ (a second instance in another availability zone) with automatic failover",
         f"- {STORAGE}; the cluster runs a single serverless instance, which DocumentDB re-provisions automatically if the instance or its availability zone fails (no committed data is lost; recovery within the RTO in the Business Continuity Plan)"),
        ("- Automatic failover for Multi-AZ resources",
         "- Automatic re-provisioning of the DocumentDB instance by the service; point-in-time recovery from automated backups"),
        ("DocumentDB backup retention and Multi-AZ", "DocumentDB backup retention"),
    ],
    P + "business-continuity-plan.md": [
        ("- **Geographic scope**: The primary region (us-east-1) with Multi-AZ deployment (us-east-1a, us-east-1b)",
         "- **Geographic scope**: The primary region (us-east-1); private subnets and Lambda functions in us-east-1a and us-east-1b; DocumentDB storage replicated across three availability zones"),
        ("Resilience within the region is provided by the Multi-AZ deployment described in section 5;",
         "Resilience within the region is provided by the availability-zone design described in section 5 (Lambda functions in two availability zones, DocumentDB storage replicated across three, automatic re-provisioning of the DocumentDB instance);"),
        ("The RTO and RPO values above are met with the Multi-AZ DocumentDB deployment, point-in-time recovery, and 90-day automated backups described in section 5.2.",
         "The RTO and RPO values above are met with DocumentDB's automatic re-provisioning of its single serverless instance (cluster storage is replicated across three availability zones, so an instance or zone failure loses no committed data), point-in-time recovery, and 90-day automated backups described in section 5.2."),
        ("- Multi-AZ deployment across us-east-1a and us-east-1b\n- Automated failover for database services (Multi-AZ DocumentDB with a second instance in another availability zone)",
         f"- Lambda functions and private subnets in us-east-1a and us-east-1b\n- {STORAGE}; {RECOVER}"),
        ("- Database replication across availability zones",
         "- DocumentDB storage replication across three availability zones (performed by the service)"),
        ("(including DocumentDB backup retention and Multi-AZ)", "(including DocumentDB backup retention)"),
        ("- Multiple availability zones become unavailable",
         "- An availability-zone outage stops the DocumentDB instance and the service has not re-provisioned it within the RTO"),
        ("Primary strategy, Multi-AZ failover:\n\n- Automatic failover between us-east-1a and us-east-1b\n- Automatic failover of DocumentDB to the second instance in another availability zone\n",
         "Primary strategy, automatic recovery within the region:\n\n- DocumentDB re-provisions its single serverless instance automatically; cluster storage, replicated across three availability zones, is unaffected\n- If the instance is not available again within the RTO, restore the cluster with point-in-time recovery (section 7.1)\n"),
        ("restated around Multi-AZ DocumentDB, point-in-time recovery,",
         "restated around DocumentDB storage replication with automatic instance recovery, point-in-time recovery,"),
    ],
    P + "incident-response-procedure.md": [
        ("   - Confirm DocumentDB replication status", "   - Confirm the DocumentDB instance status is available"),
        ("- Failover to the alternate availability zone", "- Recovery of the DocumentDB instance or point-in-time restore"),
    ],
    P + "information-security-policy.md": [
        ("- Service availability risks, managed through Multi-AZ deployment and the 99.9 % uptime SLA",
         "- Service availability risks, managed through the availability-zone design (DocumentDB storage replicated across three availability zones with automatic instance recovery; Lambda functions in two availability zones), point-in-time recovery, and the 99.9 % uptime SLA"),
        ("- Multi-AZ deployment (us-east-1a, us-east-1b)",
         "- Lambda functions and private subnets in us-east-1a and us-east-1b; DocumentDB storage replicated across three availability zones with automatic instance recovery"),
    ],
    P + "risk-assessment-procedure.md": [
        ("| Multi-AZ DocumentDB, 99.9 % SLA, 90-day backups |",
         "| DocumentDB storage replicated across three availability zones with automatic instance recovery, 99.9 % SLA, 90-day backups |"),
    ],
    P + "service-level-agreement-sla-management-policy.md": [
        ("|AWS|Infrastructure|99.99 %|Multi-AZ deployment|",
         "|AWS|Infrastructure|Per-service AWS SLAs|Lambda in two availability zones; DocumentDB storage replicated across three with automatic instance recovery; point-in-time recovery|"),
    ],
    P + "system-monitoring-and-logging-procedure.md": [
        ("- DocumentDB backup retention and Multi-AZ\n", "- DocumentDB backup retention\n"),
        ("- Validating failover health", "- Detecting DocumentDB unavailability through the API error and latency alarms"),
    ],
    P + "penetration-testing-and-security-assessment-procedure.md": [
        ("DocumentDB backup retention and Multi-AZ", "DocumentDB backup retention"),
    ],
    P + "vulnerability-management-procedure.md": [
        ("DocumentDB backup retention and Multi-AZ", "DocumentDB backup retention"),
    ],
    P + "system-description-v2.md": [
        ("| Resilience and recovery | Multi-AZ DocumentDB with automatic failover;",
         "| Resilience and recovery | DocumentDB cluster storage replicated across three Availability Zones with automatic re-provisioning of the single serverless instance;"),
        ("Multi-AZ: second instance in another Availability Zone with automatic failover;",
         "Single serverless instance; cluster storage replicated six ways across three Availability Zones, instance re-provisioned automatically by the service on failure;"),
        ("DocumentDB backup retention and Multi-AZ", "DocumentDB backup retention"),
        ("**Business continuity.** Multi-AZ DocumentDB with automatic failover;",
         "**Business continuity.** DocumentDB storage replicated across three Availability Zones with automatic instance recovery;"),
        ("staging environment, Multi-AZ DocumentDB, 90-day backups", "staging environment, 90-day backups"),
        ("the staging environment, Multi-AZ DocumentDB, 90-day backup retention", "the staging environment, 90-day backup retention"),
    ],
    # ---------------- rulebook / lint ----------------
    P + "RULEBOOK.md": [
        ("- DocumentDB **Multi-AZ** (a second instance in another AZ, automatic\n  failover).\n", ""),
        ("| Blue-green / canary deployments, load balancers, auto-scaling groups, circuit breakers, read replicas | Lambda versioned deployments with rollback via `serverless rollback`; reserved concurrency; Multi-AZ DocumentDB (R3) |",
         "| Blue-green / canary deployments, load balancers, auto-scaling groups, circuit breakers, read replicas | Lambda versioned deployments with rollback via `serverless rollback`; reserved concurrency; DocumentDB storage replicated across three AZs with automatic instance recovery |\n"
         "| Multi-AZ DocumentDB, a second / standby DocumentDB instance, automatic failover to a replica or another AZ (D26, 2026-11-01) | DocumentDB cluster storage replicated six ways across three availability zones by the service; a single `db.serverless` instance that DocumentDB re-provisions automatically on instance or AZ failure (no committed data lost; recovery within the BCP RTO); point-in-time recovery and automated backups; quarterly restore test |"),
    ],
    P + "check.py": [
        ('r"\\bPropelAuth MFA", r"\\b99\\.95\\s?%"],',
         'r"\\bPropelAuth MFA", r"\\b99\\.95\\s?%",\n                   # D26 (2026-11-01): no Multi-AZ DocumentDB\n                   r"\\bMulti-AZ\\b", r"\\bsecond (DocumentDB )?instance\\b", r"\\bstandby instance", r"\\bfailover of DocumentDB",\n                   r"\\bfail ?over to the (second instance|alternate availability zone)"],'),
    ],
    # ---------------- records / controls / tasks ----------------
    Q + "controls-v2.json": [
        ("Implementation: DocumentDB runs Multi-AZ with automatic failover; the compliance platform BCP dashboard records",
         "Implementation: DocumentDB cluster storage is replicated across three availability zones and the single serverless instance is re-provisioned automatically by the service; the compliance platform BCP dashboard records"),
        ("DocumentDB runs Multi-AZ with daily snapshots retained 90 days",
         "DocumentDB storage is replicated across three availability zones, with daily snapshots retained 90 days"),
        ("DocumentDB backups and Multi-AZ)", "DocumentDB backups)"),
        ("Implementation: DocumentDB runs Multi-AZ with automatic failover in a single region (us-east-1) by design;",
         "Implementation: DocumentDB runs a single serverless instance with storage replicated across three availability zones and automatic instance recovery, in a single region (us-east-1) by design;"),
        ("backed by Multi-AZ DocumentDB with 90-day automated backups",
         "backed by DocumentDB storage replicated across three availability zones with 90-day automated backups"),
        ("\\\"across 3 availability zones\\\" -> Multi-AZ per R3 wording;",
         "\\\"across 3 availability zones\\\" -> storage replicated across three AZs (D26, 2026-11-01; was Multi-AZ per R3);"),
    ],
    Q + "records-v2/tasks-v2.json": [
        ("showing Multi-AZ instances, KMS storage encryption", "showing the cluster instance and its Availability Zone, KMS storage encryption"),
        ("DocumentDB backup retention and Multi-AZ.", "DocumentDB backup retention."),
    ],
    Q + "records-v2/risks-v2.json": [
        ("Treatment: Multi-AZ DocumentDB in us-east-1;",
         "Treatment: DocumentDB in us-east-1 with storage replicated across three availability zones and automatic instance recovery;"),
        ("Treatment: Multi-AZ DocumentDB with automatic failover;",
         "Treatment: DocumentDB storage replicated across three availability zones with automatic instance recovery;"),
    ],
    Q + "records-v2/management-meeting-minutes-2026-10-31.md": [
        ("Decision: KMS key-separation design is kept in the standard and the AWS change is recorded as a to-do (D2).",
         "Corrected 2026-11-01: the Multi-AZ row above is withdrawn — the single DocumentDB serverless instance is kept and the policies describe storage replication across three availability zones with automatic instance recovery instead (D26). The same correction applies to \"DocumentDB backup retention and Multi-AZ\" in the configuration-check checklist below (now: DocumentDB backup retention).\n\n"
         "Decision: KMS key-separation design is kept in the standard and the AWS change is recorded as a to-do (D2)."),
    ],
    # ---------------- program docs ----------------
    D + "05-GAPS-AND-LATER.md": [
        ("DocumentDB backup retention + Multi-AZ →", "DocumentDB backup retention →"),
    ],
    D + "09-POLICY-QUALITY-CHECK.md": [
        ("| Multi‑AZ DocumentDB | second `db.serverless` instance in us‑east‑1b (auto‑promoted replica) | ~$15–20/mo idle, more under load; no downtime | prepared on the same branch |",
         "| ~~Multi‑AZ DocumentDB~~ | ~~second `db.serverless` instance in us‑east‑1b~~ | — | **withdrawn 2026-11-01 (D26)**: single instance kept, moved to H2; the instance was removed from `compliance/env-alignment` (commit 404aeb5) |"),
        ("| Claim to remove or reword | Where | Replace with |\n|---|---|---|\n",
         "| Claim to remove or reword | Where | Replace with |\n|---|---|---|\n"
         "| Multi‑AZ DocumentDB / second instance / automatic failover (D26, 2026-11-01) | BCP, Cloud Infra, InfoSec, IR, Risk, SLA, Monitoring, system description, controls, risks, tasks | cluster storage replicated six ways across three AZs by the service; single `db.serverless` instance re-provisioned automatically on failure; PITR + automated backups; BCP RTO unchanged |\n"),
    ],
}

APPEND_NOTE = (
    "\n\n## Decision applied (2026-11-01)\n\n"
    "- D26: no Multi-AZ DocumentDB (Mo, 2026-11-01; a standby instance is not worth the cost). "
    "Multi-AZ / second-instance / automatic-failover wording replaced by: DocumentDB cluster storage "
    "replicated six ways across three availability zones by the service; a single serverless instance "
    "re-provisioned automatically on instance or AZ failure; point-in-time recovery and automated backups. "
    "\"DocumentDB backup retention and Multi-AZ\" in the configuration-check checklist → \"DocumentDB backup retention\".\n"
)
CHANGE_NOTES = [
    "business-continuity-plan", "cloud-infrastructure-security-policy", "incident-response-procedure",
    "information-security-policy", "risk-assessment-procedure", "service-level-agreement-sla-management-policy",
    "system-monitoring-and-logging-procedure", "system-description-v2",
]

DECISION = (
    "\n\n## 2026-11-01\n"
    "- D26 **No Multi-AZ DocumentDB** (supersedes the Multi-AZ item in RULEBOOK R3, the environment to-do in the "
    "2026-10-31 minutes §4.4, and \"and Multi-AZ\" in the D12 configuration-check checklist). Production keeps one "
    "`db.serverless` instance in us-east-1a. Policies state what is true: cluster storage replicated six ways across three "
    "availability zones by the service; the instance re-provisioned automatically on instance or AZ failure (no committed "
    "data lost; API unavailable until it recovers, within the BCP RTO of 2 hours for database services); point-in-time "
    "recovery and automated backups (90 days once the env-alignment branch deploys). Never claim Multi-AZ, a second/standby "
    "instance, or failover to a replica. Infra: the second instance was removed from di-backend-api branch "
    "`compliance/env-alignment` (commit 404aeb5, not deployed). Lint: check.py now flags the old wording.\n"
)

CHANGES_ENTRY = (
    "\n\n## 2026-11-01 — D26: no Multi-AZ DocumentDB\n\n"
    "Applied by `scratch/no-multi-az-2026-11-01/apply.py`. Edited: business-continuity-plan, cloud-infrastructure-security-policy, "
    "incident-response-procedure, information-security-policy, risk-assessment-procedure, service-level-agreement-sla-management-policy, "
    "system-monitoring-and-logging-procedure, penetration-testing-and-security-assessment-procedure, vulnerability-management-procedure, "
    "system-description-v2; RULEBOOK (R3 bullet removed, R4 row added), check.py (new R4 patterns); controls-v2.json (5 control notes), "
    "risks-v2.json (2 treatments), tasks-v2.json (2 evidence descriptions), management-meeting-minutes-2026-10-31 (correction note, row kept); "
    "docs/05, docs/09 (§H1 row withdrawn, §H2 row added). The earlier open items on BCP \"AZ failover testing\" are moot: there is no failover "
    "to test; the quarterly restore test covers recovery.\n"
)


def main() -> int:
    """All-or-nothing: every edit is computed in memory first; if any expected match is
    missing (already applied, or the file changed underneath), nothing is written."""
    errors, out = [], {}
    for rel, pairs in EDITS.items():
        s = (ROOT / rel).read_text(encoding="utf-8")
        for old, new in pairs:
            n = s.count(old)
            if n != 1:
                errors.append(f"{rel}: expected 1 match, found {n}: {old[:80]!r}")
                continue
            s = s.replace(old, new)
        out[rel] = s
    for name in CHANGE_NOTES:
        rel = P + "changes/" + name + ".md"
        s = (ROOT / rel).read_text(encoding="utf-8")
        if "D26:" in s:
            errors.append(f"{rel}: D26 note already present")
        out[rel] = s.rstrip("\n") + APPEND_NOTE
    for rel, block in ((P + "DECISIONS-2026-10-31.md", DECISION), (P + "CHANGES.md", CHANGES_ENTRY)):
        s = (ROOT / rel).read_text(encoding="utf-8")
        if "D26" in s:
            errors.append(f"{rel}: D26 already present")
        out[rel] = s.rstrip("\n") + block
    if errors:
        for e in errors:
            print("ERROR", e)
        print("nothing written")
        return 1
    for rel, s in out.items():
        (ROOT / rel).write_text(s, encoding="utf-8")
    print(f"applied: {len(out)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
