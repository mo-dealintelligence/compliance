---
title: "Change Management Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "change-management-policy-v1.0.pdf"
---

# Change Management Policy

## 1. Purpose

This policy governs how Deal Intelligence LLC plans, approves, implements, and reviews changes to its production systems and infrastructure. Changes to the platform are executed in a controlled way that minimizes risk, maintains service availability, and preserves the integrity of customer data processing.

The policy implements the change control requirements of the Information Security Policy and supports the 99.9 % uptime SLA. It addresses SOC 2 Trust Services Criteria CC8.1 (the entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures), CC7.1 (the entity uses detection and monitoring procedures), and A1.2 (the entity authorizes, designs, develops or acquires, implements, operates, approves, maintains, and monitors environmental protections).

## 2. Scope

This policy applies to all changes affecting:

- Production AWS infrastructure components documented in the CloudFormation stack di-backend-api-prod
- Lambda functions, Fargate containers, and ECS services
- DocumentDB configurations and data schemas
- API endpoints and CloudFront distributions
- Security configurations, including IAM roles, VPC settings, and KMS keys
- PropelAuth authentication configurations
- CI/CD pipeline configurations in GitHub Actions
- Production data structures and processing logic
- Integration configurations with customer systems

Excluded from this policy:

- Development and testing environment changes (unless they affect production)
- Documentation updates that do not affect system functionality
- Read-only database queries for reporting

## 3. Definitions

**Change**: Any addition, modification, or removal of hardware, software, infrastructure, or configuration that could affect the production environment or service delivery.

**Standard change**: A pre-approved, low-risk change that follows a documented procedure and has a predictable outcome (for example, a routine security patch or a Lambda function timeout adjustment within the approved range).

**Normal change**: A change that requires review and approval through the pull-request review process before implementation.

**Emergency change**: A high-priority change required to restore service or address a critical security vulnerability, implemented through a pull request labelled `emergency` with post-hoc review within 5 business days.

**Pull-request review**: The change review and approval mechanism for all production changes: a pull request against the protected `main` branch of the `dealintelligence/di-backend-api` repository, with required GitHub Actions CI status checks (lint, tests, Bandit, Trivy, TruffleHog), a logged self-review in the pull request, and merge by the Chief Executive Officer (CEO) as final approver. Direct pushes to `main` are not permitted.

**Change window**: A pre-scheduled maintenance period communicated to customers, during off-peak hours (07:00–11:00 UTC / 02:00–06:00 ET).

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

The CEO owns this policy and is the only role with production access. The CEO:

- Serves as final approver for all production changes and merges all normal and emergency change pull requests
- Confirms that changes align with business objectives and compliance requirements
- Authorizes exceptions to standard change procedures when necessary
- Reviews post-implementation reports for all changes
- Prepares change requests with technical specifications
- Conducts impact assessments and risk analysis
- Implements approved changes following the documented procedures
- Performs rollback procedures when necessary
- Documents change outcomes and lessons learned
- Confirms that changes maintain SOC 2 compliance
- Reviews changes for security and privacy implications
- Updates compliance documentation affected by changes
- Monitors change management metrics for audit purposes

### 4.2 Go-to-Market Contractor

The Go-to-Market Contractor holds no production access and does not initiate, approve, or implement changes under this policy.

### 4.3 External SOC 2 auditor

The external SOC 2 auditor provides independent review of the change records (pull requests, CI runs, CloudTrail logs) retained under this policy.

## 5. Change management process

### 5.1 Change request initiation

Every change starts with a change request that includes:

- Description of the proposed change
- Business justification and expected benefits
- Technical specifications and implementation details
- Risk assessment using the Risk Assessment Procedure
- Impact analysis on systems, services, and customers
- Rollback plan and success criteria
- Testing requirements and validation procedures
- Proposed implementation schedule

Change requests are documented in GitHub Issues with the "change-request" label and tracked through the associated pull request and the CI/CD pipeline.

### 5.2 Change categories and approval requirements

#### 5.2.1 Standard changes

Pre-approved changes of the following types:

- Automated dependency updates proposed by GitHub Dependabot that pass all required CI status checks
- Lambda function configuration updates within defined parameters
- CloudWatch alarm threshold adjustments

Approval: pre-authorized, logged for audit purposes.

#### 5.2.2 Normal changes

- Infrastructure modifications via CloudFormation
- Database schema changes
- API endpoint additions or modifications
- Security group rule changes
- Third-party integration updates

Approval: pull-request review; all required CI status checks must pass before merge to `main`.

#### 5.2.3 Emergency changes

- Critical security vulnerability patches
- Service restoration changes
- Data breach containment measures

Approval: pull request labelled `emergency`; post-hoc review within 5 business days.

### 5.3 Change assessment and planning

Before approval, all normal and emergency changes undergo:

