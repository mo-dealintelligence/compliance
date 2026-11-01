---
title: "Access Control and Authentication Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "access-control-and-authentication-policy-v1.0.pdf"
---

# Access Control and Authentication Policy

## 1. Purpose

This Access Control and Authentication Policy establishes the framework for managing logical access to Deal Intelligence LLC's information systems, technology resources, and data assets. This policy ensures that access to the platform is appropriately restricted, authenticated, and monitored in accordance with SOC 2 Trust Service Criteria for Security (CC6.1-CC6.3), supporting our commitment to maintaining the confidentiality, integrity, and availability of customer data.

This policy operationalizes the security principles defined in the Information Security Policy and establishes technical and administrative controls that protect business contact information and lead intelligence data from unauthorized access.

## 2. Scope

This policy applies to:

- All access to Deal Intelligence systems and infrastructure, including:

   - AWS cloud infrastructure (Lambda functions, DocumentDB, Fargate containers)

   - PropelAuth authentication services

   - Development and deployment systems (GitHub repositories, CI/CD pipelines)

   - Administrative interfaces and management consoles

- All user accounts and authentication mechanisms

- All personnel requiring system access, including contractors and third-party service providers

- All devices and network connections used to access company resources

- Both production (di-backend-api-prod) and non-production environments

## 3. Policy Statement

Deal Intelligence shall implement defense-in-depth access controls utilizing PropelAuth JWT authentication, with customer multi-factor authentication inherited from Google Workspace sign-in via PropelAuth (Google SSO only), role-based access control (RBAC) with least privilege principles, and comprehensive audit logging. All access to systems containing customer data shall be authenticated, authorized, and monitored to prevent unauthorized disclosure or modification of business contact information, lead intelligence data, and customer account information.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer

The CEO owns this policy and is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration). The CEO is responsible for:

- Approving access control policies and procedures

- Authorizing privileged access requests

- Reviewing and approving access control exceptions

- Ensuring compliance with SOC 2 requirements

- Implementing and maintaining access control systems

- Conducting quarterly access reviews via automated Lambda functions

- Managing PropelAuth configuration and security settings

- Monitoring access logs and investigating anomalies

- Coordinating with AWS security services (Security Hub, CloudTrail)

- Provisioning and deprovisioning user accounts

- Configuring role-based access controls in PropelAuth

- Managing AWS IAM roles and policies

- Implementing technical access controls

- Maintaining VPC security groups and network access controls

### 4.2 Go-to-Market Contractor

- Holds no production access (no AWS, GitHub, DocumentDB or PropelAuth administrative access)

- Accesses company data only through browser SSO (Google Workspace) with MFA

- Completes onboarding, security awareness training and policy acknowledgments in the compliance platform portal

### 4.3 All Users

All personnel with system access are responsible for:

- Protecting authentication credentials

- Reporting suspected unauthorized access

- Complying with acceptable use requirements as defined in the Acceptable Use Policy

- Completing security awareness training per the Security Awareness Training Program

## 5. Access Control Requirements

### 5.1 User Authentication

#### 5.1.1 Authentication Standards

- All users shall authenticate using PropelAuth JWT tokens; customer multi-factor authentication is inherited from Google Workspace sign-in via PropelAuth (Google SSO only)

- Multi-factor authentication (MFA) for personnel shall be enforced in Google Workspace, GitHub and AWS, and is required for:

   - Google Workspace sign-in

   - Administrative access to AWS console

   - Access to production databases

   - GitHub repository access

   - CI/CD pipeline configurations

- Session timeout policies shall be enforced:

   - 30 minutes for idle sessions

   - 8 hours maximum session duration

   - Automatic re-authentication required after timeout

#### 5.1.2 Password Requirements

For systems not using Google Workspace SSO:

- Minimum 12 characters length

- Combination of uppercase, lowercase, numbers, and special characters

- Password rotation every 90 days

- No reuse of last 12 passwords

- Account lockout after 5 failed attempts

### 5.2 Authorization and Access Management

#### 5.2.1 Role-Based Access Control (RBAC)

Access shall be granted based on defined roles aligned with job responsibilities:

- **Administrator** : Full system access for Chief Executive Officer

- **Developer** : Access to development environments and non-production systems

- **Read-Only** : Limited access for reporting and monitoring purposes

- **Customer** : Access limited to their own company data via PropelAuth isolation

The Go-to-Market Contractor holds no Administrator or Developer role.

#### 5.2.2 Least Privilege Principle

- Users receive minimum access required for job functions

- Production database access restricted to VPC-isolated connections only

- No direct database access; all interactions through API layer

- Temporary elevated privileges granted only when necessary with documented approval

#### 5.2.3 Segregation of Duties

- Production deployment proceeds only through a pull request on the protected `main` branch with required CI status checks passing and a logged self-review in the pull request; deployment history is retained in GitHub Actions and CloudTrail and is independently reviewed by the external SOC 2 auditor

- Database schema changes require CEO approval

- Security configuration changes logged and reviewed quarterly

### 5.3 Account Management

#### 5.3.1 Account Provisioning

- New accounts created only with documented approval from CEO

- Unique user accounts required; no shared credentials permitted

- Initial access granted based on documented role requirements

- Account creation logged in CloudTrail audit logs

#### 5.3.2 Account Deprovisioning

- Accounts disabled immediately upon termination or role change

