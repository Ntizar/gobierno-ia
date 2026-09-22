# -*- coding: utf-8 -*-
"""Verificación pre-sesión 15: copia única de bloques ejecutados + fidelidad
canónica de [a12], [a93], [a101], [a187] contra boe_canonico y manifiestos."""
import re, json, io, sys, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAW = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
print("sha256 fichero:", hashlib.sha256(RAW.encode("utf-8")).hexdigest()[:8])

labels = re.findall(r"(?m)^## (\[[a-z0-9\\-]+\])", RAW)
from collections import Counter
c = Counter(labels)
dupe = {k: v for k, v in c.items() if v > 1}
print("etiquetas total:", len(labels), "| únicas:", len(c), "| con >1 copia:", dupe if dupe else "NINGUNA")

ejecutados = ["[a12]", "[a62]", "[a95]", "[a43]", "[a150]", "[a93]", "[a101]", "[a187]",
              "[dadecimoctava]", "[a271]"]
for b in ejecutados:
    print(b, "copias:", c.get(b, 0))

# dividir bloques
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", RAW)
blocks = {}
for i in range(1, len(parts) - 1, 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    blocks.setdefault(lab, parts[i + 1])

def squash(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9áéíóúñü\s]", "", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()

canon = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
# el canónico puede estar segmentado por bloque; test párrafo a párrafo global
canon_par = [squash(p) for p in canon.split("\n") if len(squash(p)) > 30]
body_sq = {b: squash(blocks.get(b, "")) for b in ["[a93]", "[a101]", "[a187]"]}
for b in ["[a93]", "[a101]", "[a187]"]:
    missing = [p for p in canon_par if p not in body_sq[b]]
    # párrafos canónicos que pertenecen a OTRO bloque no cuentan; aprox: comprobar si aparecen en cualquier parte del fichero
    still = [p for p in missing if p not in squash(RAW)]
    print(b, "| párrafos canon no presentes en bloque:", len(missing), "| de ellos, ausentes de TODO el fichero:", len(still))

# [a12] restituido: debe contener «interpretativas o aclaratorias»
a12 = blocks.get("[a12]", "")
print("[a12] contiene 'interpretativas o aclaratorias':", "interpretativas o aclaratorias" in a12)
print("[a12] palabras:", len(a12.split()))
for b in ["[a93]", "[a101]", "[a187]"]:
    print(b, "palabras:", len(blocks.get(b, "").split()))
