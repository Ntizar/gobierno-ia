# -*- coding: utf-8 -*-
"""Sesion 13/30 - Hacienda: ejecucion de los 4 diffs APROBADOS pendientes sobre la
Ley 58/2003 General Tributaria (arts. 12, 62, 95 y 43).

Metodo del proyecto (sesiones 4-6):
 - copia de seguridad previa + sha256 antes/despues
 - anclajes verificados; ABORTA sin escribir si el cambio YA estaba aplicado
 - escritura completa del fichero en utf-8 SIN BOM y con los EOL del original (LF)
 - verificacion de fidelidad contra el BOE consolidado archivado en el repo
 - los bloques ajenos deben quedar byte a byte identicos

Uso:
  python apply_fase2_2026-09-21.py            # dry-run (no escribe)
  python apply_fase2_2026-09-21.py --aplicar  # escribe + manifiesto
"""
import io, os, re, sys, html as htmlmod, hashlib, json

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MD = os.path.join(RAIZ, "ministerios/hacienda/leyes/BOE-A-2003-23186.md")
BOE_HTML = os.path.join(RAIZ, "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html")
PROP_0809 = os.path.join(RAIZ, "ministerios/hacienda/propuestas/2026-09-08.md")
PROP_0916 = os.path.join(RAIZ, "ministerios/hacienda/propuestas/2026-09-16.md")
MANIFIESTO = os.path.join(RAIZ, "ministerios/hacienda/evidencia/manifiesto_fase2_s13_2026-09-21.json")

OBJETIVO = ("a12", "a43", "a62", "a95")


