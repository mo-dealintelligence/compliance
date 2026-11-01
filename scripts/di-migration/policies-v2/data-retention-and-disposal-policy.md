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

## 1. Purpose

This policy sets the retention periods for information held by Deal Intelligence LLC and the methods used to dispose of it securely when those periods expire. It meets the legal retention requirements and data-minimization obligations of the General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA), and the SOC 2 Trust Services Criteria for Security, Availability, and Confidentiality.

Deal Intelligence retains information only as long as business, legal, and regulatory purposes require, and disposes of it securely when the retention period expires. Retention is enforced automatically through AWS-native services and Lambda functions.

## 2. Scope

This policy applies to all information assets owned, processed, stored, or transmitted by Deal Intelligence, including:

- **Customer data**: business contact information (names, email addresses, LinkedIn profiles, job titles, company information)
- **Market intelligence data**: competitor interaction data, lead qualification status, sourcing dates
- **User account data**: customer account credentials, authentication records, access logs
- **System and application data**: configuration files, application logs, API transaction records
- **Audit logs and security records**: CloudTrail logs, CloudWatch metrics, Security Hub findings
- **Database backups and archives**: DocumentDB backups, infrastructure snapshots
- **Development artifacts**: code repositories, container images (ECR), deployment records

The policy applies to all storage systems, databases, and backup media in the AWS infrastructure (us-east-1a and us-east-1b availability zones), including Lambda functions, Fargate containers, DocumentDB, and associated services.

Data classification tiers that inform retention decisions are defined in the Data Classification and Handling Standard.

## 3. Definitions

|**Term**|**Definition**|
|---|---|
|**Retention period**|The duration for which data is kept before disposal|
|**Disposal**|The secure destruction or deletion of data so that it is unrecoverable|
|**Legal hold**|A directive to preserve data that may be relevant to litigation or an investigation|
|**Cryptographic erasure**|Rendering data inaccessible by destroying its encryption keys|
|**Data subject**|An individual whose personal data is processed|
|**Active lead**|A business contact with activity within the retention period|
|**PII**|Personally identifiable information|

## 4. Roles and responsibilities

|**Role**|**Responsibilities**|
|---|---|
|**Chief Executive Officer (CEO)**|Approves this policy; authorizes legal holds; implements and maintains the automated retention and disposal systems; verifies deletion; monitors retention compliance; handles data subject requests; audits retention practices|
|**All personnel**|Follow the retention schedule; report retention concerns; do not delete data without authorization|

- **Policy owner**: the CEO
- **Technical implementation**: the CEO
- **Compliance monitoring**: tracked in the compliance platform
- **Audit**: annual review of retention practices by the CEO; independent review by the external SOC 2 auditor

## 5. Data retention schedule

### 5.1 Retention periods by data type

Retention periods are based on legal requirements, regulatory obligations, business needs, and data-minimization principles. They align with the SOC 2 Confidentiality criteria (C1.1, C1.2) and the storage-limitation obligations of GDPR and CCPA. This section is the single retention schedule for Deal Intelligence; other documents (including the Data Classification and Handling Standard) reference it rather than restating it.

|**Data type**|**Retention period**|**Rationale**|**Legal/compliance basis**|
|---|---|---|---|
|**Business contact information**|24 months from last activity|Active lead management, data minimization|GDPR Art. 5(1)(e), CCPA §1798.105|
|**Delivered leads (customer data)**|24 months from delivery|Customer service, contractual obligations|GDPR Art. 6(1)(b), SOC 2 C1.2|
|**User account data**|Duration of the customer relationship + 24 months, then deletion|Customer service, data minimization|GDPR Art. 5(1)(e), GDPR Art. 6(1)(b)|
|**Financial and contract records**|7 years|Financial record requirements|26 U.S.C. § 6001|
|**Market intelligence data**|24 months from collection|Business operations, data freshness|GDPR Art. 5(1)(e)|
|**Competitor interaction data**|24 months from last update|Platform functionality|GDPR Art. 6(1)(f)|
|**Audit logs (CloudTrail)**|7 years|SOC 2 requirement, security investigations|SOC 2 CC7.2, CC7.3|
|**Application logs (CloudWatch)**|90 days|Operational monitoring, compliance|SOC 2 CC7.2|
|**Security Hub findings**|7 years [CONFIRM: retention mechanism — Security Hub itself retains findings for 90 days]|Incident investigation, compliance|SOC 2 CC7.4, CC7.5|
|**Database backups (DocumentDB)**|90 days|Disaster recovery, business continuity|SOC 2 A1.2|
|**Container images (ECR)**|90 days after deprecation|Rollback capability, audit trail|SOC 2 CC8.1|
|**Authentication records**|2 years|Access review, security monitoring|SOC 2 CC6.1, CC6.2|
|**API transaction logs**|90 days (CloudWatch); the CloudTrail audit trail is retained 7 years|Performance monitoring, compliance|SOC 2 CC7.2|
|**Incident response records**|7 years|Regulatory compliance, legal hold|SOC 2 CC7.4, CC7.5|
|**Consent records**|Duration of processing + 7 years|Demonstrable consent compliance|GDPR Art. 7(1), CCPA|
|**Data subject request records**|7 years from completion|Regulatory compliance|GDPR Art. 5(2), CCPA|

