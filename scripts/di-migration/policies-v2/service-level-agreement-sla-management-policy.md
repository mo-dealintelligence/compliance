---
title: "Service Level Agreement (SLA) Management Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "service-level-agreement-sla-management-policy-v1.0.pdf"
---

# Service Level Agreement (SLA) Management Policy

## 1. Purpose

This Service Level Agreement (SLA) Management Policy establishes the framework for defining, monitoring, and maintaining service level commitments for Deal Intelligence LLC's platform. This policy ensures consistent delivery of services that meet customer expectations while maintaining compliance with SOC 2 Trust Services Criteria, specifically addressing A1.1 (Availability) and CC2.1 (Communication and Information).

This policy operationalizes the availability commitments defined in the Information Security Policy and supports the service continuity objectives established in the Business Continuity Plan, ensuring that Deal Intelligence maintains its committed 99.9% uptime SLA for the platform.

## 2. Scope

This policy applies to:

- All customer-facing services delivered through the platform

- AWS infrastructure components supporting service delivery (Lambda functions, DocumentDB, CloudFront CDN)

- Third-party services integrated into the platform (PropelAuth authentication services)

- Internal operational processes that impact service availability and performance

- All personnel responsible for service delivery, monitoring, and customer support

- Contractual service level agreements with enterprise customers

## 3. Service Level Definitions

### 3.1 Core Service Levels

Deal Intelligence commits to the following service level targets:

|**Service Component**|**SLA Target**|**Measurement Period**|**Calculation Method**|
|---|---|---|---|
|Platform Availability|99.9%|Monthly|(Total Minutes - Downtime Minutes) / Total Minutes × 100|
|API Response Time|< 2 seconds|95th percentile|CloudWatch metrics aggregation|
|Data Processing Accuracy|99.5%|Monthly|Validated records / Total processed records × 100|
|Lead Delivery Time|< 24 hours|Per request|Time from request to delivery completion|
|Authentication Service|Provided by PropelAuth under its own SLA|Monthly|PropelAuth published service status|
|Data Refresh Frequency|Daily|Business days|Successful refresh jobs / Scheduled jobs × 100|

### 3.2 Service Availability Calculation

Service availability excludes:

- Scheduled maintenance windows (communicated 72 hours in advance)

- Force majeure events as defined in customer agreements

- Customer-initiated actions causing service disruption

- Third-party service outages beyond Deal Intelligence control

## 4. SLA Monitoring and Measurement

### 4.1 Automated Monitoring Infrastructure

Service levels are continuously monitored through:

- **CloudWatch Metrics** : Real-time monitoring of Lambda function performance, API Gateway latency, and DocumentDB response times

- **CloudWatch Alarms** : Alarms on API errors and latency (p95 > 2 seconds) with real-time SNS notification

- **AWS Health Dashboard** : Regional service status monitoring for AWS infrastructure dependencies

- **PropelAuth Service Status** : Authentication service availability, which is provided by PropelAuth under its own SLA

### 4.2 Performance Metrics Collection

Key performance indicators tracked include:

|**Metric**|**Collection Method**|**Retention Period**|**Alert Threshold**|
|---|---|---|---|
|API Latency|CloudWatch API Gateway metrics|90 days|p95 > 2 seconds|
|Error Rate|Lambda function error tracking|90 days|> 1%|
|Database Performance|DocumentDB CloudWatch metrics|90 days|> 500ms query time|
|CDN Cache Hit Ratio|CloudFront distribution metrics|90 days|< 80%|
|Container Health|ECS service metrics|30 days|Task failures > 2|

## 5. Service Level Reporting

### 5.1 Availability Record and Customer Communication

The monthly availability figure is computed from CloudWatch metrics and recorded in the compliance platform, together with:

- Overall platform availability percentage

- API performance metrics (response times, error rates)

- Incident summary with root cause analysis

- Service credit calculations (if applicable)

- Planned maintenance schedule for upcoming month

Customers are notified of planned maintenance by email.

### 5.2 Internal Reporting

Monthly internal SLA reviews conducted via the compliance platform include:

- Service level achievement against targets

- Trending analysis of performance metrics

- Capacity planning recommendations

- Risk indicators per Risk Assessment Procedure

## 6. Service Credit Framework

### 6.1 Service Credit Calculation

When service levels fall below committed thresholds:

|**Monthly Uptime Percentage**|**Service Credit**|
|---|---|
|99.9% to 99.0%|5% of monthly fee|
|99.0% to 95.0%|10% of monthly fee|
|Below 95.0%|25% of monthly fee|

### 6.2 Service Credit Process

1. Customer must submit credit request within 30 days of SLA breach

2. Chief Executive Officer reviews and validates claim within 5 business days

3. Approved credits applied to next invoice or refunded upon request

4. Credit requests tracked in the compliance platform for audit purposes

## 7. Incident Impact on SLAs

### 7.1 Incident Classification

Service incidents are classified per the Incident Response Procedure:

|**Severity**|**Impact on SLA**|**Resolution Target**|
|---|---|---|
|Critical|Service unavailable|4 hours|
|High|Degraded performance|8 hours|
|Medium|Limited functionality|24 hours|
|Low|Minor issues|72 hours|

