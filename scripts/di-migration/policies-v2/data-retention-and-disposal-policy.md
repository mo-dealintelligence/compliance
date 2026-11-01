---
title: "Data Retention and Disposal Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "None"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "data-retention-and-disposal-policy-v1.0.pdf"
---

# Data Retention and Disposal Policy

## 1. Purpose and Scope

### 1.1 Purpose

This Data Retention and Disposal Policy establishes procedures for retaining and securely disposing of confidential information at Deal Intelligence LLC. The policy ensures compliance with legal retention requirements, regulatory obligations, and data minimization principles under the General Data Protection Regulation (GDPR), California Consumer Privacy Act (CCPA), and SOC 2 Trust Services Criteria.

This policy supports Deal Intelligence's commitment to:

- Protecting business contact information and market intelligence data

- Maintaining only necessary data for legitimate business purposes

- Ensuring secure and verifiable disposal of information assets

- Meeting SOC 2 Type II certification requirements across the applicable Trust Services Categories (Security, Availability, and Confidentiality)

### 1.2 Scope

This policy applies to all information assets owned, processed, stored, or transmitted by Deal Intelligence LLC, including:

- **Customer Data**: Business contact information (names, email addresses, LinkedIn profiles, job titles, company information)

- **Market Intelligence Data**: Competitor interaction data, lead qualification status, sourcing dates

- **User Account Data**: Customer account credentials, authentication records, access logs

- **System and Application Data**: Configuration files, application logs, API transaction records

- **Audit Logs and Security Records**: CloudTrail logs, CloudWatch metrics, Security Hub findings

- **Database Backups and Archives**: DocumentDB backups, infrastructure snapshots

- **Development Artifacts**: Code repositories, container images (ECR), deployment records

The policy applies to all storage systems, databases, and backup media maintained within the AWS cloud infrastructure (us-east-1a, us-east-1b availability zones), including Lambda functions, Fargate containers, DocumentDB, and associated services.

For data classification requirements that inform retention decisions, refer to the Data Classification and Handling Standard.

### 1.3 Policy Statement

Deal Intelligence LLC is committed to retaining information only as long as necessary for business, legal, and regulatory purposes, and to securely disposing of information when retention periods expire. The organization implements automated retention enforcement through AWS-native services and Lambda functions to ensure consistent compliance with this policy.

### 1.4 Related Documents

This policy should be read in conjunction with:

- Data Classification and Handling Standard

- Information Security Policy

- Privacy Notice and Data Processing Agreement Template

- Data Subject Rights Request Procedure

- Business Continuity Plan

- Encryption and Cryptographic Controls Standard

## 2. Data Retention Schedule

### 2.1 Retention Periods by Data Type

The organization has established retention periods based on legal requirements, regulatory obligations, business needs, and data minimization principles. These periods align with SOC 2 Trust Services Criteria for Confidentiality (C1.1, C1.2) and with the storage-limitation obligations of GDPR and CCPA. This section is the single retention schedule for Deal Intelligence LLC; other documents (including the Data Classification and Handling Standard) reference it rather than restating it.

|**Data Type**|**Retention Period**|**Rationale**|**Legal/Compliance Basis**|
|---|---|---|---|
|**Business Contact Information**|24 months from last activity|Active lead management, data minimization|GDPR Art. 5(1)(e), CCPA §1798.105|
|**Delivered Leads (Customer Data)**|24 months from delivery|Customer service, contractual obligations|GDPR Art. 6(1)(b), SOC 2 C1.2|
|**User Account Data**|Duration of the customer relationship + 24 months, then deletion|Customer service, data minimization|GDPR Art. 5(1)(e), GDPR Art. 6(1)(b)|
|**Financial and Contract Records**|7 years|Financial record requirements|26 U.S.C. § 6001|
|**Market Intelligence Data**|24 months from collection|Business operations, data freshness|GDPR Art. 5(1)(e)|
|**Competitor Interaction Data**|24 months from last update|Platform functionality|GDPR Art. 6(1)(f)|
|**Audit Logs (CloudTrail)**|7 years|SOC 2 requirement, security investigations|SOC 2 CC7.2, CC7.3|
|**Application Logs (CloudWatch)**|90 days|Operational monitoring, compliance|SOC 2 CC7.2|
|**Security Hub Findings**|7 years [CONFIRM: retention mechanism — Security Hub itself retains findings for 90 days]|Incident investigation, compliance|SOC 2 CC7.4, CC7.5|
|**Database Backups (DocumentDB)**|90 days|Disaster recovery, business continuity|SOC 2 A1.2|
|**Container Images (ECR)**|90 days after deprecation|Rollback capability, audit trail|SOC 2 CC8.1|
|**Authentication Records**|2 years|Access review, security monitoring|SOC 2 CC6.1, CC6.2|
|**API Transaction Logs**|90 days (CloudWatch); the CloudTrail audit trail is retained 7 years|Performance monitoring, compliance|SOC 2 CC7.2|
|**Incident Response Records**|7 years|Regulatory compliance, legal hold|SOC 2 CC7.4, CC7.5|
|**Consent Records**|Duration of processing + 7 years|Demonstrable consent compliance|GDPR Art. 7(1), CCPA|
|**Data Subject Request Records**|7 years from completion|Regulatory compliance|GDPR Art. 5(2), CCPA|

