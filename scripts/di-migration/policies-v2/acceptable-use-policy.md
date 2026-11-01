---
title: "Acceptable Use Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.1"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "acceptable-use-policy-v1.1.pdf"
---

# Acceptable Use Policy

## 1. Purpose

This Acceptable Use Policy establishes the requirements and restrictions for appropriate use of Deal Intelligence LLC's information systems, technology resources, and data assets to ensure the security, integrity, and availability of the platform. This policy enforces behavioral controls that protect customer data, maintain SOC 2 compliance, and prevent unauthorized or inappropriate activities that could compromise our service commitments.

The policy operationalizes the security principles defined in the Information Security Policy and establishes clear boundaries for system usage that align with SOC 2 Trust Services Criteria, specifically addressing CC6.1 (Logical and Physical Access Controls), CC6.6 (System Boundaries), and CC6.8 (Prevention of Unauthorized Software).

## 2. Scope

This policy applies to:

- All personnel with access to Deal Intelligence systems, including the Chief Executive Officer, the Go-to-Market Contractor, and third-party service providers

- All information systems and technology resources, including:

   - AWS cloud infrastructure components (Lambda functions, Fargate containers, DocumentDB)

   - PropelAuth authentication services

   - Development and deployment tools (GitHub, GitHub Actions CI/CD pipelines)

   - Communication and collaboration platforms

   - Customer data and business contact information

- All devices used to access company systems, whether company-owned or personal

- All network connections to Deal Intelligence infrastructure

- All data processing activities related to the platform

The policy encompasses both production and non-production environments as documented in CloudFormation stack di-backend-api-prod.

## 3. Definitions

**Acceptable Use**: Activities that align with business purposes, comply with security policies, and do not compromise system integrity or data confidentiality.

**Authorized User**: Individual granted access to Deal Intelligence systems through PropelAuth authentication with appropriate role-based permissions.

**Company Resources**: All technology assets, systems, data, and services owned, operated, or managed by Deal Intelligence LLC.

**Prohibited Activity**: Any action that violates this policy, compromises security controls, or conflicts with SOC 2 compliance requirements.

**Sensitive Data**: Business contact information, customer account data, and any information classified as Confidential or Restricted per the Data Classification and Handling Standard.

**Security Incident**: Any violation of this policy or event that compromises the confidentiality, integrity, or availability of company resources as defined in the Incident Response Procedure.

## 4. Roles and Responsibilities

### 4.1 All Users

- Comply with all provisions of this policy

- Report suspected violations or security concerns immediately

- Complete security awareness training as outlined in the Security Awareness Training Program

- Protect authentication credentials and access tokens

- Use company resources solely for authorized business purposes

### 4.2 Chief Executive Officer

- Approve policy exceptions with documented business justification

- Enforce compliance through appropriate disciplinary measures

- Allocate resources for policy implementation and monitoring

- Review policy effectiveness annually

- Monitor compliance through CloudWatch logs and Security Hub findings

- Investigate policy violations reported through the Incident Reporting system in the compliance platform

- Maintain technical controls that enforce acceptable use requirements

- Provide guidance on acceptable use questions and edge cases

- Implement technical controls within AWS infrastructure

- Configure monitoring and alerting for policy violations

- Maintain audit logs per the System Monitoring and Logging Procedure

- Review access patterns quarterly via automated Lambda functions

### 4.3 Go-to-Market Contractor

- Comply with this policy as a user under Section 4.1

- Holds no production (AWS, GitHub, DocumentDB, PropelAuth admin) access

## 5. General Use Requirements

### 5.1 Authorized Access

Users shall:

- Access systems only through approved authentication mechanisms: Google Workspace sign-in with MFA enforced for company data, and MFA enforced in GitHub and AWS for production access; customer access to the platform is authenticated by PropelAuth through Google sign-in

- Use only assigned user accounts with unique credentials

- Access data on a need-to-know basis following least privilege principles

- Comply with session timeout policies and re-authentication requirements

- Follow the Access Control and Authentication Policy for all access requests

### 5.2 Data Protection

Users shall:

