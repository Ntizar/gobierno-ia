# Verificación: todo el canon ⊆ bloque propuesto (substring normalizado, multilínea a una línea) (s17)
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = {a["id"]: a for a in canon["articulos"]}

def norm(s):
    s = s.replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

ok = True
for tag in ("a229", "a203", "a188"):
    prop = open(rf"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/bloque_propuesto_{tag}_2026-09-25.txt", encoding="utf-8").read()
    np_ = norm(prop)
    # canon completo normalizado como un solo bloque: ¿está íntegro en el propuesto?
    ct = norm(arts[tag]["texto"])
    if ct in np_:
        print(f"[{tag}] CANON ÍNTEGO en propuesto (substring completo) ✔")
        continue
    # si no, búsqueda frase a frase sobre todo el bloque normalizado
    frases = re.split(r"(?<=[.;:])\s+(?=[A-ZÁÉÍÓÚÑ«])", ct)
    aus = [f[:110] for f in frases if len(f.split()) >= 8 and f not in np_]
    print(f"[{tag}] canon NO íntegro como bloque; frases ausentes: {len(aus)}")
    for f in aus:
        print("   ·", f)
    ok = False
print("RESULTADO GLOBAL:", "PASS" if ok else "HAY HUECOS — revisar")
