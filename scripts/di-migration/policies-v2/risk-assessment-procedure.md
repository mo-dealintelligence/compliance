---
title: "Risk Assessment Procedure"
doc_type: "Procedure"
version: "2.0"
supersedes: "1.0"
acknowledgment: "Explicit"
effective_date: "<to be set at publication>"
review_date: "<one year after effective date>"
author: "Mo Messidi"
source: "risk-assessment-procedure-v1.0.pdf"
---

# Risk Assessment Procedure

## 1. Purpose

This Risk Assessment Procedure establishes the systematic approach for identifying, analyzing, evaluating, and treating information security risks that could impact Deal Intelligence LLC's ability to meet its service commitments and system requirements. The procedure ensures comprehensive risk management aligned with SOC 2 Trust Services Criteria, specifically addressing CC3.1-CC3.4 (Risk Assessment) and CC9.1-CC9.2 (Risk Mitigation).

This procedure operationalizes the risk management principles defined in the Information Security Policy and provides the framework for maintaining the risk register in the compliance platform while addressing identified risk areas including data breaches, unauthorized access, and service availability threats.

## 2. Scope

This procedure applies to:

- All information assets supporting the platform

- AWS cloud infrastructure components including Lambda functions, Fargate containers, DocumentDB, and associated services

- Third-party services and sub-processors listed in the Vendor Management Policy

- Business contact information and customer account data

- All personnel with access to Deal Intelligence systems

- Integration points with customer-controlled systems

The procedure encompasses risks across the selected Trust Services Criteria: Security, Availability, and Confidentiality.

## 3. Definitions

**Risk**: The potential for an unwanted outcome resulting from internal or external factors, as determined by likelihood and impact.

**Inherent Risk**: The risk level before considering existing controls or mitigation measures.

**Residual Risk**: The remaining risk after controls have been implemented and are operating effectively.

**Risk Appetite**: The level of risk Deal Intelligence is willing to accept in pursuit of business objectives, defined as minimal for customer data protection and moderate for operational efficiency.

**Risk Owner**: Individual responsible for managing a specific risk and ensuring treatment plans are implemented.

**Control Effectiveness**: Measure of how well a control reduces the likelihood or impact of a risk, validated through the control evidence recorded in the compliance platform.

**Risk Register**: Centralized repository of identified risks maintained in the compliance platform.

## 4. Roles and Responsibilities

### 4.1 Chief Executive Officer (CEO)

- Define organizational risk appetite and tolerance levels

- Review and approve high and critical risk treatment decisions

- Allocate resources for risk mitigation activities

- Review quarterly risk assessment reports

- Conduct annual comprehensive risk assessments

- Maintain the risk register in the compliance platform

- Coordinate risk treatment implementation

- Monitor control effectiveness through the control evidence recorded in the compliance platform

- Record risk status in the quarterly management meeting minutes

- Identify risks within AWS infrastructure components

- Implement technical controls for risk mitigation

- Monitor system-specific risk indicators

### 4.2 All Personnel

- Report identified risks or control failures immediately

- Comply with risk mitigation controls and procedures

- Participate in risk awareness activities

## 5. Risk Assessment Methodology

### 5.1 Risk Identification

Risk identification shall be conducted through:

#### 1. Annual Comprehensive Assessment

- Review of all systems and resources documented in CloudFormation stack di-backend-api-prod for security vulnerabilities

- Evaluation of sub-processor risks per the Vendor Management Policy

- Assessment of data processing activities per Data Classification and Handling Standard

#### 2. Continuous Risk Monitoring

- Security Hub findings analysis

- CloudWatch alerts and metrics review

- Container vulnerability scanning results from ECR

- Incident trends from the Incident Reporting system in the compliance platform

#### 3. Triggered Assessments

- Major system changes per Change Management Policy

- New vendor onboarding per Vendor Management Policy

- Security incidents per Incident Response Procedure

- Regulatory changes affecting GDPR or CCPA compliance

### 5.2 Risk Analysis

