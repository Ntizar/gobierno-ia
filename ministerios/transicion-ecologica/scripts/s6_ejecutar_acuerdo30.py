# Sesion 6 BLOQUE 1 — EJECUCION del acuerdo 30 (Consejo 2026-09-03): restitucion de las
# 532 palabras de omision REAL con fuerza obligatoria (22 lineas, evidencia/
# textos_restitucion_532_2026-09-04.json, clasificacion 2026-09-03 «omision_real_...») sobre
# leyes/BOE-A-2021-8447.md + supresion del rotulo dupe de [da-6] (5 palabras, observacion
# del Auditor al acuerdo 29).
#
# Anclaje: cada linea va en SU lista/parrafo segun el BOE consolidado archivado
# (evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html, modif. 04/12/2025). Los rotulos
# TITULO I/II/III/IV/VI/IX van antes de SU cabecera de articulo. Anclajes UNICOS con
# contexto exacto, o ABORTA sin escribir (leccion del incidente de ancoraje del jueves).
# Enlaces BOE partidos en <a> se insertan como parrafo continuo (k4, k10, k13+14, k15 en
# L822, k17-cierre, k20+k21) y TODO texto extra se verifica literal contra el HTML.
# El script NUNCA toca la ley directamente: lee <SRC_IN>, escribe <SRC_OUT>; la promocion
# la decide el operador. CRLF nativo conservado.
import hashlib, html, json, re, sys

BASE = "ministerios/transicion-ecologica"
SRC_IN, SRC_OUT = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
wc = lambda ls: len(re.findall(r"\S+", "\n".join(ls)))

raw = open(SRC_IN, "rb").read()
NL = "\r\n" if b"\r\n" in raw else "\n"
lines = raw.decode("utf-8").split(NL)
txt_repo = norm(NL.join(lines))

h = html.unescape(re.sub(r"<[^>]+>", " ", open(f"{BASE}/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8").read()))
hb = re.sub(r"\s+([,.;:»])", r"\1", norm(h))  # quita el espacio que deja la etiqueta </a> antes de la coma

T = json.load(open(f"{BASE}/evidencia/textos_restitucion_532_2026-09-04.json", encoding="utf-8"))
K = {k: norm(T[str(k)]) for k in range(22)}
assert sum(len(v.split()) for v in K.values()) == 532
for v in K.values():
    assert norm(v) in hb, f"JSON no es literal del BOE archivado: {v[:60]}"

def find1(pat):
    e = norm(pat)
    hits = [i for i, l in enumerate(lines) if norm(l).startswith(e)]
    assert len(hits) == 1, f"ANCLAJE NO UNICO ({len(hits)}) {pat[:55]!r} -> {hits}"
    return hits[0]

def findh(hdr):
    hits = [i for i, l in enumerate(lines) if l.strip() == hdr]
    assert len(hits) == 1, f"CABECERA NO UNICA {hdr!r} -> {hits}"
    return hits[0]

def mustin(x, tag):
    assert norm(x) in hb, f"BOE check fallido [{tag}]: {x[:70]}"
    return norm(x)

