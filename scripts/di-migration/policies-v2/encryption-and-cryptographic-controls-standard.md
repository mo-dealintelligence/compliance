---
title: "Encryption and Cryptographic Controls Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "encryption-and-cryptographic-controls-standard-v1.0.pdf"
---

# Encryption and Cryptographic Controls Standard

## 1. Purpose

This Encryption and Cryptographic Controls Standard establishes the mandatory requirements for protecting Deal Intelligence LLC's information assets through cryptographic controls. This standard ensures the confidentiality, integrity, and authenticity of business contact information, customer data, and market intelligence throughout their lifecycle in accordance with SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls) and C1.1 (Confidentiality).

This standard operationalizes the encryption requirements defined in the Information Security Policy and provides specific implementation guidance for AWS KMS encryption, TLS protocols, and cryptographic key management across our cloud infrastructure.

## 2. Scope

This standard applies to:

- All data at rest within AWS infrastructure including DocumentDB collections and S3 buckets

- All data in transit between system components, APIs, and third-party services

- Cryptographic key generation, storage, rotation, and destruction procedures

- Certificate management for CloudFront distributions and API endpoints

- JWT token signing and validation for PropelAuth authentication services

- All personnel responsible for implementing or maintaining cryptographic controls

## 3. Cryptographic Requirements

### 3.1 Encryption Standards

All cryptographic implementations shall meet or exceed the following minimum standards:

|**Data State**|**Minimum Standard**|**Implementation**|
|---|---|---|
|Data at Rest|AES-256-GCM|AWS KMS customer-managed keys (CMK)|
|Data in Transit|TLS 1.2+|AWS Certificate Manager, CloudFront|
|Key Exchange|RSA-2048 or ECDHE|CloudFront negotiation|
|Hashing|SHA-256|Lambda function integrity checks|
|Digital Signatures|RSA-2048 with SHA-256|JWT token validation|

### 3.2 Prohibited Algorithms

The following cryptographic algorithms are explicitly prohibited:

- DES, 3DES (all variants)

- MD5, SHA-1 for security purposes

- RC4 stream cipher

- TLS versions prior to 1.2

- RSA keys smaller than 2048 bits

## 4. Data at Rest Encryption

### 4.1 DocumentDB Encryption

All DocumentDB clusters shall implement:

- AWS KMS encryption enabled at cluster creation

- Customer-managed CMK (regional, us-east-1) with automatic annual rotation

- Encryption of automated backups using the same CMK

- Audit logging of all KMS key usage via CloudTrail

Implementation aligns with data classification levels defined in Data Classification and Handling Standard.

### 4.2 S3 Bucket Encryption

All S3 buckets shall enforce:

- Default encryption using SSE-KMS with customer-managed keys

- Bucket policies denying unencrypted object uploads

- Versioning enabled with encryption of all object versions

### 4.3 Lambda Environment Variables

Sensitive configuration data in Lambda functions shall be:

- Encrypted using AWS KMS customer-managed keys

- Decrypted at runtime using IAM role permissions

- Rotated quarterly in alignment with Access Control and Authentication Policy

### 4.4 Container Image Encryption

ECR repositories shall implement:

- Encryption at rest using AWS KMS

- Scan-on-push vulnerability scanning on all repositories, with critical findings remediated before deployment

- Images built and pushed only from a green GitHub Actions CI run (including Trivy image scanning)

## 5. Data in Transit Encryption

### 5.1 API Communications

All API endpoints shall enforce:

- TLS 1.2 minimum with TLS 1.3 preferred

- Certificate validation for all HTTPS connections

- HSTS headers with minimum 1-year max-age

- AWS Certificate Manager-managed certificates for all public endpoints

Reference: API Security and Rate Limiting Standard

### 5.2 VPC Communications

Internal VPC traffic shall utilize:

- VPC endpoints for AWS service communications

- A single VPC in a single region (us-east-1); encryption at rest uses a KMS regional customer-managed key with annual rotation

- Security groups restricting protocols to encrypted variants only

Reference: Cloud Infrastructure Security Policy

### 5.3 CloudFront Distribution

CDN configurations shall enforce:

