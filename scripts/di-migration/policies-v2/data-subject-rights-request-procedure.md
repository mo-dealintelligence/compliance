---
title: "Data Subject Rights Request Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "data-subject-rights-request-procedure-v1.0.pdf"
---

# Data Subject Rights Request Procedure

## 1. Purpose

This procedure defines how Deal Intelligence LLC receives, validates, processes, and responds to data subject requests under the General Data Protection Regulation (GDPR) Articles 15–22 and the California Consumer Privacy Act (CCPA) Sections 1798.100–1798.130, while maintaining the security and integrity of the platform.

Deal Intelligence acts as a data controller for the business contact information it compiles and delivers through the platform, and as a data processor for data that customers upload to or hold within their own accounts (see Section 7.2). [CONFIRM: D14 open — pending investigation]

This procedure implements the privacy principles of the Information Security Policy and the technical controls of the Data Retention and Disposal Policy for timely, compliant responses to data subject requests.

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

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

The CEO is the data protection contact and owns this procedure end to end:

- Overall procedure oversight and compliance
- Complex request adjudication
- Legal hold determinations
- Regulatory authority communications
- Annual procedure review and updates
- Day-to-day request processing
- Identity verification
- Response quality assurance
- Compliance platform administration
- Database query execution for data discovery
- System access for data updates and deletions
- Backup and archive data management
- Removal of PropelAuth user records

### 3.2 Go-to-Market Contractor

- Forwards any data subject request received to privacy@dealintelligence.io on receipt
- Does not process requests and has no production access

## 4. Data subject rights overview

### 4.1 Rights under GDPR

Deal Intelligence recognizes the following rights for EU data subjects:

|**Right**|**Description**|**Response timeline**|
|---|---|---|
|Access (Article 15)|Obtain confirmation and a copy of personal data|30 days|
|Rectification (Article 16)|Correct inaccurate personal data|30 days|
|Erasure (Article 17)|Delete personal data ("right to be forgotten")|30 days|
|Restriction (Article 18)|Restrict processing of personal data while accuracy or an objection is being verified|30 days|
|Portability (Article 20)|Receive data in a machine-readable format|30 days|
|Objection (Article 21)|Object to processing based on legitimate interests|30 days|
|Automated decision-making (Article 22)|Not be subject to solely automated decisions|30 days|

### 4.2 Rights under CCPA

California residents are entitled to:

|**Right**|**Description**|**Response timeline**|
|---|---|---|
|Know (§1798.100)|Information about data collection and use|45 days|
|Delete (§1798.105)|Request deletion of personal information|45 days|
|Opt-out (§1798.120)|Opt out of the sale of personal information|Immediate|
|Non-discrimination (§1798.125)|Equal service regardless of rights exercised|Ongoing|

## 5. Request intake and validation

### 5.1 Submission channels

Data subjects may submit requests through:

- **Primary channel**: Dedicated email address, privacy@dealintelligence.io
- **Secondary channel**: Authenticated customer portal via PropelAuth
- **Tertiary channel**: Written request to the registered business address

The CEO records every request as a dated entry in the compliance platform for tracking and audit purposes.

### 5.2 Identity verification

Identity is verified before any request is processed:

1. **Email verification**: Confirmation email sent to the registered business email address
2. **PropelAuth authentication**: For portal submissions, JWT token validation
3. **Additional verification**: For sensitive requests, additional documentation may be required:
   - Company domain verification
   - LinkedIn profile matching
   - Recent interaction history validation

### 5.3 Request validation criteria

Requests must include:

- Full name and business email address
- The specific right being exercised
- Sufficient detail to locate the data
- Preferred response format (where applicable)

## 6. Processing procedures by request type

### 6.1 Access requests

**Timeline**: 30 days (GDPR) / 45 days (CCPA)

**Process**:

1. **Data discovery (days 1–5)**
   - Query DocumentDB collections for business contact records by email address and company domain
   - Search CloudWatch logs for processing activities (90-day retention)
   - Review lead qualification and competitor interaction data
   - Check PropelAuth user records
   - Check HubSpot CRM records
2. **Data compilation (days 6–10)**
   - Extract data from all identified sources
   - Format according to the Data Classification and Handling Standard
   - Apply PII sanitization for third-party data
   - Generate a processing activity summary
3. **Review and delivery (days 11–30)**
   - Review by the CEO for exemptions or restrictions
   - Encrypt the response per the Encryption and Cryptographic Controls Standard
   - Deliver via a secure channel (encrypted email or portal download)
   - Document completion as a dated entry in the compliance platform

### 6.2 Deletion requests

**Timeline**: 30 days (GDPR) / 45 days (CCPA)

**Process**:

1. **Exemption assessment (days 1–3)**
   - Verify no legal hold per the Data Retention and Disposal Policy
   - Check contractual obligations for active leads (24-month retention)
   - Review regulatory requirements (7-year financial records)
2. **Deletion execution (days 4–15)**
   - Locate and delete the records from DocumentDB collections by email address and company domain
   - Delete the PropelAuth user record where one exists
   - Delete the HubSpot CRM record where one exists
   - Backup copies expire under the 90-day backup retention cycle and are not restored
   - Clear CloudWatch logs where permissible