- Handle business contact information according to the Data Classification and Handling Standard

- Encrypt sensitive data in transit and at rest per the Encryption and Cryptographic Controls Standard

- Not store customer data on personal devices or unauthorized locations

- Follow data retention periods defined in the Data Retention and Disposal Policy

- Report any suspected data breach immediately per the Incident Response Procedure

### 5.3 System Security

Users shall:

- Not attempt to bypass, disable, or circumvent security controls

- Not install unauthorized software or modify system configurations

- Report security vulnerabilities through proper channels per the Vulnerability Management Procedure

- Comply with change management requirements defined in the Change Management Policy

- Follow secure development practices per the Secure Software Development Lifecycle (SDLC) Standard

## 6. Prohibited Activities

The following activities are strictly prohibited:

### 6.1 Unauthorized Access

- Accessing systems or data without proper authorization

- Sharing authentication credentials or access tokens

- Using another user's account or impersonating another user

- Attempting to escalate privileges beyond assigned roles

- Accessing production databases directly, other than by the CEO via SSM Session Manager, which is logged; all other access must be through approved APIs

### 6.2 Data Misuse

- Copying, transferring, or storing customer data for personal use

- Sharing business contact information outside authorized channels

- Using customer data for purposes other than service delivery

- Violating data subject rights as defined in the Data Subject Rights Request Procedure

- Processing data in violation of GDPR or CCPA requirements

### 6.3 System Abuse

- Introducing malicious code, viruses, or security threats

- Conducting unauthorized vulnerability scans or penetration tests

- Overriding rate limits defined in the API Security and Rate Limiting Standard

- Mining cryptocurrency or running unauthorized compute workloads

- Using company resources for illegal activities or personal gain

### 6.4 Network Security Violations

- Connecting unauthorized devices to company networks

- Bypassing VPC isolation or network segmentation controls

- Establishing unauthorized network connections or tunnels

- Violating the Cloud Infrastructure Security Policy

- Exposing internal services to public internet without approval

## 7. Remote Work Requirements

Given Deal Intelligence's remote work environment, users shall:

### 7.1 Device Security

- Use full-disk encryption on all devices accessing company systems

- Maintain current operating system patches and security updates

- Run the device agent of the compliance platform where deployed

- Enable automatic screen locks with password protection

- Report lost or stolen devices immediately

### 7.2 Network Security

- Connect only through secure, encrypted connections (HTTPS/TLS)

- Access company data only through browser SSO (Google Workspace) and the AWS console/CLI with MFA

- Ensure home network routers use WPA2/WPA3 encryption

- Change default passwords on home networking equipment

### 7.3 Physical Security

- Maintain a secure workspace free from unauthorized observation

- Lock devices when stepping away from workstation

- Position screens to prevent shoulder surfing

- Securely dispose of printed materials containing sensitive data

- Not discuss confidential information in public spaces

## 8. Cloud Service Usage

### 8.1 AWS Infrastructure

Users with AWS access shall:

- Follow the Cloud Infrastructure Security Policy

- Use only approved AWS services documented in CloudFormation templates

- Not create resources outside defined regions (us-east-1)

- Follow tagging standards for resource identification

- Comply with cost optimization guidelines

### 8.2 Third-Party Services

- Use only approved sub-processors (AWS, PropelAuth, Google Workspace, GitHub, Resend, and the compliance platform, which is self-hosted on AWS)

- Follow the Vendor Management Policy and the Integration security section of the API Security and Rate Limiting Standard

- Not integrate unauthorized third-party services

- Ensure customer-controlled integrations (Slack, CRM) follow security requirements

- Report new service requirements through proper channels

## 9. Development and Testing

### 9.1 Code Management

Personnel with repository access shall:

- Follow secure coding practices defined in the Secure Software Development Lifecycle (SDLC) Standard

- Use only approved repositories and version control systems

- Not commit secrets, credentials, or sensitive data to repositories

- Follow branch protection rules and pull request requirements (required CI status checks on the protected `main` branch)

- Run pre-commit security hooks before code submission

### 9.2 Testing Environments

- Use only sanitized or synthetic data in non-production environments