#### 5.3.1 Technical review

- Logged self-review in the GitHub pull request
- Automated security scanning via GitHub Actions (Bandit, Trivy, TruffleHog)
- Dependency vulnerability assessment
- Performance impact analysis

#### 5.3.2 Security review

- Compliance with the Cloud Infrastructure Security Policy
- Data protection impact per the Data Classification and Handling Standard
- Authentication and access control validation

#### 5.3.3 Business impact assessment

- Customer notification requirements
- SLA impact analysis per the Service Level Agreement (SLA) Management Policy
- Integration dependency mapping
- Rollback time estimation

### 5.4 Change implementation

#### 5.4.1 Pre-implementation

- Customer notification for maintenance windows (minimum 72 hours for planned changes)
- Backup verification per the Business Continuity Plan
- Validation in the staging environment in a separate AWS account (no production data; scrubbed or synthetic data only)
- Implementation checklist review

#### 5.4.2 Implementation

- Procedures followed as documented in this policy and in the pull request
- Real-time monitoring via CloudWatch dashboards
- Communication updates to affected stakeholders
- Deployment from a green CI run using Lambda versioned deployments, with rollback via `serverless rollback`

#### 5.4.3 Validation

- Automated smoke tests via GitHub Actions
- Manual verification of critical functionality
- Performance metrics validation
- Security control verification

### 5.5 Post-implementation review

Within 5 business days of implementation, the CEO:

- Documents actual versus planned outcomes
- Updates the configuration management database
- Reviews any incidents or unexpected behavior
- Updates procedures as needed
- Archives the change documentation for audit purposes

## 6. Emergency change procedures

Emergency changes follow an expedited process while maintaining control.

### 6.1 Immediate response

- The CEO opens a pull request labelled `emergency` against the protected `main` branch; required CI status checks still apply
- Implementation proceeds with continuous monitoring
- The incident is documented in the compliance platform's Incident Reporting system

### 6.2 Documentation requirements

- Change request completed within 24 hours
- Post-hoc review recorded in the pull request within 5 business days
- Root cause analysis per the Incident Response Procedure

### 6.3 Follow-up actions

- Permanent fix planned if temporary measures were implemented
- Process improvement recommendations recorded
- Customer communication per the breach notification requirements

## 7. Change management tools and automation

### 7.1 Technical controls

- GitHub Actions for CI/CD pipeline automation
- Branch protection on `main` requiring a pull request and required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes
- Pre-commit hooks for security and quality checks
- CloudFormation (`serverless deploy`) as the only infrastructure change path, with drift reporting
- The monthly configuration-check Lambda, which verifies the fixed infrastructure checklist after changes and posts a dated pass/fail record to the compliance platform; security-relevant CloudTrail events (IAM policy or user changes, security-group changes, among others) alert the CEO in real time via EventBridge, the breach-detection Lambda, and SNS

### 7.2 Documentation and tracking

- GitHub Issues for change request management
- Pull request descriptions for change documentation
- CloudTrail for AWS infrastructure change audit logs
- The compliance platform for compliance reporting and metrics

## 8. Metrics and reporting

Change management metrics, drawn from GitHub and CloudTrail records, include:

- Total changes by category (standard, normal, emergency)
- Change success rate (successful changes / total changes)
- Emergency change percentage
- Average implementation time by category
- Rollback frequency and root causes
- Compliance with change windows
- Customer-impacting incidents caused by changes

The CEO reviews the metrics at the quarterly management meeting.

## 9. Audit trail

All changes maintain a complete audit trail, including:

- Change request documentation
- Approval records and timestamps
- Implementation logs and test results
- Git commit history and pull request records
- CloudTrail logs for infrastructure changes
- Post-implementation review documentation

## 10. Training and awareness

The CEO maintains current knowledge of:

- AWS best practices for change management
- Security implications of infrastructure changes
- Compliance requirements for change control
- Industry standards and emerging threats

Training is documented per the Security Awareness Training Program.

## 11. Related documents

- Information Security Policy
- Business Continuity Plan
- Cloud Infrastructure Security Policy
- Data Classification and Handling Standard
- Incident Response Procedure
- Risk Assessment Procedure
- Secure Software Development Lifecycle (SDLC) Standard
- Security Awareness Training Program
- Service Level Agreement (SLA) Management Policy
- Vulnerability Management Procedure

## 12. Policy review and updates

This policy is reviewed annually or on significant changes to:

- The AWS infrastructure architecture
- Regulatory requirements
- Business operations or service offerings
- The security threat landscape

## 13. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Change review restated as pull-request review with required CI status checks on protected `main`; emergency changes via `emergency`-labelled PR with 5-business-day post-hoc review; roles consolidated to CEO; deployment and compliance-monitoring tooling aligned to the operated environment |
