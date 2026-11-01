---
title: "Penetration Testing and Security Assessment Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "penetration-testing-and-security-assessment-procedure-v1.0.pdf"
---

# Penetration Testing and Security Assessment Procedure

## 1. Purpose

This Penetration Testing and Security Assessment Procedure establishes the formal framework for conducting systematic security assessments of Deal Intelligence LLC's platform. This procedure ensures that security vulnerabilities are proactively identified and remediated before they can be exploited, maintaining the confidentiality, integrity, and availability of business contact information and customer data.

This procedure operationalizes the security assessment requirements defined in the Information Security Policy and complements the Vulnerability Management Procedure by providing specific guidance for third-party security assessments and penetration testing activities. It directly supports SOC 2 Trust Services Criteria CC4.1 (Monitoring Activities) and CC7.1 (Detection and Monitoring).

## 2. Scope

This procedure applies to:

- Annual third-party penetration testing of production AWS infrastructure

- Quarterly automated security assessments of the platform

- API endpoint security testing for customer-facing interfaces

- Web application security assessments of the PropelAuth-integrated authentication system

- Infrastructure security reviews of AWS resources documented in CloudFormation stack di-backend-api-prod

- Container security assessments for Fargate and ECS deployments

- Database security testing for DocumentDB clusters

- Network security assessments of VPC configurations and security groups

Excluded from scope:

- Physical security assessments (not applicable for remote operations)

- Social engineering tests

- Customer-controlled third-party integrations (Slack, CRM systems)

## 3. Definitions

**Penetration Testing**: Authorized simulated cyber attack on the production environment to evaluate security controls and identify exploitable vulnerabilities.

**Security Assessment**: Systematic evaluation of security controls, configurations, and practices against established standards and best practices.

**Vulnerability**: A weakness in system security procedures, design, implementation, or internal controls that could be exploited to violate security policies.

**Critical Finding**: A vulnerability that could result in immediate compromise of customer data or system availability, requiring remediation within 24 hours (7 days for a dependency CVE rated critical that is not actively exploited).

**High-Risk Finding**: A vulnerability presenting significant risk to operations or data security, requiring remediation within 30 days.

**Medium-Risk Finding**: A vulnerability with moderate impact potential, requiring remediation within 90 days.

**Low-Risk Finding**: A vulnerability with minimal impact, tracked for remediation on a best-effort basis.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer

- Authorizes annual penetration testing engagements

- Reviews and approves remediation priorities

- Reviews executive summary of assessment findings

- Approves exceptions to remediation timelines when business justified

- Coordinates with third-party penetration testing vendors

- Provides technical documentation and access for assessments

- Implements remediation measures for identified vulnerabilities

- Validates remediation effectiveness through retesting

- Maintains assessment documentation for audit purposes

- Ensures assessments meet SOC 2 requirements

- Updates risk register based on assessment findings per Risk Assessment Procedure

- Tracks remediation progress against defined timelines

- Records assessment metrics in the compliance platform

### 4.2 External Parties

- **Penetration-test vendor**: Conducts the annual third-party penetration test under the rules of engagement in Section 6 and delivers the report and remediation validation

- **External SOC 2 auditor**: Provides independent review of assessment reports and remediation evidence

## 5. Assessment Types and Frequency

### 5.1 Annual Third-Party Penetration Testing

#### Scope Requirements:

- External network penetration testing of public-facing infrastructure

- Web application testing of API endpoints and authentication systems

- AWS cloud configuration review against CIS benchmarks

- Container security assessment of ECR images and ECS configurations

- Database security testing including access controls and encryption validation

#### Timing:

- Conducted annually in Q3 to align with SOC 2 audit cycle

- Scheduled during maintenance windows defined in Change Management Policy

- Minimum 30-day advance notice to customers for any service impact

### 5.2 Quarterly Automated Security Assessments

#### Automated Scanning:

- Continuous AWS Security Hub checks against the Foundational Security Best Practices, reviewed monthly

- Container image scanning in ECR with each deployment (scan-on-push)

- Dependency vulnerability checks via GitHub Dependabot and code scanning, and Trivy in GitHub Actions

- Infrastructure configuration checks via CloudFormation drift reporting and Security Hub configuration checks

#### Manual Reviews:

- Quarterly review of IAM policies and access permissions

- Security group and network ACL configuration audits

- CloudFormation template security analysis

- Secrets management review for API keys and credentials

### 5.3 Continuous Security Monitoring

Integration with existing monitoring infrastructure per System Monitoring and Logging Procedure:

- Real-time detection via AWS Security Hub findings routed to SNS by the breach-detection Lambda

- CloudTrail analysis for unauthorized access attempts

- CloudWatch alerts for security anomalies

- Security Hub findings aggregation and prioritization

## 6. Penetration Testing Process

### 6.1 Pre-Engagement Requirements

#### Vendor Selection:

- Vendors must demonstrate SOC 2 or ISO 27001 certification

- Required expertise in AWS cloud security and serverless architectures

- Non-disclosure agreement execution per Vendor Management Policy

- Professional liability insurance minimum $1 million coverage

#### Scoping Documentation:

- Current architecture diagrams and network topology

- List of in-scope IP addresses, domains, and AWS resources

- API documentation and authentication mechanisms

- Known vulnerabilities from previous assessments

- Business-critical systems requiring careful testing

### 6.2 Rules of Engagement

#### Authorized Testing Methods:

- Black box testing for external attack surface

