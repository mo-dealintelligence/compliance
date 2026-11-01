---
title: "Organizational Structure"
doc_type: "Record"
version: "2.0"
supersedes: "1.0"
acknowledgment: "None"
effective_date: "N/A"
review_date: "N/A"
finalized_at: "November 30, 2025 at 10:32 PM"
author: "Mo Messidi"
source: "organizational-structure-v1.0.pdf"
---

# Organizational Structure

## 1. Purpose and scope

This document defines the organizational structure of Deal Intelligence LLC: the roles that exist, their responsibilities, their access, and their accountability for the AI-powered B2B market intelligence platform and the SOC 2 compliance program (Security, Availability, and Confidentiality).

## 2. Roles

| Role | Holder | Production access | Reports to |
|---|---|---|---|
| Chief Executive Officer (CEO) | Mo Messidi | Yes — the only role with access to AWS, GitHub, DocumentDB, and PropelAuth administration | Management (quarterly management meeting) |
| Go-to-Market Contractor | William Wickey | None | CEO |

External parties: the external SOC 2 auditor, the penetration-test vendor, and the sub-processors listed in Section 5.

## 3. Governance model

The CEO owns every policy and control, approves exceptions, acts as incident commander, and is the data protection contact. Governance decisions are recorded in the quarterly management meeting minutes. Automation and AWS-managed services carry out most control execution; the compliance platform is the control register and holds the dated evidence.

Because the CEO is the only role with production access, segregation of duties between development, change approval, and production operation is achieved through compensating controls: a pull request with required CI status checks on the protected `main` branch, a logged self-review in each pull request, automated checks (Security Hub, CloudTrail) with critical findings alerting via SNS, and independent review by the external SOC 2 auditor.

## 4. Responsibilities of the CEO

### 4.1 Strategic functions

- Strategic direction: business strategy, vision, and decision-making for the platform.
- Product management: product strategy, roadmap, and feature prioritization.
- Customer success: customer support, satisfaction monitoring, and relationship management (with the Go-to-Market Contractor; see Section 4.5).

### 4.2 Technical functions

- Engineering: application development, maintenance, and architecture decisions.
- Infrastructure: AWS infrastructure management, deployment automation, and system reliability.
  - AWS resources defined in the CloudFormation stack di-backend-api-prod (deployed via the Serverless Framework).
  - Lambda functions, Fargate containers, and DocumentDB operations.
  - Multi-AZ deployment (us-east-1a, us-east-1b).

### 4.3 Compliance and security functions

- Security: information security program and technical security controls.
  - Security controls per the Information Security Policy, including encryption, access controls, and monitoring.
  - Incident response per the Incident Response Procedure.
- Compliance: SOC 2, GDPR, and CCPA program management.
  - Policy development and maintenance.
  - Control implementation and monitoring in the compliance platform's control register.
  - Audit coordination and evidence collection.
  - Privacy and data protection oversight.

### 4.4 Risk management

- Risk assessment: quarterly risk review in the compliance platform's risk register.
- Vendor management: third-party risk evaluation and annual review per the Vendor Management Policy.
- Business continuity: recovery planning and the quarterly backup restoration test per the Business Continuity Plan, recorded in the compliance platform.

### 4.5 Responsibilities of the Go-to-Market Contractor

Customer acquisition, sales and marketing, customer support, and market intelligence, as set out in Job Description - Go-to-Market Contractor. The role has no production access and is subject to onboarding, security awareness training, policy acknowledgments, the Acceptable Use Policy, and confidentiality obligations. Technical, security, and compliance matters are escalated to the CEO.

## 5. External support

### 5.1 Infrastructure and platform services (AWS)

- Compute and data: Lambda, Fargate, DocumentDB.
- Security services: KMS, Security Hub, CloudTrail, CloudWatch.
- Content delivery and networking: CloudFront, VPC.

### 5.2 Sub-processors

- AWS: infrastructure hosting (us-east-1).
- PropelAuth: authentication and identity management (JWT, Google Workspace single sign-on, RBAC).

### 5.3 Other vendors

- GitHub: source control and GitHub Actions CI.
- Google Workspace: personnel email and identity.
- Resend: transactional email.
- The compliance platform: self-hosted on AWS; risk register, incident records, business continuity records, vendor assessments, and asset inventory.

### 5.4 Contractors and consultants

Engaged as needed for:
- The annual penetration test per the Penetration Testing and Security Assessment Procedure.
- SOC 2 audit support.
- Technical implementations requiring specialized knowledge.

## 6. Compliance oversight

The CEO has direct oversight of all compliance activities.

### 6.1 Security controls

- Implementation of technical and administrative controls.
- Monitoring of control effectiveness in the compliance platform's control register. [CONFIRM: v1 read "current 86% automation rate" — struck per R4]
- Remediation of control gaps (2 controls planned for Q1–Q2 2026).
- Security awareness training per the Security Awareness Training Program.

### 6.2 Policy management

- Policy adherence and enforcement.
- Annual policy review and update.
- Communication of policy requirements.
- Alignment with the Code of Conduct.

### 6.3 Risk management

- Risk assessment and treatment.
- Vendor risk evaluation in the compliance platform.
- Change management oversight per the Change Management Policy.
- Continuous monitoring and improvement.

### 6.4 Incident response

- Incident commander.
- Customer breach notification within 48 hours.
- Post-incident review and remediation.
- Incident records in the compliance platform.

### 6.5 Data protection

- GDPR and CCPA compliance oversight.
- Data subject rights management per the Data Subject Rights Request Procedure.
- Data classification enforcement per the Data Classification and Handling Standard.
- Privacy program management.

## 7. Accountability and reporting

### 7.1 Accountability

The CEO is accountable to:
- Customers, for service delivery and data protection.
- Regulatory authorities, for compliance with applicable laws.
- The external auditor, for the SOC 2 Type II examination.

### 7.2 External reporting

- Customer communications: updates on security posture and compliance status.
- Audit reports: annual SOC 2 Type II report.
- Regulatory filings: as required by GDPR, CCPA, and other applicable regulations.

## 8. Revision history

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | November 30, 2025 | Mo Messidi | Initial document |
| 2.0 | [CONFIRM: date] | Mo Messidi | Roles listed by title with access level; "founder/owner" → CEO; Go-to-Market Contractor added; size language and resource counts removed per RULEBOOK R2 and R4; compensating controls stated |
