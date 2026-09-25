# Canon vs vivo: [a229], [a48], [a82] — detalle para propuestas de hoy (25-09)
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

for tag in ("a229", "a48", "a82"):
    a = arts[tag]
    print("=" * 70)
    print("CANON", tag, "| título:", a.get("titulo"))
    txt = a["texto"]
    print("CANON texto (primeros 700):", txt[:700].replace("\n", " ⏎ "))
    m = re.search(r"^## \[" + tag + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    b = m.group(0)
    print("--- VIVO", tag, "primeros 700:", b[:700].replace("\n", " ⏎ "))
    # ¿dónde aparece la letra a) del 48 en el fichero vivo?
    if tag == "a48":
        for mm in re.finditer(r"lugar donde tengan su residencia habitual", ley):
            s = max(0, mm.start() - 80)
            ctx = ley[s:mm.start() + 60].replace("\n", " ⏎ ")
            print("APARICIÓN en fichero:", ctx)
    if tag == "a82":
        fr = re.search(r"Véase[^\n]*", txt)
        print("CANON tiene Véase:", fr.group(0)[:200] if fr else None)
        print("VIVO tiene Véase:", bool(re.search(r"[Vv]éase", b)))
