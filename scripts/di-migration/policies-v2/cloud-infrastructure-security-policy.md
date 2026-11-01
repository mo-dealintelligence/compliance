---
title: "Cloud Infrastructure Security Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "cloud-infrastructure-security-policy-v1.0.pdf"
---

# Cloud Infrastructure Security Policy

## 1. Purpose

This Cloud Infrastructure Security Policy establishes comprehensive security requirements and controls for Deal Intelligence LLC's AWS cloud infrastructure supporting the platform. This policy ensures the protection, availability, and integrity of cloud resources while maintaining compliance with SOC 2 Trust Services Criteria and supporting the organization's 99.9% uptime SLA commitment.

This policy complements the Information Security Policy by providing specific technical controls and operational procedures for cloud infrastructure management, working in conjunction with established security frameworks to protect business contact information and maintain service reliability.

## 2. Scope

This policy applies to:

- All AWS cloud infrastructure components including Lambda functions, Fargate containers, DocumentDB clusters, and associated services

- CloudFormation stack di-backend-api-prod and all managed resources

- Virtual Private Cloud (VPC) configurations and network security controls

- Container images, registries, and orchestration services (ECR, ECS)

- Content delivery networks and edge services (CloudFront)

- Infrastructure automation and deployment pipelines

- All personnel with administrative or operational access to cloud infrastructure

This policy encompasses infrastructure-specific implementations of the Trust Services Criteria selected by Deal Intelligence: Security, Availability and Confidentiality.

## 3. Definitions

**Cloud Infrastructure** : All AWS services, resources, and configurations that support Deal Intelligence's platform operations.

**Infrastructure as Code (IaC)** : CloudFormation templates and configuration files that define and provision cloud resources programmatically.

**Container Image** : Packaged application code and dependencies stored in Amazon Elastic Container Registry (ECR).

**Security Group** : Virtual firewall controlling inbound and outbound traffic at the instance level.

**Network Access Control List (NACL)** : Optional layer of security providing subnet-level traffic control.

**AWS KMS** : AWS Key Management Service used for encryption key management and cryptographic operations.

**Multi-AZ Deployment** : Distribution of resources across multiple availability zones for high availability.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer (CEO)

The CEO owns this policy and is the only role with administrative access to the cloud infrastructure. The CEO shall:

- Configure and maintain AWS cloud resources according to security best practices

- Implement and manage CloudFormation templates for infrastructure provisioning

- Monitor infrastructure performance and security metrics

- Ensure compliance with encryption and access control requirements

- Maintain infrastructure documentation and configuration baselines

- Configure AWS Security Hub and related security services

- Review and respond to infrastructure security findings

- Manage IAM policies and service roles

- Conduct infrastructure security assessments

- Maintain CI/CD pipelines for infrastructure deployments

- Implement infrastructure monitoring and alerting

- Manage container registries and orchestration services

- Execute backup and recovery procedures

- Lead incident response activities for infrastructure events

### 4.2 Go-to-Market Contractor

- Has no access to cloud infrastructure, production systems, or deployment pipelines

- Reports any suspected infrastructure security issue to the CEO

### 4.3 External Parties

- The external SOC 2 auditor independently reviews infrastructure controls and evidence

- The penetration-test vendor performs the annual third-party penetration test

## 5. Policy Statements

### 5.1 Infrastructure Architecture and Design

#### 5.1.1 Network Segmentation

All cloud infrastructure shall be deployed within a single Virtual Private Cloud (VPC) in us-east-1 with:

- Private subnets for database and application tiers

- Public subnets only for the NAT instance, which is accessed exclusively via SSM Session Manager (no key-based shell access, no public services)

- Network segmentation enforcing least privilege access between tiers

- VPC Flow Logs enabled for network traffic analysis

#### 5.1.2 High Availability Design

Infrastructure shall maintain multi-availability zone deployment across us-east-1a and us-east-1b to support the 99.9% uptime SLA as detailed in the Service Level Agreement (SLA) Management Policy:

- DocumentDB clusters deployed Multi-AZ (a second instance in another availability zone) with automated failover capabilities

- Lambda functions deployed across multiple availability zones

- Lambda versioned deployments with reserved concurrency and rollback via `serverless rollback`

- CloudFront CDN for global content distribution

The platform operates in a single AWS region (us-east-1) by design, as stated in the Business Continuity Plan.

