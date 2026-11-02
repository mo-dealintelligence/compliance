---
title: "Service Level Agreement (SLA) Management Policy"
doc_type: "Policy"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "service-level-agreement-sla-management-policy-v1.0.pdf"
---

# Service Level Agreement (SLA) Management Policy

## 1. Purpose

This policy defines how Deal Intelligence LLC sets, monitors, and maintains the service level commitments for its platform. It supports the SOC 2 Trust Services Criteria A1.1 (Availability) and CC2.1 (Communication and Information).

It implements the availability commitments in the Information Security Policy, supports the service continuity objectives in the Business Continuity Plan, and holds Deal Intelligence to its committed 99.9 % uptime SLA.

## 2. Scope

This policy applies to:

- All customer-facing services delivered through the platform
- The AWS infrastructure that delivers them (Lambda functions, DocumentDB, CloudFront)
- Third-party services integrated into the platform (PropelAuth authentication)
- Internal operational processes that affect service availability and performance
- All personnel responsible for service delivery, monitoring, and customer support
- Contractual service level agreements with enterprise customers

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

- Owns and enforces this policy and maintains the SLA documentation
- Monitors the service in real time and responds to alerts
- Coordinates incident response
- Plans and executes maintenance windows
- Implements performance optimizations
- Records the monthly availability figure and performs the annual SLA review
- Communicates with customers on SLAs, incidents, and maintenance, and collects customer feedback
- Processes and approves service credit requests
- Is the customer escalation point for SLA disputes

### 3.2 Go-to-Market Contractor

- Has no production access or monitoring responsibilities
- Forwards customer SLA questions and feedback to the CEO

## 4. Service level definitions

### 4.1 Core service levels

Deal Intelligence commits to the following targets:

|**Service component**|**SLA target**|**Measurement period**|**Calculation method**|
|---|---|---|---|
|Platform availability|99.9 %|Monthly|(Total minutes − downtime minutes) / total minutes × 100, measured over all minutes in the month, excluding announced maintenance windows (§4.2)|
|API response time|< 2 seconds|95th percentile|CloudWatch metrics aggregation|
|Data processing accuracy|99.5 %|Monthly|Validated records / total processed records × 100|
|Lead delivery time|< 24 hours|Per request|Time from request to delivery completion|
|Authentication service|Provided by PropelAuth under its own SLA|Monthly|PropelAuth published service status|
|Data refresh frequency|Daily|Business days|Successful refresh jobs / scheduled jobs × 100|

### 4.2 Availability calculation

Availability excludes:

- Scheduled maintenance windows (notified 72 hours in advance)
- Force majeure events as defined in customer agreements
- Customer-initiated actions that disrupt the service
- Third-party service outages outside Deal Intelligence's control

## 5. SLA monitoring and measurement

### 5.1 Monitoring infrastructure

Service levels are monitored continuously through:

- **CloudWatch metrics**: real-time monitoring of Lambda function performance, CloudFront and Lambda latency, and DocumentDB response times
- **CloudWatch alarms**: alarms on API errors and latency (p95 > 2 seconds) with real-time SNS notification
- **AWS Health Dashboard**: regional service status for the AWS dependencies
- **PropelAuth service status**: authentication availability, provided by PropelAuth under its own SLA

### 5.2 Performance metrics

|**Metric**|**Collection method**|**Retention period**|**Alert threshold**|
|---|---|---|---|
|API latency|CloudWatch Lambda duration and CloudFront metrics|90 days|p95 > 2 seconds|
|Error rate|Lambda function error tracking|90 days|> 1 %|
|Database performance|DocumentDB CloudWatch metrics|90 days|> 500 ms query time|
|CDN cache hit ratio|CloudFront distribution metrics|90 days|< 80 %|
|Container health|ECS service metrics|30 days|Task failures > 2|

## 6. Service level reporting

### 6.1 Availability record and customer communication

The monthly availability figure is computed from CloudWatch metrics and recorded in the compliance platform by the CEO, as the scheduled monthly compliance-platform task "Availability record (monthly)" (owner: CEO, covered by the Monday reminder email), together with:

- Overall platform availability percentage
- API performance metrics (response times, error rates)
- Incident summary with root cause analysis
- Service credit calculations (where applicable)
- Planned maintenance schedule for the coming month

Customers are notified of planned maintenance by email.

## 7. Service credits

### 7.1 Service credit calculation

|**Monthly uptime percentage**|**Service credit**|
|---|---|
|99.9 % to 99.0 %|5 % of monthly fee|
|99.0 % to 95.0 %|10 % of monthly fee|
|Below 95.0 %|25 % of monthly fee|

### 7.2 Service credit process

1. The customer submits a credit request within 30 days of the SLA breach
2. The CEO reviews and validates the claim within 5 business days
3. Approved credits are applied to the next invoice or refunded on request
4. Credit requests are tracked in the compliance platform for audit

