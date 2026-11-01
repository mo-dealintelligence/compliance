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

This policy governs logical access to Deal Intelligence LLC's information systems, technology resources, and data. It restricts, authenticates, and monitors access to the platform in accordance with the SOC 2 Trust Services Criteria for Security (CC6.1–CC6.3) and supports the confidentiality, integrity, and availability of customer data.

The policy implements the principles of the Information Security Policy through the technical and administrative controls that protect business contact information and lead intelligence data from unauthorized access.

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
- Both the production (di-backend-api-prod) and staging stages of the stack

## 3. Policy statement

Deal Intelligence implements defense-in-depth access controls: PropelAuth JWT authentication, with customer multi-factor authentication inherited from Google Workspace sign-in via PropelAuth (Google SSO only); role-based access control (RBAC) on the principle of least privilege; and audit logging. All access to systems containing customer data is authenticated, authorized, and monitored to prevent unauthorized disclosure or modification of business contact information, lead intelligence data, and customer account information.

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

The Chief Executive Officer (CEO) owns this policy and is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration). The CEO is responsible for:

- Approving access control policies and procedures
- Authorizing privileged access requests
- Reviewing and approving access control exceptions
- Overseeing compliance with SOC 2 requirements
- Implementing and maintaining access control systems
- Conducting quarterly access reviews via automated Lambda functions
- Managing PropelAuth configuration and security settings
- Monitoring access logs and investigating anomalies
- Operating the AWS security services (CloudTrail, the monthly configuration-check Lambda, and the CloudTrail-EventBridge alerting rule)
- Provisioning and deprovisioning user accounts
- Configuring role-based access controls in PropelAuth
- Managing AWS IAM roles and policies
- Implementing technical access controls
- Maintaining VPC security groups and network access controls

### 4.2 Go-to-Market Contractor

The Go-to-Market Contractor:

- Holds no production access (no AWS, GitHub, DocumentDB, or PropelAuth administrative access)
- Accesses company data only through browser SSO (Google Workspace) with MFA, from a device with FileVault full-disk encryption (macOS) enabled
- Completes onboarding, security awareness training, and policy acknowledgments in the compliance platform portal

### 4.3 All users

All personnel with system access are responsible for:

- Protecting authentication credentials
- Using only personnel devices with FileVault full-disk encryption (macOS) enabled to access company resources
- Reporting suspected unauthorized access
- Complying with the Acceptable Use Policy
- Completing security awareness training per the Security Awareness Training Program

## 5. Access control requirements

### 5.1 User authentication

#### 5.1.1 Authentication standards

- All users authenticate using PropelAuth JWT tokens; customer multi-factor authentication is inherited from Google Workspace sign-in via PropelAuth (Google SSO only)
- Multi-factor authentication (MFA) for personnel is enforced in Google Workspace, GitHub, and AWS, and is required for:
   - Google Workspace sign-in
   - Administrative access to the AWS console
   - Access to production databases
   - GitHub repository access
   - CI/CD pipeline configuration
- Session timeouts are enforced:
   - 30 minutes for idle sessions
   - 8 hours maximum session duration
   - Automatic re-authentication after timeout

#### 5.1.2 Password requirements

For systems not using Google Workspace SSO:

- Minimum length of 12 characters
- A combination of uppercase, lowercase, numbers, and special characters
- Password rotation every 90 days
- No reuse of the last 12 passwords
- Account lockout after 5 failed attempts

### 5.2 Authorization and access management

#### 5.2.1 Role-based access control (RBAC)

Access is granted by defined roles aligned with job responsibilities:

- **Administrator**: Full system access, held by the CEO
- **Developer**: Access to development environments and non-production systems
- **Read-only**: Limited access for reporting and monitoring
- **Customer**: Access limited to their own company data via PropelAuth isolation

The Go-to-Market Contractor holds no Administrator or Developer role.

#### 5.2.2 Least privilege

- Users receive the minimum access required for their job functions
- Production database access is restricted to VPC-isolated connections only
- There is no direct database access; all interactions go through the API layer
- Temporary elevated privileges are granted only when necessary, with documented approval

#### 5.2.3 Segregation of duties

- Production deployment proceeds only through a pull request on the protected `main` branch with required CI status checks passing and a logged self-review in the pull request; deployment history is retained in GitHub Actions and CloudTrail and is independently reviewed by the external SOC 2 auditor
- Database schema changes require CEO approval
- Security configuration changes are logged in CloudTrail

### 5.3 Account management

#### 5.3.1 Account provisioning

- New accounts are created only with documented approval from the CEO
- Unique user accounts are required; shared credentials are not permitted
- Initial access is granted on documented role requirements
- Account creation is logged in CloudTrail

#### 5.3.2 Account deprovisioning

- Accounts are disabled immediately on termination or role change
- Access reviews are conducted quarterly via an automated Lambda function
- Dormant accounts (90 days inactive) are disabled automatically
- Deprovisioning activities are logged and retained per the Data Retention and Disposal Policy

#### 5.3.3 Privileged account management

