---
title: "Acceptable Use Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.1"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "acceptable-use-policy-v1.1.pdf"
---

# Acceptable Use Policy

## 1. Purpose

This policy sets the requirements and restrictions for use of Deal Intelligence LLC's information systems, technology resources, and data. It protects customer data, maintains SOC 2 compliance, and prevents unauthorized or inappropriate activities that could compromise service commitments.

The policy implements the security principles of the Information Security Policy and supports SOC 2 Trust Services Criteria CC6.1 (logical access security software, infrastructure, and architectures), CC6.6 (logical access measures protecting system boundaries), CC6.8 (prevention of unauthorized or malicious software), CC7.2 (monitoring of system components for anomalies), and CC8.1 (authorization of changes). It also supports GDPR Article 32 (security of processing) and CCPA Section 1798.150 (personal information security).

## 2. Scope

This policy applies to:

- All personnel with access to Deal Intelligence systems, including the Chief Executive Officer (CEO), the Go-to-Market Contractor, and third-party service providers
- All information systems and technology resources, including:
  - AWS cloud infrastructure components (Lambda functions, Fargate containers, DocumentDB)
  - PropelAuth authentication services
  - Development and deployment tools (GitHub, GitHub Actions CI/CD pipelines)
  - Communication and collaboration platforms
  - Customer data and business contact information
- All devices used to access company systems, whether company-owned or personal
- All network connections to Deal Intelligence infrastructure
- All data processing activities related to the platform

The policy covers production and non-production environments as documented in the CloudFormation stack di-backend-api-prod.

## 3. Definitions

**Acceptable use**: Activities that align with business purposes, comply with security policies, and do not compromise system integrity or data confidentiality.

**Authorized user**: An individual granted access to Deal Intelligence systems through PropelAuth authentication with appropriate role-based permissions.

**Company resources**: All technology assets, systems, data, and services owned, operated, or managed by Deal Intelligence LLC.

**Prohibited activity**: Any action that violates this policy, compromises security controls, or conflicts with SOC 2 compliance requirements.

**Sensitive data**: Business contact information, customer account data, and any information classified as Confidential or Restricted per the Data Classification and Handling Standard.

**Security incident**: Any violation of this policy, or any event that compromises the confidentiality, integrity, or availability of company resources, as defined in the Incident Response Procedure.

## 4. Roles and responsibilities

### 4.1 All users

- Comply with all provisions of this policy
- Report suspected violations or security concerns immediately
- Complete security awareness training per the Security Awareness Training Program
- Protect authentication credentials and access tokens
- Use company resources only for authorized business purposes

### 4.2 Chief Executive Officer (CEO)

- Approves policy exceptions with documented business justification
- Enforces compliance through disciplinary measures
- Allocates resources for policy implementation and monitoring
- Reviews policy effectiveness annually
- Monitors compliance through CloudWatch logs, the monthly configuration-check record, and CloudTrail event alerts
- Investigates policy violations reported through the Incident Reporting system in the compliance platform
- Maintains the technical controls that enforce acceptable use requirements
- Provides guidance on acceptable use questions and edge cases
- Implements technical controls within the AWS infrastructure
- Configures monitoring and alerting for policy violations
- Maintains audit logs per the System Monitoring and Logging Procedure
- Reviews access patterns quarterly via automated Lambda functions

### 4.3 Go-to-Market Contractor

- Complies with this policy as a user under Section 4.1
- Holds no production (AWS, GitHub, DocumentDB, PropelAuth admin) access

## 5. General use requirements

### 5.1 Authorized access

Users must:

- Access systems only through approved authentication mechanisms: Google Workspace sign-in with MFA enforced for company data, and MFA enforced in GitHub and AWS for production access; customer access to the platform is authenticated by PropelAuth through Google sign-in
- Use only assigned user accounts with unique credentials
- Access data on a need-to-know basis following least privilege principles
- Comply with session timeout policies and re-authentication requirements
- Follow the Access Control and Authentication Policy for all access requests

### 5.2 Data protection

Users must:

- Handle business contact information according to the Data Classification and Handling Standard
- Encrypt sensitive data in transit and at rest per the Encryption and Cryptographic Controls Standard
- Not store customer data on personal devices or in unauthorized locations
- Follow the retention periods defined in the Data Retention and Disposal Policy
- Report any suspected data breach immediately per the Incident Response Procedure

### 5.3 System security

Users must:

- Not attempt to bypass, disable, or circumvent security controls
- Not install unauthorized software or modify system configurations
- Report security vulnerabilities per the Vulnerability Management Procedure
- Comply with the Change Management Policy
- Follow secure development practices per the Secure Software Development Lifecycle (SDLC) Standard

## 6. Prohibited activities

The following activities are prohibited.

### 6.1 Unauthorized access

- Accessing systems or data without authorization
- Sharing authentication credentials or access tokens
- Using another user's account or impersonating another user
- Attempting to escalate privileges beyond assigned roles
- Accessing production databases directly, other than by the CEO via SSM Session Manager, which is logged; all other access must be through approved APIs

### 6.2 Data misuse

- Copying, transferring, or storing customer data for personal use
- Sharing business contact information outside authorized channels
- Using customer data for purposes other than service delivery
- Violating data subject rights as defined in the Data Subject Rights Request Procedure
- Processing data in violation of GDPR or CCPA requirements

### 6.3 System abuse

- Introducing malicious code, viruses, or security threats
- Conducting unauthorized vulnerability scans or penetration tests
- Overriding the rate limits defined in the API Security and Rate Limiting Standard
- Mining cryptocurrency or running unauthorized compute workloads
- Using company resources for illegal activities or personal gain

### 6.4 Network security violations