## 8. Incident impact on SLAs

### 8.1 Incident classification

Service incidents are classified per the Incident Response Procedure:

|**Severity**|**Impact on SLA**|**Resolution target**|
|---|---|---|
|P1 (Critical)|Service unavailable|4 hours|
|P2 (High)|Degraded performance|8 hours|
|P3 (Medium)|Limited functionality|24 hours|
|P4 (Low)|Minor issues|72 hours|

P1 incidents are acknowledged by the CEO within 4 business hours, with SNS paging to the CEO on security-relevant CloudTrail events and CloudWatch alarms. Response targets for other severities are in the Incident Response Procedure.

### 8.2 Communication during incidents

- Initial notification by email after acknowledgment of a P1 incident (§8.1)
- Status updates to customers every 2 hours during an active P1 incident (the internal update cadence of every 30 minutes is set in the Incident Response Procedure)
- Root cause analysis within 48 hours of resolution
- Post-incident report sent to affected customers by email

## 9. Maintenance windows

### 9.1 Scheduled maintenance

- **Standard window**: Sunday 07:00–11:00 UTC (02:00–06:00 ET), the change window defined in the Change Management Policy
- **Notification**: 72 hours' advance notice by email
- **Emergency maintenance**: 24 hours' notice where possible
- **Tracking**: recorded in the compliance platform

### 9.2 Low-impact deployments

To minimize service impact, deployments use:

- Lambda versioned deployments with rollback via `serverless rollback`
- Rolling updates for ECS container services
- Database migrations during low-traffic periods
- CloudFront cache warming before traffic shifts

## 10. Third-party dependencies

### 10.1 Sub-processor SLAs

Third-party service levels are managed per the Vendor Management Policy:

|**Service provider**|**Service**|**Their SLA**|**Our mitigation**|
|---|---|---|---|
|AWS|Infrastructure|Per-service AWS SLAs|Lambda across availability zones; DocumentDB storage replicated across three availability zones with automatic re-creation of the instance after any failure, including an availability-zone failure; 35-day point-in-time recovery|
|PropelAuth|Authentication|PropelAuth's own published SLA|Token caching, graceful degradation|

### 10.2 Dependency monitoring

- The AWS Health Dashboard and the PropelAuth published service status are monitored for dependency availability
- Fallback mechanisms cover authentication service outages
- Lambda versioned deployments with reserved concurrency and rollback via `serverless rollback`
- Vendor performance is reviewed annually in the compliance platform, supported by the continuous monthly availability record

## 11. Continuous improvement

### 11.1 Annual SLA review

The annual SLA review, with the monthly availability record in the compliance platform as its continuous input, covers:

- SLA achievement trends
- Customer feedback
- Capacity planning based on growth projections
- Technology improvements to reliability
- Updates to monitoring and alerting thresholds

### 11.2 Performance optimization

Ongoing work to improve service levels:

- Lambda function performance tuning (reserved concurrency optimization)
- Database query optimization and indexing
- CDN configuration refinement for better cache hit ratios
- API rate limiting adjustments per the API Security and Rate Limiting Standard

## 12. Audit evidence

SLA management evidence for the SOC 2 audit:

- The monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform
- Incident records in the incident reporting module of the compliance platform
- Service credit calculations and approvals
- Customer communication records
- Maintenance window notifications

## 13. Exceptions, escalations, and review

### 13.1 Custom SLAs

A request for a custom SLA requires:

1. Business justification
2. A risk assessment per the Risk Assessment Procedure
3. A technical feasibility analysis
4. CEO approval
5. Documentation in the customer contract

### 13.2 Escalation path

1. Initial report through the standard support channels
2. Escalation to the CEO, who acknowledges critical issues within 4 business hours
3. CEO review of repeated SLA breaches
4. Management review of systemic issues, recorded in the quarterly management meeting minutes

### 13.3 Review

This policy is maintained in the compliance platform. The CEO reviews it annually against customer expectations, technical capabilities, and regulatory requirements.

## 14. Related documents

- Information Security Policy
- Business Continuity Plan
- Incident Response Procedure
- Change Management Policy
- Vendor Management Policy
- System Monitoring and Logging Procedure
- Cloud Infrastructure Security Policy
- API Security and Rate Limiting Standard
- Risk Assessment Procedure

## 15. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Processing Integrity mapping removed; authentication availability deferred to PropelAuth's own SLA; synthetic monitoring, customer-facing SLA reports and public status communications, deployment-strategy and dependency-check claims replaced by CloudWatch alarms, the monthly availability record and Lambda versioned deployments; response commitment replaced by 4-business-hour P1 acknowledgment; roles reduced to CEO / Go-to-Market Contractor; export footer removed; policy review set to annual |
