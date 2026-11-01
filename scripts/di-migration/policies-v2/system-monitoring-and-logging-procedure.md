---
title: "System Monitoring and Logging Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "mo@dealintelligence.io"
source: "system-monitoring-and-logging-procedure-v1.0.pdf"
---

# System Monitoring and Logging Procedure

## 1. Purpose

This procedure establishes comprehensive requirements for monitoring, logging, and auditing all information systems and infrastructure components at Deal Intelligence LLC. This procedure ensures continuous visibility into system operations, security events, and performance metrics to support SOC 2 Trust Services Criteria for Security (CC6.1, CC7.1), Availability (A1.2), and Confidentiality (C1.1).

This procedure operationalizes the monitoring requirements defined in the Information Security Policy and provides specific implementation guidance for AWS CloudWatch, CloudTrail, Security Hub, and related monitoring technologies across our cloud infrastructure.

## 2. Scope

This procedure applies to:

- All AWS infrastructure components including Lambda functions, Fargate containers, DocumentDB clusters, and VPC resources

- Application-level logging for the platform

- Security event monitoring and alerting systems

- Performance metrics and availability monitoring

- Audit trail generation and retention

- All personnel responsible for system administration and security monitoring

## 3. Logging Requirements

### 3.1 Mandatory Log Sources

The following systems shall generate and retain logs in accordance with this procedure:

|**System Component**|**Log Type**|**Retention Period**|**Storage Location**|
|---|---|---|---|
|AWS CloudTrail|API calls and management events|7 years|S3 bucket with KMS encryption, lifecycle to Glacier, Object Lock|
|CloudWatch Logs|Application and system logs|90 days|CloudWatch Log Groups|
|VPC Flow Logs|Network traffic metadata|90 days|CloudWatch Logs|
|DocumentDB|Database audit logs|90 days|CloudWatch Logs|
|Lambda Functions|Execution logs and errors|90 days|CloudWatch Logs|
|API Gateway|Request/response logs|90 days|CloudWatch Logs|
|Security Hub|Security findings|90 days|Security Hub console|
|PropelAuth|Authentication events|30 days|PropelAuth dashboard + CloudWatch|

### 3.2 Log Content Standards

All application logs shall include:

- Timestamp in ISO 8601 format (UTC)

- Source system identifier

- User identifier (where applicable)

- Event type and severity level

- Request/response details (with PII sanitization)

- Success/failure status

- IP address and user agent (for web requests)

Sensitive data shall be sanitized in accordance with the Data Classification and Handling Standard, ensuring no plaintext passwords, API keys, or unnecessary personal information appears in logs.

### 3.3 Audit Logging Middleware

The audit logging middleware implemented for all API requests shall capture:

- JWT token validation results from PropelAuth

- User and company context from authenticated sessions

- API endpoint accessed

- HTTP method and response status

- Request duration and performance metrics

- Rate limiting enforcement actions

Reference: API Security and Rate Limiting Standard for detailed rate limiting configurations.

## 4. Monitoring Architecture

### 4.1 CloudWatch Configuration

CloudWatch monitoring shall be configured with:

- **Metrics Collection** : 1-minute resolution for critical metrics

- **Custom Metrics** : Lambda function performance, API latency, database connections

- **Dashboards** : Real-time visibility into system health and performance

- **Metric Math** : Calculated metrics for error rates and availability percentages

### 4.2 Alarms and Thresholds

Critical alarms shall be configured for:

|**Metric**|**Threshold**|**Action**|
|---|---|---|
|API Error Rate|>5% for 5 minutes|SNS notification|
|API Latency|p95 > 2 seconds|SNS notification|
|Lambda Timeout Rate|>1% for 10 minutes|SNS notification|
|Database CPU|>80% for 15 minutes|SNS notification|
|Available Storage|<20% remaining|SNS notification|
|Failed Authentication|>10 attempts/minute|SNS security alert|
|Concurrent Executions|>80 (of 100 reserved)|SNS capacity alert|

All alarm notifications are delivered in real time via SNS to the CEO. Response targets are defined in Section 8.3.

### 4.3 Security Hub Integration

AWS Security Hub shall continuously monitor:

- Compliance with AWS Foundational Security Best Practices

- CIS AWS Foundations Benchmark adherence

- Custom security standards for SOC 2 requirements

Security findings shall trigger the automated breach detection Lambda function as defined in the Incident Response Procedure, which routes Security Hub findings to SNS. Critical findings alert in real time; all Security Hub findings are reviewed monthly and the review is recorded in the compliance platform.

## 5. Log Management Procedures

### 5.1 Log Collection

Workloads run on Lambda and Fargate. Logs shall be collected through:

- **Lambda Function Logs** : Automatic streaming to CloudWatch Logs

