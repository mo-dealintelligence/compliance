#!/usr/bin/env python3
"""Quality/tone sweep of the non-policy platform records (2026-10-31).

Reads scratch/quality-sweep/data/*.json (live platform dump) and writes the
revised copies to scratch/quality-sweep/records-v2/*-v2.json, same shape as
the inputs, text fields only. Rules: policies-v2/RULEBOOK.md (R1, R2, R4, R5,
R8) and scratch/quality-sweep/QUALITY-RUBRIC.md (Q1, Q2, Q4, Q5), plus Mo's
decisions in policies-v2/DECISIONS-2026-10-31.md (marked "D<n>" inline below;
see records-v2/CHANGES-records.md "Decisions applied"), including the
second-round answers (D12 Security Hub removed, D13b availability task, D23).

    python3 -I scratch/quality-sweep/build-records-v2.py
"""
import copy
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "records-v2"
OUT.mkdir(exist_ok=True)


def load(name):
    return json.loads((DATA / name).read_text())


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# risks.json — title + description (treatment stays inside the description,
# as in the input; treatmentStrategyDescription is null in every row)
# ---------------------------------------------------------------------------
RISKS = {
    "rsk_6ae4b0ed4b75bcffbc40d4db": {
        "title": "EXTERNAL_VENDOR-002 AWS critical vendor dependency",
        "description": (
            "Deal Intelligence runs the whole production platform (Lambda, DocumentDB, S3, CloudFront, KMS, "
            "CloudTrail) on AWS in us-east-1. A prolonged regional AWS outage, account compromise "
            "or suspension, or a material change in AWS terms would halt service delivery and could expose "
            "customer data. Affects: availability (99.9 % commitment), confidentiality of customer data. AWS is "
            "one of two sub-processors (with PropelAuth) and is covered by a Data Processing Agreement. "
            "Treatment: Multi-AZ DocumentDB in us-east-1; daily automated backups retained 90 days with "
            "point-in-time recovery; quarterly backup-restore test via infrastructure as code (CloudFormation "
            "through the Serverless Framework), recorded in the compliance platform; root-account MFA and "
            "least-privilege IAM; CloudTrail with security-relevant events alerting the CEO via SNS in real time "
            "(EventBridge rule and breach-detection Lambda) and a monthly configuration-check record; annual "
            "vendor review of AWS SOC 2 / ISO 27001 reports per the Vendor Management Policy; single region "
            "by design as stated in the Business Continuity Plan. Owner: CEO."
        ),
    },
    "rsk_6ae44677d90983dded2e3924": {
        "title": "CYBERSECURITY-001 Data breach or unauthorized access",
        "description": (
            "Unauthorized access to business contact information or customer account data through compromised "
            "credentials, misconfiguration, or an unpatched vulnerability. Affects: confidentiality of customer "
            "data; 48-hour customer breach-notification commitment. Treatment: personnel MFA enforced in Google "
            "Workspace, GitHub, and AWS, customer MFA inherited from Google Workspace sign-in via PropelAuth; "
            "least-privilege IAM and RBAC; VPC isolation; KMS encryption at rest and TLS 1.2+ in transit; "
            "CloudTrail monitoring with security-relevant events alerting via SNS in real time and a monthly "
            "configuration-check record in the compliance platform; quarterly access "
            "reviews via the access-review Lambda; Dependabot, ECR scan-on-push, and Trivy in CI. Owner: CEO."
        ),
    },
    "rsk_6ae44677ee4c16e89f414239": {
        "title": "TECHNOLOGY-001 Service availability disruption",
        "description": (
            "Failure of an AWS component (Lambda, Fargate, DocumentDB) or a deployment error interrupts the daily "
            "data delivery. Affects: availability (99.9 % uptime commitment). Treatment: Multi-AZ DocumentDB with "
            "automatic failover; CloudWatch alarms on API errors and latency (p95 > 2 seconds); DocumentDB backups "
            "retained 90 days with point-in-time recovery; Lambda versioned deployments with rollback via "
            "serverless rollback; Business Continuity Plan with a quarterly backup-restore test recorded in the "
            "compliance platform. Owner: CEO."
        ),
    },
    "rsk_6ae4467687c58cec1d7cbb79": {
        "title": "OPERATIONAL_PEOPLE-001 Key-person dependency — CEO holds all production access",
        "description": (
            "The Chief Executive Officer (CEO) is the only role with production access (AWS, GitHub, DocumentDB, "
            "PropelAuth administration) and owns every policy and control. Unavailability of the CEO would "
            "interrupt operations, incident response, compliance maintenance, and customer service delivery. "
            "Affects: availability, incident response, SOC 2 control operation. Score 32.0 (probability 4, "
            "impact 3: legal 3, financial 2, reputational 3). Treatment: compensating controls per the "
            "Organizational Structure — pull request with required CI status checks on the protected main "
            "branch and a logged self-review; automated checks (the monthly configuration-check Lambda, CloudTrail) "
            "with security-relevant events alerting via SNS in real time; dated control records in the compliance platform; independent review by the "
            "external SOC 2 auditor. Treatment action (planned, due December 31 [CONFIRM: year]): document all "
            "critical processes, establish emergency access procedures with a trusted third party, and create "
            "a knowledge-transfer repository. Owner: CEO."
        ),
    },
    "rsk_6ae4467603cb938df8e33de2": {
        "title": "EXTERNAL_VENDOR-001 PropelAuth service disruption",
        "description": (
            "An outage or security incident at PropelAuth (authentication sub-processor) blocks customer sign-in "
            "to the platform. Affects: availability of customer access; authentication availability is provided "
            "by PropelAuth under its own SLA. Treatment: annual vendor review per the Vendor Management Policy; "
            "monitoring of PropelAuth status; PropelAuth contingency and customer communication steps in the "
            "Business Continuity Plan. Owner: CEO."
        ),
    },
    "rsk_6ae4467643b88095c5b12882": {
        "title": "COMPLIANCE_REGULATORY-001 Compliance documentation gaps",
        "description": (
            "Policies, procedures, and evidence drift out of date between annual reviews, creating gaps against "
            "GDPR, CCPA, and SOC 2 requirements. Affects: audit readiness; regulatory obligations. Treatment: "
            "annual policy review cycle; monthly automated evidence and quarterly evidence sweep recorded in the "
            "compliance platform; compliance platform task reminders. Owner: CEO."
        ),
    },
    "rsk_6ae44676d35dcb7389034b5d": {
        "title": "COMPLIANCE-001 Incident response capacity",
        "description": (
            "Detection of and response to a security incident may be delayed when the CEO, as incident commander, "
            "is unavailable, affecting the 48-hour customer notification commitment and SOC 2 CC7.3–CC7.5. "
            "Affects: incident response targets; customer and regulatory notification. Treatment: breach-detection "
            "Lambda, triggered by an EventBridge rule on security-relevant CloudTrail events, that alerts the CEO "
            "via SNS in real time; Incident Response Procedure (P1 "
            "acknowledged within 4 business hours); AWS Support escalation path; annual tabletop exercise "
            "recorded in the compliance platform. Owner: CEO."
        ),
    },
}

