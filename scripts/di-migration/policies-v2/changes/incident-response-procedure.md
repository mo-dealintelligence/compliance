# Incident Response Procedure — v1.0 → v2.0 change note

- R0: frontmatter — `version` 1.0 → 2.0, `supersedes: "1.0"`, publication placeholders for `effective_date`/`review_date`, `finalized_at` dropped; "Revision history" section added.
- R0: fixed "#### 1." repeated-numbering artefacts in §5.2.1, §5.2.2, §5.3.2, §5.3.3, §5.4.1 into numbered 1/2/3 lists with indented sub-bullets.
- R0/R8: restored collapsed bullets (§2 first bullet, §3 Low (P4), §4 "Document incident timeline … Perform forensic analysis", §4.4 "Report … Preserve", §5.1.3 channel list, §5.3.2 "Update security group rules and NACLs", "Review and update CloudFormation security parameters", §6.1 "SNS notifications", §6.2.2 CCPA bullets, §6.2.3 bullets, §10.1 "Post-incident review completion", §12 last run-on bullet split into two).
- R6: "di-backend-apiprod" → "di-backend-api-prod".
- R1: §2 "all five Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy" → "the Trust Services Criteria in scope: Security, Availability, and Confidentiality"; §5.2.2 "Processing integrity validation" → "Data integrity validation".
- R2/R4: §3 "Incident Response Team (IRT): Virtual team … Executive Leadership and Security Lead" → "Incident Commander: The CEO, who declares, leads, and closes incidents".
- R2: §4.1 Executive Leadership, §4.2 Security Lead and §4.3 System Owner merged into "4.1 Chief Executive Officer (Incident Commander)" with all bullets kept; §4.4 All Personnel renumbered 4.2.
- R2: §4.1 "Coordinate with legal counsel for regulatory compliance" → "Determine regulatory notification obligations under GDPR and CCPA"; §6.2.3 "Legal counsel for regulatory compliance" removed; §8.2 "As directed by counsel" → "Until the investigation is closed, and no less than 7 years".
- R4: §5.1.1 "Maintain current incident response playbooks for common scenarios" → "This procedure, together with the Business Continuity Plan and the severity matrix in Section 7, is the response reference for common scenarios" (scenario list kept); §5.4.1 "Update incident response playbooks" → "Update this procedure".
- R4: §5.1.3 "Secondary: Encrypted messaging platform" removed; §6.1 "Encrypted messaging for sensitive details" and "Video conferencing for incident command meetings" removed, replaced by "Direct phone contact for Critical incidents" (from §5.1.3) and "Incident record in the compliance platform's Incident Reporting system".
- R4/R5: §5.2.1 "Event Triage (Within 15 minutes)" → "(Critical (P1) events acknowledged within 4 business hours; other severities per Section 7.1)"; "Incident Declaration (Within 30 minutes)" → "(upon completion of triage)"; "Activate incident response team" → "The CEO assumes the Incident Commander role".
- R4: §5.3.1 "Implement emergency WAF rules in CloudFront" → "Tighten API rate limiting in middleware and restrict origin access at CloudFront".
- R4: §5.4.2 "Update incident metrics dashboard" → "Update incident metrics".
- R2: §6.1 "Real-time updates every 30 minutes for Critical incidents" → "Incident record updated every 30 minutes for Critical incidents".
- R4: §6.2.3 "Cyber insurance carrier for covered incidents" removed.
- R4/R5: §7.1 severity matrix kept; "Response Time" column → "Acknowledgement Target": P1 15 minutes → 4 business hours; P2 30 minutes → 1 business day; P3 2 hours → 5 business days; P4 24 hours → monthly Security Hub findings review. "Escalation" column → "Handling" (Executive Leadership / Security Lead → CEO; Security Hub/SNS real-time alert for P1/P2; monthly review for P4).
- R5: §8.2 "Security incident evidence: 2 years minimum" → "7 years".
- R2/R4: §8.3 "Access: Restricted to incident response team" → "Restricted to the CEO"; "Backup: Cross-region replication for critical evidence" → "S3 versioning within the single region (us-east-1)".
- R4/R5: §9.1 "Quarterly Tabletop Exercises" + "Annual Simulation" → single "Annual Tabletop Exercise (recorded in the compliance platform)" with the tabletop bullets plus customer communication practice and recovery procedure validation (pointing to the BCP full test record); "Full team activation" and "Technical incident simulation" dropped.
- R4/R5: §10.1 MTTD "< 15 minutes" → "Critical findings alerted in real time via Security Hub/SNS"; MTTR "< 30 minutes" → "Mean Time to Acknowledge (MTTA): < 4 business hours for Critical (P1)"; MTTC "< 2 hours" → "< 2 hours from acknowledgement".
- R2: §10.2 "Monthly incident summary to Executive Leadership" → "recorded in the compliance platform"; quarterly trend analysis "recorded in the management meeting minutes".
- Kept verbatim (no rule applies): §3 definitions, §5.2.2 evidence list, §5.3 containment/eradication/recovery bullets, §6.2 notification content, §7.2 escalation triggers, §8.1, §8.3 "MFA delete", §9.2 maintenance cadence, §11.

