---
title: "Data Classification and Handling Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "data-classification-and-handling-standard-v1.0.pdf"
---

# Data Classification and Handling Standard

## 1. Purpose and Scope

### 1.1 Purpose

This Data Classification and Handling Standard establishes the framework for classifying and handling information assets at Deal Intelligence LLC. This standard ensures that all data, particularly business contact information and market intelligence data processed through our B2B platform, receives appropriate protection based on its sensitivity and criticality to business operations.

This standard is the single classification document for Deal Intelligence. The former Data Classification Policy has been merged into it; the Policy's classification decision tree, data element reference and quick reference card are carried forward as Appendices A to C.

### 1.2 Scope

This standard applies to:

- All forms of data (electronic, physical, verbal) processed by Deal Intelligence

- All personnel, contractors, and third parties with access to company data

- All systems and infrastructure components within the AWS cloud environment

- Customer data including business contact information, lead qualification data, and competitive intelligence

- Internal operational and administrative data

### 1.3 Compliance Alignment

This standard supports compliance with:

- SOC 2 Trust Services Criteria (Security, Availability and Confidentiality)

- General Data Protection Regulation (GDPR)

- California Consumer Privacy Act (CCPA)

- Industry best practices for B2B data handling

## 2. Data Classification Framework

### 2.1 Classification Levels

Deal Intelligence employs a four-tier classification system aligned with our business operations and regulatory requirements:

#### 2.1.1 Public

- **Definition** : Information intended for public disclosure

- **Examples** : Marketing materials, public website content, press releases

- **Impact if Disclosed** : No adverse impact

- **Handling Requirements** : No special handling required

#### 2.1.2 Internal

- **Definition** : Information for internal business use only

- **Examples** : Internal procedures, general business communications, non-sensitive operational data

- **Impact if Disclosed** : Minor reputational impact or competitive disadvantage

- **Handling Requirements** :

   - Access restricted to authorized personnel

   - Standard authentication required via PropelAuth JWT

   - Transmission over secure channels

#### 2.1.3 Confidential

- **Definition** : Sensitive business information, including personal data, requiring enhanced protection

- **Examples** :

   - Business contact information (first name, last name, business email, LinkedIn profile URL)

   - Job titles and employer information

   - Company domains and organizational data

   - Customer account data and delivered leads

   - Lead qualification status and sourcing dates

   - Competitor interaction data

   - System configurations

   - Vendor contracts and agreements

- **Impact if Disclosed** : Significant business impact, regulatory penalties, or customer trust damage

- **Handling Requirements** :

   - Role-based access control (RBAC) enforcement

   - Encryption at rest using AWS KMS

   - TLS 1.2+ for data in transit

   - Audit logging of all access via CloudWatch

   - PII sanitization in logs

   - Subject to data subject rights requests (access, deletion, correction) per Data Subject Rights Request Procedure

   - Retention per Data Retention and Disposal Policy

#### 2.1.4 Restricted

- **Definition** : Highly sensitive data requiring maximum protection

- **Examples** :

   - Authentication credentials and tokens

   - API keys

   - Encryption keys and certificates

- **Impact if Disclosed** : Severe regulatory penalties, significant financial loss, major breach of customer trust

- **Handling Requirements** :

   - Access limited to the CEO; multi-factor authentication for personnel enforced in Google Workspace, GitHub and AWS

   - AES-256 encryption mandatory per Encryption and Cryptographic Controls Standard

   - Stored in AWS Secrets Manager or KMS-encrypted DocumentDB only

   - VPC-isolated database with no direct access

   - Continuous monitoring via Security Hub

   - PII sanitization in logs

   - Immediate incident response per Incident Response Procedure

## 3. Data Handling Requirements

### 3.1 Data Collection and Processing

- All data collection must have a defined business purpose

- Customer data processing limited to agreed purposes in Data Processing Agreements

- Minimize data collection to what is necessary for service delivery

- Implement data validation and sanitization at point of entry

### 3.2 Data Storage

- **DocumentDB Storage** : All Confidential and Restricted data stored with KMS encryption

- **Secrets Storage** : Restricted credentials and keys stored in AWS Secrets Manager

- **Container Images** : ECR repositories with vulnerability scanning enabled

- **Backup Storage** : Daily automated backups with 90-day retention

- **Log Storage** : CloudWatch logs with 90-day retention period

### 3.3 Data Transmission

- **External APIs** : TLS 1.2+ encryption required per API Security and Rate Limiting Standard