3. **Confirmation (days 16–30)**
   - Verify deletion across all systems
   - Record a dated deletion entry in the compliance platform
   - Send confirmation to the data subject
   - Maintain the deletion log per compliance requirements

### 6.3 Rectification requests

**Timeline**: 30 days

**Process**:

1. **Data location (days 1–3)**
   - Identify all instances of the incorrect data
   - Document current values and requested corrections
2. **Update execution (days 4–10)**
   - Update DocumentDB records via the authenticated API
   - Propagate changes to derived datasets
   - Update lead qualification status if affected
   - Synchronize with customer-delivered leads
3. **Verification (days 11–30)**
   - Confirm updates across all systems
   - Send confirmation with a copy of the updated data
   - Log changes in the audit trail

### 6.4 Portability requests

**Timeline**: 30 days

**Process**:

1. **Data export (days 1–10)**
   - Generate a JSON or CSV export from DocumentDB
   - Include all business contact information
   - Format according to industry standards
2. **Delivery (days 11–30)**
   - Encrypt the file per the Encryption and Cryptographic Controls Standard
   - Provide via a secure download link (7-day expiration)
   - Include a data dictionary and field descriptions

### 6.5 Restriction requests

**Timeline**: 30 days

**Process** (manual):

1. **Assessment (days 1–5)**
   - Confirm the ground for restriction (contested accuracy, pending objection, unlawful processing, or data needed for legal claims)
   - Locate the records in DocumentDB by email address and company domain
2. **Restriction execution (days 6–15)**
   - The CEO manually marks the records as restricted so that they are excluded from lead delivery and further processing, other than storage, until the restriction is lifted
   - Record the restriction as a dated entry in the compliance platform
3. **Confirmation (days 16–30)**
   - Notify the data subject that the restriction is in place
   - Notify the data subject before the restriction is lifted

## 7. Special considerations

### 7.1 Third-party data

For data sourced from third parties or public sources:

- Verification of the data subject's identity requires enhanced validation
- Deletion may be limited to Deal Intelligence systems only
- The response states the data source and any limitations

### 7.2 Customer-controlled data

For data within customer accounts, where Deal Intelligence acts as processor:

- Requests are forwarded to the customer organization for processing
- Deal Intelligence provides technical support only
- The customer is responsible for meeting the response timeline

### 7.3 Technical limitations

The following constraints may affect request fulfillment:

- Backup data follows a 90-day rotation cycle
- CloudTrail audit logs are retained for 7 years (immutable)
- Aggregated or anonymized data is excluded from individual requests

## 8. Response management

### 8.1 Communication standards

All responses must:

- Use clear, plain language without technical jargon
- Specify the right exercised and the actions taken
- Include relevant privacy notice excerpts per the Privacy Notice and Data Processing Agreement Template
- Provide contact information for follow-up questions

### 8.2 Extension procedures

If additional time is required:

- Notify the data subject within the initial timeline
- Give the specific reason for the delay
- Maximum extension: 2 additional months (GDPR) / 45 additional days (CCPA)
- Document the extension in the compliance platform

### 8.3 Denial procedures

If a request must be denied:

- Give the specific legal basis for the denial
- Explain the data subject's right to appeal
- State the supervisory authority complaint procedures
- Retain the denial documentation for at least 24 months

## 9. Runbook and tools

### 9.1 Manual runbook

The CEO processes every request through the same manual runbook:

1. **Verify identity** per Section 5.2
2. **Locate records**: DocumentDB collections by email address and company domain; the PropelAuth user; the HubSpot CRM record
3. **Act**: export, rectify, restrict, or delete per Section 6
4. **Record**: a dated entry in the compliance platform with the request type, date received, action taken, and date completed

### 9.2 Manual oversight

The CEO reviews in particular:

- Identity verification for sensitive requests
- Legal exemption assessments
- Complex multi-system deletions
- Customer communication and escalations

### 9.3 Compliance platform

The compliance platform provides:

- Centralized request tracking as dated entries with due dates
- An audit trail for all request activities
- Compliance reporting and metrics

## 10. Training and awareness

All personnel involved in data subject request processing must:

- Complete privacy training per the Security Awareness Training Program
- Understand GDPR and CCPA requirements
- Practice identity verification procedures

## 11. Integration with incident response

Data subject requests may trigger broader actions:

- Multiple deletion requests may indicate a data breach per the Incident Response Procedure
- Access requests may reveal unauthorized processing requiring investigation
- Patterns of requests are monitored via the System Monitoring and Logging Procedure

## 12. Review

This procedure is reviewed annually and updated for:

- Changes in privacy regulations
- Lessons learned from request processing
- Technical capability enhancements
- Audit findings and recommendations

The next scheduled review date is 12 months from the initial approval date, with interim updates as required by regulatory changes or operational improvements identified through the compliance platform metrics.

## 13. Related documents

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

## 14. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Scope limited to GDPR and CCPA; roles consolidated to CEO and Go-to-Market Contractor; automated DSR processing replaced by the manual runbook (DocumentDB, PropelAuth, HubSpot, compliance platform entry); restriction (Art. 18) row restored at 30 days with a manual step; contact address corrected to privacy@dealintelligence.io; controller/processor roles stated |
