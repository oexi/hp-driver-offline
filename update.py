import re, sys, os, urllib.request, urllib.parse
BASE = sys.argv[1]            # e.g. https://hub.hpgthub.com/
OUT = sys.argv[2]
EXT = r'(?:js|mjs|css|png|jpe?g|gif|svg|webp|ico|woff2?|ttf|otf|eot|json|mp4|webm|mp3|wav|bin|gltf|glb|hdr|wasm)'
# string literals / url() that look like local asset paths
PAT = re.compile(r'''["'`(]((?:\./|\.\./|/)?[A-Za-z0-9_\-./@%]+\.''' + EXT + r''')(?:\?[^"'`)]*)?["'`)]''')
seen, queue, fails = set(), ['index.html'], []
def fetch(rel):
    url = urllib.parse.urljoin(BASE, rel)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()
while queue:
    rel = queue.pop()
    rel = os.path.normpath(rel).lstrip('/')
    if rel in seen or rel.startswith('..'): continue
    seen.add(rel)
    path = os.path.join(OUT, rel)
    try:
        if os.path.exists(path):
            data = open(path, 'rb').read()
        else:
            data = fetch(rel)
            os.makedirs(os.path.dirname(path) or OUT, exist_ok=True)
            open(path, 'wb').write(data)
    except Exception as e:
        fails.append((rel, str(e))); continue
    if rel.endswith(('.html', '.js', '.mjs', '.css', '.json')):
        text = data.decode('utf-8', 'ignore')
        d = os.path.dirname(rel)
        for m in PAT.finditer(text):
            ref = m.group(1)
            if ref.startswith('//') or '://' in ref: continue
            if rel.endswith(('.js', '.mjs')) and not ref.startswith(('./', '../', '/')):
                # vite asset strings in JS are usually relative to site root or "./"
                cand = ref
            elif ref.startswith('/'):
                cand = ref
            else:
                cand = os.path.join(d, ref)
            queue.append(cand)
print('downloaded', len(seen) - len(fails), 'files')
for f in fails: print('FAIL', *f)
