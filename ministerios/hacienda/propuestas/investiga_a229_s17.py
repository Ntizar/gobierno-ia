# Investigar el hueco [a229]: localizar la frase del canon y ver qué pasó en el propuesto (s17)
import json, re

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
texto = {x["id"]: x for x in canon["articulos"]}["a229"]["texto"]
prop = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/bloque_propuesto_a229_2026-09-25.txt", encoding="utf-8").read()
vivo = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/bloque_vivo_a229_2026-09-25.txt", encoding="utf-8").read()

def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip().lower()

np_, nv = norm(prop), norm(vivo)
frases = re.split(r"(?<=[.;:])\s+(?=[A-ZÁÉÍÓÚÑ«])", norm(texto))
for f in frases:
    if len(f.split()) >= 8 and f not in np_:
        print("AUSENTE EN PROPUESTO:", f[:180])
        # ¿está en el vivo como substring cruzando saltos de línea?
        print("  ¿en vivo?:", f in nv)
        # buscar 40 primeras palabras en ambas
        head = " ".join(f.split()[:8])
        i = nv.find(head)
        print("  contexto vivo:", vivo[max(0,i-60):i+200].replace("\n", " ⏎ ") if i >= 0 else "head no encontrado en vivo")
