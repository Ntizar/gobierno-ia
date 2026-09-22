# -*- coding: utf-8 -*-
"""Volcado de los bloques objetivo [daundecima] y [davigesima] del fichero vivo,
más contexto de qué son (título, líneas) y su peso actual."""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
raw = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
for slug in ("daundecima", "davigesima", "a104", "a82"):
    m = re.search(r"(?m)^(## \[%s\][^\n]*)\n(.*?)(?=^## \[|\Z)" % slug, raw, re.S)
    if not m:
        print("== [%s] NO ENCONTRADO ==" % slug); continue
    head, body = m.group(1), m.group(2)
    print("=" * 70)
    print(head, "| palabras:", len(body.split()))
    print(body[:1800])
    print("... [TRUNCADO]" if len(body) > 1800 else "")
