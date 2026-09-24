# Claves reales del inventario F1 para df* + hashes Auditor de los bloques VIVOS.
import re, json, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"

inv = json.load(open(BASE + "/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv.get("preceptos_afectados", inv)
ks = [k for k in pa if ("dispos" in k.lower() or "final" in k.lower() or k.lower().startswith("df") or "df" in k.lower())]
print("claves con df/disposicion:", ks[:25])
for k in ks[:10]:
    print(k, "->", json.dumps(pa[k], ensure_ascii=False)[:200])

def auditor(t):
    t = t.strip("\n").replace("\r\n", "\n")
    return hashlib.sha256(t.encode("utf-8")).hexdigest()

for lab in ["dfquinta", "dfsexta", "dfoctava"]:
    p = BASE + "/ministerios/hacienda/evidencia/bloque_vivo_" + lab + "_2026-09-24.txt"
    t = open(p, encoding="utf-8", newline="").read()
    print("VIVO", lab, "| pal", len(t.split()), "| hash", auditor(t))
