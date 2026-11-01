---
title: "Encryption and Cryptographic Controls Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "encryption-and-cryptographic-controls-standard-v1.0.pdf"
---

# Encryption and Cryptographic Controls Standard

## 1. Purpose

This standard sets the mandatory cryptographic controls that protect the information assets of Deal Intelligence LLC. It protects the confidentiality, integrity, and authenticity of business contact information, customer data, and market intelligence throughout their lifecycle, in line with SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls) and C1.1 (Confidentiality).

It implements the encryption requirements of the Information Security Policy for KMS encryption, TLS, and key management across the AWS infrastructure.

## 2. Scope

This standard applies to:

- All data at rest in the AWS infrastructure, including DocumentDB collections and S3 buckets
- All data in transit between system components, APIs, and third-party services
- Cryptographic key generation, storage, rotation, and destruction
- Certificate management for CloudFront distributions and API endpoints
- JWT token signing and validation for PropelAuth authentication
- All personnel responsible for implementing or maintaining cryptographic controls

## 3. Roles and responsibilities

- **Chief Executive Officer (CEO)**: owns this standard; configures and maintains the KMS keys, certificates, and encryption settings; approves exceptions; performs the reviews and audits in §12 and §17
- **Go-to-Market Contractor**: has no access to keys, certificates, or production systems; reports suspected cryptographic issues to the CEO
- **External SOC 2 auditor and penetration-test vendor**: independently review the cryptographic controls and evidence

## 4. Cryptographic requirements

### 4.1 Encryption standards

All cryptographic implementations meet or exceed these minimums:

|**Data state**|**Minimum standard**|**Implementation**|
|---|---|---|
|Data at rest|AES-256-GCM|KMS customer-managed keys (CMK)|
|Data in transit|TLS 1.2+|ACM, CloudFront|
|Key exchange|RSA-2048 or ECDHE|CloudFront negotiation|
|Hashing|SHA-256|Lambda function integrity checks|
|Digital signatures|RSA-2048 with SHA-256|JWT token validation|

### 4.2 Prohibited algorithms

- DES and 3DES (all variants)
- MD5 and SHA-1 for security purposes
- RC4
- TLS versions before 1.2
- RSA keys smaller than 2048 bits

## 5. Encryption at rest

### 5.1 DocumentDB

All DocumentDB clusters have:

- KMS encryption enabled at cluster creation
- A customer-managed CMK (regional, us-east-1) with automatic annual rotation
- Automated backups encrypted with the same CMK
- Audit logging of all KMS key usage via CloudTrail

Encryption follows the classification tiers in the Data Classification and Handling Standard.

### 5.2 S3 buckets

All S3 buckets enforce:

- Default encryption with SSE-KMS and customer-managed keys
- Bucket policies that deny unencrypted object uploads
- Versioning, with every object version encrypted

### 5.3 Lambda environment variables

Sensitive configuration in Lambda functions is:

- Encrypted with KMS customer-managed keys
- Decrypted at runtime through IAM role permissions
- Rotated quarterly, in line with the Access Control and Authentication Policy

### 5.4 Container images

ECR repositories have:

- Encryption at rest with KMS
- Scan-on-push vulnerability scanning on all repositories, with critical findings remediated before deployment
- Images built and pushed only from a green GitHub Actions CI run (including Trivy image scanning)

## 6. Encryption in transit

### 6.1 API communications

All API endpoints enforce:

- TLS 1.2 minimum, TLS 1.3 preferred
- Certificate validation for all HTTPS connections
- HSTS headers with a minimum 1-year max-age
- ACM-managed certificates for all public endpoints

See the API Security and Rate Limiting Standard.

### 6.2 VPC communications

Internal VPC traffic uses:

- A single VPC in a single region (us-east-1); encryption at rest uses a KMS regional customer-managed key with annual rotation
- Security groups that restrict protocols to encrypted variants only

See the Cloud Infrastructure Security Policy.

### 6.3 CloudFront distributions

- Viewer protocol policy set to "Redirect HTTP to HTTPS"
- Origin protocol policy HTTPS only
- ACM certificates with automatic renewal
- Custom SSL certificate for branded domains