### 2.2 Retention Period Justification

#### 2.2.1 24-Month Active Data Retention

Business contact information, delivered leads, and customer account data (after the relationship ends) are retained for 24 months based on:

- **Data Freshness**: B2B contact information degrades in accuracy over time

- **Business Necessity**: Supports customer service and platform functionality

- **Data Minimization**: Balances operational needs with privacy principles

- **Customer Expectations**: Aligns with typical B2B data lifecycle

#### 2.2.2 7-Year Compliance Retention

Extended retention periods apply to:

- **Financial Records**: IRS requirements under 26 U.S.C. § 6001

- **Audit Logs**: SOC 2 Trust Services Criteria requirements

- **Security Records**: Incident investigation and legal hold capabilities

- **Consent Documentation**: Demonstrable compliance with GDPR/CCPA

#### 2.2.3 90-Day Operational Retention

Short-term retention applies to:

- **Operational Logs**: Performance monitoring and troubleshooting

- **Database Backups**: Disaster recovery within defined RTO/RPO objectives

- **Container Images**: Rollback capability for recent deployments

For backup retention and recovery procedures, refer to the Business Continuity Plan.

### 2.3 Legal Hold Procedures

When litigation, regulatory investigation, or audit is anticipated or pending:

1. **Hold Initiation**: Legal hold notices suspend normal retention schedules

2. **Scope Definition**: Identify affected data types, systems, and time periods

3. **Preservation**: The CEO pauses the retention enforcement Lambda function for in-scope data

4. **Documentation**: All holds are documented with justification and scope

5. **Release**: Holds are released only upon written authorization, after which normal retention resumes

Legal holds are tracked and managed through the compliance platform.

## 3. Data Disposal Methods

### 3.1 Secure Disposal Standards

All data disposal must render information unrecoverable and meet the following standards based on data classification as defined in the Data Classification and Handling Standard:

|**Data Classification**|**Disposal Method**|**Standard**|
|---|---|---|
|**Restricted**|Cryptographic erasure + secure deletion|NIST SP 800-88 Rev. 1 (Purge)|
|**Confidential**|Cryptographic erasure or secure overwrite|NIST SP 800-88 Rev. 1 (Clear/Purge)|
|**Internal**|Secure deletion|NIST SP 800-88 Rev. 1 (Clear)|
|**Public**|Standard deletion|N/A|

### 3.2 Disposal Methods by Storage Type

#### 3.2.1 DocumentDB (Primary Database)

**Method**: Record-level deletion

**Process**:

1. Identify records exceeding retention period via automated Lambda function

2. Execute deletion queries with transaction logging

3. Verify deletion through audit queries

**Verification**: Automated verification scripts confirm record removal

#### 3.2.2 CloudWatch Logs

**Method**: Automated log group retention policies

**Process**:

1. Configure retention periods (90 days) at log group creation

2. AWS automatically purges logs exceeding retention

**Verification**: CloudWatch metrics confirm log volume alignment with retention

#### 3.2.3 CloudTrail Logs

**Method**: S3 lifecycle policies with Object Lock

**Process**:

1. Logs stored in dedicated S3 bucket with versioning and Object Lock

