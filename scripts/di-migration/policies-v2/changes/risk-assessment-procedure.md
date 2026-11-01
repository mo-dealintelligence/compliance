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

## Quality sweep (2026-10-31)

- Structure: fixed 3 `####` leftovers (`#### 1. Annual Comprehensive Assessment` …) into 5.1.1–5.1.3; `#### Likelihood Scale (1-5):` / `#### Impact Scale (1-5):` pseudo-headings turned into lead-in lines; merged §10 Compliance Requirements (CC3.1–CC3.4 with COSO principle names, CC9.1–CC9.2, GDPR Art. 32/35, CCPA 1798.150) into §1 Purpose; §11 Related Documents → §10 with bold group labels instead of unnumbered `###`; revision history numbered §11.
- Voice: converted 13 "shall" constructions to present tense; removed "comprehensive" ×4 ("comprehensive risk management", "Annual comprehensive risk assessments", "Annual Comprehensive Assessment", "Comprehensive risk landscape" → "Full risk landscape"); "establishes the systematic approach" → "sets out how"; "Ongoing risk monitoring activities include:" lead-in dropped (heading says it).
- Formatting: removed blank lines between bullets and numbered steps (≈130 lines); table header bold removed; en dashes in scales and ranges; "99.9%" → "99.9 %"; "Ad-hoc" → "Ad hoc"; Oxford comma applied; lowercase after the number in scale items ("Rare – less than once per year").
- Consistency: §4.1 / §4.2 given lead-in sentences; "Define organizational risk appetite" → "Defines the risk appetite"; "Risk Score Calculation" → "Risk score".
- Related documents: same 15 documents, alphabetised within groups; all exist in the set.
- Kept: all scales, thresholds, the current-key-risks table, treatment options, KRIs, acceptance criteria.

No new CONFIRM items.

## Decisions applied (2026-10-31)

- D25: cut §6.2 weekly CloudWatch metrics analysis and the monthly vulnerability scan review (monthly line now Security Hub findings review only); cut §8.2 monthly operational reports block. Kept: §4.1/§8.1/§8.2/§9 quarterly risk reporting and review (quarterly risk review and management meeting), §6.1 annual risk assessment, §6.2 quarterly review of control evidence and tasks.
- D12: §6.2 monthly Security Hub findings review unchanged.
- D19: concerns the risk-register record, not this procedure; nothing changed here.

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed — §5.1.2 "Security Hub findings analysis" → monthly configuration-check record analysis and real-time CloudTrail event alerts; §6.1 step 2 "Review Security Hub findings" → review of the monthly configuration-check records, CloudTrail event alerts and CloudWatch metrics; §6.2 real-time row → security-relevant CloudTrail events via EventBridge → breach-detection Lambda → SNS to the CEO, monthly row → configuration-check Lambda pass/fail record reviewed and recorded in the compliance platform; revision-history v2.0 entry reworded
- D11b: not applicable here — §5.3 "Transfer: share the risk through insurance or contractual agreements" is a generic risk-treatment option, not an insurance claim or vendor requirement; left as is
