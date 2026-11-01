# Encryption and Cryptographic Controls Standard — v1.0 → v2.0 change note

Source: `data/nov2025/md/encryption-and-cryptographic-controls-standard.md`
Output: `policies-v2/encryption-and-cryptographic-controls-standard.md`

## Frontmatter
- R0: `version` 1.0 → 2.0; `supersedes: "1.0"`; `effective_date` → `"<to be set at publication>"`; `review_date` → `"<one year after effective date>"`; `doc_type` "Policy" → "Standard"; dropped export-only `finalized_at` (R6). Kept `author`, `source`, `acknowledgment`.
- R0: "## 3.1"-style sub-headings corrected to "### 3.1"; section numbers unchanged.

## Removals / rewordings / additions
- R2/R5: §17.1 "Chief Information Security Officer approval" → "CEO approval".
- R3: §6.2 Database Credentials method "AWS Secrets Manager" → "AWS Secrets Manager rotation on the DocumentDB credential"; API Keys method adds "per the rotation calendar". Frequencies unchanged (annual / 90 days / 180 days / annual / quarterly).
- R3: §4.4 "Image scanning for vulnerabilities before deployment" → "Scan-on-push vulnerability scanning on all repositories, with critical findings remediated before deployment".
- R3: §10.2 "Test encryption in staging environment" → "in the staging stage". §13.1 "Tested quarterly for restoration capability" tied to the quarterly backup-restore test (automated, recorded in the compliance platform).
- R4 (EBS): §2 removed "and EBS volumes".
- R4 (load balancers): §3.1 Key Exchange implementation "ALB/CloudFront negotiation" → "CloudFront negotiation".
- R4 (cross-region replication): §4.2 removed "Cross-region replication with encryption in transit and at rest". §6.1 removed "Cross-Region Replication Key".
- R4 (image signing): §4.4 "Signed container images for Fargate deployments" → "Images built and pushed only from a green GitHub Actions CI run (including Trivy image scanning)".
- R4 (certificate pinning): §5.1 "Certificate pinning for critical third-party integrations" → "AWS Certificate Manager-managed certificates for all public endpoints".
- R4 (PrivateLink / Transit Gateway / multi-region): §5.2 "PrivateLink for third-party service integration" and "Transit Gateway encryption for cross-region traffic" → "A single VPC in a single region (us-east-1); encryption at rest uses a KMS regional customer-managed key with annual rotation". §4.1 CMK bullet annotated "(regional, us-east-1)".
- R4 (multi-region KMS keys): §13.1 "Backed up to separate AWS regions using KMS multi-region keys" → "Held in AWS KMS as regional customer-managed keys in us-east-1; key material does not leave KMS".
- AZ-vs-region error fixed (R4 multi-region row / R0 correctness): §13.2 "Maintain key replicas in us-east-1b for us-east-1a failures" and "Implement automated failover for KMS endpoints" → "AWS KMS is a regional service; keys remain available across all availability zones in us-east-1 (including us-east-1a and us-east-1b) without replication". "Ensure backup restoration includes encryption keys" → "Ensure backup restoration uses the same KMS keys that encrypted the backups" (consistent with §4.1).
- Staging key claims (caller note): §6.3 "Separate keys for development, staging, and production environments" → "The staging stage uses its own key, separate from production"; the same sentence added under §6.1. No development-environment key claimed.
- §6.1 "AWS KMS Key Hierarchy" → "AWS KMS Keys": the broken `<mark>`/code-block tree rendered as one clean code block; dropped the fictitious "Root Account KMS Key (Restricted Access)" root node (KMS has no such hierarchy; remaining key list is v1's). Lead sentence now states the keys are maintained in us-east-1.
- R4 (ECR-only scanning): §11.2 "Identified through ECR container scanning" → "ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI".
- R5: §16.1 "Quarterly automated compliance scans via Security Hub" → "Continuous Security Hub checks, reviewed monthly and recorded in the compliance platform".
- R5: §12.1 step 5 "Notify customers within 48 hours" → "Notify affected customers within 48 hours" (matches the 48-hour customer notification value).
- R7: §8.2 reference "Third-Party Integration Security Guidelines" → "API Security and Rate Limiting Standard (Integration security) and Vendor Management Policy"; §18 entry for the Guidelines removed.
- Factual wording: §2 "JWT token encryption for PropelAuth" → "JWT token signing and validation for PropelAuth" (JWTs are signed, RS256, per §8.1; v1's own table calls it "JWT token validation").
- R8: restored real bullet lists (§2, §4.1, §4.2, §4.4, §9.2, §13.1, §15.1, §17.2); split run-on bullets in §5.3, §6.3, §7.1, §13.1, §13.2, §15.1; removed stray `<u>` fragments; §3.1 "Customer Master Keys (CMK)" → "customer-managed keys (CMK)" (current AWS term; same meaning).
- R6: §18 split the merged items ("Access Control … Cloud Infrastructure Security Policy", "Change Management Policy Vulnerability Management Procedure", "Penetration Testing … Data Retention and Disposal Policy").
- R0: added §20 Revision history.
- Kept verbatim (no rule applies): §1, §3.2, §4.3 (quarterly rotation of Lambda env-var secrets), §5.1 HSTS, §5.2 VPC endpoints, §7, §8.1, §9.1, §10.1, §11.1 (monthly TLS scans, quarterly encryption audit reports), §12.2, §14, §16.1 semi-annual key rotation audits, §16.2, §17.2, §19.

## CONFIRM
- [CONFIRM: KMS key inventory] — §6.1 keeps v1's key list (Production Data key with DocumentDB/S3/Lambda sub-keys, Backup key, Audit Log key). Confirm which customer-managed keys actually exist in us-east-1 and whether backups use the DocumentDB key (as §4.1 states) rather than a separate Backup key.
- [CONFIRM: JWT signing key rotation 180 days] — v1 claim about PropelAuth; cannot be verified from the environment. Consider "Managed by PropelAuth" without a number.
- [CONFIRM: Lambda env-var secrets rotated quarterly] — §4.3 kept from v1; not among the R3/R5 rotation facts.
- [CONFIRM: monthly TLS configuration scans / quarterly encryption audit reports / semi-annual key rotation audits] — §11.1 and §16.1 kept from v1; confirm these are evidenced in the compliance platform.
- [CONFIRM: VPC endpoints] — §5.2 "VPC endpoints for AWS service communications" kept from v1; confirm endpoints exist in the stack.
- [CONFIRM: separate account vs same account] — staging described only as "the staging stage" per R3.