2. Lifecycle policy transitions to Glacier after 1 year

3. Permanent deletion after 7-year retention

**Verification**: S3 inventory reports confirm object deletion

#### 3.2.4 Database Backups

**Method**: Automated backup expiration

**Process**:

1. DocumentDB automated backups expire per retention setting (90 days)

2. Manual snapshots tagged with expiration dates

3. Lambda function identifies and deletes expired manual snapshots

**Verification**: Backup inventory reconciliation

#### 3.2.5 Container Images (ECR)

**Method**: Lifecycle policy-based image expiration

**Process**:

1. ECR lifecycle policies remove untagged images after 14 days

2. Deprecated tagged images removed after 90 days

3. Production images retained per deployment history requirements

**Verification**: ECR image inventory audit

#### 3.2.6 Application Data (Lambda, Fargate)

**Method**: Ephemeral by design; no persistent local storage

**Process**:

1. Lambda functions use /tmp storage cleared after execution

2. Fargate containers use ephemeral storage cleared on termination

3. Persistent data stored only in DocumentDB (covered above)

**Verification**: Architecture review confirms no persistent local storage

### 3.3 Cryptographic Erasure

For data encrypted with AWS KMS (as specified in the Encryption and Cryptographic Controls Standard):

1. **Key Scheduling**: Schedule KMS key deletion (7-30 day waiting period)

2. **Key Rotation**: Rotate keys to render historical data inaccessible

3. **Key Deletion**: Permanent key deletion after waiting period

4. **Documentation**: Record key deletion in audit log

**Note**: Cryptographic erasure is the preferred method for bulk data disposal as it ensures all copies (including backups) become inaccessible.

## 4. Automated Retention Enforcement

### 4.1 Automation Architecture

Deal Intelligence implements automated retention enforcement to ensure consistent compliance and reduce human error risk:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  EventBridge    │────▶│  Lambda Function │────▶│   DocumentDB    │
│  (Scheduled)    │     │  (Retention)     │     │   (Deletion)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   CloudWatch     │
                        │   (Logging)      │
                        └──────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   SNS Alerts     │
                        │   (Notification) │
                        └──────────────────┘
