import re

canon_txt = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
secs = re.split(r"(?m)^={80,}$", canon_txt)
canon = {}
for s in secs:
    m = re.search(r"## \[(a\d+)\]", s)
    if m:
        body = s.split("\n", 2)[2].strip()
        body = re.sub(r"^palabras:.*?\n", "", body)
        canon[m.group(1)] = body

raw = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
repo = {}
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]

def sq(s):
    s = s.lower()
    s = re.sub(r"[^a-záéíóúüñ0-9]", "", s, flags=re.UNICODE)
    return s

for lab in ("a93", "a101", "a187"):
    cp = sq(canon[lab])
    print("=" * 60, lab)
    for line in [x.strip() for x in repo["[%s]" % lab].split("\n") if x.strip()]:
        if not sq(line):
            continue
        if sq(line) not in cp:
            print("  FUERA:", repr(line[:85]))
