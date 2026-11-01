---
title: "Business Continuity Plan"
doc_type: "Plan"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "business-continuity-plan-v1.0.pdf"
---

# Business Continuity Plan

## 1. Purpose

This Business Continuity Plan (BCP) establishes the framework for maintaining critical operations and meeting service commitments during disruptions to Deal Intelligence LLC's platform. This plan ensures systematic preparation, response, and recovery capabilities that protect customer data, maintain our 99.9% uptime SLA, and preserve business operations in accordance with SOC 2 Trust Service Criteria for Availability (A1.1-A1.3).

The BCP operationalizes resilience requirements defined in the Information Security Policy and integrates with the Incident Response Procedure to ensure coordinated response to business-impacting events. This plan addresses both technical disasters affecting AWS infrastructure and operational disruptions affecting service delivery capabilities.

## 2. Scope

This plan applies to:

- **Critical Business Functions**: Customer data processing, lead generation services, API availability, authentication services

- **Technology Infrastructure**: AWS cloud services (Lambda, Fargate, DocumentDB, CloudFront), PropelAuth authentication platform

- **Data Assets**: Business contact information, customer account data, lead qualification data as classified in the Data Classification and Handling Standard

- **Personnel**: All individuals responsible for maintaining service availability

- **Third-Party Dependencies**: Critical vendors identified in the Vendor Management Policy

- **Geographic Scope**: Primary region (us-east-1) with multi-availability zone deployment (us-east-1a, us-east-1b)

The platform is deployed in a single AWS region (us-east-1) by design. Resilience within the region is provided by the multi-availability zone deployment described in Section 5; recovery from a complete regional outage relies on AWS service restoration and the CloudFormation redeployment strategy in Section 7.2.

The plan encompasses scenarios ranging from minor service degradation to complete regional outages, ensuring business resilience across all operational contexts.

## 3. Roles and Responsibilities

### 3.1 Business Continuity Coordinator

**Role Holder**: Chief Executive Officer (Mo Messidi)

- Maintains and updates the Business Continuity Plan

- Coordinates annual BCP testing and exercises

- Declares business continuity events and activates this plan

- Manages communication with customers and stakeholders during disruptions

- Oversees recovery operations and return to normal operations

- Documents lessons learned and improvement opportunities

### 3.2 Technical Recovery Lead

**Role Holder**: Chief Executive Officer (Mo Messidi)

- Executes technical recovery procedures for AWS infrastructure

- Manages database restoration and data recovery operations

- Coordinates with AWS support for infrastructure issues

- Validates system functionality post-recovery

- Maintains the technical recovery procedures in this plan (Sections 6 and 7)

### 3.3 Vendor Liaison

**Role Holder**: Chief Executive Officer (Mo Messidi)

- Manages communication with critical vendors (AWS, PropelAuth)

- Coordinates vendor support during disruptions

- Ensures vendor SLA compliance and escalation procedures

- Maintains vendor contact information and support agreements

## 4. Business Impact Analysis

### 4.1 Critical Business Functions

|**Function**|**Description**|**Maximum Tolerable Downtime**|**Recovery Time Objective (RTO)**|**Recovery Point Objective (RPO)**|
|---|---|---|---|---|
|API Services|Customer-facing API endpoints for data retrieval|4 hours|2 hours|1 hour|
|Authentication Services|PropelAuth JWT authentication and authorization|2 hours|1 hour|30 minutes|
|Data Processing|Lead generation and qualification processing|8 hours|4 hours|4 hours|
|Database Services|DocumentDB cluster operations|4 hours|2 hours|1 hour|
|CDN Services|CloudFront content delivery|8 hours|4 hours|N/A|

The RTO and RPO values above are met with the Multi-AZ DocumentDB deployment, point-in-time recovery, and 90-day automated backups described in Section 5.2. Authentication availability is provided by PropelAuth under its own SLA.

### 4.2 Resource Dependencies

#### Critical Infrastructure Components:

- AWS Lambda functions (900s timeout, reserved concurrency: 100)

- AWS Fargate containers for batch processing

- DocumentDB cluster with KMS encryption

- CloudFront CDN distribution

- VPC with private subnets

- EventBridge scheduling services

- CloudFormation stack: di-backend-api-prod

#### Critical Data Assets:

- Customer account database

- Business contact information repository

- Lead qualification data

- API configuration and secrets

- Authentication tokens and session data

## 5. Preventive Controls

### 5.1 Infrastructure Resilience

- Multi-availability zone deployment across us-east-1a and us-east-1b

