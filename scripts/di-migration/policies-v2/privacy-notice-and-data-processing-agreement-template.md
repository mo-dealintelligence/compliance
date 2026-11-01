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

This Privacy Notice and Data Processing Agreement Template establishes the standardized framework for communicating Deal Intelligence LLC's data processing practices to data subjects and formalizing data protection commitments with customers. This template ensures compliance with the General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA).

This template operationalizes the privacy requirements defined in the Information Security Policy and provides legally compliant language for customer agreements, privacy notices, and data processing addenda required for services.

## 2. Scope

This template applies to:

- All customer contracts requiring data processing agreements

- Privacy notices displayed on the Deal Intelligence platform

- Sub-processor agreements with the sub-processors listed in the Vendor Management Policy

- Data subject rights request communications

- Breach notification templates

- International data transfer mechanisms

- Cookie policies and consent mechanisms

## 3. Privacy Notice Template

### 3.1 Standard Privacy Notice

#### DEAL INTELLIGENCE LLC PRIVACY NOTICE

**Effective Date:** [Date]\ **Last Updated:** [Date]

#### 3.1.1 Data Controller Information

Deal Intelligence LLC ("Deal Intelligence," "we," "us," or "our")\ [Company Address]\ Data protection contact: Chief Executive Officer\ Contact: privacy@dealintelligence.io

#### 3.1.2 Data We Collect

In accordance with our Data Classification and Handling Standard, we collect and process:

#### Business Contact Information:

- First name and last name

- Business email address

- LinkedIn profile URL

- Job title and current employer

- Company name and domain

- Lead qualification status

- Sourcing dates

#### Customer Account Data:

- Organization details

- User authentication credentials (managed by PropelAuth)

- Service usage metrics

- Billing information (if applicable)

#### Technical Data:

- IP addresses and device identifiers

- Browser type and version

- Access logs and timestamps

- API usage patterns

#### 3.1.3 Legal Basis for Processing

We process personal data under the following legal bases:

|**Processing Activity**|**Legal Basis**|**Retention Period**|
|---|---|---|
|B2B Intelligence Services|Legitimate Interest|24 months for active leads|
|Customer Account Management|Contract Performance|Duration of the relationship + 24 months|
|Security Monitoring|Legal Obligation|90 days per System Monitoring and Logging Procedure|
|Marketing Communications|Consent|Until withdrawn|

#### 3.1.4 Data Sharing and Sub-Processors

We maintain a minimal sub-processor model as defined in our Vendor Management Policy:

#### Current Sub-Processors:

- **AWS (Amazon Web Services):** Cloud infrastructure and data storage (us-east-1)

- **PropelAuth:** Authentication and identity management

- **Google Workspace:** Email, documents and personnel sign-in

- **GitHub:** Source code hosting and CI

- **Resend:** Transactional email delivery

- **Compliance platform:** Self-hosted on AWS within our own infrastructure

Customer-controlled integrations (Slack, CRM systems) are governed by the Integration security section of the API Security and Rate Limiting Standard.

#### 3.1.5 Data Security

We implement comprehensive security measures including:

- AES-256 encryption at rest via AWS KMS

- TLS 1.2+ encryption in transit

- Multi-factor authentication for personnel enforced in Google Workspace, GitHub and AWS; customer sign-in through Google Workspace via PropelAuth

- Role-based access control

- Security monitoring through CloudWatch alarms and Security Hub, with real-time alerting for critical findings

Reference: Encryption and Cryptographic Controls Standard

#### 3.1.6 Data Subject Rights

Under GDPR and CCPA, data subjects have the right to:

- Access their personal data

- Rectify inaccurate data

- Request erasure ("right to be forgotten")

- Restrict processing

- Data portability

- Object to processing

- Withdraw consent

To exercise these rights, contact: privacy@dealintelligence.io

Requests are processed according to our Data Subject Rights Request Procedure within 30 days (GDPR) or 45 days (CCPA).

#### 3.1.7 International Data Transfers

Data may be transferred to the United States where our AWS infrastructure is located (us-east-1). We ensure appropriate safeguards through:

- Standard Contractual Clauses (SCCs)

- Technical and organizational measures covered by our SOC 2 report (Security, Availability and Confidentiality)

- Encryption of all data transfers

#### 3.1.8 Data Breach Notification

In the event of a personal data breach, we will notify affected customers within 48 hours of discovery, and the supervisory authority within 72 hours where GDPR applies, in accordance with our Incident Response Procedure.

