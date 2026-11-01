# Data Retention and Disposal Policy — v1.0 → v2.0 change note

- R0: frontmatter — `version` 1.0 → 2.0, `supersedes: "1.0"`, `effective_date`/`review_date` "N/A" → publication placeholders, `finalized_at` dropped; "Revision history" section added at the end (replaces the v1 §10.2 Version Control table; §10.3/§10.4 renumbered §10.2/§10.3).
- R6: v1 body version table listed a "2.0 — February 2, 2026" row while the frontmatter said 1.0; the Revision history now records 1.0 (November 13, 2025, finalized in the compliance platform February 2, 2026) and 2.0 (this revision) so body and frontmatter agree.
- R0/R8: restored collapsed bullets throughout (§1.1 commitments, §1.2 scope items, §1.4 related documents, §2.2.1–§2.2.3 justification lists, §2.3 step 5 "resumes", §3.2.3/§3.2.6 stray "- **Process**" bullets, §7.3 report items, §9.1 training items); the split §2.1 table and the split Appendix C table each merged into one table; §4.1 broken table-plus-code diagram and Appendix A "picture text" flowchart re-rendered as single code blocks with the same content.
- R6: Appendix A `[YES]`/`[NO]` export junk → plain YES / NO branch labels in the flowchart.
- R1: §1.1 "across all applicable Trust Services Categories (Security, Availability, Processing Integrity, Confidentiality, and Privacy)" → "(Security, Availability, and Confidentiality)"; §2.1 "and Privacy (P4.1, P4.2, P4.3)" → "and with the storage-limitation obligations of GDPR and CCPA"; Market Intelligence Data basis "SOC 2 PI1.1" dropped; Appendix C "SOC 2 P4.2" row removed.
- R7: §2.1 — added the sentence that this section is the single retention schedule and other documents (including the Data Classification and Handling Standard) reference it.
- R5: §2.1 User Account Data "7 years after account closure / Financial record requirements / 26 U.S.C. § 6001" → "Duration of the customer relationship + 24 months, then deletion / Customer service, data minimization / GDPR Art. 5(1)(e), 6(1)(b)"; the 7-year IRS basis moved to a new "Financial and Contract Records — 7 years — 26 U.S.C. § 6001" row (v1 §2.2.2 already listed Financial Records under 7-year retention); §2.2.1 now names customer account data (after the relationship ends) among the 24-month items.
- R4/R5: §2.1 Application Logs (CloudWatch) "90 days (operational) / 7 years (security)" → "90 days"; API Transaction Logs "90 days (operational) / 7 years (audit)" → "90 days (CloudWatch); the CloudTrail audit trail is retained 7 years"; §3.2.2 step 3 "Security-relevant logs archived to S3 with lifecycle policies before purge" removed; Appendix B CloudWatch "90 days (operational)" → "90 days".
- R3/R4: §3.2.3 CloudTrail method "S3 lifecycle policies with secure deletion" → "with Object Lock"; step 1 adds Object Lock; step 4 "KMS key rotation upon deletion" removed; Appendix B CloudTrail configuration → "S3 lifecycle policy (Glacier after 1 year) with Object Lock".
- R4: §3.2.1 DocumentDB method "Record-level deletion with cryptographic key rotation" → "Record-level deletion"; step 3 "Rotate KMS encryption keys for affected data segments" removed.
- R4: §2.2.3 "refer to the Business Continuity Plan and Infrastructure and Recovery Policy" → "refer to the Business Continuity Plan" (document does not exist).
- R4: §4.1 "(supporting the organization's 86% control automation rate)" removed.
- R4: legal-hold registry Lambda removed — §2.3 step 3 "Automated disposal processes are suspended for in-scope data" → "The CEO pauses the retention enforcement Lambda function for in-scope data"; §4.3 step 2 "Validates no active legal holds apply" → "Is paused by the CEO for in-scope data while a legal hold recorded in the compliance platform is active"; §4.4 "Query legal hold registry before any deletion" → "The CEO checks the legal holds recorded in the compliance platform before resuming any paused deletion"; §7.2.3 "Legal hold registry" → "Legal hold records in the compliance platform".
- R4: §7.2.3 "Retention policy configurations (CloudFormation, Terraform)" → "(CloudFormation)".
- R5: §4.2 — added row "Customer Account Data Expiration — Daily — EventBridge — Delete account data >24 months after the relationship ends" so the automated-process table matches the account-data retention value (R5 says the value matches the Lambda).
- R5: §5.1 step 4 "within 30 days" → "within 30 days (GDPR) or 45 days (CCPA)".
- R7: §5.3 "sub-processors (PropelAuth, AWS)" → "sub-processors listed in the Vendor Management Policy" (the two existing bullets kept).
- R2: §6.1 Owner/Founder, Technical Operations and Compliance Function rows merged into one "Chief Executive Officer (CEO)" row carrying all three responsibility sets; §6.2 Policy Owner and Technical Implementation → CEO; Audit Responsibility adds "independent review by the external SOC 2 auditor"; §4.4 "Authorized personnel can pause automated deletion" → "The CEO can pause"; §10.2 Approval "Owner/Founder" → "Chief Executive Officer"; §10.3 Exceptions "Approval from the Owner/Founder" → "Approval from the CEO".
- R5: §7.1 "Daily Lambda audit" → "Daily automated Lambda check" (automated check, not a daily human review).
- R8: §8.2 "Incident Reporting system in the compliance platform with customizable forms" → "Incident Reporting system in the compliance platform"; §5.1 step 7 and §2.3 "the organization's compliance platform" → "the compliance platform".
- R4/R2: §9.1 "within 30 days of access" → "at onboarding"; "Role-Specific Training: Technical staff receive detailed training on automated systems" → "The CEO, as operator of the automated retention systems, maintains detailed knowledge of those systems"; training delivered "through the Security Awareness Training Program in the compliance platform portal".
- Kept verbatim (no rule applies): §3.1 disposal standards table, §3.2.4–§3.2.6, §3.3 cryptographic erasure, §4.2 other rows, §5.2, §7.1 other metrics, §7.2.1–§7.2.2, §8, §10.1, §11, Appendix C remaining rows, closing italic line.

