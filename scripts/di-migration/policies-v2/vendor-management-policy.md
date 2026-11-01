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

This Vendor Management Policy establishes the framework for evaluating, selecting, and managing third-party vendors and sub-processors who handle, process, or have access to Deal Intelligence's systems and data. This policy ensures that vendor relationships align with our SOC 2 Trust Service Criteria for Security, Availability and Confidentiality.

## 2. Scope

This policy applies to:

- All third-party vendors, suppliers, and sub-processors who access, process, store, or transmit Deal Intelligence data
- All personnel involved in vendor selection, purchasing, and management
- All systems and services provided by external parties
- Third-party services integrated with the platform, including the pre-integration assessment in section 5.3
- Current sub-processors as listed in section 8.1

## 3. Policy Statement

Deal Intelligence maintains a minimal sub-processor model to reduce third-party risk exposure. All vendors must meet our security requirements and comply with applicable data protection regulations including GDPR and CCPA. Vendor relationships shall be managed through formal agreements, regular assessments, and continuous monitoring.

## 4. Vendor Classification

### 4.1 Critical Vendors

Vendors are classified as critical if they:

- Process or store customer data (business contact information, lead data)
- Provide essential infrastructure services (AWS)
- Handle authentication and access control (PropelAuth)
- Have direct access to production systems
- Could impact our 99.9% uptime SLA commitment

### 4.2 Non-Critical Vendors

Vendors providing services that:

- Do not directly handle customer data
- Support non-production environments
- Provide professional or administrative services
- Have limited system access

## 5. Vendor Selection and Due Diligence

### 5.1 Initial Assessment

Before engaging any vendor, the following evaluation must be completed:

- Security posture review including SOC 2, ISO 27001, or equivalent certifications
- Data processing capabilities and compliance with GDPR/CCPA
- Financial stability assessment
- Service availability and SLA commitments
- Incident response and breach notification procedures
- Sub-processor management practices

### 5.2 Security Requirements

All critical vendors must demonstrate:

- Encryption for data at rest and in transit (minimum AES-256)
- Multi-factor authentication capabilities
- Regular security assessments and vulnerability management
- Documented incident response procedures
- Business continuity and disaster recovery plans
- Compliance with relevant industry standards

Vendors shall be evaluated through the standardized compliance platform Vendor Assessment workflow to ensure consistent evaluation criteria.

### 5.3 Pre-Integration Assessment

Before implementing any third-party integration with the platform, the following assessment shall be completed and recorded in the compliance platform Vendor Assessment workflow. Technical integration controls (authentication, credential management, data exchange, monitoring) are defined in the Integration security section of the API Security and Rate Limiting Standard.

|**Assessment Criteria**|**Requirement**|**Verification Method**|
|---|---|---|
|Data Processing Agreement|Required for data processors|Review by the CEO via the compliance platform|
|Security Certification|SOC 2 Type II or equivalent preferred|Vendor assessment documentation|
|API Security Standards|TLS 1.2+ encryption mandatory|Technical validation|
|Data Residency|Compliance with GDPR/CCPA requirements|Vendor documentation review|
|Authentication Method|OAuth 2.0 or API key minimum|Implementation review|
|Rate Limiting|Documented limits and retry policies|API documentation review|
|Incident Response|Breach notification terms that allow Deal Intelligence to meet its 48-hour customer notification commitment|Contractual agreement|

## 6. Contractual Requirements

### 6.1 Data Processing Agreements

All vendors processing Deal Intelligence or customer data must execute:

- Data Processing Agreement (DPA) compliant with GDPR Article 28
- Confidentiality and non-disclosure agreements
- Security addendum defining minimum security controls
- Breach notification requirements that allow Deal Intelligence to meet its 48-hour customer notification commitment
- Right to audit provisions
- Data deletion and return procedures upon termination

Reference: Privacy Notice and Data Processing Agreement Template

### 6.2 Service Level Agreements

Critical vendor contracts must include:

- Availability commitments aligned with our 99.9% uptime SLA
- Performance metrics and monitoring requirements
- Escalation procedures for service issues
- Remediation timelines for identified vulnerabilities

Reference: Service Level Agreement (SLA) Management Policy

## 7. Ongoing Vendor Management

### 7.1 Regular Assessments

**Annual Reviews**: Comprehensive security assessment for all critical vendors, including performance metrics and SLA compliance verification

**Continuous Monitoring**: Real-time monitoring of AWS infrastructure through CloudWatch and Security Hub, with the monthly availability figure recorded in the compliance platform

### 7.2 Performance Monitoring

Track and document:

- Service availability and uptime metrics
- Security incident frequency and response times
- Compliance with contractual obligations
- Customer complaint patterns related to vendor services

### 7.3 Risk Assessment Integration

Vendor risks shall be incorporated into the organization's overall risk assessment process, utilizing the Risk Assessment module in the compliance platform for the annual vendor review. Key vendor risks include:

- Service disruption impacting platform availability
- Data breach at vendor facilities
- Vendor compliance failures affecting our certifications
- Vendor financial instability

Reference: Risk Assessment Procedure

## 8. Sub-Processor Management

### 8.1 Current Sub-Processors

Deal Intelligence maintains a minimal sub-processor model with the following approved sub-processors:

1. **AWS**: Cloud infrastructure and platform services, including hosting of the compliance platform, which is self-hosted on AWS
2. **PropelAuth**: Authentication and identity management services
3. **Google Workspace**: Email, identity (SSO) and document collaboration services
4. **GitHub**: Source code hosting and CI (GitHub Actions)
5. **Resend**: Transactional email delivery

