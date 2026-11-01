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

This procedure sets out how Deal Intelligence LLC identifies, analyzes, evaluates, and treats the information security risks that could affect its ability to meet its service commitments and system requirements. It addresses SOC 2 Trust Services Criteria CC3.1 (COSO Principle 6, specifies suitable objectives), CC3.2 (COSO Principle 7, identifies and analyzes risk), CC3.3 (COSO Principle 8, assesses fraud risk), CC3.4 (COSO Principle 9, identifies and assesses changes), CC9.1 (identifies and assesses risk), and CC9.2 (implements risk mitigation activities). It also supports compliance with GDPR Article 32 (security of processing), GDPR Article 35 (data protection impact assessment), and CCPA Section 1798.150 (security breach requirements).

The procedure implements the risk management principles of the Information Security Policy and governs the risk register in the compliance platform, covering the identified risk areas of data breaches, unauthorized access, and service availability threats.

## 2. Scope

This procedure applies to:

- All information assets supporting the platform
- AWS cloud infrastructure components, including Lambda functions, Fargate containers, DocumentDB, and associated services
- Third-party services and sub-processors listed in the Vendor Management Policy
- Business contact information and customer account data
- All personnel with access to Deal Intelligence systems
- Integration points with customer-controlled systems

The procedure covers risks across the selected Trust Services Criteria: Security, Availability, and Confidentiality.

## 3. Definitions

**Risk**: The potential for an unwanted outcome resulting from internal or external factors, as determined by likelihood and impact.

**Inherent risk**: The risk level before existing controls or mitigation measures are considered.

**Residual risk**: The risk remaining after controls have been implemented and are operating effectively.

**Risk appetite**: The level of risk Deal Intelligence is willing to accept in pursuit of its business objectives, defined as minimal for customer data protection and moderate for operational efficiency.

**Risk owner**: The individual responsible for managing a specific risk and for implementing its treatment plan.

**Control effectiveness**: A measure of how well a control reduces the likelihood or impact of a risk, validated through the control evidence recorded in the compliance platform.

**Risk register**: The central repository of identified risks, maintained in the compliance platform.

## 4. Roles and responsibilities

### 4.1 Chief Executive Officer (CEO)

The Chief Executive Officer (CEO):

- Defines the risk appetite and tolerance levels
- Reviews and approves high and critical risk treatment decisions
- Allocates resources for risk mitigation
- Reviews the quarterly risk assessment reports
- Conducts the annual risk assessment
- Maintains the risk register in the compliance platform
- Coordinates risk treatment implementation
- Monitors control effectiveness through the control evidence recorded in the compliance platform
- Records risk status in the quarterly management meeting minutes
- Identifies risks within the AWS infrastructure components
- Implements technical controls for risk mitigation
- Monitors system-specific risk indicators

### 4.2 All personnel

All personnel:

- Report identified risks or control failures immediately
- Comply with risk mitigation controls and procedures
- Participate in risk awareness activities

## 5. Risk assessment methodology

### 5.1 Risk identification

Risks are identified through three channels.

#### 5.1.1 Annual assessment

- Review of all systems and resources documented in the CloudFormation stack di-backend-api-prod for security vulnerabilities
- Evaluation of sub-processor risks per the Vendor Management Policy
- Assessment of data processing activities per the Data Classification and Handling Standard

#### 5.1.2 Continuous risk monitoring

- Monthly configuration-check record analysis and real-time CloudTrail event alerts
- CloudWatch alerts and metrics review
- Container vulnerability scanning results from ECR
- Incident trends from the Incident Reporting system in the compliance platform

#### 5.1.3 Triggered assessments

- Major system changes per the Change Management Policy
- New vendor onboarding per the Vendor Management Policy
- Security incidents per the Incident Response Procedure
- Regulatory changes affecting GDPR or CCPA compliance

### 5.2 Risk analysis

Each identified risk is analyzed on the following scales.

Likelihood scale (1–5):

1. Rare – less than once per year
2. Unlikely – once per year
3. Possible – quarterly
4. Likely – monthly
5. Almost certain – weekly or more frequent

Impact scale (1–5):

1. Negligible – no customer impact, < 1 hour recovery
2. Minor – limited customer impact, < 4 hours recovery
3. Moderate – multiple customers affected, < 24 hours recovery
4. Major – significant customer impact, < 48 hours recovery
5. Critical – service-wide impact, > 48 hours recovery, or data breach

**Risk score**: Likelihood × Impact = Risk score (1–25)

### 5.3 Risk evaluation

Risk scores are evaluated against the following thresholds:

- **Critical (20–25)**: Immediate action required; CEO approval needed
- **High (15–19)**: Treatment plan required within 30 days
- **Medium (10–14)**: Treatment plan required within 90 days
- **Low (1–9)**: Accept or monitor; document the justification

Current key risks and their mitigation status:

| Risk category | Inherent risk | Controls | Residual risk |
|---|---|---|---|
| Data breach | High (16) | Encryption (KMS), monitoring, PII sanitization | Low (6) |
| Unauthorized access | High (15) | MFA, RBAC, VPC isolation | Low (4) |
| Service availability | Medium (12) | Multi-AZ DocumentDB, 99.9 % SLA, 90-day backups | Low (3) |
| Vendor failure | Medium (10) | DPAs, minimal sub-processors | Low (5) |

### 5.4 Risk treatment

