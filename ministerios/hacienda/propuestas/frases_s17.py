# Test definitivo de presencia: cada frase del canon, ¿está literal en el bloque vivo? (s17)
import json, re, unicodedata

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = canon["articulos"]
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else ""

def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("<sup>", "").replace("</sup>", "").replace("’", "'").replace("«", '"').replace("»", '"')
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

sospechosos = ["a229","a199","a27","a135","a243","a239","a67","a26","a233","a211","a40","a81","a83","a200","a164","a186","a35","a171","a221","a182","a112","a159","a247","a242","a224","a202","a46","a187","a5","a122","a181","a82","a31","a32","a73","a209","a188"]
artsd = {a["id"]: a for a in arts}
resumen = {}
for tag in sospechosos:
    a = artsd.get(tag)
    b = norm(bloque(tag))
    frases = re.split(r"(?<=[.;:])\s+", norm(a["texto"]))
    falt = []
    for f in frases:
        f = f.strip()
        if len(f) < 15:
            continue
        if f not in b:
            falt.append(f)
    fw = sum(len(f.split()) for f in falt)
    resumen[tag] = (fw, len(falt))
    print(f"== {tag}: frases ausentes literales: {len(falt)} ({fw} pal)")
    for f in falt[:4]:
        print("   ·", f[:150])

tot = sum(v[0] for v in resumen.values())
con = [t for t, v in resumen.items() if v[0] == 0]
print("---")
print("PRECEPTOS SOSPECHOSOS CUYO TEXTO CANÓNICO ESTÁ COMPLETO (test por frases):", len(con), con)
print("PALABRAS LITERALMENTE AUSENTES (suma):", tot)
