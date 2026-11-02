---
title: "Section 3 — Description of Deal Intelligence LLC's B2B Market Intelligence Platform"
doc_type: "System Description"
version: "2.0"
supersedes: "1.0 (draft of November 23, 2025)"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
acknowledgment: "None"
author: "Mo Messidi"
source: "data/system-description-draft-nov2025.md, amended per policies-v2/RULEBOOK.md"
trust_services_categories: "Security, Availability, Confidentiality"
---

# Section 3 — Description of Deal Intelligence LLC's B2B Market Intelligence Platform

**SOC 2 Type II — Security, Availability, and Confidentiality**

Description as of [CONFIRM: as-of date] and for the period [CONFIRM: period start] to [CONFIRM: period end].

This document contains confidential and proprietary information. Not for distribution outside the audit engagement.

This description is prepared in accordance with the AICPA Description Criteria for a Description of a Service Organization's System in a SOC 2 Report (DC section 200, 2018, with 2022 implementation guidance). It covers the trust services criteria for Security, Availability, and Confidentiality. "Deal Intelligence" and "the organization" refer to Deal Intelligence LLC; "the platform" refers to Deal Intelligence LLC's B2B market intelligence platform.

## Table of contents

1. Services provided
2. Principal service commitments and system requirements
3. System components
4. System boundaries
5. Subservice organizations and other vendors
6. Complementary user entity controls
7. Internal controls
8. System incidents
9. Changes to the system during the period

Appendix — Management's assertion

---

## 1. Services provided

Deal Intelligence LLC provides a business-to-business market intelligence platform that delivers automated lead generation and competitive intelligence to sales and marketing teams in enterprise and mid-market organizations. The platform aggregates, verifies, and delivers business contact information and competitor interaction data.

The platform processes the following data elements: first name, last name, business email address, LinkedIn profile URL, job title, current employer, company name, company domain, competitor interaction data, lead qualification status, and sourcing date. Active leads are retained for 24 months. Customer account data is retained for the duration of the customer relationship plus 24 months. Retention is enforced by scheduled Lambda functions that delete expired records and log each deletion.

Customers access the platform through a web application and an API. Sign-in is provided by PropelAuth using Google Workspace single sign-on as the only sign-in method, so multi-factor authentication is inherited from the customer's Google Workspace configuration. PropelAuth issues JSON Web Tokens (JWTs) that the platform validates on every request. Role-based access control and company-level and user-level data segregation isolate each customer's data in the multi-tenant environment. Customers may connect the platform to their own Slack workspace and CRM; those integrations are configured and controlled by the customer.

The organization operates remotely, with no physical office, and runs the platform entirely on Amazon Web Services (AWS) in the us-east-1 region. All personnel are bound by the Information Security Policy and the Acceptable Use Policy.

---

## 2. Principal service commitments and system requirements

Deal Intelligence makes commitments to customers in service agreements, data processing agreements, and terms of service. The commitments relevant to the applicable trust services criteria are set out below, followed by the system requirements the organization has defined to meet them.

### 2.1 Security commitments

- All user accounts authenticate through PropelAuth using Google Workspace single sign-on, with multi-factor authentication inherited from the customer's Google Workspace sign-in.
- Role-based access control enforces least privilege; each user has unique credentials, and shared accounts are not permitted.
- Customer data is isolated at the company and user level so that no customer can access another organization's data.
- Confirmed security incidents are notified to affected customers within 48 hours, and to the supervisory authority within 72 hours where GDPR applies.
- Access rights are reviewed quarterly and revoked immediately on termination.

### 2.2 Availability commitments

- Platform availability of 99.9 %, measured monthly over all minutes and excluding announced maintenance windows, as defined in customer service level agreements. Authentication availability is provided by PropelAuth under its own SLA.
- Planned maintenance windows are communicated by email 72 hours in advance.
- Recovery time objectives are defined contractually and in the Business Continuity Plan.

### 2.3 Confidentiality commitments

- Customer data is protected under non-disclosure agreements and the confidentiality provisions of service contracts.
- Customer contact information, market intelligence data, and competitive insights are classified as Confidential under a four-tier classification scheme and handled accordingly.
- Data is encrypted at rest (AES-256) and in transit (TLS 1.2 or higher).
- Expired data is removed by cryptographic erasure at the end of the 24-month retention period, with deletion logged.

### 2.4 Processing commitments

- Data is processed completely, accurately, and only as authorized. Lambda functions validate data before it is stored in DocumentDB, and submitted requests are processed within contractually defined timeframes.
- Processing activity is logged in CloudWatch (90-day retention) so that transaction flows can be reconstructed and completeness verified.
- API use is limited to 100 requests per minute per API key, enforced in application middleware, under the fair use terms of customer agreements.

### 2.5 Privacy obligations (GDPR and CCPA)

Privacy obligations are documented in the Privacy Notice and Data Processing Agreement Template and are not examined as SOC 2 Privacy criteria in this report. The organization limits processing of personal information to the business purposes stated in customer agreements; fulfills data subject requests for access, correction, deletion, and portability within 30 days under GDPR and 45 days under CCPA, tracked in the compliance platform; gives 30 days' advance notice of changes to the sub-processor list published in the Privacy Notice; and sanitizes personal information from system logs.

