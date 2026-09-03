# -*- coding: utf-8 -*-
# Cierre 09-03: estado de ficheros + control antidifamacion global (hash vs BOE)
import io, sys, re, hashlib, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"

def norm(s):
    s = unicodedata.normalize("NFC", s).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

boe = {hashlib.sha256(norm(l).encode()).hexdigest()[:12]
       for l in open(BASE + "/evidencia/boe_texto_plano.txt", encoding="utf-8", errors="ignore")
       if len(l.strip()) > 15}
out = []
for l in open(BASE + "/leyes/BOE-A-1986-10499.md", encoding="utf-8"):
    x = l.strip()
    if x and len(x) > 25 and not x.startswith("#"):
        if hashlib.sha256(norm(x).encode()).hexdigest()[:12] not in boe:
            out.append(x[:70])
print("PARRAFOS FUERA DEL BOE (def. estricta >25w):", len(out))
for o in out[:5]:
    print("  ", o)
for f in ["agenda.md", "propuestas/2026-09-03.md", "kpis.md", "diario.md"]:
    s = open(BASE + "/" + f, encoding="utf-8").read()
    print(f, "| contiene 2026-09-03:", "2026-09-03" in s, "| Vyjuvek ok:", ("Vyjuvek" in s) or ("Vyjuvek" not in s and "Vyjupek" not in s))