### 5.2 Retention period justification

**24-month active data retention.** Business contact information, delivered leads, and customer account data (after the relationship ends) are retained for 24 months because:

- **Data freshness**: B2B contact information degrades in accuracy over time
- **Business necessity**: the data supports customer service and platform functionality
- **Data minimization**: the period balances operational needs with privacy principles
- **Customer expectations**: the period matches the typical B2B data lifecycle

**7-year compliance retention.** Extended retention applies to:

- **Financial records**: IRS requirements under 26 U.S.C. § 6001
- **Audit logs**: SOC 2 Trust Services Criteria requirements
- **Security records**: incident investigation and legal hold capability
- **Consent documentation**: demonstrable compliance with GDPR and CCPA

**90-day operational retention.** Short-term retention applies to:

- **Operational logs**: performance monitoring and troubleshooting
- **Database backups**: disaster recovery within the RTO and RPO set in the Business Continuity Plan
- **Container images**: rollback capability for recent deployments

### 5.3 Legal hold procedure

When litigation, a regulatory investigation, or an audit is anticipated or pending:

1. **Hold initiation**: a legal hold notice suspends the normal retention schedule
2. **Scope definition**: the CEO identifies the affected data types, systems, and time periods
3. **Preservation**: the CEO pauses the retention enforcement Lambda function for in-scope data
4. **Documentation**: every hold is recorded with its justification and scope
5. **Release**: a hold is released only on written authorization, after which normal retention resumes

Legal holds are tracked in the compliance platform.

## 6. Data disposal methods

### 6.1 Secure disposal standards

Disposal renders information unrecoverable and meets the following standards by classification tier (see the Data Classification and Handling Standard):

|**Data classification**|**Disposal method**|**Standard**|
|---|---|---|
|**Restricted**|Cryptographic erasure + secure deletion|NIST SP 800-88 Rev. 1 (Purge)|
|**Confidential**|Cryptographic erasure or secure overwrite|NIST SP 800-88 Rev. 1 (Clear/Purge)|
|**Internal**|Secure deletion|NIST SP 800-88 Rev. 1 (Clear)|
|**Public**|Standard deletion|—|

### 6.2 Disposal methods by storage type

#### 6.2.1 DocumentDB (primary database)

**Method**: record-level deletion

**Process**:

1. The retention enforcement Lambda function identifies records past their retention period
2. Deletion queries run with transaction logging
3. Audit queries verify the deletion

**Verification**: automated verification scripts confirm record removal

#### 6.2.2 CloudWatch Logs

**Method**: log group retention policies

**Process**:

1. The 90-day retention period is set at log group creation
2. AWS purges logs past the retention period

**Verification**: CloudWatch metrics confirm log volume matches the retention setting

#### 6.2.3 CloudTrail logs

**Method**: S3 lifecycle policies with Object Lock

**Process**:

1. Logs are stored in a dedicated S3 bucket with versioning and Object Lock
2. The lifecycle policy transitions objects to Glacier after 1 year
3. Objects are permanently deleted after 7 years

**Verification**: S3 inventory reports confirm object deletion

#### 6.2.4 Database backups

**Method**: automated backup expiration

**Process**:

1. DocumentDB automated backups expire per the 90-day retention setting
2. Manual snapshots are tagged with expiration dates
3. A Lambda function identifies and deletes expired manual snapshots

**Verification**: backup inventory reconciliation

#### 6.2.5 Container images (ECR)

**Method**: lifecycle-policy image expiration

**Process**:

1. ECR lifecycle policies remove untagged images after 14 days
2. Deprecated tagged images are removed after 90 days
3. Production images are retained per deployment history requirements

