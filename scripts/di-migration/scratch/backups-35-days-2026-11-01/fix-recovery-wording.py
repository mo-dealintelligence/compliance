#!/usr/bin/env python3
"""Correct the D27 recovery wording (Mo, 2026-11-01).

apply.py (same folder) framed DocumentDB zone recovery as manual and said Lambda in two AZs
was not resilience. Both were wrong framings:
- DocumentDB re-creates a failed instance automatically after ANY failure, including an AZ
  failure (AWS: "If no Amazon DocumentDB replicas have been provisioned, in the case of a
  failure, Amazon DocumentDB will attempt to create a new instance for you automatically").
  The only manual step is a fallback if that re-creation has not completed within the RTO
  (AWS documents it as best effort when a zone is broadly affected).
- Lambda is a managed multi-AZ service; with VPC subnets in us-east-1a and us-east-1b it runs
  in either zone automatically (AWS FSBP Lambda.5 satisfied).

Ordered exact-substring replacements across the policy and record files; each must match at
least once overall. Run from the compliance repo root.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FILES = [
    *sorted((ROOT / "scripts/di-migration/policies-v2").glob("*.md")),
    *sorted((ROOT / "scripts/di-migration/policies-v2/changes").glob("*.md")),
    ROOT / "scripts/di-migration/scratch/quality-sweep/controls-v2.json",
    *sorted((ROOT / "scripts/di-migration/scratch/quality-sweep/records-v2").glob("*.json")),
    ROOT / "scripts/di-migration/scratch/quality-sweep/records-v2/decision-record-2026-11-01.md",
]
SKIP = {"CHANGES.md"}  # changelog entries keep their history

ANY = "after any failure, including an availability-zone failure"
REPL = [
    # BCP 7.2 runbook block
    ("- If the DocumentDB instance fails, the service re-creates it automatically in the same availability zone (typically within 10 minutes); cluster storage, replicated across three availability zones, is unaffected",
     "- If the DocumentDB instance or its availability zone fails, the service re-creates the instance automatically (typically within 10 minutes); cluster storage, replicated across three availability zones, is unaffected"),
    ("- If us-east-1a is unavailable, the CEO adds a `db.serverless` instance in us-east-1b to the same cluster",
     "- Fallback if automatic re-creation has not completed within the RTO: the CEO adds a `db.serverless` instance in us-east-1b to the same cluster"),
    ("- Lambda functions run in us-east-1a and us-east-1b; the NAT instance and the Fargate subnet are in us-east-1a, so outbound calls to customer CRMs and Slack and the data-collection jobs resume when us-east-1a recovers",
     "- Lambda runs across availability zones automatically (VPC subnets in us-east-1a and us-east-1b)"),
    # BCP prose
    ("automatic re-creation of the DocumentDB instance after an instance failure, and manual recovery of the instance into us-east-1b after an outage of us-east-1a)",
     "automatic re-creation of the DocumentDB instance " + ANY + ", and Lambda running across availability zones)"),
    ("after an instance failure (typically within 10 minutes), manual recovery of the instance into another availability zone after a zone outage (section 7.2), and",
     ANY + " (typically within 10 minutes), and"),
    ("re-created automatically by the service after an instance failure; after an availability-zone outage the CEO adds an instance in another availability zone to the same cluster (section 7.2)",
     "re-created automatically by the service " + ANY),
    ("- An availability-zone outage stops the DocumentDB instance (recovery is manual; section 7.2)",
     "- The DocumentDB instance has not been re-created automatically within the RTO (section 7.2)"),
    ("automatic instance re-creation, manual availability-zone recovery,",
     "automatic instance re-creation including after an availability-zone failure,"),
    # cloud infrastructure
    ("re-creates automatically after an instance failure; after an availability-zone outage the instance is recovered manually into another availability zone (no committed data is lost in either case;",
     "re-creates automatically " + ANY + " (no committed data is lost;"),
    ("Automatic re-creation of the DocumentDB instance after an instance failure; manual recovery into another availability zone after a zone outage;",
     "Automatic re-creation of the DocumentDB instance " + ANY + ";"),
    # system description
    ("after an instance failure and manual recovery into another zone after a zone outage", ANY),
    ("after an instance failure and recovered manually into another Availability Zone after a zone outage",
     "after any failure, including an Availability Zone failure"),
    # controls / risks / meta / others
    ("is re-created automatically after an instance failure and recovered manually into another zone after a zone outage",
     "is re-created automatically " + ANY),
    ("after an instance failure and manual zone recovery", ANY),
    ("after an instance failure and manual recovery into another zone", ANY),
    ("instance re-creation and manual zone recovery", "automatic instance re-creation including after an availability-zone failure"),
    ("re-creation of the instance after an instance failure", "re-creation of the instance " + ANY),
    # SLA row: Lambda back in
    ("|Per-service AWS SLAs|DocumentDB storage replicated", "|Per-service AWS SLAs|Lambda across availability zones; DocumentDB storage replicated"),
    # decision record
    ("- Instance failure: DocumentDB re-creates the instance automatically in the same availability zone, typically within 10 minutes.\n"
     "- Outage of us-east-1a: re-creation in that zone may not succeed. The CEO adds a `db.serverless` instance in us-east-1b to the same cluster; it takes over the cluster endpoint. Business Continuity Plan section 7.2.\n",
     "- Instance or availability-zone failure: DocumentDB re-creates the instance automatically, typically within 10 minutes; no committed data is lost.\n"
     "- Fallback if re-creation has not completed within the RTO: the CEO adds a `db.serverless` instance in us-east-1b to the same cluster; it takes over the cluster endpoint. Business Continuity Plan section 7.2.\n"),
    # decisions / rulebook notes
    ("the instance re-created automatically after an instance failure (same AZ, best effort; typically < 10 min); after an outage of us-east-1a, recovery is manual: add a db.serverless instance in us-east-1b to the same cluster",
     "the instance re-created automatically after any failure including an AZ failure (typically < 10 min); fallback if not back within the RTO: add a db.serverless instance in us-east-1b to the same cluster"),
    ("a single `db.serverless` instance that DocumentDB re-creates automatically after an instance failure (same AZ, best effort); after an AZ outage, recovery is manual (add an instance in us-east-1b)",
     "a single `db.serverless` instance that DocumentDB re-creates automatically after any failure including an AZ failure; fallback if not back within the RTO: add an instance in us-east-1b"),
    ("a failed instance is re-created automatically in the same AZ (best effort); an outage of us-east-1a is recovered manually by adding an instance in us-east-1b. Point-in-time restore is for corruption/deletion. \"Lambda in two AZs\" is not counted as resilience (DB, NAT and Fargate are in us-east-1a).",
     "a failed instance is re-created automatically after any failure including an AZ failure; adding an instance in us-east-1b is only the fallback if that has not completed within the RTO. Point-in-time restore is for corruption/deletion. Lambda runs across AZs automatically (corrected 2026-11-01)."),
    ("a single serverless instance re-created automatically after an instance failure (same AZ, best effort), recovered manually into us-east-1b after an outage of us-east-1a (corrected 2026-11-01, D27)",
     "a single serverless instance re-created automatically after any failure including an AZ failure; fallback: add an instance in us-east-1b (corrected 2026-11-01, D27)"),
]


def main() -> int:
    hits = {old: 0 for old, _ in REPL}
    for f in FILES:
        if f.name in SKIP or not f.exists():
            continue
        t = f.read_text()
        orig = t
        for old, new in REPL:
            c = t.count(old)
            if c:
                hits[old] += c
                t = t.replace(old, new)
        if t != orig:
            f.write_text(t)
            print(f"edited {f.relative_to(ROOT)}")
    missing = [o[:90] for o, n in hits.items() if n == 0]
    if missing:
        print("NOT FOUND:\n  " + "\n  ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
