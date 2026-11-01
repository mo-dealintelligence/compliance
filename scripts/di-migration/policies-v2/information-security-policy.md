---
title: "Information Security Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "information-security-policy-v1.0.pdf"
---

# Information Security Policy

## 1. Purpose

This Information Security Policy establishes the foundational security principles, controls, and governance framework for Deal Intelligence LLC's platform. The policy ensures the protection of customer data, system integrity, and service availability in alignment with SOC 2 Trust Services Criteria and regulatory requirements including GDPR and CCPA.

This policy serves as the cornerstone document that unifies all security-related policies and procedures across the organization, ensuring consistent implementation of controls that protect business contact information and maintain the confidentiality, integrity, and availability of our services.

## 2. Scope

This policy applies to:

- All information systems, applications, and infrastructure supporting Deal Intelligence's platform AWS cloud infrastructure including Lambda functions, Fargate containers, DocumentDB, and associated services

- All personnel with access to Deal Intelligence systems and data

- Third-party service providers and sub-processors handling customer data

- Business contact information and customer account data processed by the platform

The policy encompasses the Trust Services Criteria selected by Deal Intelligence: Security, Availability and Confidentiality.

## 3. Definitions

**Information Asset** : Any data, system, application, or infrastructure component that processes, stores, or transmits Deal Intelligence or customer information.

**Business Contact Information** : First name, last name, business email address, LinkedIn profile URL, job title, current employer, company name, company domain, and related professional data.

**Control Owner** : Individual responsible for implementing and maintaining specific security controls within their area of responsibility.

**Trust Services Criteria (TSC)** : AICPA framework comprising the Security, Availability and Confidentiality principles selected by Deal Intelligence.

**Sub-processor** : Third-party service provider that processes customer data on behalf of Deal Intelligence (the current list of sub-processors is maintained in the Vendor Management Policy).

**Security Incident** : Any event that compromises or potentially compromises the confidentiality, integrity, or availability of information assets.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer (CEO)

The CEO owns this policy and every control it describes, and is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration). The CEO:

- Approves and sponsors the information security program

- Ensures adequate resources for security initiatives

- Reviews and approves security policies annually

- Oversees compliance with SOC 2 requirements

- Implements and maintains security controls across all systems

- Coordinates security assessments and audits

- Manages security incident response activities as incident commander

- Maintains security documentation and evidence for SOC 2 compliance

- Oversees security monitoring and alerting systems

- Ensures security controls are implemented in AWS infrastructure

- Maintains secure configuration of Lambda functions and containers

- Monitors system performance and availability metrics

- Implements backup and recovery procedures

- Approves exceptions to this policy and serves as the data protection contact

### 4.2 Go-to-Market Contractor

- Has no production access

- Completes onboarding, security awareness training, and policy acknowledgments in the compliance platform portal

- Complies with the Acceptable Use Policy and confidentiality obligations

### 4.3 All Personnel

- Comply with all security policies and procedures

- Report security incidents immediately

- Protect authentication credentials and access tokens

- Complete security awareness training as required

### 4.4 External Parties

- The external SOC 2 auditor provides independent review of the controls described in this policy

- The penetration-test vendor conducts the annual third-party penetration test

- Sub-processors are managed under the Vendor Management Policy

## 5. Policy Statements

### 5.1 Risk Management

Deal Intelligence shall maintain a comprehensive risk management program that identifies, assesses, and mitigates information security risks. The program is administered in the compliance platform, which serves as the control register (controls, evidence, tasks), to reduce human error and ensure consistent enforcement.

Risk assessments shall be conducted according to the Risk Assessment Procedure and documented in the risk register in the compliance platform. Key risk areas include:

- Data breach risks mitigated through encryption and continuous monitoring

- Unauthorized access risks addressed via MFA and role-based access controls

- Service availability risks managed through multi-AZ deployment and 99.9% uptime SLA

### 5.2 Access Control and Authentication

Access to Deal Intelligence systems and data shall be controlled through:

- PropelAuth JWT authentication, with customer multi-factor authentication inherited from Google Workspace sign-in via PropelAuth (Google SSO only)

- Multi-factor authentication for personnel enforced in Google Workspace, GitHub and AWS

- Role-based access control (RBAC) implementing least privilege principles

- User and company-level data isolation

- VPC-isolated database with no direct public access

- Quarterly access reviews via automated Lambda functions

Detailed access control requirements are specified in the Access Control and Authentication Policy.

### 5.3 Data Protection and Classification

All customer data shall be protected according to its classification level as defined in the Data Classification and Handling Standard:

- Business contact information classified as Confidential

- Customer account data protected with encryption at rest and in transit

- 24-month retention period for active leads

- PII sanitization in all system logs

Encryption requirements are detailed in the Encryption and Cryptographic Controls Standard.

### 5.4 Change Management

All changes to production systems shall follow the documented change management process outlined in the Change Management Policy:

- Pre-commit hooks for security validation

- GitHub Actions CI/CD pipeline with automated testing

- Branch protection on `main` requiring a pull request with required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes

- Deployment to a staging stage before production release

- Production deployments only from a green CI run

### 5.5 Security Monitoring and Incident Response

Continuous security monitoring shall be maintained through:

- 24/7 CloudWatch monitoring with 90-day log retention

- CloudTrail audit logging for all AWS API calls

- Security Hub for automated threat detection, with critical findings alerted in real time via SNS and findings reviewed monthly

- Rate limiting controls (100 requests per minute)

