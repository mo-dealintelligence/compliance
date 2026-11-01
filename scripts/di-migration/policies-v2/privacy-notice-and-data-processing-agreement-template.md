---
title: "Privacy Notice and Data Processing Agreement Template"
doc_type: "Template"
version: "2.0"
supersedes: "1.0"
acknowledgment: "None"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "privacy-notice-and-data-processing-agreement-template-v1.0.pdf"
---

# Privacy Notice and Data Processing Agreement Template

## 1. Purpose

This template provides the standard language Deal Intelligence LLC uses to communicate its data processing practices to data subjects and to formalize data protection commitments with customers under the General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA).

It implements the privacy requirements of the Information Security Policy and supplies the language for customer agreements, privacy notices, and data processing addenda.

## 2. Scope

This template applies to:

- All customer contracts requiring data processing agreements
- Privacy notices displayed on the Deal Intelligence platform
- Sub-processor agreements with the sub-processors listed in the Vendor Management Policy
- Data subject rights request communications
- Breach notification templates
- International data transfer mechanisms
- Cookie policies and consent mechanisms

## 3. Privacy notice template

**DEAL INTELLIGENCE LLC PRIVACY NOTICE**

**Effective date:** [Date]\
**Last updated:** [Date]

### 3.1 Data controller information

Deal Intelligence LLC ("Deal Intelligence," "we," "us," or "our")\
[Company Address]\
Data protection contact: Chief Executive Officer\
Contact: privacy@dealintelligence.io

### 3.2 Data we collect

In accordance with our Data Classification and Handling Standard, we collect and process the following.

**Business contact information**

- First name and last name
- Business email address
- LinkedIn profile URL
- Job title and current employer
- Company name and domain
- Lead qualification status
- Sourcing dates

**Customer account data**

- Organization details
- User authentication credentials (managed by PropelAuth)
- Service usage metrics
- Billing information (if applicable)

**Technical data**

- IP addresses and device identifiers
- Browser type and version
- Access logs and timestamps
- API usage patterns

### 3.3 Legal basis for processing

We process personal data under the following legal bases:

|**Processing activity**|**Legal basis**|**Retention period**|
|---|---|---|
|B2B intelligence services|Legitimate interest|24 months for active leads|
|Customer account management|Contract performance|Duration of the relationship + 24 months|
|Security monitoring|Legal obligation|90 days per the System Monitoring and Logging Procedure|
|Marketing communications|Consent|Until withdrawn|

### 3.4 Data sharing and sub-processors

We maintain a minimal sub-processor model as defined in our Vendor Management Policy.

**Current sub-processors**

- **AWS (Amazon Web Services):** Cloud infrastructure and data storage (us-east-1)
- **PropelAuth:** Authentication and identity management
- **Google Workspace:** Email, documents, and personnel sign-in
- **GitHub:** Source code hosting and CI
- **Resend:** Transactional email delivery
- **Compliance platform:** Self-hosted on AWS within our own infrastructure

Customer-controlled integrations (Slack, CRM systems) are governed by the Integration security section of the API Security and Rate Limiting Standard.

### 3.5 Data security

We implement the following security measures:

- AES-256 encryption at rest via KMS
- TLS 1.2+ encryption in transit
- Multi-factor authentication for personnel enforced in Google Workspace, GitHub, and AWS; customer sign-in through Google Workspace via PropelAuth
- Role-based access control
- Security monitoring through CloudWatch alarms and Security Hub, with real-time alerting for critical findings

Reference: Encryption and Cryptographic Controls Standard

### 3.6 Data subject rights

Under GDPR and CCPA, data subjects have the right to:

- Access their personal data
- Rectify inaccurate data
- Request erasure ("right to be forgotten")
- Restrict processing
- Receive their data in a portable format
- Object to processing
- Withdraw consent

To exercise these rights, contact privacy@dealintelligence.io.

Requests are processed according to our Data Subject Rights Request Procedure within 30 days (GDPR) or 45 days (CCPA).

### 3.7 International data transfers

Data may be transferred to the United States, where our AWS infrastructure is located (us-east-1). We provide safeguards through:

- Standard Contractual Clauses (SCCs)
- Technical and organizational measures covered by our SOC 2 report (Security, Availability, and Confidentiality)
- Encryption of all data transfers

### 3.8 Data breach notification

In the event of a personal data breach, we will notify affected customers within 48 hours of discovery, and the supervisory authority within 72 hours where GDPR applies, in accordance with our Incident Response Procedure.