## CONFIRM

- §7.1 acknowledgement targets for P2 (1 business day), P3 (5 business days) and P4 (monthly review): only the P1 value (4 business hours) is given by the rulebook; the others are chosen to sit below P1 and need Mo's confirmation.
- §10.1 MTTC "< 2 hours from acknowledgement": v1 said "< 2 hours" with no reference point; confirm the measurement basis.
- §8.3 "S3 bucket with versioning and MFA delete": v1 claim not covered by any rule; confirm the evidence bucket actually has MFA delete enabled.
- §9.2 "Monthly update of contact lists and escalation paths": v1 cadence kept; confirm this is actually performed monthly.

## Quality sweep (2026-10-31)

- Severity scale: normalised to P1–P4 throughout — "Critical (P1)" → "P1 (Critical)" in definitions and the matrix, and "Critical/High severity", "Critical and High", "Medium/Low" in body text → "P1 and P2", "P3 and P4" (×9); vulnerability wording untouched.
- Voice: "establishes the systematic approach" → "sets out how"; "leverages" → "uses"; removed "ensures rapid …" framing, "proactive threat intelligence" → "threat intelligence"; "shall guide" → "guide"; "Continuous improvement based on lessons learned" → "Updates based on lessons learned"; "Archive evidence in secure S3 bucket with encryption" → "in the encrypted S3 evidence bucket".
- Formatting: removed blank lines between bullets and between numbered steps and their sub-bullets (≈170 lines); colon-suffixed pseudo-headings (`#### During Incident:` etc.) turned into lead-in lines; table header bold removed; "ECS/Fargate" → "Fargate"; "GDPR/CCPA" → "GDPR and CCPA"; "99.9%" → "99.9 %"; "100%" → "100 %"; Oxford comma applied; revision history numbered §13.
- Consistency: §4.1 / §4.2 given lead-in sentences; "Section 7" → "section 7"; "Upon" → "On".
- Related documents: alphabetised after Information Security Policy; same 12 documents, all in the set.
- Kept: 48 h / 72 h notification figures, 4-business-hour P1 acknowledgement, all KPIs, 7-year evidence retention, escalation triggers.

No new CONFIRM items.

## Decisions applied (2026-10-31)

- D3: §8.3 "S3 bucket with versioning and MFA delete" → "S3 bucket with versioning".
- D8: cut the 2-hour isolation/containment clock: §7.2 escalation trigger "Inability to contain the incident within 2 hours" removed; §10.1 "Mean time to contain (MTTC): target < 2 hours" removed. §5.2.1 / §7.1 / §10.1 P1 acknowledgement within 4 business hours kept (R4 response target, not the 4-hour triage clock).
- D10: §6.1 internal 30-minute P1 updates kept and noted as internal; §6.1 and §6.2.1 cross-reference the SLA Management Policy's customer-facing cadence (every 2 hours for P1); SLA Management Policy added to §12 Related documents.
- D25: cut §9.2 quarterly review of incident metrics and trends; cut §9.2 monthly update of contact lists and escalation paths; cut §10.2 monthly incident summary. Kept: §9.1 annual tabletop, §9.2 annual procedure review, §10.2 quarterly trend analysis recorded in the management meeting minutes (quarterly risk review / management meeting), §10.2 annual program review.
- D12: §7.1 P4 monthly Security Hub findings review unchanged.

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §1 detection-capabilities sentence, §5.1.2 detection list (Security Hub aggregation bullet → CloudTrail-EventBridge → breach-detection Lambda → SNS real-time alert with the event list; monthly configuration-check record added as the drift-detection source), §5.2 triage step "Review the Security Hub findings" → SNS alert / triggering CloudTrail event / failed configuration-check item, §5.2 evidence step "Screenshot Security Hub findings" → capture the alert, CloudTrail event record and configuration-check record, §6 improvement action "Enhance detection rules in Security Hub" → extend the EventBridge rule or the checklist, §7.1 severity matrix (P1/P2 handling "Security Hub/SNS" → "CloudTrail-EventBridge/SNS"; P4 acknowledgement target "Monthly Security Hub findings review" → "Monthly configuration-check review", handled when the record is posted), §10.1 MTTD KPI reworded.
- D11b, D13b, D14: no insurance, availability-measurement or controller/processor text in this document; nothing to apply.
