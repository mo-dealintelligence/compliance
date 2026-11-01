---
title: "Cloud Infrastructure Security Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "cloud-infrastructure-security-policy-v1.0.pdf"
---

# Cloud Infrastructure Security Policy

## 1. Purpose

This policy sets the security requirements and controls for the AWS infrastructure that runs the Deal Intelligence LLC platform. It protects the availability, integrity, and confidentiality of cloud resources, meets the SOC 2 Trust Services Criteria, and supports the 99.9 % uptime commitment in the Service Level Agreement (SLA) Management Policy.

It complements the Information Security Policy with the technical controls and operating procedures specific to cloud infrastructure.

## 2. Scope

This policy applies to:

- All AWS infrastructure components, including Lambda functions, Fargate containers, DocumentDB clusters, and associated services
- The CloudFormation stack `di-backend-api-prod` and all resources it manages
- Virtual Private Cloud (VPC) configuration and network security controls
- Container images, registries, and orchestration services (ECR, ECS)
- Content delivery and edge services (CloudFront)
- Infrastructure automation and deployment pipelines
- All personnel with administrative or operational access to cloud infrastructure

It covers the infrastructure-specific implementation of the Trust Services Criteria selected by Deal Intelligence: Security, Availability, and Confidentiality.

## 3. Definitions

- **Cloud infrastructure**: all AWS services, resources, and configurations that support the Deal Intelligence platform
- **Infrastructure as Code (IaC)**: CloudFormation templates and configuration files that define and provision cloud resources programmatically
- **Container image**: packaged application code and dependencies stored in ECR
- **Security group**: a virtual firewall controlling inbound and outbound traffic at the resource level
- **Network Access Control List (NACL)**: an optional layer of subnet-level traffic control
- **KMS**: AWS Key Management Service, used for encryption key management and cryptographic operations
- **Multi-AZ deployment**: distribution of resources across multiple availability zones for high availability

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

The CEO owns this policy and is the only role with administrative access to the cloud infrastructure. The CEO:

- Configures and maintains AWS resources according to security best practices
- Implements and maintains the CloudFormation templates that provision the infrastructure
- Monitors infrastructure performance and security metrics
- Maintains the encryption and access controls required by this policy
- Maintains infrastructure documentation and configuration baselines
- Configures the configuration-check Lambda, the CloudTrail-EventBridge alerting rule, and related security services
- Reviews and responds to infrastructure security findings
- Manages IAM policies and service roles
- Conducts infrastructure security assessments
- Maintains the CI/CD pipelines for infrastructure deployments
- Implements infrastructure monitoring and alerting
- Manages container registries and orchestration services
- Executes backup and recovery procedures
- Leads incident response for infrastructure events

### 4.2 Go-to-Market Contractor

- Has no access to cloud infrastructure, production systems, or deployment pipelines
- Reports any suspected infrastructure security issue to the CEO

### 4.3 External parties

- The external SOC 2 auditor independently reviews infrastructure controls and evidence
- The penetration-test vendor performs the annual third-party penetration test

## 5. Controls

### 5.1 Infrastructure architecture and design

#### 5.1.1 Network segmentation

All cloud infrastructure is deployed in a single VPC in us-east-1 with:

- Private subnets for the database and application tiers
- Public subnets only for the NAT instance, which is accessed exclusively via SSM Session Manager (no key-based shell access, no public services)
- Network segmentation enforcing least-privilege access between tiers
- VPC Flow Logs enabled for network traffic analysis

#### 5.1.2 High availability design

The infrastructure is deployed across the us-east-1a and us-east-1b availability zones to support the 99.9 % uptime SLA in the Service Level Agreement (SLA) Management Policy:

- DocumentDB clusters are Multi-AZ (a second instance in another availability zone) with automatic failover
- Lambda functions run across multiple availability zones
- Lambda deployments are versioned, with reserved concurrency and rollback via `serverless rollback`
- CloudFront distributes content globally

The platform runs in a single AWS region (us-east-1) by design, as stated in the Business Continuity Plan.

#### 5.1.3 Encryption

All infrastructure components implement the encryption controls in the Encryption and Cryptographic Controls Standard:

