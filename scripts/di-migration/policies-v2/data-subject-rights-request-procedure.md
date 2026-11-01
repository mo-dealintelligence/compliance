---
title: "Data Subject Rights Request Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "data-subject-rights-request-procedure-v1.0.pdf"
---

# Data Subject Rights Request Procedure

## 1. Purpose

This Data Subject Rights Request Procedure establishes the operational framework for receiving, validating, processing, and responding to data subject requests in accordance with the General Data Protection Regulation (GDPR) Articles 15-22 and the California Consumer Privacy Act (CCPA) Sections 1798.100-1798.130. This procedure ensures that Deal Intelligence LLC fulfills its obligations to data subjects while maintaining the security and integrity of the platform.

Deal Intelligence acts as a data controller for the business contact information it compiles and delivers through the platform, and as a data processor for data that customers upload to or hold within their own accounts (see Section 6.2). [CONFIRM: controller/processor framing — v1 did not state it explicitly]

This procedure operationalizes the privacy principles defined in the Information Security Policy and implements the technical controls specified in the Data Retention and Disposal Policy to ensure timely and compliant responses to data subject requests.

## 2. Scope

This procedure applies to:

- All requests from data subjects exercising their rights under GDPR, CCPA, or other applicable privacy regulations

- Business contact information processed through the platform, including:

   - First name, last name, business email address

   - LinkedIn profile URLs and job titles

   - Current employer and company information

   - Competitor interaction data and lead qualification status

- All personnel responsible for processing data subject requests

- The manual processes for request fulfillment described in Section 9

- Sub-processors involved in data processing, as listed in the Vendor Management Policy

This procedure excludes requests relating to personnel data, which are handled directly by the CEO.

## 3. Data Subject Rights Overview

### 3.1 Rights Under GDPR

Deal Intelligence recognizes the following rights for EU data subjects:

|**Right**|**Description**|**Response Timeline**|
|---|---|---|
|Access (Article 15)|Obtain confirmation and copy of personal data|30 days|
|Rectification (Article 16)|Correct inaccurate personal data|30 days|
|Erasure (Article 17)|Delete personal data ("right to be forgotten")|30 days|
|Portability (Article 20)|Receive data in machine-readable format|30 days|
|Objection (Article 21)|Object to processing based on legitimate interests|30 days|
|Automated Decision-Making (Article 22)|Not be subject to solely automated decisions|30 days|

### 3.2 Rights Under CCPA

California residents are entitled to:

|**Right**|**Description**|**Response Timeline**|
|---|---|---|
|Know (§1798.100)|Information about data collection and use|45 days|
|Delete (§1798.105)|Request deletion of personal information|45 days|
|Opt-Out (§1798.120)|Opt-out of sale of personal information|Immediate|
|Non-Discrimination (§1798.125)|Equal service regardless of rights exercise|Ongoing|

## 4. Request Intake and Validation

### 4.1 Submission Channels

Data subjects may submit requests through:

- **Primary Channel** : Dedicated email address: privacy@dealintelligence.io

- **Secondary Channel** : Authenticated customer portal via PropelAuth

- **Tertiary Channel** : Written request to registered business address

All requests are recorded by the CEO as a dated entry in the compliance platform for tracking and audit purposes.

### 4.2 Identity Verification

Before processing any request, identity verification is required:

1. **Email Verification** : Confirmation email sent to registered business email address

2. **PropelAuth Authentication** : For portal submissions, JWT token validation

3. **Additional Verification** : For sensitive requests, additional documentation may be required:

   - Company domain verification

   - LinkedIn profile matching

   - Recent interaction history validation

### 4.3 Request Validation Criteria

Requests must include:

- Full name and business email address

- Specific right being exercised

- Sufficient detail to locate the data

- Preferred response format (where applicable)

## 5. Processing Procedures by Request Type

### 5.1 Access Requests

**Timeline** : 30 days (GDPR) / 45 days (CCPA)

**Process** :

1. **Data Discovery (Days 1-5)**

   - Query DocumentDB collections for business contact records by email address and company domain

   - Search CloudWatch logs for processing activities (90-day retention)

   - Review lead qualification and competitor interaction data

   - Check PropelAuth user records

   - Check HubSpot CRM records

2. **Data Compilation (Days 6-10)**

   - Extract data from all identified sources

   - Format according to Data Classification and Handling Standard

   - Apply PII sanitization for third-party data

   - Generate processing activity summary

3. **Review and Delivery (Days 11-30)**

   - Review by the CEO for exemptions or restrictions

   - Encrypt response per Encryption and Cryptographic Controls Standard

   - Deliver via secure channel (encrypted email or portal download)

   - Document completion as a dated entry in the compliance platform

### 5.2 Deletion Requests

**Timeline** : 30 days (GDPR) / 45 days (CCPA)

**Process** :

1. **Exemption Assessment (Days 1-3)**

   - Verify no legal hold per Data Retention and Disposal Policy

   - Check contractual obligations for active leads (24-month retention)

   - Review regulatory requirements (7-year financial records)

2. **Deletion Execution (Days 4-15)**

   - Locate and delete the records from DocumentDB collections by email address and company domain

   - Delete the PropelAuth user record where one exists

   - Delete the HubSpot CRM record where one exists

   - Backup copies expire under the 90-day backup retention cycle and are not restored

   - Clear CloudWatch logs where permissible

3. **Confirmation (Days 16-30)**

   - Verify deletion across all systems

   - Record a dated deletion entry in the compliance platform

   - Send confirmation to data subject

   - Maintain deletion log per compliance requirements

### 5.3 Rectification Requests

**Timeline** : 30 days

**Process** :

1. **Data Location (Days 1-3)**

   - Identify all instances of incorrect data

   - Document current values and requested corrections

