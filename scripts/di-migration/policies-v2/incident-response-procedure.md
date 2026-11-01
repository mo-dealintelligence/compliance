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

This Incident Response Procedure establishes the systematic approach for detecting, responding to, and recovering from security incidents that could impact Deal Intelligence LLC's platform, customer data, or service commitments. The procedure ensures rapid containment, thorough investigation, and effective remediation of incidents while maintaining compliance with SOC 2 Trust Services Criteria CC7.3-CC7.5 (Incident Response) and regulatory requirements under GDPR Article 33 and CCPA Section 1798.150.

This procedure operationalizes the incident response requirements defined in the Information Security Policy and integrates with the Risk Assessment Procedure for post-incident risk evaluation. The procedure leverages Deal Intelligence's automated detection capabilities including Security Hub findings and Lambda-based breach detection to maintain the 48-hour customer notification commitment.

## 2. Scope

This procedure applies to all security events and incidents affecting:

- AWS cloud infrastructure components documented in CloudFormation stack di-backend-api-prod

- Business contact information and customer account data as classified in the Data Classification and Handling Standard

- PropelAuth authentication services and AWS infrastructure services

- API endpoints, Lambda functions, and Fargate containers

- DocumentDB instances and data processing operations

- Third-party integrations and customer-controlled systems

The procedure encompasses incidents across the Trust Services Criteria in scope: Security, Availability, and Confidentiality.

## 3. Definitions

**Security Event**: Any observable occurrence in a system or network that may indicate a potential security incident.

**Security Incident**: A confirmed event that compromises the confidentiality, integrity, or availability of information assets or violates security policies.

**Data Breach**: An incident resulting in unauthorized access to, disclosure of, or loss of business contact information or customer account data.

**Incident Severity Levels**:

- **Critical (P1)**: Service-wide outage, confirmed data breach, or complete loss of security control affecting multiple customers

- **High (P2)**: Partial service degradation, suspected data breach, or security control failure affecting limited customers

- **Medium (P3)**: Minor service impact, security vulnerability identified, or isolated control failure

- **Low (P4)**: No customer impact, informational security event, or proactive threat intelligence

**Incident Commander**: The Chief Executive Officer (CEO), who declares, leads, and closes incidents.

**Root Cause Analysis (RCA)**: Systematic investigation to identify the underlying cause of an incident and prevent recurrence.

**Evidence Preservation**: Collection and protection of digital artifacts for forensic analysis and regulatory compliance.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer (Incident Commander)

- Declare incident severity and activate response procedures

- Authorize emergency changes per Change Management Policy

- Approve external communications and breach notifications

- Determine regulatory notification obligations under GDPR and CCPA

- Conduct post-incident reviews for Critical and High severity incidents

- Lead technical investigation and containment activities

- Coordinate with AWS Support for infrastructure incidents

- Document incident timeline and actions in the compliance platform's Incident Reporting system

- Perform forensic analysis using CloudWatch logs and CloudTrail

- Implement remediation measures and validate effectiveness

- Update risk register per Risk Assessment Procedure

- Execute containment and recovery procedures

- Collect and preserve technical evidence

- Implement emergency patches and configuration changes

- Monitor system behavior post-remediation

- Update CloudFormation templates and documentation

### 4.2 All Personnel

- Report suspected security incidents immediately via designated channels

- Preserve potential evidence and avoid system modifications

- Cooperate with incident investigation activities

- Maintain confidentiality regarding incident details

## 5. Incident Response Process

### 5.1 Preparation Phase

#### 5.1.1 Incident Response Readiness

This procedure, together with the Business Continuity Plan and the severity matrix in Section 7, is the response reference for common scenarios:

- Data breach response

- Ransomware/malware infection

- DDoS attack mitigation

- Insider threat investigation

- Service availability disruption

- Authentication system compromise

#### 5.1.2 Detection Capabilities

**Automated Detection Systems**:

- Security Hub findings aggregation and alerting

- Lambda-based breach detection function monitoring for:

  - Unusual data access patterns

  - Failed authentication attempts exceeding thresholds

  - Unauthorized API usage

  - Database query anomalies

- CloudWatch alarms for service degradation

- Container vulnerability scanning alerts from ECR

#### 5.1.3 Communication Channels

- Primary: SNS security alerts to designated mobile devices

- Escalation: Direct phone contact for Critical incidents

- Customer notifications: Email via established communication channels

### 5.2 Detection and Analysis Phase

#### 5.2.1 Initial Detection

Upon detection of a potential security event through automated monitoring or manual reporting:

1. **Event Triage** (Critical (P1) events acknowledged within 4 business hours; other severities per Section 7.1)

   - Review Security Hub findings or alert details

   - Query CloudWatch logs for related events

   - Check CloudTrail for unauthorized API calls

   - Assess potential customer impact

