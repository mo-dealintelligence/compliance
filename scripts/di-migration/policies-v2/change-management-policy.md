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

This Change Management Policy establishes the formal framework for planning, approving, implementing, and reviewing all changes to Deal Intelligence LLC's production systems and infrastructure. The policy ensures that modifications to the platform are executed in a controlled manner that minimizes risk, maintains service availability, and preserves the integrity of customer data processing operations.

This policy operationalizes the change control requirements defined in the Information Security Policy and directly supports SOC 2 Trust Services Criteria CC8.1 (Change Management) while maintaining our 99.9% uptime SLA.

## 2. Scope

This policy applies to all changes affecting:

- Production AWS infrastructure components documented in CloudFormation stack di-backend-api-prod

- Lambda functions, Fargate containers, and ECS services

- DocumentDB configurations and data schemas

- API endpoints and CloudFront distributions

- Security configurations including IAM roles, VPC settings, and KMS keys

- PropelAuth authentication configurations

- CI/CD pipeline configurations in GitHub Actions

- Production data structures and processing logic

- Integration configurations with customer systems

Excluded from this policy:

- Development and testing environment changes (unless impacting production)

- Documentation updates not affecting system functionality

- Read-only database queries for reporting purposes

## 3. Definitions

**Change** : Any addition, modification, or removal of hardware, software, infrastructure, or configuration that could impact the production environment or service delivery.

**Standard Change** : Pre-approved, low-risk changes that follow documented procedures and have predictable outcomes (e.g., routine security patches, Lambda function timeout adjustments within approved ranges).

**Normal Change** : Changes requiring review and approval through the pull-request review process before implementation.

**Emergency Change** : High-priority changes required to restore service or address critical security vulnerabilities, implemented through a pull request labelled `emergency` with post-hoc review within 5 business days.

**Pull-Request Review** : The change review and approval mechanism for all production changes: a pull request against the protected `main` branch of the `dealintelligence/di-backend-api` repository, with required GitHub Actions CI status checks (lint, tests, Bandit, Trivy, TruffleHog), a logged self-review in the pull request, and merge by the Chief Executive Officer as final approver. Direct pushes to `main` are not permitted.

**Change Window** : Pre-scheduled maintenance periods communicated to customers, typically scheduled during off-peak hours (2:00 AM - 6:00 AM EST).

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer

The CEO owns this policy and is the only role with production access. The CEO:

- Serves as final approver for all production changes and merges all normal and emergency change pull requests

- Ensures changes align with business objectives and compliance requirements

- Authorizes exceptions to standard change procedures when necessary

- Reviews post-implementation reports for all changes

- Prepares change requests with technical specifications

- Conducts impact assessments and risk analysis

- Implements approved changes following documented procedures

- Performs rollback procedures when necessary

- Documents change outcomes and lessons learned

- Ensures changes maintain SOC 2 compliance requirements

- Reviews changes for security and privacy implications

- Updates compliance documentation affected by changes

- Monitors change management metrics for audit purposes

### 4.2 Go-to-Market Contractor

- Holds no production access and does not initiate, approve or implement changes under this policy

### 4.3 External SOC 2 Auditor

- Provides independent review of the change records (pull requests, CI runs, CloudTrail logs) retained under this policy

## 5. Change Management Process

### 5.1 Change Request Initiation

All changes must be initiated through a formal change request that includes:

- Description of the proposed change

- Business justification and expected benefits

- Technical specifications and implementation details

- Risk assessment using the Risk Assessment Procedure

- Impact analysis on systems, services, and customers

- Rollback plan and success criteria

- Testing requirements and validation procedures

- Proposed implementation schedule

Change requests are documented in GitHub Issues with the "change-request" label and tracked through the associated pull request and the CI/CD pipeline.

### 5.2 Change Categories and Approval Requirements

#### Standard Changes

- Pre-approved changes of the types listed below

- Automated dependency updates proposed by GitHub Dependabot that pass all required CI status checks

- Lambda function configuration updates within defined parameters

- CloudWatch alarm threshold adjustments

- Approval: Pre-authorized, logged for audit purposes

#### Normal Changes

- Infrastructure modifications via CloudFormation

- Database schema changes

- API endpoint additions or modifications

- Security group rule changes

- Third-party integration updates

- Approval: Pull-request review required; all required CI status checks must pass before merge to `main`

#### Emergency Changes

- Critical security vulnerability patches

- Service restoration changes

- Data breach containment measures

- Approval: Pull request labelled `emergency`; post-hoc review within 5 business days

### 5.3 Change Assessment and Planning

Before approval, all normal and emergency changes undergo:

#### 1. Technical Review

- Logged self-review in the GitHub pull request

