# Ultimas verificaciones s16: (1) entradas F1 de dfquinta/dfsexta/dfoctava,
# (2) el propuesto == canon del primer commit (a547104) tras normalizar LF y
# limpiar artefactos ya declarados, (3) hora, (4) ley intacta en git.
import os
import sys
import io
import json
import hashlib
import subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")

# (1) inventario F1
inv_path = os.path.join(EVID, "inventario_f1_vivo_s15_2026-09-23.json")
inv = json.load(open(inv_path, encoding="utf-8"))
items = inv if isinstance(inv, list) else inv.get("bloques") or inv.get("items") or []
if isinstance(items, dict):
    items = list(items.values())
for it in items:
    s = json.dumps(it, ensure_ascii=False)
    if "dfquinta" in s or "dfsexta" in s or "dfoctava" in s:
        print("F1:", s[:300])

# (2) canon primer commit
canon_raw = subprocess.run(
    ["git", "-C", BASE, "show", "a547104:ministerios/hacienda/leyes/BOE-A-2003-23186.md"],
    capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
for s in ["dfquinta", "dfsexta", "dfoctava"]:
    i = canon_raw.index("## [" + s + "]")
    j = canon_raw.find("\n## [", i + 5)
    if j < 0:
        j = len(canon_raw)
    canon = canon_raw[i:j].rstrip("\n")
    prop_p = os.path.join(EVID, "bloque_propuesto_" + s + "_2026-09-24.txt")
    prop = open(prop_p, "rb").read().replace(b"\r\n", b"\n").rstrip(b"\n").decode("utf-8")
    equal = (canon == prop)
    print(s, "| canon palabras =", len(canon.split()), "| prop palabras =", len(prop.split()), "| canon==prop:", equal)
    if not equal:
        # primer punto de divergencia
        k = 0
        while k < min(len(canon), len(prop)) and canon[k] == prop[k]:
            k += 1
        print("   diverge en:", repr(canon[k-20:k+60]), "VS", repr(prop[k-20:k+60]))

# (3) hora y (4) git
print("HORA:", subprocess.run(["date", "+%Y-%m-%d %H:%M %z"], capture_output=True).stdout.decode().strip())
gs = subprocess.run(["git", "-C", BASE, "status", "--porcelain", "ministerios/hacienda/leyes/BOE-A-2003-23186.md"], capture_output=True).stdout.decode()
print("git status ley:", repr(gs) if gs.strip() else "LIMPIA (sin modificaciones)")
