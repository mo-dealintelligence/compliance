import json, csv, re, collections
D=__import__("os").environ.get("COVERAGE_OUT","/tmp/coverage-review")
rows=list(csv.DictReader(open("/home/claude/repos/comp/scripts/di-migration/data/Compliance/controls-list.csv",encoding="utf-8-sig")))
controls=json.load(open(f"{D}/controls.json"))
tasks={t["id"]:t for t in json.load(open(f"{D}/tasks.json"))["data"]}
att=json.load(open(f"{D}/attachments.json"))
attn={k:[(i.get("name") or i.get("fileName")) for i in (v.get("data",v) if isinstance(v,dict) else v) or []] for k,v in att.items()}
policies=json.load(open(f"{D}/policies.json"))["data"]
R={}
print("CSV rows",len(rows), "criteria",sum(1 for r in rows if r["Identifier"].count(".")==1), "subs",sum(1 for r in rows if r["Identifier"].count(".")==2))
idre=re.compile(r"^((?:CC|A|C|PI|P)\d+\.\d+(?:\.\d+)?)\s")
by_id=collections.defaultdict(list)
for c in controls:
    m=idre.match(c["name"])
    if m: by_id[m.group(1)].append(c)
di_controls=[c for c in controls if idre.match(c["name"])]
tmpl=[c for c in controls if not idre.match(c["name"])]
print("controls total",len(controls),"DI-identified",len(di_controls),"template",len(tmpl))
dups={k:v for k,v in by_id.items() if len(v)>1}
print("duplicate ids",dups.keys())
missing=[r["Identifier"] for r in rows if r["Identifier"] not in by_id]
print("1. missing:",missing)
extra=sorted(set(by_id)-{r["Identifier"] for r in rows}); print("DI ids in Comp not in CSV:",extra)

