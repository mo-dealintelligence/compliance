# SOC 2 descoping — Processing Integrity (PI1) and Privacy (P1–P8)

Decision: Mo, 2026-10-31. The SOC 2 Type II scope is Security, Availability
and Confidentiality. The 75 controls below (17 PI, 58 P) were removed from
Comp (compliance.dealintelligence.io) together with the 6 evidence tasks that
only they cited. Everything is preserved here verbatim so the category can be
restored (the import scripts in scripts/di-migration recreate controls from
removed-controls.json).

Files
- removed-controls.csv / .json — identifier, section, verbatim description
  (incl. implementation notes), evidence files cited, policies linked, Comp id.
- Evidence files cited only by these controls (still in Drive under
  Compliance/evidence): 02_github_ci_workflow.png, aws_eventbridge_rules.png,
  middleware_py_screenshot.png, models_collections_py_screenshot.png,
  models_pii_py_screenshot.png, models_v1_py_screenshot.png.
- No policy was linked only from these controls; all 24 policies remain.

Code these controls referenced (kept — it is product/operations code, no
compliance-specific overhead):
- app/server/models/v1.py, models/pii.py (Pydantic models, PII validators)
- app/server/middleware.py (AuditLoggingMiddleware, SecurityHeadersMiddleware)
- compliance/data_retention_handler.py (Lambda dataRetentionEnforcement — kept
  for the GDPR/CCPA retention obligation)
- compliance/privacy_monitor.py, processing_integrity_monitor.py (never
  deployed; can be deleted or kept as reference)
- GitHub Actions ci.yml, DocumentDB backup/KMS settings (used by the remaining
  Security/Availability/Confidentiality controls anyway)

Execution log
- 2026-10-31: Drive archive created — folder "SOC 2 descoped — Processing
  Integrity and Privacy (2026-10-31)" (README + part1–part5 sheets, 15
  controls each) under Compliance.
- 2026-10-31: `bun import/descope-pi-privacy.ts --apply` deleted 75 controls
  and 6 evidence tasks from Comp. Live after: 136 controls, 50 tasks, all 38
  Security/Availability/Confidentiality requirements still mapped; the 26 PI/P
  requirement definitions remain in the seeded SOC 2 framework, unmapped
  (Comp has no out-of-scope flag). Ids moved to `descoped` in
  data/import-state.json.
