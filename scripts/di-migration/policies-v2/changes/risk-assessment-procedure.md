# Risk Assessment Procedure — v1.0 → v2.0 change note

- R0: frontmatter — `version` 1.0 → 2.0, `supersedes: "1.0"`, publication placeholders for `effective_date`/`review_date`, `finalized_at` dropped; "Revision history" section added.
- R0: fixed "#### 1." repeated-numbering artefacts in §5.1 (1/2/3) and the mixed "1." / "#### 1." list in §6.1 (numbered 1–6 with indented sub-bullets).
- R0/R8: restored collapsed bullets (§4.1 Executive Leadership bullets, §4.4 "Report … Comply", §5.1 "di-backend-api-prod Analysis of …", §5.1 Continuous monitoring bullets, §6.1 "Score risks", §6.2 "Ad-hoc", §8.1 "Number of risk-related incidents", §9 Medium/High bullets, §11 Standards/Procedures/Supporting run-ons split into one bullet per document).
- R1: §2 "all five selected Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy" → "the selected Trust Services Criteria: Security, Availability, and Confidentiality".
- R4: §1 "maintaining Deal Intelligence's 86% control automation rate" → "maintaining the risk register in the compliance platform".
- R4: §3 Control Effectiveness "validated through quarterly automated testing" → "validated through the control evidence recorded in the compliance platform"; Risk Register "maintained in the risk register in the compliance platform" → "maintained in the compliance platform".
- R2: §4.1 Executive Leadership, §4.2 Security Lead, §4.3 System Owner merged into "4.1 Chief Executive Officer (CEO)" with all bullets kept; "Participate in risk assessment activities" (System Owner) dropped as redundant for the CEO; §4.4 All Personnel renumbered 4.2.
- R2/R4: §4.1 "Monitor control effectiveness through automated testing" → "through the control evidence recorded in the compliance platform"; "Report risk status to executive leadership quarterly" → "Record risk status in the quarterly management meeting minutes".
- R4: §5.1 "Review of all systems documented in CloudFormation stack di-backend-api-prod Analysis of 100+ AWS resources for security vulnerabilities" → "Review of all systems and resources documented in CloudFormation stack di-backend-api-prod for security vulnerabilities".
- R7: §2 and §5.1 "sub-processors (PropelAuth and AWS)" → "sub-processors listed in the Vendor Management Policy" / "per the Vendor Management Policy" (the v2 sub-processor list is longer than two; this document now defers to the list rather than restating it).
- R2/R5: §5.3 Critical threshold "executive approval needed" → "CEO approval needed"; §6.1 step 5 "Obtain executive approval" → "Obtain CEO approval".
- R3: §5.3 Service Availability row controls "Multi-AZ, 99.9% SLA, backups" → "Multi-AZ DocumentDB, 99.9% SLA, 90-day backups" (row now true).
- R5: §6.2 "Daily: Security Hub alert review" → "Real time: Critical Security Hub findings alerted via SNS" + "Monthly: Security Hub findings review (recorded)"; R4: "Quarterly: Control effectiveness testing via Lambda functions" → "Quarterly: Review of control evidence and tasks in the compliance platform".
- R8: §4.1/§6.3/§7.4 "the compliance platform's risk assessment module" / "Business Continuity Plans module" → "the compliance platform"; §7.2 "Vendor Assessment workflow" → "vendor assessment workflow".
- R4: §8.1 "Control effectiveness rate (target: maintain >86% automation)" → "Control effectiveness rate (controls with current evidence in the compliance platform)".
- R2: §8.2 "Executive Dashboard (Quarterly)" → "Management Report (Quarterly, recorded in the management meeting minutes)"; "Control testing results" (monthly) → "Control evidence results".
- R2/R5: §9 "Low Risks: Security Lead approval" → "CEO approval"; "Medium Risks: Executive approval" → "CEO approval".
- Kept verbatim (no rule applies): §3 other definitions, §5.2 scales, §5.3 thresholds and the other three risk rows, §5.4, §6.1 week plan, §6.3, §7, §8.2 annual report, §10.

## CONFIRM

- §5.3 key-risk table scores (inherent/residual values) are carried over from v1 unchanged; confirm they match the current register in the compliance platform.
- §6.1 seven-week annual assessment timeline kept from v1; confirm it reflects how the annual assessment is actually run.
- §6.2 "Weekly: CloudWatch metrics analysis" kept from v1 (not a daily review, so not struck by R5); confirm it is performed weekly.