### 2.6 System requirements

To meet these commitments the organization has defined the following system requirements. Each is implemented by the components and controls described in Sections 3 and 7.

| Requirement | Implementation |
|---|---|
| Authentication and access | PropelAuth JWT with Google Workspace single sign-on; role-based access control; session timeouts; quarterly automated access reviews by Lambda; personnel multi-factor authentication enforced in Google Workspace, GitHub, and AWS |
| Network isolation | Single VPC with private subnets; no direct database access from outside the VPC; CloudFront with AWS Shield Standard in front of the API, origin access restricted to the Lambda function URLs |
| Encryption | DocumentDB encrypted with a regional KMS customer-managed production data key; separate customer-managed keys for backups and for audit logs (CloudTrail and CloudWatch Logs), all rotated annually; TLS 1.2 or higher with ACM-managed certificates |
| Secrets | Credentials in AWS Secrets Manager; rotation enabled on the DocumentDB credential; API keys rotated per a documented calendar |
| Infrastructure as code | All production resources defined in the CloudFormation stack `di-backend-api-prod`, deployed by `serverless deploy`, which is the only change path and reports drift |
| Change control | Pull request on the protected `main` branch of `dealintelligence/di-backend-api`; required GitHub Actions status checks; no direct pushes; deployment only from a green CI run |
| Logging and monitoring | CloudWatch logs and alarms (90-day retention); CloudTrail (7-year retention) with security-relevant events alerted in real time via EventBridge, the breach-detection Lambda and SNS; monthly configuration-check Lambda with a dated pass/fail record in the compliance platform; API request logging in middleware |
| Vulnerability management | ECR scan-on-push on all repositories; GitHub Dependabot and code scanning; Trivy in CI; annual third-party penetration test |
| Resilience and recovery | DocumentDB cluster storage replicated across three Availability Zones with automatic re-provisioning of the single serverless instance; daily automated backups retained 35 days with point-in-time recovery; Lambda reserved concurrency and versioned deployments with rollback; quarterly backup-restore test; annual tabletop exercise |
| Third parties | Vendor Management Policy: executed data processing agreements, security assessment, and annual review of PropelAuth and AWS |
| Risk | Risk assessment at least annually, with findings tracked in the compliance platform |
| Governance | The policies, standards, procedures, and plans listed in Section 3.4; the compliance platform as the control register (controls, evidence, tasks) |

---

## 3. System components

### 3.1 Infrastructure

The production environment is the CloudFormation stack `di-backend-api-prod` in a single VPC in the us-east-1 region. Operation in a single region is by design and is stated in the Business Continuity Plan. The network and data-flow diagram is maintained in the compliance platform and reproduced in Figure 1.

**Figure 1 — Network and data-flow diagram.** [Reproduced from the compliance platform; see the asset inventory and network diagram record.]

| Component | Role in the system | Configuration |
|---|---|---|
| Lambda | API request processing and scheduled jobs (access review, retention enforcement, breach detection) | 900-second timeout; reserved concurrency of 100; versioned deployments with rollback via `serverless rollback` |
| Fargate (ECS) | Batch processing with extended execution times | Tasks launched on schedule by EventBridge |
| DocumentDB | Persistent storage of customer and operational data | Single serverless instance; cluster storage replicated six ways across three Availability Zones, instance re-provisioned automatically by the service on failure; encrypted with the regional KMS customer-managed production data key (annual rotation); daily automated backups retained 35 days, encrypted with a separate backup key; point-in-time recovery enabled; private subnets only |
| ECR | Container image storage | Scan-on-push enabled on all repositories |
| EventBridge | Scheduling of batch jobs and control Lambda functions; rule on security-relevant CloudTrail events | Triggers the breach-detection Lambda on root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, and security-group changes |
| CloudFront | Content delivery and API edge, caching static assets and API responses | AWS Shield Standard; TLS 1.2 or higher; origin access restricted to the Lambda function URLs |
| VPC | Network isolation | Private subnets for database and compute; no public database endpoints |
| NAT instance | Outbound traffic and bastion access | The only instance in the environment; accessed through SSM Session Manager; no SSH keys, no public services |
| CloudWatch | Metrics, logs, alarms | 90-day log retention; alarms on API errors and latency (p95 greater than 2 seconds) |
| CloudTrail | AWS API audit log | Retained 7 years in S3 with lifecycle transition to Glacier and Object Lock |
| Configuration-check Lambda | Monthly AWS configuration checks against a fixed checklist (CloudTrail enabled and log-file validation; no public S3 buckets; no security groups open to 0.0.0.0/0 on administrative ports; root account MFA; IAM password policy; KMS key rotation; ECR scan-on-push; DocumentDB backup retention) | Scheduled monthly by EventBridge; posts a dated pass/fail record to the compliance platform |
| Secrets Manager | Credential storage and rotation | Rotation enabled on the DocumentDB credential |
| SNS | Security and availability alerting to the Chief Executive Officer (CEO) | — |
| S3 | CloudTrail archive and platform object storage | — |
| Route 53 | DNS only | — |
| KMS, ACM | Key management; TLS certificates | Regional customer-managed keys with annual rotation: a production data key (DocumentDB, S3, Lambda environment variables), a backup key, and an audit-log key (CloudTrail and CloudWatch Logs), as set out in the Encryption and Cryptographic Controls Standard; ACM-managed certificates |

