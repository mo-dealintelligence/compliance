# api-security-and-rate-limiting-standard — v1.0 → v2.0 change note

- R0: frontmatter `doc_type` Policy → Standard; `version` 1.0 → 2.0; `supersedes: "1.0"` added; `effective_date` / `review_date` set to placeholders; `finalized_at` dropped (v1 finalization timestamp does not apply to v2); "Revision history" section added.
- R1: removed "PI1.4 (Processing Integrity)" from §1 Purpose and the "PI1.4: Input validation maintains processing integrity" line from §12.1 (was §11.1).
- R8: run-on "applies to: - …" lists in §2, §3.x, §4.x, §5.x, §6.x, §7.x, §8/9.x, §10–14 restored as real bullet lists; `<u>` underline artefacts removed from cross-references; "900second" → "900-second"; "X- RateLimit-Limit" → "X-RateLimit-Limit"; "Deprecation\n\nwarnings" line break fixed.
- R4: §2 Scope — removed "WebSocket connections for real-time data streaming"; added the integration scope bullets from the merged Guidelines (customer CRM/Slack integrations, webhook/EventBridge endpoints, OAuth 2.0/JWT flows).
- Brief / R0: §3.3 "SQL injection prevention through parameterized queries in DocumentDB" → "NoSQL injection prevention through input validation and typed, parameterized query construction for DocumentDB".
- R4: §4.1 four-tier table (Standard/Premium/Public/Admin) → single tier: 100 requests/minute per API key, burst 200, all authenticated API calls. Heading "Rate Limiting Tiers" → "Rate Limiting Tier".
- R4: §4.2 "API Gateway Throttling — usage plans configured per customer tier" → "Application Rate Limiting — one rate tier of 100 requests per minute per API key, enforced in application middleware"; "Dead letter queues for throttled requests" removed from Lambda Concurrency Controls.
- R5: §5.2 added "p95" to the percentile list and "CloudWatch alarm when p95 latency exceeds 2 seconds".
- R5: §5.3 "Weekly API security posture reviews" removed; Security Hub bullet reworded to "reviewed monthly and recorded in the compliance platform; critical findings alert in real time via SNS".
- R7: §7.2 reference to the Third-Party Integration Security Guidelines → "integration security requirements in section 8 of this standard".
- R7: new §8 "Integration Security" (8.1–8.9) carrying the webhook/OAuth/integration-pattern content of the Guidelines (purpose/policy statement, authentication standards, credential management, data exchange security, approved patterns table, prohibited practices, customer-controlled CRM/Slack integrations, monitoring table and audit logging, security testing and vulnerability management, lifecycle management, GDPR/CCPA/OWASP ASVS and data-subject-rights support). Subsequent sections renumbered 8→9 … 14→15. Within the merged content:
  - R2: Guidelines §4 roles (CEO / Technical Integration Lead / Security Operations) consolidated into one CEO paragraph in the §8 intro.
  - R4: "Service-to-Service: Mutual TLS where supported" → "TLS 1.2 or higher with ACM-managed certificates"; "Certificate pinning for critical integrations" → "ACM-managed certificates for all Deal Intelligence endpoints".
  - R4: EventBridge row "DLQ for failures" → "CloudWatch logging and alarms on failed invocations".
  - R5: monitoring table "Response Time >5 seconds p95" → ">2 seconds p95"; "Certificate Expiry … Lambda notification" → "CloudWatch alarm" (matches §3.2 "certificate expiration monitoring via CloudWatch").
  - R4: "Quarterly automated security scans of integration endpoints" (DAST-type) → "Continuous dependency and code scanning … via GitHub Dependabot, GitHub code scanning, and Bandit, Trivy and TruffleHog in CI".
  - R5: vulnerability timelines "Critical 24 hours / High 7 days" → critical 24 hours (exploited/critical), dependency CVEs rated critical 7 days, high 30 days.
  - R5: operational phase "Monthly security posture reviews" → "Monthly review of Security Hub findings affecting integrations"; "Quarterly access and permission audits" → "reviews"; annual vendor reassessment now references Vendor Management Policy.
  - R4: "Legal hold implementation if required" (third-party breach response) dropped; "Consent management for optional integrations" kept (no reference to a Consent Management Procedure).
  - Pre-integration assessment table, DPA requirements and sub-processor statements went to Vendor Management Policy v2 (see that change note and the MERGED note).
