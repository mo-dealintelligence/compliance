# 04 — SOC 2 migration coverage review (read-only)

Reviewed 2026-10-30 against the live instance (`https://api.compliance.dealintelligence.io/v1`, org `org_6ae43948f44032b0bb39e61f`, SOC 2 instance `frm_6ae439498414d87c6cd98f07`). Nothing in Comp was modified.

Sources of truth: `scripts/di-migration/data/Compliance/controls-list.csv` (211 rows: 61 criteria + 150 sub-controls) and `/home/claude/soc2/report.txt` (SOC 2 Type I, as of 2026-03-02).

Scripts: `scripts/di-migration/scratch/coverage-review/fetch.py` (paced API dump) and `analyze.py` (all checks below). Re-run with `COVERAGE_OUT=/tmp/coverage-review python3 -I fetch.py && python3 -I analyze.py`.

## Headline

| # | Check | Result |
|---|-------|--------|
| 1 | Every CSV row exists as a control | PASS — 211/211 matched by identifier prefix, 0 missing, 0 duplicates, 0 DI-style ids in Comp that are not in the CSV |
| 2 | Description verbatim + Implementation Notes | PASS — 211/211 contain the CSV `Description` byte-for-byte and the `Implementation Notes` (appended as `\n\nImplementation: …`) |
| 3 | Requirement mapping | PASS — 211/211 mapped to exactly one SOC 2 requirement; every sub-control maps to its parent criterion; `C1.2`, `C1.2.1`, `C1.2.2` map to custom requirement `creq_6ae4a81e3b47de3200e55872` (identifier `C1.2`) |
| 4 | Evidence files → linked task with attachment | 310/317 file references satisfied. 7 misses, all caused by the 3 known-missing source files (see §4). No other gaps |
| 5 | Policy PDF refs → linked policy | PASS — 147/147 policy references resolve to a linked policy; 0 policies linked to a DI control without a CSV reference |
| 6 | Policies published vs draft | 10 published (the 10 audited documents, all with real content, 731–2,678 words); 42 draft. No unexpected published policies. See §6 for signature and audit-inventory gaps |
| 7 | Vendors / risks / people | PASS — 5 vendors, 6 risks, 2 people as expected. See §7 for caveats |
| 8 | Other | Defects found: 3 `done` tasks with no attachment; 35 Comp template controls still mapped to SOC 2 with 47 `todo` template tasks; platform SOC 2 template has 4 duplicate `P3.2` requirement definitions and no platform `C1.2`; audit report lists 20 policy documents, Comp publishes 10 |

Overall: the control/evidence migration itself is clean. The defects are around (a) tasks marked done without evidence, (b) Comp template content that will dilute the SOC 2 framework view, and (c) policy inventory not matching the audit report.

## 1. Control presence

- Comp has 279 controls: 211 DI controls (name starts with a TSC identifier) + 68 Comp template controls (`controlTemplateId` set).
- All 211 CSV identifiers present; none missing; no duplicate identifiers or duplicate names.
- Criterion rows are named `<id> <full criterion text>` (longest name 116 chars, e.g. `CC6.1 The entity implements logical access security software, infrastructure, and architectures over protected information assets…`). Functional but ugly in list views; cosmetic only.

## 2. Descriptions

- 0 rows where the CSV `Description` is not present verbatim in the control description (checked raw, no normalisation needed).
- 0 rows missing `Implementation Notes`; no CSV row has empty notes.
- Format: `<Description>\n\nImplementation: <Implementation Notes>`. Example: `ctl_6ae4440182262db61359f5bf` (A1.1.1).

## 3. Requirement mapping

- 211/211 DI controls have exactly one `requirementsMapped` entry, all on the SOC 2 instance (no GDPR/CCPA cross-mapping).
- 0 unmapped, 0 mapped to the wrong criterion, 0 multi-mapped.
- `C1.2*` (3 controls) map to the custom requirement `C1.2 Confidential information disposal` (`creq_6ae4a81e3b47de3200e55872`, `kind: custom`). This was necessary because Comp's platform SOC 2 template has **no `C1.2` requirement definition** — see §8.

## 4. Evidence tasks and attachments

- 66 distinct files referenced by the CSV; 317 row→file references in total (170 to screenshots/logs/records, 147 to the 10 policy PDFs).
- 56 custom (non-template) evidence tasks exist, all `status: done`, all linked to at least one DI control; 53 have exactly one attachment; `Supports: …` lists in task descriptions match the actual control links for all 56.
- 7 references are unsatisfied, all for the 3 known-missing files — confirmed these are the only ones:

| CSV row | File | Task (linked, `done`) | Attachments |
|---|---|---|---|
| C1.1.3, CC6.4.2, CC6.7.3, CC6.8.1 | `macos_filevault_status.png` | MacOS FileVault Status | none |
| CC3.2.2, CC9.2.1 | `humadroid_vendor_assessment.png` | Compliance Platform Vendor Assessment | none |
| PI1.3.1 | `models_collections_py_screenshot.png` | Models Collections Py Screenshot | none |