risks = load("risks.json")
for r in risks:
    r.update(RISKS[r["id"]])
dump("risks-v2.json", risks)

# ---------------------------------------------------------------------------
# vendors.json — description only
# ---------------------------------------------------------------------------
# D15: sub-processors are AWS and PropelAuth only; Google Workspace, GitHub and
# Resend are vendors that do not process customer data (HubSpot is not in the register).
VENDORS = {
    "Resend": (
        "Transactional email delivery for the compliance platform (notifications, sign-in links). Receives "
        "recipient addresses and message content at send time only; holds no platform data. Vendor — does not "
        "process customer data; not a sub-processor. "
        "Reviewed annually by the CEO per the Vendor Management Policy."
    ),
    "Google Workspace": (
        "Personnel email, calendar, and document storage for Deal Intelligence LLC, and the identity provider for "
        "personnel single sign-on with MFA enforced. Vendor — does not process customer data; not a sub-processor; "
        "customer Google sign-in is handled by PropelAuth. "
        "Reviewed annually by the CEO (SOC 2 report and terms) per the Vendor Management Policy."
    ),
    "GitHub": (
        "Source control for dealintelligence/di-backend-api, GitHub Actions CI, Dependabot, code and secret "
        "scanning, and branch protection on main. No customer data enters the repository or CI. Vendor — does "
        "not process customer data; not a sub-processor. Reviewed annually by the CEO (SOC 2 report and terms) per the Vendor Management Policy."
    ),
    "PropelAuth": (
        "Authentication and identity management for the Deal Intelligence platform: JWT issuance, Google Workspace "
        "single sign-on (customer MFA inherited from Google Workspace), RBAC, session management. Sub-processor "
        "under a Data Processing Agreement; carve-out in the SOC 2 examination. Reviewed annually by the CEO "
        "(SOC 2 report and terms) per the Vendor Management Policy."
    ),
    "Amazon Web Services": (
        "Cloud hosting and encrypted storage for the Deal Intelligence platform in us-east-1: Lambda, Fargate, "
        "DocumentDB, S3, CloudFront, VPC, KMS, CloudTrail, EventBridge, SNS. Sub-processor under a Data Processing "
        "Agreement; carve-out in the SOC 2 examination. Reviewed annually by the CEO (SOC 2 / ISO 27001 reports "
        "and terms) per the Vendor Management Policy."
    ),
}
vendors = load("vendors.json")
for v in vendors:
    v["description"] = VENDORS[v["name"]]
dump("vendors-v2.json", vendors)

# ---------------------------------------------------------------------------
# people.json — jobTitle / department only
# ---------------------------------------------------------------------------
people = load("people.json")
for p in people:
    if p["user"]["email"] == "william@dealintelligence.io":
        p["jobTitle"] = "Go-to-Market Contractor"
        # department stays "none" — no platform department matches; see CHANGES
    elif p["user"]["email"] == "mo@dealintelligence.io":
        p["jobTitle"] = "Chief Executive Officer"
dump("people-v2.json", people)

