---
title: "Incident Response Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "incident-response-procedure-v1.0.pdf"
---

# Incident Response Procedure

## 1. Purpose

This procedure sets out how Deal Intelligence LLC detects, responds to, and recovers from security incidents that could affect its platform, customer data, or service commitments. It provides for rapid containment, thorough investigation, and effective remediation in compliance with SOC 2 Trust Services Criteria CC7.3–CC7.5 (incident response), GDPR Article 33, and CCPA Section 1798.150.

The procedure implements the incident response requirements of the Information Security Policy and works with the Risk Assessment Procedure for post-incident risk evaluation. It uses the automated detection capabilities (CloudTrail event alerting through EventBridge and the Lambda-based breach detection, plus the monthly configuration-check record) to meet the 48-hour customer notification commitment.

## 2. Scope

This procedure applies to all security events and incidents affecting:

- AWS cloud infrastructure components documented in the CloudFormation stack di-backend-api-prod
- Business contact information and customer account data as classified in the Data Classification and Handling Standard
- PropelAuth authentication services and AWS infrastructure services
- API endpoints, Lambda functions, and Fargate containers
- DocumentDB instances and data processing operations
- Third-party integrations and customer-controlled systems

The procedure covers incidents across the Trust Services Criteria in scope: Security, Availability, and Confidentiality.

## 3. Definitions

**Security event**: Any observable occurrence in a system or network that may indicate a potential security incident.

**Security incident**: A confirmed event that compromises the confidentiality, integrity, or availability of information assets or violates security policies.

**Data breach**: An incident resulting in unauthorized access to, disclosure of, or loss of business contact information or customer account data.

**Incident severity levels**:

- **P1 (Critical)**: Service-wide outage, confirmed data breach, or complete loss of a security control affecting multiple customers
- **P2 (High)**: Partial service degradation, suspected data breach, or security control failure affecting limited customers
- **P3 (Medium)**: Minor service impact, security vulnerability identified, or isolated control failure
- **P4 (Low)**: No customer impact, informational security event, or threat intelligence

**Incident Commander**: The Chief Executive Officer (CEO), who declares, leads, and closes incidents.

**Root cause analysis (RCA)**: Systematic investigation to identify the underlying cause of an incident and prevent recurrence.

**Evidence preservation**: Collection and protection of digital artifacts for forensic analysis and regulatory compliance.

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (Incident Commander)

The CEO:

- Declares incident severity and activates the response procedures
- Authorizes emergency changes per the Change Management Policy
- Approves external communications and breach notifications
- Determines regulatory notification obligations under GDPR and CCPA
- Conducts post-incident reviews for P1 and P2 incidents
- Leads technical investigation and containment
- Coordinates with AWS Support on infrastructure incidents
- Documents the incident timeline and actions in the compliance platform's Incident Reporting system
- Performs forensic analysis using CloudWatch logs and CloudTrail
- Implements remediation measures and validates their effectiveness
- Updates the risk register per the Risk Assessment Procedure
- Executes containment and recovery procedures
- Collects and preserves technical evidence
- Implements emergency patches and configuration changes
- Monitors system behavior after remediation
- Updates CloudFormation templates and documentation

### 4.2 All personnel

All personnel:

- Report suspected security incidents immediately via the designated channels
- Preserve potential evidence and avoid system modifications
- Cooperate with incident investigations
- Maintain confidentiality regarding incident details

## 5. Incident response process

### 5.1 Preparation

#### 5.1.1 Incident response readiness

This procedure, together with the Business Continuity Plan and the severity matrix in section 7, is the response reference for the common scenarios:

- Data breach response
- Ransomware or malware infection
- DDoS attack mitigation
- Insider threat investigation
- Service availability disruption
- Authentication system compromise

#### 5.1.2 Detection capabilities

Automated detection systems:

- Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes), which trigger an EventBridge rule → the breach-detection Lambda → SNS alert to the CEO in real time
- The Lambda-based breach detection function, monitoring for:
  - Unusual data access patterns
  - Failed authentication attempts exceeding thresholds
  - Unauthorized API usage
  - Database query anomalies
- CloudWatch alarms for service degradation
- Container vulnerability scanning alerts from ECR
- The monthly configuration-check Lambda, whose dated pass/fail record in the compliance platform surfaces configuration drift (public S3 buckets, open security groups, disabled CloudTrail, and the other checklist items) for review

#### 5.1.3 Communication channels

- Primary: SNS security alerts to designated mobile devices
- Escalation: Direct phone contact for P1 incidents
- Customer notifications: Email via the established communication channels

### 5.2 Detection and analysis

#### 5.2.1 Initial detection