# --- parrafos continuos del BOE que el repo perdi6 (con enlaces fusionados) ---
K4_FULL  = mustin(K[4] + " Real Decreto 102/2011, de 28 de enero, relativo a la mejora de la calidad del aire.", "k4")
K10_FULL = mustin("4. A los efectos de lo previsto en el " + K[10] + ", de Régimen Jurídico del Sector Público, la vigencia de los convenios de transición justa vendrá determinada en las cláusulas del propio convenio, no pudiendo superar en ningún caso los siete años de duración inicial. Los firmantes podrán acordar su prórroga, antes de la finalización del plazo de vigencia previsto, por un período de hasta siete años adicionales.", "k10")
M13_14   = mustin(K[13] + " artículo 14 de la Ley 24/2013, de 26 de diciembre, del Sector Eléctrico redactado en los siguientes términos:", "k13+k14")
L820 = mustin("«8.bis. Las metodologías de retribución de las actividades de transporte y de distribución deberán contemplar incentivos económicos, que podrán tener signo positivo o negativo, para la mejora de la disponibilidad de las instalaciones, para garantizar el nivel de endeudamiento adecuado a fin de disponer de una estructura de deuda sostenible y otros objetivos.»", "8.bis")
L822 = mustin("3. Se modifica el artículo 20.9 de la Ley 24/2013, de 26 de diciembre, del Sector Eléctrico, quedando redactado en los siguientes términos:", "822 (incluye k15)")
L826 = mustin("4. El apartado 1 del artículo 60 de la Ley 18/2014, de 15 de octubre, de aprobación de medidas urgentes para el crecimiento, la competitividad y la eficiencia, queda redactado en los siguientes términos:", "826")
L829 = mustin("La metodología de retribución de las actividades de transporte, regasificación, almacenamiento y distribución de gas natural deberá incluir los incentivos que correspondan, que podrán tener signo positivo o negativo, para garantizar el nivel de endeudamiento adecuado que permita disponer de una estructura de deuda sostenible y otros objetivos.", "829")
L836 = mustin("«1. En las Leyes de Presupuestos Generales del Estado de cada año se destinará a financiar los costes del sistema eléctrico previstos en la Ley del Sector Eléctrico, referidos a fomento de energías renovables, un importe equivalente a la suma de la estimación de la recaudación anual derivada de los tributos incluidos en la Ley de medidas fiscales para la sostenibilidad energética.", "836")
P845 = mustin("«2. Las sociedades que realicen actividades incluidas en las letras a) y b) del apartado 1 anterior, deberán comunicar a la Secretaría de Estado de Energía del Ministerio para la Transición Ecológica y el Reto Demográfico las adquisiciones realizadas directamente o mediante sociedades que controlen conforme a los criterios establecidos en el " + K[20] + K[21], "845+k20+k21")
L848 = mustin("En las mismas circunstancias señaladas en el párrafo anterior, se deberán comunicar igualmente las adquisiciones que realicen las sociedades matrices de los grupos de sociedades designadas como gestor de la red de transporte de electricidad y gas natural, así como cualesquiera otras sociedades que formen parte de dichos grupos.»", "848")
L826 = mustin("4. El apartado 1 del artículo 60 de la Ley 18/2014, de 15 de octubre, de aprobación de medidas urgentes para el crecimiento, la competitividad y la eficiencia, queda redactado en los siguientes términos:", "826")
M12_FULL = mustin("1. Se añade un nuevo apartado 6 en el artículo 62 de la Ley 34/1998, de 7 de octubre, del sector de hidrocarburos, del siguiente tenor literal:", "df1-lead")
assert M12_FULL in txt_repo, "el lead fusionado de DF1 no está ya en el repo (anclaje inesperado)"
for x, tag in [(K4_FULL, "k4"), (K10_FULL, "k10"), (M13_14, "13+14"), (L820, "8.bis"), (L822, "822"), (P845, "845"), (L848, "848"), (L836, "836")]:
    assert x not in txt_repo, f"el texto {tag} YA estaba en el repo (doble insercion)"

edits = []  # (i0, i1, nuevas_lineas, tag)

# --- rotulos de TITULO antes de cada cabecera de articulo ---
for k, hdr, label, art in [(0, "## [a3] Artículo 3", "TÍTULO I", "Artículo 3."),
                           (1, "## [a7] Artículo 7", "TÍTULO II", "Artículo 7."),
                           (2, "## [a9] Artículo 9", "TÍTULO III", "Artículo 9."),
                           (3, "## [a1-6] Artículo 14", "TÍTULO IV", "Artículo 14."),
                           (8, "## [a2-9] Artículo 27", "TÍTULO VI", "Artículo 27."),
                           (11, "## [a3-9] Artículo 37", "TÍTULO IX", "Artículo 37.")]:
    i = findh(hdr)
    assert norm(lines[i+1]) == "" and lines[i+2].startswith(art), f"contexto cabecera roto {hdr}"
    edits.append((i, i - 1, [label, K[k], ""], f"rotulo {label} (k={k})"))

# --- k4: parrafo nuevo tras i) de ultima milla ---
i = find1("i) Integrar los planes específicos")
i2 = find1("Los planes de movilidad urbana sostenible")
assert i2 == i + 2, (i, i2)
edits.append((i2, i2 - 1, [K4_FULL, ""], "k4 parrafo tras i) (letra j implicita)"))

# --- k5, k6 ---
for k, anchor, prevl in [(5, "a) La identificación y evaluación", "e)"), (6, "a) Anticiparse a los impactos", "d)")]:
    i = find1(anchor)
    assert norm(lines[i-1]) == "" and norm(lines[i-2]).startswith(prevl), (i, lines[i-2][:40])
    edits.append((i, i - 1, [K[k], ""], f"k{k}"))

