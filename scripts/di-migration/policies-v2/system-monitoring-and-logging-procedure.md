---
title: "System Monitoring and Logging Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "system-monitoring-and-logging-procedure-v1.0.pdf"
---

# System Monitoring and Logging Procedure

## 1. Purpose

This procedure sets the monitoring, logging, and audit requirements for all information systems and infrastructure components at Deal Intelligence LLC. It gives continuous visibility into system operations, security events, and performance, and supports the SOC 2 Trust Services Criteria for Security (CC6.1, CC7.1), Availability (A1.2), and Confidentiality (C1.1).

It implements the monitoring requirements of the Information Security Policy for CloudWatch, CloudTrail, the configuration-check and breach-detection Lambda functions, and the related monitoring services in the AWS infrastructure.

## 2. Scope

This procedure applies to:

- All AWS infrastructure components, including Lambda functions, Fargate containers, DocumentDB clusters, and VPC resources
- Application-level logging for the platform
- Security event monitoring and alerting
- Performance and availability monitoring
- Audit trail generation and retention
- All personnel responsible for system administration and security monitoring

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

- Defines the monitoring strategy and requirements
- Configures and maintains the monitoring systems
- Implements application-level logging and maintains the logging standards in code
- Defines custom metrics and alarms
- Approves monitoring configuration changes
- Responds to operational alerts
- Reviews security alerts and trends, and performs the monthly recorded review of the configuration-check record and security alerts
- Generates compliance reports and maintains the SOC 2 evidence

### 3.2 All personnel (including the Go-to-Market Contractor)

- Report suspicious activity or anomalies to the CEO
- Comply with the logging requirements
- Protect the confidentiality of log data
- Support audit and compliance activities

## 4. Logging requirements

### 4.1 Mandatory log sources

The following systems generate and retain logs under this procedure:

|**System component**|**Log type**|**Retention period**|**Storage location**|
|---|---|---|---|
|CloudTrail|API calls and management events|7 years|S3 bucket with KMS encryption, lifecycle to Glacier, Object Lock|
|CloudWatch Logs|Application and system logs|90 days|CloudWatch log groups|
|VPC Flow Logs|Network traffic metadata|90 days|CloudWatch Logs|
|Lambda functions|Execution logs and errors|90 days|CloudWatch Logs|
|CloudFront and Lambda function URLs|Request/response logs|90 days|CloudWatch Logs|
|Configuration-check Lambda|Monthly pass/fail configuration-check records|7 years (as compliance evidence)|Compliance platform|
|PropelAuth|Authentication events|30 days|PropelAuth dashboard + CloudWatch|

### 4.2 Log content

All application logs include:

- Timestamp in ISO 8601 format (UTC)
- Source system identifier
- User identifier (where one exists)
- Event type and severity level
- Request/response details (with PII sanitization)
- Success/failure status
- IP address and user agent (for web requests)

Sensitive data is sanitized per the Data Classification and Handling Standard: no plaintext passwords, API keys, or unnecessary personal information appear in logs.

### 4.3 Audit logging middleware

The audit logging middleware on all API requests captures:

- JWT token validation results from PropelAuth
- User and company context from the authenticated session
- API endpoint accessed
- HTTP method and response status
- Request duration and performance metrics
- Rate-limiting enforcement actions

Rate-limiting configuration is in the API Security and Rate Limiting Standard.

## 5. Monitoring architecture

### 5.1 CloudWatch configuration

- **Metrics collection**: 1-minute resolution for critical metrics
- **Custom metrics**: Lambda function performance, API latency, database connections
- **Dashboards**: real-time view of system health and performance
- **Metric math**: calculated metrics for error rates and availability percentages

### 5.2 Alarms and thresholds

|**Metric**|**Threshold**|**Action**|
|---|---|---|
|API error rate|>5 % for 5 minutes|SNS notification|
|API latency|p95 > 2 seconds|SNS notification|
|Lambda timeout rate|>1 % for 10 minutes|SNS notification|
|Database CPU|>80 % for 15 minutes|SNS notification|
|Available storage|<20 % remaining|SNS notification|
|Failed authentication|>10 attempts/minute|SNS security alert|
|Concurrent executions|>80 (of 100 reserved)|SNS capacity alert|