- **VPC Flow Logs** : Network traffic analysis and security monitoring

- **CloudTrail** : Comprehensive AWS API activity logging

- **Container Logs** : ECS and Fargate container output streams

### 5.2 Log Aggregation and Correlation

Log aggregation shall utilize:

- CloudWatch Logs Insights for query and analysis

- Metric filters for extracting metrics from log data

- Time-synchronized correlation across multiple log sources

### 5.3 Log Protection

Log integrity and confidentiality shall be ensured through:

- KMS encryption for logs at rest as specified in Encryption and Cryptographic Controls Standard

- IAM policies restricting log access to authorized personnel only

- CloudTrail log file validation for tamper detection

- S3 bucket versioning and MFA delete protection

- CloudTrail bucket lifecycle policy and S3 Object Lock for 7-year compliance retention

## 6. Performance Monitoring

### 6.1 Availability Monitoring

To maintain the 99.9% uptime SLA commitment:

- CloudWatch alarms on API errors and latency (p95 > 2 seconds)

- Route 53 is used for DNS only; the platform runs in a single region (us-east-1) by design, as stated in the Business Continuity Plan

- API endpoint monitoring with response time thresholds

- Database cluster health monitoring

- Monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform

Reference: Service Level Agreement (SLA) Management Policy for detailed SLA requirements.

### 6.2 Resource Utilization

Monitor and track:

- Lambda function duration and concurrency utilization

- DocumentDB connection pool usage

- API Gateway request rates and throttling

- CloudFront cache hit ratios

- S3 request metrics and data transfer

### 6.3 Capacity Planning

Quarterly capacity reviews shall analyze:

- Historical usage trends and growth patterns

- Reserved concurrency utilization (current: 100)

- Database storage growth projections

- Cost optimization opportunities

- Performance bottleneck identification

## 7. Security Monitoring

### 7.1 Threat Detection

Continuous security monitoring shall include:

- Failed authentication attempt patterns

- Unusual API access patterns

- Privilege escalation attempts

- Data exfiltration indicators

- Vulnerability scanning results from ECR image scans

### 7.2 Automated Security Response

The automated breach detection Lambda function shall:

- Process Security Hub findings in real-time

- Trigger SNS notifications for high-severity events

- Support the recording of resulting incidents in the compliance platform Incident Reporting system by the CEO

### 7.3 Compliance Monitoring

Continuous compliance validation through:

- CloudFormation (`serverless deploy`) as the only change path, reporting configuration drift

- Security Hub configuration checks and compliance scores

- Scheduled Lambda checks (access review, retention enforcement)

- Automated policy violation detection

- The compliance platform as the control register (controls, evidence, tasks), with the monthly recorded review of Security Hub findings

Reference: Vulnerability Management Procedure for vulnerability scanning and remediation processes.

## 8. Alert Management

### 8.1 Alert Routing

Alerts shall be routed based on severity:

- **Critical** : Immediate SNS notification to the CEO

- **High** : SNS notification to the CEO

- **Medium** : Included in the monthly recorded review

- **Low** : Included in the monthly recorded review

### 8.2 Alert Suppression

To prevent alert fatigue:

- Maintenance windows shall suppress non-critical alerts

- Duplicate alert detection and consolidation

- Alert throttling for known issues under investigation

- Automated acknowledgment for expected events

### 8.3 Response Targets

Alerts shall be handled according to:

- Critical alerts and findings: delivered in real time via SNS; a resulting P1 incident is acknowledged by the CEO within 4 business hours per the Incident Response Procedure

- High alerts: reviewed by the CEO and, where an incident is declared, handled per the Incident Response Procedure

- Medium and low alerts: addressed in the monthly recorded review

- The CEO is the incident commander for all escalations

## 9. Log Analysis and Reporting

### 9.1 Regular Analysis

Log analysis activities shall include:

- Real-time SNS alerting on critical security alerts and anomalies, with a monthly recorded review of all security findings

- Weekly performance trend analysis

- Monthly access pattern reviews

- Quarterly security posture assessments

### 9.2 Reporting Requirements

Regular reports shall be generated for:

- **Executive Dashboard** : Monthly KPIs and security metrics

- **Compliance Reports** : Quarterly SOC 2 evidence collection

- **Incident Reports** : As required per Incident Response Procedure

- **Availability Reports** : Monthly availability figure computed from CloudWatch metrics and recorded in the compliance platform

### 9.3 Forensic Analysis Capabilities

Maintain forensic readiness through:

- Retention of logs and evidence relating to security incidents for 7 years

- Log export capabilities for external analysis

- Chain of custody procedures for evidence handling

- Integration with incident response workflows

## 10. Access Control for Monitoring Systems

### 10.1 Privileged Access

Access to monitoring and logging systems shall be:

- Restricted to the CEO

- Authenticated to the AWS console and CLI with MFA enforced

- Logged and audited for all administrative actions

- Reviewed quarterly as part of access reviews

Reference: Access Control and Authentication Policy for detailed access control requirements.

### 10.2 Read-Only Access

Read-only access may be granted for:

- The external SOC 2 auditor during assessments

- Third-party security assessors

- Temporary access with automatic expiration

## 11. Integration with Other Processes

### 11.1 Change Management Integration

All changes to monitoring configurations shall:

- Follow the Change Management Policy

- Include monitoring updates in change requests

- Validate monitoring functionality post-deployment

- Update alert thresholds based on new baselines

### 11.2 Incident Response Integration

Monitoring systems shall support incident response by:

- Providing real-time alerts for security events

- Maintaining forensic data for investigation

- Enabling rapid incident detection and containment

- Generating evidence for post-incident reviews

### 11.3 Business Continuity Integration

Support business continuity through:

- Monitoring backup job completion

- Tracking recovery point objectives (RPO)

- Validating failover mechanism health

- Testing disaster recovery procedures

Reference: Business Continuity Plan for detailed continuity requirements.

## 12. Compliance and Audit Support

### 12.1 Evidence Collection

Monitoring systems shall provide evidence for:

- SOC 2 Type II audit requirements

- GDPR and CCPA compliance validation

- Security control effectiveness

- SLA performance verification

### 12.2 Audit Trail Requirements

Maintain comprehensive audit trails including:

- User activity logs with session tracking

- System configuration changes

- Data access and modification records

- Security event correlation

### 12.3 Retention Compliance

Log retention shall comply with:

- SOC 2 requirements (90-day minimum for CloudWatch Logs; 7 years for CloudTrail)

- GDPR data minimization principles

- CCPA consumer rights obligations

- Business requirements for forensic analysis

Reference: Data Retention and Disposal Policy for detailed retention schedules.

## 13. Monitoring Tools and Technologies

### 13.1 Primary Monitoring Stack

- **AWS CloudWatch** : Core monitoring and logging platform

- **AWS CloudTrail** : API activity and compliance logging

- **AWS Security Hub** : Security posture management and configuration checks

- **AWS CloudFormation** : Configuration drift reporting via `serverless deploy`

- **PropelAuth** : Authentication event monitoring

### 13.2 Supporting Technologies

- **CloudWatch Logs Insights** : Log query and analysis

- **CloudWatch Alarms** : Availability and latency monitoring

- **AWS X-Ray** : Distributed tracing (when implemented)

- **Container Insights** : ECS and Fargate monitoring

- **VPC Flow Logs** : Network traffic analysis

### 13.3 Integration Points

- **The compliance platform Incident Reporting** : Security incident documentation

- **SNS Topics** : Alert distribution and notification

- **Lambda Functions** : Breach detection and scheduled checks (access review, retention enforcement)

- **S3 Buckets** : Long-term CloudTrail log archival (7 years, Object Lock)

- **EventBridge** : Event-driven automation

## 14. Roles and Responsibilities

### 14.1 Chief Executive Officer (CEO)

- Define monitoring strategy and requirements

- Review security alerts and trends

- Approve monitoring configuration changes

- Ensure compliance with SOC 2 requirements

- Configure and maintain monitoring systems

- Respond to operational alerts

- Perform the monthly recorded review of security findings and alerts

- Generate compliance reports

- Implement application-level logging

- Define custom metrics and alarms

- Maintain logging standards in code

### 14.2 All Personnel (including the Go-to-Market Contractor)

- Report suspicious activities or anomalies to the CEO

- Comply with logging requirements

- Protect log data confidentiality

- Support audit and compliance activities

## 15. Exceptions and Deviations

Any exceptions to monitoring requirements must be:

- Documented with business justification

- Risk assessed for security impact

- Approved by the CEO

- Reviewed quarterly for continued necessity

- Tracked in the Risk Assessment module in the compliance platform

## 16. Related Documents

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

## 17. Review and Updates

This procedure shall be reviewed annually and updated to reflect:

- Changes in monitoring technologies

- Emerging threat landscapes

- Compliance requirement updates

- Lessons learned from incidents

- Infrastructure architecture changes

## 18. Revision history

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | November 13, 2025 | mo@dealintelligence.io | Initial audited release |
| 2.0 | <to be set at publication> | mo@dealintelligence.io | Roles reduced to CEO / all personnel; Processing Integrity mapping removed; CloudTrail retention corrected to 7 years; instance-agent, DNS health-check, synthetic-monitoring, configuration-compliance, cross-account and scaling claims removed in favor of the controls in place; daily alert review replaced by real-time SNS alerting plus a monthly recorded review; response targets aligned with the Incident Response Procedure |