**Verification**: ECR image inventory audit

#### 6.2.6 Application data (Lambda, Fargate)

**Method**: ephemeral by design; no persistent local storage

**Process**:

1. Lambda functions use /tmp storage that is cleared after execution
2. Fargate containers use ephemeral storage that is cleared on termination
3. Persistent data is stored only in DocumentDB (§6.2.1)

**Verification**: architecture review confirms no persistent local storage

### 6.3 Cryptographic erasure

For data encrypted with KMS (see the Encryption and Cryptographic Controls Standard):

1. **Key scheduling**: schedule KMS key deletion (7–30 day waiting period)
2. **Key rotation**: rotate keys to render historical data inaccessible
3. **Key deletion**: the key is permanently deleted after the waiting period
4. **Documentation**: record the key deletion in the audit log

Cryptographic erasure is the preferred method for bulk disposal because it makes every copy, including backups, inaccessible.

## 7. Automated retention enforcement

### 7.1 Architecture

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

### 7.2 Automated processes

|**Process**|**Frequency**|**Trigger**|**Action**|
|---|---|---|---|
|Business contact cleanup|Daily|EventBridge|Delete contacts inactive >24 months|
|Lead data expiration|Daily|EventBridge|Archive/delete leads >24 months|
|Customer account data expiration|Daily|EventBridge|Delete account data >24 months after the relationship ends|
|Log retention enforcement|Continuous|CloudWatch policy|Automatic log purge|
|Backup expiration|Daily|DocumentDB/S3 lifecycle|Automatic backup deletion|
|Image cleanup|Daily|ECR lifecycle|Remove deprecated images|
|Consent record review|Monthly|EventBridge|Flag expired consent for review|

### 7.3 Retention enforcement Lambda function

The retention enforcement Lambda function:

1. **Queries** DocumentDB for records past their retention thresholds
2. **Is paused** by the CEO for in-scope data while a legal hold recorded in the compliance platform is active (§5.3)
3. **Executes** deletion with transaction logging
4. **Verifies** the deletion through confirmation queries
5. **Reports** deletion metrics to CloudWatch
6. **Alerts** via SNS on any failure or anomaly

### 7.4 Safeguards

- **Legal hold check**: the CEO checks the legal holds recorded in the compliance platform before resuming any paused deletion
- **Threshold alerts**: SNS notifies the CEO if deletion volume exceeds normal patterns
- **Rollback capability**: transaction logging supports investigation of unintended deletions
- **Manual override**: the CEO can pause automated deletion
- **Audit trail**: all automated actions are logged to CloudTrail

## 8. Data subject rights and retention

### 8.1 Right to erasure (GDPR Article 17 / CCPA §1798.105)

Data subjects may request deletion of their personal data. On receiving a valid erasure request, the CEO:

1. **Verifies** the requestor's identity per the Data Subject Rights Request Procedure
2. **Identifies** all systems containing the subject's data
3. **Confirms** that no overriding legal retention requirement applies
4. **Deletes** the data from all systems within 30 days (GDPR) or 45 days (CCPA)
5. **Notes** that backups purge the data through normal rotation (90 days)
6. **Confirms** the deletion in writing to the data subject
7. **Records** the request and actions taken in the compliance platform

The full procedure is in the Data Subject Rights Request Procedure.

### 8.2 Retention and erasure conflicts

|**Scenario**|**Resolution**|
|---|---|
|Active legal hold|Retain the data; inform the subject of the delay|
|Financial record requirement|Retain the minimum necessary; delete the remainder|
|Active customer relationship|Retain for service delivery; delete when the relationship ends|
|Consent withdrawn|Delete unless another legal basis applies|

### 8.3 Sub-processor data deletion

For data processed by the sub-processors listed in the Vendor Management Policy:

1. **PropelAuth**: authentication data is deleted on an account closure request
2. **AWS**: infrastructure data is managed per this policy; AWS does not retain customer data beyond service delivery

Sub-processor obligations are set in Data Processing Agreements, as described in the Vendor Management Policy.

## 9. Monitoring and audit

### 9.1 Retention compliance metrics

|**Metric**|**Target**|**Monitoring method**|
|---|---|---|
|Automated deletion success rate|>99 %|CloudWatch metrics|
|Data past its retention period|0 records|Daily automated Lambda check|
|Legal hold compliance|100 %|Manual review|
|Disposal verification completion|100 %|Audit log review|

Monitoring procedures are in the System Monitoring and Logging Procedure.

### 9.2 Quarterly review

