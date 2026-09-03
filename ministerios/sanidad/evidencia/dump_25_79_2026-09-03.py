# -*- coding: utf-8 -*-
# Volcado completo de los bloques a25/a79 con hash y match contra BOE plano
import re, json, hashlib, unicodedata, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
lines = open(BASE + "/leyes/BOE-A-1986-10499.md", encoding="utf-8").read().splitlines()
plano = open(BASE + "/evidencia/boe_texto_plano.txt", encoding="utf-8").read().splitlines()

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

boe = {}
for n, l in enumerate(plano):
    t = norm(l)
    if t:
        boe.setdefault(hashlib.sha256(t.encode()).hexdigest()[:12], n + 1)

heads = [(i, m.group(1)) for i, l in enumerate(lines) for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]
want = {"aveinticinco", "asetentaynueve"}
for k, (i, bid) in enumerate(heads):
    if bid not in want: continue
    j = heads[k+1][0]
    print(f"\n##### [{bid}] lineas {i+1}..{j-1} #####")
    for n in range(i+1, j):
        l = lines[n]
        if not l.strip(): continue
        h = hashlib.sha256(norm(l).encode()).hexdigest()[:12]
        b = boe.get(h, "-")
        print(f"{n+1:5d} [{h}] BOE:{b:>5} | {norm(l)}")
