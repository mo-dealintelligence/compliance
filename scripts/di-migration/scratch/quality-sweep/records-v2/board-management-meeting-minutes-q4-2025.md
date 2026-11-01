---
title: "Document Control"
doc_type: "Record"
version: "1.0"
acknowledgment: "None"
effective_date: "N/A"
review_date: "N/A"
finalized_at: "February 02, 2026 at 01:55 AM"
author: "Mo Messidi"
source: "board-management-meeting-minutes-q4-2025-v1.0.pdf"
---

> Corrected 2026-10-31: historical record, kept as finalized on February 2, 2026 — figures (including the 86 % control-automation value) and decisions are as recorded; read "Quarterly Board Meeting" / "Board" as the quarterly management meeting, "Head of GTM" as the Go-to-Market Contractor, "PropelAuth MFA" as Google Workspace single sign-on with MFA inherited through PropelAuth, "load balancing" as Lambda versioned deployments with rollback, "Trust Services Category, Criteria, Related Controls and Evidence" as the compliance platform's control register, and the Processing Integrity and Privacy rows as the scope at the time (now Security, Availability, and Confidentiality).
## Meeting Information

**Meeting Type** : [X] Quarterly Board Meeting [ ] Annual Meeting [ ] Special Meeting

**Meeting Date** : December 9, 2025 **Meeting Time** : 2:00 PM - 4:00 PM PST **Location** : [ ] In-Person [X] Video Conference [ ] Phone Conference

**Meeting Called By** : Mo Messidi (CEO)

**Meeting Purpose** : Quarterly review of financial performance, operational status, security and compliance posture, risk assessment, and strategic initiatives in alignment with SOC 2 Trust Services Criteria governance requirements.

## Attendees

**Present** : - [X] CEO: Mo Messidi - [X] Contractor: William Wickey (Head of GTM) - [ ] External Advisor: N/A - [ ] Other: N/A

**Absent** : - None

**Quorum** : [X] Yes [ ] No

_Note: Quorum established per Deal Intelligence LLC operating agreement requirements._

## Agenda

1. Call to Order

2. Review of Previous Meeting Minutes

3. Financial Review

4. Operational Updates

5. Security and Compliance Review

6. Risk Assessment Review

7. Strategic Initiatives

8. Action Items Review

9. New Business

10. Next Meeting Date

11. Adjournment

## Meeting Minutes

## 1. Call to Order

Meeting called to order at 2:00 PM PST by Mo Messidi (CEO).

CEO confirmed that proper notice was provided to all required attendees and that the meeting was being conducted in accordance with governance requirements supporting SOC 2 compliance objectives.

## 2. Review of Previous Meeting Minutes

**Previous Meeting Date** : September 15, 2025 (Q3 2025)

**Minutes Reviewed** : [X] Yes [ ] No [ ] N/A (First Meeting)

**Minutes Approved** : [X] Yes [ ] No [ ] Amendments Required

**Amendments** (if any): No amendments required. Q3 2025 minutes approved as written.

**Motion** : Mo Messidi moved to approve Q3 2025 minutes. William Wickey seconded. Motion carried unanimously.

**Previous Action Items Status** : | Action Item | Owner | Status | Notes | |-------------|-------|--------|------| | Complete SOC 2 readiness assessment | Mo Messidi | Completed | 86% control automation achieved | | Finalize vendor DPAs | Mo Messidi | Completed | PropelAuth and AWS agreements in place | | Implement quarterly access reviews | Mo Messidi | Completed | Automated Lambda function deployed |

## 3. Financial Review

**Period Covered** : October 1, 2025 – December 9, 2025

### 3.1 Revenue Summary

|**Metric**|**Status**|**Notes**|
|---|---|---|
|Total Revenue|Confidential|On track with projections|
|Growth vs. Previous Period|On track|Positive trajectory|

|**Metric**|**Status**|**Notes**|
|---|---|---|
|Key Revenue Drivers|—|New customer acquisition, existing customer expansion, feature adoption|

### 3.2 Expense Summary

|**Category**|**Monthly Amount**|**Status**|
|---|---|---|
|Infrastructure (AWS)|~$2,000|Within budget|
|Personnel|Confidential|Within budget|
|Tools/Software|~$500|PropelAuth, monitoring tools, development tools|
|Compliance Platform|Included above|the compliance platform subscription|
|**Total Expenses**|Within budget|No variances requiring board attention|

### 3.3 Financial Decisions

**Motion** : None required. Financial performance reviewed and acknowledged.

**Discussion Points** : - Infrastructure costs remain stable with current AWS resource utilization - No significant budget variances identified - Compliance-related expenditures aligned with SOC 2 Type II certification timeline

## 4. Operational Updates

### 4.1 Platform Performance

|**Metric**|**Target**|**Actual**|**Status**|
|---|---|---|---|
|System Uptime|99.9%|99.95%|✓Exceeding SLA|
|API Response Time|<500ms|<300ms avg|✓Within target|
|Incident Count (P1/P2)|0|0|✓No critical incidents|

