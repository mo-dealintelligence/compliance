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

This standard sets the mandatory requirements for securing the application programming interfaces (APIs) of Deal Intelligence LLC's B2B market intelligence platform and for rate limiting API traffic. It protects business contact information and customer data transmitted through APIs while maintaining service availability. It supports SOC 2 Trust Services Criteria CC6.1 (logical access controls through JWT authentication), CC6.6 (encryption of data in transit via TLS), CC7.1 (security monitoring through CloudWatch and Security Hub), and A1.2 (availability through rate limiting).

The standard implements the API security requirements of the Information Security Policy and complements the Cloud Infrastructure Security Policy with specific rules for API endpoints, authentication mechanisms, traffic management, and the security of third-party integrations (Section 8).

## 2. Scope

This standard applies to:

- All REST APIs exposed through CloudFront distributions in front of Lambda function URLs
- Internal service-to-service communications within VPC boundaries
- Third-party API integrations, including PropelAuth authentication services
- Lambda function endpoints with 900-second timeout configurations
- Customer-controlled integrations with CRM systems and Slack workspaces
- Webhook endpoints and event-driven integrations via EventBridge
- OAuth 2.0 and JWT-based authentication flows
- All personnel responsible for API development, deployment, and maintenance

## 3. API security requirements

### 3.1 Authentication and authorization

All API endpoints implement multi-layered authentication controls.

**JWT token validation**

- PropelAuth JWT tokens required for all authenticated endpoints
- Token expiration set to a maximum of 24 hours, with refresh token rotation
- RS256 algorithm for token signing with 2048-bit RSA keys
- Token validation performed in the API middleware on every request before business logic runs

**Authorization controls**

- Role-based access control (RBAC) enforced per the Access Control and Authentication Policy
- Company-level data isolation verified through JWT claims
- User-level permissions validated for each API request
- Least privilege principle applied to all API operations

### 3.2 Transport security

All API communications enforce the encryption requirements of the Encryption and Cryptographic Controls Standard.

**TLS configuration**

- Minimum TLS version 1.2, with TLS 1.3 preferred
- CloudFront security policy set to TLSv1.2_2021 or higher
- HSTS headers with a max-age of 31536000 seconds
- Certificate validation required for all HTTPS connections

**Certificate management**

- ACM for automatic certificate renewal
- Certificate transparency logging enabled
- CAA DNS records restricting certificate issuance to Amazon
- Monthly certificate expiration monitoring via CloudWatch

### 3.3 Input validation and sanitization

All API inputs are validated.

**Request validation**

- JSON schema validation by the Pydantic request models on every request
- Maximum request size limited to 10 MB
- Parameter type checking and range validation
- NoSQL injection prevention through input validation and typed, parameterized query construction for DocumentDB

**Data sanitization**

- HTML encoding for all user-supplied content
- PII detection and masking per the Data Classification and Handling Standard
- Email address validation for business contact information
- URL validation for LinkedIn profile links

## 4. Rate limiting implementation

### 4.1 Rate limiting tier

A single rate limiting tier is enforced for all authenticated API calls:

|**Tier**|**Requests per minute**|**Burst capacity**|**Applied to**|
|---|---|---|---|
|Standard|100 per API key|200|All authenticated API calls|

### 4.2 Rate limiting mechanisms

**Application rate limiting**

- One rate tier of 100 requests per minute per API key, enforced in application middleware
- API keys linked to PropelAuth organization IDs
- Burst capacity set to 2x the sustained rate

**Lambda concurrency controls**

- Reserved concurrency set to 100 for API Lambda functions
- Provisioned concurrency for critical endpoints
- Exponential backoff retry logic

### 4.3 Rate limit response handling

When rate limits are exceeded, the API returns:

- HTTP 429 (Too Many Requests) status code
- X-RateLimit-Limit header indicating the limit threshold
- X-RateLimit-Remaining header showing remaining requests
- X-RateLimit-Reset header with the reset timestamp
- Retry-After header suggesting the wait duration

## 5. API monitoring and logging

### 5.1 Audit logging

All API activity is logged per the System Monitoring and Logging Procedure.

**Request logging**

