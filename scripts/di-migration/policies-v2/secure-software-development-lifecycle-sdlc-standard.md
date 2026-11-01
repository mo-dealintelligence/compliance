---
title: "Secure Software Development Lifecycle (SDLC) Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "secure-software-development-lifecycle-sdlc-standard-v1.0.pdf"
---

# Secure Software Development Lifecycle (SDLC) Standard

## 1. Purpose

This standard sets the security controls applied in every phase of software development at Deal Intelligence LLC: design, development, testing, deployment, and maintenance. It supports the SOC 2 Trust Services Criteria for Security (CC3.4) and Confidentiality (C1.1).

It implements the security principles of the Information Security Policy and works with the Change Management Policy so that all software changes are developed, tested, and deployed securely, protecting business contact information and market intelligence data.

Deal Intelligence applies security-by-design throughout the development lifecycle through automated security testing, code review requirements, and vulnerability management. All code passes security validation before deployment to production, with particular attention to protecting business contact information, preventing unauthorized data access, and maintaining the 99.9 % uptime SLA.

## 2. Scope

This standard applies to:

- All software development for the Deal Intelligence platform, including:
   - Lambda functions (900 s timeout, reserved concurrency: 100)
   - Fargate container applications for batch processing
   - API development (`di-backend-api-prod`)
   - Frontend applications served via CloudFront
   - Infrastructure as Code (CloudFormation templates deployed via the Serverless Framework)
- All development environments (development, the staging AWS account, production)
- GitHub repositories (`dealintelligence/di-backend-api`) and GitHub Actions CI/CD pipelines
- Third-party libraries and dependencies
- All personnel involved in software development, testing, and deployment
- Integration points with PropelAuth authentication

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

The CEO:

- Sets and maintains the secure coding standards and guidelines
- Approves architectural security designs
- Reviews and approves production deployment decisions
- Maintains compliance with the SOC 2 development requirements
- Conducts security code reviews, recorded as a logged self-review in the pull request
- Reviews code changes via GitHub pull requests on the protected `main` branch with required CI status checks
- Manages branch protection rules and merge requirements
- Maintains automated test coverage
- Reviews dependency security alerts from GitHub Dependabot
- Manages vulnerability remediation priorities per the Vulnerability Management Procedure
- Coordinates security testing, including the annual penetration test under the Penetration Testing and Security Assessment Procedure

### 3.2 External parties

- **External SOC 2 auditor**: independently reviews the SDLC controls and change evidence
- **Penetration-test vendor**: conducts the annual third-party penetration test per the Penetration Testing and Security Assessment Procedure

## 4. SDLC security requirements

### 4.1 Planning and design

#### 4.1.1 Security requirements analysis

- Security requirements are documented for every new feature affecting:
   - Business contact data processing
   - Authentication and authorization flows
   - API endpoints handling customer data
   - Integration with third-party services
- Threat modeling is conducted for significant architectural changes
- Data flow diagrams identify all data classification tiers per the Data Classification and Handling Standard

#### 4.1.2 Architecture security review

All architectural designs incorporate:

- Defense-in-depth security controls
- Least-privilege access
- Data encryption per the Encryption and Cryptographic Controls Standard
- API security controls per the API Security and Rate Limiting Standard

### 4.2 Development

#### 4.2.1 Secure coding standards

|**Language/framework**|**Security requirements**|**Validation method**|
|---|---|---|
|Node.js/TypeScript|Input validation, parameterized queries, JWT validation|[CONFIRM: ESLint security rules — not in the GitHub Actions CI set]|
|Python (Lambda)|Input sanitization, boto3 secure defaults, secrets management|Black, isort, Flake8, and Bandit in GitHub Actions|
|Infrastructure (CloudFormation)|Least-privilege IAM, encrypted storage, VPC isolation|CloudFormation (`serverless deploy`) as the only change path; monthly configuration-check Lambda|
|Container (Docker)|Non-root users, minimal base images, no secrets in images|ECR scan-on-push; Trivy in GitHub Actions|

#### 4.2.2 Code review

- All code changes are merged through a pull request on the protected `main` branch; direct pushes to `main` are not permitted
- The author records a self-review in the pull request before merging
- Security-sensitive changes are identified in the pull request description and are subject to independent review by the external SOC 2 auditor
- Automated security checks in pre-commit hooks must pass
- Branch protection rules enforce:
   - Required status checks (GitHub Actions: Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog)
   - Up-to-date branches before merging

#### 4.2.3 Dependency management

- Dependencies are tracked in `package.json` and `requirements.txt`
- GitHub Dependabot alerts are reviewed by the CEO
- Dependency CVEs rated critical are remediated within 7 days; critical vulnerabilities that are actively exploited are remediated within 24 hours
- High-severity vulnerabilities are remediated within 30 days
- Medium-severity vulnerabilities are remediated within 90 days
- Dependency updates follow the Change Management Policy

### 4.3 Testing

#### 4.3.1 Security testing

|**Test type**|**Frequency**|**Tools/methods**|**Success criteria**|
|---|---|---|---|
|Static application security testing (SAST)|Every commit|Bandit and TruffleHog in GitHub Actions|No critical findings|
|Dependency scanning|Continuous|GitHub Dependabot and code scanning|No critical vulnerabilities|
|Container scanning|On build|ECR scan-on-push; Trivy in GitHub Actions|No critical CVEs|
|Penetration testing|Annual|Third-party assessment per the Penetration Testing and Security Assessment Procedure|Remediation plan for findings|