- **Internal Communications** : VPC private subnets for database access

- **CDN Distribution** : CloudFront with HTTPS-only policies

- **Third-Party Integrations** : Secure protocols required per the Integration security section of the API Security and Rate Limiting Standard

### 3.4 Data Access Controls

Access to classified data follows the principle of least privilege:

- **Authentication** : PropelAuth JWT; customer MFA inherited from Google Workspace sign-in via PropelAuth (Google SSO only); personnel MFA enforced in Google Workspace, GitHub and AWS

- **Authorization** : RBAC implementation with user and company-level isolation

- **Access Reviews** : Quarterly access reviews (scheduled Lambda check), recorded in the compliance platform

- **Session Management** : Timeout policies enforced

- **Audit Trail** : All access logged and monitored

For detailed access control requirements, refer to Access Control and Authentication Policy.

## 4. Data Location and Identification

### 4.1 Electronic Data

- Classification is applied through the handling rules by tier in Section 2; no classification metadata is stored in the data itself

- Confidential and Restricted data lives in known locations: the DocumentDB collections, S3 buckets and AWS Secrets Manager entries of the `di-backend-api-prod` stack

- API responses include appropriate security headers

### 4.2 System Classification

- AWS resources carry CloudFormation tags only; classification is determined by the data each resource holds per Section 2

## 5. Data Sharing and Disclosure

### 5.1 Internal Sharing

- Confidential and Restricted data shared only on need-to-know basis

- Access requests require approval from Chief Executive Officer

- Temporary access granted with defined expiration

- All sharing activities logged for audit purposes

### 5.2 External Sharing

- Customer data sharing governed by Data Processing Agreements

- Sub-processor engagement requires 30-day notice to customers

- Third-party access limited to the documented sub-processors listed in the Vendor Management Policy

- Customer-controlled integrations (Slack, CRM) managed per customer preferences

### 5.3 Data Subject Rights

- Support for GDPR and CCPA data subject requests

- Procedures defined in Data Subject Rights Request Procedure

- 30-day (GDPR) / 45-day (CCPA) response timeline for access requests

- Secure verification process before data disclosure

## 6. Data Retention and Disposal

### 6.1 Retention Periods

Retention periods for each data type (active leads, customer account data, audit logs, backups and inactive customer data) are defined in the Data Retention and Disposal Policy, which is the single retention schedule for Deal Intelligence. This standard does not restate them.

### 6.2 Secure Disposal

- Electronic data overwritten using secure deletion methods

- Database records permanently removed with audit trail

- Backup media securely wiped after retention period

- Certificates of destruction maintained where applicable

For complete retention and disposal procedures, see Data Retention and Disposal Policy.

## 7. Compliance and Monitoring

### 7.1 Continuous Monitoring

- CloudWatch monitoring with real-time alerts

- Security Hub findings reviewed monthly; critical findings alert in real time via SNS through the breach-detection Lambda

- Container vulnerability scanning in ECR

- Rate limiting enforcement (100 requests/minute)

### 7.2 Compliance Verification

- Annual classification review by Chief Executive Officer

- Quarterly access reviews (scheduled Lambda check), recorded in the compliance platform

- SOC 2 audit validation of classification controls

- Risk assessments utilizing the organization's compliance platform Risk Assessment module

### 7.3 Incident Response

- 48-hour breach notification to affected customers for incidents involving Confidential or Restricted data; 72-hour notification to the supervisory authority where GDPR applies

- Breach detection via Security Hub findings routed to SNS by the breach-detection Lambda

- SNS security alerts for classification violations

- Post-hoc review within 5 business days for emergency changes

- Incidents documented using the compliance platform's Incident Reporting forms

## 8. Training and Awareness

### 8.1 Training Requirements

- All personnel receive data classification training during onboarding

- Annual refresher training on handling requirements

- Role-specific training for those handling Restricted data

- Training completion tracked in the compliance platform portal, with the completion certificate as evidence

### 8.2 Awareness Activities

- Classification reminders in system interfaces

- Updates to personnel when this standard changes

For complete training program details, see Security Awareness Training Program.

## 9. Responsibilities

### 9.1 Chief Executive Officer

- Approve data classification framework

- Oversee compliance with classification requirements

- Review and approve classification exceptions

- Ensure adequate resources for data protection

- Classify data according to this standard (data owner)

- Implement appropriate handling controls

- Review classification annually

- Report classification incidents

### 9.2 Go-to-Market Contractor

