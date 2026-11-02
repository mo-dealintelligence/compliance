#!/usr/bin/env python3
"""Cross-set lint for the v2 policy documents against RULEBOOK.md.

Flags, per file: forbidden size/headcount language (R2), roles that must not
exist (R2), PI/Privacy TSC references (R1), removed products/claims (R4),
leftover placeholders (R6), number conflicts (R5) and missing frontmatter
fields (R0). Exit code 1 if any hard finding. Run from anywhere:

    python3 scripts/di-migration/policies-v2/check.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = sorted(p for p in HERE.glob("*.md") if p.name not in {"RULEBOOK.md", "CHANGES.md", "DECISIONS-2026-10-31.md"} and ".MERGED." not in p.name)

HARD = {
    "R2 size": [r"\bsolo\b", r"\bsole operator", r"\bsole[- ]person", r"\bone[- ]person\b", r"\bsingle[- ]person\b",
                r"\btwo[- ]person\b", r"\bsmall (team|company|organi[sz]ation|business)\b", r"\bheadcount\b",
                r"\bnumber of (employees|staff|people)\b", r"organi[sz]ation'?s? (small )?size\b", r"\bgiven (the|our) size\b",
                r"\blimited (staff|personnel|team size)\b", r"\ball employees\b", r"\bemployee(s)? and contractor(s)?\b"],
    "R2 roles": [r"\bCISO\b", r"\bChief Information Security Officer\b", r"\bSecurity Lead\b", r"\bSecurity Officer\b",
                 r"\bSystem Owner\b", r"\bSecurity Operations\b", r"\bSecOps\b", r"\bTechnical Operations Lead\b",
                 r"\bCompliance Officer\b", r"\bDevOps\b", r"\bDevelopment Team\b", r"\bEngineering Team\b", r"\bProcurement\b",
                 r"\bIT Operations\b", r"\bHuman Resources\b", r"\bHR\b", r"\bLegal Counsel\b", r"\bData Protection Officer\b",
                 r"\bDPO\b", r"\bPrivacy Operations\b", r"\bChange Advisory Board\b", r"\bCAB\b", r"\bIncident Response Team\b",
                 r"\bIRT\b", r"\bBoard of Directors\b", r"\bpeer review(er|ers)?\b", r"\bon-call personnel\b", r"\bSysAdmin\b",
                 r"\bCTO\b", r"\bInformation Security Officer\b"],
    "R1 PI/P": [r"\bPI1(\.\d)*\b", r"\bP[1-8]\.\d(\.\d)?\b", r"\bProcessing Integrity\b", r"\bPrivacy (criteria|category|Trust Services)\b",
                r"\b(all )?five (Trust Services )?(categories|criteria)\b"],
    "R4 removed": [r"\bWAF\b", r"\bGuardDuty\b", r"\bAWS Config\b", r"\bConfig rules?\b", r"\bInspector\b", r"\bEBS\b",
                   r"\bCloudWatch Agent\b", r"\bTransit Gateway\b", r"\bPrivateLink\b", r"\bVPC peering\b", r"\bcross-region\b",
                   r"\bmulti-region\b", r"\bimage signing\b", r"\bcertificate pinning\b", r"\bmutual TLS\b", r"\bmTLS\b",
                   r"\bSynthetics\b", r"\bcanar(y|ies)\b", r"\bstatus page\b", r"\bblue[- ]green\b", r"\bload balancer",
                   r"\bauto[- ]scaling group", r"\bcircuit breaker", r"\bread replica", r"\bphishing simulation", r"\bLMS\b",
                   r"\bquiz", r"\bnewsletter", r"\bsecurity champion", r"\bcyber[- ]?insurance", r"\bplaybook", r"\bWebSocket",
                   r"\bDLQ", r"\bdead[- ]letter", r"\bDAST\b", r"\b80\s?% (test |code )?coverage", r"\busage plan", r"\bPremium tier",
                   r"\bTerraform\b", r"\blegal[- ]hold (registry )?Lambda", r"\bVPN\b", r"\bendpoint (protection|detection)", r"\bEDR\b",
                   r"\bMDM\b", r"\bHumadroid", r"\bHumadriod", r"\b86\s?%", r"\b220 (implemented )?controls", r"\b100\+ ", r"\bStandard Change Catalog",
                   r"\bConsent Management Procedure", r"\bInfrastructure and Recovery Policy", r"\bmaintained separately",
                   r"\bEC2 instances?\b", r"\bSSH\b", r"\b(daily|every day) (security |alert )?review", r"\bquarterly tabletop",
                   r"\b48[- ]hour (CAB|review)", r"\b15[- ]minute", r"\b24/7\b", r"\bdistinct AWS accounts?",
                   r"\bPropelAuth MFA", r"\b99\.95\s?%",
                   # D26 (2026-11-01): no Multi-AZ DocumentDB
                   # D27 (2026-11-01): backups 35 days; no automatic recovery claimed for AZ outages
                   r"\b90[- ]day (automated )?backups?\b", r"\bbackups? retained 90\b", r"\bre-provision",
                   r"\bautomatic instance recovery\b",
                   r"\bMulti-AZ\b", r"\bsecond (DocumentDB )?instance\b", r"\bstandby instance", r"\bfailover of DocumentDB",
                   r"\bfail ?over to the (second instance|alternate availability zone)"],
    "R6 placeholders": [r"dealintelligence\.ai\b", r"\[Maintained Separately\]", r"\[YES\]", r"\[NO\]", r"Document Assignments",
                        r"\(Chief Executive Officer\)", r"di-backendapi", r"AIpowered", r"\[Original Date\]", r"\[Current Date\]"],
}
SOFT = {
    "R5 numbers": [r"\b7[- ]day backup", r"\b30[- ]minute RPO", r"\b10 business days", r"\b24[- ]hour(s)? (notification|notice)",
                   r"\b2[- ]year", r"\b5 seconds", r"\b5s p95", r"\b7 years after (account )?closure", r"\btraining within \d+ days",
                   r"\bsuspend", r"\bsemi-annual rotation audit", r"\bquarterly (vendor|SLA|performance) review"],
    "R0 confirm": [r"\[CONFIRM"],
}
FRONT = ["title", "doc_type", "version", "acknowledgment", "effective_date", "review_date", "author", "source", "supersedes"]


def main() -> int:
    hard_total = 0
    for f in FILES:
        text = f.read_text(encoding="utf-8")
        findings = []
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        if not m:
            findings.append(("R0 frontmatter", "missing", 0))
        else:
            fm = m.group(1)
            for key in FRONT:
                if not re.search(rf"^{key}:", fm, re.M):
                    findings.append(("R0 frontmatter", f"missing `{key}`", 0))
            if not re.search(r'^version:\s*"?2\.', fm, re.M):
                findings.append(("R0 frontmatter", "version not 2.x", 0))
        if "Revision history" not in text and "Revision History" not in text:
            findings.append(("R0 revision", "no Revision history section", 0))
        lines = text.split("\n")
        for group, pats in list(HARD.items()) + list(SOFT.items()):
            for pat in pats:
                rx = re.compile(pat, re.I)
                for i, line in enumerate(lines, 1):
                    if rx.search(line):
                        # allow mentions inside the Revision history row that describes the removal
                        if re.search(r"^\|?\s*2\.0", line) and group not in ("R6 placeholders",):
                            continue
                        # reviewed false positives: the compensating-control wording itself,
                        # vendor facts (AWS Support 24/7, PropelAuth status page), alarm
                        # evaluation windows, the TSP 100 title, user-entity CUEC wording
                        if re.search(r"no SSH|PropelAuth status page|AWS Support|AWS \|.*24/7|for 15 minutes|CloudWatch monitoring|"
                                     r"Trust Services Criteria for Security, Availability, Processing Integrity|User entities|"
                                     r"not examined as SOC 2 Privacy|endpoint devices accessing|network security controls", line):
                            continue
                        findings.append((group, f"`{pat}` L{i}: {line.strip()[:110]}", i))
        hard = [x for x in findings if not x[0].startswith(("R5", "R0 confirm"))]
        hard_total += len(hard)
        wc = len(text.split())
        print(f"\n== {f.name}  ({wc} words)  hard={len(hard)} soft={len(findings)-len(hard)}")
        for g, msg, _ in findings:
            print(f"  [{g}] {msg}")
    print(f"\n{len(FILES)} files, {hard_total} hard findings")
    return 1 if hard_total else 0


if __name__ == "__main__":
    sys.exit(main())