All alarm notifications are delivered in real time via SNS to the CEO. Response targets are in §9.3.

### 5.3 Configuration checks and security event alerting

A scheduled configuration-check Lambda runs monthly against a fixed checklist:

- CloudTrail enabled and log-file validation on
- No public S3 buckets
- No security groups open to 0.0.0.0/0 on administrative ports
- Root account MFA
- IAM password policy
- KMS key rotation
- ECR scan-on-push
- DocumentDB backup retention and Multi-AZ

The Lambda posts a dated pass/fail record to the compliance platform; the CEO reviews the record monthly and remediates failed checks.

Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) trigger an EventBridge rule that invokes the breach-detection Lambda function defined in the Incident Response Procedure, which sends an SNS alert to the CEO in real time.

## 6. Log management

### 6.1 Log collection

Workloads run on Lambda and Fargate. Logs are collected through:

- **Lambda function logs**: automatic streaming to CloudWatch Logs
- **VPC Flow Logs**: network traffic analysis and security monitoring
- **CloudTrail**: AWS API activity logging
- **Container logs**: ECS and Fargate container output streams

### 6.2 Log aggregation and correlation

- CloudWatch Logs Insights for query and analysis
- Metric filters to extract metrics from log data
- Time-synchronized correlation across log sources

### 6.3 Log protection

Log integrity and confidentiality are protected through:

- KMS encryption of logs at rest, per the Encryption and Cryptographic Controls Standard
- IAM policies restricting log access to authorized personnel
- CloudTrail log file validation for tamper detection
- S3 bucket versioning
- CloudTrail bucket lifecycle policy and S3 Object Lock for the 7-year retention

## 7. Performance monitoring

### 7.1 Availability monitoring

To maintain the 99.9 % uptime SLA:

- CloudWatch alarms on API errors and latency (p95 > 2 seconds)
- Route 53 is used for DNS only; the platform runs in a single region (us-east-1) by design, as stated in the Business Continuity Plan
- API endpoint monitoring with response time thresholds
- Database cluster health monitoring
- A monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform

SLA requirements are in the Service Level Agreement (SLA) Management Policy.

### 7.2 Resource utilization

The CEO monitors:

- Lambda function duration and concurrency utilization
- DocumentDB connection pool usage
- CloudFront request rates and middleware rate-limit rejections
- CloudFront cache hit ratios
- S3 request metrics and data transfer

## 8. Security monitoring

### 8.1 Threat detection

Continuous security monitoring covers:

- Failed authentication attempt patterns
- Unusual API access patterns
- Privilege escalation attempts
- Data exfiltration indicators
- Vulnerability scanning results from ECR image scans

### 8.2 Automated security response

The breach-detection Lambda function:

- Is triggered in real time by an EventBridge rule on security-relevant CloudTrail events
- Triggers SNS notifications for high-severity events
- Supports the CEO in recording resulting incidents in the incident reporting module of the compliance platform

### 8.3 Compliance monitoring

- CloudFormation (`serverless deploy`) is the only change path and reports configuration drift
- Scheduled Lambda checks (monthly configuration check, access review, retention enforcement)
- Automated policy violation detection
- The compliance platform as the control register (controls, evidence, tasks), holding the monthly configuration-check record and its review

Vulnerability scanning and remediation are in the Vulnerability Management Procedure.

## 9. Alert management

### 9.1 Alert routing

- **Critical**: immediate SNS notification to the CEO
- **High**: SNS notification to the CEO
- **Medium**: included in the monthly recorded review
- **Low**: included in the monthly recorded review

### 9.2 Alert suppression

To prevent alert fatigue:

- Maintenance windows suppress non-critical alerts
- Duplicate alerts are detected and consolidated
- Alerts for known issues under investigation are throttled
- Expected events are acknowledged automatically

### 9.3 Response targets

- Critical alerts and findings are delivered in real time via SNS; a resulting P1 incident is acknowledged by the CEO within 4 business hours per the Incident Response Procedure
- High alerts are reviewed by the CEO and, where an incident is declared, handled per the Incident Response Procedure
- Medium and low alerts are addressed in the monthly recorded review
- The CEO is the incident commander for all escalations