- Gray box testing with limited credentials for authenticated assessments

- White box testing with full documentation for comprehensive review

- Automated vulnerability scanning with rate limiting compliance per API Security and Rate Limiting Standard

#### Prohibited Activities:

- Denial of service attacks or resource exhaustion

- Data exfiltration beyond proof of concept

- Modification or deletion of production data

- Social engineering of Deal Intelligence personnel

- Testing outside defined scope or timeframes

### 6.3 Testing Execution

#### Communication Requirements:

- Daily status updates during active testing periods

- Immediate notification of critical findings to the CEO

- Coordination for any testing requiring system access

- Adherence to 100 requests/minute rate limiting for API testing

#### Testing Phases:

1. **Reconnaissance**: OSINT gathering and attack surface mapping

2. **Scanning**: Automated vulnerability identification

3. **Enumeration**: Service and version detection

4. **Exploitation**: Controlled vulnerability validation

5. **Post-Exploitation**: Impact assessment without data access

6. **Reporting**: Comprehensive documentation of findings

### 6.4 Post-Assessment Activities

#### Report Requirements:

- Executive summary with risk ratings

- Detailed technical findings with reproduction steps

- CVSS scoring for each vulnerability

- Remediation recommendations with priority rankings

- Compliance mapping to SOC 2 criteria

#### Remediation Validation:

- Retesting of critical and high-risk findings within remediation timelines

- Verification letter upon successful remediation

- Updated risk assessment per organizational risk register

## 7. Internal Security Assessments

### 7.1 Self-Assessment Procedures

Monthly security reviews conducted by the CEO and recorded in the compliance platform:

- AWS Security Hub findings review and remediation

- Container vulnerability scan results from ECR

- GitHub Dependabot alerts for code dependencies

- CloudFormation drift reporting analysis

- IAM access analyzer findings

### 7.2 Configuration Reviews

Quarterly configuration assessments:

- VPC security group rules against principle of least privilege

- S3 bucket policies and public access blocks

- KMS key policies and rotation schedules

- Lambda function permissions and resource policies

- CloudFront and Lambda function URL security configurations

### 7.3 Code Security Reviews

Integrated with Secure Software Development Lifecycle (SDLC) Standard:

- Static application security testing (SAST) via GitHub Actions (Bandit)

- Software composition analysis for open-source vulnerabilities

- Secret scanning in code repositories (TruffleHog)

- Pull request self-review and required CI status checks on the protected `main` branch before production deployment

## 8. Vulnerability Management Integration

Assessment findings are managed according to the Vulnerability Management Procedure:

#### Severity Classification:

- Critical: CVSS 9.0-10.0 or immediate data breach risk

- High: CVSS 7.0-8.9 or significant security impact

- Medium: CVSS 4.0-6.9 or moderate risk

- Low: CVSS 0.1-3.9 or minimal impact

#### Remediation Timelines:

- Critical: 24 hours for exploited or critical-rated findings, using the emergency change process (pull request labelled `emergency` with post-hoc review within 5 business days); 7 days for dependency CVEs rated critical

- High: 30 days through normal change management

- Medium: 90 days through normal change management

- Low: Best effort or next release cycle

#### Tracking and Reporting:

- Findings logged in GitHub Issues with security labels

- Remediation progress tracked in the compliance platform

- Monthly metrics reported including mean time to remediation

- Quarterly trend analysis of vulnerability categories

## 9. Third-Party Integration Security

Security assessments must evaluate integrations per the Integration security section of the API Security and Rate Limiting Standard:

- PropelAuth authentication flow security

- JWT token validation and session management

- API key management and rotation procedures

- Customer-controlled integration permissions

- Data flow analysis between systems

## 10. Compliance and Regulatory Requirements

### 10.1 SOC 2 Requirements

This procedure addresses the following Trust Services Criteria:

- CC4.1: COSO Principle 16 - Ongoing monitoring activities

- CC4.2: COSO Principle 17 - Evaluations of deficiencies

- CC7.1: Detection of actual and attempted attacks

- A1.2: Environmental protections and monitoring

### 10.2 Evidence Collection

Assessment documentation maintained for audit purposes:

- Penetration testing reports and remediation evidence

- Vulnerability scan results and trending data

- Configuration review checklists and findings

- Remediation validation and retesting results

- Risk acceptance documentation for exceptions

### 10.3 Customer Notification

Per data protection requirements:

- Critical vulnerabilities affecting customer data trigger incident response per Incident Response Procedure

- Assessment reports available to customers upon request under NDA

- Annual attestation of security assessment completion

## 11. Continuous Improvement

Post-assessment reviews conducted to identify:

- Common vulnerability patterns requiring systemic fixes

- Effectiveness of existing security controls

- Gaps in security monitoring coverage

- Opportunities for automation enhancement

- Training needs identified through findings

## 12. Related Documents

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

## 13. Policy Review and Updates

This procedure is reviewed annually or upon:

- Significant changes to AWS infrastructure architecture

- Introduction of new technologies or platforms

- Major security incidents or assessment findings

- Changes to SOC 2 requirements or industry standards

- Lessons learned from penetration testing exercises

## 14. Revision History

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|2.0|<to be set at publication>|Roles consolidated to CEO plus external parties; budget, KPI and program-maturity sections removed; automated scanning and monitoring claims restated as Security Hub, CloudFormation drift reporting, ECR scan-on-push, Dependabot/code scanning and Trivy; remediation timelines aligned; annual third-party test retained|
