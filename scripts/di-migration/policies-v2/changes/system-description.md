# Change note — System Description v1 (Nov 23, 2025 draft) → v2

Source: `data/system-description-draft-nov2025.md` (9,130 words).
Output: `policies-v2/system-description-v2.md` (11,038 words; growth is the added Other-vendors, System-incidents, CSOC table, Management's Assertion and revision-history sections).

Rules applied: `policies-v2/RULEBOOK.md` R0–R8 plus the spec in `docs/dealintelligence/08-SOC2-REPORT-QUALITY-REVIEW.md` ("What to fix before any Type II", item 2).

## Structural changes

| # | Change | Rule |
|---|---|---|
| S1 | Export junk removed: "Soc2 Compliance - SOC 2 System Description" running headers, "Page n of 29 - Generated on …" footers, PROJECT/FRAMEWORK/GENERATED block, "STATUS DRAFT / LAST UPDATED" stamps, DRAFT 100% table of contents, truncated "Linked Items" fragments ("…an...", "+8 more", "+5 more"). | R6 |
| S2 | Frontmatter added (version 2.0, supersedes 1.0, effective/review dates placeholders, doc_type, author, source, categories). | R0 |
| S3 | Title set to "Section 3 — Description of Deal Intelligence LLC's B2B Market Intelligence Platform"; system named throughout as "Deal Intelligence LLC's B2B market intelligence platform" (the name v1 uses) instead of the issued report's template name "Cybersecurity Services System". | spec item 2 |
| S4 | As-of date and period replaced with `[CONFIRM]` placeholders. | spec item 2 |
| S5 | Section 3 retitled "Subservice Organizations and Other Vendors"; subservice table rebuilt from the broken v1 Linked Items; new "Other vendors (not subservice organizations)" subsection (GitHub, Google Workspace, Resend, the compliance platform) with the reason each is not a subservice organization; CRM/Slack note. | spec item 2; R7 (sub-processor list) |
| S6 | New Section 7 "System Incidents" in the auditor's standard form with `[CONFIRM: no significant incidents in the period]`; CSOCs → Section 8, CUECs → Section 9; v1's wrong cross-reference "CUECs detailed in Section 7" corrected to Section 9. | spec item 2 |
| S7 | Section 5 split into labelled subsections (Infrastructure, Software, People, Data, Policies and procedures) matching DC 200 components; v1 prose kept. | R0 (structure kept where sound) |
| S8 | Figure 1 reference added (network diagram "maintained in the compliance platform; reproduced in Figure 1") in Sections 2 and 5; the diagram itself is not drawn. | spec item 2 |
| S9 | CSOC "Linked Items" rebuilt as a table; v1 "+8 more / +5 more" truncations replaced with the criteria named in the v1 prose. | R6 |
| S10 | Policy inventory rebuilt as a clean table from v1's Linked Items; duplicate "Acceptable Use Policy" row (v1.0 and v1.1) collapsed; version/effective-date notes dropped; Third-Party Integration Security Guidelines removed; Incident Response Procedure, Risk Assessment Procedure, Business Continuity Plan and Code of Conduct and Ethics Policy (all named in the v1 prose but absent from the v1 table) added; `[CONFIRM: final v2 document inventory and count]`. Counts "23 / 22 / 19 policies and 3 procedures" removed. | R7, R0 (never invent numbers) |
| S11 | Appendix "Management's Assertion" added in AICPA illustrative form (Type II, S/A/C, carve-out), signatory `[CONFIRM: name, title, date]`, period `[CONFIRM]`. | spec item 2 |
| S12 | Revision history added. | R0 |

## Scope (R1)

| # | v1 | v2 |
|---|---|---|
| R1-1 | §1 "support the Processing Integrity, Confidentiality, and Privacy trust service criteria" | "support the Security, Availability and Confidentiality trust services categories" |
| R1-2 | §2 "five trust service categories: Security (Common Criteria), Availability, Processing Integrity, Confidentiality, and Privacy" | "Security (Common Criteria), Availability, and Confidentiality" |
| R1-3 | §4 "across all Trust Service Criteria" / "security, availability, processing integrity, confidentiality, and privacy domains" | S/A/C only |
| R1-4 | §4 "Processing integrity guarantees ensure…" paragraph | Kept as a processing-accuracy commitment ("The organization commits to complete, accurate, and authorized data processing…") without the PI label |
| R1-5 | §4 "Privacy commitments address lawful collection… in compliance with GDPR, CCPA" | Reworded: "Privacy obligations under GDPR, CCPA… are addressed…; they are not examined as SOC 2 Privacy criteria in this report" |
| R1-6 | §6 "Availability, Processing Integrity, Confidentiality, and Privacy" (3×), "privacy protection" objectives | S/A/C; "privacy protection" dropped from objectives; "Privacy controls implement…" → "Privacy obligations under GDPR and CCPA are implemented…"; "consent management procedures" → "documented lawful bases for processing" (Consent Management Procedure does not exist, R4) |
| R1-7 | §7 CSOC mapping "P3.1, P4.3, C1.2, A1.1, P6.4" | "C1.2 and A1.1"; "supports our privacy objectives" → "supports our GDPR and CCPA obligations" |
| R1-8 | §8 CUEC "Applicable Criteria: C 1.1, C 1.2, PI 1.1, PI 1.2, PI 1.3" | "C 1.1, C 1.2" |
| R1-9 | §8 "confidentiality, integrity, availability, and privacy" | "confidentiality, integrity, and availability" |

## Roles and segregation of duties (R2)

| # | v1 | v2 |
|---|---|---|
| R2-1 | §2 "Deal Intelligence LLC's solo operator functioning remotely with comprehensive responsibility…" | "the Chief Executive Officer (CEO), who holds comprehensive responsibility… and who is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration), and the Go-to-Market Contractor, who has no production access and is subject to onboarding, security awareness training, policy acknowledgments, acceptable use and confidentiality obligations" |
| R2-2 | §2 (new paragraph) | Segregation-of-duties statement in role terms with the four compensating controls: PR/CI gate with logged self-review, CloudTrail/Security Hub logging and alerting, the compliance platform's dated records, external auditor review. No headcount, no reason given. |
| R2-3 | §5 "streamlined single-operator model with the administrator assuming…", "limited human resources availability", "inherent personnel risk", "single-operator model necessitates…" (2 paragraphs) | "People" subsection: two roles (CEO, Go-to-Market Contractor) plus external parties; "the administrator" → "the CEO"; compensating-controls paragraph; "limited human resources"/"personnel risk" language removed |
| R2-4 | §5 "despite the single-operator model" | removed |
| R2-5 | §6 "independent advisory oversight providing quarterly reviews" / "independent validation through advisory oversight" (3×) | "quarterly management meetings, minuted and recorded in the compliance platform" and "independent validation through the external SOC 2 auditor's review" |
| R2-6 | §6 "quarterly self-assessment programs evaluating control execution effectiveness" | "dated records of control execution in the compliance platform" |
| R2-7 | §6 "SNS… alerts… to designated response personnel" | "to the CEO" |
| R2-8 | §6 "appropriate for the organization's size and complexity" | removed |
| R2-9 | §6 incident response: added "with the CEO as incident commander" | R2/R4 |

## Claims aligned to the target environment (R3)

| # | v1 | v2 |
|---|---|---|
| R3-1 | §1, §2, §4, §6 "formal change management procedures through GitHub Actions CI/CD pipeline"; "branch protection rules requiring pull request reviews"; "manual approval gates for production deployments"; "manual production approvals" | PR on protected `main` of `dealintelligence/di-backend-api`, required CI status checks (lint, tests, Bandit, Trivy, TruffleHog; CI tool list Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog), no direct pushes, deploy only from a green CI run; "manual approval gates" removed |
| R3-2 | §2 "staging environment for pre-production validation"; "distinct AWS accounts" for prod/non-prod; "development and testing environments" | "a staging stage of the same CloudFormation stack… no production customer data (scrubbed or synthetic)"; separation "through distinct stack stages, resource naming, and access control policies" — no account claim. `[CONFIRM: separate account vs same account]` is tracked here only, not in the document. |
| R3-3 | §1 "multi-availability zone deployments supporting a 99.9 percent uptime"; §4 "multi-availability zone deployment across AWS regions with automated failover"; §6 "multi availability zone deployments providing geographic redundancy" | "Multi-AZ DocumentDB deployment within the us-east-1 region with automatic failover to a second instance in another Availability Zone"; "geographic redundancy" removed |
| R3-4 | §4 "DocumentDB clusters with automated backups"; "daily automated backups supporting point-in-time recovery" | "automated backups retained for 90 days, daily snapshots, point-in-time recovery enabled" (§2, §4, §5, §6) |
| R3-5 | §2 "Elastic Container Registry with vulnerability scanning enabled"; §5 "automated vulnerability scanning enabled for all pushed images" | "scan-on-push vulnerability scanning enabled on all repositories" |
| R3-6 | (none) | Secrets Manager added to in-scope components; "rotation enabled on the DocumentDB credential and API keys rotated per a documented calendar" (§4) |
| R3-7 | §4 "AWS CloudTrail logging all API operations with 90-day retention" | "seven-year retention"; §2 "CloudTrail logs… retained for seven years in S3 with lifecycle transition to Glacier and Object Lock"; §1 "with logs retained for seven years" |
| R3-8 | §4 "quarterly testing validation of Business Continuity Plan procedures"; §6 "quarterly recovery testing" / "recovery procedures validated quarterly" | "quarterly backup-restore tests and an annual tabletop exercise" |
| R3-9 | §6 (none) | "an annual third-party penetration test" added to periodic assessments |

## Claims removed with the compensating control cited (R4)

| # | v1 | v2 |
|---|---|---|
| R4-1 | §1 "The organization maintains an 86 percent automation rate for control activities" | sentence removed; remainder of paragraph kept |
| R4-2 | §1, §2, §4 "over 100 verified AWS resources", "100+ verified resources", "defines 100+ verified AWS resources" | "All AWS resources are documented through CloudFormation…"; "documented in the compliance platform's asset inventory"; "defines the AWS resources of the production environment" |
| R4-3 | §2 "execution of 220 implemented controls across 224 total examination controls"; "The 86% automation rate for control execution…"; §4 "220 implemented technical and administrative controls achieving an 86% automation rate"; "The 86% control automation rate"; §5 "achieving an 86% automation rate"; §6 "224 total controls with 220 currently implemented, achieving an 86% automation rate"; "high automation rates"; "only 2 controls planned for Q1-Q2 2026" | "the controls recorded in the compliance platform's control register"; "the compliance platform… serves as the control register (controls, evidence, and tasks)"; "Automation of control execution…"; "automation reducing operational burden"; Q1-Q2 2026 sentence removed |
| R4-4 | §1 "Humadriod compliance platform"; §2 "humadriod compliance platform"; §4 "Humadriod compliance platform"; §5 "humadriod compliance platform", "humadriod platform"; §6 "Humadriod compliance platform"; §7 "Humadriod compliance platform" (7 occurrences, all misspelled) | "the compliance platform" (R8) |
| R4-5 | §4 "with automated key rotation every 90 days"; §5 "automated key rotation policies" | "regional AWS KMS customer-managed key with automatic annual key rotation" |
| R4-6 | §4 "ECS-orchestrated Fargate containers automatically scaling based on demand patterns"; §6 "automated scaling through Fargate containers and Lambda reserved concurrency" | "Fargate tasks launched on schedule for batch workloads"; "Lambda reserved concurrency and versioned deployments with rollback" |
| R4-7 | §4 "CloudWatch monitoring detecting service degradation" (as failover trigger) | "CloudWatch alarms on API errors and latency (p95 greater than 2 seconds)" (R5 value) |
| R4-8 | §5 "CloudFront provides global content delivery network services" | "CloudFront, with AWS Shield Standard… origin access is restricted to the Lambda function URLs and TLS 1.2 or higher is enforced" (WAF compensating wording); single VPC / single region (us-east-1) by design stated; NAT instance as bastion via SSM Session Manager described |
| R4-9 | §7 "DDoS protection via AWS Shield" | "AWS Shield Standard" |
| R4-10 | §7 "Multi-availability zone deployments, automated backup capabilities, and geographic distribution of data centers" | "Multi-Availability Zone infrastructure within the us-east-1 region, automated backup capabilities, and the physical distribution of Availability Zones" |
| R4-11 | §2, §5, §6 "pre-commit hooks executing security validation checks" / "pre-commit security hooks preventing introduction of sensitive data" / "pre-commit hooks for security checks" | §2 and §6: replaced by the CI tool list; §5: "TruffleHog secret scanning preventing introduction of sensitive data [CONFIRM: whether pre-commit hooks are also configured locally]" |
| R4-12 | §5 "security monitoring operates continuously" (kept); §4 "CloudWatch provides 24/7 infrastructure monitoring"; §5 table "24/7 CloudWatch monitoring" | "continuous" (24/7 kept only for AWS data-center physical monitoring in §8, which is AWS's claim) |
| R4-13 | §6 "Privacy controls… consent management procedures documenting lawful bases" | "documented lawful bases for processing" (no Consent Management Procedure exists) |
| R4-14 | §6 data subject rights | manual DSR runbook wording added: "verify identity, locate records in DocumentDB, PropelAuth, and the CRM, act, and record a dated entry in the compliance platform" |
| R4-15 | §1 "48-hour breach notification requirements to customers and post-incident retrospectives within 24 hours for emergency changes"; §6 "post-incident retrospectives within 24 hours" | "emergency changes are submitted as pull requests labelled `emergency` and receive post-hoc review within 5 business days" (R5); §6 "post-incident retrospectives incorporating lessons learned" (24-hour figure removed) |
| R4-16 | §5 Data: (none) | "Data lives in known DocumentDB collections and S3 buckets, and handling rules are applied by classification tier" (no classification metadata/tags claim) |
| R4-17 | §5 "storage in encrypted DocumentDB instances with field-level encryption for sensitive attributes"; §6 "field-level encryption for sensitive personal information" | kept inside `[CONFIRM: field-level encryption …]` — not evidenced in docs 05/07/09 |
| R4-18 | §2 "Simple Notification Service for security event alerting" (kept); breach-detection Lambda | "custom Lambda functions for automated breach detection and response that route Security Hub findings to SNS" |

## Numbers (R5)

| # | v1 | v2 |
|---|---|---|
| R5-1 | §1, §2, §5 "24-month data retention period for active leads and customer account data" | "24-month… for active leads, and retains customer account data for the duration of the customer relationship plus 24 months" |
| R5-2 | §1 "multi-factor authentication capabilities"; §4 "maintaining multi-factor authentication capabilities for all user accounts through PropelAuth JWT integration"; §5/§6/§7 "PropelAuth… with multi-factor authentication capabilities"; §7 "bcrypt password hashing with appropriate salt rounds" | customer MFA "inherited from the customer's Google Workspace configuration" via PropelAuth Google SSO (only sign-in method); personnel MFA "enforced in Google Workspace, GitHub, and AWS"; bcrypt password hashing removed (password login is off) |
| R5-3 | §8 CUEC "User entities must enable multi-factor authentication for all administrative accounts and should implement MFA for all user accounts where technically feasible"; "user authentication credentials are properly managed" | "user entities must manage the Google Workspace accounts used to access the platform…"; "must enable multi-factor authentication in Google Workspace for all accounts used to access the platform, as the platform inherits MFA from the user entity's Google Workspace sign-in" |
| R5-4 | §4 "within statutory 30-day response timeframes" | "30 days under GDPR, 45 days under CCPA" |
| R5-5 | §6 "customer security incident notification within 48 hours meeting GDPR and CCPA obligations" | "within 48 hours and notification to the supervisory authority within 72 hours where GDPR applies" |
| R5-6 | §1 "regular vendor security assessments"; §3 "quarterly automated risk assessments executed via Lambda functions"; "real-time monitoring of service availability metrics"; §6 "Vendor risk assessments conducted quarterly"; §7 "quarterly vendor security assessments conducted via our Humadriod compliance platform" | "annual vendor security assessments"; "a continuous availability record derived from service availability metrics"; "annual vendor security assessments recorded in the compliance platform"; §4 "annual review for PropelAuth and AWS" |
| R5-7 | §4 "99.9% system availability… planned maintenance windows communicated 72 hours in advance through established notification channels" | kept; "by email" added; "authentication availability is provided by PropelAuth under its own SLA" added; §7 "ensures continuous authentication availability" → "under PropelAuth's own SLA" |
| R5-8 | §4 "Risk assessment procedures identify and treat potential threats quarterly"; §6 "quarterly change impact assessments" | "at least annually"; "change impact assessments, performed as part of the annual risk assessment and whenever a significant change is introduced" |
| R5-9 | §4 "rate limiting at 100 requests per minute" | "100 requests per minute per API key, enforced in application middleware" |
| R5-10 | §6 monitoring (none) | "Security Hub findings are reviewed monthly…; critical findings alert in real time via SNS"; "semi-annual privileged-access audits"; vulnerability remediation targets (24 h / 7 d / 30 d / 90 d / best effort); "P1 incidents acknowledged within 4 business hours"; "incident evidence retained for seven years" |
| R5-11 | §4 "AES 256 encryption… TLS 1.2 or higher" | kept; "using ACM-managed certificates" added |

## Vendors and sub-processors (R7)

| # | v1 | v2 |
|---|---|---|
| R7-1 | §1 "minimal sub-processor model with two critical service providers"; §2 "minimal sub-processor architecture with only AWS… and PropelAuth"; §3 "minimal sub-processor model, utilizing only two critical vendors"; §4 "minimal sub-processor model currently limited to PropelAuth… and AWS"; §6 "The minimal sub-processor model reduces supply chain risks" | "two subservice organizations" / "carve-out of AWS… and PropelAuth as subservice organizations" / "the sub-processor list published in the Privacy Notice; the subservice organizations for this examination are PropelAuth… and AWS" / "The carve-out of only two subservice organizations reduces supply chain risks" |
| R7-2 | §3 "Third-party services… include cloud infrastructure hosting, authentication and identity management, and compliance management platforms" | adds "source control and continuous integration, workforce identity and email, transactional email delivery" |
| R7-3 | §3 inclusive-method paragraph | kept; sentence added: "No vendor is treated under the inclusive method in this examination." |
| R7-4 | §5 "Slack for operational notifications, and the humadriod platform" | "Slack for operational notifications, Resend for transactional email, and the compliance platform" |
| R7-5 | §5 table "Third-Party Integration Security Guidelines"; "Encryption and Cryptographic Controls Standard" typed POLICY; "Privacy Notice and Data Processing Agreement Template" typed POLICY | Guidelines removed (merged into API Security Standard and Vendor Management); types set honestly (Standard / Template / Procedure / Plan / Program) |

## Wording hygiene (R6/R8)

| # | v1 | v2 |
|---|---|---|
| R8-1 | "Humadriod" ×7 | "the compliance platform" |
| R8-2 | "GitHub repositories" | "`dealintelligence/di-backend-api` GitHub repository"; CI = GitHub Actions |
| R8-3 | "CloudFormation infrastructure-as-code templates" | "CloudFormation… deployed via the Serverless Framework"; "CloudFormation via `serverless deploy` is the only change path for infrastructure and reports drift" |
| R8-4 | "sub processor" (§5) | "sub-processor" |
| R8-5 | "multi availability zone", "point in-time" (§6) | "Multi-AZ", "point-in-time" |
| R8-6 | "trust service criteria/categories" mixed | "trust services categories" / "Trust Services Criteria" per AICPA usage; otherwise v1 wording kept |
| R8-7 | §5 table note "Establishes security principles and controls for AI platform" | "for the platform" |
| R8-8 | §7 "Multi-availability zone deployments" (AWS CSOC) | "Multi-Availability Zone infrastructure" |

## Kept verbatim (R0) — notable items a reviewer may question

- §1 opening two paragraphs (company overview, data elements) except the retention sentence (R5-1).
- §2 data-processing boundary, out-of-boundary list, authentication exclusions.
- §3 vendor-management framework paragraphs (carve-out / inclusive method).
- §4 "99.9% system availability during standard business hours"; "72 hours in advance"; "4-tier data classification"; "cryptographic erasure"; "PII sanitization in system logs".
- §5 Data subsection; §6 "automated fraud detection controls implemented through CloudWatch and Security Hub integration"; "input validation… output encoding… account lockout and suspicious activity quarantine".
- §8 (now §9) CUECs in full except the MFA sentence (R5-3) and the PI criteria mapping (R1-8).
- §7 (now §8) CSOC narrative in full except the MFA/bcrypt, privacy-criteria, Shield, multi-AZ/geographic and quarterly-assessment edits listed above.

## CONFIRM list

1. `[CONFIRM: as-of date]`, `[CONFIRM: period start]`, `[CONFIRM: period end]` — header, Section 7, Management's Assertion (a, b, c).
2. `[CONFIRM: name, title, date]` — Management's Assertion signatory.
3. `[CONFIRM: no significant incidents in the period]` — Section 7.
4. `[CONFIRM: that Resend sends only transactional notifications and that no lead records are included in message bodies]` — Section 3, Other vendors.
5. `[CONFIRM: that the compliance platform deployment holds no customer data and that its hosting is within the in-scope AWS account]` — Section 3, Other vendors.
6. `[CONFIRM: whether any CRM or notification vendor receives customer data in a way that would require listing as a sub-processor]` — Section 3 (HubSpot / Slack).
7. `[CONFIRM: whether pre-commit hooks are also configured locally]` — Section 5, Software.
8. `[CONFIRM: field-level encryption for sensitive attributes, as stated in v1]` — Section 5, Data; and `[CONFIRM: field-level encryption for sensitive personal information]` — Section 6, Control activities. If not implemented, delete both.
9. `[CONFIRM: final v2 document inventory and count at publication]` — Section 5, In-scope documents table.
10. `[CONFIRM: separate account vs same account]` for the staging stage — tracked in this note only (R3); the document makes no account claim.
11. Figure 1 — the network diagram must be exported from the compliance platform and inserted at the Figure 1 placeholder in Section 5 before publication.