- KMS customer-managed keys for DocumentDB encryption
- TLS 1.2 minimum for all data in transit
- S3 bucket encryption for stored objects
- Certificate management through ACM

### 5.2 Access control and identity management

#### 5.2.1 IAM policy management

IAM is configured according to the Access Control and Authentication Policy:

- Least privilege for all IAM roles and policies
- Service-specific roles for Lambda functions and containers
- No use of the root account for daily operations
- MFA required for console access to production resources
- Quarterly access reviews recorded in the risk register in the compliance platform

#### 5.2.2 Service account management

- A unique IAM role for each service component
- Temporary credentials via AWS STS for cross-service authentication
- No hard-coded credentials in application code or configuration files
- Secrets held in Secrets Manager or Parameter Store, with Secrets Manager rotation enabled on the DocumentDB credential

#### 5.2.3 Database access controls

DocumentDB access is restricted through:

- VPC isolation with no direct internet connectivity
- Security group rules limiting access to authorized application services
- Database user authentication with strong passwords
- Connection encryption enforced at the database level

### 5.3 Container security

#### 5.3.1 Container image management

Container images are managed according to the Secure Software Development Lifecycle (SDLC) Standard:

- Scan-on-push vulnerability scanning enabled in ECR for all repositories
- Critical vulnerabilities remediated before production deployment
- Base images from trusted sources only
- Regular updates of base images and dependencies
- Images built and pushed to ECR only from a green GitHub Actions CI run (including Trivy image scanning)

#### 5.3.2 Container runtime security

ECS and Fargate deployments implement:

- Task-level IAM roles with the minimum required permissions
- Read-only root filesystems where the workload allows it
- Resource limits to prevent container escape
- Network policies restricting inter-container communication
- Logging of container activity to CloudWatch

### 5.4 Serverless security

#### 5.4.1 Lambda function security

Lambda functions are configured with:

- Function-specific IAM execution roles
- Reserved concurrency limits (100 concurrent executions)
- A maximum timeout of 900 seconds to prevent runaway functions
- Environment variable encryption for sensitive configuration
- VPC attachment for functions that need database access
- Versioned deployments with rollback via `serverless rollback`

#### 5.4.2 API security

API endpoints implement the controls in the API Security and Rate Limiting Standard:

- Rate limiting of 100 requests per minute per client, enforced in middleware
- JWT authentication via PropelAuth
- Request validation and input sanitization
- CloudWatch logging of all API calls
- CloudFront with AWS Shield Standard, TLS 1.2+, and origin access restricted to the Lambda function URLs

### 5.5 Infrastructure monitoring and logging

#### 5.5.1 Logging

Infrastructure logging follows the System Monitoring and Logging Procedure:

- CloudTrail enabled for all AWS API calls
- CloudWatch Logs for application and system logs
- CloudWatch Logs retained 90 days
- CloudTrail logs retained 7 years in S3 (lifecycle to Glacier, Object Lock)
- Log aggregation and centralized analysis
- PII sanitization in all logged data

#### 5.5.2 Security monitoring

Security monitoring runs through:

- A scheduled configuration-check Lambda that runs monthly against a fixed checklist (CloudTrail enabled and log-file validation on; no public S3 buckets; no security groups open to 0.0.0.0/0 on administrative ports; root account MFA; IAM password policy; KMS key rotation; ECR scan-on-push; DocumentDB backup retention and Multi-AZ) and posts a dated pass/fail record to the compliance platform
- CloudTrail for AWS API activity; security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- Scheduled Lambda checks (access review, retention enforcement)
- CloudWatch alarms for security events
- Security events recorded in the incident reporting module of the compliance platform

#### 5.5.3 Performance monitoring

Infrastructure performance metrics include:

- Lambda function duration and error rates
- Container CPU and memory utilization
- Database connection pool metrics
- API latency (alert at p95 > 2 seconds) and error rates
- CloudFront cache hit ratios

### 5.6 Backup and recovery

#### 5.6.1 Backups

Backups follow the Business Continuity Plan:

- Daily automated DocumentDB backups with 90-day retention
- Point-in-time recovery for databases
- Infrastructure configuration versioning in CloudFormation
- Container image versioning in ECR
- Lambda function version management

