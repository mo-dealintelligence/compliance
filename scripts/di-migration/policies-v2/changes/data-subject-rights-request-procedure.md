# Change note — data-subject-rights-request-procedure (v1.0 → v2.0)

- R0: frontmatter `doc_type` "Policy" → "Procedure", `version` 1.0 → 2.0, `effective_date` / `review_date` set to publication placeholders, added `supersedes: "1.0"`; dropped the v1 `finalized_at` export stamp.
- R0: added §15 Revision history.
- R0: fixed the Humadroid "### 1." repeated-numbering artefacts in §5.1–§5.4 into proper numbered steps 1/2/3 with indented bullets; sub-section headings "## 3.1" etc. demoted to `###` under their parents; §10.1 KPI table (split into two halves by the export) rejoined into one table.
- R0/R8: restored run-on bullets into real lists (§2, §4.3, §5.1, §5.2, §5.3, §7.1, §7.2, §12, §13); removed `<u>` artefacts and the broken "- Template" bullet in §7.1.
- R1: §1 removed "and SOC 2 Trust Service Criteria for Privacy (P6.1-P8.1)" — purpose now cites GDPR Articles 15-22 and CCPA §1798.100-1798.130 only.
- R1/brief: §1 added one paragraph stating the controller/processor roles (controller for compiled business contact information; processor for customer-uploaded/account-held data, cross-referencing §6.2) with an inline `[CONFIRM: …]` marker because v1 did not state it explicitly; §6.2 heading sentence extended with "where Deal Intelligence acts as processor".
- R6: §4.1 `privacy@dealintelligence.ai` → `privacy@dealintelligence.io`.
- R2: §2 "handled through separate HR procedures" → "handled directly by the CEO".
- R2: §8.1 Data Protection Officer, §8.2 Privacy Operations Lead and §8.3 Technical Implementation merged into §8.1 Chief Executive Officer (data protection contact; all v1 bullets retained except "Coordination with technical teams" (no teams) and "Lambda function maintenance for automated processing" (R4); "Integration with PropelAuth for authentication data" → "Removal of PropelAuth user records"); added §8.2 Go-to-Market Contractor (forwards requests to privacy@; does not process; no production access).
- R2: §5.1 step 3 "Legal review for exemptions or restrictions" → "Review by the CEO for exemptions or restrictions".
- R4: §2 "Automated and manual processes for request fulfillment" → "The manual processes for request fulfillment described in Section 9"; "Third-party sub-processors (PropelAuth and AWS)" → "Sub-processors involved in data processing, as listed in the Vendor Management Policy" (R7 list); Vendor Management Policy added to §13.
- R4: §4.1 "All requests are automatically logged in the compliance platform" → "All requests are recorded by the CEO as a dated entry in the compliance platform".
- R4: §5.1 step 1 discovery bullets made the manual runbook: "Query DocumentDB collections ... by email address and company domain", "Check PropelAuth user records", added "Check HubSpot CRM records" (HubSpot is named in the R4 runbook row); step 3 "Document completion in the compliance platform" → "as a dated entry".
- R4: §5.2 step 2 "Execute Lambda function for automated deletion" + "Remove from DocumentDB collections" → "Locate and delete the records from DocumentDB collections by email address and company domain"; "Purge from backup systems (90-day cycle)" → "Backup copies expire under the 90-day backup retention cycle and are not restored" (backup purge automation removed; consistent with §6.3); "Notify PropelAuth for authentication data removal" → "Delete the PropelAuth user record where one exists"; added "Delete the HubSpot CRM record where one exists"; step 3 "Document deletion certificate" → "Record a dated deletion entry in the compliance platform".
- R5/R4: §3.1 deleted the "Restriction (Article 18) | 72 hours" row; §5.4 Restriction Requests deleted in full (72-hour initial restriction, "Flag account in PropelAuth", "Suspend automated processing Lambda functions", SNS alerts); §5.5 Portability renumbered to §5.4.
- R4: §9 "Automation and Tools" → "Runbook and Tools": §9.1 "Automated Processing" (Lambda discovery, EventBridge deadline monitoring, SNS team alerts, CloudWatch request metrics) → §9.1 "Manual Runbook" (verify identity → locate records in DocumentDB by email/domain, PropelAuth user, HubSpot → act → record dated entry in the compliance platform); §9.2 "Human review required for" → "The CEO personally reviews" (same four bullets); §9.3 trimmed to request tracking as dated entries with due dates, audit trail, compliance reporting (removed "Automated deadline calculations and reminders" and "Template responses").
- R4: §10.2 "Monthly reports generated via the compliance platform" → "recorded in the compliance platform".
- R4: §11 removed "Review quarterly updates on regulatory changes" (newsletter-style activity; training is onboarding + annual).
- Kept verbatim (no rule applies): §3.2, §4.2, §5.3 content, §5.4 (ex-5.5) content incl. 7-day link expiry, §6.1, §6.3, §7.2 extension limits, §7.3, §10.1 targets, §12, §14, 24-month lead retention and 7-year financial records in §5.2 step 1.