A staging environment, deployed from the same CloudFormation templates into a separate AWS account in the same AWS Organization, is used for pre-production validation. It holds no production customer data (scrubbed or synthetic data only) and has its own network, database, keys, and secrets; no credential grants access to both accounts' workloads. The staging account is outside the system boundary (Section 4).

### 3.2 Software

| Category | Software |
|---|---|
| Platform runtime | Custom application code in the `dealintelligence/di-backend-api` repository, running on the Lambda runtime and in Fargate containers; CloudFormation templates deployed via the Serverless Framework |
| Authentication | PropelAuth (JWT issuance and validation, Google Workspace single sign-on, role management, session management) |
| Security and monitoring | CloudWatch; CloudTrail; a custom breach-detection Lambda triggered by an EventBridge rule on security-relevant CloudTrail events and alerting via SNS; a monthly configuration-check Lambda against a fixed checklist |
| Development and CI | GitHub (source control, Dependabot, code scanning); GitHub Actions running Black, isort, Flake8, Bandit, pytest, Trivy, and TruffleHog on every pull request. TruffleHog secret scanning prevents secrets entering the repository [CONFIRM: whether pre-commit hooks are also configured locally] |
| Business operations | CRM integrations; Slack for operational notifications; Resend for transactional email; the compliance platform for policies, the control register, evidence, acknowledgments, training records, and incident records |

### 3.3 People

Deal Intelligence has two internal roles.

- **Chief Executive Officer (CEO).** Owns every policy and control. The CEO is the only role with production access (AWS, GitHub, DocumentDB, PropelAuth administration), the approver of exceptions, the incident commander, and the data protection contact. The CEO's responsibilities cover security management (policy, risk assessment, incident response), infrastructure operations (AWS resource management, monitoring, capacity), development (code, testing, deployment, maintenance), and compliance (SOC 2 control implementation, audit coordination, documentation).
- **Go-to-Market Contractor.** Supports sales and marketing. Has no production access and is subject to onboarding, security awareness training, policy acknowledgments, the Acceptable Use Policy, and confidentiality obligations.

External parties supporting the control environment are the external SOC 2 auditor, the penetration-test vendor, and the subservice organizations and other vendors listed in Section 5.

**Segregation of duties.** Because production access is held by one role, the organization does not segregate development, change approval, and production operation across separate personnel. The compensating controls are:

1. every change to `dealintelligence/di-backend-api` is made by pull request on the protected `main` branch, passes the required CI status checks, and carries a logged self-review before merge;
2. all production activity is logged by CloudTrail, with security-relevant events alerted in real time via EventBridge, the breach-detection Lambda and SNS, and the AWS configuration checked monthly by the configuration-check Lambda against a fixed checklist, with the pass/fail record reviewed and recorded in the compliance platform;
3. control execution, evidence, and acknowledgments are recorded with dates in the compliance platform; and
4. the external SOC 2 auditor independently reviews controls and evidence.

Administrative activity is performed only through authenticated sessions that are logged. Control execution is automated where a scheduled Lambda or CI check can perform it (quarterly access reviews, retention enforcement, security scanning, infrastructure provisioning), with the CEO responsible for review and for production deployments.

### 3.4 Procedures

The control environment is governed by the documents below, each owned by the CEO, reviewed annually, and published in the compliance platform. Each document is referenced by its exact title in this description.

**In-scope documents** [CONFIRM: final v2 document inventory and count at publication]

| Document | Type | Subject |
|---|---|---|
| Information Security Policy | Policy | Security principles and control framework for the platform |
| Acceptable Use Policy | Policy | Rules for personnel use of company systems and data |
| Code of Conduct | Policy | Ethical expectations for all personnel |
| Access Control and Authentication Policy | Policy | Provisioning, role-based access control, MFA, session rules, quarterly access reviews |
| Change Management Policy | Policy | Pull-request workflow, CI gate, emergency changes |
| Cloud Infrastructure Security Policy | Policy | AWS configuration and network controls |
| Data Retention and Disposal Policy | Policy | Retention schedule and disposal methods |
| Service Level Agreement (SLA) Management Policy | Policy | 99.9 % availability commitment, maintenance windows, monthly availability record |
| Vendor Management Policy | Policy | Vendor assessment, data processing agreements, annual review |
| Data Classification and Handling Standard | Standard | Four-tier classification and handling rules by tier |
| Encryption and Cryptographic Controls Standard | Standard | Encryption and key management requirements |
| API Security and Rate Limiting Standard | Standard | API authentication, rate limiting, integration security |
| Secure Software Development Lifecycle (SDLC) Standard | Standard | Secure development and CI security checks |
| Incident Response Procedure | Procedure | Detection, containment, eradication, recovery, 48-hour customer notification |
| Risk Assessment Procedure | Procedure | Risk identification, analysis, and treatment |
| System Monitoring and Logging Procedure | Procedure | CloudWatch, CloudTrail, CloudTrail event alerting, monthly configuration checks and log retention |
| Vulnerability Management Procedure | Procedure | Scanning sources and remediation timelines |
| Penetration Testing and Security Assessment Procedure | Procedure | Annual third-party penetration test |
| Data Subject Rights Request Procedure | Procedure | GDPR and CCPA request handling |
| Privacy Notice and Data Processing Agreement Template | Template | GDPR and CCPA obligations and sub-processor list |
| Security Awareness Training Program | Program | Training at onboarding and annually |
| Business Continuity Plan | Plan | Recovery objectives, single-region statement, backup-restore and tabletop tests |