## 7. Key management

### 7.1 KMS keys

The following customer-managed KMS keys are maintained in us-east-1:

```
Production Data Encryption Key
├── DocumentDB Encryption Key
├── S3 Bucket Encryption Key
└── Lambda Environment Variable Key
Backup Encryption Key
Audit Log Encryption Key
└── CloudTrail/CloudWatch Logs Key
```

The staging environment uses its own key in the staging AWS account, separate from production.

### 7.2 Key rotation

|**Key type**|**Rotation frequency**|**Method**|
|---|---|---|
|KMS CMK|Annual|Automatic via KMS|
|API keys|90 days|Manual with overlap period, per the rotation calendar|
|JWT signing keys|180 days|PropelAuth managed|
|TLS certificates|Annual|ACM|
|Database credentials|Quarterly|Secrets Manager rotation on the DocumentDB credential|

### 7.3 Key access controls

Key access follows least privilege:

- Production keys are accessible only to production Lambda execution roles
- CloudTrail logs all key usage operations
- Quarterly access reviews are recorded in the risk assessment module of the compliance platform

See the Access Control and Authentication Policy.

## 8. Certificate management

### 8.1 Certificate lifecycle

All TLS certificates are:

- Issued by ACM or an approved Certificate Authority
- Validated by DNS validation
- Monitored for expiration, with 30-day advance alerts via CloudWatch
- Renewed automatically where the issuer supports it

### 8.2 Certificate requirements

Production certificates:

- Use 2048-bit RSA keys minimum or ECDSA P-256
- Include the complete certificate chain
- Implement OCSP stapling where the endpoint supports it
- Are not wildcard certificates for API endpoints

## 9. Authentication token security

### 9.1 JWT tokens

PropelAuth JWT tokens use:

- RS256 for signature verification
- Token expiration of no more than 24 hours
- Refresh token rotation on each use
- httpOnly cookies for storage where the client supports them

### 9.2 API keys

API keys for third-party integrations are:

- Stored encrypted in Secrets Manager
- Rotated on the schedule in §7.2
- Monitored for unauthorized usage patterns
- Revoked immediately on detection of suspicious activity

See the API Security and Rate Limiting Standard (Integration security) and the Vendor Management Policy.

## 10. Cryptographic compliance

### 10.1 Regulatory requirements

Cryptographic implementations comply with:

- GDPR Article 32 (appropriate technical measures)
- CCPA Section 1798.150 (reasonable security procedures)
- SOC 2 CC6.1 (logical access controls)
- NIST SP 800-175B

### 10.2 Export control

All cryptographic implementations:

- Comply with the U.S. Export Administration Regulations
- Are documented for compliance reporting
- Restrict strong encryption to authorized jurisdictions

## 11. Implementation procedures

### 11.1 New system deployment

1. Enable encryption by default in the CloudFormation templates
2. Configure KMS key policies before data ingestion
3. Validate the TLS configuration with SSL Labs or an equivalent tool
4. Document the encryption configuration in the system inventory

### 11.2 Encryption upgrades

For systems that need an encryption upgrade:

1. Assess the current encryption status from the latest monthly configuration-check record and the AWS console
2. Plan the migration for a maintenance window
3. Test the encryption in the staging environment
4. Implement with rollback procedures per the Change Management Policy

## 12. Monitoring and validation

### 12.1 Continuous monitoring

Encryption compliance is monitored through:

- The monthly configuration-check Lambda, whose fixed checklist includes KMS key rotation and CloudTrail log-file validation, with a dated pass/fail record posted to the compliance platform
- KMS key disable events in CloudTrail trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- CloudWatch alarms on KMS key deletion attempts

See the System Monitoring and Logging Procedure.

### 12.2 Cryptographic vulnerabilities

Cryptographic vulnerabilities are:

- Identified through ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI
- Assessed with CVSS scoring
- Remediated per the Vulnerability Management Procedure
- Tracked in the risk assessment module of the compliance platform

## 13. Incident response

### 13.1 Cryptographic incidents

