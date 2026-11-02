#!/usr/bin/env python3
"""Mo, 2026-11-01: system description v2 back to the February 2026 (Type I) wording where
he asked for it. Only system-description-v2.md is edited. Run from the compliance repo root.

Decisions applied (numbers = Mo's list):
 3  platform named "Comp AI" (was "the compliance platform"; Feb said Humadroid)
 6  zone resilience: original "multi-availability zone deployment with automated failover"
    (the Feb phrases "across AWS regions" and "triggered by CloudWatch monitoring" are not used:
    the platform is single-region and CloudWatch does not trigger failover)
 7  backups: original "daily automated backups supporting point-in-time recovery" (retention
    days live in the Data Retention and Disposal Policy: 35)
 8  recovery testing: original "quarterly recovery testing"
 10 CloudTrail 7 years kept (live: S3 lifecycle 2557 days, CloudWatch log group 2557 days);
    "transition to Glacier and Object Lock" removed (neither is configured)
 14 MFA: original "PropelAuth JWT authentication with multi-factor authentication"
 16 staging: original "staging environment for pre-production validation", no account detail
 17 vendors: annual review of the vendors' SOC 2 reports
 19 incidents: original 48-hour customer notification; retrospectives within 24 hours
 20 data requests: 30 days
Not changed here (open): 2 people, 9 Security Hub, 10b KMS rotation, 11 field-level
encryption, 15 change control, 18 self-assessment.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
F = ROOT / "scripts/di-migration/policies-v2/system-description-v2.md"

R = [
    # 14 MFA
    ("Sign-in is provided by PropelAuth using Google Workspace single sign-on as the only sign-in method, so multi-factor authentication is inherited from the customer's Google Workspace configuration.",
     "Sign-in is provided by PropelAuth JWT authentication with multi-factor authentication.", 1),
    ("- All user accounts authenticate through PropelAuth using Google Workspace single sign-on, with multi-factor authentication inherited from the customer's Google Workspace sign-in.",
     "- All user accounts authenticate through PropelAuth JWT authentication with multi-factor authentication.", 1),
    ("| PropelAuth JWT with Google Workspace single sign-on; role-based access control;",
     "| PropelAuth JWT authentication with multi-factor authentication; role-based access control;", 1),
    ("Google Workspace single sign-on (through which multi-factor authentication is inherited from the customer's Google Workspace);",
     "multi-factor authentication;", 1),
    ("PropelAuth JWT authentication with Google Workspace single sign-on (multi-factor authentication inherited from Google Workspace);",
     "PropelAuth JWT authentication with multi-factor authentication;", 1),
    # 19 incidents
    ("- Confirmed security incidents are notified to affected customers within 48 hours, and to the supervisory authority within 72 hours where GDPR applies.",
     "- Confirmed security incidents are notified to affected customers within 48 hours.", 1),
    ("customer incident notification within 48 hours and supervisory authority notification within 72 hours where GDPR applies,",
     "customer incident notification within 48 hours,", 1),
    ("P1 incidents acknowledged within 4 business hours; incident evidence retained for 7 years; customer notification within 48 hours; root cause analysis driving control improvements.",
     "48-hour breach notification to customers; post-incident retrospectives within 24 hours driving control improvements.", 1),
    ("- post-incident retrospectives feeding control improvements; and",
     "- post-incident retrospectives within 24 hours feeding control improvements; and", 1),
    # 6 + 7 + 8 resilience, backups, recovery testing
    ("| Resilience and recovery | DocumentDB cluster storage replicated across three Availability Zones with automatic re-provisioning of the single serverless instance; daily automated backups retained 35 days with point-in-time recovery; Lambda reserved concurrency and versioned deployments with rollback; quarterly backup-restore test; annual tabletop exercise |",
     "| Resilience and recovery | Multi-availability zone deployment with automated failover; daily automated backups supporting point-in-time recovery; Lambda reserved concurrency and versioned deployments with rollback; quarterly recovery testing |", 1),
    ("Single serverless instance; cluster storage replicated six ways across three Availability Zones, instance re-provisioned automatically by the service on failure; encrypted",
     "Multi-availability zone deployment with automated failover; encrypted", 1),
    ("daily automated backups retained 35 days, encrypted with a separate backup key; point-in-time recovery enabled;",
     "daily automated backups supporting point-in-time recovery, encrypted with a separate backup key;", 1),
    ("**Business continuity.** DocumentDB storage replicated across three Availability Zones with automatic instance recovery; backups retained 35 days with point-in-time recovery; quarterly backup-restore tests;",
     "**Business continuity.** Multi-availability zone deployment with automated failover; daily automated backups supporting point-in-time recovery; quarterly recovery testing;", 1),
    ("- quarterly backup-restore tests and an annual tabletop exercise;", "- quarterly recovery testing;", 1),
    ("| Recovery objectives, single-region statement, backup-restore and tabletop tests |",
     "| Recovery objectives, single-region statement, recovery testing |", 1),
    # 10 CloudTrail
    ("| Retained 7 years in S3 with lifecycle transition to Glacier and Object Lock |",
     "| Retained 7 years (S3 lifecycle and CloudWatch Logs retention) |", 1),
    # 16 staging
    ("A staging environment, deployed from the same CloudFormation templates into a separate AWS account in the same AWS Organization, is used for pre-production validation. It holds no production customer data (scrubbed or synthetic data only) and has its own network, database, keys, and secrets; no credential grants access to both accounts' workloads. The staging account is outside the system boundary (Section 4).",
     "A staging environment is used for pre-production validation.", 1),
    ("- The separate staging AWS account, its data, and personal credentials used for it.",
     "- Personal authentication credentials for non-production resources.", 1),
    # 17 vendors
    ("executed data processing agreements, security assessment, and annual review of PropelAuth and AWS |",
     "executed data processing agreements and annual review of the SOC 2 reports of PropelAuth and AWS |", 1),
    ("- Vendor risk is assessed annually for all sub-processors (CC9.2);",
     "- The SOC 2 reports of all sub-processors are reviewed annually (CC9.2);", 1),
    # 20 data requests
    ("within 30 days under GDPR and 45 days under CCPA", "within 30 days", None),
]


def main() -> int:
    t = F.read_text()
    errs = []
    for old, new, n in R:
        c = t.count(old)
        if (n is not None and c != n) or c == 0:
            errs.append(f"expected {n} of {old[:80]!r}, found {c}")
            continue
        t = t.replace(old, new)
    # 3 Comp AI
    t, k1 = re.subn(r"\bthe compliance platform's\b", "Comp AI's", t)
    t, k2 = re.subn(r"\b[Tt]he compliance platform\b", "Comp AI", t)
    print(f"Comp AI renames: {k1 + k2}")
    if errs:
        print("\n".join(errs))
        return 1
    F.write_text(t)
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Follow-up 2026-11-01 (Mo): item 17 reverted to the previous v2 wording
# ("executed data processing agreements, security assessment, and annual review of PropelAuth and AWS";
#  "Vendor risk is assessed annually for all sub-processors (CC9.2)").
