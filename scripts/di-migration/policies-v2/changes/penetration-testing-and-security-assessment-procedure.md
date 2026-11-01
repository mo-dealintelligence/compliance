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
