# security-awareness-training-program — v1.0 → v2.0 change note

Rewritten to one page per R7; the v1 16-section document is reduced to Purpose, Scope, Training Requirements, Evidence and Records, Related Documents, Review, Revision history.

- R0: `doc_type` Policy → Program; `version` 1.0 → 2.0; `supersedes: "1.0"`; placeholders for dates; `finalized_at` dropped; Revision history added.
- R4: §1 "commitment to maintaining 86% control automation while addressing human factor risks through comprehensive education and continuous reinforcement" removed.
- R2/R7: §2 Scope reduced to one sentence naming all personnel, the CEO and the Go-to-Market Contractor; "Specialized training for high-risk roles including system administration and data processing" removed.
- R4: §3.1 "within 5 business days of system access provisioning" and module durations ("2 hours") removed → onboarding training in the compliance platform portal before access to company data.
- R4/R7: §3.2 annual refresher kept; "before December 31st each year" simplified to "annually"; delivery methods (quarterly bulletins, monthly tips, post-incident briefings) removed.
- R7: §3.3 Role-Based Specialized Training, §10 Specialized Security Topics (cloud, AI/ML, supply chain), §12 Compliance and Regulatory Training, §14 Emergency Security Training removed.
- R4: §4.x content condensed to one topic list; §4.1 "MFA enrollment and usage via PropelAuth" → "multi-factor authentication enforced in Google Workspace, GitHub and AWS" (R5); §4.2 "24-month retention requirements for active leads" dropped from the topic list (retention lives in Data Retention and Disposal Policy); §4.3 phishing awareness kept as a training topic (only simulations removed); §4.4 "VPN usage", "Mobile device security requirements" → "company data accessed only through browser SSO (Google Workspace) and the AWS console/CLI with MFA"; §4.5 "Immediate reporting requirements (within 4 hours)" dropped (R5 has no 4-hour reporting value), 48-hour customer notification kept.
- R4: §5.1 LMS feature list (knowledge checks, reminders, mobile design), §5.2 Simulated Security Exercises (phishing simulations, quiz competitions, tabletop in a training context), §5.3 Just-In-Time Training removed.
- R4: §6 Training Effectiveness Measurement (80% passing score, surveys, phishing click-rate target <5%, behavioral metrics, benchmarking) removed.
- R4/R7: §7 Training Records — condensed to "completion certificate issued by the compliance platform is the evidence"; retention periods (indefinite/3 years/90 days/7 years) replaced with a reference to Data Retention and Disposal Policy; "scores" dropped (no quizzes).
- R4: §8 Non-Compliance Management (escalation at +3 days, access suspension at +7 days, re-assessment within 5 business days, performance improvement plans) removed → "Training completion is tracked by the CEO; outstanding training is followed up until complete".
- R4/R7: §9.1 contractor training (1-hour abbreviated module, 12-month threshold) → contractor acknowledgment of the Acceptable Use Policy and confidentiality obligations in the compliance platform portal at onboarding and annually; §9.2 vendor security awareness removed (vendor requirements live in Vendor Management Policy).
- R4: §11 Security Culture Development (security champions, monthly newsletter, tip of the week) removed.
- R7: §13 Training Program Governance (quarterly metrics review, budget, benchmarking, conference participation, certifications) removed.
- R7: §15 Related Documents reduced to the six documents referenced in the body; §16 Review condensed to one sentence (annual).

## CONFIRM

- The compliance platform issues a completion certificate for the security-awareness training (used as the evidence statement in §4).
- Contractor acknowledgment cadence: v2 says "at onboarding and annually" for the AUP/confidentiality acknowledgment; confirm this matches the Acceptable Use Policy v2 and the Code of Conduct annual acknowledgment (R6).
- Onboarding training "before being granted access to company data" — v1 allowed 5 business days after provisioning; confirm the stricter gating is the intended practice.

## Quality sweep (2026-10-31)

- Q1 voice: §1 rewritten to plain declarative (removed "establishes mandatory requirements… ensures… operationalizes"); "shall" removed ×3; "password manager utilization" → "password manager use"; "prohibition of credential sharing" → "no credential sharing"; §6 review sentence shortened.
- Q2 consistency: "Chief Executive Officer (CEO)" on first use (§2); "the" added before document titles (×6); Oxford commas (×2); all headings to sentence case; Revision history numbered.
- Q3 structure: Review moved before Related documents (§5/§6 swapped); Revision history → §7.
- No commitment, number, role, scope item or control changed.

### CONFIRM (new)

- None added.
