import re

canon_txt = open("ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt", encoding="utf-8").read()
secs = re.split(r"(?m)^={80,}$", canon_txt)
canon = {}
for s in secs:
    m = re.search(r"## \[(a\d+)\]", s)
    if m:
        body = s.split("\n", 2)[2].strip()
        body = re.sub(r"^palabras:.*?\n", "", body)
        canon[m.group(1)] = body

rotulos = {
 "a93": "Artículo 93. Obligaciones de información.",
 "a101": "Artículo 101. Las liquidaciones tributarias: concepto y clases.",
 "a187": "Artículo 187. Criterios de graduación de las sanciones tributarias.",
}
pies = {
 "a93": "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 13/2023, que añade la letra e) del apartado 1). Órgano de aplicación: la Administración tributaria, a cuyo efecto las obligaciones del apartado 2 se cumplen en la forma y plazos que determine la disposición reglamentaria correspondiente; los requerimientos individualizados del apartado 3 exigen autorización del órgano reglamentariamente determinado.",
 "a101": "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado (últ. mod. vigente: Ley 34/2015, que añade la letra c) del apartado 4). La comprobación e investigación de la totalidad de los elementos (apartado 3.a) corresponde al procedimiento inspector del título II; la regla general de duración del procedimiento es el plazo máximo de seis meses del artículo 104.",
 "a187": "> Consolidación 2026-09-21 (Hacienda): texto íntegro del BOE consolidado. Los incrementos del apartado 1 operan sobre la sanción mínima y son de aplicación simultánea (apartado 2); su gestión corresponde a los órganos de la Administración tributaria competentes para la imposición de sanciones (título IV).",
}

raw = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", raw)
repo = {}
for i in range(1, len(parts), 2):
    lab = re.match(r"## (\[[a-z0-9\-]+\])", parts[i]).group(1)
    repo[lab] = parts[i + 1]

wc = lambda s: len(re.findall(r"\S+", s))
tot_c = tot_p = 0
for n in ("93", "101", "187"):
    cur = wc(repo["[a%s]" % n])
    prop = wc(rotulos["a%s" % n] + "\n\n" + canon["a%s" % n] + "\n\n" + pies["a%s" % n])
    tot_c += cur; tot_p += prop
    print("a%s: actual %d -> propuesto %d (Δ %+d, %.1f%%)" % (n, cur, prop, prop - cur, 100*(prop-cur)/cur))
print("TOTAL 3 bloques: %d -> %d (Δ %+d)" % (tot_c, tot_p, tot_p - tot_c))