## 4. Data Processing Agreement Template

### 4.1 Standard DPA Structure

#### DATA PROCESSING AGREEMENT

This Data Processing Agreement ("DPA") forms part of the Service Agreement between Deal Intelligence LLC ("Processor") and [Customer Name] ("Controller").

#### 4.1.1 Definitions

Terms used in this DPA shall have the meanings set forth in the GDPR, unless otherwise defined:

- **"Personal Data"** : Business contact information as defined in Section 3.1.2

- **"Processing"** : Any operation performed on Personal Data

- **"Sub-Processor"** : Third-party service providers listed in Section 4.1.5

- **"Data Breach"** : As defined in Article 4(12) of the GDPR

#### 4.1.2 Processing Instructions

The Processor shall:

- Process Personal Data only on documented instructions from the Controller

- Ensure persons authorized to process Personal Data have committed to confidentiality

- Implement appropriate technical and organizational measures per Information Security Policy

- Maintain records of processing activities

#### 4.1.3 Security Measures

The Processor implements the following security measures:

#### Technical Measures:

- AWS KMS encryption for data at rest (AES-256)

- TLS 1.2+ for data in transit

- VPC isolation with private subnets

- CloudTrail audit logging

- Security Hub continuous monitoring

#### Organizational Measures:

- Annual security awareness training per Security Awareness Training Program

- Quarterly risk assessments via the compliance platform Risk Assessment module

- Incident response procedures with 48-hour notification

- Annual penetration testing per Penetration Testing and Security Assessment Procedure

#### 4.1.4 Data Subject Rights

The Processor shall:

- Assist the Controller in responding to data subject requests within the statutory timelines (30 days under GDPR / 45 days under CCPA)

- Implement technical measures to support data portability

- Perform data deletion and rectification per the Data Subject Rights Request Procedure

- Maintain audit logs of all data subject request fulfillment

#### 4.1.5 Sub-Processing

**Authorized Sub-Processors** : The Controller consents to the engagement of:

- AWS for infrastructure services

- PropelAuth for authentication services

- Google Workspace for email, documents and personnel sign-in

- GitHub for source code hosting and CI

- Resend for transactional email delivery

- The compliance platform, self-hosted on AWS within the Processor's own infrastructure

#### Sub-Processor Changes:

- 30-day advance notice of any sub-processor changes

- Right to object within the notice period

- Alternative arrangements or termination rights if objection is reasonable

#### 4.1.6 Data Breach Response

Upon becoming aware of a Personal Data breach, the Processor shall:

- Notify the Controller within 48 hours, with the incident information confirmed at that time

- Support the Controller's notification to the supervisory authority within 72 hours where GDPR applies

- Cooperate with the Controller's breach response

- Document all breaches in the compliance platform's Incident Reporting system

Reference: Incident Response Procedure

#### 4.1.7 Audit Rights

The Controller may exercise audit rights through:

- The Processor's SOC 2 report (Security, Availability and Confidentiality), available on request under NDA

- Quarterly security assessments

- On-demand compliance attestations

- Third-party security certifications

#### 4.1.8 Data Return and Deletion

Upon termination:

- All Personal Data returned within 30 days

- Certified deletion of all copies

- Retention only as required by law

- Deletion certificates provided

Reference: Data Retention and Disposal Policy

#### 4.1.9 Liability and Indemnification

- Liability caps aligned with Service Agreement

- Mutual indemnification for data protection violations

- Exclusions for consequential damages

## 5. Breach Notification Templates

### 5.1 Customer Breach Notification

**Subject: Important Security Update Regarding Your Deal Intelligence Account**

Dear [Customer Name],

We are writing to inform you of a security incident that may have affected your account data.

**What Happened:** [Description of incident]

**Information Involved:** [Specific data types affected]

#### What We Are Doing:

- Immediate containment measures implemented

- Full investigation underway

- Additional security controls deployed

- Coordination with law enforcement (if applicable)

**What You Should Do:** [Specific recommended actions]

**For More Information** : Contact our Chief Executive Officer at privacy@dealintelligence.io

We take the security of your data seriously and apologize for any inconvenience.

Sincerely,\ Chief Executive Officer, Deal Intelligence LLC

### 5.2 Regulatory Authority Notification

#### GDPR Article 33 Breach Notification

**1. Nature of the breach:** [Categories and approximate number of data subjects and records]

**2. Contact details** : Chief Executive Officer: [Name] Email: privacy@dealintelligence.io Phone: [Number]

