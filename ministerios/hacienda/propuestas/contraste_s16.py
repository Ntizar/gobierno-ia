# Contraste final s16: bloque propuesto vs canon BOE extraido hoy del consolidado
# (df_canon_limpio_s16_2026-09-24.txt / boe_canonico_df_2026-09-24.txt).
import os
import sys
import io
import hashlib
import difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")

def norm(t):
    t = t.replace("\r\n", "\n").replace("\u00a0", " ").strip("\n")
    return t

canon_files = ["df_canon_limpio_s16_2026-09-24.txt", "boe_canonico_df_2026-09-24.txt"]
for cf in canon_files:
    p = os.path.join(EVID, cf)
    if not os.path.exists(p):
        print("NO EXISTE", cf)
        continue
    raw = norm(open(p, encoding="utf-8").read())
    print("==", cf, "| palabras =", len(raw.split()), "| sha256 =", hashlib.sha256(raw.encode()).hexdigest()[:16])
    for s in ["dfquinta", "dfsexta", "dfoctava"]:
        tag = "## [" + s + "]"
        i = raw.find(tag)
        if i < 0:
            print("   ", s, "ausente en canon")
            continue
        j = raw.find("\n## [", i + 5)
        c = raw[i:j if j > 0 else len(raw)].rstrip("\n")
        prop_p = os.path.join(EVID, "bloque_propuesto_" + s + "_2026-09-24.txt")
        pr = open(prop_p, "rb").read().replace(b"\r\n", b"\n").rstrip(b"\n").decode("utf-8")
        if c == pr:
            print("   ", s, "IGUAL al canon | pal =", len(c.split()))
        else:
            d = sum(1 for l in difflib.unified_diff(c.split("\n"), pr.split("\n"), lineterm="") if l.startswith(("+", "-")) and not l.startswith(("+++", "---")))
            print("   ", s, "difiere del canon en", d, "lineas diff | canon pal =", len(c.split()), "prop pal =", len(pr.split()))
            cl = c.split("\n"); pl = pr.split("\n")
            for k in range(max(len(cl), len(pl))):
                a = cl[k] if k < len(cl) else "<EOF>"
                b = pl[k] if k < len(pl) else "<EOF>"
                if a != b:
                    print("     linea", k, "canon:", repr(a[:90]))
                    print("     linea", k, "prop :", repr(b[:90]))
                    break
