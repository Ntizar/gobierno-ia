# Chequeo s16: (1) entradas df en inventario F1; (2) IGAE en cafe de hoy; (3) colas canon DF 1-4,7.
import re, json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"

inv = json.load(open(BASE + "/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv.get("preceptos_afectados", inv)
print("tipo preceptos_afectados:", type(pa).__name__, "| entradas:", len(pa))
for lab in ["dfprimera", "dfsegunda", "dftercera", "dfcuarta", "dfquinta", "dfsexta", "dfseptima", "dfoctava"]:
    v = pa.get(lab) if isinstance(pa, dict) else None
    print(lab, "->", json.dumps(v, ensure_ascii=False)[:160] if v is not None else "NO ESTÁ")

# ¿palabras de ausencia totales del reescaneo?
tot = 0
if isinstance(pa, dict):
    for k, v in pa.items():
        if isinstance(v, dict):
            tot += v.get("pal_ab", v.get("palabras_ausentes", 0)) or 0
print("suma palabras ausentes (si clave existe):", tot)

txt = open(BASE + "/ministerios/hacienda/evidencia/df_canon_limpio_s16_2026-09-24.txt", encoding="utf-8").read()
for n, lab in [(1, "primera"), (2, "segunda"), (3, "tercera"), (4, "cuarta"), (7, "septima")]:
    m = re.search(r"(Disposición final " + lab + r"\.)(.*?)(?=Disposición final [a-z]+\.|\Z)", txt, flags=re.S)
    if m:
        print("canon df" + lab + ":", len(m.group(0).split()), "pal en evidencia")