_Reference: Performance monitoring conducted per Service Level Agreement (SLA) Management_ _<u>Policy</u>_

### 4.2 Infrastructure Status

**AWS Infrastructure Health** : - Multi-AZ deployment (us-east-1a, us-east-1b) operating normally - DocumentDB cluster healthy with KMS encryption active - Lambda functions performing within reserved concurrency limits (100) - CloudFront CDN distribution active with no reported issues - VPC security groups and private subnets properly configured

_Reference: Infrastructure managed per Cloud Infrastructure Security Policy and Infrastructure and_ _<u>Recovery Policy</u>_

### 4.3 Customer Operations

|**Metric**|**Q4 Status**|
|---|---|
|Active Customers|Growing|
|Customer Support Tickets|Within normal range|
|Data Subject Requests|0 pending|
|Customer Complaints|None|

_Reference: Data subject requests handled per Data Subject Rights Request Procedure_

## 5. Security and Compliance Review

### 5.1 SOC 2 Compliance Status

**Trust Services Criteria Coverage** :

|**Criteria**|**Status**|**Notes**|
|---|---|---|
|Security (Required)|✓Implemented|Core controls operational|
|Availability|✓Implemented|99.9% SLA maintained|
|Processing Integrity|✓Implemented|Data validation controls active|
|Confidentiality|✓Implemented|Encryption and access controls in place|
|Privacy|✓Implemented|GDPR/CCPA controls operational|

**Control Automation Rate** : 86% (target: maintain or improve)

**Planned Controls for Q1-Q2 2026** : 2 low-impact gaps identified and scheduled for remediation

_Reference: Control mapping documented in Trust Services Category, Criteria, Related Controls_ _<u>and Evidence</u>_

### 5.2 Security Incidents

**Reporting Period** : October 1, 2025 – December 9, 2025

|**Incident Type**|**Count**|**Status**|
|---|---|---|
|Security Breaches|0|—|
|Unauthorized Access Attempts|0 confirmed|Monitoring active|
|Data Loss Events|0|—|
|Availability Incidents|0|—|

**Incident Response Readiness** : - Automated breach detection Lambda function operational - SNS security alerts configured and tested - 48-hour customer notification capability confirmed - Incident reporting tracked via the compliance platform's Incident Reporting system

_Reference: Incident Response Procedure_

### 5.3 Access Control Review

**Quarterly Access Review Status** : Completed (automated via Lambda function)

|**Review Area**|**Status**|**Findings**|
|---|---|---|
|User Access Rights|✓Reviewed|No unauthorized access identified|
|Privileged Accounts|✓Reviewed|Appropriate restrictions in place|
|Terminated User Access|✓Verified|No orphaned accounts|
|MFA Enforcement|✓Verified|Available for all users via PropelAuth|

_Reference:_ _<u>Access Control and Authentication Policy</u>_

### 5.4 Vulnerability Management

|**Activity**|**Status**|**Notes**|
|---|---|---|
|ECR Container Scanning|Active|No critical vulnerabilities|
|Dependency Scanning|Active|GitHub Actions pipeline|

|**Activity**|**Status**|**Notes**|
|---|---|---|
|Security Hub Findings|Reviewed|No high-severity findings|
|Penetration Testing|Scheduled|Annual test planned per policy|

_Reference: Vulnerability Management Procedure and Penetration Testing and Security_ _<u>Assessment Procedure</u>_

### 5.5 Privacy and Data Protection

**GDPR/CCPA Compliance Status** : - Data Processing Agreements in place with all sub-processors - Privacy notices current and accessible - Data subject request procedures operational - 24-month retention policy enforced for active leads

_Reference: Data Retention and Disposal Policy and Privacy Notice and Data Processing_ _<u>Agreement Template</u>_

## 6. Risk Assessment Review

### 6.1 Risk Register Summary

**Risk Assessment Method** : Quarterly review utilizing the compliance platform's Risk Assessment module

|**Risk Category**|**Risk Level**|**Mitigation Status**|**Trend**|
|---|---|---|---|
|Data Breach|Medium|Mitigated|Stable ↔|
|Unauthorized Access|Medium|Mitigated|Stable ↔|
|Service Availability|Low|Mitigated|Improved ↓|
|Third-Party/Vendor|Low|Mitigated|Stable ↔|
|Regulatory Non-Compliance|Low|Mitigated|Stable ↔|

### 6.2 Key Risk Mitigations in Place

|**Risk**|**Primary Mitigations**|
|---|---|
|Data Breach|KMS encryption, VPC isolation, audit logging, PII sanitization|
|Unauthorized Access|PropelAuth MFA, RBAC, quarterly access reviews, session timeouts|
|Service Availability|Multi-AZ deployment, daily backups, load balancing, 99.9% SLA|

**Risk Primary Mitigations** Third-Party Risk Minimal sub-processor model (2), DPAs, vendor assessments

_Reference: Risk Assessment Procedure_

### 6.3 Risk Decisions

