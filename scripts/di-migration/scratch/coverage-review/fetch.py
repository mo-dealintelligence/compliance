import json, time, sys, os, urllib.request, urllib.error
BASE="https://api.compliance.dealintelligence.io/v1"
KEY=open("/home/claude/secrets/comp-api-key").read().strip()
OUT=__import__("os").environ.get("COVERAGE_OUT","/tmp/coverage-review")
os.makedirs(OUT, exist_ok=True)
last=[0.0]
def get(path):
    for attempt in range(8):
        dt=time.time()-last[0]
        if dt<0.26: time.sleep(0.26-dt)
        last[0]=time.time()
        req=urllib.request.Request(BASE+path, headers={"X-API-Key":KEY,"Accept":"application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code==429 or e.code>=500:
                time.sleep(1.5*(attempt+1)); continue
            print("ERR",path,e.code,e.read()[:300],file=sys.stderr); return None
    raise SystemExit("gave up "+path)

def unwrap(j):
    if isinstance(j,dict):
        for k in ("data","items","results"):
            if k in j and isinstance(j[k],list): return j[k]
    return j

# controls
controls=[]; page=1
while True:
    j=get(f"/controls?limit=50&page={page}")
    items=unwrap(j)
    if not items: break
    controls+=items
    meta=j if isinstance(j,dict) else {}
    print("page",page,len(items),{k:v for k,v in meta.items() if k not in('data','items')},file=sys.stderr)
    if len(items)<50: break
    page+=1
json.dump(controls,open(f"{OUT}/controls.json","w"),indent=1)
for name in ("policies","tasks","frameworks","vendors","risks","people"):
    j=get(f"/{name}")
    json.dump(j,open(f"{OUT}/{name}.json","w"),indent=1)
    print(name, len(unwrap(j)) if isinstance(unwrap(j),list) else type(j),file=sys.stderr)
fw=unwrap(json.load(open(f"{OUT}/frameworks.json")))
for f in fw:
    j=get(f"/frameworks/{f['id']}")
    json.dump(j,open(f"{OUT}/framework_{f['id']}.json","w"),indent=1)
tasks=unwrap(json.load(open(f"{OUT}/tasks.json")))
att={}
for i,t in enumerate(tasks):
    j=get(f"/tasks/{t['id']}/attachments")
    att[t['id']]=j
    if i%50==0: print("att",i,file=sys.stderr)
json.dump(att,open(f"{OUT}/attachments.json","w"),indent=1)
print("done",file=sys.stderr)