### 3.5 Data

The platform processes three categories of data, all held in known DocumentDB collections and S3 buckets and handled by classification tier under the Data Classification and Handling Standard.

| Category | Data elements | Classification |
|---|---|---|
| Business contact information | First name, last name, business email address, LinkedIn profile URL, job title, current employer, company name, company domain | Confidential |
| Processing data | Competitor interaction tracking, lead qualification status, sourcing date, enrichment metadata, processing timestamps | Confidential |
| Customer data | Account information, API authentication keys, usage metrics, billing details, delivered lead records | Confidential |

**Data flow.** Data enters through PropelAuth-authenticated API endpoints, is processed by Lambda functions and Fargate tasks in private subnets, is stored in DocumentDB encrypted with KMS [CONFIRM: field-level encryption for sensitive attributes, as stated in v1], and is delivered to customers through the API over TLS 1.2 or higher. Business contact information is obtained from authorized business intelligence sources.

**Isolation.** Data is segregated at the company and user level through database partitioning and access control.

**Retention and disposal.** Active leads are retained for 24 months; customer account data for the duration of the customer relationship plus 24 months. Scheduled Lambda functions delete expired records and log each deletion. CloudWatch logs (including API request logs captured in middleware and security event data) are retained for 90 days; CloudTrail logs for 7 years.

---

## 4. System boundaries

The system under examination is the production platform described in Section 3: the infrastructure, software, people, procedures, and data that deliver the service to customers under the Security, Availability, and Confidentiality criteria.

### 4.1 In scope

- **Infrastructure:** every AWS resource in the `di-backend-api-prod` CloudFormation stack in us-east-1 (Section 3.1), as recorded in the compliance platform's asset inventory and network diagram.
- **Data:** all business contact information, processing data, and customer data collected, processed, stored, transmitted, retained, and disposed of by the platform (Section 3.5), including collection through API endpoints, storage in DocumentDB, transmission over TLS, retention under the Data Retention and Disposal Policy, and disposal by cryptographic erasure.
- **People:** the CEO and the Go-to-Market Contractor (Section 3.3), including execution of the controls in the compliance platform's control register, incident response, change management, access reviews, monitoring, vulnerability management, risk assessment, and data subject request handling under GDPR and CCPA.
- **Authentication and access:** PropelAuth as the authentication subservice organization under an executed data processing agreement; the authentication flows between end users and the platform; administrative access to AWS; API authentication for integrations; monitoring of authentication events; provisioning, deprovisioning, and quarterly access certification.
- **Change management:** the `dealintelligence/di-backend-api` repository and its branch protection, the GitHub Actions pipeline, the staging environment used for validation, deployment from a green CI run, rollback by Lambda versioned deployments and `serverless rollback`, CloudFormation via the Serverless Framework, and ECR image scanning. Audit trails are the Git commit history and pull request records.

### 4.2 Out of scope

- The separate staging AWS account, its data, and personal credentials used for it.
- Customer-controlled integrations, including Slack, CRM systems, and other tools configured by customers, and the customer infrastructure that consumes platform data through the API.
- Customer-owned data held in third-party systems integrated through APIs, and personal information unrelated to business activities.
- Customer-managed identity providers integrated through SAML or OAuth, and authentication for customer downstream systems.
- Updates to third-party services outside the organization's control.
- Physical security of home office environments beyond the FileVault full-disk encryption (macOS) requirement of the Acceptable Use Policy; physical datacenter security is the responsibility of AWS.
- Personal devices not used for production access or customer data processing.
- External platforms, such as LinkedIn, from which public business information is sourced.

The subservice organizations AWS and PropelAuth are carved out (Section 5).

---

## 5. Subservice organizations and other vendors

### 5.1 Vendor management approach

The organization engages only the vendors needed to run the platform. Each vendor is classified by service criticality, control requirements, and the availability of an independent attestation report, and is risk-assessed under the Vendor Management Policy. The organization holds data processing agreements with all sub-processors and gives 30 days' advance notice of sub-processor changes.

Vendors with their own SOC 2 report are treated under the carve-out method: their controls are not included in this examination and are covered by their own reports, which the organization obtains and reviews annually, with evidence of review retained in the compliance platform. No vendor is treated under the inclusive method in this examination.

Vendor oversight consists of the annual review of attestation reports and terms, a continuous availability record derived from CloudWatch service availability metrics against the 99.9 % commitment with automated alerting on degradation, and change management for any vendor change. The organization maintains service descriptions, data flow diagrams, and a control responsibility matrix for each vendor, which support the complementary user entity controls in Section 6.

