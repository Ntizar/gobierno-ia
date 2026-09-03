# -*- coding: utf-8 -*-
# 1) cuales de las 21 letras a) del BOE siguen ausentes del fichero actual
# 2) detalle de dup en [aveinticinco] y [asetentaynueve] vs BOE plano (que copia es vigente)
import re, json, unicodedata, hashlib, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
ley = open(BASE + "/leyes/BOE-A-1986-10499.md", encoding="utf-8").read()
items = json.load(open(BASE + "/evidencia/a_restituir_completas_2026-09-01.json", encoding="utf-8"))

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

leys = [norm(l) for l in ley.splitlines() if l.strip()]
faltan = []
for it in items:
    t = norm(it["letra_a_BOE"])
    if t not in leys:
        faltan.append((it["linea_repo"], it["letra_a_BOE"][:70]))
print("LETRAS A AUSENTES:", len(faltan), "de", len(items))
for f in faltan:
    print("  -", f)

# bloque aveinticinco
lines = ley.splitlines()
heads = [(i, m.group(1)) for i, l in enumerate(lines) for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]
for k, (i, bid) in enumerate(heads):
    if bid != "aveinticinco": continue
    j = heads[k+1][0]
    print(f"\n== [aveinticinco] lineas {i+1}-{j} ==")
    seen = {}
    for n in range(i+1, j):
        l = lines[n]
        if not l.strip(): continue
        h = hashlib.sha256(norm(l).encode()).hexdigest()[:8]
        c = seen.get(h, 0); seen[h] = c+1
        print(f"{n+1:5d}| {norm(l)[:110]}{'  <<<DUP' if c else ''}")