# ---------------------------------------------------------------------------
# context.json — answer only
# ---------------------------------------------------------------------------
CONTEXT = {
    # people-tagged
    "ctx_6ae4467a11a0f73a4469b1cd": "Mo Messidi, Chief Executive Officer (CEO).",
    "ctx_6ae4467a997bc87734a00db9": "Mo Messidi, Chief Executive Officer (CEO).",
    # D23: ctx_6ae4467aa2b2f5daf5418873 (people-tagged duplicate of "How many
    # employees do you have?") is deleted; the onboarding entry whose answer is
    # the number (ctx_6ae43d2299a8b3b62cbc3b9b, "2") is kept — see CONTEXT_DELETE.
    # D23: sign-in method
    "ctx_6ae43d2271b191a10f8a9db3": "Google Workspace SSO and email/password, both with 2FA",
    # vendors
    "ctx_6ae44679adfe6e7474a57d5d": (
        "Amazon Web Services (infrastructure hosting) and PropelAuth (authentication) are the two subservice "
        "organizations (sub-processors) that process customer data on behalf of Deal Intelligence; both are "
        "carved out and covered by Data Processing Agreements. GitHub, Google Workspace, Resend, and the "
        "self-hosted compliance platform support operations but are not subservice organizations. "
        "Customer-controlled integrations (Slack, Salesforce, HubSpot, Clay) are outside the system boundary."
    ),
    "ctx_6ae4467999fa2ef21b09779b": (
        "Amazon Web Services (hosting and storage), PropelAuth (authentication), GitHub (source control and "
        "GitHub Actions CI), Google Workspace (personnel email and single sign-on)."
    ),
    # system description
    "ctx_6ae44679e2621a71c0853187": (
        "The in-scope system is the Deal Intelligence platform in AWS us-east-1: Lambda functions and Fargate "
        "containers (ECS) for compute, DocumentDB (Multi-AZ, KMS encryption, daily backups retained 90 days with "
        "point-in-time recovery), S3, CloudFront with AWS Shield Standard, EventBridge schedules, and a VPC with "
        "private subnets and no direct internet access to the database. Infrastructure is defined in "
        "CloudFormation via the Serverless Framework (stack di-backend-api-prod) and deployed by GitHub Actions "
        "from the dealintelligence/di-backend-api repository (pull request and CI status checks required on the "
        "protected main branch). Customer authentication is PropelAuth (JWT) with Google Workspace single sign-on, "
        "so customer MFA is inherited from Google Workspace; RBAC provides company- and user-level data isolation. "
        "Monitoring: CloudWatch (90-day log retention; alarms on API errors and latency), CloudTrail (7-year "
        "retention in S3), a scheduled configuration-check Lambda that runs monthly against a fixed checklist and "
        "posts a dated pass/fail record to the compliance platform, and an EventBridge rule that routes "
        "security-relevant CloudTrail events through the breach-detection Lambda to an SNS alert to the CEO in "
        "real time. The platform processes business "
        "contact information and competitor interaction data; active leads are retained 24 months and customer "
        "account data for the duration of the relationship plus 24 months. Subservice organizations: AWS and "
        "PropelAuth (carve-out). The compliance platform is self-hosted on AWS, holds compliance records only, and "
        "is outside the system boundary. Trust services categories: Security, Availability, Confidentiality."
    ),
    # mission — unchanged
    # services
    "ctx_6ae44678c2b732d987f6d0fa": (
        "Verified competitor activity events and competitor-customer lists delivered through a REST API, an MCP "
        "server for Claude and other AI clients, Clay enrichment, Salesforce and HubSpot CRM writes, Slack "
        "notifications, and webhooks. Events refresh daily, are named on both sides, and carry a confidence score "
        "of 0.95 or higher."
    ),
    # company background
    "ctx_6ae4467805be439197021862": (
        "Deal Intelligence LLC (Delaware) operates a business-to-business market intelligence platform. It "
        "surfaces verified competitor activity for revenue teams: named buyers at a customer's target accounts who "
        "have accepted outreach from named competitors, plus verified competitor-customer lists derived from DNS, "
        "certificate, and SSO/tenant evidence. The company is fully remote with no physical office; all "
        "infrastructure runs on AWS in us-east-1. Internal roles are the Chief Executive Officer (CEO), who holds "
        "all production access, and the Go-to-Market Contractor, who has none. [CONFIRM: v1 read \"founder-operated "
        "(single member LLC)\" — the legal form is omitted per RULEBOOK R2; add back if the auditor needs it]"
    ),
    # onboarding free-text
    "ctx_6ae43d220c17609277b54689": (
        "Deal Intelligence LLC operates a B2B market intelligence platform: verified competitor activity and "
        "competitor-customer lists for revenue teams, delivered by REST API, MCP server, Clay, CRM integrations, "
        "and Slack."
    ),
    "ctx_6ae43d221a8d934f7b43facf": json.dumps([{"name": "PropelAuth", "website": "https://propelauth.com"}]),
    "ctx_6ae43d22aa10e685567e25ae": json.dumps([{"name": "Mo Messidi", "title": "CEO"}]),
    "ctx_6ae43948bc1c823b62e62234": "SOC 2 (Security, Availability, Confidentiality)",
}
CONTEXT_DELETE = {"ctx_6ae4467aa2b2f5daf5418873"}  # D23: duplicate "How many employees do you have?"
context = load("context.json")
for c in context:
    if c["id"] in CONTEXT:
        c["answer"] = CONTEXT[c["id"]]
context = [c for c in context if c["id"] not in CONTEXT_DELETE]
dump("context-v2.json", context)