Each identified risk shall be analyzed using the following criteria:

#### Likelihood Scale (1-5):

1. Rare - Less than once per year

2. Unlikely - Once per year

3. Possible - Quarterly

4. Likely - Monthly

5. Almost Certain - Weekly or more frequent

#### Impact Scale (1-5):

1. Negligible - No customer impact, <1 hour recovery

2. Minor - Limited customer impact, <4 hours recovery

3. Moderate - Multiple customer impact, <24 hours recovery

4. Major - Significant customer impact, <48 hours recovery

5. Critical - Service-wide impact, >48 hours recovery or data breach

**Risk Score Calculation**: Likelihood × Impact = Risk Score (1-25)

### 5.3 Risk Evaluation

Risk scores shall be evaluated against the following thresholds:

- **Critical (20-25)**: Immediate action required, CEO approval needed

- **High (15-19)**: Treatment plan required within 30 days

- **Medium (10-14)**: Treatment plan required within 90 days

- **Low (1-9)**: Accept or monitor, document justification

Current key risks identified and their mitigation status:

|**Risk Category**|**Inherent Risk**|**Controls**|**Residual Risk**|
|---|---|---|---|
|Data Breach|High (16)|Encryption (KMS), monitoring, PII sanitization|Low (6)|
|Unauthorized Access|High (15)|MFA, RBAC, VPC isolation|Low (4)|
|Service Availability|Medium (12)|Multi-AZ DocumentDB, 99.9% SLA, 90-day backups|Low (3)|
|Vendor Failure|Medium (10)|DPAs, minimal sub-processors|Low (5)|

### 5.4 Risk Treatment

Risk treatment options shall be selected based on cost-benefit analysis:

1. **Avoid**: Eliminate the risk by removing the threat source

2. **Mitigate**: Implement controls to reduce likelihood or impact

3. **Transfer**: Share risk through insurance or contractual agreements

4. **Accept**: Document acceptance for risks within appetite

Treatment plans shall specify:

- Specific controls to be implemented

- Implementation timeline and milestones

- Resource requirements

- Success metrics

- Responsible parties

## 6. Risk Assessment Process

### 6.1 Annual Risk Assessment

1. **Planning Phase** (Week 1)

   - Define assessment scope and objectives

   - Review previous assessment results

   - Identify stakeholders and schedule sessions

2. **Information Gathering** (Weeks 2-3)

   - Inventory all systems via CloudFormation documentation

   - Review Security Hub findings and CloudWatch metrics

   - Analyze incident reports from the compliance platform

   - Evaluate vendor assessments

3. **Risk Identification** (Week 4)

   - Conduct threat modeling for Lambda functions and containers

   - Review vulnerability scan results

   - Assess compliance gaps against SOC 2 criteria

   - Document findings in risk register

4. **Risk Analysis and Evaluation** (Week 5)

   - Score risks using likelihood and impact matrices

   - Calculate inherent and residual risk levels

   - Prioritize risks for treatment

5. **Treatment Planning** (Week 6)

   - Develop risk treatment plans

   - Assign risk owners and timelines

   - Estimate resource requirements

   - Obtain CEO approval for critical risks

6. **Documentation and Reporting** (Week 7)

   - Update risk register in the compliance platform

   - Generate risk assessment report

   - Communicate results to stakeholders

   - Schedule follow-up reviews

### 6.2 Continuous Risk Monitoring

Ongoing risk monitoring activities include:

- **Real time**: Critical Security Hub findings alerted via SNS

- **Weekly**: CloudWatch metrics analysis

- **Monthly**: Security Hub findings review (recorded); vulnerability scan review

- **Quarterly**: Review of control evidence and tasks in the compliance platform

- **Ad-hoc**: Change-triggered assessments

### 6.3 Risk Register Maintenance

The risk register maintained in the compliance platform shall include:

- Risk identifier and description

- Risk category and affected assets

- Likelihood and impact scores

- Inherent and residual risk levels

- Control mappings

- Treatment plans and status

- Risk owner and review dates

