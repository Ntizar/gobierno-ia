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
        body = re.sub(r"^palabras:.*?\n", "", body)
        canon[m.group(1)] = body

def sq(s):
    s = s.lower()
    s = re.sub(r"[^a-záéíóúüñ0-9]", "", s, flags=re.UNICODE)
    return s

wc = lambda s: len(re.findall(r"\S+", s))
for lab, n in (("[a93]", "a93"), ("[a101]", "a101"), ("[a187]", "a187")):
    cur = repo[lab]
    cpar = sq(canon[n])
    # palabras actuales que son parte del canon (por párrafo: se cuenta el parrafo entero si esta dentro del canon o es subsecuencia)
    keep = 0
    for p in [x.strip() for x in cur.split("\n") if x.strip() and not x.startswith("##")]:
        sp = sq(p)
        if not sp:
            continue
        if sp in cpar:
            keep += wc(p)
    labels = len(re.findall(r"(?m)^Artículo \d+\.", cur))
    lab_w = 0
    for m2 in re.finditer(r"(?m)^Artículo \d+\.[^\n]*$", cur):
        lab_w += wc(m2.group(0))
    dup = wc(cur) - keep - lab_w + (wc(cur) - wc(cur))  # palabras de parrafos duplicados (excl. labels)
    print(lab, "act:", wc(cur), "| en canon:", keep, "| rótulos:", labels, "(%d pal)" % lab_w, "| fuera canon sin rótulos:", wc(cur) - keep - lab_w, "| duplicados eliminables (parrafos):", wc(cur) - keep - lab_w, "| exceso de rótulos:", (labels - 1))
    print("   restauradas:", wc(canon[n]) - keep)
