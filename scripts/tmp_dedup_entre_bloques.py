# -*- coding: utf-8 -*-
"""Comprueba duplicados de párrafos ENTRE bloques de BOE-A-2021-8447."""
import re, hashlib
from collections import defaultdict

F = "C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
lines = open(F, encoding="utf-8").read().splitlines()
bloques = []; cur = None
for i, l in enumerate(lines):
    m = re.match(r"^##\s+\[([^\]]+)\]", l)
    if m:
        if cur: cur[2] = i
        cur = [m.group(1), i, None]; bloques.append(cur)
if cur: cur[2] = len(lines)

d = defaultdict(list)
for ref, s, e in bloques:
    for j, l in enumerate(lines[s+1:e]):
        t = l.strip()
        if len(t.split()) > 15:
            h = hashlib.sha256(re.sub(r"\s+", " ", t).encode()).hexdigest()
            d[h].append((ref, s+2+j, t[:70]))
cross = {h: v for h, v in d.items() if len({r for r, _, _ in v}) > 1}
print("Parrafos duplicados ENTRE bloques:", len(cross))
for h, v in list(cross.items())[:10]:
    print([(r, n) for r, n, _ in v], "»", v[0][2])