On detection of a potential security event through automated monitoring or manual reporting:

1. **Event triage** (P1 events acknowledged within 4 business hours; other severities per section 7.1)
   - Review the SNS alert and the triggering CloudTrail event, or the failed configuration-check item
   - Query CloudWatch logs for related events
   - Check CloudTrail for unauthorized API calls
   - Assess potential customer impact
2. **Incident declaration** (on completion of triage)
   - Determine whether the event constitutes an incident
   - Assign the initial severity level
   - Create the incident record in the compliance platform's Incident Reporting system
   - The CEO assumes the Incident Commander role for P1 and P2 incidents

#### 5.2.2 Incident analysis

1. **Scope determination**
   - Identify affected systems from the CloudFormation documentation
   - Determine data exposure using the Data Classification and Handling Standard
   - Assess the number of affected customers
   - Evaluate regulatory notification requirements
2. **Evidence collection**
   - Export CloudWatch logs (90-day retention available)
   - Capture CloudTrail audit logs
   - Preserve Lambda function logs and execution history
   - Document API request logs from the audit middleware
   - Capture the SNS alert, the triggering CloudTrail event record, and the configuration-check record where relevant
   - Collect container logs from Fargate
3. **Impact assessment**
   - Business contact information exposure analysis
   - Service availability metrics against the 99.9 % SLA
   - Data integrity validation
   - Compliance implications under GDPR and CCPA

### 5.3 Containment, eradication, and recovery

#### 5.3.1 Containment strategies

Immediate containment (P1 and P2):

- Isolate affected Lambda functions or containers
- Revoke compromised IAM credentials
- Block malicious IP addresses via security groups
- Disable affected user accounts in PropelAuth
- Tighten API rate limiting in middleware and restrict origin access at CloudFront

Short-term containment (P3 and P4):

- Apply temporary security group restrictions
- Increase CloudWatch monitoring thresholds
- Enable additional logging verbosity
- Adjust rate limiting per the API Security and Rate Limiting Standard

#### 5.3.2 Eradication

1. **Root cause elimination**
   - Remove malicious code or configurations
   - Patch identified vulnerabilities per the Vulnerability Management Procedure
   - Update security group rules and NACLs
   - Rotate compromised credentials and API keys
   - Update KMS key policies if necessary
2. **System hardening**
   - Apply security patches to the Lambda runtime
   - Update container base images in ECR
   - Strengthen IAM policies per the Access Control and Authentication Policy
   - Review and update CloudFormation security parameters

#### 5.3.3 Recovery

1. **Service restoration**
   - Follow the rollback procedures in the Change Management Policy
   - Restore from backups if data integrity is compromised
   - Validate system functionality through health checks
   - Confirm the DocumentDB instance status is available
   - Verify the CloudFront distribution configuration
2. **Monitoring enhancement**
   - Increase monitoring sensitivity for affected components
   - Deploy additional CloudWatch alarms
   - Enable detailed CloudTrail logging
   - Implement compensating controls as needed

### 5.4 Post-incident activity

#### 5.4.1 Lessons learned (within 5 business days)

1. **Incident review**
   - Timeline reconstruction
   - Decision effectiveness analysis
   - Communication assessment
   - Tool and process evaluation
2. **Root cause analysis documentation**
   - Technical root cause identification
   - Contributing factors analysis
   - Control failure assessment
   - Process gap identification
3. **Improvement actions**
   - Update this procedure
   - Extend the CloudTrail-EventBridge rule or the configuration-check checklist
   - Modify the Lambda breach detection logic
   - Update the risk register per the Risk Assessment Procedure
   - Schedule security awareness training per the Security Awareness Training Program

#### 5.4.2 Documentation and reporting

- Complete the incident report in the compliance platform's Incident Reporting system
- Update incident metrics
- Archive evidence in the encrypted S3 evidence bucket
- Generate compliance reports for SOC 2 audit evidence

## 6. Communication protocols

### 6.1 Internal communications

During an incident, the incident record is updated:

- Every 30 minutes for P1 incidents
- Hourly for P2 incidents
- Daily for P3 and P4 incidents

These are internal update intervals. Customer-facing status updates follow the Service Level Agreement (SLA) Management Policy (every 2 hours for P1 incidents).

Communication methods:

- SNS notifications for automated alerts
- Direct phone contact for P1 incidents
- The incident record in the compliance platform's Incident Reporting system

### 6.2 External communications

#### 6.2.1 Customer notifications

Data breach notification (within 48 hours):

- Nature of the incident and data affected
- Potential impact on customer operations
- Mitigation measures implemented
- Recommended customer actions
- Contact information for questions

Service disruption notification (status updates every 2 hours for P1 incidents, per the Service Level Agreement (SLA) Management Policy):