```

### 4.2 Automated Processes

|**Process**|**Frequency**|**Trigger**|**Action**|
|---|---|---|---|
|Business Contact Cleanup|Daily|EventBridge|Delete contacts inactive >24 months|
|Lead Data Expiration|Daily|EventBridge|Archive/delete leads >24 months|
|Customer Account Data Expiration|Daily|EventBridge|Delete account data >24 months after the relationship ends|
|Log Retention Enforcement|Continuous|CloudWatch Policy|Automatic log purge|
|Backup Expiration|Daily|DocumentDB/S3 Lifecycle|Automatic backup deletion|
|Image Cleanup|Daily|ECR Lifecycle|Remove deprecated images|
|Consent Record Review|Monthly|EventBridge|Flag expired consent for review|

### 4.3 Retention Enforcement Lambda Function

The retention enforcement Lambda function:

1. **Queries** DocumentDB for records exceeding retention thresholds

2. **Is paused** by the CEO for in-scope data while a legal hold recorded in the compliance platform is active (Section 2.3)

3. **Executes** deletion with transaction logging

4. **Verifies** successful deletion through confirmation queries

5. **Reports** deletion metrics to CloudWatch

6. **Alerts** via SNS for any failures or anomalies

### 4.4 Exception Handling

Automated processes include safeguards:

- **Legal Hold Check**: The CEO checks the legal holds recorded in the compliance platform before resuming any paused deletion

- **Threshold Alerts**: SNS notification if deletion volume exceeds normal patterns

- **Rollback Capability**: Transaction logging enables investigation of unintended deletions

- **Manual Override**: The CEO can pause automated deletion

- **Audit Trail**: All automated actions logged to CloudTrail

## 5. Data Subject Rights and Retention

### 5.1 Right to Erasure (GDPR Article 17 / CCPA §1798.105)

Data subjects may request deletion of their personal data. Upon receiving a valid erasure request:

1. **Verification**: Confirm requestor identity per Data Subject Rights Request Procedure

2. **Scope Assessment**: Identify all systems containing the subject's data

3. **Legal Basis Review**: Confirm no overriding legal retention requirement

4. **Execution**: Delete data from all systems within 30 days (GDPR) or 45 days (CCPA)

5. **Backup Handling**: Note deletion; data will be purged from backups per normal rotation (90 days)

6. **Confirmation**: Provide written confirmation to data subject

7. **Documentation**: Record request and actions in the compliance platform

For detailed procedures, refer to the Data Subject Rights Request Procedure.

### 5.2 Retention vs. Erasure Conflicts

When erasure requests conflict with retention requirements:

|**Scenario**|**Resolution**|
|---|---|
|Active legal hold|Retain data; inform subject of delay|
|Financial record requirement|Retain minimum necessary; delete remainder|
|Active customer relationship|Retain for service delivery; delete upon relationship end|
|Consent withdrawn|Delete unless other legal basis applies|

### 5.3 Sub-Processor Data Deletion

For data processed by sub-processors listed in the Vendor Management Policy:

1. **PropelAuth**: Authentication data deleted upon account closure request

2. **AWS**: Infrastructure data managed per this policy; AWS does not retain customer data beyond service delivery

Sub-processor obligations are documented in Data Processing Agreements as outlined in the Vendor Management Policy.

## 6. Roles and Responsibilities

### 6.1 Responsibility Matrix

|**Role**|**Responsibilities**|
|---|---|
|**Chief Executive Officer (CEO)**|Policy approval, legal hold authorization, compliance oversight; implement automated retention, maintain disposal systems, verify deletion; monitor retention compliance, manage data subject requests, audit retention practices|
|**All Personnel**|Follow retention schedules, report retention concerns, avoid unauthorized deletion|

### 6.2 Accountability

- **Policy Owner**: CEO

- **Technical Implementation**: CEO

- **Compliance Monitoring**: Tracked through the compliance platform

- **Audit Responsibility**: Annual review of retention practices; independent review by the external SOC 2 auditor

## 7. Monitoring and Compliance

### 7.1 Retention Compliance Monitoring

Continuous monitoring ensures retention policy compliance:

|**Metric**|**Target**|**Monitoring Method**|
|---|---|---|
|Automated deletion success rate|>99%|CloudWatch metrics|
|Data exceeding retention period|0 records|Daily automated Lambda check|
|Legal hold compliance|100%|Manual review|
|Disposal verification completion|100%|Audit log review|

For comprehensive monitoring procedures, refer to the System Monitoring and Logging Procedure.

### 7.2 Audit and Verification

#### 7.2.1 Quarterly Reviews

- Verify automated retention processes functioning correctly

- Review exception logs and manual interventions

- Confirm legal holds are current and justified

- Validate disposal certificates for any physical media

#### 7.2.2 Annual Audit

- Comprehensive review of retention schedule appropriateness

- Verification of disposal method effectiveness

- Assessment of regulatory requirement changes

- Update retention periods as needed

#### 7.2.3 Audit Evidence

The following evidence supports SOC 2 audit requirements:

- Automated deletion logs (CloudWatch, CloudTrail)

- Retention policy configurations (CloudFormation)

- Legal hold records in the compliance platform

- Data subject request records

- Disposal verification reports

### 7.3 Reporting

Monthly retention compliance reports include:

- Volume of data deleted by category

- Exceptions and manual interventions

- Legal hold status

- Data subject erasure requests processed

- Compliance metrics and trends

## 8. Incident Response for Retention Failures

### 8.1 Retention-Related Incidents

Retention failures requiring incident response include:

- Premature data deletion (before retention period expires)

- Failure to delete data (after retention period expires)

- Unauthorized data deletion

- Legal hold violations

- Disposal verification failures

### 8.2 Response Procedures

Upon identifying a retention-related incident:

1. **Contain**: Halt affected automated processes

2. **Assess**: Determine scope and impact of the incident

3. **Recover**: Restore prematurely deleted data from backups if applicable

4. **Remediate**: Execute overdue deletions or correct process failures

5. **Report**: Document incident per Incident Response Procedure

6. **Improve**: Update processes to prevent recurrence

Incidents are documented using the Incident Reporting system in the compliance platform.

## 9. Training and Awareness

### 9.1 Training Requirements

All personnel with data handling responsibilities must complete:

- **Initial Training**: Data retention and disposal procedures at onboarding

- **Annual Refresher**: Updates on retention requirements and disposal methods

- **Role-Specific Training**: The CEO, as operator of the automated retention systems, maintains detailed knowledge of those systems

Training is delivered through the Security Awareness Training Program in the compliance platform portal.

### 9.2 Awareness Topics

- Retention schedule by data type

- Secure disposal requirements

- Legal hold procedures

- Data subject rights obligations

- Reporting retention concerns

## 10. Policy Governance

### 10.1 Review and Updates

This policy is reviewed:

- **Annually**: Comprehensive review of all provisions

- **Upon Regulatory Change**: Updates to GDPR, CCPA, or SOC 2 requirements

- **Upon Business Change**: New data types, systems, or processing activities

- **Post-Incident**: Following retention-related incidents

### 10.2 Approval

This policy is approved by the Chief Executive Officer of Deal Intelligence LLC and is effective upon publication.

### 10.3 Exceptions

Exceptions to this policy require:

1. Written justification documenting business need

2. Risk assessment of the exception

3. Approval from the CEO

4. Time-limited duration with review date

5. Documentation in the compliance platform

## 11. Definitions

|**Term**|**Definition**|
|---|---|
|**Retention Period**|The duration for which data must be maintained before disposal|
|**Disposal**|The secure destruction or deletion of data rendering it unrecoverable|
|**Legal Hold**|A directive to preserve data that may be relevant to litigation or investigation|
|**Cryptographic Erasure**|Rendering data inaccessible by destroying encryption keys|
|**Data Subject**|An individual whose personal data is processed|
|**Active Lead**|Business contact with activity within the retention period|
|**PII**|Personally Identifiable Information|

## 12. Appendices

### Appendix A: Retention Decision Flowchart

```
┌─────────────────────────────────────┐
│ Data reaches retention threshold    │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ Is there an active legal hold?      │
└─────────────────┬───────────────────┘
        ┌─────────┴─────────┐
        ▼                   ▼
       YES                  NO
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────────────┐
│ Retain until  │   │ Is there an active    │
│ hold released │   │ data subject request? │
└───────────────┘   └───────────┬───────────┘
                      ┌─────────┴─────────┐
                      ▼                   ▼
                     YES                  NO
                      │                   │
                      ▼                   ▼
              ┌───────────────┐   ┌───────────────┐
              │ Process per   │   │ Execute       │
              │ DSAR procedure│   │ disposal      │
              └───────────────┘   └───────────────┘
