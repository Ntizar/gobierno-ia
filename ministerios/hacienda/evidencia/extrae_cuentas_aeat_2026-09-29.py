#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extrae el estado de liquidacion del presupuesto de gastos de la AEAT (programa 932A)
de las Cuentas Anuales descargadas hoy. Sesion 20/30, Fase 3. Sin inventar: lo que no este, se declara."""
import re, sys, hashlib, os

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def texto(p):
    try:
        import fitz  # pymupdf
        d = fitz.open(p)
        return "\n".join(pg.get_text() for pg in d), "pymupdf"
    except Exception as e1:
        try:
            import pdfplumber
            with pdfplumber.open(p) as pdf:
                return "\n".join((pg.extract_text() or "") for pg in pdf.pages), "pdfplumber"
        except Exception as e2:
            return None, "sin_extractor(%s | %s)" % (e1, e2)

for p in sorted(f for f in os.listdir(".") if f.startswith("AEAT-cuentas-anuales")):
    print("=" * 78)
    print(p, "|", os.path.getsize(p), "B | sha256", sha256(p)[:16] + "...")
    t, how = texto(p)
    if t is None:
        print("  !! no se pudo extraer texto:", how)
        continue
    print("  extractor:", how, "| caracteres:", len(t))
    for patron in ["932A", "Aplicacion del sistema tributario", "Aplicación del sistema tributario",
                   "Aplicación del sistema tributario estatal", "932"]:
        idxs = [m.start() for m in re.finditer(re.escape(patron), t)]
        if idxs:
            print("  -- patron %r: %d apariciones (primeras lineas con cifras)" % (patron, len(idxs)))
            for i in idxs[:3]:
                frag = re.sub(r"[ \t]+", " ", t[max(0, i - 120):i + 320]).strip()
                print("     >>>", frag[:420].replace("\n", " | "))
            break
    # lineas con 932A y numeros grandes
    print("  -- lineas con 932A:")
    for ln in t.splitlines():
        if "932A" in ln or "932 A" in ln:
            print("     ", re.sub(r"\s+", " ", ln).strip()[:300])