- Not copy production data to development or testing systems

- Follow the same security controls in the staging stage as production

- Document and track all test accounts and credentials

- Destroy test environments when no longer needed

## 10. Monitoring and Compliance

### 10.1 Activity Monitoring

Deal Intelligence monitors system usage through:

- CloudWatch logs with 90-day retention

- API request audit logging middleware

- CloudTrail for AWS API calls

- Security Hub findings and alerts

- Automated compliance checks via Lambda functions

### 10.2 Compliance Verification

Compliance is verified through:

- Quarterly access reviews via automated Lambda functions

- Regular security assessments per the Penetration Testing and Security Assessment Procedure

- Continuous vulnerability scanning in ECR (scan-on-push)

- Rate limit enforcement (100 requests/minute)

- PII sanitization validation in logs

## 11. Policy Violations

### 11.1 Reporting Violations

Policy violations shall be reported through:

- The Incident Reporting system in the compliance platform

- Direct notification to the CEO

- Anonymous reporting channels if available

### 11.2 Consequences

Violations may result in:

- Immediate suspension of system access

- Formal investigation per the Incident Response Procedure

- Disciplinary action up to and including termination

- Legal action for criminal violations

- Notification to affected customers if data is compromised

### 11.3 Investigation Process

All reported violations shall be:

- Logged in the Incident Reporting system in the compliance platform

- Investigated within 24 hours of report

- Documented with findings and remediation actions

- Reviewed for process improvements

- Included in quarterly compliance reports

## 12. Exceptions

### 12.1 Exception Request Process

Exceptions to this policy require:

- Written business justification

- Risk assessment per the Risk Assessment Procedure

- Identification of compensating controls

- CEO approval

- Time-limited approval period (maximum 90 days)

### 12.2 Exception Documentation

Approved exceptions shall be:

- Documented in the risk register in the compliance platform's risk assessment module

- Reviewed quarterly for continued necessity

- Monitored for compliance with compensating controls

- Revoked when business need no longer exists

## 13. Training and Awareness

All users shall:

- Complete acceptable use training during onboarding

- Acknowledge understanding of this policy annually in the compliance platform portal

- Participate in security awareness activities per the Security Awareness Training Program

- Stay informed of policy updates and changes

- Seek clarification when uncertain about acceptable use

## 14. Compliance Requirements

This policy addresses the following SOC 2 Trust Services Criteria:

- **CC6.1**: Implements logical access security software, infrastructure, and architectures

- **CC6.6**: Implements logical access security measures to protect boundaries

- **CC6.8**: Prevents the introduction of unauthorized or malicious software

- **CC7.2**: Monitors system components for anomalies

- **CC8.1**: Authorizes, designs, develops, or acquires changes to meet objectives

The policy also supports compliance with:

- GDPR Article 32 (Security of Processing)

- CCPA Section 1798.150 (Personal Information Security)

- Industry best practices for acceptable use controls

## 15. Related Documents

### Core Policies

- Information Security Policy

- Access Control and Authentication Policy

- Change Management Policy

- Cloud Infrastructure Security Policy

### Standards and Guidelines

- Data Classification and Handling Standard

- Encryption and Cryptographic Controls Standard

- API Security and Rate Limiting Standard

- Secure Software Development Lifecycle (SDLC) Standard

### Procedures

- Risk Assessment Procedure

- Incident Response Procedure

- Vulnerability Management Procedure

- System Monitoring and Logging Procedure

- Penetration Testing and Security Assessment Procedure

### Supporting Documents

- Security Awareness Training Program

- Data Retention and Disposal Policy

- Data Subject Rights Request Procedure

- Business Continuity Plan

- Service Level Agreement (SLA) Management Policy

## 16. Revision History

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|1.1|November 13, 2025|Audited release|
|2.0|<to be set at publication>|Roles consolidated to CEO and Go-to-Market Contractor; remote-access and device requirements restated as browser SSO and AWS console/CLI with MFA plus the compliance platform device agent; MFA wording aligned; direct production database access limited to the CEO via SSM Session Manager; sub-processor list updated|
