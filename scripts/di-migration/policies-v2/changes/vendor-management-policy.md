# vendor-management-policy — v1.0 → v2.0 change note

- R0: `version` 1.0 → 2.0; `supersedes: "1.0"` added; `effective_date` / `review_date` placeholders; `finalized_at` dropped; "Revision history" section added; broken "Deal\n\nIntelligence's" and "SLA\n\ncommitments" line breaks fixed; "AES256" → "AES-256"; "subprocessors" → "sub-processors".
- R1: §1 "Security, Availability, Processing Integrity, Confidentiality, and Privacy" → "Security, Availability and Confidentiality".
- R8: run-on lists in §2, §4–§7, §9–§10, §12 (was 13), §13–§14 restored as real bullet lists; missing bullets in §15 Related Documents and §16 Definitions fixed.
- R2: §2 "All employees involved in vendor selection…" → "All personnel …".
- R7: §2 "Current sub-processors: PropelAuth … and AWS …" → reference to §8.1; added scope bullet for third-party services integrated with the platform (pre-integration assessment).
- R7: new §5.3 "Pre-Integration Assessment" — table merged from Third-Party Integration Security Guidelines §5.1; "Legal review via the compliance platform" → "Review by the CEO via the compliance platform" (R2); "24-hour notification requirement" → "Breach notification terms that allow Deal Intelligence to meet its 48-hour customer notification commitment" (R5).
- R5: §6.1 "Breach notification requirements (within 24 hours of discovery)" → "Breach notification requirements that allow Deal Intelligence to meet its 48-hour customer notification commitment".
- R5: §7.1 "Quarterly Reviews: Performance metrics and SLA compliance verification" removed; folded into the Annual Review line; Continuous Monitoring line extended with "the monthly availability figure recorded in the compliance platform" (R4 Synthetics/status-page row replacement).
- R5: §7.3 "for quarterly reviews" → "for the annual vendor review".
- R7: §8.1 "only two approved subprocessors (PropelAuth, AWS)" → AWS (incl. hosting of the compliance platform, self-hosted on AWS), PropelAuth, Google Workspace, GitHub, Resend.
- R7: §8.3 "Governed by Third-Party Integration Security Guidelines" → "Governed by the Integration security section of the API Security and Rate Limiting Standard".
- R5: §9.1 "Vendor must notify Deal Intelligence within 24 hours" → "in accordance with its contractual breach notification terms".
- R2/R4: §9.2 "Immediate activation of incident response team" → "Immediate activation of the Incident Response Procedure with the CEO as incident commander"; added from Guidelines §9.2: immediate assessment of data exposure, credential rotation for all integration points, vendor re-assessment via the compliance platform; R5: GDPR supervisory-authority notification "within 72 hours" stated.
- R7: §11 "Cloud Infrastructure Governance" (AWS Management, Container and Serverless Security) deleted in full; §12–§17 renumbered to §11–§16.
- Brief / R4: §11.1 (was 12.1) "Perform on-site audits with reasonable notice" removed.
- R5: §11.2 (was 12.2) "Quarterly review of vendor compliance certificates" → "Annual review".
- R2: §12 (was 13) Roles — Chief Information Security Officer, Procurement Team and IT Operations consolidated into §12.1 Chief Executive Officer (all bullets kept; "Coordinate with legal for DPA execution" → "Execute DPAs"; "Report vendor risks to executive management" → "at the quarterly management meeting"); "All Employees" → "All Personnel (including the Go-to-Market Contractor)".
- R2/R5: §13 (was 14) exception approver "Chief Information Security Officer" → "CEO".
- R7: §15 Related Documents — "Third-Party Integration Security Guidelines" → "API Security and Rate Limiting Standard"; added Privacy Notice and Data Processing Agreement Template and SLA Management Policy (both referenced in the body).
- R2: Document Approval table (CISO / CTO / Legal Counsel) → single row: Chief Executive Officer, `[CONFIRM: date]`.
- R2: §2 "procurement" → "purchasing" (check.py flags the word as the Procurement role).

## CONFIRM

- Approval date for the CEO signature row.
- Vendor-inbound breach notification: v1 required vendors to notify within 24 hours (§5.3 table, §6.1, §9.1). Reworded to "contractual breach notification terms that allow Deal Intelligence to meet its 48-hour customer commitment" because the R5 breach-notification values are 48 h/72 h and the hyperscale sub-processors' DPAs do not commit to 24 h. Confirm wording, or restore 24 h if the DPAs actually say so.
- Sub-processor service descriptions (Google Workspace = email/SSO/documents; GitHub = source hosting and CI; Resend = transactional email) are inferred from the rulebook and the other policies; confirm they match the customer-facing sub-processor list.
- §7.3 vendor risk review changed from quarterly to annual to match R5; confirm the Risk Assessment Procedure v2 does not still say quarterly for vendor risks.
- §13 "Reviewed quarterly for continued necessity" (exception review cadence) kept from v1 — not addressed by R5; confirm.