### 5.2 Subservice organizations (carve-out method)

| Vendor | Classification | Services provided | Attestation |
|---|---|---|---|
| Amazon Web Services (AWS) | Infrastructure provider — Risk: Critical | Compute (Lambda, Fargate/ECS), DocumentDB, VPC, KMS, CloudFront, CloudWatch, CloudTrail, ECR, Secrets Manager, S3, SNS, EventBridge, Route 53 (DNS only) | Vendor's own SOC 2 |
| PropelAuth | Critical business service — Risk: Critical | JWT authentication, Google Workspace single sign-on, role-based access control, user management, session management, token generation and validation | Vendor's own SOC 2 |

Both are classified as critical-risk vendors. The data processing agreements with both define control responsibilities and include 30 days' advance notice of sub-processor changes, a right to audit, and incident notification requirements supporting the organization's 48-hour breach notification commitment. Oversight includes annual security assessments recorded in the compliance platform, review of SOC reports and certifications, monitoring of security advisories and incident notifications, tracking of SLA compliance through CloudWatch metrics and PropelAuth's service status, and contingency plans for vendor service disruption in the Business Continuity Plan. Vendor risks are recorded in the risk register.

The organization's controls depend on these vendors at defined points: the quarterly access review Lambda reads PropelAuth user data; CloudWatch alarms consume AWS infrastructure metrics; the breach-detection Lambda is triggered by CloudTrail events delivered through EventBridge.

### 5.3 Complementary subservice organization controls (CSOCs)

The organization's controls are designed on the assumption that the following controls operate at the subservice organizations. This description does not disclose the actual controls at the subservice organizations.

