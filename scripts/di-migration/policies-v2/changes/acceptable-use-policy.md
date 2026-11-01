# Change note — Acceptable Use Policy v1.1 → v2.0

- R0: frontmatter — version 1.1 → 2.0, `supersedes: "1.1"`, `doc_type` Policy kept, effective/review dates set to placeholders, `finalized_at` export field dropped; added §16 Revision history (1.0 and 1.1 rows: 1.0 date/summary not in the v1 export — see CONFIRM).
- R2: §2 "All personnel … including employees, contractors, and third-party service providers" → "including the Chief Executive Officer, the Go-to-Market Contractor, and third-party service providers".
- R8: §2 restored scope bullets from run-on text; "CI/CD pipelines" → "GitHub Actions CI/CD pipelines"; restored run-on bullets in §4.2, §4.3, §5.1, §5.2, §5.3, §8.1, §8.2, §9.1, §10.1, §11.2, §13, §15; removed `<u>` underline artefacts.
- R2: §4 Executive Leadership, Security Lead and System Owner merged into §4.2 Chief Executive Officer (union of the three lists); added §4.3 Go-to-Market Contractor (user under §4.1, no production access).
- R5: §5.1 "(PropelAuth JWT with MFA when configured)" → Google Workspace sign-in with MFA enforced; MFA enforced in GitHub and AWS; customer access authenticated by PropelAuth through Google sign-in.
- Brief: §6.1 "Accessing production databases directly (all access must be through approved APIs)" → direct production database access limited to the CEO via SSM Session Manager and logged; all other access through approved APIs.
- R4: §6.4 "unauthorized network connections or VPN tunnels" → "or tunnels".
- R4: §7.1 "Install and maintain endpoint protection software" → "Run the device agent of the compliance platform where deployed".
- R4: §7.2 removed "Use VPN when accessing systems from public networks" and "Not use public Wi-Fi for accessing sensitive data without VPN" → "Access company data only through browser SSO (Google Workspace) and the AWS console/CLI with MFA".
- R7: §8.2 sub-processor list "(PropelAuth and AWS)" → AWS, PropelAuth, Google Workspace, GitHub, Resend, and the compliance platform (self-hosted on AWS); "Follow the Third-Party Integration Security Guidelines" → Vendor Management Policy and the Integration security section of the API Security and Rate Limiting Standard; Guidelines removed from §15.
- R2/R3: §9.1 "Developers shall" → "Personnel with repository access shall"; "branch protection rules and PR review requirements" → pull request requirements (required CI status checks on protected `main`).
- R3: §9.2 "staging" → "the staging stage".
- R3: §10.2 "Continuous vulnerability scanning in ECR" → "(scan-on-push)" added.
- R2: §11.1 "Direct notification to Security Lead" and "Escalation to executive leadership for serious violations" → single bullet "Direct notification to the CEO".
- R5: §12.1 "Executive approval for high-risk exceptions" → "CEO approval".
- R8: §13 "Acknowledge understanding of this policy annually" → "… in the compliance platform portal".
- Kept verbatim (no rule applies): §1, §3 definitions, §4.1, §5.2, §5.3, §6.2, §6.3, §7.3, §8.1, §10.1 (CloudWatch 90 days matches R5), §11.2, §11.3 (24-hour investigation), §12.2, §14 (CC-only mapping, GDPR/CCPA references), §15 structure.

## CONFIRM

- §16 Revision history: v1 export only shows version 1.1 dated November 13, 2025; the 1.0 row's date and the 1.1 summary ("Audited release") are placeholders — confirm or delete the 1.0 row.
- §3 "Authorized User … through PropelAuth authentication" kept from v1; internal personnel authenticate through Google Workspace, so confirm whether this definition should mention both.
- §7.1 "device agent of the compliance platform where deployed" — confirm the Comp device agent is actually deployed on the CEO's and the Contractor's machines; if not, drop the bullet.
- §11.1 "Anonymous reporting channels if available" kept from v1 — confirm whether any such channel exists; delete if not.
- §11.3 "Investigated within 24 hours of report" kept from v1 — not in R5; confirm this is consistent with the Incident Response Procedure's P1 4-business-hour acknowledgment.
- §12.1 "maximum 90 days" exception window kept from v1 — confirm it matches the Information Security Policy exception clause.
- R3 staging: separate account vs same account (not written into the policy).

## Quality sweep (2026-10-31)

- Q1 voice: §1 rewritten to plain declarative (removed "establishes the requirements… to ensure", "enforces behavioral controls", "operationalizes", "clear boundaries"); "shall" → "must" in all 8 obligation lists; "strictly prohibited" → "prohibited"; "encompasses" → "covers"; "Ensure home network routers use…" → "Use WPA2/WPA3 encryption on home network routers"; "Ensure customer-controlled integrations… follow" → "Apply the security requirements to customer-controlled integrations"; "Report new service requirements through proper channels" → "Raise new service requirements with the CEO" (names the owner; same obligation).
- Q1 parallel grammar: §4.2 CEO responsibilities and §4.3 contractor bullets put in third-person present ("Approves", "Complies", "Holds") to match the other policies; §7 lead-in ("Given Deal Intelligence's remote work environment, users shall:" followed by subheadings) replaced with two sentences; §8.2 and §9.2 given a lead-in ("Users must:" / "Personnel must:") so their bullets read as obligations like the neighbouring lists.
- Q2 names/roles: "Chief Executive Officer (CEO)" on first use (§2) and in the §4.2 heading; definitions in sentence case.
- Q2 headings and lists: all headings to sentence case; removed blank lines between bullets (34 lists); nested list indentation normalised; §15 Related Documents' four unnumbered `###` groupings flattened into one list (same 18 documents, all in the set).
- Q3 structure: §14 "Compliance Requirements" (SOC 2 criteria, GDPR Art. 32, CCPA §1798.150) merged into §1 — the full criteria list is kept there; "Industry best practices for acceptable use controls" dropped as content-free; Related documents → §14, Revision history → §15.
- No commitment, number, role, scope item or control changed.

### CONFIRM (new)

- §3 "Authorized user" is defined as an individual authenticated "through PropelAuth" — PropelAuth authenticates customers, while personnel sign in through Google Workspace (§5.1). Confirm whether the definition should read "through Google Workspace sign-in or PropelAuth".
- §11.1 "Anonymous reporting channels if available" — confirm whether an anonymous channel exists; if not, the bullet should be removed rather than hedged.

## Decisions applied (2026-10-31)

- D4: §7.1 device encryption stated as FileVault full-disk encryption (macOS); compliance-platform device-agent bullet dropped (revision-history summary updated to match)
- D5: §11.1 anonymous reporting channel removed; reporting is direct notification to the CEO by email
- D15: §8.2 sub-processors reduced to AWS and PropelAuth; Google Workspace, GitHub, Resend, HubSpot and the compliance platform listed as approved vendors that do not process customer data
- D22: author set to Mo Messidi
- D25: cut §11.3 quarterly compliance reports, §12.2 quarterly exception review

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §4 CEO duty "CloudWatch logs and Security Hub findings" → "CloudWatch logs, the monthly configuration-check record, and CloudTrail event alerts"; §10.1 monitoring list: "Security Hub findings and alerts" and the generic "Automated compliance checks via Lambda functions" bullets replaced by the CloudTrail-EventBridge real-time alert and the monthly configuration-check Lambda record.
- D11b, D13b, D14: no insurance, availability-measurement or controller/processor text in this document; nothing to apply.

- D1 revised (Mo, 2026-10-31): staging moves to a **separate AWS account** in the same Organization; wording updated from "staging stage of the same stack" to a staging environment/account.