Risk treatment options are selected on a cost-benefit basis:

1. **Avoid**: Eliminate the risk by removing the threat source
2. **Mitigate**: Implement controls to reduce likelihood or impact
3. **Transfer**: Share the risk through insurance or contractual agreements
4. **Accept**: Document acceptance for risks within appetite

Treatment plans specify:

- The controls to be implemented
- Implementation timeline and milestones
- Resource requirements
- Success metrics
- Responsible parties

## 6. Risk assessment process

### 6.1 Annual risk assessment

1. **Planning** (week 1)
   - Define the assessment scope and objectives
   - Review the previous assessment results
   - Identify stakeholders and schedule sessions
2. **Information gathering** (weeks 2–3)
   - Inventory all systems via the CloudFormation documentation
   - Review the monthly configuration-check records, CloudTrail event alerts and CloudWatch metrics
   - Analyze incident reports from the compliance platform
   - Evaluate vendor assessments
3. **Risk identification** (week 4)
   - Conduct threat modeling for Lambda functions and containers
   - Review vulnerability scan results
   - Assess compliance gaps against the SOC 2 criteria
   - Document findings in the risk register
4. **Risk analysis and evaluation** (week 5)
   - Score risks on the likelihood and impact scales
   - Calculate inherent and residual risk levels
   - Prioritize risks for treatment
5. **Treatment planning** (week 6)
   - Develop risk treatment plans
   - Assign risk owners and timelines
   - Estimate resource requirements
   - Obtain CEO approval for critical risks
6. **Documentation and reporting** (week 7)
   - Update the risk register in the compliance platform
   - Generate the risk assessment report
   - Communicate results to stakeholders
   - Schedule follow-up reviews

### 6.2 Continuous risk monitoring

- **Real time**: Security-relevant CloudTrail events (root sign-in, IAM policy or user changes, CloudTrail stop/delete, KMS key disable, security-group changes) alerted to the CEO via EventBridge, the breach-detection Lambda and SNS
- **Monthly**: Configuration-check Lambda run against the fixed checklist, with the dated pass/fail record reviewed and remediated (recorded in the compliance platform)
- **Quarterly**: Review of control evidence and tasks in the compliance platform
- **Ad hoc**: Change-triggered assessments

### 6.3 Risk register maintenance

Each risk register entry in the compliance platform includes:

- Risk identifier and description
- Risk category and affected assets
- Likelihood and impact scores
- Inherent and residual risk levels
- Control mappings
- Treatment plans and status
- Risk owner and review dates
- Related incidents or findings

## 7. Integration with other processes

### 7.1 Change management

Changes under the Change Management Policy with a risk score of Medium or higher undergo a risk assessment before implementation.

### 7.2 Vendor management

New vendors are assessed under this procedure together with the Vendor Management Policy, using the vendor assessment workflow in the compliance platform.

### 7.3 Incident response

Security incidents managed under the Incident Response Procedure trigger a risk reassessment for the affected areas.

### 7.4 Business continuity

Risk assessment results inform the Business Continuity Plan priorities and the recovery objectives maintained in the compliance platform.

### 7.5 Vulnerability management

Vulnerabilities identified through the Vulnerability Management Procedure are entered in the risk register with the appropriate scoring.

## 8. Risk metrics and reporting

### 8.1 Key risk indicators (KRIs)

The following KRIs are monitored and reported quarterly:

- Number of critical and high risks
- Percentage of risks with completed treatment plans
- Average time to implement risk treatments
- Control effectiveness rate (controls with current evidence in the compliance platform)
- Number of risk-related incidents
- Vendor risk assessment completion rate

### 8.2 Reporting requirements

Management report (quarterly, recorded in the management meeting minutes):

- Risk heat map
- Top 10 risks and treatment status
- Risk trend analysis
- Control effectiveness metrics
- Compliance status against the SOC 2 criteria

Annual risk assessment report:

- Full risk landscape
- Year-over-year comparison
- Control maturity assessment
- Resource requirements for risk mitigation
- Strategic risk recommendations

## 9. Risk acceptance criteria

Risk acceptance requires formal documentation and approval:

- **Low risks (1–9)**: CEO approval
- **Medium risks (10–14)**: CEO approval with documented justification
- **High and critical risks (15–25)**: Not acceptable without mitigation

Accepted risks are:

- Documented in the risk register with justification
- Reviewed quarterly for changes in risk profile
- Re-evaluated annually or on significant changes

## 10. Related documents

**Policies**

- Information Security Policy
- Change Management Policy
- Cloud Infrastructure Security Policy
- Data Retention and Disposal Policy
- Service Level Agreement (SLA) Management Policy
- Vendor Management Policy

**Standards**

- API Security and Rate Limiting Standard
- Data Classification and Handling Standard
- Encryption and Cryptographic Controls Standard

**Procedures and plans**

- Business Continuity Plan
- Incident Response Procedure
- Penetration Testing and Security Assessment Procedure
- System Monitoring and Logging Procedure
- Vulnerability Management Procedure

**Other**

- Security Awareness Training Program

## 11. Revision history

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 1.0 | November 13, 2025 | Mo Messidi | Initial procedure |
| 2.0 | <to be set at publication> | Mo Messidi | Scope limited to Security, Availability, and Confidentiality; roles consolidated to the CEO; the compliance platform stated as the control register and source of control effectiveness; monthly configuration-check record with real-time CloudTrail event alerting |