- Related incidents or findings

## 7. Integration with Other Processes

### 7.1 Change Management

All changes identified in the Change Management Policy with risk scores of Medium or higher shall undergo formal risk assessment before implementation.

### 7.2 Vendor Management

New vendors shall be assessed according to this procedure in conjunction with the Vendor Management Policy using the vendor assessment workflow in the compliance platform.

### 7.3 Incident Response

Security incidents managed per the Incident Response Procedure shall trigger risk reassessment for affected areas.

### 7.4 Business Continuity

Risk assessment results shall inform the Business Continuity Plan priorities and recovery objectives maintained in the compliance platform.

### 7.5 Vulnerability Management

Vulnerabilities identified through the Vulnerability Management Procedure shall be incorporated into the risk register with appropriate scoring.

## 8. Risk Metrics and Reporting

### 8.1 Key Risk Indicators (KRIs)

The following KRIs shall be monitored and reported quarterly:

- Number of critical and high risks

- Percentage of risks with completed treatment plans

- Average time to implement risk treatments

- Control effectiveness rate (controls with current evidence in the compliance platform)

- Number of risk-related incidents

- Vendor risk assessment completion rate

### 8.2 Reporting Requirements

**Management Report** (Quarterly, recorded in the management meeting minutes):

- Risk heat map

- Top 10 risks and treatment status

- Risk trend analysis

- Control effectiveness metrics

- Compliance status against SOC 2 criteria

**Operational Reports** (Monthly):

- New risks identified

- Treatment plan progress

- Control evidence results

- Incident correlation analysis

**Annual Risk Assessment Report**:

- Comprehensive risk landscape

- Year-over-year comparison

- Control maturity assessment

- Resource requirements for risk mitigation

- Strategic risk recommendations

## 9. Risk Acceptance Criteria

Risk acceptance requires formal documentation and approval:

- **Low Risks (1-9)**: CEO approval

- **Medium Risks (10-14)**: CEO approval with documented justification

- **High/Critical Risks (15-25)**: Not acceptable without mitigation

Accepted risks shall be:

- Documented in the risk register with justification

- Reviewed quarterly for changes in risk profile

- Re-evaluated annually or upon significant changes

## 10. Compliance Requirements

This procedure addresses the following SOC 2 Trust Services Criteria:

- **CC3.1**: COSO Principle 6 - Specifies Suitable Objectives

- **CC3.2**: COSO Principle 7 - Identifies and Analyzes Risk

- **CC3.3**: COSO Principle 8 - Assesses Fraud Risk

- **CC3.4**: COSO Principle 9 - Identifies and Assesses Changes

- **CC9.1**: Identifies and Assesses Risk

- **CC9.2**: Implements Risk Mitigation Activities

The procedure also supports compliance with:

- GDPR Article 32 (Security of Processing)

- GDPR Article 35 (Data Protection Impact Assessment)

- CCPA Section 1798.150 (Security Breach Requirements)

## 11. Related Documents

### Core Policies

- Information Security Policy

- Change Management Policy

- Vendor Management Policy

- Cloud Infrastructure Security Policy

### Standards and Guidelines

- Data Classification and Handling Standard

- Encryption and Cryptographic Controls Standard

- API Security and Rate Limiting Standard

### Procedures

- Incident Response Procedure

- Business Continuity Plan

- Vulnerability Management Procedure

- Penetration Testing and Security Assessment Procedure

- System Monitoring and Logging Procedure

### Supporting Documents

- Security Awareness Training Program

- Data Retention and Disposal Policy

- Service Level Agreement (SLA) Management Policy

## Revision history

|**Version**|**Date**|**Author**|**Changes**|
|---|---|---|---|
|1.0|November 13, 2025|Mo Messidi|Initial procedure|
|2.0|<to be set at publication>|Mo Messidi|Scope limited to Security, Availability and Confidentiality; roles consolidated to the CEO; the compliance platform stated as the control register and source of control effectiveness; Security Hub review monthly with real-time critical alerting|