Defects:
- **3 tasks are marked `done` with zero attachments.** An auditor opening them sees a completed evidence task with nothing behind it. They should be `todo`/`in_progress` or get a replacement file.
- The source export does contain `humadroid_vendor_assessment_aws.png` and `humadroid_vendor_assessment_propelauth.png` (under `data/Compliance/evidence/screenshots`), which are not referenced by the CSV and were not uploaded anywhere. The task description for "Compliance Platform Vendor Assessment" says "Humadroid vendor assessment (AWS) confirming SOC 2 Type II compliance" — these two files are almost certainly the intended evidence and should be attached (migration gap, not a source gap).
- Evidence for FileVault and `collections.py` must be recaptured; nothing in the export substitutes for them.

## 5. Policy links from PDF references

- 147/147 references to the 10 policy PDFs resolve to the correctly named linked policy on the control (e.g. `business-continuity-plan-v1.0.pdf` on A1.2.3 → policy "Business Continuity Plan").
- 0 DI controls linked to a template or draft policy; 0 DI controls with a policy link not backed by a CSV reference.
- Every DI control has at least one task or policy linked (0 bare controls).

## 6. Policies

52 policies: 10 published (all custom/imported), 42 draft (34 Comp templates + 8 custom "Deal Intelligence internal policy (docs/*.md, v2023.1)" documents).

Published — all 10 audited documents, content present:

| Policy | Words | Required to sign | Signed by |
|---|---|---|---|
| Information Security Policy | 1,417 | yes | Mo |
| Access Control and Authentication Policy | 1,319 | yes | Mo |
| Change Management Policy | 1,199 | yes | Mo |
| Data Classification Policy | 2,678 | **no** | — |
| Data Retention and Disposal Policy | 2,636 | **no** | — |
| Code of Conduct | 731 | **no** | — |
| Privacy Notice and Data Processing Agreement Template | 1,593 | yes | Mo |
| Incident Response Procedure | 1,771 | yes | Mo |
| Risk Assessment Procedure | 1,499 | yes | Mo |
| Business Continuity Plan | 1,549 | yes | Mo |

Findings:
- No other policy is published. PASS.
- **Code of Conduct is not required-to-sign and has no acknowledgments.** The audit report's CA-01/CA-02 describe a Code of Conduct binding "all personnel, contractors, and business partners" with endorsement; Comp has no record of anyone acknowledging it. Same for Data Classification and Data Retention. Worth confirming against the Humadroid "Explicit" acknowledgment settings the README says drove this flag.
- The contractor (william@dealintelligence.io) has signed none of the 7 required-to-sign policies.
- `approverId` is null on all 10 published policies; `reviewDate` is null on the 3 not-required-to-sign ones (the other 7 are set to 2026-11-13).
- Name drift vs. audit report: report calls it "Data Classification and Handling Standard"; Comp has "Data Classification Policy". Minor.
- **Audit report inventory mismatch.** The report (pp. 16–17) says the control environment has "23 documented policies and procedures, with 22 published" and tables 20 named documents. Comp publishes 10. Of the 20 in the report table:
  - Published in Comp (6): Information Security Policy, Change Management Policy, Access Control and Authentication Policy, Data Classification (Standard→Policy), Data Retention and Disposal Policy, Privacy Notice and DPA Template.
  - Present only as **draft** custom policies whose description says "Satisfies audited inventory item(s): …" (9 items via 8 policies): Vendor Management Policy, Acceptable Use Policy (both v1.0 and v1.1 rows), Encryption and Cryptographic Controls Standard, System Monitoring and Logging Procedure, Vulnerability Management Procedure, Cloud Infrastructure Security Policy, Security Awareness Training Program, Penetration Testing and Security Assessment Procedure, SDLC Standard.
  - **Absent from Comp entirely (4):** API Security and Rate Limiting Standard, Service Level Agreement (SLA) Management Policy, Data Subject Rights Request Procedure, Third-Party Integration Security Guidelines.
  - Conversely, Code of Conduct, Incident Response Procedure, Risk Assessment Procedure and Business Continuity Plan are published in Comp and discussed in the report's prose but are not in the report's document table.
- The 8 custom draft policies are a generic "v2023.1" policy pack (`docs/sdlc.md`, `docs/rar.md`, …) rather than the audited documents; if they are published to close the inventory gap they should be checked for content that contradicts the published audited policies (e.g. two overlapping vulnerability-management and vendor-management policies).

## 7. Vendors, risks, people

Vendors (5, all `status: assessed`): Amazon Web Services (cloud, sub-processor), PropelAuth (SaaS, sub-processor), GitHub, Google Workspace, Resend. Matches the report's "two critical sub-processors (AWS, PropelAuth)". No assignee set on any vendor; no vendor has linked tasks (the AI assessment tasks the API reference says `POST /vendors` triggers are not present).

Risks (6, all `open`, treatment `mitigate`):