- Automated failover mechanisms for database services (Multi-AZ DocumentDB with a second instance in another availability zone)

- Lambda versioned deployments with rollback via `serverless rollback`

- CloudFront edge caching to reduce origin load

- Reserved concurrency settings to prevent resource exhaustion

### 5.2 Data Protection

- Daily automated backups with 90-day retention period

- Database replication across availability zones

- Point-in-time recovery capability for DocumentDB

- Encrypted backups using AWS KMS

- Quarterly backup restoration testing as documented in the System Monitoring and Logging Procedure, recorded in the compliance platform

### 5.3 Monitoring and Early Warning

- CloudWatch monitoring with automated alerting

- Security Hub findings for threat detection

- SNS notifications for critical events

- Resource utilization monitoring and capacity planning

- Integration with the breach-detection Lambda function that routes Security Hub findings to SNS

## 6. Response Procedures

### 6.1 Activation Criteria

The Business Continuity Plan is activated when:

- Primary AWS region (us-east-1) experiences significant outage

- Multiple availability zones become unavailable

- Critical vendor services (PropelAuth) experience extended outage

- Data corruption or loss affects production systems

- Security incident impacts service availability (coordinated with Incident Response Procedure)

### 6.2 Initial Response (0-2 hours)

#### 1. Detection and Assessment

- Automated monitoring alerts trigger via CloudWatch/SNS

- The CEO assesses impact and severity

- Determine if BCP activation is required

- Document initial findings in the compliance platform's Incident Reporting system

#### 2. Communication Initiation

- Notify affected customers via email within 2 hours

- Open AWS support case if infrastructure-related

- Contact PropelAuth support if authentication-affected

#### 3. Immediate Mitigation

- Implement traffic rerouting if partial services available

- Enable read-only mode if database writes affected

- Activate CloudFront failover origins if configured

- Scale unaffected resources to handle additional load

### 6.3 Recovery Operations (2-8 hours)

#### 1. Infrastructure Recovery

- Execute CloudFormation stack recovery procedures

- Restore DocumentDB from most recent backup

- Redeploy Lambda functions from ECR repositories

- Validate VPC and networking configuration

- Restore EventBridge schedules and rules

#### 2. Data Recovery

- Identify last known good backup point

- Execute database restoration procedures

- Validate data integrity post-restoration

- Reconcile any data gaps using point-in-time recovery

- Update lead processing queues

#### 3. Service Validation

- Execute comprehensive health checks

- Validate authentication services functionality

- Test API endpoints and response times

- Verify data processing pipelines

- Confirm third-party integrations

### 6.4 Return to Normal Operations

#### 1. Service Restoration

- Gradually restore full service capabilities

- Monitor system stability and performance

- Clear any processing backlogs

- Validate all automated processes

#### 2. Communication

- Notify customers of service restoration via email

- Provide incident summary and impact assessment

- Close support tickets with vendors

#### 3. Post-Incident Activities

- Conduct retrospective within 24 hours

- Document lessons learned in the compliance platform

- Update recovery procedures as needed

- Schedule follow-up testing if required

## 7. Recovery Strategies

### 7.1 Data Recovery Strategy

#### Backup Architecture:

- Daily automated backups at 02:00 UTC

- 90-day retention for all production data

- Point-in-time recovery enabled on the DocumentDB cluster

- Encrypted backups using customer-managed KMS keys

#### Recovery Procedures:

- Point-in-time recovery for transactions within RPO

- Full database restoration from daily backups

- Incremental recovery using point-in-time recovery

- Data validation using checksums and integrity checks

### 7.2 Infrastructure Recovery Strategy

#### Primary Strategy: Multi-AZ Failover

- Automatic failover between us-east-1a and us-east-1b

- Automatic failover of DocumentDB to the second instance in another availability zone

- Lambda functions distributed across AZs

- CloudWatch alarms on API errors and latency detect the failure

#### Secondary Strategy: CloudFormation Redeployment

- Complete infrastructure recreation from templates

- Parameter store values for configuration

- ECR images for application deployment

- Automated deployment via GitHub Actions (`serverless deploy`) from a green CI run

### 7.3 Vendor Service Recovery

#### PropelAuth Contingency:

- Cached authentication tokens (30-minute validity)

- Fallback to read-only mode for unauthenticated users

- Emergency bypass for critical operations (with audit logging)

- Alternative authentication provider evaluation

#### AWS Service Contingency:

- Service-specific recovery based on AWS SLAs

- Single-region deployment (us-east-1) by design; recovery from a regional outage relies on AWS service restoration

