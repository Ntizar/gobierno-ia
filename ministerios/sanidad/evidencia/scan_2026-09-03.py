import re, hashlib, json, sys
path = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad/leyes/BOE-A-1986-10499.md"
text = open(path, encoding='utf-8').read()
lines = text.splitlines()
blocks = []
cur = None
for i, l in enumerate(lines):
    m = re.match(r'^## \[(a\w+)\] (.*)$', l)
    if m:
        cur = {'id': m.group(1), 'title': m.group(2), 'start': i + 1, 'lines': []}
        blocks.append(cur)
    elif cur is not None:
        cur['lines'].append(l)

report = []
for b in blocks:
    paras = [l.strip() for l in b['lines'] if l.strip()]
    seen = {}
    for p in paras:
        h = hashlib.sha256(p.encode()).hexdigest()[:12]
        seen.setdefault(h, []).append(p)
    extra = sum(len(v) - 1 for v in seen.values() if len(v) > 1)
    words_extra = sum(len(v[0].split()) * (len(v) - 1) for v in seen.values() if len(v) > 1)
    if extra > 0:
        examples = [(v[0][:90], len(v), len(v[0].split())) for v in seen.values() if len(v) > 1]
        report.append({'id': b['id'], 'title': b['title'], 'start': b['start'],
                       'extra': extra, 'words_extra': words_extra, 'examples': examples})

print(f"Bloques totales: {len(blocks)}")
print(f"Bloques con repeticion interna: {len(report)}")
print(f"Palabras duplicadas: {sum(r['words_extra'] for r in report)}")
for r in sorted(report, key=lambda x: -x['words_extra']):
    print(f"[{r['id']}] (linea {r['start']}) extra={r['extra']} words={r['words_extra']} :: {r['title'][:60]}")
# detalle de los bloques pedidos
want = set(sys.argv[1:])
for r in report:
    if r['id'] in want:
        print("\n== DETALLE", r['id'], "==")
        for ex, n, w in r['examples']:
            print(f"  x{n} ({w}w): {ex}")
json.dump(report, open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad/evidencia/scan_2026-09-03.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