- Container vulnerability scanning in ECR

Security incidents shall be managed according to the Incident Response Procedure, with 48-hour breach notification to affected customers. The Incident Reporting system in the compliance platform shall be used for documenting and tracking all security incidents.

### 5.6 Vendor and Third-Party Management

Third-party service providers shall be managed according to the Vendor Management Policy:

- Data Processing Agreements required for all sub-processors

- 30-day advance notice for sub-processor changes

- Annual security assessments using the Vendor Assessment workflow in the compliance platform

- Current sub-processors listed in the Vendor Management Policy

Third-party integrations shall comply with the Integration security section of the API Security and Rate Limiting Standard.

### 5.7 Business Continuity and Disaster Recovery

Business continuity capabilities shall be maintained as specified in the Business Continuity Plan:

- Multi-availability zone deployment (us-east-1a, us-east-1b)

- Daily automated backups with 90-day retention

- Quarterly backup restoration testing

- Documented RTO/RPO objectives

- Business continuity planning managed through the Business Continuity Plans module in the compliance platform

### 5.8 Vulnerability Management

System vulnerabilities shall be identified and remediated according to the Vulnerability Management Procedure:

- Automated vulnerability scanning for containers

- Security patches applied within defined timeframes

- Penetration testing conducted as specified in the Penetration Testing and Security Assessment Procedure

### 5.9 Secure Development

Software development shall follow secure coding practices defined in the Secure Software Development Lifecycle (SDLC) Standard:

- Security testing integrated into CI/CD pipeline

- Logged self-review in the pull request, with automated security checks (Bandit, Trivy, TruffleHog) in CI

- Dependency scanning and management

- API security controls per the API Security and Rate Limiting Standard

### 5.10 Cloud Infrastructure Security

AWS cloud infrastructure shall be secured according to the Cloud Infrastructure Security Policy:

- CloudFormation templates for consistent deployment

- Security groups with least privilege network access

- KMS encryption for data at rest

- VPC isolation for sensitive resources

### 5.11 Privacy and Data Subject Rights

Privacy requirements shall be implemented as specified in the Data Subject Rights Request Procedure and Privacy Notice and Data Processing Agreement Template:

- GDPR and CCPA compliance for B2B data processing

- Data subject request handling within regulatory timeframes

- Privacy notices and consent management

- Data retention and disposal per the Data Retention and Disposal Policy

### 5.12 Security Awareness and Training

Personnel shall receive security awareness training as outlined in the Security Awareness Training Program:

- Initial security training for all new personnel

- Annual refresher training

- Role-specific security training as required

- Completion certificates recorded in the compliance platform portal

### 5.13 Acceptable Use

All personnel shall comply with the Acceptable Use Policy regarding appropriate use of Deal Intelligence systems and resources.

## 6. Monitoring and Review

### 6.1 Control Testing

- Controls, evidence and tasks tracked in the compliance platform as the control register

- Annual comprehensive security assessment

- Continuous monitoring through CloudWatch and Security Hub

- Regular vulnerability assessments

### 6.2 Policy Review

- Annual policy review and update cycle

- Ad-hoc updates for significant changes or incidents

- Stakeholder feedback incorporation

- Regulatory compliance verification

### 6.3 Audit and Compliance

- Annual SOC 2 Type II audit

- Quarterly internal compliance assessments

- Evidence collection and retention per the System Monitoring and Logging Procedure

- Management review of security metrics and KPIs

### 6.4 Performance Metrics

- 99.9% service availability target

- 48-hour breach notification to affected customers

- 90-day log retention compliance

## 7. Enforcement

Violations of this policy may result in disciplinary action up to and including termination of employment or contract. Security incidents resulting from policy violations shall be documented and reviewed to prevent recurrence.

## 8. Related Documents

### Core Policies

- Change Management Policy

- Vendor Management Policy

- Acceptable Use Policy

- Access Control and Authentication Policy

- Cloud Infrastructure Security Policy

### Standards and Guidelines

- Data Classification and Handling Standard

- Encryption and Cryptographic Controls Standard

- API Security and Rate Limiting Standard

- Secure Software Development Lifecycle (SDLC) Standard

### Procedures

- Risk Assessment Procedure

- Incident Response Procedure

- Business Continuity Plan

- Vulnerability Management Procedure

- Penetration Testing and Security Assessment Procedure

- System Monitoring and Logging Procedure

- Data Subject Rights Request Procedure

### Supporting Documents

- Data Retention and Disposal Policy

- Privacy Notice and Data Processing Agreement Template

- Security Awareness Training Program

- Service Level Agreement (SLA) Management Policy

## 9. Compliance Mapping

This policy addresses the following SOC 2 Trust Services Criteria:

- **CC1.1-CC1.5** : Control Environment

- **CC2.1-CC2.3** : Communication and Information

- **CC3.1-CC3.4** : Risk Assessment

- **CC4.1-CC4.2** : Monitoring Activities

- **CC5.1-CC5.3** : Control Activities

- **CC6.1-CC6.8** : Logical and Physical Access Controls

- **CC7.1-CC7.5** : System Operations

- **CC8.1** : Change Management

- **CC9.1-CC9.2** : Risk Mitigation

- **A1.1-A1.3** : Availability

- **C1.1-C1.2** : Confidentiality

## 10. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Scope limited to Security, Availability and Confidentiality; roles consolidated to CEO and Go-to-Market Contractor; control-automation and review-frequency claims aligned to the operated environment; related-document list corrected |
