# Contraste propuesto vs canon BOE consolidado (estructura #### por DF).
import os
import sys
import io
import hashlib
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")

raw = open(os.path.join(EVID, "boe_canonico_df_2026-09-24.txt"), encoding="utf-8").read()
parts = re.split(r"(?m)^#### BOE consolidado — Disposición final (\w+)[^\n]*\n", raw)
# parts: [pre, nombre1, texto1, nombre2, texto2, ...]
canon = {}
for i in range(1, len(parts) - 1, 2):
    canon[parts[i]] = parts[i + 1].strip("\n")
print("DF en canon:", sorted(canon.keys()))

nom2slug = {"quinta": "dfquinta", "sexta": "dfsexta", "octava": "dfoctava"}
for nom, slug in nom2slug.items():
    c = canon.get(nom, "")
    prop_p = os.path.join(EVID, "bloque_propuesto_" + slug + "_2026-09-24.txt")
    pr = open(prop_p, "rb").read().replace(b"\r\n", b"\n").rstrip(b"\n").decode("utf-8")
    # canon body sin la cabecera ## [slug] que lleva el propuesto
    core_prop = pr.split("\n", 2)  # ['## [x] ...', '', resto]
    body = core_prop[2] if len(core_prop) > 2 else ""
    def clean(t):
        t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)      # enlaces md -> texto
        t = t.replace(" ,", ",").replace(" ;", ";").replace(" .", ".")
        t = re.sub(r"\s*\n\s*", "\n", t)
        return t.strip()
    cc, bc = clean(c), clean(body)
    if cc == bc:
        print(slug, "IGUAL al canon (normalizado) | pal prop =", len(pr.split()))
    else:
        # cuantas lineas difieren
        cl, bl = cc.split("\n"), bc.split("\n")
        diffs = 0
        first = None
        for k in range(max(len(cl), len(bl))):
            a = cl[k] if k < len(cl) else "<EOF>"
            b = bl[k] if k < len(bl) else "<EOF>"
            if a != b:
                diffs += 1
                if first is None:
                    first = (k, a[:100], b[:100])
        print(slug, "difiere en", diffs, "lineas | canon pal =", len(c.split()), "prop pal =", len(pr.split()))
        if first:
            print("   primera divergencia linea", first[0])
            print("     canon:", repr(first[1]))
            print("     prop :", repr(first[2]))
