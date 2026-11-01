# Change note — code-of-conduct (v1.0 → v2.0)

- R0: frontmatter `version` 1.0 → 2.0, `effective_date` "N/A" and `review_date` "N/A" → publication placeholders, added `supersedes: "1.0"`; dropped v1 `finalized_at`. v1 headings were unnumbered; left unnumbered (structure kept).
- R0: added "Revision History" section.
- R0/R8: restored the collapsed "- a - b - c" run-on lists into real lists (Scope, General Standards, Conflicts of Interest, Intellectual Property, Customer Data Handling, Security Responsibilities, Reporting Obligations, reporting channels, Non-Retaliation, Disciplinary Actions, Related Policies); removed `<u>` artefacts.
- R2: Purpose "all employees, contractors, and stakeholders" → "all personnel, contractors, and stakeholders".
- R2: Scope "Full-time and part-time employees / Contractors and consultants / Board members and advisors / Third-party representatives" → "The Chief Executive Officer / The Go-to-Market Contractor / Contractors and consultants engaged by Deal Intelligence / Third-party representatives acting on behalf of Deal Intelligence" (Board members removed).
- R2: Conflicts of Interest "Disclose ... to management" → "to the CEO"; "Obtain approval before engaging in outside employment" → "Obtain approval from the CEO before ...".
- R2: Reporting channels "Direct supervisor or management / Compliance team" → "The CEO"; compliance platform Incident Reporting system and "Anonymous reporting channels when available" kept.
- R6: frontmatter `acknowledgment: "None"` → `"Explicit"`.
- R6: Acknowledgment section "upon hiring" → "at onboarding"; "Annual re-acknowledgment is required" → "... required and recorded in the compliance platform portal"; "documented in compliance records" → "documented in the compliance platform".
- R6: closing Acknowledgment "By signing below or acknowledging electronically" → "By acknowledging electronically in the compliance platform portal"; removed the "Signature / Print Name / Date" wet-signature lines (acknowledgment is captured in the portal).
- R6: "AIpowered" → "AI-powered".
- R7: Third-Party Interactions "Follow Third-Party Integration Security Guidelines" → "Follow the Integration security section of the API Security and Rate Limiting Standard".
- Kept verbatim (no rule applies): Core Principles, Privacy Compliance (already GDPR/CCPA wording), Acceptable Use, Non-Retaliation, Disciplinary Actions, Monitoring and Review, Related Policies list.

## CONFIRM

- "Anonymous reporting channels when available" kept verbatim; confirm whether any anonymous channel exists or delete the bullet.
- "Suspension with or without pay" and "Performance improvement plans" kept as v1 disciplinary steps; confirm they are meaningful for a contractor relationship or trim to warnings / termination of contract / legal action.
- Revision history v1 date taken from the v1 `finalized_at` (November 30, 2025) because v1 `effective_date` was "N/A"; confirm.

## Quality sweep (2026-10-31)

- Structure: v1 headings were unnumbered; numbered as `## 1.`–`## 11.` with `### n.n` sub-headings (Purpose, Scope, Core principles, Professional conduct, Data protection and privacy, Technology and systems use, Reporting and non-retaliation, Compliance and enforcement, Related documents, Acknowledgment, Revision history).
- Voice: "maintaining the highest standards of integrity in providing" → "the integrity with which Deal Intelligence provides"; "Ensure proper licensing" → "Use only properly licensed software"; "Ensure vendors comply" → "Confirm that vendors comply"; "Ensure appropriate consent" → "Confirm appropriate consent"; "our" → "the" where it named a document; "should be made through" → "are made through"; "must acknowledge understanding of this Code" → "acknowledge this Code".
- Formatting: removed blank lines between bullets (≈60 lines); "Deal Intelligence LLC" on first mention; "Chief Executive Officer (CEO)" in Scope; "Report violations … through appropriate channels" → "through the channels in section 7".
- Related documents: expanded from 4 to 13 — added every document the body already cites (Access Control and Authentication Policy, API Security and Rate Limiting Standard, Change Management Policy, Data Classification and Handling Standard, Data Retention and Disposal Policy, Data Subject Rights Request Procedure, Secure Software Development Lifecycle (SDLC) Standard, Security Awareness Training Program, Vendor Management Policy); all exist in the set.
- Kept: disciplinary steps and anonymous-channel bullet (existing CONFIRM items), acknowledgment wording.

No new CONFIRM items.

## Decisions applied (2026-10-31)

- D4: §5.2 new bullet "Access company data only from a device with FileVault full-disk encryption (macOS) enabled, through browser SSO with MFA".
- D5: §7.1 "Anonymous reporting channels, when available" removed; reporting goes to the CEO by email.
- D6: §7.1 CEO reporting channel given the address compliance@dealintelligence.io.
- Closes the existing CONFIRM item on the anonymous channel.