#### 5.1.3 Encryption Requirements

All infrastructure components shall implement encryption controls as specified in the Encryption and Cryptographic Controls Standard:

- AWS KMS customer-managed keys for DocumentDB encryption

- TLS 1.2 minimum for all data in transit

- S3 bucket encryption for stored objects

- Certificate management through AWS Certificate Manager

### 5.2 Access Control and Identity Management

#### 5.2.1 IAM Policy Management

AWS Identity and Access Management (IAM) shall be configured according to the Access Control and Authentication Policy:

- Principle of least privilege for all IAM roles and policies

- Service-specific roles for Lambda functions and containers

- No use of root account for daily operations

- MFA required for console access to production resources

- Quarterly access reviews documented in the risk register in the compliance platform

#### 5.2.2 Service Account Management

- Unique IAM roles for each service component

- Temporary credentials via AWS STS for cross-service authentication

- No hard-coded credentials in application code or configuration files

- Secrets management through AWS Secrets Manager or Parameter Store, with Secrets Manager rotation enabled on the DocumentDB credential

#### 5.2.3 Database Access Controls

DocumentDB access shall be restricted through:

- VPC isolation with no direct internet connectivity

- Security group rules limiting access to authorized application services

- Database user authentication with strong passwords

- Connection encryption enforced at the database level

- Audit logging for all database operations

### 5.3 Container Security

#### 5.3.1 Container Image Management

All container images shall be managed according to secure development practices outlined in the Secure Software Development Lifecycle (SDLC) Standard:

- Scan-on-push vulnerability scanning enabled in Amazon ECR for all repositories

- Critical vulnerabilities remediated before production deployment

- Base images from trusted sources only

- Regular updates of base images and dependencies

- Images built and pushed to ECR only from a green GitHub Actions CI run (including Trivy image scanning)

#### 5.3.2 Container Runtime Security

ECS and Fargate deployments shall implement:

- Task-level IAM roles with minimal required permissions

- Read-only root filesystems where applicable

- Resource limits to prevent container escape

- Network policies restricting inter-container communication

- Logging of container activities to CloudWatch

### 5.4 Serverless Security

#### 5.4.1 Lambda Function Security

Lambda functions shall be configured with:

- Function-specific IAM execution roles

- Reserved concurrency limits (100 concurrent executions)

- Maximum timeout of 900 seconds to prevent runaway functions

- Environment variable encryption for sensitive configuration

- VPC attachment for functions requiring database access

- Versioned deployments with rollback via `serverless rollback`

#### 5.4.2 API Gateway Security

API endpoints shall implement controls defined in the API Security and Rate Limiting Standard:

- Rate limiting of 100 requests per minute per client, enforced in middleware

- JWT authentication via PropelAuth integration

- Request validation and input sanitization

- CloudWatch logging for all API calls

- CloudFront with AWS Shield Standard, TLS 1.2+, and origin access restricted to the Lambda function URLs

### 5.5 Infrastructure Monitoring and Logging

#### 5.5.1 Logging Requirements

Infrastructure logging shall comply with the System Monitoring and Logging Procedure:

- CloudTrail enabled for all AWS API calls

- CloudWatch Logs for application and system logs

- 90-day retention period for CloudWatch Logs

- CloudTrail logs retained 7 years in S3 (lifecycle to Glacier, Object Lock)

- Log aggregation and centralized analysis

- PII sanitization in all logged data

#### 5.5.2 Security Monitoring

Continuous security monitoring through:

- AWS Security Hub (AWS Foundational Security Best Practices) for centralized security findings, including configuration checks

- CloudTrail for AWS API activity

- The breach-detection Lambda function that routes Security Hub findings to SNS

- Scheduled Lambda checks (access review, retention enforcement)

- CloudWatch alarms for security events

- SNS notifications for critical findings in real time; all Security Hub findings reviewed monthly and the review recorded in the compliance platform

- Integration with the Incident Reporting system in the compliance platform for security events

#### 5.5.3 Performance Monitoring

Infrastructure performance metrics including:

- Lambda function duration and error rates

- Container CPU and memory utilization

- Database connection pool metrics

- API latency (alert at p95 > 2 seconds) and error rates

- CloudFront cache hit ratios

### 5.6 Backup and Recovery

#### 5.6.1 Backup Requirements