| Subservice organization | Complementary controls expected | Applicable criteria |
|---|---|---|
| AWS | Physical and environmental security of data centers, including 24/7 monitoring, multi-factor authentication for facility access, fire suppression, climate control, and power redundancy; network isolation and DDoS protection (Shield Standard); KMS key management and storage encryption; encryption in transit (TLS 1.2 or higher); Availability Zone redundancy and managed backup infrastructure within us-east-1; monitoring services (CloudWatch, CloudTrail, ECR scanning); controlled change management of AWS services; compliance with SOC 2 and ISO 27001 | CC6.1, CC6.4, CC6.6, CC6.7, CC7.1, CC7.2, CC7.3, CC8.1, A1.1, A1.2, A1.3, C1.1 |
| PropelAuth | Secure JWT token generation and validation; Google Workspace single sign-on (through which multi-factor authentication is inherited from the customer's Google Workspace); rate limiting and account lockout against brute force; secure session handling with timeout policies, token refresh, and protection against session hijacking; encryption of user profile data and authentication logs at rest and in transit; secure disposal of tokens and session data; redundant infrastructure with automatic failover under PropelAuth's own SLA; compliance with privacy regulations under the data processing agreement, supporting GDPR and CCPA obligations | CC6.1, CC6.2, CC6.3, CC6.5, A1.1, C1.2 |

### 5.4 Other vendors (not subservice organizations)

The following vendors support operation of the system but are not subservice organizations under the AICPA Description Criteria: their controls are not necessary, in combination with Deal Intelligence's controls, to achieve the service commitments and system requirements for Security, Availability, and Confidentiality of the production platform. None of them processes customer data; they are vendors under the Vendor Management Policy, not sub-processors, and the customer-facing sub-processor list names AWS and PropelAuth only. Each is subject to annual review of attestation reports and terms.

- **GitHub (source control and continuous integration).** Hosts the `dealintelligence/di-backend-api` repository and runs the GitHub Actions pipeline. Production data never enters the repository or the CI environment; GitHub does not process customer data. The change-management controls that rely on GitHub (branch protection, required status checks, pull request records) are Deal Intelligence's own controls, configured and evidenced by Deal Intelligence, and are tested in this examination. GitHub's own security is covered by its SOC 2 report, reviewed annually.
- **Google Workspace (workforce identity and email).** Provides personnel email and the identity provider for personnel single sign-on, with multi-factor authentication enforced for all personnel accounts. It does not host or process platform customer data. Personnel access control, MFA enforcement, and account provisioning and deprovisioning are Deal Intelligence's own controls, evidenced from the Google Workspace administration console, and are tested in this examination. Google's own security is covered by its SOC 2 report, reviewed annually.
- **Resend (transactional email).** Delivers transactional email (notifications and account messages) on behalf of the platform. Resend receives recipient addresses and message content only at the time of sending; it does not process customer data and does not host platform data, and its availability is not required to deliver the platform's market intelligence services.
- **The compliance platform (self-hosted on AWS, records only).** Holds policies, the control register, evidence, acknowledgments, training records, incident records, and the network diagram. It is self-hosted in Deal Intelligence's AWS environment, holds compliance records only, and does not store, process, or transmit customer data; it is not a vendor-operated service and therefore not a subservice organization. [CONFIRM: that the compliance platform deployment holds no customer data and that its hosting is within the in-scope AWS account.]

HubSpot (CRM) and Slack are used for business operations and operational notifications; they do not process customer data, do not host platform data, and are outside the system boundary (Section 4).

---

## 6. Complementary user entity controls

The platform operates under a shared responsibility model. Deal Intelligence's controls are designed on the assumption that user entities implement the controls below in their own environments. User entities are responsible for determining, in light of their own risk tolerance and regulatory requirements, whether these controls are in place and operating.

### 6.1 Access management (CC6.1, CC6.2, CC6.3, C1.1)

Platform sign-in is through the user entity's Google Workspace single sign-on, and the platform inherits multi-factor authentication from that sign-in. User entities are expected to:

- manage the Google Workspace accounts used to access the platform, including minimum password complexity, regular rotation, and a prohibition on credential sharing;
- enable multi-factor authentication in Google Workspace for every account used to access the platform;
- provision access through a documented approval workflow aligned with job responsibilities;
- review access rights quarterly, adjust them on personnel changes, and revoke access immediately for terminated personnel; and
- assign a unique account to each individual, with shared accounts prohibited except where technically required and compensating controls are in place.

### 6.2 Endpoint security (CC6.8, CC7.1, CC7.2, C1.2)

For all workstations and mobile devices used to access the platform, user entities are expected to:

- deploy enterprise-grade endpoint protection software, with real-time monitoring and automated threat response, on all endpoint devices accessing the platform;
- apply critical security patches within 72 hours of release and routine updates within 30 days;
- enable full-disk encryption using industry-standard algorithms on any device that may cache or store platform data;
- enforce baseline security configurations through centralized management and restrict local administrative privileges to authorized IT personnel; and
- apply application control to prevent unauthorized software, with continuous compliance monitoring and remediation of non-compliant devices.

### 6.3 Network security (CC6.6, CC6.7, CC7.2, A1.2)

User entities are expected to:

- connect to the platform only over TLS 1.2 or higher with certificate validation;
- operate firewalls with explicit allow rules and a default deny policy;
- segment systems that process business intelligence data and monitor inter-zone traffic;
- run intrusion detection and prevention with current signatures and rules for platform traffic;
- apply network security controls for remote access, namely VPN with multi-factor authentication, and retain network logs for monitoring and investigation; and
- use WPA2-Enterprise or WPA3 with 802.1X authentication on any wireless network over which the platform is accessed.

### 6.4 Data governance and handling (C1.1, C1.2)

User entities are expected to:

- classify platform-sourced information as confidential or higher;
- define and enforce retention periods, purging lead data within 24 months unless legal or compliance requirements dictate otherwise;
- deploy data loss prevention configured to detect and block unauthorized transmission of business contact information;
- encrypt any local storage of platform data with AES-256 or equivalent, with key management covering generation, storage, rotation, and recovery; and
- mask or tokenize platform data replicated to non-production environments, and document data lineage through internal systems.

### 6.5 Personnel security (CC1.1, CC1.4, CC1.5, CC2.2)

For personnel with platform access, user entities are expected to:

- conduct background screening (identity verification, employment history, and criminal background checks where permitted by law);
- provide security awareness training covering password security, social engineering, phishing, data handling, and incident reporting within 30 days of hire and annually thereafter;
- execute confidentiality and non-disclosure agreements with all personnel and third parties who may access business intelligence data, with terms that extend beyond the engagement;
- monitor for insider threats, including anomalous platform access or data usage; and
- enforce separation of duties so that no individual both initiates and approves high-risk transactions involving platform data, with defined disciplinary procedures for violations.

### 6.6 Physical and environmental security (CC6.4, CC6.5, A1.2)

At facilities where the platform is accessed or its data is processed, user entities are expected to:

- restrict physical access with card readers, biometrics, or other multi-factor mechanisms, with visitor registration, escort, and temporary badge procedures;
- enforce clean desk and clear screen policies, with regular verification, and secure printed reports and portable media;
- monitor temperature, humidity, water, and smoke conditions affecting systems used to access the platform;
- dispose of platform data securely (cross-cut shredding for paper; NIST-compliant sanitization for electronic media); and
- for remote work, require private work areas, locking storage, and privacy screens.

### 6.7 Change management and incident response (CC7.3, CC7.4, CC7.5, CC8.1, CC9.1, A1.3)

User entities are expected to:

- follow documented change procedures (impact assessment, testing, approval, rollback) for integration configurations, API connections, and data processing workflows;
- maintain separate development, test, and production environments for custom integrations, with security testing before production;
- maintain an incident response plan with classification, escalation, and response protocols for data breaches, system compromise, and service disruption;
- operate 24x7 security monitoring of critical systems with severity-based response times, and retain logs for forensic readiness; and
- report security incidents that may affect platform data to Deal Intelligence within 24 hours of confirmation, and coordinate joint response where required.

---

## 7. Internal controls

The control framework is maintained in the compliance platform, which is the control register (controls, evidence, and tasks). Controls are documented in the policies and procedures listed in Section 3.4 and are organized below by the five COSO components and by control area.

### 7.1 Control environment

- The Information Security Policy, Acceptable Use Policy, and Code of Conduct set the organization's security principles and behavioral expectations. Personnel acknowledge them in the compliance platform portal.
- Quarterly management meetings, minuted and recorded in the compliance platform, review control effectiveness and risk; the minutes are the governance record.
- Roles, reporting lines, and decision rights are documented in role definitions (Section 3.3).
- Security awareness training is completed at onboarding and annually under the Security Awareness Training Program, with completion certificates retained as evidence.
- Control execution is recorded with dates in the compliance platform, and the external SOC 2 auditor independently reviews control design and operating effectiveness.

### 7.2 Risk assessment

- The Risk Assessment Procedure is executed at least annually. It documents objectives and risk tolerance, maintains a risk register (including data breach, unauthorized access, and service availability risks), rates likelihood and impact, and records treatment decisions. Findings are tracked in the compliance platform.
- Change impact assessments are performed as part of the annual risk assessment and whenever a significant change is introduced, covering technology, regulatory, and threat changes.
- Fraud risk is addressed through CloudWatch monitoring and real-time alerting on security-relevant CloudTrail events.
- Business disruption scenarios are identified, mitigated, and tested under the Business Continuity Plan.
- Vendor risk is assessed annually for all sub-processors (CC9.2); PropelAuth and AWS are authorized to handle customer data under data processing agreements. Customer-controlled integrations (Slack, CRM) leave data-sharing decisions with the customer.

### 7.3 Information and communication

- Internal: CloudWatch metrics, alarms, and logs (90-day retention); EventBridge schedules and rules for control Lambda functions (quarterly access reviews, retention enforcement, monthly configuration checks, breach detection on security-relevant CloudTrail events); SNS alerts to the CEO.
- External: customer incident notification within 48 hours and supervisory authority notification within 72 hours where GDPR applies, under the Incident Response Procedure; privacy notices and data processing agreements stating security commitments; 30 days' notice of sub-processor changes; maintenance notices by email 72 hours in advance.
- The compliance platform is the repository for incident records, control documentation, and the audit trail of related communications.

### 7.4 Monitoring activities

Continuous:

- CloudWatch alarms on infrastructure performance, API errors, and latency (p95 greater than 2 seconds);
- the breach-detection Lambda, triggered by an EventBridge rule on security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) and alerting the CEO via SNS in real time;
- ECR scan-on-push on all container images;
- rate limiting (100 requests per minute per API key); and
- PII sanitization in logs.

