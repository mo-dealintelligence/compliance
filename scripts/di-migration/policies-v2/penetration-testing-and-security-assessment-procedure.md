---
title: "Penetration Testing and Security Assessment Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "penetration-testing-and-security-assessment-procedure-v1.0.pdf"
---

# Penetration Testing and Security Assessment Procedure

## 1. Purpose

This procedure defines how Deal Intelligence LLC assesses the security of its platform through third-party penetration testing and internal security assessments. Its aim is to identify and remediate vulnerabilities before they are exploited, protecting the confidentiality, integrity, and availability of business contact information and customer data.

It implements the assessment requirements of the Information Security Policy and complements the Vulnerability Management Procedure with specific rules for third-party assessments and penetration testing. It supports SOC 2 Trust Services Criteria CC4.1 (ongoing monitoring activities), CC4.2 (evaluation of deficiencies), CC7.1 (detection of actual and attempted attacks), and A1.2 (environmental protections and monitoring).

## 2. Scope

This procedure applies to:

- Annual third-party penetration testing of production AWS infrastructure
- Automated security assessments of the platform
- API endpoint security testing for customer-facing interfaces
- Web application security assessments of the PropelAuth-integrated authentication system
- Infrastructure security reviews of AWS resources documented in the CloudFormation stack di-backend-api-prod
- Container security assessments for Fargate and ECS deployments
- Database security testing for DocumentDB clusters
- Network security assessments of VPC configurations and security groups

Excluded from scope:

- Physical security assessments (not applicable to remote operations)
- Social engineering tests
- Customer-controlled third-party integrations (Slack, CRM systems)

## 3. Definitions

**Penetration testing**: An authorized simulated attack on the production environment to evaluate security controls and identify exploitable vulnerabilities.

**Security assessment**: A systematic evaluation of security controls, configurations, and practices against established standards.

**Vulnerability**: A weakness in system security procedures, design, implementation, or internal controls that could be exploited to violate security policies.

**Critical**: A vulnerability that could result in immediate compromise of customer data or system availability. Remediated within 24 hours (7 days for a dependency CVE rated critical that is not actively exploited).

**High**: A vulnerability presenting significant risk to operations or data security. Remediated within 30 days.

**Medium**: A vulnerability with moderate impact potential. Remediated within 90 days.

**Low**: A vulnerability with minimal impact. Tracked for remediation on a best-effort basis.

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

- Authorizes annual penetration testing engagements
- Reviews and approves remediation priorities
- Reviews the executive summary of assessment findings
- Approves exceptions to remediation timelines when business justified
- Coordinates with the penetration-test vendor
- Provides technical documentation and access for assessments
- Implements remediation measures for identified vulnerabilities
- Validates remediation effectiveness through retesting
- Maintains assessment documentation for audit purposes
- Confirms that assessments meet SOC 2 requirements
- Updates the risk register based on assessment findings per the Risk Assessment Procedure
- Tracks remediation progress against defined timelines
- Records assessment metrics in the compliance platform

### 4.2 External parties

- **Penetration-test vendor**: Conducts the annual third-party penetration test under the rules of engagement in Section 6 and delivers the report and remediation validation
- **External SOC 2 auditor**: Provides independent review of assessment reports and remediation evidence

## 5. Assessment types and frequency

### 5.1 Annual third-party penetration testing

**Scope requirements**

- External network penetration testing of public-facing infrastructure
- Web application testing of API endpoints and authentication systems
- AWS cloud configuration review against CIS benchmarks
- Container security assessment of ECR images and ECS configurations
- Database security testing, including access controls and encryption validation

**Timing**

- Conducted annually in Q3 to align with the SOC 2 audit cycle
- Scheduled during the maintenance windows defined in the Change Management Policy
- Minimum 30 days' advance notice to customers for any service impact

### 5.2 Automated security assessments

**Automated scanning**

- Monthly configuration-check Lambda run against a fixed checklist (CloudTrail enabled and log-file validation, no public S3 buckets, no security groups open to 0.0.0.0/0 on administrative ports, root account MFA, IAM password policy, KMS key rotation, ECR scan-on-push, DocumentDB backup retention and Multi-AZ), posting a dated pass/fail record to the compliance platform
- Container image scanning in ECR with each deployment (scan-on-push)
- Dependency vulnerability checks via GitHub Dependabot and code scanning, and Trivy in GitHub Actions
- Infrastructure configuration checks via CloudFormation drift reporting and the monthly configuration-check Lambda

**Access review**

- Quarterly access review of IAM policies and access permissions (scheduled Lambda check), recorded in the compliance platform

### 5.3 Continuous security monitoring

Assessment activity uses the monitoring defined in the System Monitoring and Logging Procedure:

- Real-time detection of security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) via an EventBridge rule that triggers the breach-detection Lambda, which sends an SNS alert to the CEO
- CloudTrail analysis for unauthorized access attempts
- CloudWatch alerts for security anomalies
- Monthly configuration-check record review and prioritization of failed checks

## 6. Penetration testing process

### 6.1 Pre-engagement requirements

**Vendor selection**

- Vendors must hold SOC 2 or ISO 27001 certification
- Vendors must have expertise in AWS cloud security and serverless architectures
- A non-disclosure agreement is executed per the Vendor Management Policy

**Scoping documentation**