2. **Update Execution (Days 4-10)**

   - Update DocumentDB records via authenticated API

   - Propagate changes to derived datasets

   - Update lead qualification status if affected

   - Synchronize with customer-delivered leads

3. **Verification (Days 11-30)**

   - Confirm updates across all systems

   - Send confirmation with updated data copy

   - Log changes in audit trail

### 5.4 Portability Requests

**Timeline** : 30 days

**Process** :

1. **Data Export (Days 1-10)**

   - Generate JSON or CSV export from DocumentDB

   - Include all business contact information

   - Format according to industry standards

2. **Delivery (Days 11-30)**

   - Encrypt file per Encryption and Cryptographic Controls Standard

   - Provide via secure download link (7-day expiration)

   - Include data dictionary and field descriptions

## 6. Special Considerations

### 6.1 Third-Party Data

For data sourced from third parties or public sources:

- Verification of data subject identity requires enhanced validation

- Deletion may be limited to Deal Intelligence systems only

- Clear communication about data source and limitations

### 6.2 Customer-Controlled Data

For data within customer accounts, where Deal Intelligence acts as processor:

- Requests forwarded to customer organization for processing

- Deal Intelligence provides technical support only

- Customer responsible for response timeline compliance

### 6.3 Technical Limitations

Certain technical constraints may affect request fulfillment:

- Backup data follows 90-day rotation cycle

- CloudTrail audit logs retained for 7 years (immutable)

- Aggregated or anonymized data excluded from individual requests

## 7. Response Management

### 7.1 Communication Standards

All responses must:

- Use clear, plain language avoiding technical jargon

- Specify the right exercised and actions taken

- Include relevant privacy notice excerpts per Privacy Notice and Data Processing Agreement Template

- Provide contact information for follow-up questions

### 7.2 Extension Procedures

If additional time is required:

- Notify data subject within initial timeline

- Provide specific reason for delay

- Maximum extension: 2 additional months (GDPR) / 45 additional days (CCPA)

- Document extension in the compliance platform

### 7.3 Denial Procedures

If a request must be denied:

- Provide specific legal basis for denial

- Explain data subject's right to appeal

- Document supervisory authority complaint procedures

- Maintain denial documentation for 24 months minimum

## 8. Roles and Responsibilities

### 8.1 Chief Executive Officer

The CEO is the data protection contact and owns this procedure end to end:

- Overall procedure oversight and compliance

- Complex request adjudication

- Legal hold determinations

- Regulatory authority communications

- Annual procedure review and updates

- Day-to-day request processing

- Identity verification procedures

- Response quality assurance

- Compliance platform administration

- Database query execution for data discovery

- System access for data updates/deletions

- Backup and archive data management

- Removal of PropelAuth user records

### 8.2 Go-to-Market Contractor

- Forwards any data subject request received to privacy@dealintelligence.io on receipt

- Does not process requests and has no production access

## 9. Runbook and Tools

### 9.1 Manual Runbook

Every request is processed by the CEO through the same manual runbook:

1. **Verify identity** per Section 4.2

2. **Locate records** : DocumentDB collections by email address and company domain; the PropelAuth user; the HubSpot CRM record

3. **Act** : export, rectify or delete per Section 5

4. **Record** : a dated entry in the compliance platform with the request type, date received, action taken and date completed

### 9.2 Manual Oversight

The CEO personally reviews:

- Identity verification for sensitive requests

- Legal exemption assessments

- Complex multi-system deletions

- Customer communication and escalations

### 9.3 Compliance Platform Integration

The compliance platform provides:

- Centralized request tracking as dated entries with due dates

- Audit trail for all request activities

- Compliance reporting and metrics

## 10. Metrics and Reporting

### 10.1 Key Performance Indicators

|**Metric**|**Target**|**Measurement Frequency**|
|---|---|---|
|Average Response Time|<20 days|Monthly|
|On-Time Response Rate|>95%|Monthly|
|Request Volume|Baseline tracking|Monthly|
|Denial Rate|<5%|Quarterly|
|Extension Rate|<10%|Quarterly|

### 10.2 Compliance Reporting

Monthly reports recorded in the compliance platform include:

- Total requests by type and jurisdiction

- Response time distribution

- Exemption and denial analysis

- Process improvement opportunities

## 11. Training and Awareness

All personnel involved in data subject request processing must:

- Complete privacy training per Security Awareness Training Program

- Understand GDPR and CCPA requirements

- Practice identity verification procedures

## 12. Integration with Incident Response

Data subject requests may trigger broader actions:

- Multiple deletion requests may indicate a data breach per Incident Response Procedure

- Access requests may reveal unauthorized processing requiring investigation

- Patterns of requests monitored via System Monitoring and Logging Procedure

## 13. Related Documents

- Information Security Policy

- Data Retention and Disposal Policy

- Privacy Notice and Data Processing Agreement Template

- Data Classification and Handling Standard

- Access Control and Authentication Policy

- Encryption and Cryptographic Controls Standard

- Incident Response Procedure

- Security Awareness Training Program

- System Monitoring and Logging Procedure

- Vendor Management Policy

## 14. Review and Updates

This procedure shall be reviewed annually and updated to reflect:

- Changes in privacy regulations

- Lessons learned from request processing

- Technical capability enhancements

- Audit findings and recommendations

The next scheduled review date is 12 months from the initial approval date, with interim updates as required by regulatory changes or operational improvements identified through the compliance platform metrics.

## 15. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Scope limited to GDPR and CCPA; roles consolidated to CEO and Go-to-Market Contractor; automated DSR processing replaced by the manual runbook (DocumentDB, PropelAuth, HubSpot, compliance platform entry); 72-hour restriction commitment removed; contact address corrected to privacy@dealintelligence.io; controller/processor roles stated |
