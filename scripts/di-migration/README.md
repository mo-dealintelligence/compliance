# di-migration — Humadroid SOC 2 export → Comp

Everything under `data/` is git-ignored (internal compliance material).

```
# 0. source material (Google Drive "Deal Intelligence/Compliance") → data/
#    (done with save_drive_result.py via the Drive MCP; see manifest.json)
# 1. policies: PDF → Markdown → TipTap
python3 -I pdf_to_md.py data/Compliance/evidence/policies-procedures data/markdown
node md_to_tiptap.mjs data/markdown data/tiptap
# 2. plan: controls matrix + documents + evidence files → data/import-plan.json
bun import/plan.ts
# 3. import into Comp (idempotent; state in data/import-state.json)
COMP_API_URL=https://compliance-api.dealintelligence.io COMP_API_KEY=comp_... \
COMP_USER_ID=usr_... COMP_MEMBER_ID=mem_... bun import/run.ts [--dry-run] [--only=policies,controls]
```

Mapping decisions:
- One Comp control per TSC criterion row of the matrix (61), named `<id> <criterion>`, description = criterion + the DI sub-controls and implementation notes, mapped to Comp's SOC 2 requirement with the same identifier.
- Policies/procedures/plans (10) become editable, published policies (acknowledgment required where Humadroid had "Explicit"). Records (8: minutes, certificates, evaluation, job descriptions, org structure) become done evidence tasks with the PDF attached.
- Every screenshot/log referenced by the matrix becomes one done evidence task with the file attached, linked to each control that cites it.
- Vendors, people and auditor-view context come from `import/seed-data.ts`.
- Comp's own SOC 2 template controls/policies/tasks stay (they drive recurring Type 2 evidence); DI's controls sit next to them.