### 8.2 Sub-Processor Changes

- Customers must receive 30-day advance notice of any sub-processor changes
- Notification shall include the identity and services of the new sub-processor
- Customers may object to new sub-processors within the notice period
- Objection procedures shall be documented in customer agreements

### 8.3 Customer-Controlled Integrations

Third-party integrations such as Slack and CRM systems are:

- Implemented and controlled directly by customers
- Not considered Deal Intelligence sub-processors
- Subject to customer's own vendor management policies
- Governed by the Integration security section of the API Security and Rate Limiting Standard

## 9. Vendor Incident Management

### 9.1 Incident Response

When a security incident occurs at a vendor:

- Vendor must notify Deal Intelligence in accordance with its contractual breach notification terms
- Incident details logged in the compliance platform's Incident Reporting system
- Impact assessment conducted within 48 hours
- Customer notification within 48 hours if customer data is affected
- Post-incident review conducted with vendor

Reference: Incident Response Procedure

### 9.2 Breach Response

In case of a data breach at a vendor facility:

- Immediate activation of the Incident Response Procedure with the CEO as incident commander
- Immediate assessment of Deal Intelligence data exposure
- Forensic analysis to determine scope and impact
- Credential rotation for all integration points with the vendor
- Regulatory notifications as required by GDPR/CCPA (within 72 hours to the supervisory authority where GDPR applies)
- Customer notifications via established communication channels
- Remediation plan development and implementation
- Vendor re-assessment via the compliance platform

## 10. Vendor Termination

### 10.1 Termination Procedures

Upon vendor relationship termination:

- Secure data transfer or certified deletion within 30 days
- Return of all Deal Intelligence property and credentials
- Revocation of all access rights and accounts
- Final security assessment and audit
- Documentation of termination in vendor management records

### 10.2 Transition Planning

- Identify alternative vendors or in-house capabilities
- Develop transition timeline minimizing service disruption
- Ensure continuity of critical services during transition
- Update Business Continuity Plans in the compliance platform

Reference: Business Continuity Plan

## 11. Compliance and Audit

### 11.1 Audit Rights

Deal Intelligence reserves the right to:

- Conduct annual security assessments of critical vendors
- Request SOC 2 Type II or equivalent attestation reports
- Review vendor security documentation and procedures

### 11.2 Compliance Monitoring

- Annual review of vendor compliance certificates
- Annual validation of GDPR/CCPA compliance measures
- Continuous monitoring of vendor security advisories
- Regular updates to vendor risk profiles in the compliance platform

## 12. Roles and Responsibilities

### 12.1 Chief Executive Officer

- Approve all critical vendor relationships
- Oversee vendor risk assessment program
- Ensure policy compliance and updates
- Report vendor risks at the quarterly management meeting
- Conduct initial vendor evaluations
- Ensure contractual requirements are met
- Maintain vendor documentation and agreements
- Execute DPAs
- Monitor vendor service performance
- Manage technical integrations and access controls
- Coordinate incident response with vendors
- Maintain vendor configuration documentation

### 12.2 All Personnel (including the Go-to-Market Contractor)

- Report vendor security concerns
- Follow approved vendor engagement procedures
- Protect vendor confidential information
- Comply with vendor-specific security requirements

## 13. Policy Exceptions

Any exceptions to this policy must be:

- Documented with business justification
- Risk assessed and mitigation controls defined
- Approved by the CEO
- Reviewed quarterly for continued necessity
- Tracked in the risk register

## 14. Policy Review and Updates

This policy shall be:

- Reviewed annually or upon significant changes
- Updated to reflect new regulatory requirements
- Aligned with SOC 2 audit findings and recommendations
- Distributed to all relevant stakeholders
- Version controlled with change history maintained

## 15. Related Documents

- Information Security Policy
- Risk Assessment Procedure
- Incident Response Procedure
- Business Continuity Plan
- Data Classification and Handling Standard
- Cloud Infrastructure Security Policy
- API Security and Rate Limiting Standard
- Privacy Notice and Data Processing Agreement Template
- Service Level Agreement (SLA) Management Policy

## 16. Definitions

- **Sub-processor**: A third party engaged by Deal Intelligence to process customer data
- **Critical Vendor**: A vendor whose failure could significantly impact service delivery or data security
- **DPA**: Data Processing Agreement as required under GDPR Article 28
- **SLA**: Service Level Agreement defining performance commitments
- **Vendor**: Any third-party organization providing services to Deal Intelligence

## Document Approval

|**Role**|**Name**|**Signature**|**Date**|
|---|---|---|---|
|Chief Executive Officer|||[CONFIRM: date]|

_This document is maintained in the compliance platform and subject to version control and audit logging._

## Revision history

|**Version**|**Date**|**Author**|**Summary**|
|---|---|---|---|
|1.0|November 13, 2025|mo@dealintelligence.io|Initial audited version|
|2.0|<to be set at publication>|mo@dealintelligence.io|Scope aligned to Security, Availability and Confidentiality; sub-processor list updated (AWS, PropelAuth, Google Workspace, GitHub, Resend, compliance platform self-hosted on AWS); annual vendor reviews; Cloud Infrastructure Governance section removed; on-site audits removed; roles consolidated to CEO; vendor-assessment and DPA content merged in from the Third-Party Integration Security Guidelines|