# ---------------------------------------------------------------------------
# tasks.json — title + description. Cadence per docs/dealintelligence/11 §2.
# Source-file line kept (it keys the screenshot uploader); PI/P criteria
# dropped from the Supports line (R1).
# ---------------------------------------------------------------------------
MONTHLY = "Cadence: monthly (automated evidence run)."
QUARTERLY = "Cadence: quarterly (evidence sweep)."
ANNUAL = "Cadence: annual (compliance week)."

TASKS = {
    "MacOS FileVault Status": (
        "macOS FileVault status screenshot",
        f"Screenshot of System Settings showing FileVault full-disk encryption enabled on each personnel macOS device (CEO; Go-to-Market Contractor). {QUARTERLY}",  # D4
    ),
    "GitHub Actions Workflows": (
        "GitHub Actions workflows screenshot",
        f"Screenshot of the Actions tab of dealintelligence/di-backend-api listing the CI workflows (lint, tests, Bandit, Trivy, TruffleHog). {QUARTERLY}",
    ),
    "GitHub Deploy Workflow": (
        "GitHub deploy workflow screenshot",
        f"Screenshot of the deploy workflow definition showing deployment runs only from a green CI run (serverless deploy). {QUARTERLY}",
    ),
    "GitHub Workflow Run Details": (
        "GitHub workflow run history screenshot",
        f"Screenshot of recent workflow runs showing CI execution history and status for dealintelligence/di-backend-api. {QUARTERLY}",
    ),
    "GitHub Dependabot": (
        "Dependabot alerts screenshot",
        f"Screenshot of the Dependabot alerts page showing open alerts by severity and automated update pull requests. {MONTHLY}",
    ),
    "GitHub Secret Scanning": (
        "GitHub code security settings screenshot",
        f"Screenshot of the repository's code security settings showing secret scanning, push protection, and code scanning enabled. {QUARTERLY}",
    ),
    "GitHub Branch Protection": (
        "GitHub branch protection screenshot",
        f"Screenshot of the branch protection rule for main: pull request required, CI status checks required, no direct pushes. {MONTHLY}",
    ),
    "Annual Performance Evaluation Ceo": (
        "CEO annual performance evaluation",
        f"The CEO's annual self-evaluation submitted in the employee-performance-evaluation form: criteria, ratings, evidence, and development actions. {ANNUAL}",
    ),
    "AWS Cloudformation Stacks": (
        "CloudFormation stacks screenshot",
        f"Screenshot of the CloudFormation console showing the di-backend-api-prod stack (and staging stage) with status and last update. {QUARTERLY}",
    ),
    "AWS CloudTrail Trails": (
        "CloudTrail trails screenshot",
        f"Screenshot of the CloudTrail console showing the trail enabled, the S3 destination, and log file validation. {MONTHLY}",
    ),
    "AWS CloudWatch Alarms": (
        "CloudWatch alarms screenshot",
        f"Screenshot of the CloudWatch alarms list showing the API error, latency (p95 > 2 seconds), and capacity alarms with their SNS actions and state. {MONTHLY}",
    ),
    "AWS CloudWatch Log Groups": (
        "CloudWatch log groups screenshot",
        f"Screenshot of the CloudWatch log groups list showing the Lambda and API audit log groups with 90-day retention. {MONTHLY}",
    ),
    "AWS DocumentDB Backups": (
        "DocumentDB backups screenshot",
        f"Screenshot of the DocumentDB backups view showing daily automated snapshots, 90-day retention, and point-in-time recovery enabled. {QUARTERLY}",
    ),
    "AWS DocumentDB Cluster": (
        "DocumentDB cluster configuration screenshot",
        f"Screenshot of the DocumentDB cluster details showing Multi-AZ instances, KMS storage encryption, TLS enforcement, and backup retention. {QUARTERLY}",
    ),
    "AWS ECR Repositories": (
        "ECR repositories and scan results screenshot",
        f"Screenshot of the ECR repositories list showing scan-on-push enabled and the latest image scan findings. {MONTHLY}",
    ),
    "AWS IAM Password Policy": (
        "IAM password policy screenshot",
        f"Screenshot of the IAM account password policy settings. {MONTHLY}",
    ),
    "AWS IAM Roles": (
        "IAM roles screenshot",
        f"Screenshot of the IAM roles list showing the Lambda execution and deployment roles with their attached policies. {QUARTERLY}",
    ),
    "AWS IAM Users": (
        "IAM users screenshot",
        f"Screenshot of the IAM users list showing each user, MFA status, and last activity, as input to the quarterly access review. {QUARTERLY}",
    ),
    "AWS KMS Keys": (
        "KMS keys screenshot",
        f"Screenshot of the KMS customer-managed keys list showing the keys, their status, and automatic annual rotation enabled. {MONTHLY}",
    ),
    "AWS Lambda Functions": (
        "Lambda functions inventory screenshot",
        f"Screenshot of the Lambda functions list showing the platform functions, including accessReview and dataRetentionEnforcement. {QUARTERLY}",
    ),
    "AWS S3 Bucket Encryption": (
        "S3 bucket encryption screenshot",
        f"Screenshot of a bucket's properties showing default encryption enabled. {MONTHLY}",
    ),
    "AWS S3 Buckets": (
        "S3 buckets and lifecycle rules screenshot",
        f"Screenshot of the S3 buckets list and the lifecycle rules on the CloudTrail bucket (Glacier transition, Object Lock, 7-year retention). {QUARTERLY}",
    ),
    "AWS Security Groups": (
        "VPC security groups screenshot",
        f"Screenshot of the security groups list with inbound and outbound rules showing no open administrative ports and database access limited to the VPC. {MONTHLY}",
    ),
    # D12: Security Hub removed. The findings task becomes the configuration-check
    # record; the summary task becomes the record of the real-time half of the
    # replacement control (EventBridge rule -> breach-detection Lambda -> SNS).
    "AWS Securityhub Findings": (
        "Configuration-check record (monthly)",
        f"Dated pass/fail record posted by the scheduled configuration-check Lambda, which runs monthly against a fixed checklist: CloudTrail enabled and log-file validation on; no public S3 buckets; no security groups open to 0.0.0.0/0 on administrative ports; root account MFA; IAM password policy; KMS key rotation; ECR scan-on-push; DocumentDB backup retention and Multi-AZ. Each failed item is reviewed by the CEO and tracked to remediation. {MONTHLY}",
    ),
    "AWS Securityhub Overview": (
        "Security-event alert rule screenshot",
        f"Screenshot of the EventBridge rule that matches security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) with the breach-detection Lambda as target, and the SNS subscription that alerts the CEO in real time. {MONTHLY}",
    ),
    "AWS SNS Topics": (
        "SNS topics screenshot",
        f"Screenshot of the SNS topics list showing the security-alert and incident-notification topics and their subscriptions. {MONTHLY}",
    ),
    "AWS VPC List": (
        "VPC list screenshot",
        f"Screenshot of the VPC console listing the platform VPC, as part of the asset inventory. {QUARTERLY}",
    ),
    "AWS VPC Subnets": (
        "VPC subnets screenshot",
        f"Screenshot of the subnets list showing the private subnets in us-east-1a and us-east-1b. {QUARTERLY}",
    ),
    "Board Management Meeting Minutes Q4 2025": (
        "Quarterly management meeting minutes",
        f"The quarter's management meeting minutes submitted in the board-meeting form: attendees by role, decisions, risk and access-review acknowledgment, vendor review, and action items with owner and due date. {QUARTERLY}",
    ),
    "CloudTrail Events": (
        "CloudTrail event export",
        f"JSON export of recent CloudTrail events (IAM and configuration changes) from the audit trail. {QUARTERLY}",
    ),
    "Ethics And Privacy Training Completion Certificate William Wickey": (
        "Go-to-Market Contractor training completion certificate",
        f"Training completion certificate for the Go-to-Market Contractor, generated by the compliance platform on completion of security awareness and privacy training. {ANNUAL}",
    ),
    "Ethics And Security Training Completion Certificate Mo Messidi": (
        "CEO training completion certificate",
        f"Training completion certificate for the CEO, generated by the compliance platform on completion of security awareness and ethics training. {ANNUAL}",
    ),
    "Ethics Violation Log 2025": (
        "Ethics violation log",
        f"The year's ethics violation log: reports received, investigations, resolutions, and the no-violations statement signed by the CEO. {ANNUAL} Updated within 48 hours of any report.",
    ),
    "Compliance Platform Bcp Dashboard": (
        "Business continuity plan record screenshot",
        f"Screenshot of the compliance platform's business continuity records showing the critical processes, RTO values, and active plans. {QUARTERLY}",
    ),
    "Compliance Platform Bcp Test Results": (
        "Backup restore test result record",
        f"The quarterly backup-restore test record in the compliance platform: date, snapshot restored, document count check, RTO achieved, and outcome. {QUARTERLY}",
    ),
    "Compliance Platform Incident Reporting": (
        "Incident records screenshot",
        f"Screenshot of the compliance platform's incident record list showing incidents for the period and their status. {QUARTERLY} Per event: open a record for each incident.",
    ),
    "Compliance Platform Risk Detail": (
        "Risk detail record screenshot",
        f"Screenshot of one risk record in the compliance platform showing likelihood and impact scoring, residual scores, and treatment. {QUARTERLY}",
    ),
    "Compliance Platform Risk Register": (
        "Risk register screenshot",
        f"Screenshot of the compliance platform's risk register showing all risks with category, scores, and treatment status, after the quarterly review. {QUARTERLY}",
    ),
    "Compliance Platform Vendor Assessment": (
        "Vendor assessment record screenshot",
        f"Screenshot of a vendor assessment record in the compliance platform (for example AWS) showing the SOC 2 report reviewed and the review date. {ANNUAL}",
    ),
    "Compliance Platform Vendor Dashboard": (
        "Vendor inventory screenshot",
        f"Screenshot of the compliance platform's vendor list showing each vendor, sub-processor flag, assessment status, and review date. {ANNUAL}",
    ),
    "Job Description Chief Executive Officer": (
        "CEO job description",
        f"Job Description - Chief Executive Officer: purpose, responsibilities, access level, required competence, and acknowledgment. {ANNUAL}",
    ),
    "Job Description Go To Market Contractor": (
        "Go-to-Market Contractor job description",
        f"Job Description - Go-to-Market Contractor: purpose, responsibilities, access level (no production access), required competence, and signed acknowledgment. {ANNUAL}",
    ),
    "Lambda App Events": (
        "Lambda application log export",
        f"JSON export of recent Lambda application log events from CloudWatch Logs showing operational and audit entries. {QUARTERLY}",
    ),
    "Organizational Structure": (
        "Organizational structure document",
        f"Organizational Structure: roles, holders, production access, reporting lines, and compensating controls. {ANNUAL}",
    ),
    "PropelAuth Api Keys": (
        "PropelAuth API keys screenshot",
        f"Screenshot of the PropelAuth API keys page showing the active keys and their creation dates, as input to the API key rotation calendar. {QUARTERLY}",
    ),
    "PropelAuth Mfa Settings": (
        "PropelAuth sign-in settings screenshot",
        f"Screenshot of the PropelAuth sign-in and MFA settings page showing Google Workspace single sign-on as the customer sign-in method (MFA inherited from Google Workspace). {QUARTERLY} [CONFIRM: that the page shows the Google SSO configuration]",
    ),
    "PropelAuth Roles": (
        "PropelAuth roles screenshot",
        f"Screenshot of the PropelAuth roles configuration (Owner, Admin, Member) and their permissions, as input to the quarterly access review. {QUARTERLY}",
    ),
    "PropelAuth Security Settings": (
        "PropelAuth security settings screenshot",
        f"Screenshot of the PropelAuth security settings page: password and session settings, allowed sign-in methods. {QUARTERLY}",
    ),
    "PropelAuth Users": (
        "PropelAuth users screenshot",
        f"Screenshot of the PropelAuth users list showing each user, organization, role, and last sign-in, as input to the quarterly access review. {QUARTERLY}",
    ),
    "VPC Flow Events": (
        "VPC Flow Logs export",
        f"JSON export of recent VPC Flow Log records (ACCEPT and REJECT) showing network traffic monitoring at the VPC boundary. {QUARTERLY}",
    ),
}