## 4. Data Processing Agreement template

**DATA PROCESSING AGREEMENT**

This Data Processing Agreement ("DPA") forms part of the Service Agreement between Deal Intelligence LLC ("Processor") and [Customer Name] ("Controller").

### 4.1 Definitions

Terms used in this DPA shall have the meanings set forth in the GDPR, unless otherwise defined:

- **"Personal Data"**: Business contact information as defined in Section 3.2
- **"Processing"**: Any operation performed on Personal Data
- **"Sub-Processor"**: Third-party service providers listed in Section 4.5
- **"Data Breach"**: As defined in Article 4(12) of the GDPR

### 4.2 Processing instructions

The Processor shall:

- Process Personal Data only on documented instructions from the Controller
- Ensure that persons authorized to process Personal Data have committed to confidentiality
- Implement appropriate technical and organizational measures per the Information Security Policy
- Maintain records of processing activities

### 4.3 Security measures

The Processor implements the following security measures.

**Technical measures**

- KMS encryption for data at rest (AES-256)
- TLS 1.2+ for data in transit
- VPC isolation with private subnets
- CloudTrail audit logging
- Security Hub continuous monitoring

**Organizational measures**

- Annual security awareness training per the Security Awareness Training Program
- Quarterly risk assessments via the compliance platform Risk Assessment module
- Incident response procedures with 48-hour notification
- Annual penetration testing per the Penetration Testing and Security Assessment Procedure

### 4.4 Data subject rights

The Processor shall:

- Assist the Controller in responding to data subject requests within the statutory timelines (30 days under GDPR / 45 days under CCPA)
- Implement technical measures to support data portability
- Perform data deletion and rectification per the Data Subject Rights Request Procedure
- Maintain audit logs of all data subject request fulfillment

### 4.5 Sub-processing

**Authorized Sub-Processors**: The Controller consents to the engagement of:

- AWS for infrastructure services
- PropelAuth for authentication services
- Google Workspace for email, documents, and personnel sign-in
- GitHub for source code hosting and CI
- Resend for transactional email delivery
- The compliance platform, self-hosted on AWS within the Processor's own infrastructure

**Sub-Processor changes**

- 30 days' advance notice of any Sub-Processor change
- Right to object within the notice period
- Alternative arrangements or termination rights if the objection is reasonable

### 4.6 Data breach response

Upon becoming aware of a Personal Data breach, the Processor shall:

- Notify the Controller within 48 hours, with the incident information confirmed at that time
- Support the Controller's notification to the supervisory authority within 72 hours where GDPR applies
- Cooperate with the Controller's breach response
- Document all breaches in the compliance platform's Incident Reporting system

Reference: Incident Response Procedure

### 4.7 Audit rights

The Controller may exercise audit rights through:

- The Processor's SOC 2 report (Security, Availability, and Confidentiality), available on request under NDA
- Quarterly security assessments
- On-demand compliance attestations
- Third-party security certifications

### 4.8 Data return and deletion

Upon termination:

- All Personal Data returned within 30 days
- Certified deletion of all copies
- Retention only as required by law
- Deletion certificates provided

Reference: Data Retention and Disposal Policy

### 4.9 Liability and indemnification

- Liability caps aligned with the Service Agreement
- Mutual indemnification for data protection violations
- Exclusions for consequential damages

## 5. Breach notification templates

### 5.1 Customer breach notification

**Subject: Important Security Update Regarding Your Deal Intelligence Account**

Dear [Customer Name],

We are writing to inform you of a security incident that may have affected your account data.

**What happened:** [Description of incident]

**Information involved:** [Specific data types affected]

**What we are doing:**

- Immediate containment measures implemented
- Full investigation underway
- Additional security controls deployed
- Coordination with law enforcement (if applicable)

**What you should do:** [Specific recommended actions]

**For more information:** Contact our Chief Executive Officer at privacy@dealintelligence.io

We take the security of your data seriously and apologize for any inconvenience.

Sincerely,\
Chief Executive Officer, Deal Intelligence LLC

### 5.2 Regulatory authority notification

**GDPR Article 33 breach notification**

1. **Nature of the breach:** [Categories and approximate number of data subjects and records]
2. **Contact details:** Chief Executive Officer, [Name]; email privacy@dealintelligence.io; phone [Number]
3. **Likely consequences:** [Assessment of potential impact]
4. **Measures taken:** [Technical and organizational measures implemented]
5. **Documentation:** Incident logged in the compliance platform Incident Reporting system, reference [Incident ID]