- Connecting unauthorized devices to company networks
- Bypassing VPC isolation or network segmentation controls
- Establishing unauthorized network connections or tunnels
- Violating the Cloud Infrastructure Security Policy
- Exposing internal services to the public internet without approval

## 7. Remote work requirements

Deal Intelligence operates remotely. Users must meet the following requirements.

### 7.1 Device security

- Use FileVault full-disk encryption (macOS) on all devices accessing company systems
- Maintain current operating system patches and security updates
- Enable automatic screen locks with password protection
- Report lost or stolen devices immediately

### 7.2 Network security

- Connect only through secure, encrypted connections (HTTPS/TLS)
- Access company data only through browser SSO (Google Workspace) and the AWS console/CLI with MFA
- Use WPA2/WPA3 encryption on home network routers
- Change default passwords on home networking equipment

### 7.3 Physical security

- Maintain a secure workspace free from unauthorized observation
- Lock devices when stepping away from the workstation
- Position screens to prevent shoulder surfing
- Securely dispose of printed materials containing sensitive data
- Not discuss confidential information in public spaces

## 8. Cloud service usage

### 8.1 AWS infrastructure

Users with AWS access must:

- Follow the Cloud Infrastructure Security Policy
- Use only approved AWS services documented in CloudFormation templates
- Not create resources outside the defined region (us-east-1)
- Follow tagging standards for resource identification
- Comply with cost optimization guidelines

### 8.2 Third-party services

Users must:

- Use only approved sub-processors (AWS and PropelAuth) and approved vendors (Google Workspace, GitHub, Resend, HubSpot, and the compliance platform, which is self-hosted on AWS); the vendors do not process customer data
- Follow the Vendor Management Policy and the Integration security section of the API Security and Rate Limiting Standard
- Not integrate unauthorized third-party services
- Apply the security requirements to customer-controlled integrations (Slack, CRM)
- Raise new service requirements with the CEO

## 9. Development and testing

### 9.1 Code management

Personnel with repository access must:

- Follow secure coding practices defined in the Secure Software Development Lifecycle (SDLC) Standard
- Use only approved repositories and version control systems
- Not commit secrets, credentials, or sensitive data to repositories
- Follow branch protection rules and pull request requirements (required CI status checks on the protected `main` branch)
- Run pre-commit security hooks before code submission

### 9.2 Testing environments

Personnel must:

- Use only sanitized or synthetic data in non-production environments
- Not copy production data to development or testing systems
- Apply the same security controls in the staging environment as in production
- Document and track all test accounts and credentials
- Destroy test environments when no longer needed

## 10. Monitoring and compliance

### 10.1 Activity monitoring

Deal Intelligence monitors system usage through:

- CloudWatch logs with 90-day retention
- API request audit logging middleware
- CloudTrail for AWS API calls, with security-relevant events (root sign-in, IAM changes, CloudTrail stop/delete, KMS key disable, security-group changes) alerted to the CEO in real time via EventBridge, the breach-detection Lambda, and SNS
- Monthly configuration-check Lambda run against a fixed checklist, with a dated pass/fail record posted to the compliance platform

### 10.2 Compliance verification

Compliance is verified through:

- Quarterly access reviews via automated Lambda functions
- Security assessments per the Penetration Testing and Security Assessment Procedure
- Continuous vulnerability scanning in ECR (scan-on-push)
- Rate limit enforcement (100 requests/minute)
- PII sanitization validation in logs

## 11. Policy violations

### 11.1 Reporting violations

Policy violations are reported through:

- The Incident Reporting system in the compliance platform
- Direct notification to the CEO by email

### 11.2 Consequences

Violations may result in:

- Immediate suspension of system access
- Formal investigation per the Incident Response Procedure
- Disciplinary action up to and including termination
- Legal action for criminal violations
- Notification to affected customers if data is compromised

### 11.3 Investigation process

All reported violations are:

- Logged in the Incident Reporting system in the compliance platform
- Investigated within 24 hours of the report
- Documented with findings and remediation actions
- Reviewed for process improvements

## 12. Exceptions

### 12.1 Exception request process

Exceptions to this policy require:

- Written business justification
- A risk assessment per the Risk Assessment Procedure
- Identification of compensating controls
- CEO approval
- A time-limited approval period (maximum 90 days)

### 12.2 Exception documentation

Approved exceptions are:

- Documented in the risk register in the compliance platform's risk assessment module
- Monitored for compliance with compensating controls
- Revoked when the business need no longer exists

## 13. Training and awareness

All users must:

- Complete acceptable use training during onboarding
- Acknowledge this policy annually in the compliance platform portal
- Participate in security awareness activities per the Security Awareness Training Program
- Stay informed of policy updates
- Seek clarification when uncertain about acceptable use

## 14. Related documents

- Information Security Policy
- Access Control and Authentication Policy
- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Classification and Handling Standard
- Encryption and Cryptographic Controls Standard
- API Security and Rate Limiting Standard
- Secure Software Development Lifecycle (SDLC) Standard
- Risk Assessment Procedure
- Incident Response Procedure
- Vulnerability Management Procedure
- System Monitoring and Logging Procedure
- Penetration Testing and Security Assessment Procedure
- Security Awareness Training Program
- Data Retention and Disposal Policy
- Data Subject Rights Request Procedure
- Business Continuity Plan
- Service Level Agreement (SLA) Management Policy

## 15. Revision history

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|1.1|November 13, 2025|Audited release|
|2.0|<to be set at publication>|Roles consolidated to CEO and Go-to-Market Contractor; remote-access and device requirements restated as browser SSO and AWS console/CLI with MFA plus FileVault full-disk encryption; MFA wording aligned; direct production database access limited to the CEO via SSM Session Manager; sub-processor list updated|
