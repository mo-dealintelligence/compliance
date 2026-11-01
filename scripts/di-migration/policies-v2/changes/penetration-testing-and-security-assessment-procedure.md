# Change note — Penetration Testing and Security Assessment Procedure v1.0 → v2.0

- R0: frontmatter — version 1.0 → 2.0, `supersedes: "1.0"`, `doc_type` Policy → Procedure, effective/review dates set to placeholders, `finalized_at` export field dropped; added §14 Revision history; sections renumbered after deletions (v1 §13 → §11, §14 → §12, §15 → §13).
- R6: §2 "dibackend-api-prod" → "di-backend-api-prod".
- R2: §2 exclusion "Social engineering tests (limited applicability for solo operation)" → "Social engineering tests" (size language removed).
- R8: restored run-on bullets in §1, §2, §4.3, §5.1, §5.2, §5.3, §6.4, §7.2, §9, §10.1, §13 (v1 §15); removed `<u>` underline artefacts.
- R5: §3 definitions — Critical 24 hours kept, with 7-day clock for non-exploited critical dependency CVEs; High 7 days → 30 days; Medium 30 days → 90 days; Low 90 days → best effort.
- R2: §4 Technical Operations Lead and Compliance Officer merged into §4.1 Chief Executive Officer; "Reports assessment metrics to stakeholders" → records in the compliance platform; added §4.2 External Parties (penetration-test vendor, external SOC 2 auditor).
- Brief (budget): §4.1 removed "Ensures budget allocation for security assessments".
- R3: §2, §5.1 annual third-party penetration test kept as written.
- R4/R5: §5.2 "Weekly vulnerability scans via AWS Security Hub and Inspector" → continuous Security Hub checks reviewed monthly (Inspector removed); "API security testing using automated OWASP ZAP scans" removed (DAST); "Infrastructure compliance checks via AWS Config rules" → CloudFormation drift reporting and Security Hub configuration checks; Dependabot line expanded to Dependabot + code scanning + Trivy; ECR line notes scan-on-push.
- R4: §5.3 "Real-time threat detection via AWS GuardDuty" → Security Hub findings routed to SNS by the breach-detection Lambda; CloudTrail analysis split into its own bullet.
- R4: §6.3 "Immediate notification of critical findings via encrypted channels" → "to the CEO" (encrypted-messaging claim removed).
- R4: §7.1 "CloudFormation drift detection analysis" → "CloudFormation drift reporting analysis"; "conducted by CEO" → "conducted by the CEO and recorded in the compliance platform" (R5 monthly review recorded).
- R4: §7.2 "API Gateway security configurations" → "CloudFront and Lambda function URL security configurations".
- R2/R4: §7.3 SAST and secret scanning name the CI tools (Bandit, TruffleHog); "Pull request security reviews before production deployment" → PR self-review with required CI status checks on protected `main`.
- R5: §8 remediation timelines — Critical 24 h with emergency change process defined as PR labelled `emergency` + post-hoc review within 5 business days, plus 7 days for critical dependency CVEs; "High: 7 days with expedited change approval" → 30 days through normal change management; Medium 30 → 90 days; Low 90 days → best effort or next release cycle.
- R7: §9 and §12 "Third-Party Integration Security Guidelines" → Integration security section of the API Security and Rate Limiting Standard; removed from Related Documents.
- Brief (budget/KPI/maturity): deleted v1 §11 Budget and Resource Planning, v1 §12 Metrics and Reporting (12.1 KPIs, 12.2 Executive Reporting), and v1 §13.2 Program Maturity; v1 §13.1 Lessons Learned kept as §11 Continuous Improvement.
- Kept verbatim (no rule applies): §3 Penetration Testing / Security Assessment / Vulnerability definitions, §5.1 scope and timing (Q3, 30-day customer notice), §6.1 vendor selection ($1 million insurance), §6.2 rules of engagement, §6.3 phases, §6.4 report requirements, §8 severity classification and tracking, §10.

## CONFIRM