**3. Likely consequences:** [Assessment of potential impact]

**4. Measures taken:** [Technical and organizational measures implemented]

**5. Documentation** : Incident logged in the compliance platform Incident Reporting system Reference: [Incident ID]

## 6. Cookie Policy Template

### 6.1 Standard Cookie Notice

#### Cookie Policy

Deal Intelligence uses cookies and similar technologies to:

- Maintain session security

- Remember user preferences

- Analyze platform usage

- Improve service performance

#### Types of Cookies:

|**Cookie Type**|**Purpose**|**Duration**|**Opt-Out**|
|---|---|---|---|
|Essential|Authentication, security|Session|Not available|
|Functional|User preferences|30 days|Via settings|
|Analytics|Usage statistics|90 days|Via settings|
|Performance|CDN optimization|7 days|Via settings|

**Managing Cookies** : Users can manage cookie preferences through account settings or browser controls.

## 7. International Data Transfer Mechanisms

### 7.1 Standard Contractual Clauses

The following SCCs shall be incorporated by reference:

- Module 1: Controller to Controller transfers

- Module 2: Controller to Processor transfers

- Module 3: Processor to Processor transfers

- Module 4: Processor to Controller transfers

### 7.2 Transfer Impact Assessment

#### Assessment Factors:

- Laws of destination country (United States)

- Technical security measures (encryption, access controls)

- Organizational measures (policies, training)

- Sub-processor commitments

#### Supplementary Measures:

- End-to-end encryption for sensitive data

- Pseudonymization where feasible

- Enhanced access controls

- Regular security assessments

## 8. Consent Management

### 8.1 Consent Collection Template

**Marketing Consent:**

☐ I consent to receive marketing communications from Deal Intelligence

☐ I consent to data processing for service improvement purposes

**Consent Withdrawal** : You may withdraw consent at any time by:

- Clicking unsubscribe in any email

- Updating preferences in account settings

- Contacting privacy@dealintelligence.io

### 8.2 Consent Records

Maintain consent records including:

- Identity of data subject

- Specific consent granted

- Timestamp of consent

- Method of collection

- Withdrawal date (if applicable)

## 9. Privacy Impact Assessment Template

### 9.1 PIA Triggers

Conduct PIAs for:

- New data processing activities

- Changes to existing processing

- New sub-processor engagement

- International data transfers

- High-risk processing operations

### 9.2 PIA Documentation

Document the following:

- Processing purpose and necessity

- Data minimization assessment

- Security risk evaluation

- Compliance verification

- Mitigation measures

Reference: Risk Assessment Procedure

## 10. Compliance Monitoring

### 10.1 Privacy Metrics

Track and report:

- Data subject request response times

- Breach notification timeliness

- Consent rates and withdrawals

- Sub-processor compliance status

- Privacy training completion

### 10.2 Regular Reviews

- Quarterly privacy assessments via the compliance platform Risk Assessment module

- Annual DPA reviews and updates

- Semi-annual consent audit

- Annual tabletop exercise recorded in the compliance platform

## 11. Implementation Guidelines

### 11.1 Document Deployment

1. Customize templates with organization-specific information

2. Legal review by qualified counsel

3. Integration with customer onboarding process

4. Publication on platform and website

5. Version control and change tracking

### 11.2 Training Requirements

All personnel handling personal data must complete:

- GDPR/CCPA compliance training

- Privacy by design principles

- Data subject rights handling

- Breach response procedures

Reference: Security Awareness Training Program

## 12. Related Documents

- Information Security Policy

- Data Classification and Handling Standard

- Data Retention and Disposal Policy

- Data Subject Rights Request Procedure

- Incident Response Procedure

- Vendor Management Policy

- Access Control and Authentication Policy

- Encryption and Cryptographic Controls Standard

- API Security and Rate Limiting Standard

## 13. Review and Updates

This template shall be reviewed annually and updated to reflect:

- Changes in privacy regulations

- New processing activities

- Sub-processor modifications

- Lessons learned from incidents

- Customer feedback and requirements

Updates shall be managed through the Change Management Policy with appropriate stakeholder notification.

## 14. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Retyped as Template (no acknowledgment); scope limited to GDPR and CCPA; breach notification set to 48 hours to customers / 72 hours to the authority (24-hour promise removed); DSR assistance set to 30/45 days; SOC 2 report available on request under NDA; sub-processor list aligned to the Vendor Management Policy; account data retention set to relationship + 24 months; roles consolidated to CEO |