- Handles Internal and Confidential data only as authorized by the CEO

- Has no production (AWS, GitHub, DocumentDB, PropelAuth admin) access and no access to Restricted data

- Subject to the requirements for all personnel below

### 9.3 All Personnel

- Understand classification levels and requirements

- Handle data according to its classification

- Report suspected misclassification or mishandling

- Complete required training

## 10. Exceptions and Violations

### 10.1 Exception Process

- Exceptions require written justification

- Risk assessment required for all exceptions

- Approval by Chief Executive Officer

- Compensating controls must be implemented

- Exceptions reviewed quarterly

### 10.2 Violation Consequences

- Violations investigated per Incident Response Procedure

- Corrective actions determined based on severity

- Retraining required for unintentional violations

- Disciplinary action for willful violations

## 11. Related Documents

This standard should be read in conjunction with:

- Information Security Policy

- Access Control and Authentication Policy

- Encryption and Cryptographic Controls Standard

- Data Retention and Disposal Policy

- Privacy Notice and Data Processing Agreement Template

- Data Subject Rights Request Procedure

- Incident Response Procedure

- Vendor Management Policy

## 12. Document Review and Maintenance

This standard will be reviewed annually or upon:

- Significant changes to data processing activities

- Introduction of new data types or systems

- Regulatory requirement changes

- Security incident involving data classification

- Audit findings or recommendations

## 13. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Data Classification Policy merged in (decision tree, data element reference and quick reference card as Appendices A to C); business contact information classified Confidential; scope limited to Security, Availability and Confidentiality; classification metadata fields, resource tags and email markings removed in favor of handling rules by tier; roles consolidated to CEO and Go-to-Market Contractor; retention schedule referenced to Data Retention and Disposal Policy; notification, review and MFA wording aligned |

## Appendix A: Classification Decision Tree

```
START: Is the data authentication credentials, encryption keys, API keys, or security secrets?
  │
  ├─ YES → RESTRICTED
  │
  └─ NO → Does the data contain PII or business contact information?
           │
           ├─ YES → CONFIDENTIAL
           │
           └─ NO → Is the data intended for internal use only?
                    │
                    ├─ YES → INTERNAL
                    │
                    └─ NO → Has the data been approved for public release?
                             │
                             ├─ YES → PUBLIC
                             │
                             └─ NO → Default to INTERNAL, seek guidance from the CEO
```

## Appendix B: Data Element Classification Reference

|**Data Element**|**Classification**|**Regulatory Basis**|
|---|---|---|
|First name, last name|CONFIDENTIAL|GDPR Art. 4(1), CCPA §1798.140(o)|
|Business email address|CONFIDENTIAL|GDPR Art. 4(1), CCPA §1798.140(o)|
|LinkedIn profile URL|CONFIDENTIAL|GDPR Art. 4(1)|
|Job title|CONFIDENTIAL|GDPR Art. 4(1)|
|Current employer|CONFIDENTIAL|GDPR Art. 4(1)|
|Company name/domain|CONFIDENTIAL|Business data|
|Competitor interaction data|CONFIDENTIAL|Business data|
|Lead qualification status|CONFIDENTIAL|Business data|
|Sourcing dates|CONFIDENTIAL|Business data|
|Customer account data|CONFIDENTIAL|GDPR Art. 4(1), CCPA|
|API keys/tokens|RESTRICTED|Security requirement|
|Encryption keys|RESTRICTED|Security requirement|
|Database credentials|RESTRICTED|Security requirement|
|System logs (sanitized)|INTERNAL|Operational data|
|Architecture documentation|INTERNAL|Business data|
|Marketing materials|PUBLIC|Approved for release|

Business contact information is processed under the GDPR legitimate interest basis for B2B marketing and is subject to CCPA business contact exemption considerations. Market intelligence derived from it is CONFIDENTIAL at the individual level; aggregated or anonymized data is INTERNAL or PUBLIC depending on disclosure approval by the CEO.

## Appendix C: Quick Reference Card

**Before handling any data, ask:**

1. **What classification level is this data?**

2. **Am I authorized to access this data?**

3. **Am I using approved storage and transmission methods?**

4. **Have I applied appropriate security controls?**

5. **Do I know how to report a suspected incident?**

**When in doubt:**

- Classify at the higher level

- Contact the CEO for guidance

- Do not share externally until classification is confirmed

**Report incidents immediately** through the compliance platform Incident Reporting system or contact the CEO directly.

_This document is classified as Internal Use and should be handled accordingly._
