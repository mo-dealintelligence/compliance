---
title: "Data Classification and Handling Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "data-classification-and-handling-standard-v1.0.pdf"
---

# Data Classification and Handling Standard

## 1. Purpose

This standard defines how Deal Intelligence LLC classifies and handles information assets, so that all data, in particular the business contact information and market intelligence data processed through the B2B platform, receives protection matching its sensitivity and its criticality to business operations. It supports the SOC 2 Trust Services Criteria (Security, Availability, and Confidentiality), the General Data Protection Regulation (GDPR), and the California Consumer Privacy Act (CCPA).

This standard is the single classification document for Deal Intelligence. The former Data Classification Policy has been merged into it; the Policy's classification decision tree, data element reference, and quick reference card are carried forward as Appendices A to C.

## 2. Scope

This standard applies to:

- All forms of data (electronic, physical, verbal) processed by Deal Intelligence
- All personnel, contractors, and third parties with access to company data
- All systems and infrastructure components within the AWS cloud environment
- Customer data, including business contact information, lead qualification data, and competitive intelligence
- Internal operational and administrative data

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

- Approves the data classification framework
- Oversees compliance with classification requirements
- Reviews and approves classification exceptions
- Allocates resources for data protection
- Classifies data according to this standard (data owner)
- Implements the handling controls
- Reviews classification annually
- Reports classification incidents

### 3.2 Go-to-Market Contractor

- Handles Internal and Confidential data only as authorized by the CEO
- Has no production (AWS, GitHub, DocumentDB, PropelAuth admin) access and no access to Restricted data
- Is subject to the requirements for all personnel in Section 3.3

### 3.3 All personnel

- Understand the classification levels and requirements
- Handle data according to its classification
- Report suspected misclassification or mishandling
- Complete required training

## 4. Classification levels

Deal Intelligence uses a four-tier classification system aligned with its business operations and regulatory requirements.

### 4.1 Public

- **Definition**: Information intended for public disclosure
- **Examples**: Marketing materials, public website content, press releases
- **Impact if disclosed**: No adverse impact
- **Handling requirements**: No special handling required

### 4.2 Internal

- **Definition**: Information for internal business use only
- **Examples**: Internal procedures, general business communications, non-sensitive operational data
- **Impact if disclosed**: Minor reputational impact or competitive disadvantage
- **Handling requirements**:
  - Access restricted to authorized personnel
  - Standard authentication required via PropelAuth JWT
  - Transmission over secure channels

### 4.3 Confidential

- **Definition**: Sensitive business information, including personal data, requiring enhanced protection
- **Examples**:
  - Business contact information (first name, last name, business email, LinkedIn profile URL)
  - Job titles and employer information
  - Company domains and organizational data
  - Customer account data and delivered leads
  - Lead qualification status and sourcing dates
  - Competitor interaction data
  - System configurations
  - Vendor contracts and agreements
- **Impact if disclosed**: Significant business impact, regulatory penalties, or damage to customer trust
- **Handling requirements**:
  - Role-based access control (RBAC) enforcement
  - Encryption at rest using KMS
  - FileVault full-disk encryption (macOS) on personnel devices that access the data
  - TLS 1.2+ for data in transit
  - Audit logging of all access via CloudWatch
  - PII sanitization in logs
  - Subject to data subject rights requests (access, deletion, correction) per the Data Subject Rights Request Procedure
  - Retention per the Data Retention and Disposal Policy

### 4.4 Restricted

- **Definition**: Highly sensitive data requiring maximum protection
- **Examples**:
  - Authentication credentials and tokens
  - API keys
  - Encryption keys and certificates
- **Impact if disclosed**: Severe regulatory penalties, significant financial loss, major breach of customer trust
- **Handling requirements**:
  - Access limited to the CEO; multi-factor authentication for personnel enforced in Google Workspace, GitHub, and AWS
  - AES-256 encryption mandatory per the Encryption and Cryptographic Controls Standard
  - Stored in Secrets Manager or KMS-encrypted DocumentDB only
  - VPC-isolated database with no direct access
  - Monthly configuration-check record and real-time CloudTrail event alerts
  - PII sanitization in logs
  - Immediate incident response per the Incident Response Procedure

## 5. Data handling requirements

### 5.1 Data collection and processing

