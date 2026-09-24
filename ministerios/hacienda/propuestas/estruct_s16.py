# Estructura de los ficheros canon DF + entradas F1 de df* + IGAE hoy en el repo.
import os
import sys
import io
import json
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")

for cf in ["df_canon_limpio_s16_2026-09-24.txt", "boe_canonico_df_2026-09-24.txt"]:
    raw = open(os.path.join(EVID, cf), encoding="utf-8").read()
    heads = re.findall(r"(?m)^.{0,90}Disposición final (?:quinta|sexta|octava).{0,40}", raw)
    print("==", cf)
    for h in heads[:6]:
        print("   ", repr(h))
    marks = re.findall(r"(?m)^#{1,3} \[[a-z0-9]+\]", raw)
    print("    rotulos tipo [xx]:", marks[:12])

inv_path = os.path.join(EVID, "inventario_f1_vivo_s15_2026-09-23.json")
inv = json.load(open(inv_path, encoding="utf-8"))
print("tipo inventario:", type(inv).__name__)
def walk(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        s = json.dumps(obj, ensure_ascii=False)
        if any(k in s for k in ["dfquinta", "dfsexta", "dfoctava"]) and len(s) < 600:
            hits.append((path, s))
        else:
            for k, v in obj.items():
                hits += walk(v, path + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += walk(v, path + "[%d]" % i)
    return hits
for p, s in walk(inv):
    print("F1:", s[:400])