- AWS support escalation procedures

- Alternative cloud provider evaluation for future resilience

## 8. Testing and Maintenance

### 8.1 Testing Schedule

|**Test Type**|**Frequency**|**Scope**|**Responsible Party**|
|---|---|---|---|
|Backup Restoration|Quarterly|Database recovery validation (automated, recorded in the compliance platform)|CEO|
|Failover Testing|Semi-annually|AZ failover procedures|CEO|
|Full BCP Exercise|Annually|Complete plan activation|CEO|
|Communication Test|Quarterly|Notification systems|CEO|
|Vendor Coordination|Annually|Third-party response|CEO|

### 8.2 Plan Maintenance

#### Review Triggers:

- After any BCP activation

- Following significant infrastructure changes

- When new critical services are added

- After vendor or technology changes

- Annually at minimum

#### Update Process:

1. Review current plan effectiveness

2. Incorporate lessons learned from tests/incidents

3. Update contact information and procedures

4. Validate technical recovery procedures

5. Obtain approval from the CEO

6. Distribute updated plan to relevant parties

7. Update plan in the compliance platform

### 8.3 Training Requirements

- Annual BCP awareness training for all personnel

- Technical recovery procedures exercised by the CEO through the quarterly backup restoration test

- Vendor coordination procedures review semi-annually

- Integration with Security Awareness Training Program

## 9. Communication Plan

### 9.1 Internal Communication

#### During Disruption:

- Immediate notification via SNS alerts

- Status updates every 30 minutes during active incidents

- Coordination through designated communication channels

- Documentation in the compliance platform Incident Reporting system

### 9.2 External Communication

#### Customer Notification:

- Initial notification within 2 hours of disruption

- Updates every 4 hours or upon significant status change

- Final resolution notice with impact summary

- Follow-up communication within 48 hours

#### Notification Templates:

- Initial disruption notice

- Service degradation advisory

- Recovery progress update

- Service restoration confirmation

- Post-incident report

### 9.3 Stakeholder Contact Information

|**Stakeholder**|**Contact Method**|**Timing**|
|---|---|---|
|Customers|Email|Within 2 hours|
|AWS Support|Support Console|Immediate for infrastructure issues|
|PropelAuth Support|Support Portal|Immediate for auth issues|
|Data Processors|Email|Within 4 hours if data affected|

## 10. Compliance and Reporting

### 10.1 Regulatory Requirements

- **SOC 2 Availability**: Maintain documented BCP with regular testing

- **GDPR Article 32**: Ensure ability to restore availability and access to data

- **CCPA**: Maintain reasonable security procedures including disaster recovery

### 10.2 Reporting Requirements

#### Internal Reporting:

- BCP test results documented in the compliance platform

- Annual effectiveness review recorded in the management meeting minutes

- Incident activation reports within 24 hours

- Quarterly metrics on recovery objectives

#### External Reporting:

- Customer notifications per SLA requirements

- Regulatory notifications if data breach involved

- Audit evidence for SOC 2 examination

- Vendor performance against SLAs

## 11. Appendices

### Appendix A: Emergency Contact List

|**Contact**|**Role**|**Phone**|**Email**|**Escalation**|
|---|---|---|---|---|
|Mo Messidi|CEO / All BCP Roles|[CONFIRM: phone]|[CONFIRM: email]|Primary|
|AWS Support|Infrastructure|Via Console|Via Console|24/7|
|PropelAuth Support|Authentication|Via Portal|Via Portal|Business Hours|

### Appendix B: Recovery Procedures

The recovery procedures for the platform are those documented in Sections 6 and 7 of this plan, covering:

- DocumentDB recovery (backup restoration and point-in-time recovery)

- Lambda function redeployment from ECR

- CloudFormation stack recovery (`serverless deploy`)

- PropelAuth contingency

- Data validation

### Appendix C: Related Documentation

- Incident Response Procedure

- Change Management Policy

- Vendor Management Policy

- Service Level Agreement (SLA) Management Policy

- Cloud Infrastructure Security Policy

## Revision history

|**Version**|**Date**|**Author**|**Changes**|
|---|---|---|---|
|1.0|November 13, 2025|Mo Messidi|Initial plan|
|2.0|<to be set at publication>|Mo Messidi|Single-region (us-east-1) design stated; resilience and recovery strategy restated around Multi-AZ DocumentDB, point-in-time recovery, 90-day backups and Lambda versioned rollback; customer notification by email; roles consolidated to the CEO; contact placeholders fixed|
