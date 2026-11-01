# Change note — data-classification-policy (v1.0 → MERGED, no v2)

- R7: no v2 written. The Policy is merged into `policies-v2/data-classification-and-handling-standard.md` (v2.0); `policies-v2/data-classification-policy.MERGED.md` records what was carried over and what was dropped.
- R7: carried into the Standard — Appendix A decision tree, Appendix B data element reference (two table halves joined), Appendix C quick reference card, §6.1/§6.3 notes on legitimate-interest basis and aggregated data, business contact information = Confidential, API keys/credentials/keys = Restricted, Secrets Manager as the approved Restricted storage location.
- R7: dropped — the Policy's own tier definitions and §2.2 Classification Summary Matrix (Standard's tiers kept), §5.3 retention table and retention figures (retention schedule lives only in Data Retention & Disposal), §4.1/§4.2 storage and transmission tables (the Standard's §3.2/§3.3 cover storage and transmission).
- R1: dropped the "P3.1 / P4.1 / P6.1" mappings in §2.1.2 and the second §8.1 table.
- R2: dropped the roles Data Owner, Data Custodian and Information Security (§3.1, §3.2, §3.4); "Information Security" in Appendix C → CEO; §11.2 "Approval from Information Security and Data Owner" → CEO (already the approver in the Standard §10.1); blank §12.3 Document Approval table dropped.
- R4: dropped "Apply classification labels to documents and communications" (§3.3, §5.1 step 2), "Initial Training: Within 5 days of receiving system access" (§9.1), "24/7 system monitoring" (§4.4), "Automated quarterly access reviews via Lambda function" wording (§4.3, §11.1 — the Standard uses "scheduled Lambda check, recorded in the compliance platform"), the reference to the non-existent Consent Management Procedure (§5.1), and the Third-Party Integration Security Guidelines reference (§7.2, R7).
- R5: the Policy's §10.3 "Post-incident retrospective within 24 hours for emergency changes" is superseded by the Standard's "5 business days".
- R6: the Policy's §12.2 Version History (a "2.0 | February 2, 2026 | Information Security" row for a document that was never published as 2.0) is not carried forward.

## CONFIRM

- Retire the Data Classification Policy record in the compliance platform and re-point any control/evidence that cites it to the Data Classification and Handling Standard v2.0.
- The Policy's §7.1 sub-processor table (AWS, PropelAuth only) is not carried into the Standard; the Standard now points to the Vendor Management Policy list (AWS, PropelAuth, Google Workspace, GitHub, Resend, compliance platform hosting). Confirm that list is final before the Standard is published.