- All data collection has a defined business purpose
- Customer data processing is limited to the purposes agreed in Data Processing Agreements
- Data collection is minimized to what is necessary for service delivery
- Data is validated and sanitized at the point of entry

### 5.2 Data storage

- **DocumentDB storage**: All Confidential and Restricted data stored with KMS encryption
- **Secrets storage**: Restricted credentials and keys stored in Secrets Manager
- **Container images**: ECR repositories with vulnerability scanning enabled
- **Backup storage**: Daily automated backups with 90-day retention
- **Log storage**: CloudWatch logs with 90-day retention

### 5.3 Data transmission

- **External APIs**: TLS 1.2+ encryption required per the API Security and Rate Limiting Standard
- **Internal communications**: VPC private subnets for database access
- **CDN distribution**: CloudFront with HTTPS-only policies
- **Third-party integrations**: Secure protocols required per the Integration security section of the API Security and Rate Limiting Standard

### 5.4 Data access controls

Access to classified data follows the principle of least privilege:

- **Authentication**: PropelAuth JWT; customer MFA inherited from Google Workspace sign-in via PropelAuth (Google SSO only); personnel MFA enforced in Google Workspace, GitHub, and AWS
- **Authorization**: RBAC with user- and company-level isolation
- **Access reviews**: Quarterly access reviews (scheduled Lambda check), recorded in the compliance platform
- **Session management**: Timeout policies enforced
- **Audit trail**: All access logged and monitored

Detailed access control requirements are in the Access Control and Authentication Policy.

## 6. Data location and identification

### 6.1 Electronic data

- Classification is applied through the handling rules by tier in Section 4; no classification metadata is stored in the data itself
- Confidential and Restricted data lives in known locations: the DocumentDB collections, S3 buckets, and Secrets Manager entries of the `di-backend-api-prod` stack
- API responses include the required security headers

### 6.2 System classification

- AWS resources carry CloudFormation tags only; classification is determined by the data each resource holds per Section 4

## 7. Data sharing and disclosure

### 7.1 Internal sharing

- Confidential and Restricted data is shared only on a need-to-know basis
- Access requests require approval from the CEO
- Temporary access is granted with a defined expiration
- All sharing activities are logged for audit purposes

### 7.2 External sharing

- Customer data sharing is governed by Data Processing Agreements
- Sub-processor engagement requires 30 days' notice to customers
- Third-party access is limited to the documented sub-processors listed in the Vendor Management Policy
- Customer-controlled integrations (Slack, CRM) are managed per customer preferences

### 7.3 Data subject rights

- GDPR and CCPA data subject requests are supported
- Procedures are defined in the Data Subject Rights Request Procedure
- Response timeline for access requests: 30 days (GDPR) / 45 days (CCPA)
- Identity is verified before data is disclosed

## 8. Data retention and disposal

### 8.1 Retention periods

Retention periods for each data type (active leads, customer account data, audit logs, backups, and inactive customer data) are defined in the Data Retention and Disposal Policy, which is the single retention schedule for Deal Intelligence. This standard does not restate them.

### 8.2 Secure disposal

- Electronic data is overwritten using secure deletion methods
- Database records are permanently removed, with an audit trail
- Backup media is securely wiped after the retention period
- Certificates of destruction are maintained where applicable

Complete retention and disposal procedures are in the Data Retention and Disposal Policy.

## 9. Monitoring and incident response

### 9.1 Continuous monitoring

- CloudWatch monitoring with real-time alerts
- Monthly configuration-check Lambda run against a fixed checklist (including no public S3 buckets and KMS key rotation), with a dated pass/fail record posted to the compliance platform
- Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, KMS key disable, among others) trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- Container vulnerability scanning in ECR
- Rate limiting enforcement (100 requests/minute)

### 9.2 Compliance verification

- Annual classification review by the CEO
- Quarterly access reviews (scheduled Lambda check), recorded in the compliance platform
- SOC 2 audit validation of classification controls
- Risk assessments using the compliance platform Risk Assessment module

### 9.3 Incident response

- 48-hour breach notification to affected customers for incidents involving Confidential or Restricted data; 72-hour notification to the supervisory authority where GDPR applies
- Breach detection via security-relevant CloudTrail events routed by EventBridge to the breach-detection Lambda, which alerts the CEO via SNS
- SNS security alerts for classification violations
- Post-hoc review within 5 business days for emergency changes
- Incidents documented using the compliance platform's Incident Reporting forms

