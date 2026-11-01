---
title: "API Security and Rate Limiting Standard"
doc_type: "Standard"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "api-security-and-rate-limiting-standard-v1.0.pdf"
---

# API Security and Rate Limiting Standard

## 1. Purpose

This API Security and Rate Limiting Standard establishes mandatory requirements for securing application programming interfaces (APIs) and implementing rate limiting controls across Deal Intelligence LLC's B2B market intelligence platform. This standard ensures the protection of business contact information and customer data transmitted through APIs while maintaining service availability in accordance with SOC 2 Trust Service Criteria CC6.1 (Logical and Physical Access Controls) and A1.2 (Availability).

This standard operationalizes the API security requirements defined in the Information Security Policy and complements the Cloud Infrastructure Security Policy by providing specific implementation guidance for API endpoints, authentication mechanisms, traffic management controls, and the security of third-party integrations (section 8).

## 2. Scope

This standard applies to:

- All REST APIs exposed through AWS API Gateway and CloudFront distributions
- Internal service-to-service communications within VPC boundaries
- Third-party API integrations including PropelAuth authentication services
- Lambda function endpoints with 900-second timeout configurations
- Customer-controlled integrations with CRM systems and Slack workspaces
- Webhook endpoints and event-driven integrations via EventBridge
- OAuth 2.0 and JWT-based authentication flows
- All personnel responsible for API development, deployment, and maintenance

## 3. API Security Requirements

### 3.1 Authentication and Authorization

All API endpoints shall implement multi-layered authentication controls:

**JWT Token Validation**

- PropelAuth JWT tokens required for all authenticated endpoints
- Token expiration set to maximum 24 hours with refresh token rotation
- RS256 algorithm for token signing with 2048-bit RSA keys
- Token validation performed at API Gateway level before Lambda invocation

**Authorization Controls**

- Role-based access control (RBAC) enforced per Access Control and Authentication Policy
- Company-level data isolation verified through JWT claims
- User-level permissions validated for each API request
- Least privilege principle applied to all API operations

### 3.2 Transport Security

All API communications shall enforce encryption standards defined in Encryption and Cryptographic Controls Standard:

**TLS Configuration**

- Minimum TLS version 1.2 with TLS 1.3 preferred
- CloudFront security policy set to TLSv1.2_2021 or higher
- HSTS headers with 31536000 seconds max-age
- Certificate validation required for all HTTPS connections

**Certificate Management**

- AWS Certificate Manager for automatic certificate renewal
- Certificate transparency logging enabled
- CAA DNS records restricting certificate issuance to Amazon
- Monthly certificate expiration monitoring via CloudWatch

### 3.3 Input Validation and Sanitization

All API inputs shall undergo comprehensive validation:

**Request Validation**

- JSON schema validation at API Gateway level
- Maximum request size limited to 10MB
- Parameter type checking and range validation
- NoSQL injection prevention through input validation and typed, parameterized query construction for DocumentDB

**Data Sanitization**

- HTML encoding for all user-supplied content
- PII detection and masking in accordance with Data Classification and Handling Standard
- Email address validation for business contact information
- URL validation for LinkedIn profile links

## 4. Rate Limiting Implementation

### 4.1 Rate Limiting Tier

A single rate limiting tier shall be enforced for all authenticated API calls:

|**Tier**|**Requests per Minute**|**Burst Capacity**|**Applied To**|
|---|---|---|---|
|Standard|100 per API key|200|All authenticated API calls|

### 4.2 Rate Limiting Mechanisms

**Application Rate Limiting**

- One rate tier of 100 requests per minute per API key, enforced in application middleware
- API keys linked to PropelAuth organization IDs
- Burst capacity set to 2x sustained rate

**Lambda Concurrency Controls**

- Reserved concurrency set to 100 for API Lambda functions
- Provisioned concurrency for critical endpoints
- Exponential backoff retry logic implementation

### 4.3 Rate Limit Response Handling

When rate limits are exceeded:

- HTTP 429 (Too Many Requests) status code returned
- X-RateLimit-Limit header indicating limit threshold
- X-RateLimit-Remaining header showing remaining requests
- X-RateLimit-Reset header with reset timestamp
- Retry-After header suggesting wait duration

## 5. API Monitoring and Logging

### 5.1 Audit Logging

All API activity shall be logged per System Monitoring and Logging Procedure:

**Request Logging**

- Timestamp, source IP, and user identifier
- HTTP method, endpoint path, and response code
- Request duration and data volume
- Authentication status and authorization decisions
- PII sanitization applied before logging