Critical (P1) incidents are acknowledged by the CEO within 4 business hours, with Security Hub/SNS paging for critical findings. Response targets for other severities are defined in the Incident Response Procedure.

### 7.2 Communication During Incidents

Customer communication requirements:

- Initial notification by email following acknowledgment of a critical incident (see Section 7.1)

- Status updates every 2 hours during active incidents

- Root cause analysis within 48 hours of resolution

- Post-incident report provided to affected customers by email

## 8. Maintenance Windows

### 8.1 Scheduled Maintenance

- **Standard Window** : Sunday 02:00-06:00 UTC

- **Notification Period** : 72 hours advance notice via email

- **Emergency Maintenance** : 24 hours notice when possible

- **Maintenance Tracking** : Recorded in the compliance platform

### 8.2 Zero-Downtime Deployments

Preferred deployment strategies to minimize service impact:

- Lambda versioned deployments with rollback via `serverless rollback`

- Rolling updates for ECS container services

- Database migrations during low-traffic periods

- CloudFront cache warming before traffic shifts

## 9. Third-Party Service Dependencies

### 9.1 Sub-Processor SLAs

Management of third-party service levels per Vendor Management Policy:

|**Service Provider**|**Service**|**Their SLA**|**Our Mitigation**|
|---|---|---|---|
|AWS|Infrastructure|99.99%|Multi-AZ deployment|
|PropelAuth|Authentication|PropelAuth's own published SLA|Token caching, graceful degradation|

### 9.2 Dependency Monitoring

- AWS Health Dashboard and PropelAuth published service status monitored for dependency availability

- Fallback mechanisms for authentication service outages

- Lambda versioned deployments with reserved concurrency and rollback via `serverless rollback`

- Vendor performance reviewed annually in the compliance platform, supported by the continuous monthly availability record

## 10. Continuous Improvement

### 10.1 SLA Review Process

Annual SLA reviews (with the monthly availability record in the compliance platform as the continuous input) include:

- Analysis of SLA achievement trends

- Customer feedback incorporation

- Capacity planning based on growth projections

- Technology improvements to enhance reliability

- Updates to monitoring and alerting thresholds

### 10.2 Performance Optimization

Ongoing initiatives to improve service levels:

- Lambda function performance tuning (reserved concurrency optimization)

- Database query optimization and indexing improvements

- CDN configuration refinement for better cache hit ratios

- API rate limiting adjustments per API Security and Rate Limiting Standard

## 11. Roles and Responsibilities

### 11.1 Chief Executive Officer (CEO)

- Overall SLA policy ownership and enforcement

- Service credit approval authority

- Customer escalation point for SLA disputes

- Annual SLA review and reporting; monthly availability record

- Real-time service monitoring and alerting

- Incident response coordination

- Performance optimization implementation

- Maintenance window planning and execution

- Customer SLA communication and reporting

- Service credit request processing

- Customer feedback collection

- SLA documentation maintenance

### 11.2 Go-to-Market Contractor

- No production access or monitoring responsibilities

- Forwards customer SLA questions and feedback to the CEO

## 12. Compliance and Audit

### 12.1 SOC 2 Evidence Collection

SLA management evidence for SOC 2 audit includes:

- Monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform

- Incident response logs from the compliance platform Incident Reporting system

- Service credit calculations and approvals

- Customer communication records

- Maintenance window notifications

### 12.2 Regulatory Compliance

SLA management supports compliance with:

- **GDPR Article 32** : Ensuring ongoing availability of processing systems

- **CCPA Section 1798.150** : Maintaining reasonable security procedures

- **SOC 2 Availability Criteria** : Demonstrating system availability commitments

## 13. Exceptions and Escalations

### 13.1 SLA Exceptions

Requests for custom SLAs require:

1. Business justification documentation

2. Risk assessment per established procedures

3. Technical feasibility analysis

4. Chief Executive Officer approval

5. Documentation in customer contract

### 13.2 Escalation Path

For SLA-related issues:

1. Initial report through standard support channels

2. Escalation to the Chief Executive Officer, who acknowledges critical issues within 4 business hours

3. CEO review for repeated SLA breaches

4. Management review for systemic issues, recorded in the quarterly management meeting minutes

## 14. Related Documents

- Information Security Policy

- Business Continuity Plan

- Incident Response Procedure

- Change Management Policy

- Vendor Management Policy

- System Monitoring and Logging Procedure

- Cloud Infrastructure Security Policy

- API Security and Rate Limiting Standard

- Risk Assessment Procedure

_This policy is maintained in the compliance platform and subject to annual review to ensure alignment with customer expectations, technical capabilities, and regulatory requirements._

## 15. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Processing Integrity mapping removed; authentication availability deferred to PropelAuth's own SLA; synthetic monitoring, customer-facing SLA reports and public status communications, deployment-strategy and dependency-check claims replaced by CloudWatch alarms, the monthly availability record and Lambda versioned deployments; response commitment replaced by 4-business-hour P1 acknowledgment; roles reduced to CEO / Go-to-Market Contractor; export footer removed; policy review set to annual |
