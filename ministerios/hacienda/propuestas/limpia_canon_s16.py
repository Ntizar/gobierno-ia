# Limpieza canon s16 + agregados del inventario F1 + hashes definitivos de las 3 DF candidatas.
import re, sys, io, hashlib, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
CF = BASE + r"/ministerios/hacienda/evidencia/boe_canonico_df_2026-09-24.txt"
raw = open(CF, encoding="utf-8").read()

# limpiar líneas de navegación del BOE
lines = [l for l in raw.split("\n") if l.strip() not in ("Subir",) and not re.match(r"^\[Bloque \d+:\s*#", l.strip())]
clean = "\n".join(lines)
# colapsar espacios sobrantes al final de cada línea
clean = re.sub(r"(?m)[ \t]+$", "", clean)
open(CF, "w", encoding="utf-8", newline="\n").write(clean.strip() + "\n")

canon = {}
for m in re.finditer(r"#### BOE consolidado — Disposición final (\w+) \(Ley 58/2003[^)]*\)\n(.*?)(?=\n\n####|\n\n#### Fuente|\Z)", clean, re.S):
    canon[m.group(1)] = m.group(2).strip()

WS = re.compile(r"\S+")
lg = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")

def auditor_hash(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n", "\n").encode("utf-8")).hexdigest()

inv = json.load(open(BASE + r"/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv["preceptos_afectados"]
tot_casos = sum(v["casos"] for v in pa.values() if isinstance(v, dict) and "casos" in v)
tot_pal = sum(v["palabras"] for v in pa.values() if isinstance(v, dict) and "palabras" in v)
print("inventario: preceptos", len(pa), "| suma casos", tot_casos, "| suma palabras", tot_pal)
print("palabras ley viva:", len(WS.findall(lg)))

for o, slug in [("cuarta", "dfcuarta"), ("quinta", "dfquinta"), ("sexta", "dfsexta")]:
    m = re.search(r"(?ms)^## \[" + slug + r"\].*?(?=^## \[|\Z)", lg)
    live = m.group(0).rstrip("\n")
    prop = "## [" + slug + "] Disposición final " + o + "\n\n" + canon[o]
    print("==", slug, "| canon pal", len(WS.findall(canon[o])), "| final:", repr(canon[o][-70:]))
    print("   ACTUAL pal", len(WS.findall(live)), "hash", auditor_hash(live))
    print("   PROP   pal", len(WS.findall(prop)), "hash", auditor_hash(prop))
    open(BASE + r"/ministerios/hacienda/evidencia/bloque_propuesto_" + slug + "_2026-09-24.txt", "w", encoding="utf-8", newline="\n").write(prop.strip("\n"))
    print("   inv:", json.dumps(pa.get("[" + slug + "]"), ensure_ascii=False)[:220])
print("\nSHA ley:", hashlib.sha256(lg.encode("utf-8")).hexdigest())
