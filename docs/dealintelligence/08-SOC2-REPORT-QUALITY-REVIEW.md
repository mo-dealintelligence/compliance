# 08 — SOC 2 Type I report: quality review and auditor decision (2026-10-31)

Inputs: the issued report (`Deal Intelligence LLC SOC2 Type 1.pdf`, 43 pages,
opinion dated March 3, 2026, as-of date March 2, 2026), the Humadroid-generated
system description draft (Nov 23, 2025, 29 pages), the audited policy set, and
what the platform actually looks like today (05/06/07 in this folder). The
comparison baseline is what reports from established SOC 2 practices
(Schellman, A-LIGN, Prescient, Insight Assurance, Big 4) look like and what
enterprise security reviewers check when they read one.

## Short answer

The report is **structurally correct and will pass most mid-market vendor
reviews**: four AICPA sections, unqualified opinion, correct references
(DC 200 2018 w/ 2022 guidance, TSP 100 2017 w/ 2022 points of focus),
carve-out of AWS and PropelAuth stated properly, CUECs and CSOCs present,
signed by a licensed CPA firm (CA CBA 9916, AICPA 900256001398, peer-review
enrolled). For the price and speed, that is what a boutique firm is for.

It is **not a top-tier report**, and the gap is in the two things a
sophisticated reader looks at first: Section 4 is a generic control catalog
that never names a single real system, and Section 3 is the Humadroid AI draft
pasted in with template leftovers and claims that are not true today. Neither
is fatal for a Type I. Both become a problem in a Type II, because that is
where the same auditor will test 138 generic controls against evidence, and
where customers' security teams read the tests.

**Recommendation:** keep ConstellationGRC for the Type II *only if* they agree
in writing to (a) a Section 4 rewritten from your real control matrix (the 211
controls in Comp, with the system names), (b) a corrected Section 3, and (c)
narrowing scope to Security + Availability + Confidentiality unless you have
a customer demanding Privacy/Processing Integrity. If they push back on (a),
that tells you the catalog is their product, and you should take the Type II
to a mid-tier firm. Either way, verify the firm's peer review status on the
AICPA Peer Review Public File before signing (they say "enrolled"; a completed
peer review is what a bank or enterprise procurement will ask for).

## What a strong report has that this one does not

| Area | Top-tier practice | This report |
|------|-------------------|-------------|
| Section 4 controls | Entity-specific: "Access to the AWS production account requires SSO through Google Workspace with hardware MFA; the `OrganizationAccountAccessRole` is the only cross-account path…" Each control names the system, the owner, the frequency and the evidence. | 138 "CA-nn — The company …" statements. Zero mentions of AWS, PropelAuth, GitHub, Lambda, DocumentDB or CloudWatch anywhere in Section 4. The same CA-numbered catalog, with the same wording, appears in other clients' reports signed by the same CPA (e.g. a public 2025 Type I signed as Lakewood Associates P.C.). |
| Section 3 accuracy | Reviewed line by line by the auditor; claims are tied to evidence. | Verbatim Humadroid draft. "Humadriod" misspelled 7×. Management assertion refers to the "Cybersecurity Services System" (template name). Scope paragraph in Section 1 references "operating effectiveness" for a Type I, then an "Other Matter" paragraph disclaims it. Assertion says the description is as of **February 26**, opinion says **March 2**. Assertion carries no signatory name or title. |
| Claims vs reality | Description matches the environment the auditor saw. | Claims "branch protection rules requiring pull request reviews", "staging environment for pre-production validation", "manual approval gates" — today commits go straight to `main`, CI is red, `deploy.yml` is manual with the build commented out. Claims "multi-availability zone deployments" — the DocumentDB cluster reports `MultiAZ=false`. Claims "distinct AWS accounts" for prod/non-prod — one account is in scope and no non-prod account is named. "100+ verified AWS resources", "220 implemented controls, 86 % automation" are Humadroid dashboard numbers, not something an auditor can verify. |
| Solo-operator disclosure | Stated plainly, with the segregation-of-duties limitation and compensating controls (automation, logging, independent review). | The Nov draft said "solo operator functioning remotely"; the issued report removed that phrase. A Type II reader will find one committer, one AWS user, one approver, and ask why the description did not say so. |
| Subservice organizations | Every material third party listed with carve-out/inclusive treatment. | Only AWS and PropelAuth. GitHub (source and CI), Google Workspace (identity, email), Humadroid/Comp (compliance records), Resend are in the description or in the vendor register but not treated as subservice organizations or explained as non-subservice vendors. |
| System incidents | DC 200 asks for disclosure of significant incidents (or a statement that there were none). | No incidents section. |
| Diagrams | Network/data-flow diagram in Section 3. | None (the text says data-flow diagrams are "maintained"; none is shown). |
| Scope | Security, plus the categories customers ask for. | All five categories for a one-person company. Privacy (P1–P8) alone adds ~18 criteria that will each need operating evidence in the Type II. |

## What is fine

- Opinion, scope and responsibility paragraphs follow the AICPA illustrative
  report; carve-out language is correct; restricted-use paragraph present.
- Policy inventory in Section 3 matches the audited package exactly (22
  published documents) — that part is real and now lives in Comp.
- The CUEC list is reasonable for a data-delivery product (customer-side
  access management, integration security, data handling).
- Turnaround and cost: opinion issued one day after the as-of date.

## Who the auditor is

ConstellationGRC CPA P.C., Huntington Beach, incorporated March 27, 2025
(previously signing as Lakewood Associates P.C.); one managing partner
(Tineyi Gwariwa, CPA, ~10 years audit incl. Deloitte) plus a second
principal; SOC 2 and HIPAA only; Vanta/Sprinto partner; five 5-star G2
reviews from startups citing price and speed. Legitimate, licensed, and
exactly what it says it is: fast, cheap, startup-focused. Not a firm an
enterprise buyer's security team will recognise, which matters only if your
buyers are enterprises with formal TPRM.

## Decision guide

| If your buyers are… | Then… |
|---|---|
| Mid-market revenue teams, MCP/Clay users, Deepgram-size pilots | Keep ConstellationGRC. Fix the content (below). The logo on the cover does not matter; the Section 4 content does. |
| Enterprises with procurement/TPRM (Fortune 1000, banks, public companies) | Move the Type II to a mid-tier firm with a recognised name and a completed peer review. Expect a longer engagement and a real control walkthrough; that is the point. |

## What to fix before any Type II, regardless of firm

1. Section 4 rebuilt from the Comp control matrix (211 controls, verbatim
   descriptions with implementation notes) — the auditor maps those to criteria
   instead of their catalog.
2. Section 3 corrected: spelling, dates, assertion signatory, "Cybersecurity
   Services System", solo-operator disclosure with compensating controls,
   subservice organizations (add GitHub, Google Workspace, Comp; say why
   Resend/others are not subservice orgs), incidents section, network diagram
   (now in Comp), remove numbers you cannot evidence (100+ resources, 220
   controls, 86 %).
3. Make the description true: branch protection + PRs, green CI, a real
   staging path or delete the claim, DocumentDB multi-AZ or reword, ECR
   scan-on-push on all repos (05 §A).
4. Narrow categories to what customers ask for.
5. Confirm peer-review status (AICPA Peer Review Public File) and ask for the
   engagement letter to name the partner who will perform the Type II testing.
