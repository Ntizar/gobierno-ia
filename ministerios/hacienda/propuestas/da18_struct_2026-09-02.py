# Extraer [dadecimoctava] con estructura estricta de parrafos del HTML vivo del BOE (09-02)
import re, io, sys, json, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

raw = open("../evidencia/boe_vivo_LGT_2026-09-02.html", encoding="utf-8", errors="replace").read()
# anclas del BOE consolidado: name="...dadecimoctava..." localizar todas las variantes
i = raw.find('id="dadecimoctava"')
assert i > 0, "ancla dadecimoctava no encontrada"
j = raw.find('id="dadecimonovena"', i+10)
assert j > i, "ancla dadecimonovena no encontrada"
chunk = raw[i:j]
# limpiar: quitar <script>...</style> etc, preservar <p>
chunk = re.sub(r"<script.*?</script>", "", chunk, flags=re.S)
chunk = re.sub(r"<style.*?</style>", "", chunk, flags=re.S)
# quitar notas de referencia del BOE (Ref. BOE-A-..., "Se modifica por...", "Seleccionar redaccion")
paras = re.split(r"</p>|<br\s*/?>", chunk)
out = []
for p in paras:
    t = re.sub(r"<[^>]+>", "", p)
    t = H.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 3:
        out.append(t)
# filtrar basura de navegacion
basura = ("Seleccionar", "Redacci\u00f3n en vigor", "Mostrar", "Ocultar", "Subir", "[Bloque", "Referencias", "Historial", "Alt", "Este documento")
clean = []
for t in out:
    if any(b in t for b in basura) or t.startswith("gobierno de") or "es:BOE-A-" in t:
        continue
    if re.match(r"^(Ref\.|Se (modifica|añade|deroga|suprime))", t):
        continue
    clean.append(t)
print("num parrafos:", len(clean))
for n, t in enumerate(clean):
    print(f"P{n:02d}|({len(t.split())}w) {t[:140]}")
json.dump(clean, open("../evidencia/da18_boe_pars_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("guardado en evidencia/da18_boe_pars_2026-09-02.json")