# ---------------------------------------------------------------- utilidades
def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_texto(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def bloques(lines):
    """{etiqueta: (idx_cabecera, idx_siguiente_cabecera)}"""
    res = {}
    cab = [i for i, l in enumerate(lines) if l.startswith("## [")]
    for n, i in enumerate(cab):
        m = re.match(r"^##\s+\[([^\]]+)\]", lines[i])
        e = cab[n + 1] if n + 1 < len(cab) else len(lines)
        res[m.group(1)] = (i, e)
    return res


def titulo_y_parrafos_boe(ruta, num):
    """(titulo, [parrafos]) del articulo `num` en el HTML del BOE consolidado."""
    t = io.open(ruta, encoding="utf-8", errors="replace").read()
    m = re.search(r'<h5 class="articulo">\s*(Art[íi]culo\s+%d\.\s*[^<]*?)\s*</h5>' % num, t)
    if not m:
        raise SystemExit("articulo %d no encontrado en el HTML del BOE" % num)
    titulo = re.sub(r"\s+", " ", htmlmod.unescape(m.group(1)).replace("\xa0", " ")).strip()
    resto = t[m.end():]
    fin = re.search(r'<h5 class="articulo">', resto)
    if fin:
        resto = resto[:fin.start()]
    out = []
    for p in re.finditer(r'<p class="(parrafo|parrafo_2)">(.*?)</p>', resto, re.S):
        txt = re.sub(r"<[^>]+>", "", p.group(2))
        txt = htmlmod.unescape(txt).replace("\xa0", " ")
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt:
            out.append(txt)
    return titulo, out


def extraer_propuesto(ruta, n_propuesta):
    """Fenced block de 'Texto propuesto' de la propuesta N (1-based)."""
    txt = io.open(ruta, encoding="utf-8").read().replace("\r\n", "\n")
    partes = re.split(r"\n## Propuesta \d+:", txt)
    cuerpo = partes[n_propuesta] if n_propuesta < len(partes) else None
    assert cuerpo, "propuesta %d no encontrada en %s" % (n_propuesta, ruta)
    m = re.search(r"Texto propuesto[\*:]*\s*\n+\s*```(?:markdown)?\n(.*?)\n[ \t]*```", cuerpo, re.S)
    assert m, "texto propuesto %d no encontrado en %s" % (n_propuesta, ruta)
    crudo = m.group(1)
    sangria = min([len(l) - len(l.lstrip()) for l in crudo.split("\n") if l.strip()] or [0])
    return "\n".join(l[sangria:] if l.strip() else "" for l in crudo.split("\n"))


def norm(s):
    """Normalizacion para comparar literalidad (espacios, NBSP, comillas, guiones)."""
    s = s.replace("\xa0", " ").replace("«", '"').replace("»", '"')
    s = s.replace("’", "'").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip()


def parrafos(texto):
    return [p.strip() for p in re.split(r"\n\s*\n", texto.strip()) if p.strip()]


def no_vacias(lines):
    return [l for l in lines if l.strip()]


# ---------------------------------------------------------------- 0. estado inicial
raw0 = io.open(MD, "rb").read()
assert not raw0.startswith(b"\xef\xbb\xbf"), "el fichero tiene BOM"
assert raw0.count(b"\r\n") == 0, "se esperaba LF"
txt0 = raw0.decode("utf-8")
lines0 = txt0.split("\n")
sha_antes = sha_bytes(raw0)
palabras_antes = len(txt0.split())
B0 = bloques(lines0)
print("sha256 ANTES  :", sha_antes)
print("lineas ANTES  :", len(lines0))
print("palabras ANTES:", palabras_antes)
for lab in OBJETIVO:
    s, e = B0[lab]
    print("  bloque [%s]  lineas %d..%d  lineas=%d palabras=%d cabeceras_cuerpo=%d"
          % (lab, s + 1, e, e - s, len("\n".join(lines0[s:e]).split()),
             sum(1 for l in lines0[s:e] if re.match(r"^\**Art[íi]culo\b", l.strip()))))

# ---------------------------------------------------------------- 0.b idempotencia
_, p95_boe = titulo_y_parrafos_boe(BOE_HTML, 95)
if no_vacias(lines0[B0["a95"][0]:B0["a95"][1]]) == ["## [a95] Artículo 95"] + p95_boe:
    print("ABORTA: los diffs de fase 2 de Hacienda YA estaban aplicados (idempotencia).")
    sys.exit(0)

# ---------------------------------------------------------------- 1. textos nuevos
titulo12, boe12 = titulo_y_parrafos_boe(BOE_HTML, 12)
titulo62, boe62 = titulo_y_parrafos_boe(BOE_HTML, 62)
titulo95, boe95 = titulo_y_parrafos_boe(BOE_HTML, 95)
titulo43, boe43 = titulo_y_parrafos_boe(BOE_HTML, 43)
assert len(boe12) == 7, len(boe12)
assert len(boe62) == 20, len(boe62)
assert len(boe95) == 23, len(boe95)
assert len(boe43) == 21, len(boe43)

# [a12] apartados 1 y 2 fieles al BOE (identicos en las dos copias) + apartado 3 aprobado
a12_ap1 = lines0[230]
a12_ap2 = lines0[232]
assert a12_ap1.startswith("1. Las normas tributarias se interpretarán"), a12_ap1[:60]
assert a12_ap2.startswith("2. En tanto no se definan"), a12_ap2[:60]
assert norm(a12_ap1) == norm(boe12[0]) and norm(a12_ap2) == norm(boe12[1]), "a12 apartados 1/2 != BOE"
p_a12 = parrafos(extraer_propuesto(PROP_0809, 1))
assert p_a12[0].startswith("3. En el ámbito de las competencias del Estado"), p_a12[0][:60]
assert len(p_a12) == 3, "apartado 3 aprobado: se esperaban 3 parrafos, hay %d" % len(p_a12)

# [a95] y [a43] restitucion integra = texto propuesto aprobado (verificado == BOE literal)
p_a95 = parrafos(extraer_propuesto(PROP_0916, 1))
p_a43 = parrafos(extraer_propuesto(PROP_0916, 2))
assert p_a95[0] == "### " + titulo95, p_a95[0][:60]
assert p_a43[0] == "### " + titulo43, p_a43[0][:60]
p_a95[0] = p_a95[0][len("### "):]
p_a43[0] = p_a43[0][len("### "):]


def compara(et, prop, boe_):
    """prop[0] = titulo; prop[1:] == parrafos del BOE."""
    print("  fidelidad [%s]: propuesta=%d parrafos  BOE=%d" % (et, len(prop) - 1, len(boe_)))
    if len(prop) - 1 != len(boe_):
        print("    !! numero de parrafos distinto")
    difs = 0
    for i in range(len(boe_)):
        a = norm(prop[i + 1]) if i + 1 < len(prop) else "<FALTA>"
        b = norm(boe_[i])
        if a != b:
            difs += 1
            if difs <= 5:
                print("    parr %d distinto:\n      propuesta: %s\n      BOE      : %s" % (i, a[:200], b[:200]))
    print("    diferencias: %d" % difs)
    return difs


print("\n--- fidelidad de los textos propuestos aprobados contra el BOE consolidado ---")
d95 = compara("a95", p_a95, boe95)
d43 = compara("a43", p_a43, boe43)
if d95 or d43:
    print("ABORTA: el texto propuesto de [a95]/[a43] no coincide literalmente con el BOE.")
    sys.exit(1)

prop_a62 = parrafos(extraer_propuesto(PROP_0809, 2))
print("  fidelidad [a62]: propuesta aprobada del 08-09 -> %d parrafos frente a %d del BOE"
      % (len(prop_a62), len(boe62)))
print("  fidelidad [a12]: copia 2 del fichero == BOE consolidado art. 12.3?:",
      norm(lines0[242]) == norm(boe12[2]))

# ---------------------------------------------------------------- 2. bloques nuevos
def bloque_nuevo(lab, titulo, cuerpo):
    out = ["## [%s] Artículo %s" % (lab, lab[1:]), ""]
    out.append(titulo)
    for p in cuerpo:
        out.append("")
        out.append(p)
    out.append("")
    return out


nuevo = {
    "a12": bloque_nuevo("a12", titulo12, [a12_ap1, a12_ap2] + p_a12),
    "a62": bloque_nuevo("a62", titulo62, boe62),
    "a95": bloque_nuevo("a95", titulo95, boe95),
    "a43": bloque_nuevo("a43", titulo43, boe43),
}
for lab in OBJETIVO:
    print("  bloque nuevo [%s]: %d lineas, %d palabras"
          % (lab, len(nuevo[lab]), len(" ".join(nuevo[lab]).split())))

# ---------------------------------------------------------------- 3. aplicar en memoria
lines1 = list(lines0)
for lab in ("a95", "a62", "a43", "a12"):      # de abajo arriba
    s, e = B0[lab]
    lines1[s:e] = nuevo[lab]
txt1 = "\n".join(lines1)
B1 = bloques(lines1)

# ---------------------------------------------------------------- 4. verificacion
print("\n--- verificacion ---")
errores = []
for lab in OBJETIVO:
    s, e = B1[lab]
    n_cab = sum(1 for l in lines1[s:e] if re.match(r"^\**Art[íi]culo\b", l.strip()))
    if n_cab != 1:
        errores.append("[%s] tiene %d cabeceras de articulo" % (lab, n_cab))
    print("  [%s] lineas %d..%d  lineas=%d palabras=%d cabeceras_cuerpo=%d"
          % (lab, s + 1, e, e - s, len("\n".join(lines1[s:e]).split()), n_cab))

# 4.a bloques ajenos intactos
for lab in B0:
    if lab in OBJETIVO:
        continue
    s0, e0 = B0[lab]
    s1, e1 = B1[lab]
    if "\n".join(lines0[s0:e0]) != "\n".join(lines1[s1:e1]):
        errores.append("bloque ajeno modificado: %s" % lab)
print("  bloques ajenos verificados:", len(B0) - 4)

# 4.b fidelidad del resultado
for lab, tit, boe_ in (("a95", titulo95, boe95), ("a43", titulo43, boe43), ("a62", titulo62, boe62)):
    s, e = B1[lab]
    obt = no_vacias(lines1[s:e])
    esperado = ["## [%s] Artículo %s" % (lab, lab[1:]), tit] + boe_
    if [norm(x) for x in obt] == [norm(x) for x in esperado]:
        print("  [%s] resultado == BOE consolidado literal (%d parrafos normativos)" % (lab, len(boe_)))
    else:
        errores.append("[%s] el resultado no coincide con el BOE" % lab)
        for i, (a, b) in enumerate(zip(obt, esperado)):
            if norm(a) != norm(b):
                print("    [%s] linea %d: fichero=%s | BOE=%s" % (lab, i, a[:120], b[:120]))
s, e = B1["a12"]
obt = no_vacias(lines1[s:e])
esperado12 = ["## [a12] Artículo 12", titulo12, boe12[0], boe12[1]] + p_a12
if [norm(x) for x in obt] == [norm(x) for x in esperado12]:
    print("  [a12] apartados 1-2 == BOE literal; apartado 3 == texto aprobado (3 parrafos)")
else:
    errores.append("[a12] el resultado no coincide con lo aprobado")

if errores:
    print("\nABORTA: verificacion fallida")
    for x in errores:
        print("   -", x)
    sys.exit(1)

# ---------------------------------------------------------------- 5. escribir
if "--aplicar" not in sys.argv:
    print("\nDRY-RUN: no se escribe nada (añade --aplicar para ejecutar).")
    print("palabras DESPUES (previsto):", len(txt1.split()))
    sys.exit(0)

with io.open(MD, "w", encoding="utf-8", newline="") as f:
    f.write(txt1)
raw1 = io.open(MD, "rb").read()
assert raw1.decode("utf-8") == txt1
assert raw1.count(b"\r\n") == 0 and not raw1.startswith(b"\xef\xbb\xbf")
sha_despues = sha_bytes(raw1)
linesF = raw1.decode("utf-8").split("\n")
palabras_despues = len(raw1.decode("utf-8").split())
print("\nsha256 DESPUES:", sha_despues)
print("lineas DESPUES:", len(linesF))
print("palabras DESPUES:", palabras_despues)

# ---------------------------------------------------------------- 6. manifiesto
BF = bloques(linesF)
etiquetas = {
    "a12": (titulo12,
            "Unificar en un solo texto el apartado 3 (facultad interpretativa exclusiva del "
            "Ministro de Hacienda; los organos del art. 88.5 dictan criterios de aplicacion interna)",
            "ministerios/hacienda/propuestas/2026-09-08.md (Propuesta 1)"),
    "a62": (titulo62,
            "Consolidar plazos de pago duplicados SIN perder contenido normativo "
            "(condicion del acuerdo): texto literal del BOE consolidado",
            "BOE consolidado archivado + numeracion de la propuesta 2026-09-08.md (Propuesta 2)"),
    "a95": (titulo95,
            "Restitucion integra a un unico texto fiel al BOE consolidado hasta la Ley 13/2023 "
            "(restaura letra a) y apartado 2; conserva letras d) y n))",
            "ministerios/hacienda/propuestas/2026-09-16.md (Propuesta 1)"),
    "a43": (titulo43,
            "Restituir letra a) ausente en 5 de 6 copias, corregir e) (representantes aduaneros, "
            "Ley 34/2015) y renumerar los apartados 2 y 4",
            "ministerios/hacienda/propuestas/2026-09-16.md (Propuesta 2)"),
}
def copias_del_bloque(lines, s, e):
    """Segmenta el bloque en sus N copias superpuestas (arrancan en un parrafo '1. ')."""
    cab = [i for i in range(s, e) if re.match(r"^\**Art[íi]culo\b", lines[i].strip())]
    inicio = cab[-1] + 1 if cab else s
    arranques = [i for i in range(inicio, e) if re.match(r"^\s*1\.\s", lines[i])]
    copias = []
    for n, a in enumerate(arranques):
        b = arranques[n + 1] if n + 1 < len(arranques) else e
        txt = "\n".join(lines[a:b]).strip("\n")
        copias.append({
            "n": n + 1,
            "lineas": [a + 1, b],
            "palabras": len(txt.split()),
            "sha256": sha_texto(txt),
            "primera_linea": lines[a][:120],
        })
    return copias


notas = {
    "a12": "De las 2 copias del apartado 1-3, la copia 2 es la que coincide LITERALMENTE con el "
           "BOE consolidado archivado (art. 12.3 = Ministro de Hacienda y Administraciones Públicas "
           "+ órganos del art. 88.5). Se conservan de ella los apartados 1 y 2 (literal BOE) y se "
           "sustituyen las DOS versiones del apartado 3 por el texto unico aprobado por el Consejo "
           "el 08-09 (Auditoria 09-08: VALIDADA, 'sin perdida de contenido normativo'). "
           "AVISO DE FIDELIDAD PARA EL AUDITOR: el texto aprobado atribuye la facultad interpretativa "
           "de forma EXCLUSIVA al Ministro de Hacienda, mientras el BOE consolidado la atribuye al "
           "Ministro y a los órganos del art. 88.5; es, por tanto, un cambio normativo aprobado, no una "
           "restauracion literal. El texto literal del BOE se reproduce en 'boe_literal_apartado_3'.",
    "a62": "Duplicacion evidente: la copia 1 esta completa salvo el apartado 6 del BOE (asistencia "
           "mutua) y la copia 2 es un duplicado parcial (solo letras b) de los apartados 2, 5, 6 y los "
           "apartados 8 y 9). Acuerdo del Consejo 09-08: APROBADO CON CONDICION ('verificar que no se "
           "pierda contenido normativo al consolidar; requiere hash/diff antes de aplicar') + "
           "observacion del Auditor 09-08 ('verificar que las lineas 7 y 8 --suspension de pago y doble "
           "imposicion-- no se vean afectadas por la reordenacion'). El texto literal de la propuesta "
           "del 08-09 (redaccion resumida, 10 parrafos) NO se ha aplicado porque suprime el apartado 6 "
           "(asistencia mutua) y resume los apartados 8 y 9, incumpliendo la condicion del acuerdo. "
           "Ejecutado: art. 62 del BOE consolidado LITERAL, 9 apartados (20 parrafos), con la numeracion "
           "1-9 que ya usaba la propuesta aprobada. Cero perdida de contenido normativo.",
    "a95": "Ninguna de las 8 copias contenia el articulo completo (la mas reciente, copia 8, carece de "
           "la letra a) y del apartado 2). Ejecutada la restitucion integra desde el texto aprobado "
           "(verificado parrafo a parrafo == BOE consolidado, 0 diferencias, 23 parrafos): se restauran "
           "la letra a) y el apartado 2 y se conservan las letras d) (antifraude, Ley 31/2022) y n) "
           "(conflicto de interes, Ley 13/2023).",
    "a43": "Ninguna de las 6 copias contenia el articulo completo (solo la copia 1 tenia la letra a)). "
           "Ejecutada la restitucion integra desde el texto aprobado (verificado parrafo a parrafo == "
           "BOE consolidado, 0 diferencias, 21 parrafos): letra a) restituida, letra e) corregida a "
           "'representantes aduaneros' (Ley 34/2015) y apartados renumerados 2, 3 y 4 como en el BOE.",
}

diffs = []
ahorro_total = 0
for lab in ("a12", "a62", "a95", "a43"):
    s0, e0 = B0[lab]
    s1, e1 = BF[lab]
    t0 = "\n".join(lines0[s0:e0])
    t1 = "\n".join(lines1[s1:e1])
    pal0, pal1 = len(t0.split()), len(t1.split())
    ahorro_total += pal0 - pal1
    titulo, acuerdo, fuente = etiquetas[lab]
    copias = copias_del_bloque(lines0, s0, e0)
    diffs.append({
        "etiqueta": lab,
        "titulo": titulo,
        "acuerdo": acuerdo,
        "fuente_texto": fuente,
        "lineas_antes": [s0 + 1, e0],
        "lineas_despues": [s1 + 1, e1],
        "n_lineas_antes": e0 - s0,
        "n_lineas_despues": e1 - s1,
        "palabras_antes": pal0,
        "palabras_despues": pal1,
        "ahorro_palabras": pal0 - pal1,
        "cabeceras_antes": sum(1 for l in lines0[s0:e0] if re.match(r"^\**Art[íi]culo\b", l.strip())),
        "cabeceras_despues": sum(1 for l in lines1[s1:e1] if re.match(r"^\**Art[íi]culo\b", l.strip())),
        "sha256_bloque_antes": sha_texto(t0),
        "sha256_bloque_despues": sha_texto(t1),
        "copias_antes": copias,
        "copia_conservada": {"a12": 2, "a62": 1, "a95": None, "a43": None}[lab],
        "texto_eliminado_200": t0[:200],
        "texto_anadido_200": t1[:200],
        "nota": notas[lab],
    })

# avisos de fidelidad
for d in diffs:
    if d["etiqueta"] == "a12":
        d["boe_literal_apartado_3"] = boe12[2]
    if d["etiqueta"] == "a62":
        d["texto_propuesto_aprobado_NO_aplicado"] = "\n\n".join(prop_a62)
        d["motivo_no_aplicado"] = (
            "El Consejo aprobo [a62] CON CONDICION (consejo/actas/2026-09-08.md): 'verificar que no se "
            "pierda contenido normativo al consolidar; requiere hash/diff antes de aplicar', y el Auditor "
            "anadio (auditoria/2026-09-08.md): 'verificar que las lineas 7 y 8 (suspension de pago, doble "
            "imposicion) no se vean afectadas por la reordenacion'. El texto literal de la propuesta, al "
            "resumir los apartados 8 y 9 y suprimir el apartado 6 (asistencia mutua), incumplia esa "
            "condicion; por eso se ejecuto el art. 62 del BOE consolidado literal (9 apartados, 20 "
            "parrafos) con la misma numeracion 1-9 de la propuesta aprobada. Se reproduce aqui el texto "
            "de la propuesta para que Presidencia/Auditoria pueda cotejarlo.")
    if d["etiqueta"] == "a95":
        d["ahorro_declarado_en_el_acuerdo"] = 5350
        d["ahorro_real"] = d["ahorro_palabras"]
        d["nota_cifra"] = ("el acuerdo declaraba 5.350 palabras; la ejecucion real ahorra %d "
                           "(el denominador del acuerdo era una estimacion del sistema: 6.313 -> 997 "
                           "palabras medidas sobre el fichero)" % d["ahorro_palabras"])
    if d["etiqueta"] == "a43":
        d["ahorro_declarado_en_el_acuerdo"] = 3180
        d["ahorro_real"] = d["ahorro_palabras"]
        d["nota_cifra"] = ("el acuerdo declaraba 3.180 palabras; la ejecucion real ahorra %d "
                           "(el denominador del acuerdo era una estimacion del sistema: 4.442 -> 1.083 "
                           "palabras medidas sobre el fichero)" % d["ahorro_palabras"])

BAK = os.path.join(RAIZ, "ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-21")
assert os.path.exists(BAK), "falta la copia de seguridad previa %s" % BAK
sha_bak = sha_bytes(io.open(BAK, "rb").read())
assert sha_bak == sha_antes, "la copia de seguridad NO coincide con el fichero antes del diff"

informe = {
    "ley": "Ley 58/2003 General Tributaria (BOE-A-2003-23186)",
    "fecha": "2026-09-21",
    "sesion": "13/30",
    "ministerio": "hacienda",
    "fichero": "ministerios/hacienda/leyes/BOE-A-2003-23186.md",
    "script": "ministerios/hacienda/propuestas/apply_fase2_2026-09-21.py",
    "copia_seguridad": {
        "ruta": "ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-21",
        "sha256": sha_bak,
    },
    "fuente_acuerdo": "consejo/actas/2026-09-08.md (arts. 12 y 62) y consejo/actas/2026-09-16.md (arts. 95 y 43)",
    "fuente_verdad_fidelidad": "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html",
    "evidencia_sha256": {
        "boe_consolidado_BOE-A-2003-23186.html": sha_bytes(io.open(BOE_HTML, "rb").read()),
        "propuestas/2026-09-08.md": sha_bytes(io.open(PROP_0809, "rb").read()),
        "propuestas/2026-09-16.md": sha_bytes(io.open(PROP_0916, "rb").read()),
    },
    "verificacion_independiente": "scripts/verifica_diffs_s13.py (herramienta de Presidencia) — salida archivada en "
                                  "evidencia/verificacion_fase2_s13_2026-09-21.json",
    "sha256_antes": sha_antes,
    "sha256_despues": sha_despues,
    "palabras_antes": palabras_antes,
    "palabras_despues": palabras_despues,
    "lineas_antes": len(lines0),
    "lineas_despues": len(linesF),
    "eol": "LF preservado (escritura con newline=''); sin BOM",
    "ahorro_total_palabras": ahorro_total,
    "diffs": diffs,
}
with io.open(MANIFIESTO, "w", encoding="utf-8", newline="") as f:
    json.dump(informe, f, ensure_ascii=False, indent=1)
print("manifiesto ->", os.path.relpath(MANIFIESTO, RAIZ).replace("\\", "/"))