- Current architecture diagrams and network topology
- List of in-scope IP addresses, domains, and AWS resources
- API documentation and authentication mechanisms
- Known vulnerabilities from previous assessments
- Business-critical systems requiring careful testing

### 6.2 Rules of engagement

**Authorized testing methods**

- Black box testing of the external attack surface
- Gray box testing with limited credentials for authenticated assessments
- White box testing with full documentation for in-depth review
- Automated vulnerability scanning within the rate limits of the API Security and Rate Limiting Standard

**Prohibited activities**

- Denial of service attacks or resource exhaustion
- Data exfiltration beyond proof of concept
- Modification or deletion of production data
- Social engineering of Deal Intelligence personnel
- Testing outside the defined scope or timeframes

### 6.3 Testing execution

**Communication requirements**

- Daily status updates during active testing periods
- Immediate notification of critical findings to the CEO
- Coordination for any testing requiring system access
- Adherence to the 100 requests/minute rate limit for API testing

**Testing phases**

1. **Reconnaissance**: OSINT gathering and attack surface mapping
2. **Scanning**: Automated vulnerability identification
3. **Enumeration**: Service and version detection
4. **Exploitation**: Controlled vulnerability validation
5. **Post-exploitation**: Impact assessment without data access
6. **Reporting**: Documentation of findings

### 6.4 Post-assessment activities

**Report requirements**

- Executive summary with risk ratings
- Detailed technical findings with reproduction steps
- CVSS score for each vulnerability
- Remediation recommendations with priority rankings
- Mapping to SOC 2 criteria

**Remediation validation**

- Retesting of Critical and High findings within the remediation timelines
- Verification letter upon successful remediation
- Risk register updated per the Risk Assessment Procedure

## 7. Internal security assessments

### 7.1 Self-assessment procedures

The CEO conducts a monthly security review and records it in the compliance platform. The review covers:

- The monthly configuration-check record and remediation of failed checks
- Container vulnerability scan results from ECR
- GitHub Dependabot alerts for code dependencies
- CloudFormation drift reporting

### 7.2 Code security reviews

Code security reviews follow the Secure Software Development Lifecycle (SDLC) Standard:

- Static application security testing (SAST) via GitHub Actions (Bandit)
- Software composition analysis for open-source vulnerabilities
- Secret scanning in code repositories (TruffleHog)
- Pull request self-review and required CI status checks on the protected `main` branch before production deployment

## 8. Vulnerability management integration

Assessment findings are managed according to the Vulnerability Management Procedure.

**Severity classification**

- Critical: CVSS 9.0–10.0 or immediate data breach risk
- High: CVSS 7.0–8.9 or significant security impact
- Medium: CVSS 4.0–6.9 or moderate risk
- Low: CVSS 0.1–3.9 or minimal impact

**Remediation timelines**

- Critical: within 24 hours for exploited or critical-rated findings, using the emergency change process (pull request labelled `emergency` with post-hoc review within 5 business days); within 7 days for dependency CVEs rated critical
- High: within 30 days through normal change management
- Medium: within 90 days through normal change management
- Low: best effort or next release cycle

**Tracking and reporting**

- Findings logged in GitHub Issues with security labels
- Remediation progress tracked in the compliance platform

## 9. Third-party integration security

Security assessments evaluate integrations per the Integration security section of the API Security and Rate Limiting Standard:

- PropelAuth authentication flow security
- JWT token validation and session management
- API key management and rotation procedures
- Customer-controlled integration permissions
- Data flow analysis between systems

## 10. Records and customer notification

### 10.1 Evidence

The following assessment records are maintained for audit purposes:

- Penetration testing reports and remediation evidence
- Vulnerability scan results
- Remediation validation and retesting results
- Risk acceptance documentation for exceptions

### 10.2 Customer notification

- Critical vulnerabilities affecting customer data trigger incident response per the Incident Response Procedure
- Assessment reports are available to customers on request under NDA
- An annual attestation of security assessment completion is produced

## 11. Continuous improvement

After each assessment the CEO reviews:

- Common vulnerability patterns requiring systemic fixes
- Effectiveness of existing security controls
- Gaps in security monitoring coverage
- Opportunities for further automation
- Training needs identified through findings

## 12. Review

This procedure is reviewed annually or upon:

- Significant changes to the AWS infrastructure architecture
- Introduction of new technologies or platforms
- Major security incidents or assessment findings
- Changes to SOC 2 requirements or industry standards
- Lessons learned from penetration testing exercises

## 13. Related documents

- Information Security Policy
- Risk Assessment Procedure
- Vulnerability Management Procedure
- Incident Response Procedure
- Change Management Policy
- Cloud Infrastructure Security Policy
- Secure Software Development Lifecycle (SDLC) Standard
- API Security and Rate Limiting Standard
- System Monitoring and Logging Procedure
- Vendor Management Policy
- Business Continuity Plan

## 14. Revision history

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|2.0|<to be set at publication>|Roles consolidated to CEO plus external parties; budget, KPI and program-maturity sections removed; automated scanning and monitoring claims restated as the monthly configuration-check Lambda, CloudTrail-EventBridge event alerting, CloudFormation drift reporting, ECR scan-on-push, Dependabot/code scanning and Trivy; remediation timelines aligned; annual third-party test retained|