DROP_CRITERIA = re.compile(r"^(PI|P)\d")


def supports_line(desc):
    m = re.search(r"Supports: (.*)", desc)
    if not m:
        return None
    keep = [c.strip() for c in m.group(1).split(",") if not DROP_CRITERIA.match(c.strip())]
    return "Supports: " + ", ".join(keep) if keep else None


tasks = load("tasks.json")
for t in tasks:
    new_title, new_desc = TASKS[t["title"]]
    sup = supports_line(t["description"])
    src = re.search(r"Source file: (.*)", t["description"])
    tail = [s for s in (sup, f"Source file: {src.group(1).strip()}" if src else None) if s]
    t["title"] = new_title
    t["description"] = new_desc + ("\n\n" + "\n".join(tail) if tail else "")

# D13b: a monthly "Availability record (monthly)" task must exist (owner CEO).
# None does in the live dump, so it is appended with "new": true for the apply
# step to create (no id yet; frequency monthly; status todo).
if not any("vailability record" in t["title"] for t in tasks):
    tasks.append({
        "id": None,
        "new": True,
        "title": "Availability record (monthly)",
        "description": (
            "Monthly availability record for the Deal Intelligence platform: the month's uptime percentage against "
            "the 99.9 % commitment, measured over all minutes from CloudWatch metrics excluding announced maintenance "
            "windows, the minutes of unplanned downtime, and any customer-facing incident. Prepared by the CEO from "
            "the CloudWatch availability metrics; the Monday reminder email covers this task. "
            f"{MONTHLY}\n\nSupports: A1.1, A1.1.1, A1.2, A1.2.3, CC7.2.2"
        ),
        "frequency": "monthly",
        "owner": "CEO",
        "status": "todo",
        "createdAt": None,
        "updatedAt": None,
        "taskTemplateId": None,
    })