- §2 "Quarterly automated security assessments" and §5.2 heading kept from v1 — confirm a quarterly assessment record exists in the compliance platform alongside the monthly Security Hub review.
- §5.1 "Conducted annually in Q3" — confirm Q3 is still the intended window.
- §6.1 "Professional liability insurance minimum $1 million coverage" kept from v1 — confirm this vendor requirement is still wanted.
- §7.1 "IAM access analyzer findings" kept from v1 — confirm IAM Access Analyzer is enabled.
- §8 "Findings logged in GitHub Issues with security labels" kept from v1 — confirm pentest findings are logged in GitHub Issues rather than only in the compliance platform.
- §10.3 "Annual attestation of security assessment completion" kept from v1 — confirm an attestation is produced.
- R3 staging: separate account vs same account (not written into the policy).

## Quality sweep (2026-10-31)

- Q1 voice: §1 rewritten from "establishes the formal framework… ensures that… proactively" to plain declarative; removed filler ("comprehensive" ×3, "formal framework", "proactively", "ensures that"); §5.3, §7.1, §7.2, §7.3, §8, §11 lead-ins turned into full sentences naming the owner (the CEO) and the record (the compliance platform).
- Q1 parallel grammar: §6.1 vendor-selection bullets made parallel ("Vendors must…"); §10.2 bullets made full sentences; §6.4 "Updated risk assessment per organizational risk register" → "Risk register updated per the Risk Assessment Procedure" (same commitment, real document name).
- Q2 headings: all headings to sentence case; 19 `####` run-in headings ("Scope Requirements:", "Timing:", …) converted to bold paragraph labels so the numbered hierarchy stops at `###`; "Chief Executive Officer (CEO)" on first use.
- Q2 severity: §3 definitions "Critical Finding / High-Risk Finding / Medium-Risk Finding / Low-Risk Finding" → Critical / High / Medium / Low to match §8 and the Vulnerability Management Procedure; §6.4 "critical and high-risk findings" → "Critical and High findings".
- Q2 numbers: durations as "within 24 hours / 7 days / 30 days / 90 days" in §8; CVSS ranges with en dashes; "Minimum 30-day advance notice" → "Minimum 30 days' advance notice"; "AWS Security Hub" → "Security Hub" ×3; "IAM access analyzer" → "IAM Access Analyzer".
- Q2 lists: removed blank lines between bullets throughout (all 30 lists).
- Q3 structure: §10 "Compliance and Regulatory Requirements" — §10.1 SOC 2 criteria list merged into §1 (which already named two of the four criteria); §10.2/§10.3 kept as §10 "Records and customer notification"; §13 "Policy Review and Updates" → §12 "Review" and moved before Related documents; Related documents → §13, Revision history → §14 (section count unchanged at 14).
- No commitment, number, role, scope item or control changed.

### CONFIRM (new)

- None added. Existing CONFIRM items above still stand.

## Decisions applied (2026-10-31)

- D3: removed IAM Access Analyzer findings from §7.1 monthly security review
- D11: §6.1 vendor insurance — dropped the $1 million figure; professional liability insurance required without an amount
- D22: author set to Mo Messidi
- D25: cut §2/§5.2 "quarterly" automated security assessments (retitled "Automated security assessments"; continuous scanning kept); cut §5.2 manual reviews (SG/NACL audits, CloudFormation template analysis, secrets review) — kept only the quarterly access review; deleted §7.2 quarterly configuration reviews (incl. KMS key-policy/rotation audit) and renumbered §7.3→§7.2; cut §8 monthly metrics and quarterly trend analysis; cut §10.1 "trending data" and configuration review checklists

## Decisions applied (2026-10-31, round 2)

- D11b: §6.1 "Vendors must carry professional liability insurance" deleted — no insurance requirement remains anywhere in the document (CONFIRM item on §6.1 resolved)
- D12: Security Hub removed — §5.2 continuous FSBP checks → monthly configuration-check Lambda against the fixed checklist, posting a dated pass/fail record to the compliance platform; §5.2 "Security Hub configuration checks" → the monthly configuration-check Lambda; §5.3 real-time detection → security-relevant CloudTrail events via EventBridge rule → breach-detection Lambda → SNS alert to the CEO; §5.3 "Security Hub findings aggregation and prioritization" → monthly configuration-check record review; §7.1 monthly review item "Security Hub findings and their remediation" → the monthly configuration-check record and remediation of failed checks; §14 v2.0 revision entry reworded accordingly (CONFIRM item on §2/§5.2 "monthly Security Hub review" now reads as the monthly configuration-check record)
