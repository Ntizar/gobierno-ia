#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostico de deuda de ejecucion — Gobierno IA (sesion 13/30).
Cuenta cabeceras de articulo repetidas y palabras por bloque afectado.
Solo LEE. No modifica nada.
"""
import re, hashlib, json, sys, io, os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ministerios")
LEYES = {
    "hacienda": ("BOE-A-2003-23186.md", ["Art\u00edculo 12", "Art\u00edculo 43", "Art\u00edculo 62", "Art\u00edculo 95"]),
    "sanidad": ("BOE-A-1986-10499.md", ["Art\u00edculo 3", "Art\u00edculo 6", "Art\u00edculo 16", "Art\u00edculo 20", "Art\u00edculo 4"]),
    "transicion-ecologica": ("BOE-A-2021-8447.md", ["Art\u00edculo 1", "Art\u00edculo 2", "Art\u00edculo 4", "Art\u00edculo 14", "Art\u00edculo 15"]),
}

out = {}
for min_, (fname, arts) in LEYES.items():
    path = os.path.join(BASE, min_, "leyes", fname)
    with io.open(path, encoding="utf-8") as f:
        txt = f.read()
    raw = txt.encode("utf-8")
    info = {
        "fichero": path,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "palabras_total": len(txt.split()),
        "lineas": txt.count("\n") + 1,
        "articulos": {},
    }
    for a in arts:
        # cabeceras tipo "**Articulo 12**", "##### Articulo 12", "## Articulo 12." etc.
        pat = re.compile(r"^[#*\s>]*" + re.escape(a) + r"\b[^\n]{0,80}$", re.M)
        hits = pat.findall(txt)
        idxs = [m.start() for m in pat.finditer(txt)]
        info["articulos"][a] = {
            "n_cabeceras": len(hits),
            "cabeceras": [h.strip()[:90] for h in hits],
            "lineas": [txt[:i].count("\n") + 1 for i in idxs],
        }
    out[min_] = info

out["_generado"] = "diag_deuda.py — solo lectura"
print(json.dumps(out, ensure_ascii=False, indent=1))