- Automated security scanning via GitHub Actions (Bandit, Trivy, TruffleHog)

- Dependency vulnerability assessment

- Performance impact analysis

#### 2. Security Review

- Compliance with Cloud Infrastructure Security Policy

- Data protection impact per Data Classification and Handling Standard

- Authentication and access control validation

#### 3. Business Impact Assessment

- Customer notification requirements

- SLA impact analysis per Service Level Agreement (SLA) Management Policy

- Integration dependency mapping

- Rollback time estimation

### 5.4 Change Implementation

All approved changes follow these implementation requirements:

#### 1. Pre-Implementation

- Customer notification for maintenance windows (minimum 72 hours for planned changes)

- Backup verification per Business Continuity Plan

- Validation in the staging stage of the CloudFormation stack (no production data; scrubbed or synthetic data only)

- Implementation checklist review

#### 2. Implementation

- Follow the procedures documented in this policy and in the pull request

- Real-time monitoring via CloudWatch dashboards

- Communication updates to affected stakeholders

- Deployment from a green CI run using Lambda versioned deployments, with rollback via `serverless rollback`

#### 3. Validation

- Automated smoke tests via GitHub Actions

- Manual verification of critical functionality

- Performance metrics validation

- Security control verification

### 5.5 Post-Implementation Review

Within 5 business days of implementation:

- Document actual vs. planned outcomes

- Update configuration management database

- Review any incidents or unexpected behaviors

- Update procedures as needed

- Archive change documentation for audit purposes

## 6. Emergency Change Procedures

Emergency changes follow an expedited process while maintaining control:

#### 1. Immediate Response

- CEO opens a pull request labelled `emergency` against the protected `main` branch; required CI status checks still apply

- Implementation proceeds with continuous monitoring

- Incident documented in the compliance platform's Incident Reporting system

#### 2. Documentation Requirements

- Complete change request within 24 hours

- Post-hoc review recorded in the pull request within 5 business days

- Root cause analysis per Incident Response Procedure

#### 3. Follow-up Actions

- Permanent fix planning if temporary measures implemented

- Process improvement recommendations

- Customer communication per breach notification requirements

## 7. Change Management Tools and Automation

### 7.1 Technical Controls

- GitHub Actions for CI/CD pipeline automation

- Branch protection on `main` requiring a pull request and required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes

- Pre-commit hooks for security and quality checks

- CloudFormation (`serverless deploy`) as the only infrastructure change path, with drift reporting

- Security Hub configuration checks for compliance monitoring

### 7.2 Documentation and Tracking

- GitHub Issues for change request management

- Pull request descriptions for change documentation

- CloudTrail for AWS infrastructure change audit logs

- The compliance platform for compliance reporting and metrics

## 8. Metrics and Reporting

Monthly change management metrics tracked include:

- Total changes by category (standard, normal, emergency)

- Change success rate (successful/total changes)

- Emergency change percentage

- Average implementation time by category

- Rollback frequency and root causes

- Compliance with change windows

- Customer-impacting incidents from changes

Reports are reviewed monthly by CEO and included in quarterly compliance reviews.

## 9. Compliance and Audit

### 9.1 SOC 2 Requirements

This policy addresses the following SOC 2 criteria:

- CC8.1: The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures

- CC7.1: To meet its objectives, the entity uses detection and monitoring procedures

- A1.2: The entity authorizes, designs, develops or acquires, implements, operates, approves, maintains, and monitors environmental protections

### 9.2 Audit Trail Requirements

All changes maintain complete audit trails including:

- Change request documentation

- Approval records and timestamps

- Implementation logs and test results

- Git commit history and pull request records

- CloudTrail logs for infrastructure changes

- Post-implementation review documentation

## 10. Training and Awareness

The CEO maintains current knowledge of:

- AWS best practices for change management

- Security implications of infrastructure changes

- Compliance requirements for change control

- Industry standards and emerging threats

Training is documented in the Security Awareness Training Program.

## 11. Related Documents

- Information Security Policy

- Incident Response Procedure

- Business Continuity Plan

- Risk Assessment Procedure

- Secure Software Development Lifecycle (SDLC) Standard

- Cloud Infrastructure Security Policy

- Vulnerability Management Procedure

## 12. Policy Review and Updates

This policy is reviewed annually or upon significant changes to:

- AWS infrastructure architecture

- Regulatory requirements

- Business operations or service offerings

- Security threat landscape

## 13. Revision History

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Change review restated as pull-request review with required CI status checks on protected `main`; emergency changes via `emergency`-labelled PR with 5-business-day post-hoc review; roles consolidated to CEO; deployment and compliance-monitoring tooling aligned to the operated environment |