Infrastructure backup procedures shall align with the Business Continuity Plan:

- Daily automated DocumentDB backups with 90-day retention

- Point-in-time recovery capability for databases

- Infrastructure configuration versioning in CloudFormation

- Container image versioning in ECR

- Lambda function version management

#### 5.6.2 Recovery Procedures

- Documented recovery time objectives (RTO) and recovery point objectives (RPO)

- Quarterly backup restoration testing (automated, recorded in the compliance platform)

- Automated failover for Multi-AZ resources

- Rollback procedures for infrastructure changes

- Disaster recovery procedures documented in the Business Continuity Plan

### 5.7 Change Management

#### 5.7.1 Infrastructure Changes

All infrastructure modifications shall follow the Change Management Policy:

- CloudFormation templates (deployed via the Serverless Framework) for infrastructure provisioning

- Version control for all IaC templates in the `dealintelligence/di-backend-api` repository

- Validation in a staging stage of the same CloudFormation stack, containing no production data, before production

- Pull request with required CI status checks on the protected `main` branch for production deployments; deploy only from a green CI run

- Rollback via `serverless rollback`

#### 5.7.2 Configuration Management

- Baseline configurations documented for all infrastructure components

- CloudFormation (`serverless deploy`) is the only change path and reports configuration drift

- Security Hub configuration checks and scheduled Lambda checks for non-compliant resources

- Regular configuration reviews and updates

### 5.8 Vulnerability Management

Infrastructure vulnerability management shall follow the Vulnerability Management Procedure:

- Regular security assessments of cloud infrastructure

- Automated vulnerability scanning through ECR scan-on-push, GitHub Dependabot and code scanning, and Trivy in CI

- Patch management for managed services

- Security finding prioritization based on severity

- Remediation tracking through Security Hub

### 5.9 Third-Party Services

AWS as the primary infrastructure provider shall be managed according to the Vendor Management Policy:

- Annual review of AWS security certifications and compliance

- Monitoring of AWS service health dashboards

- Review of AWS security bulletins and advisories

- Participation in AWS Well-Architected reviews

## 6. Compliance Requirements

### 6.1 SOC 2 Requirements

Infrastructure controls shall address all applicable Trust Services Criteria:

- **Security** : Implementation of technical controls for infrastructure protection

- **Availability** : Multi-AZ deployment and automated failover mechanisms

- **Confidentiality** : Encryption and access controls for sensitive data

### 6.2 Regulatory Compliance

Infrastructure shall support GDPR and CCPA compliance through:

- Data residency controls and geographic restrictions

- Encryption of personal data at rest and in transit

- Audit logging for data access and modifications

- Support for data deletion and retention requirements defined in the Data Retention and Disposal Policy

## 7. Implementation and Enforcement

### 7.1 Implementation Timeline

- Immediate enforcement for all new infrastructure deployments

- Existing infrastructure review and remediation within 30 days

- Monthly review of Security Hub findings, recorded in the compliance platform

- Annual third-party penetration test

### 7.2 Policy Violations

Non-compliance with this policy may result in:

- Immediate remediation requirements

- Restricted access to production infrastructure

- Incident documentation in the Incident Reporting system in the compliance platform

- Escalation to the CEO for repeated violations

### 7.3 Exceptions

Policy exceptions must be:

- Documented with business justification

- Approved by the CEO

- Time-limited with defined remediation plans

- Tracked in the risk register in the compliance platform

## 8. Related Documents

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

## 9. Review and Updates

This policy shall be reviewed annually and updated to reflect:

- Changes in AWS service offerings and best practices

- Evolution of Deal Intelligence's infrastructure architecture

- Updates to compliance requirements and industry standards

- Lessons learned from security incidents and assessments

- Recommendations from penetration testing and security assessments

The next scheduled review date shall be recorded in the compliance platform and coordinated with the annual review cycle of related security policies.

## 10. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Roles reduced to CEO / Go-to-Market Contractor; SOC 2 scope set to Security, Availability, Confidentiality; perimeter, threat-detection, configuration-compliance, instance, image-integrity and deployment claims replaced by the controls in place (CloudFront + Shield Standard, Security Hub + breach-detection Lambda, CloudFormation drift reporting, ECR scan-on-push, Lambda versioned deployments); log retention split (CloudWatch 90 days, CloudTrail 7 years); single-region statement added |