The CEO:

- Verifies that the automated retention processes are functioning
- Reviews exception logs and manual interventions
- Confirms that legal holds are current and justified
- Validates disposal certificates for any physical media

### 9.3 Annual audit

The CEO:

- Reviews whether the retention schedule is still appropriate
- Verifies the effectiveness of the disposal methods
- Assesses changes in regulatory requirements
- Updates retention periods as needed

### 9.4 Audit evidence

- Automated deletion logs (CloudWatch, CloudTrail)
- Retention policy configurations (CloudFormation)
- Legal hold records in the compliance platform
- Data subject request records
- Disposal verification reports

### 9.5 Reporting

Monthly retention compliance reports include:

- Volume of data deleted by category
- Exceptions and manual interventions
- Legal hold status
- Data subject erasure requests processed
- Compliance metrics and trends

## 10. Retention incidents

### 10.1 Retention-related incidents

The following retention failures are handled as incidents:

- Premature data deletion (before the retention period expires)
- Failure to delete data after the retention period expires
- Unauthorized data deletion
- Legal hold violations
- Disposal verification failures

### 10.2 Response

On identifying a retention-related incident, the CEO:

1. **Contains**: halts the affected automated processes
2. **Assesses**: determines the scope and impact
3. **Recovers**: restores prematurely deleted data from backups where applicable
4. **Remediates**: executes overdue deletions or corrects the process failure
5. **Reports**: documents the incident per the Incident Response Procedure
6. **Improves**: updates processes to prevent recurrence

Incidents are recorded in the incident reporting module of the compliance platform.

## 11. Training and awareness

All personnel with data handling responsibilities complete:

- **Initial training**: data retention and disposal procedures at onboarding
- **Annual refresher**: updates on retention requirements and disposal methods
- **Role-specific training**: the CEO, as operator of the automated retention systems, maintains detailed knowledge of those systems

Training is delivered through the Security Awareness Training Program in the compliance platform portal and covers the retention schedule by data type, secure disposal requirements, legal hold procedures, data subject rights obligations, and how to report retention concerns.

## 12. Policy review and exceptions

### 12.1 Review

The CEO reviews this policy:

- **Annually**
- **On regulatory change**: changes to GDPR, CCPA, or SOC 2 requirements
- **On business change**: new data types, systems, or processing activities
- **After an incident**: following any retention-related incident

The policy is approved by the CEO and is effective on publication.

### 12.2 Exceptions

An exception to this policy requires:

1. Written justification of the business need
2. A risk assessment of the exception
3. Approval by the CEO
4. A time limit with a review date
5. A record in the compliance platform

## 13. Related documents

- Data Classification and Handling Standard
- Information Security Policy
- Privacy Notice and Data Processing Agreement Template
- Data Subject Rights Request Procedure
- Business Continuity Plan
- Encryption and Cryptographic Controls Standard
- Incident Response Procedure
- System Monitoring and Logging Procedure
- Vendor Management Policy

## 14. Appendices

### Appendix A: Retention decision flowchart

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

### Appendix B: AWS service retention configuration

|**AWS service**|**Retention setting**|**Configuration method**|
|---|---|---|
|CloudWatch Logs|90 days|Log group retention policy|
|CloudTrail|7 years|S3 lifecycle policy (Glacier after 1 year) with Object Lock|
|DocumentDB backups|90 days|Automated backup retention|
|ECR images|90 days (deprecated)|Lifecycle policy|
|S3 objects|Per data type|Lifecycle rules|

### Appendix C: Compliance mapping

|**Requirement**|**Policy section**|**Control**|
|---|---|---|
|SOC 2 CC6.5|§6, §7|Secure disposal of data|
|SOC 2 C1.2|§5|Confidential information disposal|
|GDPR Art. 5(1)(e)|§5|Storage limitation|
|GDPR Art. 17|§8|Right to erasure|
|CCPA §1798.105|§8|Right to deletion|

## Revision history

|**Version**|**Date**|**Author**|**Changes**|
|---|---|---|---|
|1.0|November 13, 2025|Deal Intelligence|Initial policy (finalized in the compliance platform February 2, 2026)|
|2.0|<to be set at publication>|Mo Messidi|Scope limited to Security, Availability and Confidentiality; account data retention set to relationship + 24 months; CloudWatch Logs 90 days, CloudTrail 7 years via S3 lifecycle and Object Lock; legal holds managed in the compliance platform; roles consolidated to the CEO; this document is the single retention schedule|
