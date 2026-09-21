import re, hashlib

path = "ministerios/hacienda/leyes/BOE-A-2003-23186.md"
raw = open(path, encoding="utf-8").read()

# posiciones de los bloques objetivo
for lab in ("[a93]", "[a101]", "[a187]"):
    m = re.search(r"(?m)^## %s .*$" % re.escape(lab), raw)
    start_line = raw[:m.start()].count("\n") + 1
    nxt = re.search(r"(?m)^## \[[a-z0-9\-]+\]", raw[m.end():])
    end_line = raw[:m.end() + nxt.start()].count("\n") if nxt else raw.count("\n")
    body = raw[m.end():m.end() + (nxt.start() if nxt else len(raw))]
    words = len(re.findall(r"\S+", body))
    lines_body = body.count("\n")
    print(lab, "cabecera línea", start_line, "| cuerpo hasta", end_line, "| líneas cuerpo:", lines_body, "| palabras:", words,
          "| sha:", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])

# palabras del canon + pie
canon = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
secs = re.split(r"(?m)^={80,}$", canon)
import textwrap
for s in secs:
    m = re.search(r"## \[(a\d+)\].*?palabras: (\d+) \| sha256: (\w+)", s, re.S)
    if m:
        body = s.split("sha256:")[1].split("\n", 1)[1].strip()
        print("canon", m.group(1), "palabras declaradas:", m.group(2), "| recomputadas:", len(re.findall(r"\S+", body)), "| sha:", m.group(3)[:16])

# palabras de los pies de consolidación propuestos
pies = {
 "pie_a93": "Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 13/2023, que añade la letra e) del apartado 1). Órgano de aplicación: la Administración tributaria, a cuyo efecto las obligaciones del apartado 2 se cumplen en la forma y plazos que determine la disposición reglamentaria correspondiente; los requerimientos individualizados del apartado 3 exigen autorización del órgano reglamentariamente determinado.",
 "pie_a101": "Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 34/2015, que añade la letra c) del apartado 4). La comprobación e investigación de la totalidad de los elementos (apartado 3.a) corresponde al procedimiento inspector del título II; la regla general de duración del procedimiento es el plazo máximo de seis meses del artículo 104.",
 "pie_a187": "Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado. Los incrementos del apartado 1 operan sobre la sanción mínima y son de aplicación simultánea (apartado 2); su gestión corresponde a los órganos de la Administración tributaria competentes para la imposición de sanciones (título IV).",
}
for k, v in pies.items():
    print(k, "palabras:", len(re.findall(r"\S+", v)))
