# Cloud Infrastructure Security Policy — v1.0 → v2.0 change note

Source: `data/nov2025/md/cloud-infrastructure-security-policy.md`
Output: `policies-v2/cloud-infrastructure-security-policy.md`

## Frontmatter
- R0: `version` 1.0 → 2.0; added `supersedes: "1.0"`; `effective_date` → `"<to be set at publication>"`; `review_date` → `"<one year after effective date>"`; dropped the export-only `finalized_at` field (R6 export leftover). Kept `author`, `source`, `acknowledgment`, `doc_type: Policy`.

## Removals / rewordings / additions
- R1: §2 "five Trust Services Criteria … Security, Availability, Processing Integrity, Confidentiality, and Privacy" → "Security, Availability and Confidentiality".
- R1: §6.1 removed the Processing Integrity and Privacy bullets; split the collapsed "Processing Integrity … **Confidentiality**" line so Confidentiality stands alone.
- R2: §4 roles "Infrastructure Administrator", "Security Administrator", "DevOps Engineer" → single §4.1 CEO (all v1 bullets merged; "Coordinate with the Security Lead defined in the Information Security Policy" dropped; "Support incident response activities" → "Lead incident response activities" since the CEO is incident commander). Added §4.2 Go-to-Market Contractor (no infrastructure access) and §4.3 External Parties (auditor, penetration-test vendor) per the R2 role set.
- R2: §7.2 "Escalation to executive leadership" → "Escalation to the CEO".
- R2/R5: §7.3 exception approver "Security Lead" → CEO.
- R2/R3: §5.7.1 "Change approval process for production deployments" → pull request with required CI status checks on protected `main`; deploy only from a green CI run (compensating control).
- R3: §5.7.1 "Staging environment validation before production" → "Validation in a staging stage of the same CloudFormation stack, containing no production data, before production". No account language.
- R3: §5.1.2 DocumentDB bullet now states Multi-AZ (second instance in another AZ) explicitly.
- R3: §5.2.2 Secrets Manager bullet adds "Secrets Manager rotation enabled on the DocumentDB credential".
- R3: §5.3.1 "Vulnerability scanning enabled in Amazon ECR for all images" → "Scan-on-push vulnerability scanning enabled in Amazon ECR for all repositories".
- R3: §5.6.2 quarterly restore test annotated "(automated, recorded in the compliance platform)"; run-on "RTO/RPO Quarterly backup restoration testing" split into two bullets.
- R3: §7.1 "Annual third-party infrastructure security assessment" → "Annual third-party penetration test".
- R4 (WAF): §5.4.2 "WAF rules for common attack pattern blocking" → "CloudFront with AWS Shield Standard, TLS 1.2+, and origin access restricted to the Lambda function URLs"; rate-limit bullet now says "enforced in middleware".
- R4 (GuardDuty): §5.5.2 "GuardDuty for threat detection" → Security Hub (Foundational Security Best Practices) + CloudTrail + the breach-detection Lambda routing findings to SNS.
- R4 (Config): §5.5.2 "Config Rules for compliance monitoring" → Security Hub configuration checks + scheduled Lambda checks (access review, retention enforcement). §5.7.2 "Configuration drift detection through AWS Config" → "CloudFormation (`serverless deploy`) is the only change path and reports configuration drift"; "Automated remediation for non-compliant resources" → "Security Hub configuration checks and scheduled Lambda checks for non-compliant resources". §7.1 "Quarterly compliance assessments through AWS Config Rules" → monthly Security Hub findings review recorded in the compliance platform (R5).
- R4 (EC2/EBS/Inspector): §5.1.3 removed "Encrypted EBS volumes for EC2 instances". §5.1.1 "Public subnets only for load balancers and NAT gateways" → "Public subnets only for the NAT instance, which is accessed exclusively via SSM Session Manager (no key-based shell access, no public services)". §5.8 "Automated vulnerability scanning for container images" → ECR scan-on-push, GitHub Dependabot and code scanning, Trivy in CI.
- R4 (image signing): §5.3.1 "Image signing for production deployments" → "Images built and pushed to ECR only from a green GitHub Actions CI run (including Trivy image scanning)".
- R4 (Transit Gateway/PrivateLink/multi-region): v1 contained no Transit Gateway, PrivateLink, VPC peering or cross-region text in this document; §5.1.1 now states "a single Virtual Private Cloud (VPC) in us-east-1" and §5.1.2 adds "The platform operates in a single AWS region (us-east-1) by design, as stated in the Business Continuity Plan" (R4 Route 53/multi-region row, R8 region).
- R4 (load balancers / auto-scaling / DLQs): §5.1.2 "Load balancing for containerized services" → "Lambda versioned deployments with reserved concurrency and rollback via `serverless rollback`". §5.4.1 "Dead letter queues for failed invocation handling" → "Versioned deployments with rollback via `serverless rollback`". §5.7.1 "Automated rollback capabilities" → "Rollback via `serverless rollback`".
- R4 (runbooks maintained separately): §5.6.2 "Disaster recovery runbooks maintained in the Business Continuity Plans module in the compliance platform" → "Disaster recovery procedures documented in the Business Continuity Plan".
- R5: §5.5.1 "90-day retention period for all log data" → "90-day retention period for CloudWatch Logs" + "CloudTrail logs retained 7 years in S3 (lifecycle to Glacier, Object Lock)" (also R3).
- R5: §5.5.2 added "SNS notifications for critical findings in real time; all Security Hub findings reviewed monthly and the review recorded in the compliance platform" (replaces "SNS notifications for critical alerts").
- R5: §5.5.3 "API Gateway latency and error rates" → "API latency (alert at p95 > 2 seconds) and error rates".
- R8: §5.7.1 infra-as-code wording now "CloudFormation templates (deployed via the Serverless Framework)" and "Version control … in the `dealintelligence/di-backend-api` repository".
- R8: §9 "documented in the Business Continuity Plans module in the compliance platform" → "recorded in the compliance platform".
- R8: restored real bullet lists where v1 collapsed them (§2 first two items, §5.1.3, §5.2.2, §5.4.1, §5.5.3, §6.2, §5.7.2); removed stray `<u>` underline fragments and the mid-sentence "Policy:" line break in §5.1.2/§5.1.3.
- R6: §8 Related Documents — split the merged "SLA Management Policy Data Retention and Disposal Policy" item into two entries.
- R0: added §10 Revision history.
- Kept verbatim (no rule applies): §1, §3 definitions, §5.2.1, §5.2.3, §5.3.2, §5.4.1 reserved concurrency 100 / 900 s timeout, §5.5.3 other metrics, §5.6.1, §5.9 (incl. "Participation in AWS Well-Architected reviews"), §6.2 content, §7.2 other bullets, §9 bullets.

## CONFIRM
- [CONFIRM: API Gateway vs Lambda function URLs] — v1 §5.4.2 heading "API Gateway Security" and the R4-mandated WAF replacement text "origin access restricted to the Lambda function URLs" now sit in the same section. Heading kept as v1 (API Gateway itself is not in the R4 removal list). Confirm which is in the stack and align the heading/wording.
- [CONFIRM: separate account vs same account] — staging stage described without any account language per R3.
- [CONFIRM: VPC Flow Logs, DocumentDB audit logging, ECS network policies, AWS Well-Architected reviews] — kept verbatim from v1 because no rule removes them; worth checking they are actually enabled.