- Viewer Protocol Policy set to "Redirect HTTP to HTTPS"

- Origin Protocol Policy using HTTPS only

- AWS Certificate Manager certificates with automatic renewal

- Custom SSL certificate for branded domains

## 6. Key Management

### 6.1 AWS KMS Keys

The following customer-managed KMS keys shall be maintained in us-east-1:

```
Production Data Encryption Key
├── DocumentDB Encryption Key
├── S3 Bucket Encryption Key
└── Lambda Environment Variable Key
Backup Encryption Key
Audit Log Encryption Key
└── CloudTrail/CloudWatch Logs Key
```

The staging stage uses its own key, separate from production.

### 6.2 Key Rotation Requirements

|**Key Type**|**Rotation Frequency**|**Method**|
|---|---|---|
|AWS KMS CMK|Annual|Automatic via KMS|
|API Keys|90 days|Manual with overlap period, per the rotation calendar|
|JWT Signing Keys|180 days|PropelAuth managed|
|TLS Certificates|Annual|AWS Certificate Manager|
|Database Credentials|Quarterly|AWS Secrets Manager rotation on the DocumentDB credential|

### 6.3 Key Access Controls

Key access shall be restricted following the principle of least privilege:

- Production keys accessible only to production Lambda execution roles

- The staging stage uses its own key, separate from production

- CloudTrail logging of all key usage operations

- Quarterly access reviews documented in the compliance platform's Risk Assessment module

Reference: Access Control and Authentication Policy

## 7. Certificate Management

### 7.1 Certificate Lifecycle

All TLS certificates shall be:

- Issued by AWS Certificate Manager or approved Certificate Authorities

- Validated using DNS validation method

- Monitored for expiration with 30-day advance alerts via CloudWatch

- Automatically renewed where supported

### 7.2 Certificate Requirements

Production certificates must:

- Use 2048-bit RSA keys minimum or ECDSA P-256

- Include complete certificate chains

- Implement OCSP stapling where supported

- Exclude wildcard certificates for API endpoints

## 8. Authentication Token Security

### 8.1 JWT Token Protection

PropelAuth JWT tokens shall implement:

- RS256 algorithm for signature verification

- Token expiration not exceeding 24 hours

- Refresh token rotation on each use

- Secure storage in httpOnly cookies where applicable

### 8.2 API Key Management

API keys for third-party integrations shall be:

- Stored in AWS Secrets Manager with encryption

- Rotated according to schedule defined in Section 6.2

- Monitored for unauthorized usage patterns

- Revoked immediately upon suspicious activity detection

Reference: API Security and Rate Limiting Standard (Integration security) and Vendor Management Policy

## 9. Cryptographic Compliance

### 9.1 Regulatory Requirements

Cryptographic implementations shall comply with:

- GDPR Article 32 requiring appropriate technical measures

- CCPA Section 1798.150 reasonable security procedures

- SOC 2 CC6.1 criteria for logical access controls

- NIST SP 800-175B cryptographic standards

### 9.2 Export Control Compliance

All cryptographic implementations shall:

- Comply with U.S. Export Administration Regulations

- Document cryptographic capabilities for compliance reporting

- Restrict strong encryption to authorized jurisdictions

## 10. Implementation Procedures

### 10.1 New System Deployment

When deploying new systems:

1. Enable encryption by default using CloudFormation templates

2. Configure KMS key policies before data ingestion

3. Validate TLS configuration using SSL Labs or equivalent

4. Document encryption configuration in system inventory

### 10.2 Legacy System Migration

For systems requiring encryption upgrade:

1. Assess current encryption status via Security Hub

2. Plan migration during maintenance windows

3. Test encryption in the staging stage

4. Implement with rollback procedures per Change Management Policy

## 11. Monitoring and Validation

### 11.1 Continuous Monitoring

Encryption compliance shall be monitored through:

- AWS Security Hub encryption checks

- CloudWatch alarms for KMS key deletion attempts

- Monthly TLS configuration scans

- Quarterly encryption audit reports

Reference: System Monitoring and Logging Procedure

### 11.2 Vulnerability Management

Cryptographic vulnerabilities shall be:

- Identified through ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI

- Assessed using CVSS scoring methodology

- Remediated according to Vulnerability Management Procedure

- Tracked in the compliance platform's Risk Assessment module

## 12. Incident Response

### 12.1 Cryptographic Incidents

In the event of cryptographic compromise:

1. Immediately revoke affected keys/certificates

2. Generate new cryptographic materials

3. Re-encrypt affected data with new keys

4. Document incident in the compliance platform's Incident Reporting system

5. Notify affected customers within 48 hours if data confidentiality impacted

Reference: Incident Response Procedure

### 12.2 Key Compromise Procedures

Upon suspected key compromise:

- Rotate affected keys immediately

- Review CloudTrail logs for unauthorized key usage

- Update all systems using compromised keys

- Conduct forensic analysis of potential data exposure

## 13. Backup and Recovery

### 13.1 Key Backup Procedures

Cryptographic materials shall be:

- Held in AWS KMS as regional customer-managed keys in us-east-1; key material does not leave KMS

- Protected with equivalent encryption standards

- Tested quarterly for restoration capability as part of the quarterly backup-restore test (automated, recorded in the compliance platform)

- Documented in Business Continuity Plan

### 13.2 Disaster Recovery

In disaster scenarios:

- AWS KMS is a regional service; keys remain available across all availability zones in us-east-1 (including us-east-1a and us-east-1b) without replication

- Ensure backup restoration uses the same KMS keys that encrypted the backups

- Validate encryption post-recovery

## 14. Third-Party Encryption

### 14.1 Vendor Encryption Requirements

All vendors processing Deal Intelligence data must:

- Implement AES-256 encryption for data at rest

- Use TLS 1.2+ for data transmission

- Provide encryption attestation in SOC 2 reports

- Comply with requirements in Vendor Management Policy

### 14.2 Customer-Controlled Integrations

For customer-managed integrations:

- Provide encryption guidance documentation

- Support encrypted API communications

- Enable audit logging of integration activities

- Maintain encryption throughout data pipeline

## 15. Training and Awareness

### 15.1 Cryptographic Training

Personnel implementing cryptographic controls shall:

- Complete annual security awareness training on encryption

- Understand key management responsibilities

- Follow secure coding practices for cryptographic implementations

- Report cryptographic vulnerabilities immediately

Reference: Security Awareness Training Program

## 16. Compliance Verification

### 16.1 Annual Assessment

Cryptographic controls shall undergo:

- Annual penetration testing of TLS implementations

- Continuous Security Hub checks, reviewed monthly and recorded in the compliance platform

- Semi-annual key rotation audits

- Continuous monitoring via CloudWatch metrics

Reference: Penetration Testing and Security Assessment Procedure

### 16.2 Audit Evidence

The following evidence shall be maintained:

- KMS key rotation logs in CloudTrail

- Certificate issuance and renewal records

- Encryption configuration screenshots

- Security Hub compliance reports

## 17. Exceptions and Deviations

### 17.1 Exception Process

Any deviation from encryption standards requires:

- Documented business justification

- Risk assessment in the compliance platform's Risk Assessment module

- Compensating controls definition

- CEO approval

- Quarterly review for continued necessity

### 17.2 Legacy System Exceptions

Legacy systems unable to meet current standards shall:

- Be documented in the risk register

- Implement compensating controls

- Have defined migration timelines

- Be isolated from production data where possible

## 18. Related Documents

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

## 19. Review and Updates

This standard shall be reviewed annually and updated to reflect:

- Changes in cryptographic best practices

- New regulatory requirements

- Emerging cryptographic vulnerabilities

- Updates to AWS encryption services

- Findings from security assessments and audits

## 20. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Typed as Standard; exception approver set to CEO; volume, replication, private-connectivity, multi-region key, image-integrity and certificate-binding claims removed in favor of the regional KMS key, ACM certificates, TLS 1.2+ and ECR scan-on-push; corrected the availability-zone key-replica statement (KMS is regional); staging key statement limited to "the staging stage uses its own key"; rotation table tied to Secrets Manager and the API key rotation calendar; integration-guidelines reference redirected after merge |