dump("tasks-v2.json", tasks)

# ---------------------------------------------------------------------------
# policies-meta.json — description only (name/frequency/department unchanged)
# ---------------------------------------------------------------------------
# D4 (FileVault wording in the AUP line) and D13 (availability measurement in the SLA line) applied.
POLICY_DESC = {
    "Data Classification and Handling Standard": "Classification tiers and handling rules for the data the platform processes; business contact data is Confidential. Single classification document (the Data Classification Policy is merged into it). Owner: CEO; reviewed annually.",
    "Vulnerability Management Procedure": "How vulnerabilities are found (ECR scan-on-push, Dependabot and code scanning, Trivy in CI, the monthly configuration-check Lambda) and remediated: Critical within 24 hours, dependency CVEs rated Critical within 7 days, High 30 days, Medium 90 days. Owner: CEO; reviewed annually.",
    "Vendor Management Policy": "Assessment, Data Processing Agreements, and annual review of vendors and the two sub-processors (AWS, PropelAuth); 30-day customer notice for sub-processor changes. Owner: CEO; reviewed annually.",
    "Third-Party Integration Security Guidelines": "Merged: integration patterns moved to the API Security and Rate Limiting Standard (Integration security section) and assessment/DPA content to the Vendor Management Policy. [CONFIRM: archive this policy in the platform]",
    "System Monitoring and Logging Procedure": "Monitoring and logging requirements: CloudWatch alarms and 90-day log retention, CloudTrail with 7-year retention, an EventBridge rule on security-relevant CloudTrail events with real-time SNS alerting via the breach-detection Lambda, and the monthly configuration-check record. Owner: CEO; reviewed annually.",
    "Service Level Agreement (SLA) Management Policy": "The 99.9 % platform availability commitment, measured monthly over all minutes from CloudWatch metrics excluding announced maintenance windows, maintenance notice by email, and the monthly availability record in the compliance platform. Owner: CEO; reviewed annually.",
    "Security Awareness Training Program": "Security awareness and ethics training in the compliance platform portal at onboarding and annually for all personnel, with the completion certificate as evidence. Owner: CEO; reviewed annually.",
    "Secure Software Development Lifecycle (SDLC) Standard": "Security requirements through design, development, testing, and deployment of the platform: pull-request workflow on protected main, CI checks (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog), staging-stage validation. Owner: CEO; reviewed annually.",
    "Penetration Testing and Security Assessment Procedure": "Annual third-party penetration test and internal security assessments, with findings remediated per the Vulnerability Management Procedure. Owner: CEO; reviewed annually.",
    "Encryption and Cryptographic Controls Standard": "Encryption at rest with a regional KMS customer-managed key (annual rotation), TLS 1.2+ in transit with ACM certificates, and key management rules. Owner: CEO; reviewed annually.",
    "Data Subject Rights Request Procedure": "Receiving, verifying, and fulfilling GDPR and CCPA data subject requests within 30 days (GDPR) or 45 days (CCPA), with each request recorded in the compliance platform. Owner: CEO; reviewed annually.",
    "Cloud Infrastructure Security Policy": "Security requirements for the AWS environment in us-east-1: VPC isolation, IAM least privilege with MFA, CloudFormation via the Serverless Framework as the only change path, CloudTrail with the EventBridge security-event rule, and the monthly configuration-check Lambda. Owner: CEO; reviewed annually.",
    "API Security and Rate Limiting Standard": "Requirements for the platform's APIs: PropelAuth JWT authentication, TLS 1.2+, rate limiting of 100 requests per minute per key enforced in middleware, audit logging, and integration security. Owner: CEO; reviewed annually.",
    "Acceptable Use Policy": "Rules for use of Deal Intelligence systems and data by all personnel: approved tools, MFA, browser SSO through Google Workspace, FileVault full-disk encryption on personnel devices, prohibited activities. Acknowledged annually in the compliance platform portal. Owner: CEO.",
    "Risk Assessment Procedure": "Identifying, scoring (likelihood × impact, 1–25), treating, and reviewing risks in the compliance platform's risk register: quarterly review, annual assessment. Owner: CEO; reviewed annually.",
    "Privacy Notice and Data Processing Agreement Template": "Template privacy notice and Data Processing Agreement for customers under GDPR and CCPA: processing purposes, sub-processors, data subject rights, breach notification within 48 hours. Owner: CEO; reviewed annually.",
    "Information Security Policy": "Parent policy for the security program: principles, roles (CEO owns every control; Go-to-Market Contractor has no production access), control objectives for Security, Availability, and Confidentiality, exceptions approved by the CEO. Reviewed annually.",
    "Incident Response Procedure": "Detection, triage (P1–P4), containment, and recovery for security incidents; CEO as incident commander; P1 acknowledged within 4 business hours; customer notification within 48 hours; annual tabletop exercise. Owner: CEO; reviewed annually.",
    "Data Retention and Disposal Policy": "Retention periods (active leads 24 months; customer account data for the relationship plus 24 months; CloudWatch Logs 90 days; CloudTrail 7 years) and secure disposal enforced by the retention Lambda. Owner: CEO; reviewed annually.",
    "Data Classification Policy": "Merged into the Data Classification and Handling Standard (decision tree carried as an appendix). [CONFIRM: archive this policy in the platform]",
    "Code of Conduct": "Ethical standards and conduct expectations for all personnel and contractors; acknowledged annually in the compliance platform portal. Owner: CEO; reviewed annually.",
    "Change Management Policy": "How production changes are made: pull request on protected main with required CI status checks, deploy only from a green CI run, rollback via serverless rollback, emergency changes labelled emergency with post-hoc review within 5 business days. Owner: CEO; reviewed annually.",
    "Business Continuity Plan": "Recovery of the platform after a disruption: Multi-AZ DocumentDB, 90-day backups with point-in-time recovery, CloudFormation redeployment, RTO/RPO targets, quarterly backup-restore test; single region (us-east-1) by design. Owner: CEO; reviewed annually.",
    "Access Control and Authentication Policy": "Who may access which systems and how: Google Workspace SSO with MFA for personnel, customer MFA inherited through PropelAuth, RBAC and least privilege, quarterly access reviews, semi-annual privileged-access audit. Owner: CEO; reviewed annually.",
}
pols = load("policies-meta.json")
for p in pols:
    p["description"] = POLICY_DESC[p["name"]]
