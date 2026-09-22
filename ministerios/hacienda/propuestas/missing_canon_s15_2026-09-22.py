# -*- coding: utf-8 -*-
"""Listar los párrafos del canon BOE (a93/a101/a187) ausentes del fichero vivo."""
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
RAW = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
def squash(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9áéíóúñü\s]", "", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()
canon = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
all_sq = squash(RAW)
seen = set()
n = 0
for p in canon.split("\n"):
    q = squash(p)
    if len(q) > 30 and q not in all_sq and q not in seen:
        seen.add(q); n += 1
        print(f"[{n}] AUSENTE:", q[:260])
        print("---")
print("total ausentes:", n)
