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

This Business Continuity Plan (BCP) sets out how Deal Intelligence LLC maintains critical operations and meets its service commitments during disruptions to the platform. It covers preparation, response, and recovery so that customer data is protected, the 99.9 % uptime SLA is maintained, and business operations continue, in accordance with the SOC 2 Trust Services Criteria for Availability (A1.1–A1.3).

The BCP implements the resilience requirements of the Information Security Policy and works with the Incident Response Procedure for a coordinated response to business-impacting events. It addresses both technical disasters affecting the AWS infrastructure and operational disruptions affecting service delivery.

## 2. Scope

This plan applies to:

- **Critical business functions**: Customer data processing, lead generation services, API availability, and authentication services
- **Technology infrastructure**: AWS cloud services (Lambda, Fargate, DocumentDB, CloudFront) and the PropelAuth authentication platform
- **Data assets**: Business contact information, customer account data, and lead qualification data as classified in the Data Classification and Handling Standard
- **Personnel**: All individuals responsible for maintaining service availability
- **Third-party dependencies**: Critical vendors identified in the Vendor Management Policy
- **Geographic scope**: The primary region (us-east-1); private subnets and Lambda functions in us-east-1a and us-east-1b; DocumentDB storage replicated across three availability zones

The platform is deployed in a single AWS region (us-east-1) by design. Resilience within the region is provided by the availability-zone design described in section 5 (DocumentDB storage replicated across three availability zones, automatic re-creation of the DocumentDB instance after an instance failure, and manual recovery of the instance into us-east-1b after an outage of us-east-1a); recovery from a complete regional outage relies on AWS service restoration and the CloudFormation redeployment strategy in section 7.2.

The plan covers scenarios from minor service degradation to a complete regional outage.

## 3. Roles and responsibilities

### 3.1 Chief Executive Officer (CEO)

The Chief Executive Officer (CEO) holds all three BCP roles.

As **business continuity coordinator**, the CEO:

- Maintains and updates this plan
- Coordinates the annual BCP testing and exercises
- Declares business continuity events and activates this plan
- Manages communication with customers and stakeholders during disruptions
- Oversees recovery operations and the return to normal operations
- Documents lessons learned and improvement opportunities

As **technical recovery lead**, the CEO:

- Executes the technical recovery procedures for the AWS infrastructure
- Manages database restoration and data recovery operations
- Coordinates with AWS Support on infrastructure issues
- Validates system functionality after recovery
- Maintains the technical recovery procedures in this plan (sections 6 and 7)

As **vendor liaison**, the CEO:

- Manages communication with critical vendors (AWS, PropelAuth)
- Coordinates vendor support during disruptions
- Tracks vendor SLA compliance and escalation procedures
- Maintains vendor contact information and support agreements

## 4. Business impact analysis

### 4.1 Critical business functions

| Function | Description | Maximum tolerable downtime | Recovery time objective (RTO) | Recovery point objective (RPO) |
|---|---|---|---|---|
| API services | Customer-facing API endpoints for data retrieval | 4 hours | 2 hours | 1 hour |
| Authentication services | PropelAuth JWT authentication and authorization | 2 hours | 1 hour | 30 minutes |
| Data processing | Lead generation and qualification processing | 8 hours | 4 hours | 4 hours |
| Database services | DocumentDB cluster operations | 4 hours | 2 hours | 1 hour |
| CDN services | CloudFront content delivery | 8 hours | 4 hours | — |

The RTO and RPO values above are met with DocumentDB's automatic re-creation of its single serverless instance after an instance failure (typically within 10 minutes), manual recovery of the instance into another availability zone after a zone outage (section 7.2), and point-in-time recovery from 35 days of automated backups (section 5.2). Cluster storage is replicated across three availability zones, so neither failure loses committed data. Authentication availability is provided by PropelAuth under its own SLA.

### 4.2 Resource dependencies

Critical infrastructure components:

- Lambda functions (900 s timeout, reserved concurrency 100)
- Fargate containers for batch processing
- DocumentDB cluster with KMS encryption
- CloudFront distribution
- VPC with private subnets
- EventBridge scheduling
- CloudFormation stack di-backend-api-prod

Critical data assets:

- Customer account database
- Business contact information repository
- Lead qualification data
- API configuration and secrets
- Authentication tokens and session data

## 5. Preventive controls

### 5.1 Infrastructure resilience

- Lambda functions and private subnets in us-east-1a and us-east-1b
- DocumentDB cluster storage replicated six ways across three availability zones; the single serverless instance re-created automatically by the service after an instance failure; after an availability-zone outage the CEO adds an instance in another availability zone to the same cluster (section 7.2)
- Lambda versioned deployments with rollback via `serverless rollback`
- CloudFront edge caching to reduce origin load
- Reserved concurrency settings to prevent resource exhaustion

