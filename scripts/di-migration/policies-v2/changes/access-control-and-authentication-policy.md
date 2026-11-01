# Change note — access-control-and-authentication-policy (v1.0 → v2.0)

- R0: frontmatter `version` 1.0 → 2.0, publication placeholders for `effective_date` / `review_date`, added `supersedes: "1.0"`; dropped v1 `finalized_at`.
- R0: added §16 Revision history.
- R0/R8: restored run-on bullets into real lists (§2, §4.3, §5.1.2, §5.2.1, §5.2.3, §5.3.1, §6.2, §6.3, §7.1, §13, §14); removed `<u>` artefacts.
- R2: §4.2 Information Security Officer and §4.3 System Administrator merged into §4.1 Chief Executive Officer with every v1 bullet retained; added the R2 statement that the CEO is the only role with production access.
- R2: added §4.2 Go-to-Market Contractor (no production access; browser SSO with MFA; onboarding/training/acknowledgments in the compliance platform portal). v1 §4.4 All Users renumbered to §4.3, text kept.
- R2: §5.2.1 added one line "The Go-to-Market Contractor holds no Administrator or Developer role." (the four RBAC roles are kept as v1 system roles).
- R2: §5.2.3 "Production deployment requires manual approval separate from code commit" → compensating control: pull request on protected `main` with required CI status checks and logged self-review, history in GitHub Actions and CloudTrail, independent review by the external SOC 2 auditor.
- R2: §15 Approval block converted to a single-row table: CEO, `[CONFIRM: date]`.
- R4: §6.3 "AWS Systems Manager Session Manager for EC2 access (no SSH keys)" → Session Manager for the NAT instance used as a bastion (no SSH keys, no public services); other workloads on Lambda and Fargate.
- R4: §6.3 "Resource tagging for access control and cost allocation" → "CloudFormation resource tags for cost allocation" (no access-control / classification tags).
- R5: §3 and §5.1.1 "PropelAuth JWT authentication with multi-factor authentication capabilities" → customer MFA inherited from Google Workspace sign-in via PropelAuth (Google SSO only); personnel MFA enforced in Google Workspace, GitHub and AWS; "Google Workspace sign-in" added to the MFA-required list.
- R5: §5.1.2 "For systems not using PropelAuth SSO" → "For systems not using Google Workspace SSO".
- R5: §7.3 "Security Hub findings reviewed daily" → "reviewed monthly (recorded); critical findings alert in real time via SNS".
- R5: §9.1 "Regular security assessments" → "Annual security assessments".
- R6: §14 footer "Last Review Date: Current / Next Review Date: One year from current date / Version: 2.0" → publication placeholders matching the frontmatter (v1 body said 2.0 while frontmatter said 1.0); removed the `\` line-break artefacts.
- R7: §9.1 "PropelAuth and AWS as approved sub-processors only" → "Approved sub-processors only, as listed in the Vendor Management Policy".
- R7: §9.2 "Third-Party Integration Security Guidelines" → Integration security section of the API Security and Rate Limiting Standard.
- Kept verbatim (no rule applies): §1, session timeouts, password rules, §5.2.2, §5.3.x, §6.1, §6.2, §7.1, §7.2, §8, §10, §11, §12, "Recognizing phishing attempts" as a training topic (not a simulation).

## CONFIRM

- §6.3 "AWS Organizations SCPs limiting high-risk actions" kept verbatim (v1 claim). R3 says to say nothing about accounts; SCPs imply an AWS Organization. Confirm SCPs exist, or delete the bullet.
- §5.2.1 "Developer" and "Read-Only" RBAC roles kept as system roles even though only the CEO holds production access; confirm these roles exist in PropelAuth/IAM or collapse to Administrator + Customer.
- §5.3.3 "Service accounts rotated quarterly" kept; R3 describes Secrets Manager rotation on the DocumentDB credential and API-key rotation per calendar — confirm quarterly is the calendar value.
- §8.1 "Monthly review of security group rules and network ACLs" kept; confirm a monthly record exists in the compliance platform.
- §15 approval date: `[CONFIRM: date]`.
