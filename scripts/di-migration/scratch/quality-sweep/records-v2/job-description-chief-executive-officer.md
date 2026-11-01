---
title: "Job Description - Chief Executive Officer"
doc_type: "Record"
version: "2.0"
supersedes: "1.0"
acknowledgment: "None"
effective_date: "N/A"
review_date: "N/A"
finalized_at: ""
author: "Mo Messidi"
source: "job-description-chief-executive-officer-v1.0.pdf"
---

# Job Description - Chief Executive Officer

## 1. Position summary

The Chief Executive Officer (CEO) is responsible for the strategic direction, technical architecture, security, compliance, and day-to-day operations of Deal Intelligence LLC. The CEO is the architect and developer of the AI-powered B2B market intelligence platform, owns every policy and control, and is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration).

The CEO is accountable for SOC 2 Type II (Security, Availability, and Confidentiality), GDPR, and CCPA compliance across all organizational activities, and for protecting the confidentiality and integrity of customer data: business contact information, competitor interaction data, and market intelligence.

Reporting relationships are described in the Organizational Structure.

## 2. Access level

| System | Access |
|---|---|
| AWS (production, us-east-1) | Administrative; MFA enforced |
| GitHub (`dealintelligence/di-backend-api`) | Organization owner; MFA enforced |
| DocumentDB | Administrative, through the VPC only |
| PropelAuth | Administrative |
| Google Workspace | Super admin; MFA enforced |
| Compliance platform | Owner |

## 3. Responsibilities

### 3.1 Strategic leadership (20 %)

Business strategy:
- Define and execute company vision, mission, and strategic objectives.
- Maintain the product roadmap in line with market demand and compliance requirements.
- Make business decisions balancing growth, security, and compliance.
- Manage company finances, budget allocation, and resource planning.
- Pursue growth opportunities without weakening the security posture.
- Enter partnerships with due diligence per the Vendor Management Policy.

Leadership and governance:
- Set security and compliance expectations for contractor personnel.
- Maintain a culture of integrity, security awareness, and ethical conduct as defined in the Code of Conduct.
- Represent the company to customers, partners, auditors, and stakeholders.
- Make hiring and contractor-engagement decisions, with background verification.
- Chair the quarterly management review and record decisions in the management meeting minutes (see Management Meeting Minutes - Q4 2025).
- Confirm that all personnel complete security awareness training per the Security Awareness Training Program.

### 3.2 Technical architecture and development (40 %)

System architecture:
- Design and maintain the platform's system architecture.
- Make technology-stack decisions in line with security and compliance requirements.
- Maintain scalability, performance, and availability across the AWS infrastructure.
- Optimize infrastructure cost without removing security controls.
- Plan technical growth on security-by-design principles.
- Maintain architecture documentation per the Cloud Infrastructure Security Policy.

Software development:
- Develop and maintain the codebase following the Secure Software Development Lifecycle (SDLC) Standard.
- Implement features and enhancements with security review.
- Fix bugs and resolve technical issues with change documentation.
- Submit every change as a pull request on the protected `main` branch, with required CI status checks and a logged self-review in the pull request.
- Maintain technical documentation, including API specifications, per the API Security and Rate Limiting Standard.
- Maintain the automated security checks in the GitHub Actions pipeline (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog).

Infrastructure management:
- Manage the AWS infrastructure: Lambda functions, Fargate containers, DocumentDB, and supporting services.
- Configure and maintain the VPC: private subnets, security groups, and network access controls.
- Manage container orchestration via ECS with ECR scan-on-push enabled.
- Maintain the CloudFront configuration.
- Maintain the Multi-AZ deployment (us-east-1a, us-east-1b).
- Maintain infrastructure as code via CloudFormation through the Serverless Framework (stack: di-backend-api-prod).

### 3.3 Security and compliance (25 %)

Security program:
- Act as the designated security and data-protection contact for Deal Intelligence.
- Establish, implement, and maintain the information security program per the Information Security Policy.
- Maintain compliance with the SOC 2 Trust Services Criteria for Security, Availability, and Confidentiality.
- Maintain GDPR and CCPA compliance for B2B data processing.
- Conduct and document risk assessments in the compliance platform's risk register per the Risk Assessment Procedure.
- Oversee vulnerability management and remediation per the Vulnerability Management Procedure.
- Coordinate the annual penetration test per the Penetration Testing and Security Assessment Procedure.

Access control and authentication:
- Manage the PropelAuth JWT configuration with Google Workspace single sign-on (customer MFA inherited from Google Workspace).
- Maintain role-based access control (RBAC) on the least-privilege principle.
- Maintain user- and company-level data isolation within the platform.
- Conduct quarterly access reviews via the access-review Lambda function.
- Maintain session timeout and access logging per the Access Control and Authentication Policy.

Data protection:
- Classify and handle data per the Data Classification and Handling Standard.
- Maintain encryption controls per the Encryption and Cryptographic Controls Standard.
- Oversee data retention (24 months for active leads, 90 days for logs) per the Data Retention and Disposal Policy.
- Maintain PII sanitization in logs.
- Process data subject rights requests per the Data Subject Rights Request Procedure.
- Maintain Data Processing Agreements with sub-processors (PropelAuth, AWS).

