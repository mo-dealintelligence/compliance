#!/usr/bin/env python3
"""Pull a read-only snapshot of the Comp org for the readiness audit.
usage: COMP_API_URL=... COMP_API_KEY=... python3 fetch.py <out dir>"""
import json, os, sys, time, urllib.request, urllib.parse
U = os.environ['COMP_API_URL'].rstrip('/') + '/v1'
K = os.environ['COMP_API_KEY']
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
def get(path, **q):
    for attempt in range(8):
        url = U + path + ('?' + urllib.parse.urlencode(q) if q else '')
        req = urllib.request.Request(url, headers={'X-API-Key': K})
        try:
            with urllib.request.urlopen(req, timeout=60) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(5 * (attempt + 1)); continue
            return {'_error': e.code, '_body': e.read().decode()[:300]}
    return {'_error': 'throttled'}
def list_all(path, **q):
    items = []
    for page in range(1, 100):
        r = get(path, page=page, perPage=100, **q)
        data = r.get('data', r) if isinstance(r, dict) else r
        if not isinstance(data, list): return {'_raw': r}
        items += data
        if len(data) < 100: break
    return items
snap = {}
for name, path in [('controls', '/controls'), ('policies', '/policies'), ('tasks', '/tasks'), ('risks', '/risks'),
                   ('vendors', '/vendors'), ('people', '/people'), ('frameworks', '/frameworks'),
                   ('findings', '/findings'), ('evidence_forms', '/evidence-forms'),
                   ('evidence_statuses', '/evidence-forms/statuses'), ('integrations', '/integration-platform/integrations'),
                   ('context', '/context'), ('org', '/organization'), ('devices', '/devices'),
                   ('attachments', '/attachments'), ('training_completions', '/training/completions')]:
    snap[name] = list_all(path) if name in ('controls', 'policies', 'tasks', 'risks', 'vendors', 'people', 'findings', 'attachments') else get(path)
    n = len(snap[name]) if isinstance(snap[name], list) else type(snap[name]).__name__
    print(f'{name}: {n}')
json.dump(snap, open(os.path.join(out, 'snapshot.json'), 'w'), indent=1)
# per-control detail (relations/progress)
details = {}
for c in snap['controls'] if isinstance(snap['controls'], list) else []:
    details[c['id']] = get(f"/controls/{c['id']}")
json.dump(details, open(os.path.join(out, 'control-details.json'), 'w'), indent=1)
print('control details:', len(details))