- Expected resolution timeframe
- Workaround procedures, if available
- Updates on restoration progress
- Post-incident report availability

#### 6.2.2 Regulatory notifications

GDPR (within 72 hours):

- Notify the supervisory authority of personal data breaches
- Document the justification for any delayed notification
- Provide breach details per Article 33

CCPA:

- Notify affected California residents without unreasonable delay
- Provide breach details per Section 1798.150

#### 6.2.3 Third-party notifications

- AWS Support for infrastructure-related incidents
- PropelAuth for authentication system incidents

## 7. Incident classification and prioritization

### 7.1 Severity matrix

| Severity | Customer impact | Data impact | Service impact | Acknowledgement target | Handling |
|---|---|---|---|---|---|
| P1 (Critical) | Multiple customers affected | Confirmed data breach | Complete service outage | 4 business hours | Real-time CloudTrail-EventBridge/SNS alert to the CEO; Incident Commander role activated |
| P2 (High) | Single customer affected | Suspected data breach | Partial service degradation | 1 business day | Real-time CloudTrail-EventBridge/SNS alert to the CEO; Incident Commander role activated |
| P3 (Medium) | No direct customer impact | Data integrity concerns | Minor feature unavailability | 5 business days | Handled by the CEO; recorded in the compliance platform |
| P4 (Low) | No customer impact | No data impact | No service impact | Monthly configuration-check review | Reviewed by the CEO when the monthly configuration-check record is posted |

### 7.2 Escalation triggers

- Evidence of a deliberate attack or insider threat
- Media or public attention
- Regulatory inquiry or investigation
- Customer data exposure exceeding 100 records
- Service degradation breaching the 99.9 % SLA commitment

## 8. Evidence management

### 8.1 Evidence collection requirements

- Maintain chain-of-custody documentation
- Use write-once storage for critical evidence
- Apply legal hold when required
- Verify evidence integrity through checksums
- Document collection methods and timestamps

### 8.2 Evidence retention

- Security incident evidence: 7 years
- Data breach evidence: 7 years
- Regulatory investigation evidence: until the investigation is closed, and no less than 7 years
- Routine event logs: 90 days per standard retention

### 8.3 Evidence storage

- Primary: S3 bucket with versioning
- Encryption: KMS customer-managed keys
- Access: restricted to the CEO
- Backup: S3 versioning within the single region (us-east-1)

## 9. Testing and maintenance

### 9.1 Incident response testing

Annual tabletop exercise (recorded in the compliance platform):

- Scenario-based discussion
- Decision-making evaluation
- Communication protocol validation
- Documentation review
- Customer communication practice
- Recovery procedure validation (the Business Continuity Plan full test record)

### 9.2 Procedure maintenance

- Annual review and update of this procedure
- Updates based on lessons learned
- Integration with updates to related policies and procedures

## 10. Metrics and reporting

### 10.1 Key performance indicators

- Mean time to detect (MTTD): security-relevant CloudTrail events alerted in real time via EventBridge/SNS
- Mean time to acknowledge (MTTA): target < 4 business hours for P1
- Mean time to resolve (MTTRes): target < 24 hours
- Customer notification compliance: 100 % within 48 hours
- Post-incident review completion: 100 % within 5 business days

### 10.2 Reporting requirements

- Quarterly trend analysis for risk assessment updates, recorded in the management meeting minutes
- Annual incident response program review
- SOC 2 audit evidence compilation
- Regulatory compliance reporting as required

## 11. Integration with business continuity

This procedure coordinates with the Business Continuity Plan for incidents requiring:

- Disaster recovery activation
- Recovery of the DocumentDB instance or point-in-time restore
- Extended service disruption management
- Crisis communication protocols
- Backup restoration procedures

The recovery time objectives (RTO) and recovery point objectives (RPO) defined in the Business Continuity Plan guide recovery prioritization during major incidents.

## 12. Related documents

- Information Security Policy
- Access Control and Authentication Policy
- API Security and Rate Limiting Standard
- Business Continuity Plan
- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Classification and Handling Standard
- Privacy Notice and Data Processing Agreement Template
- Risk Assessment Procedure
- Security Awareness Training Program
- Service Level Agreement (SLA) Management Policy
- System Monitoring and Logging Procedure
- Vulnerability Management Procedure

## 13. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial procedure |
| 2.0 | <to be set at publication> | Mo Messidi | Scope limited to Security, Availability, and Confidentiality; CEO as Incident Commander; annual tabletop exercise; P1 acknowledgement within 4 business hours; 7-year evidence retention; containment, communication, and evidence-storage controls restated to the deployed environment |
