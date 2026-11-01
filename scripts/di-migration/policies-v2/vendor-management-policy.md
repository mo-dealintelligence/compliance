---
title: "Vendor Management Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "vendor-management-policy-v1.0.pdf"
---

# Vendor Management Policy

## 1. Purpose

This policy defines how Deal Intelligence LLC evaluates, selects, and manages third-party vendors and sub-processors that handle, process, or have access to its systems and data. It keeps vendor relationships aligned with the SOC 2 Trust Services Criteria for Security, Availability, and Confidentiality.

## 2. Scope

This policy applies to:

- All third-party vendors, suppliers, and sub-processors that access, process, store, or transmit Deal Intelligence data
- All personnel involved in vendor selection, purchasing, and management
- All systems and services provided by external parties
- Third-party services integrated with the platform, including the pre-integration assessment in Section 7.3
- Current sub-processors as listed in Section 10.1

## 3. Definitions

- **Vendor**: Any third-party organization providing services to Deal Intelligence
- **Critical vendor**: A vendor whose failure could significantly impact service delivery or data security
- **Sub-processor**: A third party engaged by Deal Intelligence to process customer data
- **DPA**: Data Processing Agreement, as required under GDPR Article 28
- **SLA**: Service Level Agreement defining performance commitments

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

- Approves all critical vendor relationships
- Oversees the vendor risk assessment program
- Keeps this policy current and enforced
- Reports vendor risks at the quarterly management meeting
- Conducts initial vendor evaluations
- Confirms that contractual requirements are met
- Maintains vendor documentation and agreements
- Executes DPAs
- Monitors vendor service performance
- Manages technical integrations and access controls
- Coordinates incident response with vendors
- Maintains vendor configuration documentation

### 4.2 All personnel (including the Go-to-Market Contractor)

- Report vendor security concerns
- Follow approved vendor engagement procedures
- Protect vendor confidential information
- Comply with vendor-specific security requirements

## 5. Policy statement

Deal Intelligence maintains a minimal sub-processor model to reduce third-party risk exposure. All vendors must meet its security requirements and comply with applicable data protection regulations, including GDPR and CCPA. Vendor relationships are managed through formal agreements, regular assessments, and continuous monitoring.

## 6. Vendor classification

### 6.1 Critical vendors

Vendors are classified as critical if they:

- Process or store customer data (business contact information, lead data)
- Provide essential infrastructure services (AWS)
- Handle authentication and access control (PropelAuth)
- Have direct access to production systems
- Could impact the 99.9 % uptime SLA commitment

### 6.2 Non-critical vendors

Vendors are classified as non-critical if they:

- Do not directly handle customer data
- Support non-production environments
- Provide professional or administrative services
- Have limited system access

## 7. Vendor selection and due diligence

### 7.1 Initial assessment

Before engaging any vendor, the CEO completes the following evaluation:

- Security posture review, including SOC 2, ISO 27001, or equivalent certifications
- Data processing capabilities and compliance with GDPR/CCPA
- Financial stability assessment
- Service availability and SLA commitments
- Incident response and breach notification procedures
- Sub-processor management practices

### 7.2 Security requirements

All critical vendors must demonstrate:

- Encryption for data at rest and in transit (minimum AES-256)
- Multi-factor authentication capabilities
- Regular security assessments and vulnerability management
- Documented incident response procedures
- Business continuity and disaster recovery plans
- Compliance with relevant industry standards

Vendors are evaluated through the compliance platform Vendor Assessment workflow, which applies the same criteria to every vendor.

### 7.3 Pre-integration assessment

Before any third-party integration with the platform is implemented, the following assessment is completed and recorded in the compliance platform Vendor Assessment workflow. Technical integration controls (authentication, credential management, data exchange, monitoring) are defined in the Integration security section of the API Security and Rate Limiting Standard.

|**Assessment criteria**|**Requirement**|**Verification method**|
|---|---|---|
|Data Processing Agreement|Required for data processors|Review by the CEO via the compliance platform|
|Security certification|SOC 2 Type II or equivalent preferred|Vendor assessment documentation|
|API security standards|TLS 1.2+ encryption mandatory|Technical validation|
|Data residency|Compliance with GDPR/CCPA requirements|Vendor documentation review|
|Authentication method|OAuth 2.0 or API key minimum|Implementation review|
|Rate limiting|Documented limits and retry policies|API documentation review|
|Incident response|Breach notification terms that allow Deal Intelligence to meet its 48-hour customer notification commitment|Contractual agreement|

## 8. Contractual requirements

### 8.1 Data Processing Agreements

All vendors processing Deal Intelligence or customer data must execute:

- A Data Processing Agreement (DPA) compliant with GDPR Article 28
- Confidentiality and non-disclosure agreements
- A security addendum defining minimum security controls
- Breach notification requirements that allow Deal Intelligence to meet its 48-hour customer notification commitment
- Right-to-audit provisions
- Data deletion and return procedures upon termination

Reference: Privacy Notice and Data Processing Agreement Template

### 8.2 Service Level Agreements

Critical vendor contracts must include:

- Availability commitments aligned with the 99.9 % uptime SLA
- Performance metrics and monitoring requirements
- Escalation procedures for service issues
- Remediation timelines for identified vulnerabilities

Reference: Service Level Agreement (SLA) Management Policy

## 9. Ongoing vendor management

### 9.1 Regular assessments

**Annual reviews**: Security assessment of all critical vendors, including performance metrics and SLA compliance verification

