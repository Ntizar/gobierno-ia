import re

raw = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
repo = {}
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]

canon_txt = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
secs = re.split(r"(?m)^={80,}$", canon_txt)
canon = {}
for s in secs:
    m = re.search(r"## \[(a\d+)\]", s)
    if m:
        body = s.split("\n", 2)[2].strip()
        # quitar la linea de cabecera "palabras:..."
        body = re.sub(r"^palabras:.*?\n", "", body)
        canon[m.group(1)] = body

def sq(s):
    s = s.lower()
    s = re.sub(r"[^a-záéíóúüñ0-9\s]", "", s, flags=re.UNICODE)
    return s.replace(" ", "")

# a187: que palabras del repo NO estan en el canon
lab = "a187"
rparas = [p.strip() for p in repo["[%s]" % lab].split("\n") if p.strip()]
cpara_set = set()
for p in canon[lab].split("\n"):
    p = p.strip()
    if p:
        cpara_set.add(sq(p))
cpat = " ".join(sq(canon[lab]))
for p in rparas:
    if p.startswith("##"):
        continue
    if sq(p) not in cpat:
        print("NO-CANON [%s]: %r" % (lab, p[:100]))

# a93 y a101 igual
for lab in ("a93", "a101"):
    for p in [x.strip() for x in repo["[%s]" % lab].split("\n") if x.strip()]:
        ok = any(sq(p) == c for c in cpara_set) if False else (sq(p) in sq(canon[lab]))
        if not ok:
            print("NO-CANON [%s]: %r" % (lab, p[:90]))