2. **Incident Declaration** (upon completion of triage)

   - Determine if event constitutes an incident

   - Assign initial severity level

   - Create incident record in the compliance platform's Incident Reporting system

   - The CEO assumes the Incident Commander role if Critical or High severity

#### 5.2.2 Incident Analysis

1. **Scope Determination**

   - Identify affected systems from CloudFormation documentation

   - Determine data exposure using Data Classification and Handling Standard

   - Assess number of affected customers

   - Evaluate regulatory notification requirements

2. **Evidence Collection**

   - Export CloudWatch logs (90-day retention available)

   - Capture CloudTrail audit logs

   - Preserve Lambda function logs and execution history

   - Document API request logs from audit middleware

   - Screenshot Security Hub findings and alerts

   - Collect container logs from ECS/Fargate

3. **Impact Assessment**

   - Business contact information exposure analysis

   - Service availability metrics against 99.9% SLA

   - Data integrity validation

   - Compliance implications for GDPR/CCPA

### 5.3 Containment, Eradication, and Recovery Phase

#### 5.3.1 Containment Strategies

**Immediate Containment** (Critical/High Severity):

- Isolate affected Lambda functions or containers

- Revoke compromised IAM credentials

- Block malicious IP addresses via security groups

- Disable affected user accounts in PropelAuth

- Tighten API rate limiting in middleware and restrict origin access at CloudFront

**Short-term Containment** (Medium/Low Severity):

- Apply temporary security group restrictions

- Increase CloudWatch monitoring thresholds

- Enable additional logging verbosity

- Implement rate limiting adjustments per API Security and Rate Limiting Standard

#### 5.3.2 Eradication

1. **Root Cause Elimination**

   - Remove malicious code or configurations

   - Patch identified vulnerabilities per Vulnerability Management Procedure

   - Update security group rules and NACLs

   - Rotate compromised credentials and API keys

   - Update KMS key policies if necessary

2. **System Hardening**

   - Apply security patches to Lambda runtime

   - Update container base images in ECR

   - Strengthen IAM policies per Access Control and Authentication Policy

   - Review and update CloudFormation security parameters

#### 5.3.3 Recovery

1. **Service Restoration**

   - Follow rollback procedures from Change Management Policy

   - Restore from backups if data integrity compromised

   - Validate system functionality through health checks

   - Confirm DocumentDB replication status

   - Verify CloudFront distribution configuration

2. **Monitoring Enhancement**

   - Increase monitoring sensitivity for affected components

   - Deploy additional CloudWatch alarms

   - Enable detailed CloudTrail logging

   - Implement compensating controls as needed

### 5.4 Post-Incident Activity Phase

#### 5.4.1 Lessons Learned (Within 5 Business Days)

1. **Incident Review**

   - Timeline reconstruction

   - Decision effectiveness analysis

   - Communication assessment

   - Tool and process evaluation

2. **Root Cause Analysis Documentation**

   - Technical root cause identification

   - Contributing factors analysis

   - Control failure assessment

   - Process gap identification

3. **Improvement Actions**

   - Update this procedure

   - Enhance detection rules in Security Hub

   - Modify Lambda breach detection logic

   - Update risk register per Risk Assessment Procedure

   - Schedule security awareness training per Security Awareness Training Program

#### 5.4.2 Documentation and Reporting

- Complete incident report in the compliance platform's Incident Reporting system

- Update incident metrics

- Archive evidence in secure S3 bucket with encryption

- Generate compliance reports for SOC 2 audit evidence

## 6. Communication Protocols

### 6.1 Internal Communications

#### During Incident:

- Incident record updated every 30 minutes for Critical incidents

- Hourly updates for High severity incidents

- Daily updates for Medium/Low severity incidents

#### Communication Methods:

- SNS notifications for automated alerts

- Direct phone contact for Critical incidents

- Incident record in the compliance platform's Incident Reporting system

### 6.2 External Communications

#### 6.2.1 Customer Notifications

**Data Breach Notification** (Within 48 hours):

- Nature of the incident and data affected

- Potential impact on customer operations

- Mitigation measures implemented

- Recommended customer actions

- Contact information for questions

**Service Disruption Notification**:

- Expected resolution timeframe

- Workaround procedures if available

- Updates on restoration progress

- Post-incident report availability

#### 6.2.2 Regulatory Notifications

**GDPR Requirements** (Within 72 hours):

- Notify supervisory authority of personal data breaches

- Document justification for any delayed notifications

- Provide breach details per Article 33 requirements

**CCPA Requirements**:

- Notify affected California residents without unreasonable delay

- Provide breach details per Section 1798.150 requirements

#### 6.2.3 Third-Party Notifications

- AWS Support for infrastructure-related incidents

- PropelAuth for authentication system incidents

## 7. Incident Classification and Prioritization

### 7.1 Severity Matrix

|**Severity**|**Customer Impact**|**Data Impact**|**Service Impact**|**Acknowledgement Target**|**Handling**|
|---|---|---|---|---|---|
|Critical (P1)|Multiple customers affected|Confirmed data breach|Complete service outage|4 business hours|Real-time Security Hub/SNS alert to the CEO; Incident Commander role activated|
|High (P2)|Single customer affected|Suspected data breach|Partial service degradation|1 business day|Real-time Security Hub/SNS alert to the CEO; Incident Commander role activated|
|Medium (P3)|No direct customer impact|Data integrity concerns|Minor feature unavailability|5 business days|Handled by the CEO; recorded in the compliance platform|
|Low (P4)|No customer impact|No data impact|No service impact|Monthly Security Hub findings review|Reviewed by the CEO at the monthly findings review|

### 7.2 Escalation Triggers

- Inability to contain incident within 2 hours

- Evidence of deliberate attack or insider threat

- Media or public attention

- Regulatory inquiry or investigation

- Customer data exposure exceeding 100 records

- Service degradation exceeding 99.9% SLA commitment

## 8. Evidence Management

### 8.1 Evidence Collection Requirements

- Maintain chain of custody documentation

- Use write-once storage for critical evidence

- Apply legal hold when required

- Ensure evidence integrity through checksums

- Document collection methods and timestamps

### 8.2 Evidence Retention

- Security incident evidence: 7 years

- Data breach evidence: 7 years

- Regulatory investigation evidence: Until the investigation is closed, and no less than 7 years

- Routine event logs: 90 days per standard retention

### 8.3 Evidence Storage

- Primary: S3 bucket with versioning and MFA delete

- Encryption: KMS customer-managed keys

- Access: Restricted to the CEO

- Backup: S3 versioning within the single region (us-east-1)

## 9. Testing and Maintenance

### 9.1 Incident Response Testing

**Annual Tabletop Exercise** (recorded in the compliance platform):

- Scenario-based discussions

- Decision-making evaluation

- Communication protocol validation

- Documentation review

- Customer communication practice

- Recovery procedure validation (the Business Continuity Plan full test record)

### 9.2 Procedure Maintenance

- Annual review and update of incident response procedure

- Quarterly review of incident metrics and trends

- Monthly update of contact lists and escalation paths

- Continuous improvement based on lessons learned

- Integration with updates to related policies and procedures

## 10. Metrics and Reporting

### 10.1 Key Performance Indicators

- Mean Time to Detect (MTTD): Critical findings alerted in real time via Security Hub/SNS

- Mean Time to Acknowledge (MTTA): Target < 4 business hours for Critical (P1)

- Mean Time to Contain (MTTC): Target < 2 hours from acknowledgement

- Mean Time to Resolve (MTTRes): Target < 24 hours

- Customer notification compliance: 100% within 48 hours

- Post-incident review completion: 100% within 5 business days

### 10.2 Reporting Requirements

- Monthly incident summary recorded in the compliance platform

- Quarterly trend analysis for risk assessment updates, recorded in the management meeting minutes

- Annual incident response program review

- SOC 2 audit evidence compilation

- Regulatory compliance reporting as required

## 11. Integration with Business Continuity

This procedure coordinates with the Business Continuity Plan for incidents requiring:

- Disaster recovery activation

- Failover to alternate availability zones

- Extended service disruption management

- Crisis communication protocols

- Backup restoration procedures

Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) defined in the Business Continuity Plan shall guide recovery prioritization during major incidents.

## 12. Related Documents

- Information Security Policy

- Risk Assessment Procedure

- Change Management Policy

- Business Continuity Plan

- Data Classification and Handling Standard

- Access Control and Authentication Policy

- Vulnerability Management Procedure

- System Monitoring and Logging Procedure

- Security Awareness Training Program

- Cloud Infrastructure Security Policy

- API Security and Rate Limiting Standard

- Privacy Notice and Data Processing Agreement Template

## Revision history

|**Version**|**Date**|**Author**|**Changes**|
|---|---|---|---|
|1.0|November 13, 2025|Mo Messidi|Initial procedure|
|2.0|<to be set at publication>|Mo Messidi|Scope limited to Security, Availability and Confidentiality; CEO as Incident Commander; annual tabletop exercise; P1 acknowledgement within 4 business hours; 7-year evidence retention; containment, communication and evidence-storage controls restated to the deployed environment|