- R4: §9.1 (was 8.1) "Dynamic application security testing (DAST) before production deployment" removed; SAST line now names the GitHub Actions CI tools (Bandit, Trivy, TruffleHog).
- R2: §9.1 "Security code reviews for authentication and authorization logic" → "Pull request with required CI status checks on the protected `main` branch, with a logged self-review of authentication and authorization logic in the PR".
- R4: §9.2 "Unit tests with minimum 80% code coverage" → "Unit tests (pytest) executed as a required CI status check, alongside Black, isort and Flake8".
- R4: §10.1 "Rate limiting thresholds and tiers" → "Rate limiting threshold".
- R7: §11.1 added incident type "Security incidents involving third-party integrations or a breach at a third-party service"; §11.2 steps extended with isolation of the affected integration, credential rotation, vendor involvement and vendor re-assessment (from Guidelines §9).
- R5: §11.2 "Impact assessment within 4 hours" → "within 4 business hours" (aligns with the P1 acknowledgement target).
- R5: §13.1 "95th percentile latency under 500ms" → "under 2 seconds" (one latency value, matching the p95 > 2 s alert).
- R4: §13.2 "API Gateway throttling statistics" → "Rate limiting (HTTP 429) statistics"; "Customer tier distribution" removed (no tiers).
- R7: §14 Related Documents — "Third-Party Integration Security Guidelines" removed; Vendor Management Policy, Penetration Testing and Security Assessment Procedure and Data Subject Rights Request Procedure added (all now referenced in the body).
- R2: §15 "automated notifications to the responsible party" → "to the CEO".

## CONFIRM

- API Gateway vs Lambda function URLs: v1 states token validation, JSON schema validation and configuration logging "at API Gateway level"; the R4 WAF row says origin access is restricted to "the Lambda function URLs". v1 API Gateway wording kept unchanged; confirm which front door is in production and whether API Gateway wording should become Lambda function URLs.
- Burst capacity of 200 (2x sustained) retained from v1 for the single tier; confirm the middleware actually implements a burst allowance, otherwise drop the Burst Capacity column and the "2x" bullet.
- "Provisioned concurrency for critical endpoints" (§4.2) and "Failover to cached JWT validation during PropelAuth outages" (§7.1) retained from v1 — not in the R4 removal list; confirm they exist.
- §13.1 SLO latency changed from 500 ms to 2 s to match the single R5 value; confirm the intended p95 objective.
- Section renumbering (new §8 pushes v1 §8–14 to §9–15): other v2 documents that cite this standard by section number should be checked.

## Quality sweep (2026-10-31)