```

### Appendix B: AWS Service Retention Configuration

|**AWS Service**|**Retention Setting**|**Configuration Method**|
|---|---|---|
|CloudWatch Logs|90 days|Log group retention policy|
|CloudTrail|7 years|S3 lifecycle policy (Glacier after 1 year) with Object Lock|
|DocumentDB Backups|90 days|Automated backup retention|
|ECR Images|90 days (deprecated)|Lifecycle policy|
|S3 Objects|Per data type|Lifecycle rules|

### Appendix C: Compliance Mapping

|**Requirement**|**Policy Section**|**Control**|
|---|---|---|
|SOC 2 CC6.5|Section 3, 4|Secure disposal of data|
|SOC 2 C1.2|Section 2|Confidential information disposal|
|GDPR Art. 5(1)(e)|Section 2|Storage limitation|
|GDPR Art. 17|Section 5|Right to erasure|
|CCPA §1798.105|Section 5|Right to deletion|

_This policy supports Deal Intelligence LLC's commitment to SOC 2 Type II certification and ongoing compliance with GDPR and CCPA requirements for B2B data processing._

## Revision history

|**Version**|**Date**|**Author**|**Changes**|
|---|---|---|---|
|1.0|November 13, 2025|Deal Intelligence|Initial policy (finalized in the compliance platform February 2, 2026)|
|2.0|<to be set at publication>|Mo Messidi|Scope limited to Security, Availability and Confidentiality; account data retention set to relationship + 24 months; CloudWatch Logs 90 days, CloudTrail 7 years via S3 lifecycle and Object Lock; legal holds managed in the compliance platform; roles consolidated to the CEO; this document is the single retention schedule|