#### 4.3.2 Test data

- Production data is not used in development or testing environments
- Test data is anonymized or synthetic
- Test environments implement the access controls in the Access Control and Authentication Policy

### 4.4 Deployment

#### 4.4.1 Deployment controls

- All deployments follow the Change Management Policy
- Production deployments require:
   - Successful completion of all security tests
   - Deployment only from a green CI run on `main`, approved via the GitHub Actions workflow
   - Deployment to the staging environment first
   - Documented automated rollback procedures
- Infrastructure changes use Infrastructure as Code (CloudFormation via the Serverless Framework)
- Secrets are managed in Secrets Manager or Parameter Store

#### 4.4.2 Release security checklist

Before deployment:

- [ ] Security testing completed and passed
- [ ] Pull request merged with required CI status checks passing and self-review recorded
- [ ] No critical or high vulnerabilities in dependencies
- [ ] API rate limiting configured per the API Security and Rate Limiting Standard
- [ ] Logging and monitoring configured per the System Monitoring and Logging Procedure
- [ ] Encryption enabled for data at rest and in transit
- [ ] Access controls implemented and tested

### 4.5 Maintenance

#### 4.5.1 Security patch management

- Security patches are evaluated and applied by severity:
   - Critical (exploited or critical-rated): within 24 hours
   - Critical dependency CVEs: within 7 days
   - High: within 30 days
   - Medium: within 90 days
   - Low: best effort
- Emergency patches follow the expedited process in the Incident Response Procedure

#### 4.5.2 Continuous security monitoring

- CloudWatch metrics and the monthly configuration-check record are reviewed monthly and the review recorded in the compliance platform; security-relevant CloudTrail events alert the CEO in real time via EventBridge, the breach-detection Lambda and SNS
- Security metrics tracked:
   - Time to remediate vulnerabilities
   - Number of security findings by severity
   - Code coverage for security tests
   - Failed deployments due to security issues

## 5. Security tools and automation

### 5.1 Security toolchain

|**Tool/service**|**Purpose**|**Integration point**|
|---|---|---|
|GitHub Actions|CI/CD security scanning (Black, isort, Flake8, Bandit, pytest, Trivy, TruffleHog)|Every commit/PR|
|GitHub Dependabot|Dependency vulnerability alerts|Continuous scans|
|Configuration-check Lambda|Monthly AWS configuration checks against a fixed checklist, with a dated pass/fail record in the compliance platform|Monthly schedule|
|ECR image scanning|Container vulnerability detection|On image push|
|CloudFormation (Serverless Framework)|Infrastructure as Code; only change path, reports drift|Deployment|
|Pre-commit hooks|Local security checks|Before commit|
|CloudTrail|Audit logging|All API calls|

### 5.2 Automated security controls

- Pre-commit hooks for secret detection and linting
- GitHub Actions workflows for SAST and dependency checking
- Scheduled Lambda functions for security monitoring per the System Monitoring and Logging Procedure
- The breach-detection Lambda function, triggered by an EventBridge rule on security-relevant CloudTrail events, that sends SNS alerts to the CEO
- SNS notifications for critical security events

## 6. Secure development training

All personnel with development access complete:

- Security awareness training in the compliance platform portal at onboarding and annually, per the Security Awareness Training Program
- OWASP Top 10 awareness training
- AWS security best practices training
- Incident response procedure familiarization

## 7. Third-party code and libraries

### 7.1 Open source usage

- All open source components are documented
- License compliance is verified
- Security vulnerabilities are tracked via GitHub security advisories
- Components with known critical vulnerabilities are not used

### 7.2 Third-party integration security

- The PropelAuth integration follows the Integration security section of the API Security and Rate Limiting Standard
- API integrations implement authentication and rate limiting
- Data shared with third parties is classified and protected per its tier

## 8. Compliance and monitoring

### 8.1 Key performance indicators

|**Metric**|**Target**|**Measurement frequency**|
|---|---|---|
|Pull requests merged with passing CI status checks|100 %|Per deployment|

### 8.2 Continuous improvement

- Post-incident reviews identify SDLC improvements per the Incident Response Procedure
- Annual penetration test findings drive security enhancements
- Industry best practices are evaluated for adoption

## 9. Exceptions and review

### 9.1 Exceptions

An exception to this standard is:

- Documented with its business justification
- Risk-assessed per the Risk Assessment Procedure
- Approved by the CEO
- Tracked in the compliance platform

### 9.2 Review

The CEO reviews this standard annually and updates it for:

- Changes in development technologies and practices
- Emerging security threats and vulnerabilities
- Lessons learned from security incidents
- Updates to SOC 2 requirements
- Findings from penetration tests and security assessments

## 10. Related documents

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

## 11. Revision history

|**Version**|**Date**|**Summary**|
|---|---|---|
|1.0|November 13, 2025|Initial release|
|2.0|<to be set at publication>|Scope limited to Security, Availability and Confidentiality; roles consolidated to CEO with PR/CI compensating controls; CI toolchain and remediation timelines aligned; dynamic-testing and coverage-percentage claims removed; integration-security reference redirected to the API Security and Rate Limiting Standard|