### 5.2 Data protection

- Continuous automated backups with 35-day point-in-time recovery
- DocumentDB storage replication across three availability zones (performed by the service)
- Point-in-time recovery on DocumentDB
- Backups encrypted with KMS
- Quarterly backup restoration testing as documented in the System Monitoring and Logging Procedure, recorded in the compliance platform

### 5.3 Monitoring and early warning

- CloudWatch monitoring with automated alerting
- SNS notifications for critical events
- Resource utilization monitoring and capacity planning
- Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) routed by an EventBridge rule to the breach-detection Lambda, which alerts the CEO via SNS in real time
- Monthly configuration-check Lambda run against a fixed checklist (including DocumentDB backup retention), with a dated pass/fail record posted to the compliance platform

## 6. Response procedures

### 6.1 Activation criteria

This plan is activated when:

- The primary AWS region (us-east-1) experiences a significant outage
- An availability-zone outage stops the DocumentDB instance (recovery is manual; section 7.2)
- A critical vendor service (PropelAuth) experiences an extended outage
- Data corruption or loss affects production systems
- A security incident affects service availability (coordinated with the Incident Response Procedure)

### 6.2 Initial response (0–2 hours)

#### 6.2.1 Detection and assessment

- CloudWatch and SNS alerts trigger automatically
- The CEO assesses impact and severity
- The CEO determines whether BCP activation is required
- Initial findings are documented in the compliance platform's Incident Reporting system

#### 6.2.2 Communication initiation

- Affected customers are notified by email within 2 hours
- An AWS Support case is opened if the disruption is infrastructure-related
- PropelAuth support is contacted if authentication is affected

#### 6.2.3 Immediate mitigation

- Reroute traffic if partial services are available
- Enable read-only mode if database writes are affected
- Activate CloudFront failover origins if configured
- Scale unaffected resources to handle the additional load

### 6.3 Recovery operations (2–8 hours)

#### 6.3.1 Infrastructure recovery

- Execute the CloudFormation stack recovery procedures
- Restore DocumentDB from the most recent backup
- Redeploy Lambda functions from the ECR repositories
- Validate the VPC and networking configuration
- Restore EventBridge schedules and rules

#### 6.3.2 Data recovery

- Identify the last known good backup point
- Execute the database restoration procedures
- Validate data integrity after restoration
- Reconcile any data gaps using point-in-time recovery
- Update the lead processing queues

#### 6.3.3 Service validation

- Execute health checks
- Validate authentication services
- Test API endpoints and response times
- Verify data processing pipelines
- Confirm third-party integrations

### 6.4 Return to normal operations

#### 6.4.1 Service restoration

- Restore full service capabilities gradually
- Monitor system stability and performance
- Clear any processing backlogs
- Validate all automated processes

#### 6.4.2 Communication

- Notify customers of service restoration by email
- Provide an incident summary and impact assessment
- Close support tickets with vendors

#### 6.4.3 Post-incident activities

- Conduct a retrospective within 24 hours
- Document lessons learned in the compliance platform
- Update recovery procedures as needed
- Schedule follow-up testing if required

## 7. Recovery strategies

### 7.1 Data recovery strategy

Backup architecture:

- Continuous automated backups, with the daily backup window 03:00–04:00 UTC
- 35-day backup retention covering all production data (the DocumentDB maximum)
- Point-in-time recovery enabled on the DocumentDB cluster
- Backups encrypted with customer-managed KMS keys

Recovery procedures:

- Point-in-time recovery for transactions within the RPO
- Full database restoration from the daily backups
- Incremental recovery using point-in-time recovery
- Data validation using checksums and integrity checks

### 7.2 Infrastructure recovery strategy

Primary strategy, automatic recovery within the region:

- If the DocumentDB instance fails, the service re-creates it automatically in the same availability zone (typically within 10 minutes); cluster storage, replicated across three availability zones, is unaffected
- If us-east-1a is unavailable, the CEO adds a `db.serverless` instance in us-east-1b to the same cluster (`aws docdb create-db-instance`); it takes over the same cluster endpoint, so no configuration change is needed
- Point-in-time recovery (section 7.1) is used for data corruption or deletion, not for availability-zone failures
- Lambda functions run in us-east-1a and us-east-1b; the NAT instance and the Fargate subnet are in us-east-1a, so outbound calls to customer CRMs and Slack and the data-collection jobs resume when us-east-1a recovers
- CloudWatch alarms on API errors and latency detect the failure

Secondary strategy, CloudFormation redeployment:

- Complete infrastructure recreation from templates
- Configuration values from Parameter Store
- Application deployment from ECR images
- Automated deployment via GitHub Actions (`serverless deploy`) from a green CI run

### 7.3 Vendor service recovery

PropelAuth contingency:

- Cached authentication tokens (30-minute validity)
- Fallback to read-only mode for unauthenticated users
- Emergency bypass for critical operations (with audit logging)
- Evaluation of an alternative authentication provider

AWS service contingency:

- Service-specific recovery based on the AWS SLAs
- Single-region deployment (us-east-1) by design; recovery from a regional outage relies on AWS service restoration
- AWS Support escalation procedures
- Evaluation of an alternative cloud provider for future resilience

## 8. Testing and maintenance

### 8.1 Testing schedule

| Test type | Frequency | Scope | Responsible party |
|---|---|---|---|
| Backup restoration | Quarterly | Database recovery validation (automated, recorded in the compliance platform) | CEO |
| Full BCP exercise | Annually | Complete plan activation | CEO |

### 8.2 Plan maintenance

Review triggers:

- After any BCP activation
- Following significant infrastructure changes
- When new critical services are added
- After vendor or technology changes
- Annually at minimum

Update process:

1. Review the current plan's effectiveness
2. Incorporate lessons learned from tests and incidents
3. Update contact information and procedures
4. Validate the technical recovery procedures
5. Obtain approval from the CEO
6. Distribute the updated plan to the relevant parties
7. Update the plan in the compliance platform

### 8.3 Training requirements

- Annual BCP awareness training for all personnel
- Technical recovery procedures exercised by the CEO through the quarterly backup restoration test
- Integration with the Security Awareness Training Program

## 9. Communication plan

### 9.1 Internal communication

During a disruption:

- Immediate notification via SNS alerts
- Status updates every 30 minutes during active incidents
- Coordination through the designated communication channels
- Documentation in the compliance platform Incident Reporting system

### 9.2 External communication

Customer notification:

- Initial notification within 2 hours of the disruption
- Updates at the cadence in the Service Level Agreement (SLA) Management Policy (every 2 hours for P1 incidents) or on a significant status change
- Final resolution notice with an impact summary
- Follow-up communication within 48 hours

Notification templates:

- Initial disruption notice
- Service degradation advisory
- Recovery progress update
- Service restoration confirmation
- Post-incident report

### 9.3 Stakeholder contact information

| Stakeholder | Contact method | Timing |
|---|---|---|
| Customers | Email | Within 2 hours |
| AWS Support | Support console | Immediate for infrastructure issues |
| PropelAuth support | Support portal | Immediate for authentication issues |
| Data processors | Email | Within 4 hours if data is affected |

## 10. Compliance and reporting

### 10.1 Regulatory requirements

- **SOC 2 Availability**: Maintain a documented BCP with regular testing
- **GDPR Article 32**: Maintain the ability to restore availability of and access to data
- **CCPA**: Maintain reasonable security procedures, including disaster recovery

### 10.2 Reporting requirements

Internal reporting:

- BCP test results documented in the compliance platform
- Annual effectiveness review recorded in the management meeting minutes
- Incident activation reports within 24 hours

External reporting:

- Customer notifications per the SLA requirements
- Regulatory notifications if a data breach is involved
- Audit evidence for the SOC 2 examination
- Vendor performance against SLAs

## 11. Appendices

### Appendix A: Emergency contact list

| Contact | Role | Phone | Email | Escalation |
|---|---|---|---|---|
| Mo Messidi | CEO / all BCP roles | [CONFIRM: phone] | [CONFIRM: email] | Primary |
| AWS Support | Infrastructure | Via console | Via console | 24/7 |
| PropelAuth support | Authentication | Via portal | Via portal | Business hours |

### Appendix B: Recovery procedures

The recovery procedures for the platform are those documented in sections 6 and 7 of this plan, covering:

- DocumentDB recovery (backup restoration and point-in-time recovery)
- Lambda function redeployment from ECR
- CloudFormation stack recovery (`serverless deploy`)
- PropelAuth contingency
- Data validation

### Appendix C: Related documents

- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Classification and Handling Standard
- Incident Response Procedure
- Information Security Policy
- Security Awareness Training Program
- Service Level Agreement (SLA) Management Policy
- System Monitoring and Logging Procedure
- Vendor Management Policy

## 12. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial plan |
| 2.0 | <to be set at publication> | Mo Messidi | Single-region (us-east-1) design stated; resilience and recovery strategy restated around DocumentDB storage replication, automatic instance re-creation, manual availability-zone recovery, 35-day point-in-time recovery, and Lambda versioned rollback; customer notification by email; roles consolidated to the CEO; contact placeholders fixed |