Periodic:

- the monthly configuration-check Lambda run against the fixed checklist, with the dated pass/fail record posted to and reviewed in the compliance platform;
- quarterly automated access reviews by Lambda; semi-annual privileged-access audits;
- vulnerability assessment under the Vulnerability Management Procedure and an annual third-party penetration test;
- quarterly backup-restore tests and an annual tabletop exercise;
- post-incident retrospectives feeding control improvements; and
- the external SOC 2 auditor's review.

### 7.5 Control activities

**Access control.** PropelAuth JWT authentication with Google Workspace single sign-on (multi-factor authentication inherited from Google Workspace); role-based access control with least privilege; user registration and identity verification before access is granted; VPC isolation with private subnets; quarterly automated access reviews by Lambda; personnel MFA enforced in Google Workspace, GitHub, and AWS; company data accessed only through browser SSO with MFA from personnel devices with FileVault full-disk encryption (macOS).

**Data protection.** KMS encryption of DocumentDB; TLS for all data in transit; [CONFIRM: field-level encryption for sensitive personal information]; data sanitization standards for complete removal of sensitive data; automated disposal by scheduled Lambda under the retention policy.

**Change management.** Pull request on the protected `main` branch with required GitHub Actions checks (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog) and no direct pushes; validation in the staging environment; deployment only from a green CI run; rollback by `serverless rollback`; emergency changes submitted as pull requests labelled `emergency` with post-hoc review within 5 business days; all infrastructure defined in CloudFormation.

**Application security.** Input validation against injection; output encoding against cross-site scripting; automated error detection and data quarantine; security event classification; automated responses including account lockout and suspicious activity quarantine.

**Vulnerability management.** ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI. Remediation targets: 24 hours for exploited or critical vulnerabilities; 7 days for dependency CVEs rated Critical; 30 days High; 90 days Medium; best effort Low.

**Incident response.** Detection, containment, eradication, and recovery under the Incident Response Procedure, with the CEO as incident commander; SNS notification of critical findings; P1 incidents acknowledged within 4 business hours; incident evidence retained for 7 years; customer notification within 48 hours; root cause analysis driving control improvements.

**Business continuity.** DocumentDB storage replicated across three Availability Zones with automatic instance recovery; backups retained 35 days with point-in-time recovery; quarterly backup-restore tests; Lambda reserved concurrency and versioned deployments with rollback; AWS physical and environmental controls (Section 5.3), supporting the 99.9 % availability commitment.

**Privacy (GDPR and CCPA).** Four-tier classification with handling rules; documented lawful bases for processing; data subject requests handled by manual runbook (verify identity; locate records in DocumentDB, PropelAuth, and the CRM; act; record a dated entry in the compliance platform); 24-month lead retention with automated purge; records of processing.

---

## 8. System incidents

