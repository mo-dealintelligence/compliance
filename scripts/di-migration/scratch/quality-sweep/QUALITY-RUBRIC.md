# Quality and tone rubric — compliance content sweep (2026-10-31)

Applies on top of `policies-v2/RULEBOOK.md` (content rules R0–R8 stay
binding). This rubric governs *how it reads*. The audience is an external
auditor and a customer's security reviewer; the voice is one organisation
speaking plainly about what it does.

## Q1. Voice
- Plain, declarative, present tense: "The CEO reviews access quarterly."
  Not "The organization shall endeavor to ensure that…".
- Specific over generic: name the system, the record, the cadence, the
  owner. A sentence that could appear in any company's policy is a
  candidate for deletion.
- One idea per sentence; prefer < 30 words. No stacked adjectives.
- Marketing / filler words removed: comprehensive, robust, state-of-the-art,
  cutting-edge, best-in-class, world-class, seamless, holistic, leverage
  (verb), synergy, proactive(ly) (unless contrasted with reactive),
  ensure that (→ plain verb), in order to (→ to), utilize (→ use),
  "it is important to note", "as previously mentioned".
- No AI-template cadence: no paragraph that only restates the heading, no
  "This section describes…", no closing summaries that repeat the section.
- No hedging that weakens a control ("where feasible", "as appropriate",
  "may be") unless the hedge is the actual rule — then say the condition.

## Q2. Consistency (across the whole set)
- Names: Deal Intelligence (first mention "Deal Intelligence LLC"), AWS,
  Amazon DocumentDB → "DocumentDB", AWS Lambda → "Lambda", Amazon ECS
  (Fargate) → "Fargate", CloudWatch, CloudTrail, Security Hub, KMS, ACM, S3,
  CloudFront, SNS, EventBridge, Secrets Manager, Systems Manager Session
  Manager → "SSM Session Manager", PropelAuth, Google Workspace, GitHub,
  GitHub Actions, Dependabot, Resend, "the compliance platform" (never Comp
  or Humadroid in published text), "compliance platform portal".
- Roles: "Chief Executive Officer (CEO)" on first use, "the CEO" after;
  "Go-to-Market Contractor"; "personnel" (not staff/employees/team members).
- Document titles referenced exactly as their `title:` frontmatter.
- Numbers: digits (24 hours, 90 days, 99.9 %); "p95"; durations as
  "within 24 hours"; dates "November 13, 2025"; times "02:00 UTC"
  (not EST/EDT unless the customer-facing window needs local time —
  then give both).
- Severity scale: P1–P4 everywhere (incident) and Critical/High/Medium/Low
  (vulnerability) — do not mix.
- Headings: numbered `## 1.` top level, `### 1.1` second; no `####` single
  "1." leftovers; sentence case after the number.
- Lists: parallel grammar; bullets are fragments or full sentences, not
  mixed within one list; no blank line between bullets of the same list.
- Tables: header row, no empty cells (use "—").
- Spelling: American. Oxford comma used.

## Q3. Structure (policies)
Purpose → Scope → Definitions (only if used) → Roles and responsibilities →
the controls/procedure → Monitoring/metrics (only if a record exists) →
Exceptions → Related documents → Revision history. Delete sections that
have no content of their own (e.g. "Compliance" sections that only say the
policy supports SOC 2). Related-documents lists must only name documents
that exist in the set.

## Q4. Records (minutes, evaluations, job descriptions, org structure,
ethics log, certificates, risks, vendors, context answers, tasks, controls)
- Minutes read as minutes: date, attendees by role, agenda, decisions,
  actions with owner and due date. No narrative self-praise.
- Evaluations: criteria, rating, evidence, development actions. Factual.
- Job descriptions: purpose, responsibilities, access level, required
  acknowledgments; no recruiting copy.
- Risk/vendor descriptions: what the risk is, what it affects, the
  treatment, the owner (CEO); likelihood/impact words match the scale used
  in the Risk Assessment Procedure.
- Control descriptions (the "Implementation:" note): one or two sentences
  naming the mechanism and the evidence record. No "Given the
  organization's size…", no vendor products that were removed (R4), no
  stale numbers (R5), no Humadroid.
- Task titles: noun phrases naming the evidence ("CloudWatch alarms
  screenshot"), not filenames; descriptions say what to capture and how
  often.
- Context answers (onboarding Q&A): short, factual, current; the
  headcount answer is a platform field, leave the number but make sure no
  other text repeats it.

## Q5. What not to do
- Do not change meaning, commitments, numbers, or scope — that is the
  rulebook's job and it is already applied. If a quality fix would change
  a commitment, leave the text and add it to the CONFIRM list.
- Do not shorten for its own sake; cut only filler, duplication and
  generic text.
- Do not invent records, dates, or names.
