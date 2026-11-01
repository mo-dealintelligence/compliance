# Change note — Secure Software Development Lifecycle (SDLC) Standard v1.0 → v2.0

- R0: frontmatter — version 1.0 → 2.0, `supersedes: "1.0"`, `doc_type` Policy → Standard, effective/review dates set to placeholders, `finalized_at` export field dropped; added §13 Revision history.
- R1: §1 removed "Processing Integrity (PI1.2-PI1.5)" from the TSC mapping; kept CC3.4 and C1.1.
- R8: §2 restored run-on "All personnel … Integration points with PropelAuth" into two bullets; named repository `dealintelligence/di-backend-api`, GitHub Actions CI, CloudFormation via Serverless Framework.
- R3: §2 "staging" → "the staging stage"; §5.4.1 "Deployment to staging environment first" → "Deployment to the staging stage first"; "Manual approval via GitHub Actions workflow" → "Deployment only from a green CI run on `main`, approved via the GitHub Actions workflow".
- R2: §4 collapsed CTO / Security Champion / Development Lead (all Mo Messidi) into §4.1 Chief Executive Officer with the union of the three responsibility lists; "Conducting peer code reviews via GitHub pull requests" → self-review on PR with required CI status checks on protected `main`; added §4.2 External Parties (external SOC 2 auditor, penetration-test vendor) as the independent-review compensating control.
- R2/R4: §5.2.2 "All code changes require pull request review" → PR on protected `main`, no direct pushes, logged self-review; "Security-sensitive changes require additional security champion review" → identified in PR description, independent review by external auditor; dropped "Dismiss stale reviews on new commits" (reviewer-dependent setting); required status checks named (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog).
- R4: §5.2.1 table — Python validation "Bandit security linter" → "Black, isort, Flake8 and Bandit in GitHub Actions"; CloudFormation validation "cfn-lint, cfn-nag" → CloudFormation as only change path + Security Hub configuration checks; Container "ECR vulnerability scanning" → "ECR scan-on-push; Trivy in GitHub Actions"; Node.js "ESLint security rules" → `[CONFIRM]` placeholder.
- R5: §5.2.3 dependency clocks — "Critical within 7 days" → dependency CVEs rated critical 7 days, actively exploited critical 24 hours; High 30 days; added Medium 90 days.
- R4: §5.3.1 removed the DAST row (OWASP ZAP); SAST tools → "Bandit and TruffleHog in GitHub Actions"; Dependency scanning "Daily / Dependabot, npm audit" → "Continuous / GitHub Dependabot and code scanning"; Container → ECR scan-on-push + Trivy.
- R2: §5.4.2 "Code review approved by authorized reviewer" → PR merged with required CI checks passing and self-review recorded.
- R5: §5.5.1 patch clocks — Critical 48 h → 24 h (exploited/critical), added critical dependency CVEs 7 days; High 7 d → 30 d; Medium 30 d → 90 d; Low 90 d → best effort.
- R5: §5.5.2 "reviewed daily" → reviewed monthly (recorded) with real-time SNS alerting for critical findings.
- R0: §6.1 removed the duplicated table header; Dependabot "Daily scans" → "Continuous scans"; GitHub Actions purpose names the CI set.
- R4: §6.1 "CloudFormation Guard | IaC security validation | Pre-deployment" → "CloudFormation (Serverless Framework) | only change path, reports drift | Deployment".
- R4: §6.2 "EventBridge rules for security alert routing" → "The breach-detection Lambda that routes Security Hub findings to SNS".
- R4: §7 "Initial secure coding training within 30 days of access grant" and "Annual security awareness training" → security awareness training in the compliance platform portal at onboarding and annually; run-on "Program OWASP Top 10" split into separate bullets.
- R7: §8.2 and §11 "Third-Party Integration Security Guidelines" → Integration security section of the API Security and Rate Limiting Standard; reference removed from Related Documents.
- R5: §9.2 KPI thresholds "> 48 hours" → "> 24 hours", "High > 7 days" → "> 30 days"; "Code review coverage 100%" → "Pull requests merged with passing CI status checks 100%".
- R4: §9.2 removed "Security test automation coverage > 80%" row.
- R8: restored bullet lists collapsed into run-on sentences in §5.1.2, §8.1, §8.2, §9.1, §9.3, §10; removed `<u>` underline artefacts.

## CONFIRM

- §5.2.1 Node.js/TypeScript row: is there any Node/TypeScript code in `di-backend-api` or the frontend, and is ESLint run anywhere? If not, delete the row.
- §5.2.1 CloudFormation row: v1 cited cfn-lint / cfn-nag; replaced with CloudFormation + Security Hub checks. Confirm neither tool is actually in CI.
- §4.1 keeps the name "Mo Messidi" as in v1; confirm whether v2 documents should name the CEO or use the title only.
- §5.4.1 "approved via the GitHub Actions workflow": confirm a manual approval gate (environment protection rule) exists on the production deploy job; otherwise reduce to "deployed from a green CI run on `main`".
- §5.5.2 "Container vulnerability scans shall be reviewed weekly" kept from v1 — confirm this cadence is actually recorded.
- R3 staging: separate account vs same account (not written into the policy).
