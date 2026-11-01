#!/usr/bin/env python3
"""Quality sweep — control descriptions (2026-10-31).

Reads  scratch/quality-sweep/data/controls.json  (136 controls, v1 as held in Comp)
Writes scratch/quality-sweep/controls-v2.json    (same order; {id,name,description,changed,notes})

Rules applied (see policies-v2/RULEBOOK.md and QUALITY-RUBRIC.md Q4):
  * Requirement text (before "Implementation:") is kept verbatim except for
    R1 (PI/Privacy TSC mentions), R2 (size language, "all employees"/"team
    members" -> personnel, role names -> CEO / Go-to-Market Contractor).
    Every requirement edit is an exact-string replacement in REQ_EDITS and
    is asserted to match, so nothing is silently skipped.
  * The "Implementation:" note is replaced by the hand-written text in
    IMPL, keyed by the control's identifier prefix (e.g. "CC6.1.2").
  * Names are never changed (v1 names are truncated at ~110 chars; left as is).

Run:  python3 -I scratch/quality-sweep/rewrite_controls.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "data" / "controls.json"
OUT = HERE / "controls-v2.json"

# ---------------------------------------------------------------------------
# Requirement-text edits: control prefix -> list of (old, new, rule)
# ---------------------------------------------------------------------------
REQ_EDITS = {
    "A1.2.1": [
        ("For a remote-first technology company of this size, reliance on enterprise cloud providers",
         "Reliance on enterprise cloud providers", "R2"),
    ],
    "A1.3.1": [
        ("Given the remote work environment and small team size, testing shall include",
         "Testing shall include", "R2"),
    ],
    "C1.1.1": [
        ("Given the remote work environment and small team size, the policy should specifically address",
         "The policy should specifically address", "R2"),
        ("All team members must acknowledge", "All personnel must acknowledge", "R2"),
    ],
    "C1.1.2": [
        ("For a remote technology company, this includes establishing", "This includes establishing", "R2"),
        ("how team members identify", "how personnel identify", "R2"),
    ],
    "C1.1.3": [
        ("For the remote work environment, establish technical controls", "Establish technical controls", "R2"),
        ("Given the small team size, assign clear ownership", "Assign clear ownership", "R2"),
    ],
    "C1.1": [
        ("Train employees on recognizing", "Train personnel on recognizing", "R2"),
    ],
    "CC1.1.2": [
        ("For a small organization operating remotely, this includes", "This includes", "R2"),
    ],
    "CC1.1.4": [
        ("Given the small team size and remote environment, the organization shall ensure",
         "The organization shall ensure", "R2"),
    ],
    "CC1.1": [
        ("Small companies can start simple but must cover all stakeholders who interact with their systems and data.",
         "Controls must cover all stakeholders who interact with the organization's systems and data.", "R2"),
    ],
    "CC1.2.1": [
        ("Given the company's size of 2-5 employees, this authority may be", "This authority may be", "R2"),
    ],
    "CC1.2": [
        ("For smaller companies, this might be an outside advisor", "This might be an outside advisor", "R2"),
    ],
    "CC1.3.1": [
        ("Given the company's small size and remote work environment, this documentation must",
         "This documentation must", "R2"),
    ],
    "CC1.3.2": [
        ("Given the organization's size constraints, the framework shall implement",
         "The framework shall implement", "R2"),
    ],
    "CC1.4.1": [
        ("Given the company's small size (2-5 employees) and the nature of contractor relationships, the organization shall verify",
         "The organization shall verify", "R2"),
        ("For a remote technology company of this size, this includes", "This includes", "R2"),
        ("expected of all team members", "expected of all personnel", "R2"),
    ],
    "CC1.4.2": [
        ("Given the organization's size and remote work environment, training shall address",
         "Training shall address", "R2"),
    ],
    "CC1.4": [
        (" Small companies might start with basic security awareness but should expand training as they grow.", "", "R2"),
    ],
    "CC1.5.1": [
        ("Given the remote work environment and small team size, each team member's security accountabilities must be",
         "Security accountabilities for each role must be", "R2"),
    ],
    "CC1.5.2": [
        ("For a small remote team, this process should be", "This process should be", "R2"),
    ],
    "CC2.1": [
        (" Small companies should start with basic inventories and build more sophisticated information management over time.", "", "R2"),
    ],
    "CC2.2.1": [
        ("Given the organization's size, this may be consolidated", "This may be consolidated", "R2"),
    ],
    "CC2.2.3": [
        ("Given the small team size and remote environment, reporting procedures must",
         "Reporting procedures must", "R2"),
    ],
    "CC3.1.1": [
        ("protecting customer data, maintaining system availability, ensuring processing integrity, safeguarding confidential information, and respecting privacy rights",
         "protecting customer data, maintaining system availability, safeguarding confidential information, and meeting GDPR and CCPA obligations", "R1"),
    ],
    "CC3.1": [
        ("protecting customer data, maintaining system availability, ensuring accurate processing, keeping confidential information secret, and respecting privacy rights",
         "protecting customer data, maintaining system availability, and keeping confidential information secret", "R1"),
    ],
    "CC3.3.2": [
        ("For a technology company of this size operating remotely, controls shall include",
         "Controls shall include", "R2"),
    ],
    "CC3.4.1": [
        ("Given the organization's small team size and remote work environment, this process shall be",
         "This process shall be", "R2"),
    ],
    "CC4.1.1": [
        ("Given the organization's size, monitoring activities should be", "Monitoring activities should be", "R2"),
    ],
    "CC4.2.1": [
        ("Given the organization's size, a streamlined approach", "A streamlined approach", "R2"),
    ],
    "CC4.2.2": [
        ("For an organization of this size operating in a remote environment, communication protocols should",
         "Communication protocols should", "R2"),
    ],
    "CC5.1.2": [
        ("procedural safeguards (policies, training, and manual processes) appropriate for a small technology organization.",
         "procedural safeguards (policies, training, and manual processes).", "R2"),
    ],
    "CC5.2.2": [
        ("For a technology company of this size, this includes", "This includes", "R2"),
    ],
    "CC6.3.1": [
        ("Given the small team size, document the specific access rights required for each team member's responsibilities",
         "Document the specific access rights required for each role's responsibilities", "R2"),
    ],
    "CC6.3.2": [
        ("For this organization's size, the founder or designated lead shall approve all access changes.",
         "The CEO or a delegate approved by the CEO shall approve all access changes.", "R2"),
    ],
    "CC6.3.3": [
        ("Given the organization's small size where complete segregation may not be feasible, implement compensating controls",
         "Where complete segregation is not feasible, implement compensating controls", "R2"),
    ],
    "CC6.4.2": [
        ("Employees shall be required to implement", "Personnel shall be required to implement", "R2"),
    ],
    "CC6.5.2": [
        ("procedures for employees to return or certify", "procedures for personnel to return or certify", "R2"),
    ],
    "CC6.7.3": [
        ("Given the small team size and remote work environment, this includes", "This includes", "R2"),
        ("For a company of this size, centralized mobile device management (MDM) is not required;",
         "Centralized mobile device management (MDM) is not required;", "R2"),
    ],
    "CC6.8.1": [
        ("For a small remote team using macOS devices, this includes", "For macOS devices, this includes", "R2"),
        ("Given the organization's size and remote work environment, endpoint protection focuses on",
         "Endpoint protection focuses on", "R2"),
    ],
    "CC6.8.3": [
        ("Given the small team size, cross-training shall ensure multiple team members can execute response procedures.",
         "Cross-training shall ensure that more than one person can execute response procedures.", "R2"),
    ],
    "CC7.1.1": [
        ("Given the remote work environment and small team size, cloud-native configuration management",
         "Cloud-native configuration management", "R2"),
    ],
    "CC7.2.1": [
        ("a centralized security monitoring infrastructure appropriate for a small, remote-first technology company.",
         "a centralized security monitoring infrastructure.", "R2"),
    ],
    "CC7.2.2": [
        ("regardless of team member location", "regardless of location", "R2"),
    ],
    "CC7.2.3": [
        ("Given the small team size, procedures shall define", "Procedures shall define", "R2"),
    ],
    "CC7.3.1": [
        ("Given the remote work environment and small team size, the procedure shall include",
         "The procedure shall include", "R2"),
        ("accessible to all team members", "accessible to all personnel", "R2"),
    ],
    "CC7.4.1": [
        ("Given the small team size, the program should be", "The program should be", "R2"),
        ("accessible to all team members", "accessible to all personnel", "R2"),
    ],
    "CC7.4.2": [
        ("accounting for the remote work environment and small team structure",
         "accounting for the remote work environment", "R2"),
        ("Ensure all team members understand", "Ensure all personnel understand", "R2"),
    ],
    "CC7.5.2": [
        ("For a small remote team, tabletop exercises", "Tabletop exercises", "R2"),
    ],
    "CC8.1.1": [
        ("Given the small team size, a designated individual with appropriate authority must approve changes",
         "The CEO must approve changes", "R2"),
    ],
    "CC8.1.2": [
        ("Given the small team, testing responsibilities", "Testing responsibilities", "R2"),
    ],
    "CC8.1.3": [
        ("Appropriate segregation of duties shall be maintained where feasible given team size—at minimum, requiring peer review or secondary approval before production deployment.",
         "Appropriate segregation of duties shall be maintained where feasible; at minimum, every production deployment shall pass through a pull request on the protected main branch with required CI status checks and a logged self-review before merge.", "R2"),
    ],
    "CC9.1.3": [
        ("Given the organization's size, tabletop exercises", "Tabletop exercises", "R2"),
    ],
    "CC9.2.1": [
        ("For a small remote team, this process should be", "This process should be", "R2"),
    ],
    "CC9.2.2": [
        ("Given the organization's size, standard security addendum templates", "Standard security addendum templates", "R2"),
    ],
    "CC9.2.3": [
        ("For a small organization, annual reviews", "Annual reviews", "R2"),
    ],
}

# ---------------------------------------------------------------------------
# Implementation notes: control prefix -> (new note, change-type tags, extra note for CHANGES)
# Tags: humadroid, r4, r5, size, role, specific (made more specific), confirm, none
# ---------------------------------------------------------------------------
IMPL = {
    "A1.1.1": (
        "CloudWatch collects Lambda invocation, duration, error, and memory metrics, and CloudWatch alarms fire on the defined thresholds. "
        "Evidence: AWS CloudWatch Alarms, AWS CloudWatch Log Groups, Lambda App Events.",
        ["specific"], ""),
    "A1.1.2": (
        "CloudWatch retains metric history for trend analysis and DocumentDB storage growth is tracked in the cluster console; capacity is reviewed annually in the quarterly management meeting. "
        "Evidence: AWS CloudWatch Alarms, AWS DocumentDB Cluster.",
        ["role"], "\"board meetings\" -> management meeting (R2)."),
    "A1.1": (
        "CloudWatch monitors Lambda and DocumentDB capacity and alarms fire on threshold breaches. "
        "Evidence: AWS CloudWatch Alarms, AWS CloudWatch Log Groups, Lambda App Events.",
        ["specific"], ""),
    "A1.2.1": (
        "Physical security, redundant power, and environmental controls are provided by AWS data centers and verified through the AWS SOC 2 report reviewed in the AWS vendor assessment in the compliance platform.",
        ["specific"], "No task linked; the AWS vendor assessment record (Compliance Platform Vendor Assessment) is the evidence."),
    "A1.2.2": (
        "DocumentDB automated daily snapshots are retained 90 days with point-in-time recovery enabled, and a backup-restore test is run quarterly and recorded in the compliance platform. "
        "Evidence: AWS DocumentDB Backups, AWS DocumentDB Cluster.",
        ["r5"], "7-day retention -> 90 days (R3/R5); quarterly restore test added (R3)."),
    "A1.2.3": (
        "DocumentDB runs Multi-AZ with automatic failover; the compliance platform BCP dashboard records an RTO of 2 hours for AWS infrastructure, and the BCP full test executed February 4, 2026 completed with a 100 % success rate. "
        "Evidence: AWS DocumentDB Cluster, Compliance Platform Bcp Dashboard, Compliance Platform Bcp Test Results.",
        ["humadroid", "r4", "confirm"], "\"across 3 availability zones\" -> Multi-AZ per R3 wording; \"Q1 2025\" test label dropped in favour of the execution date (see CONFIRM)."),
    "A1.2": (
        "AWS data centers are SOC 2 attested; DocumentDB runs Multi-AZ with daily snapshots retained 90 days and point-in-time recovery enabled. "
        "Evidence: AWS DocumentDB Backups, AWS DocumentDB Cluster.",
        ["r5"], "7-day retention -> 90 days."),
    "A1.3.1": (
        "The BCP full test (plan: AWS Service Disruption Recovery; scenario: full system recovery from backups using infrastructure as code) was executed February 4, 2026 with the CEO as coordinator. "
        "Evidence: AWS DocumentDB Backups, Compliance Platform Bcp Test Results.",
        ["role", "confirm"], "Coordinator named by role instead of person; \"Q1 2025\" label dropped (CONFIRM)."),
    "A1.3.2": (
        "Test results are recorded in the compliance platform BCP test record: status Completed, success rate 100 %, system recovered successfully, plan status Active, one exercise to date. "
        "Evidence: Compliance Platform Bcp Test Results.",
        ["humadroid", "confirm"], "\"Q1 2025\" label dropped (CONFIRM)."),
    "A1.3": (
        "The BCP full test executed February 4, 2026 (full system recovery from backups using infrastructure as code) completed with status Completed and a 100 % success rate. "
        "Evidence: AWS DocumentDB Backups, Compliance Platform Bcp Test Results.",
        ["confirm"], "\"Q1 2025\" label dropped (CONFIRM)."),
    "C1.1.1": (
        "The Data Classification and Handling Standard defines four tiers (Public, Internal, Confidential, Restricted) with criteria per tier; personnel acknowledge it in the compliance platform portal.",
        ["specific"], "Tier names taken from the C1.1 note; acknowledgment mechanism per R6/R8."),
    "C1.1.2": (
        "Confidential information is identified by tier using the handling rules in the Data Classification and Handling Standard; data lives in known DocumentDB collections and S3 buckets, with CloudFormation tags on resources.",
        ["r4"], "v1 \"metadata tagging\" and file labeling removed per R4 (classification metadata/tags row); replaced with the R4 compensating wording."),
    "C1.1.3": (
        "Data at rest is encrypted with KMS customer-managed keys and personnel devices with FileVault; retention periods per tier are set in the Data Retention and Disposal Policy. "
        "Evidence: AWS KMS Keys, MacOS FileVault Status.",
        ["specific"], ""),
    "C1.1": (
        "Data is classified into four tiers (Public, Internal, Confidential, Restricted) under the Data Classification and Handling Standard and encrypted at rest with KMS. "
        "Evidence: AWS KMS Keys.",
        ["specific"], ""),
    "C1.2.1": (
        "Disposal triggers (retention expiry, contract termination, deletion requests) are defined in the Data Retention and Disposal Policy; KMS key deletion provides cryptographic erasure. "
        "Evidence: AWS KMS Keys.",
        ["none"], "Wording tightened only."),
    "C1.2.2": (
        "Deletions are evidenced by CloudTrail (KMS key usage), S3 access logs, and CloudWatch Logs, and dated disposal entries are recorded in the compliance platform. "
        "Evidence: AWS CloudTrail Trails, AWS CloudWatch Log Groups.",
        ["specific"], "Dated disposal entry in the compliance platform per R4 (DSR runbook row)."),
    "C1.2": (
        "S3 lifecycle rules and the scheduled retention-enforcement Lambda delete data at the end of its retention period; KMS key deletion provides cryptographic erasure, per the Data Retention and Disposal Policy. "
        "Evidence: AWS KMS Keys, AWS S3 Buckets.",
        ["specific"], "Retention-enforcement Lambda named from the R4 table."),
    "CC1.1.1": (
        "The Code of Conduct covers integrity, confidentiality, conflicts of interest, and remote-work conduct; it is approved by the CEO and acknowledged annually by all personnel in the compliance platform portal.",
        ["specific"], "Acknowledgment mechanism per R6."),
    "CC1.1.2": (
        "The CEO signed the Code of Conduct and completed security training; both are recorded in the compliance platform. "
        "Evidence: Ethics And Security Training Completion Certificate Mo Messidi.",
        ["none"], ""),
    "CC1.1.3": (
        "Ethics and security-awareness training is completed in the compliance platform at onboarding and annually; the current certificates are dated December 9, 2025. "
        "Evidence: Ethics And Privacy Training Completion Certificate William Wickey, Ethics And Security Training Completion Certificate Mo Messidi.",
        ["specific"], "Date format per Q2."),
    "CC1.1.4": (
        "Reporting and investigation steps are set out in the Code of Conduct; reports are recorded in the ethics violation log, which shows zero violations in 2025. "
        "Evidence: Ethics Violation Log 2025.",
        ["none"], ""),
    "CC1.1": (
        "The Code of Conduct is signed by all personnel; training completed in 2025 (CEO 8 hours security, Go-to-Market Contractor 4 hours privacy) and the ethics violation log shows zero violations. "
        "Evidence: Ethics And Privacy Training Completion Certificate William Wickey, Ethics And Security Training Completion Certificate Mo Messidi, Ethics Violation Log 2025.",
        ["role"], "\"contractor\" -> Go-to-Market Contractor; \"signed by all\" -> all personnel."),
    "CC1.2.1": (
        "The CEO provides oversight with consultation from an external advisor; the arrangement is documented in the organizational structure and the management meeting minutes. "
        "Evidence: Board Management Meeting Minutes Q4 2025, Organizational Structure.",
        ["confirm"], "Independence basis and the external advisor are v1 claims; CONFIRM."),
    "CC1.2.2": (
        "Quarterly management meetings review security posture, incidents, and compliance status; the Q4 2025 meeting is minuted. "
        "Evidence: Board Management Meeting Minutes Q4 2025.",
        ["role"], "Board -> management meeting (R2)."),
    "CC1.2": (
        "The Q4 2025 management meeting reviewed compliance status, security posture, and control effectiveness. "
        "Evidence: Board Management Meeting Minutes Q4 2025.",
        ["none"], ""),
    "CC1.3.1": (
        "Reporting lines and escalation paths are documented in the organizational structure, reviewed annually. "
        "Evidence: Organizational Structure.",
        ["size"], "\"for remote team\" removed."),
    "CC1.3.2": (
        "Job descriptions define decision authority for each role and IAM roles enforce technical access; where duties cannot be segregated, the compensating controls are the pull-request workflow with required CI checks, CloudTrail logging, and the external auditor's review. "
        "Evidence: Job Description Chief Executive Officer, Job Description Go To Market Contractor.",
        ["specific"], "Compensating controls cited from R2."),
    "CC1.3": (
        "The organizational structure defines roles and reporting lines, and the job descriptions specify security responsibilities. "
        "Evidence: Job Description Chief Executive Officer, Job Description Go To Market Contractor, Organizational Structure.",
        ["none"], ""),
    "CC1.4.1": (
        "Competency requirements are set in the job descriptions, professional references are verified, and security training is completed before production access (certificates dated December 9, 2025). "
        "Evidence: Ethics And Privacy Training Completion Certificate William Wickey, Ethics And Security Training Completion Certificate Mo Messidi, Job Description Chief Executive Officer, Job Description Go To Market Contractor.",
        ["none"], "Date format."),
    "CC1.4.2": (
        "Security-awareness training is completed in the compliance platform at onboarding and annually, and security responsibilities are assessed in the annual performance evaluation. "
        "Evidence: Annual Performance Evaluation Ceo.",
        ["specific"], "Training mechanism per R4 table."),
    "CC1.4": (
        "Training completed in 2025: CEO 8 hours, Go-to-Market Contractor 4 hours; certificates dated December 9, 2025 are held in the compliance platform. "
        "Evidence: Ethics And Privacy Training Completion Certificate William Wickey, Ethics And Security Training Completion Certificate Mo Messidi.",
        ["role"], ""),
    "CC1.5.1": (
        "Security responsibilities are documented in each job description and reviewed in the annual performance evaluation. "
        "Evidence: PropelAuth Security Settings.",
        ["confirm"], "Linked evidence (PropelAuth Security Settings) does not match the control; CONFIRM link."),
    "CC1.5.2": (
        "Personnel MFA is enforced in AWS (the IAM credential report shows 100 % MFA) and in Google Workspace and GitHub; customer sign-in is Google SSO through PropelAuth, which inherits Google Workspace MFA. The annual performance evaluation assesses security responsibilities. "
        "Evidence: Annual Performance Evaluation Ceo, AWS IAM Users, PropelAuth Users.",
        ["r5"], "\"PropelAuth enforces MFA\" -> R5 MFA wording."),
    "CC1.5": (
        "Customer sign-in is Google SSO through PropelAuth; IAM roles enforce least privilege in AWS; quarterly access reviews are minuted in the management meeting. "
        "Evidence: AWS IAM Users, Board Management Meeting Minutes Q4 2025, PropelAuth Security Settings, PropelAuth Users.",
        ["r5", "role"], "MFA wording per R5; board -> management."),
    "CC2.1.1": (
        "The AWS asset inventory (8 Lambda functions, 1 DocumentDB cluster, S3 buckets, VPC) is exported with the AWS CLI and reviewed annually in the Q4 management meeting. "
        "Evidence: AWS DocumentDB Cluster, AWS Lambda Functions, AWS S3 Buckets, AWS VPC List.",
        ["role"], "Board -> management."),
    "CC2.1.2": (
        "Data is classified as Public, Internal, Confidential, or Restricted under the Data Classification and Handling Standard, and data flows are documented in the system description. "
        "Evidence: AWS KMS Keys.",
        ["specific"], "\"Data flows documented\" located in the system description (R0)."),
    "CC2.1": (
        "The asset inventory (Lambda functions, DocumentDB, S3 buckets) is exported with the AWS CLI; handling rules per tier are in the Data Classification and Handling Standard. "
        "Evidence: AWS DocumentDB Cluster, AWS Lambda Functions, AWS S3 Buckets.",
        ["none"], ""),
    "CC2.2.1": (
        "Security objectives, policy changes, and control responsibilities are communicated through policy acknowledgments in the compliance platform portal and the quarterly management meeting.",
        ["confirm"], "v1 \"regular team communications\" is generic; mechanism named from R6/R8 (portal) and R2 (management meeting). CONFIRM."),
    "CC2.2.2": (
        "Security-awareness training is completed in the compliance platform at onboarding and annually; completion certificates are the evidence.",
        ["specific"], "Per R4 table; no task linked (certificates are linked to CC1.1.3/CC1.4)."),
    "CC2.2.3": (
        "Personnel report incidents and concerns to the CEO as set out in the Incident Response Procedure and the Code of Conduct; reports are recorded in the compliance platform incident register.",
        ["specific"], "Incident register per R4 (\"compliance platform is the control register\")."),
    "CC2.2": (
        "The Information Security Policy is acknowledged by all personnel in the compliance platform portal, training is completed annually, and reporting steps are in the Incident Response Procedure.",
        ["specific"], ""),
    "CC2.3.1": (
        "The privacy notice is published on dealintelligence.io and security documentation is provided to customers on request after CEO review.",
        ["none"], ""),
    "CC2.3.2": (
        "External parties report security concerns to the security contact published in the privacy notice; reports are triaged under the Incident Response Procedure, and the DPA template defines vendor notification duties.",
        ["confirm"], "v1 names no contact address; CONFIRM the published security contact."),
    "CC2.3": (
        "The privacy notice is published, a security contact is available to external parties, and security requirements for vendors are set in the DPA template.",
        ["none"], ""),
    "CC3.1.1": (
        "Security objectives are stated in the Risk Assessment Procedure and reviewed annually by the CEO; the compliance platform risk register holds 7 risks across categories. "
        "Evidence: Compliance Platform Risk Register.",
        ["humadroid", "r5"], "Risk count 6 -> 7 (current register export)."),
    "CC3.1.2": (
        "Security Hub findings and the annual risk assessment identify threats; the compliance platform tracks each risk by category with severity scoring. "
        "Evidence: AWS Securityhub Findings, Compliance Platform Risk Register.",
        ["humadroid"], ""),
    "CC3.1": (
        "The Risk Assessment Procedure documents objectives and the identification method; the compliance platform risk register tracks 7 identified risks. "
        "Evidence: AWS Securityhub Findings, Compliance Platform Risk Register.",
        ["humadroid", "r5"], "Risk count 6 -> 7."),
    "CC3.2.1": (
        "The Risk Assessment Procedure covers enterprise, system, and process risks from internal and external factors; the compliance platform scores risks using the Multi-Impact Assessment method. "
        "Evidence: Compliance Platform Risk Detail.",
        ["humadroid"], ""),
    "CC3.2.2": (
        "The compliance platform vendor register holds 5 vendors (AWS, PropelAuth, GitHub, Google Workspace, Resend) with risk tiers; SOC 2 reports are checked in the vendor assessment. "
        "Evidence: Compliance Platform Vendor Assessment, Compliance Platform Vendor Dashboard.",
        ["humadroid", "r5"], "Vendor count 2 -> 5 (current vendor export)."),
    "CC3.2": (
        "The CEO performs the annual risk assessment; each risk carries a likelihood and impact score in the compliance platform risk detail. "
        "Evidence: AWS Securityhub Overview, Compliance Platform Risk Detail.",
        ["humadroid", "confirm"], "v1 example \"4/3 = score 32\" dropped (arithmetic does not match); CONFIRM the scoring formula."),
    "CC3.3.1": (
        "The fraud triangle is evaluated in the annual risk assessment; the People Risk entry in the compliance platform records a Mitigate treatment with documented actions. "
        "Evidence: Compliance Platform Risk Detail.",
        ["humadroid"], ""),
    "CC3.3.2": (
        "CloudTrail logs all API activity and Security Hub aggregates findings; the breach-detection Lambda routes critical findings to SNS for review. "
        "Evidence: AWS CloudTrail Trails, AWS Securityhub Findings.",
        ["r4"], "GuardDuty -> Security Hub + CloudTrail + breach-detection Lambda (R4)."),
    "CC3.3": (
        "Fraud risk is assessed under the Risk Assessment Procedure; the compliance platform risk register includes a People Risk category covering insider threats. "
        "Evidence: AWS Securityhub Overview, Compliance Platform Risk Register.",
        ["humadroid"], ""),
    "CC3.4.1": (
        "Security Hub flags configuration changes and new vulnerabilities, and the CEO reviews vendor, regulatory, and personnel changes in the quarterly risk review. "
        "Evidence: AWS Securityhub Overview.",
        ["specific"], "Quarterly risk review from the CC3.4 note."),
    "CC3.4.2": (
        "Change triggers and the quarterly review cadence are set in the Risk Assessment Procedure; each quarterly risk review is recorded as a snapshot in the compliance platform risk register.",
        ["specific"], "Quarterly snapshot from the CC3.4 note."),
    "CC3.4": (
        "Security Hub monitors for significant configuration changes, and the Q4 2025 risk snapshot in the compliance platform records the quarterly risk review. "
        "Evidence: AWS Securityhub Findings, AWS Securityhub Overview, Compliance Platform Risk Register.",
        ["humadroid"], ""),
    "CC4.1.1": (
        "CloudWatch alarms and log reviews provide continuous monitoring, and the compliance platform is the control register for periodic control evaluation. "
        "Evidence: AWS CloudWatch Alarms, AWS CloudWatch Log Groups, CloudTrail Events, Lambda App Events.",
        ["specific"], ""),
    "CC4.1.2": (
        "Security Hub and Dependabot provide continuous vulnerability scanning (21 Dependabot alerts tracked), an annual third-party penetration test is performed, and the quarterly access review is minuted in the management meeting. "
        "Evidence: GitHub Dependabot, AWS Securityhub Findings, Board Management Meeting Minutes Q4 2025.",
        ["r4", "r5"], "GuardDuty removed; annual access review -> quarterly (R5); pen test from R3."),
    "CC4.1": (
        "CloudWatch and Security Hub provide continuous monitoring, and the scheduled access-review Lambda performs periodic reviews. "
        "Evidence: AWS CloudWatch Alarms, AWS Lambda Functions, AWS Securityhub Overview, CloudTrail Events, Lambda App Events.",
        ["r4"], "GuardDuty removed."),
    "CC4.2.1": (
        "Security Hub findings carry a severity, an owner (the CEO), and a remediation date; they are reviewed monthly and tracked in the compliance platform. "
        "Evidence: AWS Securityhub Findings.",
        ["specific"], "Monthly review per R5."),
    "CC4.2.2": (
        "Critical Security Hub findings alert the CEO in real time via SNS; other findings are reviewed monthly, and program status is reported in the quarterly management meeting. "
        "Evidence: AWS CloudWatch Log Groups, CloudTrail Events.",
        ["specific"], "Escalation mechanism from R4/R5."),
    "CC4.2": (
        "Security Hub identifies deficiencies, CloudWatch Logs and CloudTrail support investigation, and remediation is tracked in the compliance platform. "
        "Evidence: AWS CloudWatch Log Groups, AWS Securityhub Findings, CloudTrail Events.",
        ["none"], ""),
    "CC5.1.1": (
        "Controls are mapped to risks in the compliance platform; IAM roles and KMS encryption are the preventive access and data controls. "
        "Evidence: AWS IAM Roles, AWS KMS Keys.",
        ["specific"], ""),
    "CC5.1.2": (
        "Detective controls are CloudWatch alarms, Security Hub findings, and CloudTrail, with the breach-detection Lambda routing critical findings to SNS. "
        "Evidence: AWS CloudWatch Alarms, AWS Securityhub Overview.",
        ["r4"], "GuardDuty removed."),
    "CC5.1": (
        "Preventive controls: IAM and KMS; detective: CloudWatch, Security Hub, and CloudTrail; corrective: the Incident Response Procedure and Lambda versioned rollback. "
        "Evidence: AWS CloudWatch Alarms, AWS IAM Roles, AWS KMS Keys.",
        ["r4"], "GuardDuty removed; rollback mechanism from R4."),
    "CC5.2.1": (
        "Infrastructure is defined in CloudFormation and deployed through the Serverless Framework, so every deployment is version-controlled; the CEO is the only role with administrative access. "
        "Evidence: AWS Cloudformation Stacks.",
        ["role"], ""),
    "CC5.2.2": (
        "All changes go through a pull request on the protected main branch with required CI status checks and a logged self-review; emergency changes use a PR labelled emergency with post-hoc review within 5 business days. "
        "Evidence: GitHub Branch Protection.",
        ["r5"], "\"PR approval required\" -> PR + CI gate + self-review (R2/R3); emergency path per R5."),
    "CC5.2.3": (
        "New vendors and technologies are assessed in the compliance platform vendor assessment before use, under the Vendor Management Policy.",
        ["specific"], ""),
    "CC5.2": (
        "Infrastructure is deployed as code with CloudFormation, and GitHub branch protection requires a pull request with passing CI status checks before merge. "
        "Evidence: GitHub Deploy Workflow, GitHub Branch Protection, AWS Cloudformation Stacks.",
        ["r5"], "\"enforces code review\" -> PR + CI gate."),
    "CC5.3.1": (
        "Each policy has an operating procedure (Access Control, Change Management, Incident Response) published in the compliance platform portal and accessible to all personnel.",
        ["specific"], ""),
    "CC5.3.2": (
        "Role competencies are set in the job descriptions, training completion is recorded in the compliance platform, and IAM grants access to the CEO only.",
        ["role"], ""),
    "CC5.3.3": (
        "Policies and procedures are reviewed annually by the CEO; the review was minuted in the Q4 2025 management meeting and the next review is due Q4 2026. "
        "Evidence: Board Management Meeting Minutes Q4 2025.",
        ["role"], "Board -> management."),
    "CC5.3": (
        "Policies are put into practice through the Access Control and Authentication Policy, Change Management Policy, and Incident Response Procedure, all published in the compliance platform portal.",
        ["specific"], ""),
    "CC6.1.1": (
        "User accounts are inventoried in PropelAuth, the IAM credential report shows 100 % MFA, and the asset inventory is reviewed annually in the Q4 management meeting. "
        "Evidence: PropelAuth Security Settings, PropelAuth Users.",
        ["role"], "Board -> management."),
    "CC6.1.2": (
        "Customer sign-in is Google SSO through PropelAuth; the IAM password policy requires 14+ characters, complexity, and 90-day rotation, and personnel MFA is enforced in AWS, GitHub, and Google Workspace. "
        "Evidence: AWS IAM Password Policy, PropelAuth Security Settings.",
        ["r5"], "MFA wording per R5; password facts kept from v1."),
    "CC6.1.3": (
        "Workloads run in private VPC subnets with no direct internet access; security groups and network ACLs filter traffic. "
        "Evidence: AWS Security Groups, AWS VPC List, AWS VPC Subnets.",
        ["none"], ""),
    "CC6.1.4": (
        "KMS customer-managed keys (8 keys) with annual rotation encrypt DocumentDB and S3; all S3 buckets have default encryption. "
        "Evidence: AWS DocumentDB Cluster, AWS KMS Keys, AWS S3 Bucket Encryption.",
        ["none"], "Key count kept from v1 (CHANGES.md already carries a KMS inventory CONFIRM)."),
    "CC6.1.5": (
        "IAM roles grant least privilege, the DocumentDB credential is rotated by Secrets Manager, and API keys are rotated per the rotation calendar. "
        "Evidence: AWS IAM Roles, AWS IAM Users.",
        ["specific"], "Rotation facts from R3."),
    "CC6.1": (
        "Customer sign-in is Google SSO through PropelAuth; AWS access uses IAM with MFA and the IAM password policy. "
        "Evidence: AWS IAM Password Policy, AWS IAM Roles, AWS IAM Users, PropelAuth Security Settings, PropelAuth Users.",
        ["r5"], "MFA wording per R5."),
    "CC6.2.1": (
        "Users are registered in PropelAuth; the CEO approves each access request before provisioning, and roles are assigned on least privilege under the Access Control and Authentication Policy. "
        "Evidence: PropelAuth Security Settings, PropelAuth Users.",
        ["none"], ""),
    "CC6.2.2": (
        "PropelAuth holds the user inventory, IAM users have 100 % MFA, access is reviewed quarterly (minuted in the Q4 2025 management meeting), and offboarding revokes access within 1 business day. "
        "Evidence: AWS IAM Users, Board Management Meeting Minutes Q4 2025, PropelAuth Users.",
        ["r5", "role"], "Annual access review -> quarterly (R5)."),
    "CC6.2": (
        "PropelAuth registers and authenticates users via Google SSO, and AWS IAM enforces MFA and the password policy. "
        "Evidence: AWS IAM Password Policy, PropelAuth Mfa Settings, PropelAuth Security Settings.",
        ["r5"], "MFA wording."),
    "CC6.3.1": (
        "PropelAuth roles and IAM roles map each role to its permitted resources and access level. "
        "Evidence: AWS IAM Roles, PropelAuth Roles.",
        ["none"], ""),
    "CC6.3.2": (
        "The CEO approves all access changes; CloudTrail logs IAM changes, PropelAuth logs user provisioning, and access is revoked within 1 business day of termination. "
        "Evidence: AWS CloudTrail Trails, AWS IAM Users, PropelAuth Users.",
        ["none"], ""),
    "CC6.3.3": (
        "Where duties cannot be segregated, the compensating controls are the pull-request workflow with required CI status checks, CloudTrail and CloudWatch logging, and independent review by the external auditor. "
        "Evidence: AWS CloudWatch Log Groups, AWS Security Groups.",
        ["specific"], "Compensating controls cited from R2."),
    "CC6.3": (
        "PropelAuth roles define application access and IAM roles enforce AWS permissions. "
        "Evidence: AWS IAM Roles, PropelAuth Roles, PropelAuth Users.",
        ["none"], ""),
    "CC6.4.1": (
        "AWS data centers provide physical access controls, environmental protections, and 24/7 security; the AWS SOC 2 report is reviewed in the compliance platform vendor assessment.",
        ["specific"], ""),
    "CC6.4.2": (
        "Devices are encrypted with FileVault and stored securely; lost or stolen devices are reported within 24 hours under the Information Security Policy. "
        "Evidence: MacOS FileVault Status.",
        ["confirm"], "24-hour reporting kept from v1; the Acceptable Use Policy v2 says \"immediately\" (CONFIRM)."),
    "CC6.4": (
        "The organization is fully remote; physical security is provided by AWS SOC 2 attested data centers.",
        ["none"], ""),
    "CC6.5.1": (
        "Cloud data is disposed of by S3 lifecycle deletion and KMS cryptographic erasure; device media are wiped to NIST 800-88 under the Data Retention and Disposal Policy. "
        "Evidence: AWS KMS Keys.",
        ["none"], ""),
    "CC6.5.2": (
        "KMS key deletion is logged in CloudTrail and CloudWatch Logs and S3 access logs evidence deletion; a dated disposal entry is recorded in the compliance platform. "
        "Evidence: AWS CloudWatch Log Groups, AWS KMS Keys.",
        ["specific"], ""),
    "CC6.5": (
        "KMS cryptographic erasure, S3 lifecycle rules, and the scheduled retention-enforcement Lambda dispose of data at the triggers set in the Data Retention and Disposal Policy. "
        "Evidence: AWS KMS Keys, AWS Lambda Functions.",
        ["specific"], ""),
    "CC6.6.1": (
        "Infrastructure sits in private VPC subnets behind security groups; public entry is CloudFront with AWS Shield Standard and TLS 1.2+, with origin access restricted to the Lambda function URLs. "
        "Evidence: AWS Security Groups.",
        ["r4"], "Perimeter wording from the R4 WAF row."),
    "CC6.6.2": (
        "Company systems are reached only through browser SSO (Google Workspace) and the AWS console/CLI with MFA; no VPN is used, IAM enforces least privilege, and CloudTrail and CloudWatch log all access. "
        "Evidence: AWS CloudTrail Trails, AWS CloudWatch Log Groups, PropelAuth Mfa Settings, PropelAuth Security Settings.",
        ["r4", "r5"], "\"PropelAuth + MFA\" -> R4/R5 remote-access wording."),
    "CC6.6.3": (
        "Security Hub, CloudTrail, and the breach-detection Lambda detect threats and route critical findings to SNS; CloudWatch alarms and VPC Flow Logs provide alerting. "
        "Evidence: AWS CloudWatch Alarms, AWS Security Groups, VPC Flow Events.",
        ["r4"], "Detection mechanism from the R4 GuardDuty row."),
    "CC6.6": (
        "Security groups restrict traffic, network ACLs add a second layer, and DocumentDB is not reachable from the internet. "
        "Evidence: AWS Security Groups, AWS VPC Subnets.",
        ["none"], ""),
    "CC6.7.1": (
        "All endpoints are HTTPS only with TLS 1.2+ and ACM-managed certificates; API keys are managed in PropelAuth. "
        "Evidence: AWS IAM Roles, PropelAuth Api Keys.",
        ["r4"], "ACM/TLS per R4."),
    "CC6.7.2": (
        "All data lives in AWS (DocumentDB, S3) and is reached only through PropelAuth and IAM; TLS 1.2+ protects data in transit. "
        "Evidence: AWS IAM Roles, AWS S3 Bucket Encryption, PropelAuth Security Settings.",
        ["none"], ""),
    "CC6.7.3": (
        "FileVault encrypts all macOS devices, customer sign-in is Google SSO through PropelAuth with session timeout configured, and lost devices are reported within 24 hours under the Information Security Policy. "
        "Evidence: MacOS FileVault Status, PropelAuth Security Settings.",
        ["r5", "confirm"], "MFA wording per R5; 24-hour reporting CONFIRM (see CC6.4.2)."),
    "CC6.7.4": (
        "DocumentDB requires TLS, and CloudWatch Logs, CloudTrail, and VPC Flow Logs record data access for review. "
        "Evidence: AWS CloudWatch Log Groups, AWS DocumentDB Cluster, CloudTrail Events, VPC Flow Events.",
        ["none"], ""),
    "CC6.7": (
        "TLS 1.2+ protects all data in transit, endpoints are HTTPS only, and access requires PropelAuth or IAM authentication. "
        "Evidence: AWS IAM Roles, PropelAuth Security Settings.",
        ["none"], ""),
    "CC6.8.1": (
        "macOS XProtect and Gatekeeper and FileVault protect devices, with the compliance platform device agent where deployed; ECR scan-on-push, Dependabot, and Security Hub cover containers and code. "
        "Evidence: GitHub Dependabot, AWS ECR Repositories, AWS Securityhub Findings, MacOS FileVault Status.",
        ["r4"], "Device agent per R4."),
    "CC6.8.2": (
        "Dependabot proposes dependency updates that merge through the pull-request CI gate; critical dependency CVEs are remediated within 7 days. "
        "Evidence: GitHub Dependabot, GitHub Secret Scanning.",
        ["r5"], "Remediation SLA per R5."),
    "CC6.8.3": (
        "Security-awareness training covers phishing and malware, and the Incident Response Procedure defines containment steps for malware events. "
        "Evidence: Ethics And Security Training Completion Certificate Mo Messidi.",
        ["none"], ""),
    "CC6.8": (
        "ECR scan-on-push scans containers, Dependabot and code scanning cover dependencies (21 alerts tracked), and Trivy runs in CI; Security Hub aggregates findings. "
        "Evidence: GitHub Dependabot, AWS ECR Repositories, AWS Securityhub Findings.",
        ["r4", "confirm"], "v1 \"Code scanning via AWS not GitHub\" conflicts with the R4 table (GitHub code scanning); CONFIRM."),
    "CC7.1.1": (
        "CloudFormation (serverless deploy) is the only change path and reports drift; Security Hub configuration checks and CloudTrail detect unplanned changes. "
        "Evidence: AWS Securityhub Overview, CloudTrail Events.",
        ["r4"], "Baseline/drift wording from the R4 AWS Config row."),
    "CC7.1.2": (
        "Dependabot and Security Hub scan continuously, and Security Hub findings are reviewed monthly with critical findings alerting in real time. "
        "Evidence: GitHub Dependabot, AWS Securityhub Findings.",
        ["r5"], "Monthly review per R5."),
    "CC7.1": (
        "Security Hub, ECR scan-on-push, Dependabot, code scanning, and Trivy in CI detect new vulnerabilities; CloudTrail detects configuration changes. "
        "Evidence: GitHub Dependabot, AWS ECR Repositories, AWS Securityhub Findings, CloudTrail Events.",
        ["r4", "confirm"], "GuardDuty removed; code-scanning location CONFIRM (see CC6.8)."),
    "CC7.2.1": (
        "CloudTrail logs all AWS API calls with integrity validation, CloudWatch Logs retain application and VPC Flow Logs for 90 days, and Security Hub aggregates findings. "
        "Evidence: AWS CloudWatch Log Groups, CloudTrail Events, VPC Flow Events.",
        ["specific"], ""),
    "CC7.2.2": (
        "CloudWatch alarms fire on API errors and latency (p95 > 2 seconds) and on Lambda failures; critical Security Hub findings are routed to SNS in real time. "
        "Evidence: AWS CloudWatch Alarms, Lambda App Events, VPC Flow Events.",
        ["r5"], "Thresholds per R5/R4."),
    "CC7.2.3": (
        "The CEO reviews Security Hub findings monthly and receives SNS alerts in real time; logs are retained 90 days and the Incident Response Procedure sets triage and escalation. "
        "Evidence: AWS CloudWatch Alarms, AWS CloudWatch Log Groups, CloudTrail Events, Lambda App Events.",
        ["r5"], ""),
    "CC7.2": (
        "CloudTrail logs every API call with integrity validation and is retained 7 years; CloudWatch alarms and Logs (90 days) cover application events. "
        "Evidence: GitHub Actions Workflows, AWS CloudWatch Alarms, AWS CloudWatch Log Groups, CloudTrail Events, Lambda App Events, VPC Flow Events.",
        ["r5"], "CloudTrail 90-day retention -> 7 years (R5)."),
    "CC7.3.1": (
        "The Incident Response Procedure defines severity levels P1 to P4, classification criteria, and the CEO as triage owner; alerts arrive via SNS. "
        "Evidence: AWS SNS Topics.",
        ["specific"], "Severity scale per Q2."),
    "CC7.3.2": (
        "CloudWatch alarms publish to SNS topics; P1 events are acknowledged within 4 business hours and investigated under the Incident Response Procedure. "
        "Evidence: AWS CloudWatch Alarms, CloudTrail Events, VPC Flow Events.",
        ["r4"], "Response target per R4."),
    "CC7.3": (
        "Security Hub findings and SNS alerts are evaluated against CloudTrail and VPC Flow Logs; the compliance platform incident register shows 0 open incidents and 100 % SLA compliance. "
        "Evidence: AWS CloudWatch Alarms, AWS Securityhub Findings, AWS SNS Topics, CloudTrail Events, Compliance Platform Incident Reporting, VPC Flow Events.",
        ["humadroid"], ""),
    "CC7.4.1": (
        "The Incident Response Procedure defines incident criteria, severity levels P1 to P4, escalation thresholds, and response targets, and is reviewed annually.",
        ["specific"], ""),
    "CC7.4.2": (
        "The CEO is incident commander; the Incident Response Procedure documents roles, the escalation chain, and criteria for engaging external parties. "
        "Evidence: Organizational Structure.",
        ["confirm"], "Requirement asks for a backup incident commander; none is named (CONFIRM)."),
    "CC7.4.3": (
        "Containment uses IAM credential revocation and VPC isolation; remediation and recovery steps are in the Incident Response Procedure. "
        "Evidence: AWS SNS Topics, CloudTrail Events, VPC Flow Events.",
        ["none"], ""),
    "CC7.4.4": (
        "Incidents are documented on the Incident Response Procedure template with evidence from CloudWatch Logs and CloudTrail retained 7 years; notifications go out via SNS and customers are notified within 48 hours. "
        "Evidence: AWS CloudWatch Log Groups, AWS SNS Topics, CloudTrail Events.",
        ["r5"], "Evidence retention and notification window per R5."),
    "CC7.4.5": (
        "Post-incident reviews follow the Incident Response Procedure and lessons learned are minuted in the quarterly management meeting. "
        "Evidence: Board Management Meeting Minutes Q4 2025.",
        ["role"], "Board -> management."),
    "CC7.4": (
        "The Incident Response Procedure defines roles, escalation, containment, and remediation; the compliance platform incident register shows 0 open incidents and 100 % SLA compliance, and Security Hub provides detection. "
        "Evidence: AWS Securityhub Findings, AWS SNS Topics, CloudTrail Events, Compliance Platform Incident Reporting, VPC Flow Events.",
        ["humadroid"], ""),
    "CC7.5.1": (
        "The Business Continuity Plan documents recovery from security incidents, with DocumentDB point-in-time recovery and CloudFormation redeploy as the recovery path. "
        "Evidence: AWS CloudTrail Trails.",
        ["specific"], ""),
    "CC7.5.2": (
        "The BCP full test of February 4, 2026 exercised incident recovery (full system recovery from backups using infrastructure as code); backup restores are tested quarterly and the BCP annually. "
        "Evidence: AWS DocumentDB Backups, Compliance Platform Bcp Test Results.",
        ["r5", "confirm"], "Quarterly restore test per R3/R5; \"Q1 2025\" label dropped (CONFIRM)."),
    "CC7.5": (
        "Recovery follows the Business Continuity Plan: restore DocumentDB from backups or point-in-time recovery and redeploy with CloudFormation; CloudWatch and CloudTrail verify the restored system. "
        "Evidence: AWS CloudTrail Trails, AWS CloudWatch Log Groups, CloudTrail Events, Lambda App Events.",
        ["r4"], "GuardDuty removed; v1 note did not describe recovery."),
    "CC8.1.1": (
        "Every change is a pull request on the protected main branch approved by the CEO after CI passes; emergency changes use a PR labelled emergency with post-hoc review within 5 business days, and deployment is by CloudFormation. "
        "Evidence: GitHub Deploy Workflow, AWS Cloudformation Stacks.",
        ["r5"], "Authorization and emergency path per R3/R5."),
    "CC8.1.2": (
        "Pull requests must pass CI status checks (lint, tests, Bandit, Trivy, TruffleHog) and are validated on the staging stage before merge to main. "
        "Evidence: GitHub Branch Protection.",
        ["r5"], "\"PR approval\" -> CI gate + staging (R3)."),
    "CC8.1.3": (
        "Production deploys only from a green CI run on a pull request with a logged self-review, merged by the CEO as final approver; Dependabot updates follow the same path. "
        "Evidence: GitHub Branch Protection.",
        ["r5"], "Segregation replaced by the R2 compensating control."),
    "CC8.1": (
        "GitHub branch protection requires a pull request with passing CI status checks before merge, and CloudFormation deploys the same stack to staging and production. "
        "Evidence: GitHub Deploy Workflow, GitHub Workflow Run Details, GitHub Branch Protection.",
        ["r5"], "\"PR review required\" -> PR + CI gate."),
    "CC9.1.1": (
        "The Business Continuity Plan identifies critical systems with RTO/RPO; the compliance platform BCP dashboard records AWS infrastructure (RTO 2 hours), customer data pipeline (RTO 4 hours), and DocumentDB (RTO 4 hours). "
        "Evidence: Compliance Platform Bcp Dashboard.",
        ["humadroid", "confirm"], "\"MongoDB\" -> DocumentDB (Q2); CONFIRM the dashboard label."),
    "CC9.1.2": (
        "DocumentDB runs Multi-AZ with automatic failover in a single region (us-east-1) by design; the compliance platform BCP dashboard shows 8 active plans with 0 overdue exercises. "
        "Evidence: AWS DocumentDB Cluster, Compliance Platform Bcp Dashboard.",
        ["humadroid", "r4"], "\"geographic redundancy\" -> single region per R4."),
    "CC9.1.3": (
        "The BCP full test executed February 4, 2026 (full system recovery from backups using infrastructure as code) completed with a 100 % success rate; backup restores are tested quarterly. "
        "Evidence: AWS DocumentDB Backups, Compliance Platform Bcp Test Results.",
        ["r5", "confirm"], "\"Q1 2025\" label dropped (CONFIRM)."),
    "CC9.1": (
        "The Business Continuity Plan sets RTO/RPO; the compliance platform BCP dashboard holds 8 processes (7 critical) and 8 active plans, backed by Multi-AZ DocumentDB with 90-day automated backups. "
        "Evidence: AWS DocumentDB Backups, AWS DocumentDB Cluster, Compliance Platform Bcp Dashboard.",
        ["humadroid"], ""),
    "CC9.2.1": (
        "Vendors are assessed in the compliance platform before engagement; the AWS assessment verifies SOC 2 Type II and assigns risk tier Critical. "
        "Evidence: Compliance Platform Vendor Assessment.",
        ["none"], ""),
    "CC9.2.2": (
        "The Privacy Notice and Data Processing Agreement Template sets confidentiality, breach notification, audit rights, and termination terms for vendor agreements.",
        ["none"], ""),
    "CC9.2.3": (
        "Critical vendors are reassessed annually in the compliance platform vendor dashboard (AWS and PropelAuth most recently), and the Business Continuity Plan documents vendor contingency. "
        "Evidence: Compliance Platform Vendor Dashboard.",
        ["humadroid", "r5"], "\"2 months ago\" relative date removed; annual cadence per R5."),
    "CC9.2": (
        "The compliance platform vendor register tracks 5 vendors (AWS, PropelAuth, GitHub, Google Workspace, Resend) with risk tiers and assessment status. "
        "Evidence: Compliance Platform Vendor Dashboard.",
        ["humadroid", "r5"], "Vendor count 2 -> 5."),
}

BANNED = re.compile(
    r"Humadroid|GuardDuty|AWS Config\b|\bWAF\b|Inspector|\bEC2\b|multi-region|Given the organization's (size|small)|"
    r"small (remote )?team|small (company|organization)|of this size|2-5 employees|all employees|"
    r"Board of Directors|board meeting|7-day|team member",
    re.I,
)
# the AICPA criterion text legitimately says "board of directors"; allow in REQ only for CC1.2
ALLOWED_REQ = {"CC1.2": [re.compile(r"board of directors", re.I)]}


def prefix(name: str) -> str:
    return name.split(" ", 1)[0]


def main() -> int:
    controls = json.loads(SRC.read_text())
    out, problems = [], []
    used_req, used_impl = set(), set()
    for c in controls:
        pfx = prefix(c["name"])
        desc = c["description"]
        if "Implementation:" not in desc:
            problems.append(f"{pfx}: no Implementation: marker")
            out.append({**c, "changed": False, "notes": "no Implementation marker"})
            continue
        req, _ = desc.split("Implementation:", 1)
        req_new = req
        rules = []
        for old, new, rule in REQ_EDITS.get(pfx, []):
            if old not in req_new:
                problems.append(f"{pfx}: requirement edit not found: {old[:60]!r}")
                continue
            req_new = req_new.replace(old, new, 1)
            rules.append(rule)
        used_req.add(pfx)
        if pfx not in IMPL:
            problems.append(f"{pfx}: no implementation note written")
            impl_new, tags, extra = desc.split("Implementation:", 1)[1].strip(), ["none"], "MISSING"
        else:
            impl_new, tags, extra = IMPL[pfx]
            used_impl.add(pfx)
        # evidence references must point at linked tasks
        if "Evidence:" in impl_new:
            ev = impl_new.split("Evidence:", 1)[1].strip().rstrip(".")
            for item in [e.strip() for e in ev.split(",")]:
                if item not in c["tasks"]:
                    problems.append(f"{pfx}: evidence {item!r} not in tasks {c['tasks']}")
        new_desc = req_new.rstrip() + "\n\nImplementation: " + impl_new.strip()
        for m in BANNED.finditer(new_desc):
            if any(a.search(m.group(0)) for a in ALLOWED_REQ.get(pfx, [])):
                continue
            problems.append(f"{pfx}: banned term {m.group(0)!r} remains")
        changed = new_desc != desc
        note_bits = []
        if rules:
            note_bits.append("Requirement: " + ", ".join(sorted(set(rules))) + " edit(s).")
        note_bits.append("Implementation: " + ", ".join(tags) + ("; " + extra if extra else "."))
        out.append({
            "id": c["id"],
            "name": c["name"],
            "description": new_desc,
            "changed": changed,
            "notes": " ".join(note_bits),
        })
    for k in REQ_EDITS:
        if k not in used_req:
            problems.append(f"REQ_EDITS key {k} matched no control")
    for k in IMPL:
        if k not in used_impl:
            problems.append(f"IMPL key {k} matched no control")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT} ({len(out)} controls, {sum(o['changed'] for o in out)} changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
