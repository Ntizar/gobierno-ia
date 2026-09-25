# Últimas comprobaciones antes de escribir (s17)
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

print("A) ¿Dónde está la letra a) del art.48 en el fichero vivo?")
for mm in re.finditer(r"personas físicas, el lugar[^\n]*", ley):
    s = max(0, mm.start() - 250)
    head = ley[s:mm.start()].split("\n")
    tag = next((h for h in reversed(head) if h.startswith("## [")), "?")
    print(f"   en bloque {tag}: {mm.group(0)[:90]}")

print("\nB) Líneas 'Véase'/'véase' en bloque vivo [a82]:")
m = re.search(r"^## \[a82\].*?(?=^## \[|\Z)", ley, re.S | re.M)
for line in m.group(0).split("\n"):
    if re.search(r"[Vv]éase", line):
        print("   ·", line.strip()[:220])

print("\nC) Canon a229 completo → archivo evidencia:")
open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/canon_a229_s17_2026-09-25.txt", "w", encoding="utf-8").write(
    arts["a229"]["titulo"] + "\n\n" + arts["a229"]["texto"])
print("   palabras canon a229:", len(arts["a229"]["texto"].split()))

print("\nD) ¿Está la letra a) del canon a48 en el propio JSON canónico?")
print("   'a) Para las personas físicas' en canon a48:", "a) Para las personas físicas" in arts["a48"]["texto"])
print("   'a) En única instancia' en canon a229:", "a) En única instancia" in arts["a229"]["texto"])