Monitoring and incident response:
- Maintain CloudWatch monitoring and alarms with 90-day log retention.
- Maintain the audit-logging middleware for all API requests.
- Maintain CloudTrail for AWS API calls.
- Review the monthly configuration-check record posted by the configuration-check Lambda and remediate any failed item; security-relevant CloudTrail events alert in real time via EventBridge, the breach-detection Lambda, and SNS.
- Record the monthly availability figure in the compliance platform task "Availability record (monthly)".
- Act as incident commander per the Incident Response Procedure.
- Notify affected customers within 48 hours of a confirmed breach.
- Record incidents in the compliance platform.
- Complete post-incident retrospectives within 24 hours for emergency changes.

Change management:
- Approve all production changes per the Change Management Policy.
- Maintain the GitHub Actions CI pipeline with automated testing and security scans.
- Enforce branch protection on `main`: pull request required, CI status checks required, no direct pushes.
- Validate changes on the staging stage before production release.
- Deploy to production only from a green CI run.
- Maintain rollback via Lambda versioned deployments and `serverless rollback`.

### 3.4 Business continuity and vendor management (15 %)

Business continuity:
- Maintain and test the Business Continuity Plan, with records in the compliance platform.
- Maintain recovery capability against the RTO/RPO objectives.
- Oversee daily automated backups with 90-day retention.
- Conduct the quarterly backup restoration test.
- Maintain the 99.9 % uptime SLA per the Service Level Agreement (SLA) Management Policy.
- Manage capacity planning. [CONFIRM: v1 cited a "Capacity Management Policy and Procedures" that is not in the document set]

Vendor management:
- Evaluate and approve all third-party vendors through the compliance platform's vendor assessment.
- Maintain the sub-processor model (PropelAuth, AWS).
- Maintain Data Processing Agreements with all sub-processors.
- Give customers 30 days' notice of sub-processor changes.
- Conduct the annual vendor security review per the Vendor Management Policy.
- Review third-party integration security per the API Security and Rate Limiting Standard (Integration security section).

## 4. Required competence

Education and experience:
- Bachelor's degree in Computer Science, Information Technology, or a related field, or equivalent experience.
- 5+ years of experience in software development and system architecture.
- 3+ years of experience in cloud infrastructure management (AWS preferred).
- Experience with security and compliance frameworks.
- Experience leading technical organizations.

Technical knowledge:
- AWS: Lambda, Fargate, DocumentDB, ECS, VPC, CloudFront, CloudWatch, CloudTrail.
- The programming languages used for platform development.
- Infrastructure as code: CloudFormation via the Serverless Framework.
- Security tooling: CloudTrail and EventBridge event rules, vulnerability scanners (ECR scan-on-push, Dependabot, Trivy), SIEM concepts.
- CI/CD: GitHub Actions, automated testing, deployment pipelines.
- Authentication: JWT, OAuth, MFA.

Security and compliance knowledge:
- SOC 2 Trust Services Criteria and audit requirements.
- GDPR and CCPA requirements for B2B data processing.
- Encryption standards and key management.
- Secure software development practices.
- Incident response and business continuity principles.

## 5. Authority and decision rights

Full authority:
- Strategic direction and business decisions.
- Technology stack and architecture decisions.
- Production deployment approvals.
- Security policy exceptions, with documented justification.
- Vendor selection and contract approval.
- Budget allocation and resource prioritization.
- Hiring and contractor engagement decisions.

Shared authority:
- Compliance framework interpretation, with the external auditor or advisors.
- Customer contract terms, with legal review where needed.

Matters recorded in the management meeting minutes:
- Material security incidents affecting customer data.
- Significant compliance gaps or audit findings.
- Major strategic pivots or business model changes.

## 6. Performance metrics

### 6.1 Security and compliance

| Metric | Target |
|---|---|
| SOC 2 Type II status | Maintained |
| Security incidents (P1/P2) | 0 per quarter |
| Vulnerability remediation (Critical) | Within 24 hours |
| Vulnerability remediation (High) | Within 30 days |
| Access review completion | 100 % quarterly |
| Security training completion | 100 % annually |

### 6.2 Operational

| Metric | Target |
|---|---|
| Platform uptime | ≥ 99.9 % |
| API response time (p95) | Per SLA requirements |
| Backup success rate | 100 % |
| Backup restoration test | Quarterly |
| Change success rate | ≥ 95 % |

### 6.3 Business

[CONFIRM: v1 listed customer satisfaction, revenue growth, and operational efficiency with target "As defined" — set targets or remove the section]

## 7. Acknowledgment of responsibilities

By accepting this position, the CEO acknowledges:

1. Accountability for the security, availability, and integrity of Deal Intelligence's systems and customer data.
2. Commitment to maintaining SOC 2 Type II and GDPR/CCPA compliance.
3. Agreement to uphold the Code of Conduct.
4. Obligation to protect confidential information per the Data Classification and Handling Standard.
5. Commitment to ongoing security awareness and compliance improvement.

| Field | Value |
|---|---|
| Name | Mo Messidi |
| Signature | _________________________ |
| Date | _________________________ |

## 8. Related documents

- Organizational Structure
- Information Security Policy
- Code of Conduct
- Acceptable Use Policy
- Access Control and Authentication Policy
- Incident Response Procedure
- Change Management Policy
- Business Continuity Plan

## 9. Revision history

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [CONFIRM: date] | Mo Messidi | Initial job description |
| 2.0 | [CONFIRM: date] | Mo Messidi | Recruiting copy removed; access level added; role, product, and number wording per RULEBOOK R2, R4, R5; references to documents not in the set removed; control-automation metric struck (D17); High-severity remediation target set to 30 days (D8); Security Hub review replaced by the monthly configuration-check record and real-time CloudTrail-EventBridge alerts, monthly availability record added (D12, D13b) |
