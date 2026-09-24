# Volcado s16: contenido vivo de bloques DF y top-F1 -> evidencia para el informe.
import re, sys, io, json

BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
raw = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
parts = re.split(r"(?m)^(?=## \[)", raw)
WS = re.compile(r"\S+")

out = []
targets = {"dfprimera","dfsegunda","dftercera","dfcuarta","dfquinta","dfsexta"}
inv = json.load(open(BASE + r"/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv["preceptos_afectados"]
# top bloques por palabras del inventario (estructura: dict etiqueta -> info)
tops = sorted(pa.items(), key=lambda kv: -(kv[1].get("palabras", 0) if isinstance(kv[1], dict) else 0))[:12]
for t, info in tops:
    targets.add(t)

for p in parts:
    m = re.match(r"## \[([a-z0-9\-]+)\]", p)
    if m and m.group(1) in targets:
        out.append(p.rstrip("\n"))

with open(BASE + r"/ministerios/hacienda/evidencia/volcado_bloques_s16_2026-09-24.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n\n".join(out))
print("bloques volcados:", len(out))
print("tops inventario:", [(t, (info.get("palabras") if isinstance(info, dict) else "?")) for t, info in tops])
