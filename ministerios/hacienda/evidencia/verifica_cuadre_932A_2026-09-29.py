#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sesion 20/30 (Fase 3, 2026-09-29). Verificacion del cuadre del programa 932A
contra las Cuentas Anuales de la AEAT (documento oficial descargado hoy al repo).
No inventa: imprime lo que encuentra y el cuadre aritmetico."""
import re, os, hashlib
from decimal import Decimal

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def esp(s):
    """'1.817.977.437,08' -> Decimal"""
    return Decimal(s.replace(".", "").replace(",", "."))

print("### Ficheros nuevos de hoy (evidencia Fase 3, jornada 2) ###")
for f in ["AEAT-cuentas-anuales-2024.pdf", "AEAT-cuentas-anuales-2025.pdf",
          "rdl18-2026-consolidado.pdf", "rdl18-2026-txt.html"]:
    if os.path.exists(f):
        print("  %-34s %10d B  sha256 %s" % (f, os.path.getsize(f), sha(f)))
    else:
        print("  %-34s NO EXISTE" % f)

print()
print("### Cuadre del programa 932A (AEAT, Cuentas Anuales 2024, E.I gastos) ###")
cifras = {
    "1.817.977.437,08": "credito definitivo del programa 932A",
    "1.776.913.651,22": "obligaciones reconocidas netas",
    "41.063.785,86": "remanente de credito (fila TOTAL de la pagina)",
}
t = open("aeat_cuentas_2024.txt", encoding="utf-8", errors="replace").read()
for c, d in cifras.items():
    n = t.count(c)
    print("  %-20s (%s): %d aparicion(es) en el texto extraido" % (c, d, n))

c3 = esp("1.817.977.437,08"); c5 = esp("1.776.913.651,22"); c8 = esp("41.063.785,86")
print()
print("  resta: 1.817.977.437,08 - 1.776.913.651,22 = %s" % (c3 - c5))
print("  cuadra con la fila TOTAL de la pagina 19? %s" % ("SI" if (c3 - c5) == c8 else "NO"))
