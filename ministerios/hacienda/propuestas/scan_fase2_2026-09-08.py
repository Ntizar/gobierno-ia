# Medidor Fase 2: tamaño real de los bloques [a12], [a57], [a65] de la LGT
# (palabras del bloque, párrafos duplicados literales, palabras duplicadas, rótulos repetidos)
import re, json

path = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
raw = open(path, encoding="utf-8").read()
blocks = re.split(r'(?=^## \[)', raw, flags=re.M)

def get(slug):
    for b in blocks:
        if b.startswith(f"## [{slug}]"):
            return b
    return None

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

report = {}
for slug in ["a12", "a57", "a65"]:
    b = get(slug)
    assert b, slug
    body = b.split("\n\n", 1)[1]
    paras = [norm(p) for p in body.split("\n\n") if norm(p)]
    counts = {}
    for p in paras:
        counts[p] = counts.get(p, 0) + 1
    dups = {k: v for k, v in counts.items() if v > 1}
    dup_words = sum(len(k.split()) * (v - 1) for k, v in dups.items())
    titulo = norm(paras[0]) if paras else ""
    rep_titulo = sum(v - 1 for k, v in counts.items() if k == titulo)
    report[slug] = {
        "palabras_bloque": len(b.split()),
        "parrafos": len(paras),
        "parrafos_unicos": len(counts),
        "parrafos_dup_lit": len(dups),
        "palabras_dup": dup_words,
        "rotulo_repetido_x": rep_titulo,
    }

# palabras totales del fichero (convención crudo del 09-04: len(b.split()) sobre todo el raw)
report["_fichero"] = {"palabras_crudo": len(raw.split())}
# versionado de [a12]: qué redacción del ap.3 es la vigente según el texto (exclusiva vs compartida)
b12 = get("a12")
report["a12"]["v1_exclusiva_ministro"] = "de forma exclusiva al Ministro de Hacienda" in b12
report["a12"]["v2_compartmentida_88_5"] = "88.5 de esta Ley" in b12
# [a65]: cuál es la última copia (la más completa: con letras b)-g) y estados/ayudas de Estado)
b65 = get("a65")
report["a65"]["menciones_letra_g_isps"] = "pagos fraccionados del Impuesto sobre Sociedades" in b65
report["a65"]["menciones_ayudas_estado"] = "ayudas de Estado" in b65
report["a65"]["menciones_efectos_timbrados"] = b65.count("efectos timbrados")
report["a65"]["menciones_de_masas_concursal"] = b65.count("créditos contra la masa")
report["a65"]["inadmision_parrafo"] = b65.count("serán objeto de inadmisión")

print(json.dumps(report, ensure_ascii=False, indent=2))
with open("ministerios/hacienda/evidencia/scan_fase2_a12_a57_a65_2026-09-08.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