#### 5.6.2 Recovery

- Recovery time objectives (RTO) and recovery point objectives (RPO) are set in the Business Continuity Plan
- Quarterly backup restoration test (automated, recorded in the compliance platform)
- Automatic failover for Multi-AZ resources
- Rollback procedures for infrastructure changes
- Disaster recovery procedures in the Business Continuity Plan

### 5.7 Change management

#### 5.7.1 Infrastructure changes

All infrastructure changes follow the Change Management Policy:

- CloudFormation templates (deployed via the Serverless Framework) provision the infrastructure
- All IaC templates are version-controlled in the `dealintelligence/di-backend-api` repository
- Changes are validated in a staging environment deployed from the same CloudFormation templates into a separate AWS account, containing no production data, before production
- Production deployments require a pull request with required CI status checks on the protected `main` branch and deploy only from a green CI run
- Rollback via `serverless rollback`

#### 5.7.2 Configuration management

- Baseline configurations are documented for all infrastructure components
- CloudFormation (`serverless deploy`) is the only change path and reports configuration drift
- The monthly configuration-check Lambda and the other scheduled Lambda checks detect non-compliant resources
- Configurations are reviewed and updated regularly

### 5.8 Vulnerability management

Infrastructure vulnerability management follows the Vulnerability Management Procedure:

- Regular security assessments of the cloud infrastructure
- Automated vulnerability scanning through ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI
- Patch management for managed services
- Prioritization of security findings by severity
- Remediation tracked in the compliance platform

### 5.9 Third-party services

AWS, as the infrastructure provider, is managed according to the Vendor Management Policy:

- Annual review of AWS security certifications and compliance
- Monitoring of the AWS service health dashboard
- Review of AWS security bulletins and advisories
- Participation in AWS Well-Architected reviews

### 5.10 GDPR and CCPA support

The infrastructure supports GDPR and CCPA compliance through:

- Data residency controls and geographic restrictions
- Encryption of personal data at rest and in transit
- Audit logging of data access and modification
- Support for the deletion and retention requirements in the Data Retention and Disposal Policy

## 6. Enforcement

### 6.1 Implementation

- Immediate enforcement for all new infrastructure deployments
- Review and remediation of existing infrastructure within 30 days
- Monthly configuration-check record in the compliance platform
- Annual third-party penetration test

### 6.2 Policy violations

Non-compliance with this policy may result in:

- Immediate remediation requirements
- Restricted access to production infrastructure
- An incident record in the incident reporting module of the compliance platform
- Escalation to the CEO for repeated violations

### 6.3 Exceptions

A policy exception is:

- Documented with its business justification
- Approved by the CEO
- Time-limited, with a remediation plan
- Tracked in the risk register in the compliance platform

### 6.4 Review

The CEO reviews this policy annually and updates it for:

- Changes in AWS services and best practices
- Changes in the Deal Intelligence infrastructure architecture
- Updates to compliance requirements and industry standards
- Lessons learned from security incidents and assessments
- Recommendations from penetration tests and security assessments

The next review date is recorded in the compliance platform and aligned with the annual review cycle of the related security policies.

## 7. Related documents

- Information Security Policy
- Access Control and Authentication Policy
- Change Management Policy
- Incident Response Procedure
- Business Continuity Plan
- Data Classification and Handling Standard
- Encryption and Cryptographic Controls Standard
- System Monitoring and Logging Procedure
- Vulnerability Management Procedure
- API Security and Rate Limiting Standard
- Secure Software Development Lifecycle (SDLC) Standard
- Vendor Management Policy
- Service Level Agreement (SLA) Management Policy
- Data Retention and Disposal Policy

## 8. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Roles reduced to CEO / Go-to-Market Contractor; SOC 2 scope set to Security, Availability, Confidentiality; perimeter, threat-detection, configuration-compliance, instance, image-integrity and deployment claims replaced by the controls in place (CloudFront + Shield Standard, monthly configuration-check Lambda + CloudTrail-EventBridge breach-detection alerting, CloudFormation drift reporting, ECR scan-on-push, Lambda versioned deployments); log retention split (CloudWatch 90 days, CloudTrail 7 years); single-region statement added |