**Board Acknowledgment** : The board reviewed and acknowledged the current risk posture. No additional risk treatment decisions required at this time.

**Motion** : Mo Messidi moved to accept the Q4 2025 risk assessment findings. William Wickey seconded. Motion carried unanimously.

## 7. Strategic Initiatives

### 7.1 SOC 2 Type II Certification

|**Milestone**|**Target Date**|**Status**|
|---|---|---|
|Policy Framework Complete|Q4 2025|✓Completed|
|Control Implementation|Q4 2025|✓86% automated|
|Gap Remediation|Q1-Q2 2026|In progress (2 items)|
|Type II Audit Period|2026|Planned|
|Certification Target|2026|On track|

### 7.2 Platform Development

|**Initiative**|**Status**|**Notes**|
|---|---|---|
|Feature Enhancements|On track|Per product roadmap|
|Security Improvements|Ongoing|Continuous improvement|
|Infrastructure Optimization|Ongoing|Cost and performance monitoring|

### 7.3 Business Development

|**Initiative**|**Owner**|**Status**|
|---|---|---|
|Customer Acquisition|William Wickey|Active|
|Market Expansion|William Wickey|Planning|
|Partnership Development|Mo Messidi|Evaluating|

## 8. Action Items Review

### 8.1 Completed Action Items from Q3 2025

|**Action Item**|**Owner**|**Completion Date**|
|---|---|---|
|Deploy automated access review Lambda|Mo Messidi|October 2025|
|Complete vendor DPA renewals|Mo Messidi|November 2025|
|Update incident response procedures|Mo Messidi|November 2025|

### 8.2 New Action Items for Q1 2026

|**Action Item**|**Owner**|**Due Date**|**Priority**|
|---|---|---|---|
|Complete 2 remaining control implementations|Mo Messidi|Q1 2026|Medium|
|Conduct annual penetration test|Mo Messidi|Q1 2026|High|
|Review and update Business Continuity Plan|Mo Messidi|Q1 2026|Medium|
|Complete annual security awareness training|Mo Messidi|Q1 2026|High|
|Prepare for SOC 2 Type II audit engagement|Mo Messidi|Q2 2026|High|

_Reference: Training requirements per Security Awareness Training Program_

## 9. New Business

### 9.1 Items Raised

|**Topic**|**Discussion**|**Decision/Action**|
|---|---|---|
|Q1 2026 backup restoration test|Quarterly test due per BCP|Schedule for January 2026|

|**Topic**|**Discussion**|**Decision/Action**|
|---|---|---|
|Annual policy review cycle|Policies due for annual review|Begin review cycle Q1 2026|
|Ethics violation log review|2025 log reviewed|No violations reported|

_Reference: Ethics Violation Log - 2025 and Business Continuity Plan_

### 9.2 Vendor Management Update

**Current Sub-Processors** :

|**Vendor**|**Service**|**DPA Status**|**Last Assessment**|
|---|---|---|---|
|AWS|Infrastructure|✓Active|Q4 2025|
|PropelAuth|Authentication|✓Active|Q4 2025|

**Vendor Changes** : None. 30-day notice requirement maintained per policy.

_Reference: Vendor Management Policy_

## 10. Next Meeting Date

**Next Quarterly Meeting** : March 2026 (Q1 2026 Review)

**Proposed Date** : Week of March 9, 2026

**Proposed Agenda Items** : - Q1 2026 financial review - SOC 2 Type II audit preparation status - Annual penetration test results - Policy annual review status - Risk assessment update

## 11. Adjournment

**Motion to Adjourn** : Mo Messidi moved to adjourn. William Wickey seconded.

**Meeting Adjourned** : 3:45 PM PST

## Approvals

|**Role**|**Name**|**Signature**|**Date**|
|---|---|---|---|
|CEO|Mo Messidi|_________________|________|
|Meeting Recorder|Mo Messidi|_________________|________|

## Appendices

## Appendix A: Related Documents

The following documents were referenced during this meeting:

- <u>Information Security Policy</u>

- <u>Access Control and Authentication Policy</u>

- <u>Incident Response Procedure</u>

- <u>Risk Assessment Procedure</u>

- <u>Business Continuity Plan</u>

- <u>Vendor Management Policy</u>

- <u>Change Management Policy</u>

## Appendix B: Compliance Framework Alignment

This meeting and its documentation support the following SOC 2 Trust Services Criteria:

|**Criteria**|**Relevance**|
|---|---|
|CC1.1|Demonstrates commitment to integrity and ethical values through governance oversight|
|CC1.2|Board exercises oversight of internal control system|
|CC1.3|Management establishes structure, reporting lines, and responsibilities|
|CC2.1|Information communicated internally to support functioning of internal control|
|CC3.1|Risk assessment process identifies and assesses risks|
|CC4.1|Monitoring activities evaluate whether controls are present and functioning|

_Document maintained in accordance with Deal Intelligence LLC governance requirements and SOC 2 compliance objectives._

**Document Information**
