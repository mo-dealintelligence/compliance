# Policy set v2 — amendment rulebook (2026-10-31)

Source decisions: docs/dealintelligence/09 (§A–H5), 11 (§2–3), 08, 05, and
Mo's calls in the 2026-10-31 session. Every v2 document in this folder is
produced by applying these rules to the v1 markdown in
`data/markdown/` (Feb-2026 export) and `data/nov2025/md/` (audited Nov-2025
package). Where no rule applies, the v1 text is kept verbatim — these are
audited documents; the goal is a correct v2, not a rewrite.

## R0. Method
- Work from the v1 markdown. Keep the structure, section numbering (fix the
  Humadroid "#### 1." repeated-numbering artefacts into proper 1/2/3), the
  tables, and the Deal-Intelligence-specific wording (Lambda, DocumentDB,
  PropelAuth, CloudWatch, the real data elements).
- Frontmatter: bump `version` to the next major (1.0 → 2.0, 1.1 → 2.0),
  `effective_date` left as `"<to be set at publication>"`, `review_date`
  one year after; `doc_type` set honestly (Policy / Standard / Procedure /
  Plan / Template / Program); keep `author`, `source`, `acknowledgment`.
  Add `supersedes: "<v1 version>"`.
- Add a final section "Revision history" with one row per version; the v2
  row summarises the change in one line.
- Write a per-document change note (what was removed / reworded / added and
  the rule number) into `CHANGES.md` in this folder.
- Never invent facts, names, dates, vendors, or numbers. If a fact is
  required and unknown, write `[CONFIRM: …]` and list it in CHANGES.md.

## R1. Scope — SOC 2 Type II = Security, Availability, Confidentiality
- Remove every reference to Processing Integrity (PI1.x) and Privacy
  (P1–P8) *as SOC 2 criteria*. Where a sentence maps a control to "PI1.4" or
  "P6.6", drop that mapping (keep CC/A/C mappings).
- Privacy obligations stay — as **GDPR/CCPA** obligations, not SOC 2
  Privacy. Privacy documents (Privacy Notice & DPA Template, Data Subject
  Rights Request Procedure) keep their purpose; change "SOC 2 Privacy
  criteria" wording to "GDPR and CCPA".
- Replace "all five Trust Services Categories" / lists of five with
  "Security, Availability and Confidentiality".

## R2. Company size and roles — never state headcount
- Never write: solo, sole operator, one-person, single-person, two-person,
  small team, "given the organization's size", "small company", headcount,
  number of employees/people, "all employees" (use "all personnel").
- Exactly two internal roles exist:
  - **Chief Executive Officer (CEO)** — owns every policy and control;
    the only role with production (AWS, GitHub, DocumentDB, PropelAuth
    admin) access; approver of exceptions; incident commander; data
    protection contact.
  - **Go-to-Market Contractor** — no production access; subject to
    onboarding, training, acknowledgments, acceptable use, confidentiality.
  Plus external parties: the external SOC 2 auditor, penetration-test
  vendor, sub-processors.
- Replace: CISO, Security Lead, Security Officer, ISO, System Owner,
  Security Operations, SecOps, Technical Operations Lead, Compliance
  Officer, DevOps (Team), Development Team, Engineering, Procurement, IT
  (Operations), HR, Legal Counsel, DPO / Data Protection Officer, Privacy
  Operations Lead, Change Advisory Board (CAB), Incident Response Team,
  Board of Directors, managers, peer reviewers, on-call personnel,
  SysAdmin → **CEO** (or "the CEO or a delegate approved by the CEO" where
  delegation is plausible). "Board of Directors" → "management" (the
  quarterly management meeting minutes are the governance record).
- Where v1 relies on a second person (peer code review, change approval
  separate from implementer, four-eyes), state the **compensating control**
  instead: pull request with required CI status checks on a protected
  `main` branch, logged self-review in the PR, automated checks (Security
  Hub, CloudTrail), and independent review by the external auditor. Never
  say *why* there is no second person.
- Blank approval tables (CISO/CTO/Legal) → single row: CEO, with
  `[CONFIRM: date]`.

## R3. Claims kept because the environment is being fixed (doc 09 §H1)
Keep these claims as written (tighten numbers to the target value):
- DocumentDB automated backups retained **90 days**, point-in-time recovery
  enabled, daily snapshots.
- DocumentDB **Multi-AZ** (a second instance in another AZ, automatic
  failover).
