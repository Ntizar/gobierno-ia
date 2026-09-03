# -*- coding: utf-8 -*-
# Imprime bloques concretos de la ley con numeracion de linea real + hash por parrafo
import re, hashlib, unicodedata, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
path = BASE + "/leyes/BOE-A-1986-10499.md"
lines = open(path, encoding="utf-8").read().splitlines()

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

targets = sys.argv[1:]
heads = [(i, m.group(1)) for i, l in enumerate(lines) for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]
for k, (i, bid) in enumerate(heads):
    if bid not in targets:
        continue
    j = heads[k+1][0] if k+1 < len(heads) else len(lines)
    print(f"\n===== [{bid}] lineas {i+1}-{j} ({j-i-1} lineas) =====")
    seen = {}
    for n in range(i+1, j):
        l = lines[n]
        if not l.strip():
            continue
        h = hashlib.sha256(norm(l).encode()).hexdigest()[:8]
        c = seen.setdefault(h, 0); seen[h] = c + 1
        mark = f" <<<DUP#{c+1}" if c > 0 else ""
        print(f"{n+1:5d}| {l.strip()[:150]}{mark}")