- Timestamp, source IP, and user identifier
- HTTP method, endpoint path, and response code
- Request duration and data volume
- Authentication status and authorization decisions
- PII sanitization applied before logging

**Security event logging**

- Failed authentication attempts
- Authorization violations
- Rate limit breaches
- Input validation failures
- Suspicious request patterns

### 5.2 Performance monitoring

API performance metrics are tracked via CloudWatch:

- Request latency percentiles (p50, p90, p95, p99), with a CloudWatch alarm when p95 latency exceeds 2 seconds
- Error rates by endpoint and error type
- Throughput in requests per second
- Lambda cold start frequency
- Integration latency for third-party APIs

### 5.3 Security monitoring

Continuous security monitoring is implemented through:

- Security Hub findings for API vulnerabilities, reviewed monthly and recorded in the compliance platform; critical findings alert in real time via SNS
- CloudTrail logging of all CloudFront and Lambda configuration changes
- Automated alerting for anomalous API usage patterns
- The Incident Response Procedure for confirmed security events

## 6. API versioning and deprecation

### 6.1 Versioning strategy

API versioning follows semantic versioning:

- Major version changes for breaking modifications
- Minor version changes for backward-compatible features
- Patch version changes for bug fixes
- Version specified in the URL path (e.g., /v1/, /v2/)

### 6.2 Deprecation process

API deprecation provides customers with:

- Minimum 90 days' deprecation notice for non-critical endpoints
- Minimum 180 days' notice for critical business operations
- Deprecation warnings in API responses
- Migration guides published in developer documentation
- Sunset headers indicating the deprecation timeline

## 7. Third-party API integration security

### 7.1 PropelAuth integration

The authentication service integration maintains:

- Secure storage of PropelAuth API keys in Secrets Manager
- Key rotation every 90 days per the Encryption and Cryptographic Controls Standard
- Webhook signature validation for all callbacks
- Rate limiting applied to authentication requests
- Failover to cached JWT validation during PropelAuth outages

### 7.2 Customer-controlled integrations

Third-party integrations managed by customers follow the integration security requirements in Section 8 of this standard:

- OAuth 2.0 authorization code flow required
- Refresh tokens stored with AES-256 encryption
- Scope limited to the minimum required permissions
- Integration audit logs retained for 90 days
- Customer notification of integration failures

## 8. Integration security

This section sets the security requirements for integrating external services, APIs, and platforms with the Deal Intelligence platform, so that business contact information and market intelligence data remain protected when processed through third-party services. Vendor assessment, Data Processing Agreement, and sub-processor requirements for integration partners are defined in the Vendor Management Policy. AWS infrastructure services are covered by the Cloud Infrastructure Security Policy and are platform services, not third-party integrations.

All integrations undergo security assessment before implementation, use encrypted communication channels, implement authentication and authorization, and maintain audit logging, so that external connections do not compromise the confidentiality, integrity, or availability of customer data. Customer-controlled integrations are isolated at the company level to prevent cross-tenant data exposure.

The CEO:

- Approves new third-party integration partnerships
- Authorizes integration security exceptions
- Implements secure integration patterns
- Manages API keys and authentication credentials in Secrets Manager
- Reviews integration audit logs via CloudWatch
- Investigates anomalous integration behavior
- Conducts quarterly integration access reviews

### 8.1 Authentication standards

All third-party integrations implement:

- **PropelAuth integrations**: JWT tokens with the RS256 signing algorithm
- **Customer CRM integrations**: OAuth 2.0 with refresh token rotation
- **Webhook endpoints**: HMAC-SHA256 signature verification
- **Edge**: CloudFront in front of Lambda function URLs, with API key validation in the middleware
- **Service-to-service**: TLS 1.2 or higher with ACM-managed certificates

### 8.2 Credential management

Integration credentials are managed as follows:

- Stored in Secrets Manager with automatic rotation
- No hardcoded credentials in Lambda functions or containers
- Unique credentials per integration instance
- Quarterly credential rotation for long-lived tokens
- Immediate revocation upon a security incident

### 8.3 Data exchange security

**Encryption requirements**, aligned with the Encryption and Cryptographic Controls Standard:

- All data in transit encrypted using TLS 1.2 or higher
- ACM-managed certificates for all Deal Intelligence endpoints
- Payload encryption for sensitive data fields
- No transmission of Restricted classification data to third parties

**Data minimization**

- Only necessary data fields shared with third parties
- PII fields excluded unless explicitly required
- Customer data isolated by company_id partition
- No bulk data exports without CEO approval

### 8.4 Integration architecture patterns

**Approved integration patterns**

|**Pattern**|**Use case**|**Security controls**|
|---|---|---|
|CloudFront → Lambda function URL|Customer API access|Rate limiting, JWT validation, CloudWatch logging|
|Lambda function integration|Event processing|VPC isolation, IAM roles, timeout controls|
|EventBridge rules|Asynchronous events|Event filtering, CloudWatch logging and alarms on failed invocations|
|Webhook receiver|External notifications|Signature validation, replay protection|
|OAuth 2.0 flow|Customer authorization|PKCE implementation, state parameter validation|

**Prohibited practices**

- Direct database access by third-party services
- Unencrypted data transmission
- Shared authentication credentials across customers
- Synchronous calls exceeding a 30-second timeout
- Integration points without error handling

### 8.5 Customer-controlled integrations

**CRM system integration** — customer CRM integrations implement:

- Company-level isolation using PropelAuth organization IDs
- OAuth 2.0 authorization with customer consent
- Field mapping configuration stored in DocumentDB
- Sync status tracking with error reporting
- Rate limiting per customer organization (100 requests/minute)

**Slack integration** — Slack workspace integrations enforce:

- Workspace-specific webhook URLs
- Channel access restrictions
- Message formatting without PII exposure
- Audit logging of all notifications sent
- Customer-controlled enable/disable toggles

### 8.6 Integration monitoring and logging

Thresholds are defined in the System Monitoring and Logging Procedure:

|**Metric**|**Threshold**|**Alert method**|
|---|---|---|
|API error rate|>5 % over 5 minutes|SNS notification|
|Authentication failures|>10 per minute|Security Hub finding|
|Response time|p95 > 2 seconds|CloudWatch alarm|
|Data volume|>1 GB per hour|Billing alert|
|Certificate expiry|<30 days|CloudWatch alarm|

All integrations log:

- Authentication attempts and outcomes
- Data access requests with customer context
- Configuration changes to integration settings
- Error conditions and retry attempts
- Performance metrics for SLA monitoring

Logs are retained per the Data Retention and Disposal Policy, with 90-day CloudWatch retention for operational logs.

### 8.7 Integration security testing and vulnerability management

Testing follows the Penetration Testing and Security Assessment Procedure:

- Continuous dependency and code scanning of integration code via GitHub Dependabot, GitHub code scanning, and Bandit, Trivy, and TruffleHog in CI
- Annual penetration testing, including third-party integration vectors
- OWASP Top 10 vulnerability assessment for web-based integrations
- Authentication bypass testing for OAuth flows
- Input validation testing for webhook receivers

Integration vulnerabilities are managed per the Vulnerability Management Procedure:

- Critical vulnerabilities remediated within 24 hours (exploited or critical); dependency CVEs rated critical within 7 days
- High vulnerabilities remediated within 30 days
- Integration disabled if the remediation timeline cannot be met
- Customer notification for vulnerabilities affecting their data

### 8.8 Integration lifecycle management

**Implementation phase** — new integrations follow the Secure Software Development Lifecycle (SDLC) Standard:

1. Security requirements definition
2. Threat modeling for integration points
3. Secure coding practices for integration logic
4. Security testing before production deployment
5. Documentation in the compliance platform

**Operational phase** — active integrations require:

- Monthly review of Security Hub findings affecting integrations
- Quarterly access and permission reviews
- Annual vendor reassessment per the Vendor Management Policy
- Continuous monitoring via CloudWatch
- Performance tracking against SLAs

**Decommissioning phase** — when retiring integrations:

1. Customer notification 30 days in advance
2. Data migration or export options provided
3. Credential revocation and deletion
4. Audit log preservation per the Data Retention and Disposal Policy
5. Documentation update in configuration management

### 8.9 Data protection for integrations

Third-party integrations comply with GDPR (data processor agreements for EU data handling), CCPA (consumer rights preserved across integrations), and OWASP ASVS Level 2 for web integrations. Integration design supports the Data Subject Rights Request Procedure through:

- Data portability through standardized export formats
- Right to erasure propagation to integrated systems
- Consent management for optional integrations
- Access request fulfillment, including third-party data

## 9. API development security

### 9.1 Secure development practices

API development follows the Secure Software Development Lifecycle (SDLC) Standard:

- Security requirements defined during the design phase
- Threat modeling for new API endpoints
- Static application security testing (SAST) in the GitHub Actions CI pipeline (Bandit, Trivy, TruffleHog)
- Pull request with required CI status checks on the protected `main` branch, with a logged self-review of authentication and authorization logic in the PR

### 9.2 API testing requirements

The following testing is required before deployment:

- Unit tests (pytest) executed as a required CI status check, alongside Black, isort, and Flake8
- Integration tests for third-party dependencies
- Performance testing under expected load conditions
- Security testing, including OWASP Top 10 API vulnerabilities
- Penetration testing annually per the Penetration Testing and Security Assessment Procedure

## 10. API documentation and inventory

### 10.1 API documentation

All APIs maintain current documentation, including:

- OpenAPI 3.0 specification files
- Authentication and authorization requirements
- Rate limiting threshold
- Request/response schemas with examples
- Error codes and troubleshooting guides

### 10.2 API inventory management

The API inventory is tracked in the compliance platform and records:

- Endpoint URL and version
- Data classification level per the Data Classification and Handling Standard
- Authentication mechanism
- Rate limiting configuration
- Last security assessment date

## 11. Incident response for API security events

### 11.1 API security incidents

API-specific incidents requiring immediate response:

- Unauthorized API access or data exfiltration
- API key or token compromise
- Distributed denial of service (DDoS) attacks
- Rate limiting bypass attempts
- API vulnerability exploitation
- Security incidents involving third-party integrations, or a breach at a third-party service

### 11.2 Response procedures

Upon detection of an API security incident:

1. Immediate containment by revoking the API key, blocking at the middleware rate limiter or CloudFront, or isolating the affected integration
2. Credential rotation for compromised authentication tokens and affected integration points
3. Incident logged in the compliance platform Incident Reporting system
4. Impact assessment within 4 business hours
5. Customer notification within 48 hours if data is affected
6. Post-incident review per the Incident Response Procedure, including third-party vendor involvement and vendor reassessment per the Vendor Management Policy where a third-party service was breached

## 12. Data protection requirements

API operations comply with GDPR and CCPA through:

- Data minimization in API responses
- Purpose limitation for data processing
- Audit trails for compliance demonstration
- Support for data subject rights per the Data Subject Rights Request Procedure

## 13. Performance and availability

### 13.1 Service level objectives

API performance targets are aligned with the Service Level Agreement (SLA) Management Policy:

- 99.9 % API availability, measured monthly
- p95 latency under 2 seconds
- Error rate below 0.1 % for valid requests
- Rate limit accuracy within 5 % tolerance

### 13.2 Capacity planning

Quarterly capacity reviews assess:

- API request volume trends
- Lambda concurrent execution metrics
- Rate limiting (HTTP 429) statistics
- Infrastructure scaling requirements

## 14. Review

This standard is reviewed annually and updated for:

- Changes in API architecture or technology stack
- Emerging API security threats and vulnerabilities
- Updates to regulatory requirements
- Lessons learned from security incidents
- Customer feedback and requirements

The next scheduled review date is recorded in the compliance platform, which notifies the CEO 30 days before the review date.

## 15. Related documents

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
- Data Retention and Disposal Policy

## 16. Revision history

|**Version**|**Date**|**Author**|**Summary**|
|---|---|---|---|
|1.0|November 13, 2025|mo@dealintelligence.io|Initial audited version|
|2.0|<to be set at publication>|mo@dealintelligence.io|Scope aligned to Security, Availability and Confidentiality; single 100 requests/minute rate tier enforced in middleware; usage plans, WebSockets, DLQs, DAST and coverage targets removed; p95 > 2 s latency alert; monthly Security Hub review; NoSQL input-validation wording; Third-Party Integration Security Guidelines merged in as section 8 (Integration security)|