- Access reviews conducted quarterly via automated Lambda function

- Dormant accounts (90 days inactive) automatically disabled

- Deprovisioning activities logged and retained per Data Retention and Disposal Policy

#### 5.3.3 Privileged Account Management

- AWS root account secured with MFA and used only for emergency access

- IAM roles used for programmatic access instead of long-term credentials

- Service accounts rotated quarterly

- All privileged access logged and monitored via CloudTrail

## 6. Technical Controls

### 6.1 Network Access Controls

- VPC isolation for production resources (us-east-1a, us-east-1b)

- Private subnets for database and internal services

- Security groups configured with least privilege rules

- Network ACLs restricting traffic between tiers

- CloudFront CDN for public-facing content delivery

### 6.2 API Access Controls

- Rate limiting enforced (100 requests per minute)

- JWT token validation on all API endpoints

- Input validation and sanitization per API Security and Rate Limiting Standard

- CORS policies restricting cross-origin requests

### 6.3 Infrastructure Access Controls

- AWS Systems Manager Session Manager for access to the NAT instance used as a bastion (no SSH keys, no public services); all other workloads run on Lambda and Fargate

- CloudFormation stack protection for production resources

- CloudFormation resource tags for cost allocation

- AWS Organizations SCPs limiting high-risk actions

## 7. Monitoring and Logging

### 7.1 Access Logging Requirements

All access attempts shall be logged including:

- User identity (PropelAuth user ID or AWS principal)

- Timestamp of access attempt

- Resource accessed

- Action performed

- Success or failure status

- Source IP address

### 7.2 Log Management

- CloudWatch Logs retention: 90 days minimum

- CloudTrail enabled for all AWS API calls

- Audit logging middleware for application-level access

- PII sanitization in logs to protect privacy

- Log aggregation to centralized CloudWatch dashboard

### 7.3 Security Monitoring

- Security Hub findings reviewed monthly (recorded); critical findings alert in real time via SNS

- Automated breach detection Lambda functions

- SNS alerts for suspicious activities

- Failed authentication attempts monitored

- Privilege escalation attempts flagged

For detailed monitoring procedures, refer to System Monitoring and Logging Procedure.

## 8. Access Reviews

### 8.1 Periodic Reviews

- Quarterly automated access reviews via Lambda function

- Semi-annual privileged access audit by CEO

- Annual third-party access assessment per Vendor Management Policy

- Monthly review of security group rules and network ACLs

### 8.2 Review Documentation

Access reviews shall document:

- Users reviewed and their current roles

- Access rights validated or modified

- Accounts disabled or removed

- Exceptions approved with business justification

- Review completion date and reviewer

## 9. Third-Party Access

### 9.1 Vendor Access Management

- Approved sub-processors only, as listed in the Vendor Management Policy

- Data Processing Agreements required before access

- Vendor access limited to specific services and data

- 30-day notice for sub-processor changes

- Annual security assessments per Vendor Management Policy

### 9.2 Customer Integrations

- Customer-controlled integrations (Slack, CRM) via secure APIs

- OAuth 2.0 or API key authentication required

- Scoped permissions limiting data access

- Integration security requirements provided in the Integration security section of the API Security and Rate Limiting Standard

## 10. Incident Response

Access control incidents shall be managed according to the Incident Response Procedure, including:

- Immediate account suspension for suspected compromise

- Password reset requirements after incidents

- 48-hour breach notification to affected customers

- Post-incident access review and remediation

- Documentation in the compliance platform Incident Reporting system

## 11. Compliance and Exceptions

### 11.1 Compliance Monitoring

- Quarterly compliance assessments by CEO

- Annual SOC 2 audit validation

- Continuous monitoring via AWS Security Hub

- Automated compliance checks in CI/CD pipeline

### 11.2 Exception Management

- Exceptions require written approval from CEO

- Temporary exceptions limited to 30 days maximum

- Compensating controls required for all exceptions

- Exception log maintained with business justification

## 12. Training and Awareness

All personnel shall receive access control training covering:

- Password security and MFA usage

- Recognizing phishing attempts

- Proper handling of access credentials

- Incident reporting procedures

- Annual refresher training required

Training requirements detailed in Security Awareness Training Program.

## 13. Related Documents

- Information Security Policy

- Acceptable Use Policy

- Data Classification and Handling Standard

- Incident Response Procedure

- Change Management Policy

- API Security and Rate Limiting Standard

- Cloud Infrastructure Security Policy

## 14. Policy Review and Maintenance

This policy shall be reviewed annually and updated as needed to reflect:

- Changes in regulatory requirements

- Updates to technology infrastructure

- Lessons learned from security incidents

- Results of access control audits

- Evolution of threat landscape

**Policy Owner:** Mo Messidi, Chief Executive Officer
**Last Review Date:** <to be set at publication>
**Next Review Date:** <one year after effective date>
**Version:** 2.0

## 15. Approval

This Access Control and Authentication Policy has been reviewed and approved by:

| Name | Role | Date |
|---|---|---|
| Mo Messidi | Chief Executive Officer, Deal Intelligence LLC | [CONFIRM: date] |

## 16. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Roles consolidated to CEO and Go-to-Market Contractor; MFA described as Google Workspace / GitHub / AWS enforcement; segregation of duties restated as the PR + CI-gate control; Security Hub review monthly with real-time SNS alerting; bastion and sub-processor wording aligned to the operated environment |