def last_content_before(h):
    j = h - 1
    while j >= 0 and norm(lines[j]) == "":
        j -= 1
    return j

# --- k7, k9, k10: antes de cabeceras Art 20/28/29 (el ancla debe ser el ultimo contenido) ---
for hdr, anchor, newl, tag in [
    ("## [a2-2] Artículo 20", "i) Realizar el seguimiento", [K[7], ""], "k7 art19.5"),
    ("## [a2-10] Artículo 28", "e) El marco de elaboración", [K[9], ""], "k9 art27.3"),
    ("## [a2-11] Artículo 29", "e) Cuando se considere procedente", [K10_FULL, ""], "k10 art28.4")]:
    h = findh(hdr); i = find1(anchor)
    assert last_content_before(h) == i, f"{tag}: ancla {i} no es ultimo contenido antes de {h}"
    edits.append((h, h - 1, newl, tag))

# --- DF1: cuerpo k12..k17 tras el lead fusionado, antes de [df-2] ---
lead = find1("1. Se añade un nuevo apartado 6 en el")
df2 = findh("## [df-2] Disposición final segunda")
assert last_content_before(df2) == lead, "DF1: el lead no es ultimo contenido"
edits.append((df2, df2 - 1, [K[12], "", M13_14, L820, "", L822, K[16], "", L826, K[17], L829, ""], "DF1 cuerpo k12-k17"))

# --- DF2: cuerpo k18-k19 tras el lead, antes de [df-3] ---
lead = find1("La disposición adicional segunda de la Ley 15/2012")
df3 = findh("## [df-3] Disposición final tercera")
assert last_content_before(df3) == lead, "DF2: el lead no es ultimo contenido"
edits.append((df3, df3 - 1, [L836, K[18], K[19], ""], "DF2 cuerpo k18-k19"))

# --- DF3: cuerpo k20-k21 tras el lead, antes de [df-4] ---
lead = find1("El apartado 2 de la disposición adicional novena")
df4 = findh("## [df-4] Disposición final cuarta")
assert last_content_before(df4) == lead, "DF3: el lead no es ultimo contenido"
edits.append((df4, df4 - 1, [P845, L848, ""], "DF3 cuerpo k20-k21"))

# --- [da-6]: borrar rotulo dupe y su blanco previo ---
rn = [norm(x) for x in lines]
tit = [i for i, l in enumerate(rn) if l == "Disposición adicional sexta. Transporte Ferroviario."]
assert len(tit) == 2 and tit[1] == tit[0] + 2 and rn[tit[1]-1] == "", tit
edits.append((tit[1] - 1, tit[1], [], "[da-6] rotulo dupe fuera (-5 palabras)"))

# --- aplicar de abajo arriba ---
edits.sort(key=lambda e: -e[0])
for i0, i1, newl, tag in edits:
    lines[i0:i1 + 1] = newl

out = NL.join(lines)
open(SRC_OUT, "wb").write(out.encode("utf-8"))

# --- verificacion post ---
chk = norm(out)
missing = [k for k in range(22) if K[k] not in chk]
rn2 = [norm(x) for x in out.split(NL)]
d6 = sum(1 for l in rn2 if l == "Disposición adicional sexta. Transporte Ferroviario.")
titulos = sorted(l for l in rn2 if re.match(r"^T[IÍ]TULO [IVX]+$", l))
assert not missing, f"FALTAN tras la ejecucion: {missing}"
assert d6 == 1, d6
# SOLO los 6 del JSON 532: los titulos V, VII y VIII siguen ausentes (deuda fase 3)
assert len(titulos) == 6, titulos
print(json.dumps({
  "entrada": SRC_IN, "salida": SRC_OUT,
  "sha256_entrada": hashlib.sha256(raw).hexdigest(),
  "sha256_salida": hashlib.sha256(out.encode("utf-8")).hexdigest(),
  "lineas_antes": len(raw.decode("utf-8").split(NL)), "lineas": len(rn2),
  "palabras_antes": wc(raw.decode("utf-8").split(NL)), "palabras": wc(out.split(NL)),
  "faltan_json": missing, "da6_rotulos": d6, "rotulos_titulo": titulos,
  "ediciones": [t for _, _, _, t in edits],
}, ensure_ascii=False, indent=1))
