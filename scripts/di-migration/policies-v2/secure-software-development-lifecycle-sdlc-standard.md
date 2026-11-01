---
title: "Secure Software Development Lifecycle (SDLC) Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "secure-software-development-lifecycle-sdlc-standard-v1.0.pdf"
---

# Secure Software Development Lifecycle (SDLC) Standard

## 1. Purpose

This Secure Software Development Lifecycle (SDLC) Standard establishes the framework for integrating security controls throughout all phases of software development at Deal Intelligence LLC. This standard ensures that security is embedded into the design, development, testing, and deployment of our platform in accordance with SOC 2 Trust Service Criteria for Security (CC3.4) and Confidentiality (C1.1).

This standard operationalizes the security principles defined in the Information Security Policy and works in conjunction with the Change Management Policy to ensure that all software changes are developed, tested, and deployed securely while maintaining the integrity of business contact information and market intelligence data.

## 2. Scope

This standard applies to:

- All software development activities for the Deal Intelligence platform, including:

   - AWS Lambda functions (900s timeout, reserved concurrency: 100)

   - Fargate container applications for batch processing

   - API development (di-backend-api-prod)

   - Frontend applications served via CloudFront CDN

   - Infrastructure as Code (CloudFormation templates deployed via the Serverless Framework)

- All development environments (development, the staging stage, production)

- GitHub repositories (`dealintelligence/di-backend-api`) and GitHub Actions CI/CD pipelines

- Third-party libraries and dependencies

- All personnel involved in software development, testing, and deployment activities

- Integration points with PropelAuth authentication services

## 3. Policy Statement

Deal Intelligence shall implement security-by-design principles throughout the software development lifecycle, incorporating automated security testing, code review requirements, and vulnerability management processes. All code shall undergo security validation before deployment to production, with particular emphasis on protecting business contact information, preventing unauthorized data access, and maintaining the 99.9% uptime SLA commitment.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer

**Mo Messidi** - As Chief Executive Officer, responsible for:

- Establishing secure coding standards and guidelines

- Approving architectural security designs

- Reviewing and approving production deployment decisions

- Ensuring compliance with SOC 2 development requirements

- Conducting security code reviews, recorded as a logged self-review in the pull request

- Managing vulnerability remediation priorities per the Vulnerability Management Procedure

- Coordinating security testing activities

- Maintaining the secure coding guidelines

- Reviewing dependency security alerts from GitHub Dependabot

- Implementing secure coding practices

- Reviewing code changes via GitHub pull requests on the protected `main` branch with required CI status checks

- Managing branch protection rules and merge requirements

- Ensuring automated testing coverage

- Coordinating with the Penetration Testing and Security Assessment Procedure

### 4.2 External Parties

- **External SOC 2 auditor**: provides independent review of SDLC controls and change evidence

- **Penetration-test vendor**: conducts the annual third-party penetration test per the Penetration Testing and Security Assessment Procedure

## 5. SDLC Security Requirements

### 5.1 Planning and Design Phase

#### 5.1.1 Security Requirements Analysis

- Security requirements shall be documented for all new features affecting:

   - Business contact data processing

   - Authentication and authorization flows

   - API endpoints handling customer data

   - Integration with third-party services

- Threat modeling shall be conducted for significant architectural changes

- Data flow diagrams shall identify all data classification levels per the Data Classification and Handling Standard

#### 5.1.2 Architecture Security Review

All architectural designs shall incorporate:

- Defense-in-depth security controls

- Principle of least privilege access

- Data encryption requirements per the Encryption and Cryptographic Controls Standard

- API security controls per the API Security and Rate Limiting Standard

### 5.2 Development Phase

#### 5.2.1 Secure Coding Standards

The following secure coding practices shall be enforced:

|**Language/Framework**|**Security Requirements**|**Validation Method**|
|---|---|---|
|Node.js/TypeScript|Input validation, parameterized queries, JWT validation|[CONFIRM: ESLint security rules — not in the GitHub Actions CI set]|
|Python (Lambda)|Input sanitization, boto3 secure defaults, secrets management|Black, isort, Flake8 and Bandit in GitHub Actions|
|Infrastructure (CloudFormation)|Least privilege IAM, encrypted storage, VPC isolation|CloudFormation (`serverless deploy`) as the only change path; Security Hub configuration checks|
|Container (Docker)|Non-root users, minimal base images, no secrets in images|ECR scan-on-push; Trivy in GitHub Actions|

#### 5.2.2 Code Review Requirements

- All code changes shall be merged through a pull request on the protected `main` branch; direct pushes to `main` are not permitted

- The author shall record a self-review in the pull request before merging

- Security-sensitive changes shall be identified in the pull request description and are subject to independent review by the external SOC 2 auditor

- Automated security checks via pre-commit hooks must pass

- Branch protection rules enforce:

   - Required status checks (GitHub Actions: Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog)

   - Require up-to-date branches before merging

#### 5.2.3 Dependency Management

- Dependencies shall be tracked in package.json/requirements.txt

- GitHub Dependabot alerts shall be reviewed weekly

- Dependency CVEs rated critical shall be remediated within 7 days; critical vulnerabilities that are actively exploited shall be remediated within 24 hours

- High severity vulnerabilities shall be remediated within 30 days

- Medium severity vulnerabilities shall be remediated within 90 days

- Dependency updates shall follow the Change Management Policy

### 5.3 Testing Phase

#### 5.3.1 Security Testing Requirements

|**Test Type**|**Frequency**|**Tools/Methods**|**Success Criteria**|
|---|---|---|---|
|Static Application Security Testing (SAST)|Every commit|Bandit and TruffleHog in GitHub Actions|No critical findings|
|Dependency Scanning|Continuous|GitHub Dependabot and code scanning|No critical vulnerabilities|
|Container Scanning|On build|ECR scan-on-push; Trivy in GitHub Actions|No critical CVEs|
|Penetration Testing|Annual|Third-party assessment per Penetration Testing Procedure|Remediation plan for findings|

#### 5.3.2 Test Data Management

- Production data shall not be used in development or testing environments

- Test data shall be anonymized or synthetic

- Test environments shall implement access controls per the Access Control and Authentication Policy

### 5.4 Deployment Phase

#### 5.4.1 Deployment Security Controls

- All deployments shall follow the approved Change Management Policy

- Production deployments require:

   - Successful completion of all security tests

   - Deployment only from a green CI run on `main`, approved via the GitHub Actions workflow

   - Deployment to the staging stage first

   - Automated rollback procedures documented

- Infrastructure changes shall use Infrastructure as Code (CloudFormation via the Serverless Framework)

- Secrets shall be managed via AWS Secrets Manager/Parameter Store

#### 5.4.2 Release Security Checklist

Pre-deployment verification:

- [ ] Security testing completed and passed

- [ ] Pull request merged with required CI status checks passing and self-review recorded

- [ ] No critical or high vulnerabilities in dependencies

- [ ] API rate limiting configured per API Security Standard

- [ ] Logging and monitoring configured per System Monitoring and Logging Procedure

- [ ] Encryption enabled for data at rest and in transit

- [ ] Access controls implemented and tested

### 5.5 Maintenance Phase

#### 5.5.1 Security Patch Management

- Security patches shall be evaluated and applied according to severity:

   - Critical (exploited or critical-rated): Within 24 hours

   - Critical dependency CVEs: Within 7 days

   - High: Within 30 days

   - Medium: Within 90 days

   - Low: Best effort

- Emergency patches follow the expedited process in the Incident Response Procedure

#### 5.5.2 Continuous Security Monitoring

- CloudWatch and Security Hub findings shall be reviewed monthly and the review recorded; critical findings alert in real time via SNS

- Container vulnerability scans shall be reviewed weekly

- Security metrics shall be tracked:

   - Time to remediate vulnerabilities

   - Number of security findings by severity

   - Code coverage for security tests

   - Failed deployment due to security issues

## 6. Security Tools and Automation