**Security Event Logging**

- Failed authentication attempts
- Authorization violations
- Rate limit breaches
- Input validation failures
- Suspicious request patterns

### 5.2 Performance Monitoring

API performance metrics tracked via CloudWatch:

- Request latency percentiles (p50, p90, p95, p99), with a CloudWatch alarm when p95 latency exceeds 2 seconds
- Error rates by endpoint and error type
- Throughput in requests per second
- Lambda cold start frequency
- Integration latency for third-party APIs

### 5.3 Security Monitoring

Continuous security monitoring implemented through:

- AWS Security Hub findings for API vulnerabilities, reviewed monthly and recorded in the compliance platform; critical findings alert in real time via SNS
- CloudTrail logging of all API Gateway configuration changes
- Automated alerting for anomalous API usage patterns
- Integration with incident response procedures defined in Incident Response Procedure

## 6. API Versioning and Deprecation

### 6.1 Versioning Strategy

API versioning shall follow semantic versioning principles:

- Major version changes for breaking modifications
- Minor version changes for backward-compatible features
- Patch version changes for bug fixes
- Version specified in URL path (e.g., /v1/, /v2/)

### 6.2 Deprecation Process

API deprecation shall provide adequate customer notice:

- Minimum 90-day deprecation notice for non-critical endpoints
- Minimum 180-day notice for critical business operations
- Deprecation warnings in API responses
- Migration guides published in developer documentation
- Sunset headers indicating deprecation timeline

## 7. Third-Party API Integration Security

### 7.1 PropelAuth Integration

Authentication service integration shall maintain:

- Secure storage of PropelAuth API keys in AWS Secrets Manager
- Key rotation every 90 days per Encryption and Cryptographic Controls Standard
- Webhook signature validation for all callbacks
- Rate limiting applied to authentication requests
- Failover to cached JWT validation during PropelAuth outages

### 7.2 Customer-Controlled Integrations

Third-party integrations managed by customers shall follow the integration security requirements in section 8 of this standard:

- OAuth 2.0 authorization code flow required
- Refresh tokens stored with AES-256 encryption
- Scope limited to minimum required permissions
- Integration audit logs retained for 90 days
- Customer notification of integration failures

## 8. Integration Security

This section establishes the security requirements and controls for integrating external services, APIs, and platforms with Deal Intelligence's platform. It ensures that business contact information and market intelligence data remain protected when processed through third-party services. Vendor assessment, Data Processing Agreement, and sub-processor requirements for integration partners are defined in the Vendor Management Policy. AWS infrastructure services are covered under the Cloud Infrastructure Security Policy and are considered platform services rather than third-party integrations.

Deal Intelligence shall implement defense-in-depth security controls for all third-party integrations, ensuring that external connections do not compromise the confidentiality, integrity, or availability of customer data. All integrations shall undergo security assessment prior to implementation, utilize encrypted communication channels, implement appropriate authentication and authorization mechanisms, and maintain comprehensive audit logging. Customer-controlled integrations shall be isolated at the company level to prevent cross-tenant data exposure.

The CEO approves new third-party integration partnerships, authorizes integration security exceptions, implements secure integration patterns, manages API keys and authentication credentials in AWS Secrets Manager, reviews integration audit logs via CloudWatch, investigates anomalous integration behavior, and conducts quarterly integration access reviews.

### 8.1 Authentication Standards

All third-party integrations shall implement:

- **PropelAuth Integrations**: JWT tokens with RS256 signing algorithm
- **Customer CRM Integrations**: OAuth 2.0 with refresh token rotation
- **Webhook Endpoints**: HMAC-SHA256 signature verification
- **API Gateway**: AWS API Gateway with API key validation
- **Service-to-Service**: TLS 1.2 or higher with ACM-managed certificates

### 8.2 Credential Management

Integration credentials shall be managed according to:

- Storage in AWS Secrets Manager with automatic rotation
- No hardcoded credentials in Lambda functions or containers
- Unique credentials per integration instance
- Quarterly credential rotation for long-lived tokens
- Immediate revocation upon security incident

### 8.3 Data Exchange Security

**Encryption Requirements**, aligned with the Encryption and Cryptographic Controls Standard:

- All data in transit encrypted using TLS 1.2 or higher
- ACM-managed certificates for all Deal Intelligence endpoints
- Payload encryption for sensitive data fields
- No transmission of Restricted classification data to third parties

**Data Minimization**

- Only necessary data fields shared with third parties
- PII fields excluded unless explicitly required
- Customer data isolated by company_id partition
- No bulk data exports without CEO approval