On cryptographic compromise, the CEO:

1. Immediately revokes the affected keys or certificates
2. Generates new cryptographic material
3. Re-encrypts the affected data with the new keys
4. Records the incident in the incident reporting module of the compliance platform
5. Notifies affected customers within 48 hours if data confidentiality is affected

See the Incident Response Procedure.

### 13.2 Key compromise

On suspected key compromise, the CEO:

- Rotates the affected keys immediately
- Reviews CloudTrail logs for unauthorized key usage
- Updates all systems that used the compromised keys
- Conducts forensic analysis of potential data exposure

## 14. Backup and recovery

### 14.1 Key backup

Cryptographic material is:

- Held in KMS as regional customer-managed keys in us-east-1; key material does not leave KMS
- Protected with equivalent encryption standards
- Tested quarterly for restoration as part of the quarterly backup-restore test (automated, recorded in the compliance platform)
- Documented in the Business Continuity Plan

### 14.2 Disaster recovery

- KMS is a regional service; keys remain available across all availability zones in us-east-1 (including us-east-1a and us-east-1b) without replication
- Backup restoration uses the same KMS keys that encrypted the backups
- Encryption is validated after recovery

## 15. Third-party encryption

### 15.1 Vendor requirements

All vendors processing Deal Intelligence data:

- Implement AES-256 encryption for data at rest
- Use TLS 1.2+ for data transmission
- Provide encryption attestation in their SOC 2 reports
- Comply with the Vendor Management Policy

### 15.2 Customer-controlled integrations

For customer-managed integrations, Deal Intelligence:

- Provides encryption guidance documentation
- Supports encrypted API communications
- Enables audit logging of integration activity
- Maintains encryption throughout the data pipeline

## 16. Training

Personnel implementing cryptographic controls complete annual security awareness training on encryption through the Security Awareness Training Program, understand their key management responsibilities, follow secure coding practices for cryptographic implementations, and report cryptographic vulnerabilities immediately.

## 17. Compliance verification

### 17.1 Assessments

- Annual penetration testing of TLS implementations (see the Penetration Testing and Security Assessment Procedure)
- Monthly configuration-check record (KMS key rotation) in the compliance platform
- Continuous monitoring via CloudWatch metrics

### 17.2 Audit evidence

- KMS key rotation logs in CloudTrail
- Certificate issuance and renewal records
- Encryption configuration screenshots
- Monthly configuration-check records

## 18. Exceptions and review

### 18.1 Exceptions

A deviation from this standard requires:

- Documented business justification
- A risk assessment in the risk assessment module of the compliance platform
- Defined compensating controls
- CEO approval

### 18.2 Legacy system exceptions

A legacy system that cannot meet this standard is:

- Documented in the risk register
- Covered by compensating controls
- Given a migration timeline
- Isolated from production data where possible

### 18.3 Review

The CEO reviews this standard annually and updates it for:

- Changes in cryptographic best practices
- New regulatory requirements
- Emerging cryptographic vulnerabilities
- Updates to AWS encryption services
- Findings from security assessments and audits

## 19. Related documents

- Information Security Policy
- Data Classification and Handling Standard
- Access Control and Authentication Policy
- Cloud Infrastructure Security Policy
- API Security and Rate Limiting Standard
- Vendor Management Policy
- Incident Response Procedure
- Business Continuity Plan
- Change Management Policy
- Vulnerability Management Procedure
- System Monitoring and Logging Procedure
- Security Awareness Training Program
- Penetration Testing and Security Assessment Procedure
- Data Retention and Disposal Policy
- Secure Software Development Lifecycle (SDLC) Standard

## 20. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Typed as Standard; exception approver set to CEO; volume, replication, private-connectivity, multi-region key, image-integrity and certificate-binding claims removed in favor of the regional KMS key, ACM certificates, TLS 1.2+ and ECR scan-on-push; corrected the availability-zone key-replica statement (KMS is regional); staging key statement limited to "the staging environment uses its own key"; rotation table tied to Secrets Manager and the API key rotation calendar; integration-guidelines reference redirected after merge |
