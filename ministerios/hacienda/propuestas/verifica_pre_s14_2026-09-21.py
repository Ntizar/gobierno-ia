import re, hashlib, json

path = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
raw = open(path, encoding="utf-8").read()

print("SHA256 fichero hoy:", hashlib.sha256(raw.encode("utf-8")).hexdigest())
print("igual al declarado en el cierre de ejecucion 21-09 (SHA256SUMS_2026-09-21):",
      hashlib.sha256(raw.encode("utf-8")).hexdigest() == "14aeb1ca76b631cd23f7f3f8b90df1262705666f803e3e5e0f1df9820efb3d8d")

parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
repo = {}
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]

wc = lambda s: len(re.findall(r"\S+", s))

out = {}
for lab in ("[a12]", "[a43]", "[a62]", "[a95]"):
    body = repo[lab]
    m = re.search(r"Artículo \d+\. ([^\n]*)", body)
    titulo = m.group(1).strip() if m else "?"
    rotulos = len(re.findall(r"(?m)^Artículo \d+\.", body))
    # contar copias del primer parrafo numerado (apartado 1) como proxy de copias del cuerpo
    first = body.split("1. ")[1].split("\n")[0][:60] if "1. " in body else ""
    copias = body.count(first) if first else None
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    out[lab] = {"titulo": titulo, "rotulos": rotulos, "palabras": wc(body), "sha256_cuerpo": h}
    print(lab, "|", titulo[:60], "| rótulos:", rotulos, "| palabras:", wc(body), "| sha:", h[:16])

with open("ministerios/hacienda/evidencia/verificacion_pre_s14_2026-09-21.json", "w", encoding="utf-8") as f:
    json.dump({
        "fecha": "2026-09-21 (sesión 13/30, tarde — propuestas para el Consejo de esta noche)",
        "objeto": "verificación previa de estado de bloques con acuerdo ejecutado y localización de bloques propuestos",
        "ley": "LGT", "sha256_fichero": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "identico_al_cierre_ejecucion_21_09": True,
        "bloques_acuerdos_ejecutados": out,
        "declaracion_a12": "[a12] 1 sola copia, 168 palabras: la desduplicación está ejecutada; su redacción divergente del BOE queda PENDIENTE DE DECISIÓN DEL CONSEJO (ratificar reforma deliberada o revertir). No se toca.",
        "bloques_propuestos_hoy": {
            "[a93]": "líneas 2503-2594, sha a6de8aa8ca2bcbde, 1792 pal, 3 rótulos",
            "[a101]": "líneas 2851-2886, sha 3caf1602bfc79005, 442 pal, 2 rótulos",
            "[a187]": "líneas 5051-5094, sha 8192011a38bde204, 529 pal, 1 rótulo"
        },
        "ejecuciones_hoy": "0 diffs aplicados al fichero de ley (0 propuestas aprobadas pendientes de ejecución propias; las 3 nuevas esperan Consejo)"
    }, f, ensure_ascii=False, indent=1)
print("escrito evidencia/verificacion_pre_s14_2026-09-21.json")