**Continuous monitoring**: Real-time monitoring of AWS infrastructure through CloudWatch and Security Hub, with the monthly availability figure recorded in the compliance platform

### 9.2 Performance monitoring

The CEO tracks and documents:

- Service availability and uptime metrics
- Security incident frequency and response times
- Compliance with contractual obligations
- Customer complaint patterns related to vendor services

### 9.3 Risk assessment integration

Vendor risks are part of the overall risk assessment process, using the Risk Assessment module in the compliance platform for the annual vendor review. Key vendor risks include:

- Service disruption impacting platform availability
- Data breach at vendor facilities
- Vendor compliance failures affecting Deal Intelligence's certifications
- Vendor financial instability

Reference: Risk Assessment Procedure

## 10. Sub-processor management

### 10.1 Current sub-processors

Deal Intelligence maintains a minimal sub-processor model with the following approved sub-processors:

1. **AWS**: Cloud infrastructure and platform services, including hosting of the compliance platform, which is self-hosted on AWS
2. **PropelAuth**: Authentication and identity management services
3. **Google Workspace**: Email, identity (SSO), and document collaboration services
4. **GitHub**: Source code hosting and CI (GitHub Actions)
5. **Resend**: Transactional email delivery

### 10.2 Sub-processor changes

- Customers receive 30 days' advance notice of any sub-processor change
- The notice identifies the new sub-processor and its services
- Customers may object to a new sub-processor within the notice period
- Objection procedures are documented in customer agreements

### 10.3 Customer-controlled integrations

Third-party integrations such as Slack and CRM systems are:

- Implemented and controlled directly by customers
- Not considered Deal Intelligence sub-processors
- Subject to the customer's own vendor management policies
- Governed by the Integration security section of the API Security and Rate Limiting Standard

## 11. Vendor incident management

### 11.1 Incident response

When a security incident occurs at a vendor:

- The vendor notifies Deal Intelligence in accordance with its contractual breach notification terms
- Incident details are logged in the compliance platform's Incident Reporting system
- An impact assessment is conducted within 48 hours
- Customers are notified within 48 hours if customer data is affected
- A post-incident review is conducted with the vendor

Reference: Incident Response Procedure

### 11.2 Breach response

In case of a data breach at a vendor facility:

- The Incident Response Procedure is activated immediately, with the CEO as incident commander
- Deal Intelligence data exposure is assessed immediately
- Forensic analysis determines scope and impact
- Credentials are rotated for all integration points with the vendor
- Regulatory notifications are made as required by GDPR/CCPA (within 72 hours to the supervisory authority where GDPR applies)
- Customers are notified via established communication channels
- A remediation plan is developed and implemented
- The vendor is reassessed via the compliance platform

## 12. Vendor termination

### 12.1 Termination procedures

Upon termination of a vendor relationship:

- Secure data transfer or certified deletion within 30 days
- Return of all Deal Intelligence property and credentials
- Revocation of all access rights and accounts
- Final security assessment and audit
- Documentation of the termination in vendor management records

### 12.2 Transition planning

- Identify alternative vendors or in-house capabilities
- Develop a transition timeline that minimizes service disruption
- Maintain continuity of critical services during the transition
- Update the Business Continuity Plan in the compliance platform

Reference: Business Continuity Plan

## 13. Audit rights and compliance monitoring

### 13.1 Audit rights

Deal Intelligence reserves the right to:

- Conduct annual security assessments of critical vendors
- Request SOC 2 Type II or equivalent attestation reports
- Review vendor security documentation and procedures

### 13.2 Compliance monitoring

- Annual review of vendor compliance certificates
- Annual validation of GDPR/CCPA compliance measures
- Continuous monitoring of vendor security advisories
- Regular updates to vendor risk profiles in the compliance platform

## 14. Exceptions

Any exception to this policy must be:

- Documented with business justification
- Risk assessed, with mitigation controls defined
- Approved by the CEO
- Reviewed quarterly for continued necessity
- Tracked in the risk register

## 15. Review

This policy is:

- Reviewed annually or upon significant changes
- Updated to reflect new regulatory requirements
- Aligned with SOC 2 audit findings and recommendations
- Distributed to all relevant stakeholders
- Version controlled, with change history maintained

## 16. Related documents

- Information Security Policy
- Risk Assessment Procedure
- Incident Response Procedure
- Business Continuity Plan
- Data Classification and Handling Standard
- Cloud Infrastructure Security Policy
- API Security and Rate Limiting Standard
- Privacy Notice and Data Processing Agreement Template
- Service Level Agreement (SLA) Management Policy

## 17. Document approval

|**Role**|**Name**|**Signature**|**Date**|
|---|---|---|---|
|Chief Executive Officer|||[CONFIRM: date]|

_This document is maintained in the compliance platform and subject to version control and audit logging._

## 18. Revision history

|**Version**|**Date**|**Author**|**Summary**|
|---|---|---|---|
|1.0|November 13, 2025|mo@dealintelligence.io|Initial audited version|
|2.0|<to be set at publication>|mo@dealintelligence.io|Scope aligned to Security, Availability and Confidentiality; sub-processor list updated (AWS, PropelAuth, Google Workspace, GitHub, Resend, compliance platform self-hosted on AWS); annual vendor reviews; Cloud Infrastructure Governance section removed; on-site audits removed; roles consolidated to CEO; vendor-assessment and DPA content merged in from the Third-Party Integration Security Guidelines|