- Q1 voice: "shall" removed throughout (23 occurrences → present tense "implements / is enforced / follows"); §1 tightened ("establishes mandatory requirements… ensures the protection of… operationalizes" → plain statements); §8 intro paragraph 2 rewritten without "defense-in-depth", "comprehensive audit logging", "utilize" (same four commitments kept: assessment before implementation, encrypted channels, authn/authz, audit logging, company-level isolation); §8 CEO responsibilities turned from a seven-clause sentence into a bullet list; "comprehensive validation/testing" → "validated" / "the following testing is required"; "adequate customer notice" → "provides customers with"; §15 "shall be reviewed… automated notifications" → "is reviewed… the compliance platform notifies the CEO".
- Q2 names: "AWS Certificate Manager" → "ACM"; "AWS Secrets Manager" → "Secrets Manager" ×3; "AWS Security Hub" → "Security Hub"; "SOC 2 Trust Service Criteria" → "Trust Services Criteria"; "95th percentile latency" → "p95 latency"; table "Response Time >2 seconds p95" → "p95 > 2 seconds".
- Q2 numbers: "10MB" → "10 MB", "1GB" → "1 GB", percentages spaced ("99.9 %", "0.1 %", "5 %", ">5 %"); "Minimum 90-day deprecation notice" → "Minimum 90 days' deprecation notice".
- Q2 headings: all headings to sentence case; table headers to sentence case; unnumbered "## Revision history" → "## 16. Revision history".
- Q2 lists: §4.3 lead-in made a sentence ("the API returns:"); §5.3 "Integration with incident response procedures defined in Incident Response Procedure" → "The Incident Response Procedure for confirmed security events"; §8.8 "Audit log preservation per retention policy" → "per the Data Retention and Disposal Policy" (real title); "the" added before document titles where missing (×14).
- Q3 structure: §12 "Compliance and Regulatory Requirements" — §12.1 SOC 2 mapping (CC6.1, CC6.6, CC7.1, A1.2) merged into §1; §12.2 kept as §12 "Data protection requirements"; §15 "Review and Updates" → §14 "Review", Related documents → §15 (Data Retention and Disposal Policy added, since §8.6 and §8.8 cite it), Revision history → §16.
- No commitment, number, role, scope item or control changed.

### CONFIRM (new)

- "AWS API Gateway" is named 8 times (§2, §3.1 token validation "at API Gateway level", §3.3 JSON schema validation, §5.3, §8.1, §8.4, §11.2). The rulebook (R4) describes the edge as CloudFront with origin access restricted to Lambda function URLs, and the Penetration Testing procedure v2 replaced "API Gateway security configurations" with "CloudFront and Lambda function URL". Confirm whether API Gateway is actually deployed; if not, these claims need restating (left unchanged — would change the control).
- §7 "Third-party API integration security" (PropelAuth, customer-controlled integrations) overlaps §8.5 "Customer-controlled integrations" after the R7 merge. Confirm whether §7.2 should be folded into §8.5 (left as is — both lists carry distinct commitments).

- R4/Q2 (post-sweep, settled from serverless.yml: 'API Gateway not used - using Lambda Function URL + CloudFront'): every 'API Gateway' reference replaced with CloudFront → Lambda function URL / middleware.

## Decisions applied (2026-10-31)

- D8: §11.2 removed the "impact assessment within 4 business hours" triage clock (steps renumbered)
- D22: author set to Mo Messidi (frontmatter and revision history)
- D25: cut §3.2 "monthly" certificate expiration monitoring (CloudWatch monitoring kept, no cadence); §8 integration access review folded into the quarterly access review; cut §8.2 quarterly credential rotation; deleted §13.2 quarterly capacity reviews (§13 now a single section)

## Decisions applied (2026-10-31, round 2)

- D12: Security Hub removed. §1 CC7.1 mapping now "CloudWatch, the monthly configuration-check Lambda, and CloudTrail event alerting"; §5.3 Security monitoring: the "Security Hub findings for API vulnerabilities, reviewed monthly" bullet replaced by the monthly configuration-check Lambda record (public-S3 and open-security-group checklist items named), the CloudTrail-EventBridge → breach-detection Lambda → SNS real-time alert, and the unchanged vulnerability-awareness stack (ECR scan-on-push, Dependabot, code scanning, Trivy); §7 alert table "Authentication failures → Security Hub finding" → "CloudWatch alarm" (Security Hub never emitted that signal; CloudWatch alarm is the same mechanism as the response-time row — [CONFIRM: alarm exists]); §8 operational-phase bullet "Monthly review of Security Hub findings affecting integrations" deleted — the configuration checklist has no integration-specific item, so there is no replacement record (D25 logic); revision-history summary reworded.
- D13b: §13 "99.9 % API availability, measured monthly" now points to the SLA Management Policy's measurement rule and the monthly availability record (the compliance-platform task is defined there).
- D11b, D14: no insurance or controller/processor text in this document; nothing to apply.