dump("policies-meta-v2.json", pols)

# ---------------------------------------------------------------------------
# native-records-v2.json — revised payload objects from evidence/native-records.ts
# (only the records whose text changed; same keys and structure)
# ---------------------------------------------------------------------------
NATIVE = {
    "board-meeting-q4-2025": {
        "formType": "board-meeting",
        "payload": {
            "submissionDate": "2025-12-09T22:00:00.000Z",
            "date": "2025-12-09",
            "attendees": "Mo Messidi (Chief Executive Officer); William Wickey (Go-to-Market Contractor). Quorum established.",
            "meetingMinutes": (
                "Q4 2025 quarterly management meeting — Deal Intelligence LLC\n"
                "Source: board-management-meeting-minutes-q4-2025-v1.0.pdf (audited record, finalized 2026-02-02); "
                "historical record, not edited (D17) — text as in data/markdown/board-management-meeting-minutes-q4-2025.md "
                "plus the one-line 'Corrected 2026-10-31' note in scratch/quality-sweep/records-v2/\n\n"
                "<minutes body: docBody('board-management-meeting-minutes-q4-2025') from the v1 markdown, unchanged>"
            ),
            "meetingMinutesApprovedBy": "Mo Messidi (CEO, meeting recorder)",
            "approvedDate": "2026-02-02",
        },
    },
    "performance-evaluation-ceo-2025": {
        "formType": "employee-performance-evaluation",
        "payload": {
            "submissionDate": "2025-12-09T22:00:00.000Z",
            "employeeName": "Mo Messidi (Chief Executive Officer)",
            "manager": "Self-evaluation — CEO; management review recorded in the Q4 2025 management meeting minutes",
            "reviewPeriodTo": "2025-12-09",
            "overallRating": "exceeds-expectations",
            "managerComments": (
                "Annual Performance Evaluation — CEO, period 2025-01-01 to 2025-12-09. Composite rating 4.95/5 (Exceptional).\n\n"
                "<summary: section 8.2 of the v1 evaluation markdown (data/markdown/annual-performance-evaluation-ceo.md), "
                "unchanged — historical record (D17)>\n\n"
                "Areas for improvement: control automation 86 % → 95 % (Q2 2026); 2 remaining SOC 2 controls (Q1–Q2 2026); "
                "penetration testing cadence (Q2 2026). Full record: annual-performance-evaluation-ceo-v1.0.pdf."
            ),
            "managerSignature": "Mo Messidi",
            "managerSignatureDate": "2025-12-09",
        },
    },
    "bcp-full-test-2026-02": {
        "formType": "tabletop-exercise",
        "name": "BCP full test 2026-02-04",  # D18: record name; the "Q1 2025" label is dropped
        "payload": {
            "submissionDate": "2026-02-04T08:25:00.000Z",
            "exerciseDate": "2026-02-04",
            "facilitator": "Mo Messidi (CEO, exercise coordinator)",
            "scenarioType": "custom",
            "scenarioDescription": (
                "BCP full test 2026-02-04. AWS service disruption — full systems recovery from backups using infrastructure as code "
                "(CloudFormation via the Serverless Framework, serverless.yml). Plan: \"AWS Service Disruption Recovery\" "
                "(process: AWS Infrastructure Operations). Type: full recovery test, not a discussion-only tabletop."
            ),
            "attendees": [{"name": "Mo Messidi", "roleTitle": "Chief Executive Officer", "department": "Executive"}],
            "sessionNotes": (
                "Scheduled 2026-03-04; executed early on 2026-02-04 (started 00:24, completed 00:25 PST; 08:24–08:25 UTC). "
                "Recovered all AWS infrastructure from backups via the serverless.yml deployment. Result: system recovered "
                "successfully; plan success rate 100 % (1/1 exercises). Recorded in the compliance platform's business "
                "continuity module (screenshot attached)."
            ),
            "actionItems": [
                {
                    "finding": "Full recovery succeeded; no gaps identified in the restore path.",
                    "improvementAction": "Repeat the backup-restore test quarterly per the Business Continuity Plan and record the RTO and RPO achieved in the compliance platform.",
                    "assignedOwner": "Mo Messidi",
                    "dueDate": "2026-05-04",
                }
            ],
            "evidenceFile": "<uploaded file reference, unchanged>",
        },
    },
    "rbac-matrix": {
        "formType": "rbac-matrix",
        "payload": {
            "submissionDate": "<today, unchanged>",
            "matrixRows": [
                {"system": "PropelAuth (Deal Intelligence platform authentication)", "roleName": "Owner", "permissionsScope": "Full organization administration in the Deal Intelligence platform; manage members and billing", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "PropelAuth (Deal Intelligence platform authentication)", "roleName": "Admin", "permissionsScope": "Organization administration; manage members and settings", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "PropelAuth (Deal Intelligence platform authentication)", "roleName": "Member (default role)", "permissionsScope": "Standard product access to the organization's data; no member or billing management", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "Compliance platform (self-hosted on AWS)", "roleName": "Owner — Mo Messidi (CEO)", "permissionsScope": "Full administration of the compliance program: policies, controls, evidence, people, settings", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "Compliance platform (self-hosted on AWS)", "roleName": "Employee — William Wickey (Go-to-Market Contractor)", "permissionsScope": "Compliance platform portal only: policy acknowledgment and security training", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "GitHub (mo-dealintelligence organization) [CONFIRM: RULEBOOK R8 names the repository dealintelligence/di-backend-api — confirm the organization name]", "roleName": "Organization owner — Mo Messidi (CEO)", "permissionsScope": "All repositories, branch protection, secrets, GitHub Actions; MFA enforced", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                {"system": "Google Workspace (dealintelligence.io)", "roleName": "Super Admin — Mo Messidi (CEO)", "permissionsScope": "Workspace administration, user lifecycle, security settings; MFA enforced", "approvedBy": "Mo Messidi", "lastReviewed": "<today>"},
                "<AWS IAM rows from --inventory rbac-aws-rows.json, unchanged>",
            ],
        },
    },
}
dump("native-records-v2.json", NATIVE)
print("wrote", sorted(p.name for p in OUT.glob("*-v2.json")))