### 8.4 Integration Architecture Patterns

**Approved Integration Patterns**

|**Pattern**|**Use Case**|**Security Controls**|
|---|---|---|
|API Gateway Proxy|Customer API access|Rate limiting, JWT validation, CloudWatch logging|
|Lambda Function Integration|Event processing|VPC isolation, IAM roles, timeout controls|
|EventBridge Rules|Asynchronous events|Event filtering, CloudWatch logging and alarms on failed invocations|
|Webhook Receiver|External notifications|Signature validation, replay protection|
|OAuth 2.0 Flow|Customer authorization|PKCE implementation, state parameter validation|

**Prohibited Practices**

- Direct database access by third-party services
- Unencrypted data transmission
- Shared authentication credentials across customers
- Synchronous calls exceeding 30-second timeout
- Integration points without error handling

### 8.5 Customer-Controlled Integrations

**CRM System Integration** — customer CRM integrations shall implement:

- Company-level isolation using PropelAuth organization IDs
- OAuth 2.0 authorization with customer consent
- Field mapping configuration stored in DocumentDB
- Sync status tracking with error reporting
- Rate limiting per customer organization (100 requests/minute)

**Slack Integration** — Slack workspace integrations shall enforce:

- Workspace-specific webhook URLs
- Channel access restrictions
- Message formatting without PII exposure
- Audit logging of all notifications sent
- Customer-controlled enable/disable toggles

### 8.6 Integration Monitoring and Logging

As defined in the System Monitoring and Logging Procedure:

|**Metric**|**Threshold**|**Alert Method**|
|---|---|---|
|API Error Rate|>5% over 5 minutes|SNS notification|
|Authentication Failures|>10 per minute|Security Hub finding|
|Response Time|>2 seconds p95|CloudWatch alarm|
|Data Volume|>1GB per hour|Billing alert|
|Certificate Expiry|<30 days|CloudWatch alarm|

All integrations shall log:

- Authentication attempts and outcomes
- Data access requests with customer context
- Configuration changes to integration settings
- Error conditions and retry attempts
- Performance metrics for SLA monitoring

Logs shall be retained according to the Data Retention and Disposal Policy with 90-day CloudWatch retention for operational logs.

### 8.7 Integration Security Testing and Vulnerability Management

Following the Penetration Testing and Security Assessment Procedure:

- Continuous dependency and code scanning of integration code via GitHub Dependabot, GitHub code scanning, and Bandit, Trivy and TruffleHog in CI
- Annual penetration testing including third-party integration vectors
- OWASP Top 10 vulnerability assessment for web-based integrations
- Authentication bypass testing for OAuth flows
- Input validation testing for webhook receivers

Integration vulnerabilities shall be managed per the Vulnerability Management Procedure:

- Critical vulnerabilities remediated within 24 hours (exploited or critical); dependency CVEs rated critical within 7 days
- High vulnerabilities remediated within 30 days
- Integration disabled if remediation timeline cannot be met
- Customer notification for vulnerabilities affecting their data

### 8.8 Integration Lifecycle Management

**Implementation Phase** — new integrations follow the Secure Software Development Lifecycle (SDLC) Standard:

1. Security requirements definition
2. Threat modeling for integration points
3. Secure coding practices for integration logic
4. Security testing before production deployment
5. Documentation in the compliance platform

**Operational Phase** — active integrations require:

- Monthly review of Security Hub findings affecting integrations
- Quarterly access and permission reviews
- Annual vendor reassessment per Vendor Management Policy
- Continuous monitoring via CloudWatch
- Performance tracking against SLAs

**Decommissioning Phase** — when retiring integrations:

1. Customer notification 30 days in advance
2. Data migration or export options provided
3. Credential revocation and deletion
4. Audit log preservation per retention policy
5. Documentation update in configuration management

### 8.9 Data Protection for Integrations

Third-party integrations shall maintain compliance with GDPR (data processor agreements for EU data handling) and CCPA (consumer rights preservation across integrations), and OWASP ASVS Level 2 for web integrations. Integration design shall support the Data Subject Rights Request Procedure:

- Data portability through standardized export formats
- Right to erasure propagation to integrated systems
- Consent management for optional integrations
- Access request fulfillment including third-party data

## 9. API Development Security

### 9.1 Secure Development Practices

API development shall adhere to Secure Software Development Lifecycle (SDLC) Standard:

- Security requirements defined during design phase
- Threat modeling for new API endpoints
- Static application security testing (SAST) in the GitHub Actions CI pipeline (Bandit, Trivy, TruffleHog)
- Pull request with required CI status checks on the protected `main` branch, with a logged self-review of authentication and authorization logic in the PR