## CONFIRM

- §2.1 Security Hub Findings "7 years": Security Hub natively retains findings for 90 days; confirm how (or whether) findings are retained for 7 years, or change the row to 90 days with review records kept in the compliance platform. Marked `[CONFIRM: …]` in the table.
- §4.2 new "Customer Account Data Expiration" row: confirm the retention enforcement Lambda actually deletes customer account data at relationship end + 24 months (R5 says it does; the row was not in v1).
- §2.1 Authentication Records "2 years": kept from v1; these records live in PropelAuth — confirm the value and the mechanism.
- §2.1 Consent Records "Duration of processing + 7 years" and the monthly "Consent Record Review" EventBridge process in §4.2: kept from v1; confirm these exist (the Consent Management Procedure referenced elsewhere does not).
- §3.2.4 "Lambda function identifies and deletes expired manual snapshots": kept from v1; confirm this Lambda exists.
- §3.2.5 ECR "untagged images after 14 days": kept from v1; confirm the lifecycle policy value.
- §7.1 targets (">99%", "0 records") and §7.3 monthly retention compliance reports: kept from v1; confirm the monthly report is actually produced.
- Revision history: v1 body table dated the policy November 13, 2025 (1.0) and February 2, 2026 (2.0) while the frontmatter was 1.0 finalized February 2, 2026 — confirm the 1.0 date to show.

## Quality sweep (2026-10-31)

- Structure reordered to the Q3 sequence: Purpose → Scope → Definitions (was §11) → Roles and responsibilities (was §6) → Retention schedule → Disposal → Automated enforcement → Data subject rights → Monitoring and audit → Retention incidents → Training → Policy review and exceptions → Related documents (was §1.4) → Appendices → Revision history; all sections renumbered and Appendix C section references updated.
- Merged §1.3 Policy Statement into §1 Purpose (duplicated the purpose text); dropped the four "commitment to" bullets in §1.1 (restated the purpose and the scope); dropped the closing italic "This policy supports … SOC 2 Type II certification" line (summary with no content); dropped §10.2 Approval as a separate heading (one sentence, kept inside §12.1).
- §5.2 justification: three `####` sub-headings (2.2.1–2.2.3) folded into bold lead-ins under one heading.
- §11 Training: §9.2 Awareness Topics list folded into one sentence (the list only named topics).
- Removed blank lines between bullets throughout (~70 lists/bullets); headings changed to sentence case after the number; bold table/bullet labels changed to sentence case.
- Voice: "must render", "ensures", "ensure consistent compliance", "is committed to" → plain present tense; passive steps in §5.3, §8.1, §10.2 given a subject (the CEO, per the roles table); "Note:" prefix removed in §6.3; "comprehensive" ×2 and "detailed" (procedures) removed; "via automated Lambda function" → named the retention enforcement Lambda function.
- Consistency: "AWS KMS" → "KMS"; "N/A" table cell → "—"; ">99%" / "100%" → ">99 %" / "100 %"; "Section 2.3" → "§5.3"; "Incident Reporting system" → "incident reporting module of the compliance platform"; "Chief Executive Officer of Deal Intelligence LLC" → "the CEO" (first use already expanded in §4).
- Related documents: added Incident Response Procedure, System Monitoring and Logging Procedure, and Vendor Management Policy (all referenced in the body and all in the set); no non-existent documents were referenced.
- Word count 2666 → 2554.

### New CONFIRM items

- §9.2/§9.3: the quarterly review and annual audit now name the CEO as the actor (v1/v2 left the subject implicit; the roles table assigns "audits retention practices" to the CEO). Confirm.
- §8.1: the erasure steps now name the CEO as the actor (roles table: "handles data subject requests"). Confirm.

## Decisions applied (2026-10-31)

- D25: cut §7.2 monthly consent-record review row; cut §9.2 quarterly review (section deleted); cut §9.3 annual retention audit (section deleted, annual policy review in §12.1 remains; §4 "Audit" bullet now points to §12.1); cut §9.5 monthly retention compliance reports (section deleted); §9.4 renumbered to §9.2

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §2 data-category list "Security Hub findings" → "monthly configuration-check records"; §2.1 schedule row "Security Hub findings — 7 years [CONFIRM: Security Hub retains 90 days]" → "Configuration-check records (monthly, compliance platform) — 7 years". The CONFIRM is resolved: the record is now a dated pass/fail document posted to the compliance platform, so 7 years (matching the other compliance-platform records) no longer depends on a native AWS retention limit.
- D11b, D13b, D14: no insurance, availability-measurement or controller/processor text in this document; nothing to apply.