| Title | Category | Inherent → residual |
|---|---|---|
| CYBERSECURITY-001 Data Breach / Unauthorized Access **(reconstructed — review)** | technology | possible/severe → unlikely/moderate |
| TECHNOLOGY-001 Service Availability Disruption **(reconstructed — review)** | technology | possible/moderate → unlikely/minor |
| OPERATIONAL_PEOPLE-001 Single Point of Failure - Solo Operator Dependency | people | likely/moderate → possible/minor |
| EXTERNAL_VENDOR-001 PropelAuth Service Disruption | vendor_management | possible/major → unlikely/moderate |
| COMPLIANCE_REGULATORY-001 Compliance Documentation Gaps | regulatory | possible/moderate → unlikely/minor |
| COMPLIANCE-001 Inadequate Incident Response Capacity | regulatory | possible/moderate → unlikely/moderate |

- Two risk titles carry a literal "(reconstructed — review)" marker. That text is visible to an auditor; the risks need to be validated against the Humadroid register screenshot (`humadroid_risk_register.png`) and the marker removed.
- The register has no AWS vendor risk even though the report classifies both AWS and PropelAuth as "critical risk" vendors (only PropelAuth has one).

People (2): Mo Messidi (`mo@dealintelligence.io`, owner) and william (`william@dealintelligence.io`, contractor). Both `isActive`, neither has `jobTitle`, `department` (`none`) or `onboardDate` set; contractor display name is just "william" (the evidence certificate is for "William Wickey").

## 8. Other inconsistencies

1. **Comp template controls still mapped to SOC 2.** 35 of the 68 template controls carry 120 SOC 2 requirement mappings, e.g. `Access Rights` → CC6.1/CC6.2/CC6.3/PI1.4/PI1.5, `Data Privacy` → 21 P-series mappings, `Risk Management` → CC3.1–CC3.4/CC9.1. They sit beside the DI controls in every criterion and are backed by 47 `todo` template tasks (121 task links) and 34 draft template policies, so the SOC 2 framework view will read as largely incomplete even though the audited DI evidence is 100% linked. The README says these stay deliberately for Type II recurring evidence; if so, the template tasks need owners/frequencies and the template policies need to be either published or archived, otherwise this is noise an auditor will have to be talked through. (`scripts/di-migration/import/cleanup-templates.ts` exists but was evidently not run against the SOC 2 mappings.)
2. **Platform SOC 2 template defects (Comp seed data, not the migration):** the requirement definitions for the SOC 2 framework contain `P3.2` four times (`frk_rq_683f834daeb15e457c90c0ee`, `…8345a76125f5c3a71d5c`, `…833cb9cd7f024ff9535f`, `…83098dfd2e4ed385afd4`, identical names) and no `C1.2` at all; 64 definitions for 61 real criteria. The template control `Data Privacy` is therefore mapped to P3.2 four times. DI's own controls are unaffected (they map to the first P3.2 id and to the custom C1.2), but the duplicates will show up as empty rows in the framework/requirement view.
3. **GDPR and CCPA framework instances are enabled** (`frm_6ae43949ee87bc430f1d286b`, `frm_6ae439494232c9924d7fcccd`) with their template controls (e.g. `CCPA-Compliant Privacy Policy`, `Lawful Basis Register`, `Minor Consent Management`), tasks and draft policies. They are out of scope of the audited SOC 2 program and add to the unfinished-looking template inventory.
4. **Control count vs. report.** The audit report states "224 total controls with 220 currently implemented" (p. 17); the CSV/Comp has 211 DI controls. The difference is in the Humadroid export, not the migration, but the numbers will not reconcile if someone compares.
5. `evidenceSubmissions` on the SOC 2 instance is empty and `lastReviewDate`/`nextReviewDate` are null on all 211 DI controls — no review cadence is set for Type II.
6. Task descriptions concatenate every CSV "Evidence files descriptions" fragment for a file across rows (e.g. "IAM Roles Console PropelAuth security settings IAM Roles. IAM roles enforcing access"), including unrelated text (`aws_iam_roles.png` task mentions PropelAuth). Cosmetic, but misleading if read literally.

## Recommended fixes (in priority order)

1. Attach `humadroid_vendor_assessment_aws.png` + `humadroid_vendor_assessment_propelauth.png` to "Compliance Platform Vendor Assessment"; set the FileVault and Models Collections tasks back to `todo` until recaptured.
2. Remove "(reconstructed — review)" from two risk titles after validating them; consider an AWS vendor risk.
3. Decide on Code of Conduct / Data Classification / Data Retention acknowledgment; get the contractor to acknowledge required policies.
4. Either unmap/archive the 35 template controls (and their 47 tasks, 34 draft policies) from SOC 2, or assign and schedule them for Type II.
5. Close the policy inventory gap vs. the audit report: publish (after review) the 8 draft custom policies, and source or write the 4 missing documents.
6. Disable GDPR/CCPA instances unless they are intentionally in scope.
