# Comp API reference for the SOC 2 importer

See `scripts/di-migration/README.md` for how this is used. Summary of the
endpoints the importer relies on (all under `/v1`, header `X-API-Key`):

- API keys: `POST /organization/api-keys` `{name, expiresAt:'never', scopes:[...]}`; key auth carries only its scopes (use the "Full Access" preset).
- Org: created in the UI (`/setup`); `PATCH /organization` for settings; SOC 2 framework via `POST /frameworks {frameworkIds}` (seed id `frk_683f377429b8408d1c85f9bd`), instance via `GET /frameworks`.
- Requirements: `GET /frameworks/:fiId` → `requirementDefinitions[]` with `identifier` like `CC1.1`.
- Controls: `POST /controls {name, description, requirementMappings:[{requirementId, frameworkInstanceId}]}`; link policies/tasks with `POST /controls/:id/policies/link` and `/tasks/link`, each called with and without `?frameworkInstanceId=` (framework view reads the instance-scoped links). No PATCH on controls.
- Tasks (evidence): `POST /tasks {title, description, frequency?, department?}` → `PATCH /tasks/:id {status:'done'}`; attachments `POST /tasks/:id/attachments {fileName, fileType, fileData(base64)|s3Key, userId}` (userId required for API keys; 100 MB max; presign via `POST /uploads/presign`).
- Policies: `POST /policies {name, content:[tiptap nodes], status:'published', isRequiredToSign, frequency:'yearly', department, signedBy:[memberIds]}`; versions under `/policies/:id/versions`. `visibility` is UI-only.
- Vendors: `POST /vendors {name, description, category, status, isSubProcessor, inherent*/residual*}` (triggers an AI assessment task); `PATCH` for treatment.
- Risks: `POST /risks {title, description, category, likelihood, impact, residualLikelihood, residualImpact, treatmentStrategy, status}`.
- People: `POST /people/invite {invites:[{email, roles:['employee'], sendPortalEmail:false}]}` creates employee members immediately; `GET /people` for ids; training completion is session-only (attach certificates as task evidence instead).
- Comments: `POST /comments {content, entityType:'task'|'policy'|'vendor'|'risk', entityId, userId}` (no comments on controls → implementation notes go in the control description).
- Context (auditor view Q&A): `POST /context {question, answer}`.
- Evidence export: `GET /tasks/:id/evidence/export`, `POST /evidence-export/all`.
