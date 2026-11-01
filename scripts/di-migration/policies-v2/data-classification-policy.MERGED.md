# Data Classification Policy — MERGED (no v2)

The Data Classification Policy (v1.0, `data/markdown/data-classification-policy.md`, Feb-2026 export) has been merged into the **Data Classification and Handling Standard v2.0** (`policies-v2/data-classification-and-handling-standard.md`) per RULEBOOK R7. There is no v2 of this Policy; the Standard is the single classification document.

What was carried over into the Standard:

- The classification decision tree (Policy Appendix A) → Standard Appendix A.
- The data element classification reference (Policy Appendix B, both halves joined into one table) → Standard Appendix B, with the Policy §6.1/§6.3 notes on the legitimate-interest basis and on aggregated market intelligence data appended beneath it.
- The quick reference card (Policy Appendix C) → Standard Appendix C, with "Information Security" → CEO (R2).
- Business contact information is classified **Confidential** (Policy §2.1.2 / §6.1), replacing the Standard v1 placement of it under Restricted.
- API keys, credentials and keys are **Restricted** (Policy §2.1.1), and the Policy's approved storage location for them (AWS Secrets Manager) is reflected in Standard §2.1.4 and §3.2.

What was deliberately not carried over:

- The Policy's own tier definitions and Classification Summary Matrix (§2.1–2.2) — the Standard's tier structure is kept (R7).
- The retention table (Policy §5.3) and the retention figures in the matrix — the retention schedule lives only in the Data Retention and Disposal Policy and is referenced from Standard §6.1 (R7).
- The SOC 2 alignment tables and "P3.1 / P4.1 / P6.1" mappings (§2.1.2, §8.1) — Privacy criteria are out of scope (R1).
- The roles Data Owner, Data Custodian and Information Security (§3) — only the CEO and the Go-to-Market Contractor exist (R2).
- "Apply classification labels to documents and communications" (§3.3, §5.1) — labeling/marking is removed (R4).
- "Initial training within 5 days of receiving system access" (§9.1) — removed (R4).
- The reference to a Consent Management Procedure (§5.1) — the document does not exist (R4).
- The Policy's version history row "2.0 | February 2, 2026 | Information Security" and the blank Document Approval table — superseded by the Standard's Revision history (R0/R2).

Retire the Policy in the compliance platform and point any control that cited it to the Standard.
