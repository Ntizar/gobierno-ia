# -*- coding: utf-8 -*-
# Duplication ENTRE bloques en LGS (el scan ministerial solo mira dentro de bloque)
import io, re, hashlib
from collections import defaultdict
REPO = "C:/Users/d_ant/Projects/gobierno-ia"
lgs = io.open(REPO + "/ministerios/sanidad/leyes/BOE-A-1986-10499.md", encoding="utf-8").read()
loc = defaultdict(list)
for blk in re.split(r"(?m)^(?=## \[)", lgs):
    h = re.match(r"## \[([^\]]+)\]", blk)
    if not h: continue
    body = blk.split("\n", 1)[1] if "\n" in blk else ""
    for l in body.splitlines():
        t = re.sub(r"\s+", " ", l.strip().lower())
        if len(t.split()) >= 8:
            loc[hashlib.sha256(t.encode()).hexdigest()[:16]].append((h.group(1), len(t.split())))
x = {k: v for k, v in loc.items() if len(set(b for b, _ in v)) > 1}
tot = sum(len(c) - len(set(b for b, _ in c)) and max(w for _, w in c) or 0 for c in x.values())
print("LGS parrafos repetidos entre bloques distintos:", len(x))
for k, v in list(x.items())[:15]:
    print("  bloques:", sorted(set(b for b, _ in v)), "| palabras:", v[0][1])
# mismo test en L7 y LGT, solo conteo
for name, path in [("L7", "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"),
                   ("LGT", "ministerios/hacienda/leyes/BOE-A-2003-23186.md")]:
    t = io.open(REPO + "/" + path, encoding="utf-8").read()
    lo = defaultdict(set)
    dupw = 0
    tmp = defaultdict(list)
    for blk in re.split(r"(?m)^(?=## \[)", t):
        h = re.match(r"## \[([^\]]+)\]", blk)
        if not h: continue
        for l in blk.split("\n", 1)[1].splitlines():
            s = re.sub(r"\s+", " ", l.strip().lower())
            if len(s.split()) >= 8:
                tmp[hashlib.sha256(s.encode()).hexdigest()[:16]].append((h.group(1), len(s.split())))
    cross = {k: v for k, v in tmp.items() if len(set(b for b, _ in v)) > 1}
    w = sum(max(cnt for _, cnt in v) * (len(v) - 1) for v in cross.values())
    print(name, "parrafos repetidos entre bloques:", len(cross), "| palabras (aprox):", w)
