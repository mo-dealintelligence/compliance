# third-party-integration-security-guidelines — v1.0 → MERGED (no v2)

- R7: document retired; `policies-v2/third-party-integration-security-guidelines.MERGED.md` written with a section-by-section destination table.
- R7: §1, §2 (integration bullets), §3, §5.2–§5.4, §6, §7, §8, §9, §10, §11 → API Security and Rate Limiting Standard v2.0 §8 "Integration Security" (and §2, §11). Rule-driven edits applied there are listed in `changes/api-security-and-rate-limiting-standard.md` (mutual TLS, certificate pinning, DLQ, quarterly endpoint scans, 5 s p95, 7-day high timeline, Legal hold, roles).
- R7: §5.1 Pre-Integration Assessment table, DPA requirements (§10.1 GDPR processor agreements), §6/§8.3 "not a sub-processor" statement, and §9.2 third-party breach response steps → Vendor Management Policy v2.0 §5.3, §6.1, §8.3 and §9.2.
- R1: "PI1.1 (Processing Integrity)" mapping in §1 dropped during the merge.
- R2: §4.2 Technical Integration Lead and §4.3 Security Operations consolidated into the CEO.
- R4: §12 / §13 (related documents, review) not carried over; destination documents have their own.

## CONFIRM

- Other v2 documents that still list "Third-Party Integration Security Guidelines" in their Related Documents (v1 Security Awareness Training Program, Vendor Management Policy, API Security Standard did; others may) need the reference repointed to API Security and Rate Limiting Standard §8 or Vendor Management Policy.