## CONFIRM

- Controller/processor framing in §1 (inline `[CONFIRM]`): v1 only implied it via §6.2. Confirm the wording "controller for the business contact information it compiles and delivers; processor for data customers upload to or hold within their own accounts" and remove the marker.
- Article 18 (restriction of processing) now has no row in §3.1 and no procedure section, because the brief said to delete the 72-hour restriction row. GDPR still grants the right; if Mo wants it covered, add a "Restriction (Article 18) | 30 days" row and a manual step (CEO excludes the record from delivery until resolved).
- §4.1 "Secondary Channel: Authenticated customer portal via PropelAuth" kept verbatim — confirm a DSR submission path actually exists in the portal; otherwise delete the channel.
- §5.2 "Clear CloudWatch logs where permissible" kept — confirm log entries are ever cleared manually, or reword to "logs expire under the 90-day retention".
- HubSpot is named as a location of contact records (from the R4 runbook row) but is not in the R7 sub-processor list; confirm whether HubSpot should be added to the Vendor Management sub-processor list.
- §10.1 KPI targets (<20 days average, >95 % on-time, <5 % denial, <10 % extension; monthly/quarterly measurement) kept verbatim — confirm these are tracked in the compliance platform or drop the table.
- Frontmatter `finalized_at` dropped; confirm the migration script does not require that key.

## Quality sweep (2026-10-31)

- Q3 structure: §8 Roles and responsibilities moved to §3 (sections 3–8 renumbered 4–9; internal references updated: 6.2 → 7.2, 4.2 → 5.2, 5 → 6; Section 9 unchanged); §14 "Review and Updates" → §13 "Review" and moved before Related documents (§14); Revision history → §15. No section deleted.
- Q1 voice: §1 rewritten to plain declarative (removed "establishes the operational framework", "ensures that", "operationalizes… to ensure"); "shall be reviewed" → "is reviewed"; §7.x and §8.x fragment/imperative mixes made parallel ("Requests are forwarded…", "The customer is responsible…", "Give the specific reason…"); §7.1 "Clear communication about data source and limitations" → "The response states the data source and any limitations"; §9.2 "The CEO personally reviews" → "The CEO reviews in particular" (the CEO already processes every request under §9.1); §9.3 heading "Compliance Platform Integration" → "Compliance platform".
- Q2 consistency: "Chief Executive Officer (CEO)" in the roles heading; "the" added before document titles (×9); Oxford commas; percentages spaced (">95 %", "<5 %", "<10 %"); en dashes in ranges ("Articles 15–22", "days 1–5"); "Opt-out of sale" → "Opt out of the sale".
- Q2 headings/lists/tables: all headings and table headers to sentence case; "**Primary Channel** :" spacing fixed (×11); removed blank lines between bullets and numbered items (all lists); nested lists indented consistently.
- No commitment, number, role, scope item or control changed; the existing §1 [CONFIRM: controller/processor framing] is kept.

### CONFIRM (new)

- None added.

## Decisions applied (2026-10-31)

- D14: §1 controller/processor framing confirmed; [CONFIRM] tag removed
- D16: §4.1 GDPR Art. 18 restriction row restored at 30 days; new §6.5 manual restriction process; §9.1 runbook "Act" step includes restrict (revision-history summary updated)
- D22: author set to Mo Messidi (frontmatter and revision history)
- D25: deleted §10 Metrics and reporting (monthly/quarterly KPI table rows and monthly compliance reports); §§11–15 renumbered to 10–14

## Decisions applied (2026-10-31, round 2)

- D14: marked OPEN — `[CONFIRM: D14 open — pending investigation]` appended to the §1 controller/processor framing sentence; applied text kept unchanged pending the investigation
