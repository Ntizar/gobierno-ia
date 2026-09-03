# Reconocimiento de los JSON de fidelidad para construir el manifiesto masivo (sesion 5/30)
import json, io, sys, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open("../evidencia/fidelidad_letras_a_2026-09-01.json", encoding="utf-8"))
print("tipo:", type(d).__name__)
recs = d if isinstance(d, list) else d.get("registros", d.get("records", []))
if isinstance(d, dict):
    print("claves:", list(d.keys()))
print("num registros:", len(recs))
ks = collections.Counter()
for r in recs:
    ks.update(r.keys())
print("campos:", dict(ks))
print("ejemplo:", json.dumps(recs[0], ensure_ascii=False)[:400])
bloques = collections.Counter(r.get("bloque") for r in recs)
print("bloques distintos:", len(bloques))
print("top bloques:", bloques.most_common(8))
val = collections.Counter(str(r.get("contenido_en_repo")) for r in recs)
print("contenido_en_repo:", dict(val))
tot_pal = sum(int(r.get("palabras_est") or 0) for r in recs)
print("palabras_est suma:", tot_pal)
# categorias presentes?
cats = collections.Counter(str(r.get("categoria", "-")) for r in recs)
print("categoria:", dict(cats))
