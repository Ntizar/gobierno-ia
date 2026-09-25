# [a82] deficiente: reconstrucción desde canon + conservación de fragmentos vivos (s17, 25-09)
import json, re, hashlib

ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
a82 = {x["id"]: x for x in canon["articulos"]}["a82"]
EV = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

m = re.search(r"^## \[a82\].*?(?=^## \[|\Z)", ley, re.S | re.M)
vivo = m.group(0).rstrip("\n")

def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip().lower()

def frases(txt):
    txt = re.sub(r"\s+", " ", txt.replace("\u00a0", " ")).strip()
    return [p.strip() for p in re.split(r"(?<=[.;:])\s+(?=[A-ZÁÉÍÓÚÑ«])", txt) if len(p.split()) >= 8]

nv = norm(vivo)
extra = [f for f in frases(vivo) if norm(f) not in norm(a82["texto"]) and len(f.split()) >= 8]
print("vivo:", len(vivo.split()), "pal | canon:", len(a82["texto"].split()), "pal | frases vivas ajenas al canon:", len(extra))
for f in extra[:10]:
    print("   ·", f[:120])

prop = "## [a82] Artículo 82\n\n" + a82["titulo"].strip() + "\n\n" + a82["texto"].strip()
if extra:
    pies = "\n\n".join("> **AMENDADO PENDIENTE DE CONSOLIDACIÓN (reescaneo 2026-09-25).** Fragmento del bloque vivo no contenido en el texto consolidado (BOE): «" + f + "»" for f in extra)
    prop += "\n\n" + pies
prop = prop.rstrip()
open(EV + "/bloque_propuesto_a82_2026-09-25.txt", "w", encoding="utf-8", newline="\n").write(prop)
open(EV + "/bloque_vivo_a82_2026-09-25.txt", "w", encoding="utf-8", newline="\n").write(vivo)

# validación: canon ⊆ propuesto (substring) y cobertura por frases
ok = norm(a82["texto"]) in norm(prop)
ncov = sum(1 for f in frases(a82["texto"]) if norm(f) in norm(prop))
print(f"propuesto: {len(prop.split())} pal | canon ⊆ propuesto íntegro: {ok} | frases canon cubiertas: {ncov}/{len(frases(a82['texto']))}")
print("sha vivo    :", hashlib.sha256(vivo.replace("\r\n","\n").encode()).hexdigest()[:8])
print("sha propuesto:", hashlib.sha256(prop.replace("\r\n","\n").encode()).hexdigest()[:8])