[CONFIRM: no significant incidents in the period] During the period [CONFIRM: period start] to [CONFIRM: period end], Deal Intelligence LLC identified no system incidents that (a) were the result of controls that were not suitably designed or operating effectively, or (b) otherwise resulted in a significant failure in the achievement of one or more of the service commitments and system requirements for Security, Availability, or Confidentiality, that would require disclosure in this description.

[If an incident is to be disclosed, replace the paragraph above with, for each incident: the nature of the incident, the timing of the incident, the extent (or nature) of its effect on the system and on the achievement of service commitments and system requirements, and the remediation taken.]

---

## 9. Changes to the system during the period

[CONFIRM: significant changes to the system during the period, if any] During the period [CONFIRM: period start] to [CONFIRM: period end], Deal Intelligence LLC made no changes to the system that were significant to the achievement of its service commitments and system requirements for Security, Availability, or Confidentiality.

[If changes are to be disclosed, replace the paragraph above with, for each change: the nature of the change, when it took effect, and its effect on the system, the controls, or the service commitments and system requirements. Changes adopted since the SOC 2 Type I report (as of March 2, 2026) — including the pull-request workflow with required CI checks, the staging environment, 35-day backup retention, 7-year CloudTrail retention, ECR scan-on-push, and secrets rotation — should be listed here if they took effect within the period.]

---

## Appendix — Management's assertion

Deal Intelligence LLC's management (hereinafter "management") has prepared the accompanying description of Deal Intelligence LLC's B2B market intelligence platform (the "system") titled "Description of Deal Intelligence LLC's B2B Market Intelligence Platform" throughout the period [CONFIRM: period start] to [CONFIRM: period end] (the "description") based on the criteria for a description of a service organization's system in DC section 200, *2018 Description Criteria for a Description of a Service Organization's System in a SOC 2 Report* (with revised implementation guidance for 2022) (the "description criteria"). The description is intended to provide report users with information about the system that may be useful when assessing the risks arising from interactions with the system, particularly information about system controls that management has designed, implemented, and operated to provide reasonable assurance that its service commitments and system requirements were achieved based on the trust services criteria relevant to Security, Availability, and Confidentiality (the "applicable trust services criteria") set forth in TSP section 100, *2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy* (with revised points of focus, 2022).

Deal Intelligence LLC uses Amazon Web Services (AWS) to provide cloud infrastructure hosting and PropelAuth to provide authentication services (the "subservice organizations"). The description indicates that complementary subservice organization controls that are suitably designed and operating effectively are necessary, along with controls at Deal Intelligence LLC, to achieve Deal Intelligence LLC's service commitments and system requirements based on the applicable trust services criteria. The description presents Deal Intelligence LLC's controls, the applicable trust services criteria, and the types of complementary subservice organization controls assumed in the design of Deal Intelligence LLC's controls. The description does not disclose the actual controls at the subservice organizations.

The description also indicates that complementary user entity controls that are suitably designed and operating effectively are necessary, along with controls at Deal Intelligence LLC, to achieve Deal Intelligence LLC's service commitments and system requirements based on the applicable trust services criteria. The description presents Deal Intelligence LLC's controls, the applicable trust services criteria, and the complementary user entity controls assumed in the design of Deal Intelligence LLC's controls.

We confirm, to the best of our knowledge and belief, that:

a. the description presents Deal Intelligence LLC's B2B market intelligence platform that was designed and implemented throughout the period [CONFIRM: period start] to [CONFIRM: period end] in accordance with the description criteria;

b. the controls stated in the description were suitably designed throughout the period [CONFIRM: period start] to [CONFIRM: period end] to provide reasonable assurance that Deal Intelligence LLC's service commitments and system requirements would be achieved based on the applicable trust services criteria, if its controls operated effectively throughout that period, and if the subservice organizations and user entities applied the complementary controls assumed in the design of Deal Intelligence LLC's controls throughout that period; and

c. the controls stated in the description operated effectively throughout the period [CONFIRM: period start] to [CONFIRM: period end] to provide reasonable assurance that Deal Intelligence LLC's service commitments and system requirements were achieved based on the applicable trust services criteria, if complementary subservice organization controls and complementary user entity controls assumed in the design of Deal Intelligence LLC's controls operated effectively throughout that period.

[CONFIRM: name, title, date]
Deal Intelligence LLC

---

## Revision history

| Version | Date | Summary |
|---|---|---|
| 1.0 | November 23, 2025 | Draft system description generated in the prior compliance tool; basis of the SOC 2 Type I report (as of March 2, 2026). |
| 2.0 | <to be set at publication> | Scope narrowed to Security, Availability, and Confidentiality; claims aligned to the target environment (PR workflow, staging environment, 35-day backups, 7-year CloudTrail, ECR scan-on-push, secrets rotation); unevidenced numbers and controls removed; roles stated with compensating controls for segregation of duties; other vendors, system incidents, changes in the period, network diagram reference, and management's assertion added; restructured to the DC 200 order with duplicated architecture text removed; wording hygiene per RULEBOOK R0–R8; decisions of 2026-10-31 applied (KMS key-separation target design, FileVault endpoint encryption, availability measured monthly over all minutes excluding announced maintenance, other vendors stated as not processing customer data). |