## 10. Training and awareness

### 10.1 Training requirements

- All personnel receive data classification training during onboarding
- Annual refresher training on handling requirements
- Role-specific training for those handling Restricted data
- Training completion tracked in the compliance platform portal, with the completion certificate as evidence

### 10.2 Awareness activities

- Classification reminders in system interfaces
- Updates to personnel when this standard changes

The full training program is in the Security Awareness Training Program.

## 11. Exceptions and violations

### 11.1 Exception process

- Exceptions require written justification
- A risk assessment is required for all exceptions
- Exceptions are approved by the CEO
- Compensating controls must be implemented

### 11.2 Violation consequences

- Violations are investigated per the Incident Response Procedure
- Corrective actions are determined by severity
- Retraining is required for unintentional violations
- Willful violations result in disciplinary action

## 12. Review

This standard is reviewed annually or upon:

- Significant changes to data processing activities
- Introduction of new data types or systems
- Regulatory requirement changes
- A security incident involving data classification
- Audit findings or recommendations

## 13. Related documents

- Information Security Policy
- Access Control and Authentication Policy
- Encryption and Cryptographic Controls Standard
- Data Retention and Disposal Policy
- Privacy Notice and Data Processing Agreement Template
- Data Subject Rights Request Procedure
- Incident Response Procedure
- Vendor Management Policy
- API Security and Rate Limiting Standard
- Security Awareness Training Program

## Appendix A: Classification decision tree

```
START: Is the data authentication credentials, encryption keys, API keys, or security secrets?
  │
  ├─ YES → Restricted
  │
  └─ NO → Does the data contain PII or business contact information?
           │
           ├─ YES → Confidential
           │
           └─ NO → Is the data intended for internal use only?
                    │
                    ├─ YES → Internal
                    │
                    └─ NO → Has the data been approved for public release?
                             │
                             ├─ YES → Public
                             │
                             └─ NO → Default to Internal; seek guidance from the CEO
```

## Appendix B: Data element classification reference

|**Data element**|**Classification**|**Regulatory basis**|
|---|---|---|
|First name, last name|Confidential|GDPR Art. 4(1), CCPA §1798.140(o)|
|Business email address|Confidential|GDPR Art. 4(1), CCPA §1798.140(o)|
|LinkedIn profile URL|Confidential|GDPR Art. 4(1)|
|Job title|Confidential|GDPR Art. 4(1)|
|Current employer|Confidential|GDPR Art. 4(1)|
|Company name/domain|Confidential|Business data|
|Competitor interaction data|Confidential|Business data|
|Lead qualification status|Confidential|Business data|
|Sourcing dates|Confidential|Business data|
|Customer account data|Confidential|GDPR Art. 4(1), CCPA|
|API keys/tokens|Restricted|Security requirement|
|Encryption keys|Restricted|Security requirement|
|Database credentials|Restricted|Security requirement|
|System logs (sanitized)|Internal|Operational data|
|Architecture documentation|Internal|Business data|
|Marketing materials|Public|Approved for release|

Business contact information is processed under the GDPR legitimate interest basis for B2B marketing and is subject to CCPA business contact exemption considerations. Market intelligence derived from it is Confidential at the individual level; aggregated or anonymized data is Internal or Public depending on disclosure approval by the CEO.

## Appendix C: Quick reference card

**Before handling any data, ask:**

1. What classification level is this data?
2. Am I authorized to access this data?
3. Am I using approved storage and transmission methods?
4. Have I applied the required security controls?
5. Do I know how to report a suspected incident?

**When in doubt:**

- Classify at the higher level
- Contact the CEO for guidance
- Do not share externally until the classification is confirmed

**Report incidents immediately** through the compliance platform Incident Reporting system or contact the CEO directly.

_This document is classified as Internal and is handled accordingly._

## 14. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Data Classification Policy merged in (decision tree, data element reference and quick reference card as Appendices A to C); business contact information classified Confidential; scope limited to Security, Availability and Confidentiality; classification metadata fields, resource tags and email markings removed in favor of handling rules by tier; roles consolidated to CEO and Go-to-Market Contractor; retention schedule referenced to Data Retention and Disposal Policy; notification, review and MFA wording aligned |