### 6.1 Integrated Security Toolchain

|**Tool/Service**|**Purpose**|**Integration Point**|
|---|---|---|
|GitHub Actions|CI/CD security scanning (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog)|Every commit/PR|
|GitHub Dependabot|Dependency vulnerability alerts|Continuous scans|
|AWS Security Hub|Centralized security findings|Continuous monitoring|
|ECR Image Scanning|Container vulnerability detection|On image push|
|CloudFormation (Serverless Framework)|Infrastructure as code; only change path, reports drift|Deployment|
|Pre-commit hooks|Local security checks|Before commit|
|AWS CloudTrail|Audit logging|All API calls|

### 6.2 Automated Security Controls

The following automated controls are implemented:

- Pre-commit hooks for secret detection and linting

- GitHub Actions workflows for SAST and dependency checking

- Automated Lambda functions for security monitoring per System Monitoring and Logging Procedure

- The breach-detection Lambda that routes Security Hub findings to SNS

- SNS notifications for critical security events

## 7. Secure Development Training

All personnel with development access shall complete:

- Security awareness training in the compliance platform portal at onboarding and annually per the Security Awareness Training Program

- OWASP Top 10 awareness training

- AWS security best practices training

- Incident response procedures familiarization

## 8. Third-Party Code and Libraries

### 8.1 Open Source Usage

- All open source components shall be documented

- License compliance shall be verified

- Security vulnerabilities shall be tracked via GitHub security advisories

- Components with known critical vulnerabilities shall not be used

### 8.2 Third-Party Integration Security

- Integration with PropelAuth shall follow the Integration security section of the API Security and Rate Limiting Standard

- API integrations shall implement authentication and rate limiting

- Data shared with third parties shall be classified and protected accordingly

## 9. Compliance and Monitoring

### 9.1 Compliance Verification

- Quarterly reviews of SDLC security controls effectiveness

- Annual assessment against SOC 2 CC3.4 requirements

- Monthly vulnerability metrics review

- Weekly Dependabot alert review

### 9.2 Key Performance Indicators

|**Metric**|**Target**|**Measurement Frequency**|
|---|---|---|
|Critical vulnerabilities open > 24 hours|0|Weekly|
|High vulnerabilities open > 30 days|< 5|Weekly|
|Failed deployments due to security|< 10%|Monthly|
|Pull requests merged with passing CI status checks|100%|Per deployment|

### 9.3 Continuous Improvement

- Post-incident reviews shall identify SDLC improvements per the Incident Response Procedure

- Annual penetration test findings shall drive security enhancements

- Security metrics shall be reviewed quarterly for trend analysis

- Industry best practices shall be evaluated for adoption

## 10. Exceptions and Deviations

Any exceptions to this standard must be:

- Documented with business justification

- Risk assessed per the Risk Assessment Procedure

- Approved by the Chief Executive Officer

- Reviewed quarterly for continued necessity

- Tracked in the compliance platform

## 11. Related Documents

- Information Security Policy

- Change Management Policy

- Vulnerability Management Procedure

- API Security and Rate Limiting Standard

- Encryption and Cryptographic Controls Standard

- Access Control and Authentication Policy

- Cloud Infrastructure Security Policy

- System Monitoring and Logging Procedure

- Incident Response Procedure

- Penetration Testing and Security Assessment Procedure

- Risk Assessment Procedure

- Data Classification and Handling Standard

- Security Awareness Training Program

## 12. Review and Updates

This standard shall be reviewed annually and updated to reflect:

- Changes in development technologies and practices

- Emerging security threats and vulnerabilities

- Lessons learned from security incidents

- Updates to SOC 2 requirements

- Findings from penetration tests and security assessments

## 13. Revision History

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|2.0|<to be set at publication>|Scope limited to Security, Availability and Confidentiality; roles consolidated to CEO with PR/CI compensating controls; CI toolchain and remediation timelines aligned; dynamic-testing and coverage-percentage claims removed; integration-security reference redirected to the API Security and Rate Limiting Standard|
