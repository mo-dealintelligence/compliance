# Evidence collection (screenshots, scheduled)

`shot-list.json` is the authoritative list of recurring evidence: one entry per
Comp evidence task with the page to open, what must be visible, the cadence
(monthly/quarterly) and the source system. It was derived from the 45
screenshots + 3 log exports that passed the SOC 2 Type I, so the frames match
what the auditor already accepted.

## Run (Claude scheduled task, on the Mac with Chrome signed in)

1. For every shot due (cadence vs last run in `runs/`), open `url` in Chrome,
   confirm `mustShow` is on screen, capture a full-page screenshot named
   `<file stem>_<YYYY-MM-DD>.png` into a capture folder. For `aws-cli` entries
   run the command and save the JSON. For `mac` entries take a local screenshot.
   For `comp` entries the page is Comp itself.
2. `COMP_API_URL=… COMP_API_KEY=… COMP_USER_ID=… bun evidence/upload.ts <capture folder>`
   attaches each file to its task, marks the task done and writes `runs/<date>.json`.
3. Report anything that could not be captured (sign-in expired, page moved) —
   never skip silently.

Sign-ins needed in Chrome: AWS console (prod account 164482277879), GitHub
(`dealintelligence` org), PropelAuth, Google Admin. Humadroid entries now point
at Comp's own pages (risk register, vendors, BCP) — Humadroid is retired.
