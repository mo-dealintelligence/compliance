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

This policy sets the security principles, controls, and governance for the Deal Intelligence LLC platform. It protects customer data, system integrity, and service availability in line with the SOC 2 Trust Services Criteria and with GDPR and CCPA. It is the parent document for every other security policy, standard, and procedure in the set, and it protects the confidentiality, integrity, and availability of the business contact information the platform processes.

This policy addresses SOC 2 Trust Services Criteria CC1.1–CC1.5 (control environment), CC2.1–CC2.3 (communication and information), CC3.1–CC3.4 (risk assessment), CC4.1–CC4.2 (monitoring activities), CC5.1–CC5.3 (control activities), CC6.1–CC6.8 (logical and physical access controls), CC7.1–CC7.5 (system operations), CC8.1 (change management), CC9.1–CC9.2 (risk mitigation), A1.1–A1.3 (availability), and C1.1–C1.2 (confidentiality).

## 2. Scope

This policy applies to:

- All information systems, applications, and infrastructure supporting the Deal Intelligence platform, including the AWS cloud infrastructure (Lambda functions, Fargate containers, DocumentDB, and associated services)
- All personnel with access to Deal Intelligence systems and data
- Third-party service providers and sub-processors handling customer data
- Business contact information and customer account data processed by the platform

The policy covers the Trust Services Criteria selected by Deal Intelligence: Security, Availability, and Confidentiality.

## 3. Definitions

**Information asset**: Any data, system, application, or infrastructure component that processes, stores, or transmits Deal Intelligence or customer information.

**Business contact information**: First name, last name, business email address, LinkedIn profile URL, job title, current employer, company name, company domain, and related professional data.

**Control owner**: The individual responsible for implementing and maintaining specific security controls within their area of responsibility.

**Trust Services Criteria (TSC)**: The AICPA framework comprising the Security, Availability, and Confidentiality principles selected by Deal Intelligence.

**Sub-processor**: A third-party service provider that processes customer data on behalf of Deal Intelligence. The current list of sub-processors is maintained in the Vendor Management Policy.

**Security incident**: Any event that compromises or potentially compromises the confidentiality, integrity, or availability of information assets.

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

The Chief Executive Officer (CEO) owns this policy and every control it describes, and is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration). The CEO:

- Approves and sponsors the information security program
- Provides the resources for security initiatives
- Reviews and approves security policies annually
- Oversees compliance with SOC 2 requirements
- Implements and maintains security controls across all systems
- Coordinates security assessments and audits
- Manages security incident response as incident commander
- Maintains security documentation and evidence for SOC 2 compliance
- Oversees security monitoring and alerting systems
- Implements security controls in the AWS infrastructure
- Maintains the secure configuration of Lambda functions and containers
- Monitors system performance and availability metrics
- Implements backup and recovery procedures
- Approves exceptions to this policy and serves as the data protection contact

### 4.2 Go-to-Market Contractor

The Go-to-Market Contractor:

- Has no production access
- Completes onboarding, security awareness training, and policy acknowledgments in the compliance platform portal
- Complies with the Acceptable Use Policy and confidentiality obligations

### 4.3 All personnel

All personnel:

- Comply with all security policies and procedures
- Report security incidents immediately
- Protect authentication credentials and access tokens
- Complete security awareness training as required

### 4.4 External parties

- The external SOC 2 auditor provides independent review of the controls described in this policy
- The penetration-test vendor conducts the annual third-party penetration test
- Sub-processors are managed under the Vendor Management Policy

## 5. Policy statements

### 5.1 Risk management

Deal Intelligence maintains a risk management program that identifies, assesses, and mitigates information security risks. The program is administered in the compliance platform, which serves as the control register (controls, evidence, tasks).

Risk assessments follow the Risk Assessment Procedure and are documented in the risk register in the compliance platform. Key risk areas include:

- Data breach risks, mitigated through encryption and continuous monitoring
- Unauthorized access risks, addressed through MFA and role-based access controls
- Service availability risks, managed through the availability-zone design (DocumentDB storage replicated across three availability zones with automatic instance recovery; Lambda functions in two availability zones), point-in-time recovery, and the 99.9 % uptime SLA

### 5.2 Access control and authentication

Access to Deal Intelligence systems and data is controlled through:

- PropelAuth JWT authentication, with customer multi-factor authentication inherited from Google Workspace sign-in via PropelAuth (Google SSO only)
- Multi-factor authentication for personnel enforced in Google Workspace, GitHub, and AWS
- Role-based access control (RBAC) implementing least privilege
- User-level and company-level data isolation
- A VPC-isolated database with no direct public access
- Quarterly access reviews via automated Lambda functions

Detailed access control requirements are in the Access Control and Authentication Policy.

### 5.3 Data protection and classification

All customer data is protected according to its classification level as defined in the Data Classification and Handling Standard:

- Business contact information is classified as Confidential
- Customer account data is encrypted at rest and in transit
- Active leads are retained for 24 months
- PII is sanitized in all system logs

Encryption requirements are in the Encryption and Cryptographic Controls Standard.

### 5.4 Change management

All changes to production systems follow the Change Management Policy:

- Pre-commit hooks for security validation
- GitHub Actions CI/CD pipeline with automated testing
- Branch protection on `main` requiring a pull request with required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes
- Deployment to a staging environment in a separate AWS account before production release
- Production deployments only from a green CI run

### 5.5 Security monitoring and incident response

Security monitoring is maintained through:

- 24/7 CloudWatch monitoring with 90-day log retention
- CloudTrail audit logging for all AWS API calls; security-relevant events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- A scheduled configuration-check Lambda that runs monthly against a fixed checklist and posts a dated pass/fail record to the compliance platform
- Rate limiting (100 requests per minute)
- Container vulnerability scanning in ECR

Security incidents are managed according to the Incident Response Procedure, with breach notification to affected customers within 48 hours. All security incidents are documented and tracked in the Incident Reporting system in the compliance platform.

### 5.6 Vendor and third-party management

Third-party service providers are managed according to the Vendor Management Policy:

- Data Processing Agreements are required for all sub-processors
- Sub-processor changes are announced 30 days in advance
- Annual security assessments use the Vendor Assessment workflow in the compliance platform
- Current sub-processors are listed in the Vendor Management Policy

Third-party integrations comply with the Integration security section of the API Security and Rate Limiting Standard.

### 5.7 Business continuity and disaster recovery

Business continuity capabilities are maintained as specified in the Business Continuity Plan:

- Lambda functions and private subnets in us-east-1a and us-east-1b; DocumentDB storage replicated across three availability zones with automatic instance recovery
- Daily automated backups with 35-day retention
- Quarterly backup restoration testing
- Documented RTO and RPO objectives
- Business continuity planning managed in the Business Continuity Plans module of the compliance platform

### 5.8 Vulnerability management

System vulnerabilities are identified and remediated according to the Vulnerability Management Procedure:

- Automated vulnerability scanning for containers
- Security patches applied within the defined timeframes
- Penetration testing conducted as specified in the Penetration Testing and Security Assessment Procedure

### 5.9 Secure development

Software development follows the secure coding practices in the Secure Software Development Lifecycle (SDLC) Standard:

- Security testing integrated into the CI/CD pipeline
- Logged self-review in the pull request, with automated security checks (Bandit, Trivy, TruffleHog) in CI
- Dependency scanning and management
- API security controls per the API Security and Rate Limiting Standard

### 5.10 Cloud infrastructure security

The AWS cloud infrastructure is secured according to the Cloud Infrastructure Security Policy:

- CloudFormation templates for consistent deployment
- Security groups with least-privilege network access
- KMS encryption for data at rest
- VPC isolation for sensitive resources

### 5.11 Privacy and data subject rights

Privacy requirements are implemented as specified in the Data Subject Rights Request Procedure and the Privacy Notice and Data Processing Agreement Template:

- GDPR and CCPA compliance for B2B data processing
- Data subject requests handled within the regulatory timeframes
- Privacy notices and consent management
- Data retention and disposal per the Data Retention and Disposal Policy

### 5.12 Security awareness and training

Personnel receive security awareness training as outlined in the Security Awareness Training Program:

- Initial security training for all new personnel
- Annual refresher training
- Role-specific security training as required
- Completion certificates recorded in the compliance platform portal

### 5.13 Acceptable use

All personnel comply with the Acceptable Use Policy on the appropriate use of Deal Intelligence systems and resources.

## 6. Monitoring and review

### 6.1 Control testing

- Controls, evidence, and tasks are tracked in the compliance platform as the control register
- An annual security assessment is performed
- Continuous monitoring runs through CloudWatch and CloudTrail event alerting, with the monthly configuration-check record as the recurring evidence
- Vulnerability assessments are performed per the Vulnerability Management Procedure

### 6.2 Policy review

- Policies are reviewed and updated annually
- Ad-hoc updates follow significant changes or incidents
- Stakeholder feedback is incorporated
- Regulatory compliance is verified

### 6.3 Audit and compliance

- Annual SOC 2 Type II audit
- Evidence collection and retention per the System Monitoring and Logging Procedure
- Management review of security metrics and KPIs

### 6.4 Performance metrics

- 99.9 % service availability target
- Breach notification to affected customers within 48 hours
- 90-day log retention

## 7. Enforcement

Violations of this policy may result in disciplinary action up to and including termination of employment or contract. Security incidents resulting from policy violations are documented and reviewed to prevent recurrence.

## 8. Related documents

**Policies**

- Access Control and Authentication Policy
- Acceptable Use Policy
- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Retention and Disposal Policy
- Service Level Agreement (SLA) Management Policy
- Vendor Management Policy

**Standards**

- API Security and Rate Limiting Standard
- Data Classification and Handling Standard
- Encryption and Cryptographic Controls Standard
- Secure Software Development Lifecycle (SDLC) Standard

**Procedures and plans**

- Business Continuity Plan
- Data Subject Rights Request Procedure
- Incident Response Procedure
- Penetration Testing and Security Assessment Procedure
- Risk Assessment Procedure
- System Monitoring and Logging Procedure
- Vulnerability Management Procedure

**Other**

- Privacy Notice and Data Processing Agreement Template
- Security Awareness Training Program

## 9. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Scope limited to Security, Availability, and Confidentiality; roles consolidated to CEO and Go-to-Market Contractor; control-automation and review-frequency claims aligned to the operated environment; related-document list corrected |