def norm(s): return re.sub(r"\s+"," ",s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"').replace(" "," ")).strip()
# 2. description
desc_miss=[];notes_miss=[];notes_empty=[]; raw_desc_miss=[]
for r in rows:
    c=by_id.get(r["Identifier"]); 
    if not c: continue
    c=c[0]; d=c["description"] or ""
    if r["Description"] not in d:
        raw_desc_miss.append(r["Identifier"])
        if norm(r["Description"]) not in norm(d): desc_miss.append((r["Identifier"], r["Description"][:80], d[:80]))
    n=r["Implementation Notes"].strip()
    if not n: notes_empty.append(r["Identifier"])
    elif n not in d and norm(n) not in norm(d): notes_miss.append((r["Identifier"], n[:80]))
print("2. desc not verbatim (raw):",len(raw_desc_miss), raw_desc_miss[:20]); print("   desc missing after whitespace/quote norm:",len(desc_miss)); 
for x in desc_miss[:10]: print("   ",x)
print("   notes empty in CSV:",len(notes_empty),notes_empty); print("   notes missing:",len(notes_miss)); 
for x in notes_miss[:20]: print("   ",x)
# also check criterion title in description for criterion rows? CSV Title of criterion rows = criterion text; control name uses it.
# 3. mapping
unmapped=[];wrong=[];multi=[]
for r in rows:
    c=by_id.get(r["Identifier"]); 
    if not c: continue
    c=c[0]; ident=r["Identifier"]; parent=".".join(ident.split(".")[:2])
    maps=c.get("requirementsMapped") or []
    socmaps=[m for m in maps if (m.get("frameworkInstance") or {}).get("id")=="frm_6ae439498414d87c6cd98f07"]
    ids=[(m.get("requirement") or m.get("customRequirement") or {}).get("identifier") for m in socmaps]
    if not socmaps: unmapped.append(ident)
    elif parent not in ids: wrong.append((ident,ids))
    if len(maps)>1: multi.append((ident,[ (m.get("requirement") or m.get("customRequirement") or {}).get("identifier") for m in maps]))
print("3. unmapped:",unmapped); print("   wrong parent:",wrong); print("   multi-mapped:",multi)
c12=[(r["Identifier"], [(m.get("customRequirement") or {}).get("identifier"), m.get("customRequirementId")] ) for r in rows if r["Identifier"].startswith("C1.2") for m in by_id[r["Identifier"]][0]["requirementsMapped"]]
print("   C1.2 mappings:",c12)
# 4. evidence
def files(r): return [f.strip() for f in r["Evidence files"].split(",") if f.strip()]
allfiles=collections.Counter(f for r in rows for f in files(r))
print("4. distinct evidence refs:",len(allfiles))
pdf_policy={}
pnames={p["name"].lower():p for p in policies}
# build file->tasks map via attachments
file_tasks=collections.defaultdict(set)
for tid,names in attn.items():
    for n in names: file_tasks[n].add(tid)
ev_missing=[]; ev_noattach=[]; ok=0; policy_pdf_refs=collections.Counter()
POLICY_PDFS={"information-security-policy-v1.0.pdf","access-control-and-authentication-policy-v1.0.pdf","change-management-policy-v1.0.pdf","data-classification-policy-v1.0.pdf","data-retention-and-disposal-policy-v1.0.pdf","code-of-conduct-v1.0.pdf","privacy-notice-and-data-processing-agreement-template-v1.0.pdf","incident-response-procedure-v1.0.pdf","risk-assessment-procedure-v1.0.pdf","business-continuity-plan-v1.0.pdf"}
for r in rows:
    c=by_id.get(r["Identifier"]); 
    if not c: continue
    c=c[0]; ctids={t["id"] for t in c.get("tasks") or []}
    for f in files(r):
        if f in POLICY_PDFS: policy_pdf_refs[f]+=1; continue
        linked=ctids & file_tasks.get(f,set())
        if linked: ok+=1
        else:
            # task linked by title?
            titled=[tasks[t]["title"] for t in ctids if t in tasks and (f.rsplit(".",1)[0].replace("_"," ").lower() in (tasks[t]["title"]+" "+(tasks[t]["description"] or "")).lower())]
            ev_missing.append((r["Identifier"],f,titled))
print("   evidence refs satisfied:",ok,"missing:",len(ev_missing))
mc=collections.Counter(f for _,f,_ in ev_missing); print("   missing by file:",mc)
# 5. policy PDF refs -> policy link
pdf2pol={"information-security-policy-v1.0.pdf":"information security policy","access-control-and-authentication-policy-v1.0.pdf":"access control","change-management-policy-v1.0.pdf":"change management policy","data-classification-policy-v1.0.pdf":"data classification","data-retention-and-disposal-policy-v1.0.pdf":"data retention","code-of-conduct-v1.0.pdf":"code of conduct","privacy-notice-and-data-processing-agreement-template-v1.0.pdf":"privacy notice","incident-response-procedure-v1.0.pdf":"incident response","risk-assessment-procedure-v1.0.pdf":"risk assessment","business-continuity-plan-v1.0.pdf":"business continuity"}
pol_miss=[]; pol_ok=0; pol_extra=[]
for r in rows:
    c=by_id.get(r["Identifier"]); 
    if not c: continue
    c=c[0]; lp=[p["name"].lower() for p in c.get("policies") or []]
    refs=[f for f in files(r) if f in POLICY_PDFS]
    for f in refs:
        if any(pdf2pol[f] in n for n in lp): pol_ok+=1
        else: pol_miss.append((r["Identifier"],f,lp))
    for n in lp:
        if not any(pdf2pol[f] in n for f in refs): pol_extra.append((r["Identifier"],n,refs))
print("5. policy refs ok:",pol_ok,"missing:",len(pol_miss)); 
for x in pol_miss: print("   ",x)
print("   policies linked with no CSV ref:",len(pol_extra)); 
for x in pol_extra[:40]: print("   ",x)
# 6 policies
print("6. policies:",len(policies))
for p in sorted(policies,key=lambda p:(p["status"],p["name"])):
    cl=len(json.dumps(p["content"])) if p["content"] else 0
    print("   ",p["status"],"|",p["name"],"| tmpl" if p["policyTemplateId"] else "| custom","| content",cl,"| sign",p["isRequiredToSign"],"signedBy",len(p["signedBy"] or []),"| archived",p["isArchived"])
# 8 misc
print("8. empty descriptions:",[c["name"] for c in controls if not (c["description"] or "").strip()])
namec=collections.Counter(c["name"] for c in controls); print("   dup names:",[k for k,v in namec.items() if v>1])
# template controls mapped to SOC2
tm=[(c["name"],[(m.get("requirement") or m.get("customRequirement") or {}).get("identifier") for m in c["requirementsMapped"] if (m.get("frameworkInstance") or {}).get("id")=="frm_6ae439498414d87c6cd98f07"]) for c in tmpl]
tm=[x for x in tm if x[1]]
print("   template controls mapped to SOC2:",len(tm)); 
for x in tm: print("    ",x)
# tasks: DI tasks vs template
di_tasks=[t for t in tasks.values() if not t["taskTemplateId"]]; tt=[t for t in tasks.values() if t["taskTemplateId"]]
print("   tasks: custom",len(di_tasks),"template",len(tt))
print("   custom tasks without attachments:",[(t["title"],t["status"]) for t in di_tasks if not attn.get(t["id"])])
print("   template tasks status:",collections.Counter(t["status"] for t in tt))
print("   custom tasks status:",collections.Counter(t["status"] for t in di_tasks))
# tasks with attachments but not linked to any control
linked=set(t["id"] for c in controls for t in c.get("tasks") or [])
print("   custom tasks not linked to any control:",[tasks[t]["title"] for t in tasks if t not in linked and not tasks[t]["taskTemplateId"]])
# DI controls with no tasks and no policies
print("   DI controls with no tasks and no policies:",len([c for c in di_controls if not c["tasks"] and not c["policies"]]),[c["name"][:30] for c in di_controls if not c["tasks"] and not c["policies"]])
json.dump({"ev_missing":ev_missing,"pol_miss":pol_miss,"pol_extra":pol_extra,"desc_miss":desc_miss,"notes_miss":notes_miss},open(f"{D}/findings.json","w"),indent=1)