- The AWS root account is secured with MFA and used only for emergency access
- IAM roles are used for programmatic access instead of long-term credentials
- Service accounts are rotated quarterly
- All privileged access is logged and monitored via CloudTrail

## 6. Technical controls

### 6.1 Network access controls

- VPC isolation for production resources (us-east-1a, us-east-1b)
- Private subnets for the database and internal services
- Security groups configured with least-privilege rules
- Network ACLs restricting traffic between tiers
- CloudFront for public-facing content delivery

### 6.2 API access controls

- Rate limiting enforced (100 requests per minute)
- JWT token validation on all API endpoints
- Input validation and sanitization per the API Security and Rate Limiting Standard
- CORS policies restricting cross-origin requests

### 6.3 Infrastructure access controls

- SSM Session Manager for access to the NAT instance used as a bastion (no SSH keys, no public services); all other workloads run on Lambda and Fargate
- CloudFormation stack protection for production resources
- CloudFormation resource tags for cost allocation
- AWS Organizations SCPs limiting high-risk actions

## 7. Monitoring and logging

### 7.1 Access logging requirements

All access attempts are logged with:

- User identity (PropelAuth user ID or AWS principal)
- Timestamp of the access attempt
- Resource accessed
- Action performed
- Success or failure status
- Source IP address

### 7.2 Log management

- CloudWatch Logs retention: 90 days minimum
- CloudTrail enabled for all AWS API calls
- Audit logging middleware for application-level access
- PII sanitization in logs
- Log aggregation to a centralized CloudWatch dashboard

### 7.3 Security monitoring

- Monthly configuration-check Lambda run against the fixed checklist (root account MFA, IAM password policy, CloudTrail enabled and log-file validation on, among other items), with a dated pass/fail record posted to the compliance platform
- Security-relevant CloudTrail events (root sign-in, IAM policy or user changes) trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- Failed authentication attempts monitored
- Privilege escalation attempts flagged

Detailed monitoring procedures are in the System Monitoring and Logging Procedure.

## 8. Access reviews

### 8.1 Periodic reviews

- Quarterly automated access reviews via Lambda function
- Semi-annual privileged access audit by the CEO
- Annual third-party access assessment per the Vendor Management Policy

### 8.2 Review documentation

Each access review records:

- Users reviewed and their current roles
- Access rights validated or modified
- Accounts disabled or removed
- Exceptions approved, with business justification
- Review completion date and reviewer

## 9. Third-party access

### 9.1 Vendor access management

- Approved sub-processors only, as listed in the Vendor Management Policy
- Data Processing Agreements required before access
- Vendor access limited to specific services and data
- 30-day notice for sub-processor changes
- Annual security assessments per the Vendor Management Policy

### 9.2 Customer integrations

- Customer-controlled integrations (Slack, CRM) via secure APIs
- OAuth 2.0 or API key authentication required
- Scoped permissions limiting data access
- Integration security requirements per the Integration security section of the API Security and Rate Limiting Standard

## 10. Incident response

Access control incidents are managed according to the Incident Response Procedure, including:

- Immediate account suspension for suspected compromise
- Password resets after incidents
- Breach notification to affected customers within 48 hours
- Post-incident access review and remediation
- Documentation in the compliance platform Incident Reporting system

## 11. Compliance and exceptions

### 11.1 Compliance monitoring

- Annual SOC 2 audit validation
- Monthly configuration-check record in the compliance platform
- Automated compliance checks in the CI/CD pipeline

### 11.2 Exception management

- Exceptions require written approval from the CEO
- Temporary exceptions are limited to 30 days
- Compensating controls are required for all exceptions
- An exception log is maintained with business justification

## 12. Training and awareness

All personnel receive access control training covering:

- Password security and MFA usage
- Recognizing phishing attempts
- Proper handling of access credentials
- Incident reporting procedures

Refresher training is required annually. Training requirements are in the Security Awareness Training Program.

## 13. Related documents

- Information Security Policy
- Acceptable Use Policy
- API Security and Rate Limiting Standard
- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Classification and Handling Standard
- Data Retention and Disposal Policy
- Incident Response Procedure
- Security Awareness Training Program
- System Monitoring and Logging Procedure
- Vendor Management Policy

## 14. Policy review and maintenance

This policy is reviewed annually and updated as needed to reflect:

- Changes in regulatory requirements
- Updates to the technology infrastructure
- Lessons learned from security incidents
- Results of access control audits
- Changes in the threat landscape

**Policy owner:** Chief Executive Officer
**Last review date:** <to be set at publication>
**Next review date:** <one year after effective date>
**Version:** 2.0

## 15. Approval

This policy has been reviewed and approved by:

| Name | Role | Date |
|---|---|---|
| Mo Messidi | Chief Executive Officer, Deal Intelligence LLC | [CONFIRM: date] |

## 16. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Roles consolidated to CEO and Go-to-Market Contractor; MFA described as Google Workspace / GitHub / AWS enforcement; segregation of duties restated as the PR + CI-gate control; monthly configuration-check Lambda record with real-time CloudTrail-EventBridge alerting; bastion and sub-processor wording aligned to the operated environment |
