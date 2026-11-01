# 09 — Policy set quality check (2026-10-31)

Scope: the 24 published policies in Comp (10 from the Drive export dated
Feb 2026, 14 from the audited Nov‑2025 package). Each was read in full
against one rubric (purpose fit, Deal‑Intelligence specificity, roles that
don't exist here, every numeric commitment, claims that must be true in
production, placeholders, contradictions); numbers were then cross‑checked
across documents and against the live AWS account and repo.

Per‑policy rubric output: `scripts/di-migration/scratch/policy-qc/` (3 review
files). This document is the synthesis.

## Headline

The set is **complete and recognisably yours** (every document names Lambda,
DocumentDB, PropelAuth, CloudWatch, the real data elements), and it passed a
Type I as written. But it was written **for a 20‑person company with a
staging environment and a security team**, and it **asserts controls your
AWS account and repo contradict**. In a Type II the auditor tests what the
policy says. Right now ~25 % of the stated controls would fail or have no
evidence. The fix is mostly deletion: cut what you do not do, collapse roles
to "CEO (sole operator)" and "contractor", and align six numbers.

Something I introduced and have now fixed: my PDF→Comp converter replaced
"Humadroid" with "the compliance platform" and produced "the the compliance
platform compliance platform" in 14 documents. Corrected and re‑published
today (content only; names, status and signatures untouched). Also filled
two `[Original Date]/[Current Date]` placeholders left by Humadroid in the
Data Retention and Data Classification version tables (v1.0 → Nov 13 2025,
v2.0 → Feb 2 2026 — confirm the v1.0 date for Data Classification Policy).
The remaining formatting problem — bullet lists collapsed into run‑on
sentences ("This policy applies to: - All third‑party vendors … - All
employees …") — is how Humadroid rendered the PDFs that the auditor
accepted; it is in the originals, not the conversion.

## A. Claims that are false today (fix the environment or the text)

| Claim | Stated in | Reality |
|---|---|---|
| Branch protection, PR reviews before merge, "manual approval separate from code commit" | Change Mgmt, SDLC, InfoSec, AUP, Pentest, Vuln Mgmt, Access Control | Direct pushes to `main`, no protection, CI red, deploy is manual-only |
| Staging environment / "validate in staging first" / separate non‑prod account / dev‑staging‑prod KMS keys | Change Mgmt, SDLC, InfoSec, Cloud Infra, Encryption, Vuln Mgmt, AUP, Access Control | None evidenced; one AWS account |
| Multi‑AZ DocumentDB with automatic failover, read replicas | InfoSec, Cloud Infra, BCP, SLA, Risk Assessment | `MultiAZ=false` |
| Backups 90‑day retention | 7 documents | 35 days configured |
| RPO 30 min–1 h for API/auth/DB | BCP | Daily backup at 02:00 UTC unless PITR is on (RPO up to 24 h) |
| WAF on CloudFront, GuardDuty, AWS Config drift detection + auto‑remediation, Inspector on EC2, EBS/EC2, Route 53 multi‑region health checks, Transit Gateway, PrivateLink, image signing, certificate pinning, VPN, endpoint protection, encrypted messaging, cyber‑insurance carrier, status page, Synthetics canaries every 5 min, customer portal SLA reports | Cloud Infra, Monitoring, Encryption, IR, SLA, AUP, Vuln Mgmt, Third‑Party | Not in the account / not evidenced |
| "Quarterly control testing via Lambda", "86 % control automation", "220 controls", "100+ resources" | InfoSec, Risk, Retention, Training, Vendor | Humadroid dashboard figures; no source now |
| Phishing simulations, LMS with quizzes (80 % pass), monthly newsletter, security champions, quarterly surveys | Security Awareness Training Program | ~75 % generic; none exists. Comp's training module + certificate is the real control |
| "Quarterly tabletop exercises" + "annual full simulation" | Incident Response | One BCP full test exists (Feb 2026); no tabletop record |
| Database classification metadata fields, resource/classification tags, email subject marking | Data Classification Standard | Not implemented |
| SAST + DAST in CI, 80 % unit‑test coverage, API Gateway usage plans per tier, WebSockets, DLQs | API Security Standard, SDLC | CI failing; single rate tier |
| Secrets Manager automatic rotation, quarterly DB credential rotation, semi‑annual rotation audits | Encryption, Third‑Party | No rotation history to show |
| CloudTrail retained 7 years immutable, security logs archived to S3 7 years | Retention, DSR | CloudTrail bucket exists; lifecycle/lock unverified; CloudWatch = 90 d |

## B. Numbers that disagree between documents

| Topic | Values found | Pick one |
|---|---|---|
| Critical vulnerability remediation | 24 h (Pentest, Vuln Mgmt, Third‑Party) · 48 h (SDLC patches) · 7 days (SDLC dependencies) | 24 h for exploited/critical, 7 d for dependency CVEs — state both explicitly in SDLC |
| Breach notification | 48 h to customers (8 docs) · 24 h to controller (DPA §4.1.6) · 72 h to individuals (DPA §3.1.8) · 72 h to authority (IR, GDPR) | 48 h customers; 72 h supervisory authority; drop the 24 h DPA promise |
| DSR assistance / response | 10 business days (DPA) · 30 days GDPR / 45 CCPA (DSR procedure) · 72 h "restriction" (DSR table, no legal basis) | 30/45 days; delete 10 bd and 72 h |
| Customer account data retention | relationship + 24 months (Classification) · 7 years after closure (Retention, DPA) | one value |
| Incident evidence retention | 2 years (IR) · 7 years (Retention, Classification) | 7 years |
| API latency alert | > 2 s p95 (SLA, Monitoring) · > 5 s p95 (Third‑Party) | 2 s |
| Exception approver | CEO (Pentest, SDLC, SLA, Third‑Party) · CISO (Monitoring, Vendor, Vuln Mgmt, Encryption) | CEO |
| Access Control policy version | frontmatter 1.0 · footer 2.0 · "Last review: Current" | 1.0, real dates |
| Auth SLA | 99.95 % promised = PropelAuth's own SLA | leave headroom or exclude |
| MFA | "required" (Classification §2.1.4, Access Control) · "available"/"when configured" (same docs, AUP) · PropelAuth is Google‑SSO‑only, 2FA enforcement off | Say: customer MFA inherited from Google; staff MFA enforced in Google Workspace/GitHub/AWS |

## C. Roles that do not exist

CISO, Security Lead, System Owner, Security Operations, Technical Operations
Lead, Compliance Officer, DevOps Team, Development Team, Procurement, IT
Operations, HR, Legal Counsel, Data Protection Officer, Privacy Operations
Lead, Change Advisory Board (named as "(Chief Executive Officer)" with the name
missing), Board of Directors, "all employees", "managers", "peer reviewers",
"on‑call personnel". Vendor Management has a blank approval table for CISO /
CTO / Legal Counsel. Several documents (Pentest §2, BCP) admit "solo
operation" in one paragraph and staff three roles in the next.

Replace with two: **Chief Executive Officer (sole operator; owns every
control)** and **Contractor (GTM; no production access)**, plus the auditor.
Where a policy needs a second pair of eyes (code review, change approval,
conflict‑of‑interest reporting), say what the compensating control is: CI
gate, automated checks, logged self‑review, external auditor.

## D. Placeholders and template leftovers (verbatim, still in the published text)

- DPA template: `[Customer Name]`, `[Date]`, `[Company Address]`, `Data Protection Officer: [Name]/[Email Address]`, `[Specific data types affected]`, `[Incident ID]` — acceptable in a template, but it is published as a signed "Policy" with Explicit acknowledgment; retype it as a template, no signature.
- Data Retention: `[YES]/[NO]` checkboxes in the legal‑hold form; "Terraform"; "Infrastructure and Recovery Policy" (does not exist).
- BCP: `[Maintained Separately]` for the coordinator's phone/email; Appendix B runbooks "maintained separately" (not in the set).
- Change Mgmt: "consisting of (Chief Executive Officer)"; "Standard Change Catalog" (does not exist); "di-backendapi-prod".
- Incident Response: six named playbooks that do not exist.
- Data Classification Policy: "Consent Management Procedure" (does not exist); author "Information Security"; blank owner/approver table.
- SLA: trailing export junk "Document Information Document Assignments (1) mo@dealintelligence.io Pending".
- DSR procedure: **privacy@dealintelligence.ai** (every other document says .io) — a customer‑facing error an auditor will test by sending a request.
- Code of Conduct: frontmatter acknowledgment "None" while the body requires annual signed acknowledgment; "AIpowered"; effective date N/A.
- Numbering "#### 1." repeated for every sub‑step in BCP, Change Mgmt, IR, Risk, DSR (Humadroid export).
- Frontmatter `doc_type: Policy` on 8 documents that are standards, procedures or a template.

## E. Structural overlaps

- **Data Classification Policy (Feb 2026) vs Data Classification and Handling Standard (Nov 2025)** — two documents, two tier tables, and they disagree on where business‑contact data sits (Confidential vs Restricted) and on account‑data retention. Keep one. Since the auditor saw the Standard, keep the Standard and fold the Policy's decision tree/appendices into it.
- **Third‑Party Integration Security Guidelines** calls itself "this policy", has no owner, and overlaps Vendor Management (assessment/DPA) and API Security (webhook/OAuth patterns). Merge into those two.
- **Vendor Management §11** is a paste of Cloud Infrastructure Security; delete.
- **Security Awareness Training Program** is an enterprise LMS program; reduce to one page (onboarding within N days, annual refresher, contractor acknowledgment, evidence = Comp training certificate).
- Retention schedule appears in three places (Retention, Classification ×2) with differences; keep it only in Retention and reference it.

## F. Per‑policy verdicts

| Policy | Verdict | Main reason |
|---|---|---|
| Information Security Policy | KEEP, fix | cornerstone; remove 5 false claims (branch protection, staging, PR reviews, multi‑AZ, 90‑day backups), map roles |
| Access Control & Authentication | FIX | version/date footer, SCPs/Session Manager/EC2/non‑prod claims, MFA wording, ISO/SysAdmin → CEO |
| Change Management | FIX heavily | CAB/48 h review by the implementer; branch protection/staging/smoke tests false; rewrite as solo‑operator change standard with CI gate |
| SDLC Standard | FIX heavily | highest‑risk: every §5.2.2/§5.4.1 control is auditable and false today; reconcile 24 h/48 h/7 d |
| Cloud Infrastructure Security | FIX heavily | most testable against the account: Multi‑AZ, WAF, GuardDuty, Config, EC2/EBS, image signing, staging; backups 35 d |
| Business Continuity Plan | FIX | RTO/RPO impossible with daily backups + single AZ; read replicas/LB/cross‑region/status page; placeholders; the quarterly restore test is real — keep it |
| Incident Response Procedure | FIX | 3‑person IRT → CEO; evidence retention 2 y vs 7 y; WAF/playbooks/insurance; keep severity matrix |
| Risk Assessment Procedure | FIX | roles; "86 %"/Lambda‑tested controls; Multi‑AZ row; numbering; register now lives in Comp |
| Vulnerability Management | KEEP, fix | sound severity/SLA table; CISO/DevOps → CEO; EC2/Inspector/WAF/staging |
| Penetration Testing Procedure | FIX | roles; budget/KPI/maturity sections; PR reviews; needs a real annual vendor + report |
| System Monitoring & Logging | KEEP, fix | retention table matches reality; strip EC2 agent/Route 53/cross‑account/auto‑scaling/Synthetics; CISO → CEO |
| Encryption Standard | FIX | cut to KMS/ACM/PropelAuth facts; AZ‑vs‑region error; staging keys; rotation audits; CISO → CEO |
| API Security Standard | FIX | one rate tier; no usage plans/WebSockets/DAST/80 % coverage; "SQL injection… DocumentDB" |
| Vendor Management | FIX | blank CISO/CTO/Legal approval table; §11 duplicate; sub‑processor list honest (add GitHub, Google Workspace, Comp); "on‑site audits of AWS" |
| Third‑Party Integration Guidelines | MERGE | into API Security + Vendor Management |
| Data Classification Standard | KEEP (as the one classification doc), fix | Confidential/Restricted overlap for contact data; drop tagging/labeling claims |
| Data Classification Policy | MERGE into the Standard | duplicate, blank approval table |
| Data Retention & Disposal | FIX | 35‑day backups; strip legal‑hold Lambda/S3 archive architecture unless real; Terraform; align account‑data retention |
| Data Subject Rights Procedure | FIX | **.ai email**; DPO/Privacy Ops → CEO; automation claims → actual manual steps; controller vs processor |
| Privacy Notice & DPA Template | FIX | controller/processor role; 24/48/72 h; 10 bd vs 30 d; "annual Type II report" promise; retype as template |
| Acceptable Use Policy | FIX | branch protection/staging/VPN/endpoint protection; direct DB access prohibited while you do it |
| SLA Management Policy | FIX | Multi‑AZ; export junk footer; canaries/portal reports; 15‑min critical response implies 24/7 |
| Security Awareness Training Program | REWRITE to one page | enterprise LMS program; keep what Comp's training module evidences |
| Code of Conduct | KEEP, light fix | acknowledgment metadata; roles; needs William's signed acknowledgment |

## G. Suggested order

1. Fix the .ai email and the four number conflicts that are customer‑facing (DPA/IR/DSR clocks, retention) — these are contractual.
2. Decide environment vs text for the Section A rows: cheapest is to make branch protection + CI gate true (one afternoon) and delete the rest (staging, multi‑AZ, WAF, GuardDuty, Synthetics, LMS). Set backups to 90 d or rewrite to 35 d.
3. Role collapse + placeholder clean‑up across all 24 (mechanical; I can script the role/term replacements and give you a redline per policy to approve).
4. Merges (Classification, Third‑Party, Vendor §11, Training).
5. Re‑publish as v2.0 in Comp with a changelog line per policy, then re‑acknowledge — the auditor will see a dated review, which is itself CC1/CC5 evidence.