### 9.2 API Testing Requirements

Comprehensive testing required before deployment:

- Unit tests (pytest) executed as a required CI status check, alongside Black, isort and Flake8
- Integration tests for third-party dependencies
- Performance testing under expected load conditions
- Security testing including OWASP Top 10 API vulnerabilities
- Penetration testing annually per Penetration Testing and Security Assessment Procedure

## 10. API Documentation and Inventory

### 10.1 API Documentation

All APIs shall maintain current documentation including:

- OpenAPI 3.0 specification files
- Authentication and authorization requirements
- Rate limiting threshold
- Request/response schemas with examples
- Error codes and troubleshooting guides

### 10.2 API Inventory Management

API inventory tracked in the compliance platform:

- Endpoint URL and version
- Data classification level per Data Classification and Handling Standard
- Authentication mechanism
- Rate limiting configuration
- Last security assessment date

## 11. Incident Response for API Security Events

### 11.1 API Security Incidents

API-specific incidents requiring immediate response:

- Unauthorized API access or data exfiltration
- API key or token compromise
- Distributed denial of service (DDoS) attacks
- Rate limiting bypass attempts
- API vulnerability exploitation
- Security incidents involving third-party integrations or a breach at a third-party service

### 11.2 Response Procedures

Upon detection of API security incident:

1. Immediate containment through API Gateway throttling or blocking, or isolation of the affected integration
2. Credential rotation for compromised authentication tokens and affected integration points
3. Incident logged in the compliance platform Incident Reporting system
4. Impact assessment within 4 business hours
5. Customer notification within 48 hours if data affected
6. Post-incident review per Incident Response Procedure, including third-party vendor involvement and vendor re-assessment per Vendor Management Policy where a third-party service was breached

## 12. Compliance and Regulatory Requirements

### 12.1 SOC 2 Compliance

API security controls support SOC 2 Trust Service Criteria:

- CC6.1: Logical access controls through JWT authentication
- CC6.6: Encryption of data in transit via TLS
- CC7.1: Security monitoring through CloudWatch and Security Hub
- A1.2: Rate limiting ensures service availability

### 12.2 Data Protection Compliance

API operations comply with GDPR and CCPA requirements:

- Data minimization in API responses
- Purpose limitation for data processing
- Audit trails for compliance demonstration
- Support for data subject rights per Data Subject Rights Request Procedure

## 13. Performance and Availability

### 13.1 Service Level Objectives

API performance targets aligned with Service Level Agreement (SLA) Management Policy:

- 99.9% API availability measured monthly
- 95th percentile latency under 2 seconds
- Error rate below 0.1% for valid requests
- Rate limit accuracy within 5% tolerance

### 13.2 Capacity Planning

Quarterly capacity reviews shall assess:

- API request volume trends
- Lambda concurrent execution metrics
- Rate limiting (HTTP 429) statistics
- Infrastructure scaling requirements

## 14. Related Documents

- Information Security Policy
- Access Control and Authentication Policy
- Encryption and Cryptographic Controls Standard
- Cloud Infrastructure Security Policy
- System Monitoring and Logging Procedure
- Incident Response Procedure
- Secure Software Development Lifecycle (SDLC) Standard
- Vendor Management Policy
- Data Classification and Handling Standard
- Vulnerability Management Procedure
- Change Management Policy
- Service Level Agreement (SLA) Management Policy
- Penetration Testing and Security Assessment Procedure
- Data Subject Rights Request Procedure

## 15. Review and Updates

This standard shall be reviewed annually and updated to reflect:

- Changes in API architecture or technology stack
- Emerging API security threats and vulnerabilities
- Updates to regulatory requirements
- Lessons learned from security incidents
- Customer feedback and requirements

The next scheduled review date shall be documented in the compliance platform with automated notifications to the CEO 30 days prior to the review date.

## Revision history

|**Version**|**Date**|**Author**|**Summary**|
|---|---|---|---|
|1.0|November 13, 2025|mo@dealintelligence.io|Initial audited version|
|2.0|<to be set at publication>|mo@dealintelligence.io|Scope aligned to Security, Availability and Confidentiality; single 100 requests/minute rate tier enforced in middleware; usage plans, WebSockets, DLQs, DAST and coverage targets removed; p95 > 2 s latency alert; monthly Security Hub review; NoSQL input-validation wording; Third-Party Integration Security Guidelines merged in as section 8 (Integration security)|