- **Pull-request workflow** on a protected `main`: PR required, CI status
  checks required (lint, tests, Bandit, Trivy, TruffleHog), no direct
  pushes; deploy only from a green CI run.
- A **staging stage** of the same CloudFormation stack for pre-production
  validation, with no production data (scrubbed or synthetic). Do **not**
  claim a separate AWS account; say "a staging stage" and nothing about
  accounts. (Decision on separate account pending — write
  `[CONFIRM: separate account vs same account]` only in CHANGES.md, not in
  the policy.)
- Secrets rotation: Secrets Manager rotation on the DocumentDB credential;
  API key rotation per calendar.
- CloudTrail logs retained 7 years in S3 (lifecycle to Glacier, Object
  Lock).
- ECR scan-on-push on all repositories.
- Quarterly backup-restore test (automated, recorded in Comp).
- Annual third-party penetration test.

## R4. Claims to remove, with the compensating control to cite (doc 09 §H5)
| Remove | Say instead |
|---|---|
| AWS WAF (on CloudFront or API) | CloudFront with AWS Shield Standard, TLS 1.2+, origin access restricted to the Lambda function URLs, API rate limiting (100 requests/minute) enforced in middleware |
| GuardDuty | AWS Security Hub (Foundational Security Best Practices) + CloudTrail + the breach-detection Lambda that routes Security Hub findings to SNS |
| AWS Config (rules, drift detection, auto-remediation) | CloudFormation (`serverless deploy`) is the only change path and reports drift; Security Hub configuration checks; scheduled Lambda checks (access review, retention enforcement) |
| Inspector, EC2 fleet, EBS, CloudWatch Agent, SSH bastions | workloads run on Lambda and Fargate; the only instance is the NAT instance used as a bastion via SSM Session Manager (no SSH keys, no public services); vulnerability scanning = ECR scan-on-push, GitHub Dependabot and code scanning, Trivy in CI |
| Route 53 multi-region health checks / failover routing | Route 53 for DNS only; CloudWatch alarms on API errors and latency; single region (us-east-1) by design, stated in the BCP |
| Transit Gateway, PrivateLink, VPC peering, cross-region replication, multi-region KMS keys | single VPC, single region; KMS regional customer-managed key with annual rotation |
| Image signing, certificate pinning, mutual TLS | ECR scan-on-push; ACM-managed certificates; TLS 1.2+ |
| CloudWatch Synthetics canaries, status page, customer-portal SLA reports | CloudWatch alarms; monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform; email notice for maintenance |
| Blue-green / canary deployments, load balancers, auto-scaling groups, circuit breakers, read replicas | Lambda versioned deployments with rollback via `serverless rollback`; reserved concurrency; Multi-AZ DocumentDB (R3) |
| Phishing simulations, LMS quizzes / 80 % pass marks, newsletters, security champions, surveys, "training within 5 days / access suspended at +7" | security-awareness training in the compliance platform at onboarding and annually; completion certificate as evidence; contractor acknowledgment |
| Quarterly tabletop + annual full simulation; three-person IRT; 24/7 15-minute response; cyber-insurance; encrypted messaging apps; named playbooks | annual tabletop exercise recorded in the compliance platform; CEO as incident commander; response targets: P1 acknowledged within 4 business hours, Security Hub/SNS paging for critical findings; the BCP full test record |
| Classification metadata fields in the database, resource/classification tags, email subject markings, file-naming conventions | handling rules by tier; data lives in known DocumentDB collections and S3 buckets; CloudFormation tags on resources only |
| API Gateway usage plans / Premium / Admin tiers, WebSockets, DLQs, DAST, 80 % coverage | one rate tier (100 requests/minute per key); CI = Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog |
| Legal-hold registry Lambda, S3 security-log archive architecture, KMS "segment" rotation, Terraform | CloudWatch Logs 90 days; CloudTrail bucket lifecycle + Object Lock (7 years); CloudFormation |
| Automated DSR deletion Lambda, EventBridge deadline monitoring, PropelAuth flags, backup purge automation | manual DSR runbook: verify identity, locate records (DocumentDB by email/domain, PropelAuth user, HubSpot), act, record dated entry in the compliance platform |
| VPN, endpoint protection/EDR suites, MDM | company data accessed only through browser SSO (Google Workspace) and the AWS console/CLI with MFA; device agent of the compliance platform where deployed |
| "86 % control automation", "220 controls", "100+ resources", "quarterly control testing via Lambda" | the compliance platform is the control register (controls, evidence, tasks) |
| Humadroid (any mention) | "the compliance platform" |
| Non-existent documents: Standard Change Catalog, Consent Management Procedure, Infrastructure and Recovery Policy, incident playbooks, runbooks "maintained separately" | delete the reference, or point to the real document (BCP, IR procedure, this document) |