## 6. Cookie policy template

**COOKIE POLICY**

Deal Intelligence uses cookies and similar technologies to:

- Maintain session security
- Remember user preferences
- Analyze platform usage
- Improve service performance

**Types of cookies**

|**Cookie type**|**Purpose**|**Duration**|**Opt-out**|
|---|---|---|---|
|Essential|Authentication, security|Session|Not available|
|Functional|User preferences|30 days|Via settings|
|Analytics|Usage statistics|90 days|Via settings|
|Performance|CDN optimization|7 days|Via settings|

**Managing cookies:** Users can manage cookie preferences through account settings or browser controls.

## 7. International data transfer mechanisms

### 7.1 Standard Contractual Clauses

The following SCCs are incorporated by reference:

- Module 1: Controller to Controller transfers
- Module 2: Controller to Processor transfers
- Module 3: Processor to Processor transfers
- Module 4: Processor to Controller transfers

### 7.2 Transfer impact assessment

**Assessment factors**

- Laws of the destination country (United States)
- Technical security measures (encryption, access controls)
- Organizational measures (policies, training)
- Sub-processor commitments

**Supplementary measures**

- End-to-end encryption for sensitive data
- Pseudonymization where feasible
- Enhanced access controls
- Regular security assessments

## 8. Consent management

### 8.1 Consent collection template

**Marketing consent:**

☐ I consent to receive marketing communications from Deal Intelligence

☐ I consent to data processing for service improvement purposes

**Consent withdrawal:** You may withdraw consent at any time by:

- Clicking unsubscribe in any email
- Updating preferences in account settings
- Contacting privacy@dealintelligence.io

### 8.2 Consent records

Consent records include:

- Identity of the data subject
- Specific consent granted
- Timestamp of consent
- Method of collection
- Withdrawal date (if applicable)

## 9. Privacy impact assessment template

### 9.1 PIA triggers

PIAs are conducted for:

- New data processing activities
- Changes to existing processing
- New sub-processor engagement
- International data transfers
- High-risk processing operations

### 9.2 PIA documentation

Each PIA documents:

- Processing purpose and necessity
- Data minimization assessment
- Security risk evaluation
- Compliance verification
- Mitigation measures

Reference: Risk Assessment Procedure

## 10. Compliance monitoring

### 10.1 Privacy metrics

The CEO tracks and reports:

- Data subject request response times
- Breach notification timeliness
- Consent rates and withdrawals
- Sub-processor compliance status
- Privacy training completion

### 10.2 Regular reviews

- Quarterly privacy assessments via the compliance platform Risk Assessment module
- Annual DPA reviews and updates
- Semi-annual consent audit
- Annual tabletop exercise recorded in the compliance platform

## 11. Implementation guidelines

### 11.1 Document deployment

1. Customize the templates with organization-specific information
2. Legal review by qualified counsel
3. Integration with the customer onboarding process
4. Publication on the platform and website
5. Version control and change tracking

### 11.2 Training requirements

All personnel handling personal data complete training on:

- GDPR/CCPA compliance
- Privacy by design principles
- Data subject rights handling
- Breach response procedures

Reference: Security Awareness Training Program

## 12. Review

This template is reviewed annually and updated for:

- Changes in privacy regulations
- New processing activities
- Sub-processor modifications
- Lessons learned from incidents
- Customer feedback and requirements

Updates are managed through the Change Management Policy, with stakeholder notification.

## 13. Related documents

- Information Security Policy
- Data Classification and Handling Standard
- Data Retention and Disposal Policy
- Data Subject Rights Request Procedure
- Incident Response Procedure
- Vendor Management Policy
- Access Control and Authentication Policy
- Encryption and Cryptographic Controls Standard
- API Security and Rate Limiting Standard
- System Monitoring and Logging Procedure
- Security Awareness Training Program
- Penetration Testing and Security Assessment Procedure
- Risk Assessment Procedure
- Change Management Policy

## 14. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Retyped as Template (no acknowledgment); scope limited to GDPR and CCPA; breach notification set to 48 hours to customers / 72 hours to the authority (24-hour promise removed); DSR assistance set to 30/45 days; SOC 2 report available on request under NDA; sub-processor list aligned to the Vendor Management Policy; account data retention set to relationship + 24 months; roles consolidated to CEO |
