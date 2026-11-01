# Change note — change-management-policy (v1.0 → v2.0)

- R0: frontmatter `version` 1.0 → 2.0, publication placeholders, added `supersedes: "1.0"`; dropped v1 `finalized_at`. `doc_type` left as "Policy" and title unchanged (every other document cross-references "Change Management Policy"); the review model inside is now the PR + CI-gate standard.
- R0: fixed the repeated "#### 1." numbering artefacts in §5.3, §5.4 and §6 into 1/2/3.
- R0: added §13 Revision history.
- R0/R8: restored run-on bullets into real lists (§2, §4.1, §5.1, §5.3, §5.4, §6, §7.1, §9.2, §11, §12); removed `<u>` artefacts.
- R2/R5: §3 "Change Advisory Board (CAB)" definition (with the "(Chief Executive Officer)" missing-name artefact, R6) deleted → new "Pull-Request Review" definition: PR against protected `main` of `dealintelligence/di-backend-api`, required GitHub Actions status checks (lint, tests, Bandit, Trivy, TruffleHog), logged self-review, CEO merges as final approver, no direct pushes (R8 repo name and CI).
- R2/R5: §3 Normal Change "through the Change Advisory Board process" → "through the pull-request review process"; Emergency Change "following expedited approval procedures" → "pull request labelled `emergency` with post-hoc review within 5 business days".
- R2: §4.1 "Serves as Change Advisory Board Chair / Reviews and approves all normal and emergency changes" → "Serves as final approver for all production changes and merges all normal and emergency change pull requests"; §4.2 Technical Implementation Lead and §4.3 Compliance Officer merged into §4.1 CEO with every v1 bullet retained.
- R2: added §4.2 Go-to-Market Contractor (no production access, no change role) and §4.3 External SOC 2 Auditor (independent review of change records, the R2 compensating control).
- R2: §5.3 "Code review via GitHub pull request" → "Logged self-review in the GitHub pull request"; CI scanners named (Bandit, Trivy, TruffleHog).
- R2: §10 "CEO, serving in all technical and compliance roles, maintains" → "The CEO maintains" (removed the size-implying clause).
- R3: §5.4 "Staging environment validation" → "Validation in the staging stage of the CloudFormation stack (no production data; scrubbed or synthetic data only)". Nothing said about accounts.
- R3/R4: §5.4 "Incremental deployment using blue-green or canary strategies" → "Deployment from a green CI run using Lambda versioned deployments, with rollback via `serverless rollback`".
- R4: §1 removed "and 86% control automation rate".
- R4: §5.2 "Pre-approved changes listed in the Standard Change Catalog" → "Pre-approved changes of the types listed below" (catalog does not exist).
- R4: §5.2 "Automated security patches via AWS Systems Manager" (EC2-fleet patching) → "Automated dependency updates proposed by GitHub Dependabot that pass all required CI status checks".
- R4: §5.4 "Follow documented runbooks and procedures" → "Follow the procedures documented in this policy and in the pull request"; §5.5 "Update runbooks and procedures as needed" → "Update procedures as needed".
- R4: §7.1 "CloudFormation drift detection for infrastructure changes AWS Config rules for compliance monitoring" → "CloudFormation (`serverless deploy`) as the only infrastructure change path, with drift reporting" + "Security Hub configuration checks for compliance monitoring".
- R5: §5.2 Normal "Approval: CAB review required, minimum 48-hour review period" → "Pull-request review required; all required CI status checks must pass before merge to `main`".
- R5: §5.2 Emergency "Approval: Expedited CAB approval, post-implementation review within 24 hours" → "Pull request labelled `emergency`; post-hoc review within 5 business days".
- R5: §6 "CEO authorizes emergency change verbally or via email" → "CEO opens a pull request labelled `emergency` against the protected `main` branch; required CI status checks still apply"; "Full CAB review within 48 hours" → "Post-hoc review recorded in the pull request within 5 business days". "Complete change request within 24 hours" kept.
- R6: §2 "di-backendapi-prod" → "di-backend-api-prod".
- R3: §7.1 "Branch protection rules enforcing pull request reviews" → "Branch protection on `main` requiring a pull request and required CI status checks (lint, tests, Bandit, Trivy, TruffleHog); no direct pushes".
- R8: §5.1 "tracked through the CI/CD pipeline" → "tracked through the associated pull request and the CI/CD pipeline".
- Kept verbatim (no rule applies): §1 first paragraph, §2 lists, Standard Change / Change / Change Window definitions, §5.1 request contents, §5.3 security and business review, §5.4 pre-implementation notice (72 hours) and validation, §5.5 timing, §8, §9, §11, §12.

## CONFIRM

- §5.5 "Update configuration management database" kept verbatim; no CMDB is named anywhere in the rulebook. Confirm whether this should read "Confirm the CloudFormation stack reflects the deployed configuration" or be deleted.
- §5.2 Standard change "Automated dependency updates proposed by GitHub Dependabot that pass all required CI status checks" is my substitution for SSM patching; confirm Dependabot PRs are treated as pre-approved standard changes (otherwise move them to Normal).
- §3 Change Window "2:00 AM - 6:00 AM EST" and §5.4 "minimum 72 hours" customer notice kept verbatim; confirm these are still operated.
- Title/doc_type: brief said "PR + CI-gate standard"; kept title "Change Management Policy" and `doc_type: Policy` because cross-references use that name. Confirm if a rename to "Change Management Standard" is wanted (would require updating references in every other document).
- R3 note for CHANGES only: `[CONFIRM: separate account vs same account]` for the staging stage.