## R5. Numbers — one value each (doc 09 §B/H3)
- Critical vulnerability remediation: **24 hours** for exploited/critical;
  **7 days** for dependency CVEs rated critical; 30 days high; 90 days
  medium; best effort low. State all explicitly where a table exists.
- Breach notification: **48 hours** to affected customers; **72 hours** to
  the supervisory authority where GDPR applies. Delete the 24-hour DPA promise.
- DSR response: **30 days** (GDPR) / **45 days** (CCPA). Delete 10 business
  days and the 72-hour "restriction" row.
- Customer account data retention: **duration of the relationship + 24
  months**, then deletion (matches the Lambda). Replace "7 years after
  closure" for account data. (Financial/contract records 7 years is fine.)
- Incident evidence retention: **7 years**.
- API latency alert: **p95 > 2 seconds**.
- Exception approver: **CEO**.
- MFA: customer MFA inherited from Google Workspace sign-in via PropelAuth
  (Google SSO only); personnel MFA enforced in Google Workspace, GitHub and
  AWS. Never "PropelAuth MFA".
- Availability SLA: 99.9 % platform; do not promise 99.95 % auth (say
  "authentication availability is provided by PropelAuth under its own SLA").
- Backups: 90 days (R3). CloudWatch Logs: 90 days. CloudTrail: 7 years.
- Access reviews: quarterly; privileged-access audit semi-annual.
- Security Hub findings: reviewed **monthly** (recorded); critical findings
  alert in real time via SNS. No daily reviews anywhere ("daily security
  alert review" → monthly review + real-time alerting).
- Change review: PR + CI gate; emergency change = PR labelled `emergency`
  with post-hoc review within 5 business days. No "48-hour CAB".
- Vendor reviews: annual (plus continuous availability record). No
  quarterly vendor SLA reviews.
- Policy review: annual.
- Tabletop: annual. Backup restore test: quarterly.
- Password/session facts: keep v1 unless they conflict with the above.

## R6. Placeholders and leftovers (doc 09 §D)
- `privacy@dealintelligence.ai` → `privacy@dealintelligence.io`.
- Remove export junk ("Document Information Document Assignments …").
- `[Maintained Separately]`, `[YES]/[NO]`, "(Chief Executive Officer)" with
  the missing name, "di-backendapi-prod" → "di-backend-api-prod", "AIpowered"
  → "AI-powered".
- DPA template keeps its `[Customer Name]`-style fields but is typed
  `Template`, `acknowledgment: "None"`, and the title says "Template".
- Version/date footers inside the body must match the frontmatter.
- Code of Conduct: `acknowledgment: "Explicit"`; annual acknowledgment
  recorded in the compliance platform portal.

## R7. Merges (doc 09 §E/H4)
- **Data Classification Policy** → merged into **Data Classification and
  Handling Standard** (keep the Standard's tier table; business-contact
  data = Confidential; fold in the Policy's decision tree as an appendix;
  retention schedule lives only in Data Retention & Disposal and is
  referenced). The Policy becomes `MERGED.md` note only (no v2).
- **Third-Party Integration Security Guidelines** → the webhook/OAuth/
  integration-pattern content goes to **API Security Standard** (new
  section "Integration security"), the assessment/DPA content to **Vendor
  Management**. No v2 of the Guidelines.
- **Vendor Management §11** (Cloud Infrastructure paste) → delete.
  Sub-processor list: AWS, PropelAuth, Google Workspace, GitHub, Resend,
  and the compliance platform's hosting (self-hosted on AWS — state that).
- **Security Awareness Training Program** → one page.

## R8. Wording hygiene
- "the compliance platform" for Comp/Humadroid; "compliance platform
  portal" for acknowledgments/training.
- GitHub repository: `dealintelligence/di-backend-api`; CI = GitHub Actions.
- Region: us-east-1. Infra as code: CloudFormation via Serverless Framework.
- Keep British/American spelling as in v1 (American).
- Bullet lists that v1 collapsed into run-on sentences ("applies to: - All
  …") are restored as real lists.