## 10. Log analysis and reporting

### 10.1 Regular analysis

- Real-time SNS alerting on critical security alerts and anomalies, with a monthly recorded review of the configuration-check record and security alerts

### 10.2 Reports

- **Incident reports**: as required by the Incident Response Procedure
- **Availability reports**: the monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform

### 10.3 Forensic readiness

- Logs and evidence relating to security incidents are retained for 7 years
- Logs can be exported for external analysis
- Chain-of-custody procedures apply to evidence handling
- Monitoring output feeds the incident response workflow

## 11. Access to monitoring systems

### 11.1 Privileged access

Access to monitoring and logging systems is:

- Restricted to the CEO
- Authenticated to the AWS console and CLI with MFA enforced
- Logged and audited for all administrative actions
- Reviewed quarterly as part of the access reviews

Access control requirements are in the Access Control and Authentication Policy.

### 11.2 Read-only access

Read-only access may be granted, with automatic expiration, to:

- The external SOC 2 auditor during assessments
- Third-party security assessors

## 12. Integration with other processes

### 12.1 Change management

Changes to monitoring configurations follow the Change Management Policy. Change requests include the monitoring updates; monitoring is validated after deployment and alert thresholds are updated to the new baselines.

### 12.2 Business continuity

Monitoring supports the Business Continuity Plan by:

- Monitoring backup job completion
- Tracking the recovery point objective (RPO)
- Validating failover health
- Supporting disaster recovery tests

### 12.3 Retention

Log retention follows the Data Retention and Disposal Policy (CloudWatch Logs 90 days; CloudTrail 7 years; incident evidence 7 years).

## 13. Monitoring tools

### 13.1 Primary monitoring stack

- **CloudWatch**: core monitoring and logging platform
- **CloudTrail**: API activity and compliance logging
- **Configuration-check Lambda**: monthly AWS configuration checks against a fixed checklist
- **Breach-detection Lambda**: real-time alerting on security-relevant CloudTrail events via EventBridge and SNS
- **CloudFormation**: configuration drift reporting via `serverless deploy`
- **PropelAuth**: authentication event monitoring

### 13.2 Supporting technologies

- **CloudWatch Logs Insights**: log query and analysis
- **CloudWatch alarms**: availability and latency monitoring
- **AWS X-Ray**: distributed tracing (when implemented)
- **Container Insights**: ECS and Fargate monitoring
- **VPC Flow Logs**: network traffic analysis

### 13.3 Integration points

- **Compliance platform incident reporting module**: security incident documentation
- **SNS topics**: alert distribution and notification
- **Lambda functions**: breach detection and scheduled checks (monthly configuration check, access review, retention enforcement)
- **S3 buckets**: long-term CloudTrail log archival (7 years, Object Lock)
- **EventBridge**: event-driven automation

## 14. Exceptions and review

### 14.1 Exceptions

An exception to the monitoring requirements is:

- Documented with its business justification
- Risk-assessed for security impact
- Approved by the CEO
- Tracked in the risk assessment module of the compliance platform

### 14.2 Review

The CEO reviews this procedure annually and updates it for:

- Changes in monitoring technologies
- Emerging threats
- Compliance requirement updates
- Lessons learned from incidents
- Infrastructure architecture changes

## 15. Related documents

- Information Security Policy
- Incident Response Procedure
- Access Control and Authentication Policy
- Data Classification and Handling Standard
- Vulnerability Management Procedure
- Change Management Policy
- Business Continuity Plan
- Cloud Infrastructure Security Policy
- Encryption and Cryptographic Controls Standard
- Service Level Agreement (SLA) Management Policy
- Data Retention and Disposal Policy
- API Security and Rate Limiting Standard

## 16. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial audited release |
| 2.0 | <to be set at publication> | Mo Messidi | Roles reduced to CEO / all personnel; Processing Integrity mapping removed; CloudTrail retention corrected to 7 years; instance-agent, DNS health-check, synthetic-monitoring, configuration-compliance, cross-account and scaling claims removed in favor of the controls in place; daily alert review replaced by real-time SNS alerting plus a monthly recorded review; response targets aligned with the Incident Response Procedure |
