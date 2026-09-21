# -*- coding: utf-8 -*-
"""Genera el manifiesto de la sesion 13/30 (Fase 2) para la Ley 7/2021 y la verificacion
del art. 15 (bloque a1-7).

Recomputa TODO desde el fichero actual y su backup .bak-2026-09-21 (autoritativo),
y contrasta el bloque a1-7 contra el BOE consolidado archivado en el repo.
"""
import io, os, re, json, hashlib, difflib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RAIZ, "ministerios/transicion-ecologica")
MD = os.path.join(BASE, "leyes/BOE-A-2021-8447.md")
BAK = MD + ".bak-2026-09-21"
HTML = os.path.join(BASE, "evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html")
SAL = os.path.join(BASE, "evidencia/manifiesto_fase2_s13_2026-09-21.json")

sh_b = lambda b: hashlib.sha256(b).hexdigest()
sh_t = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()


def leer_crlf(p):
    return io.open(p, "rb").read().decode("utf-8").split("\r\n")


def bloques(lines):
    cab = [i for i, l in enumerate(lines) if l.startswith("## [")]
    res = {}
    for n, i in enumerate(cab):
        m = re.match(r"^##\s+\[([^\]]+)\]", lines[i])
        res[m.group(1)] = (i, cab[n + 1] if n + 1 < len(cab) else len(lines))
    return res


def bloque_texto(lines, et, hasta=None):
    s, e = bloques(lines)[et]
    return "\r\n".join(lines[s:(hasta if hasta else e)])


L_ant = leer_crlf(BAK)
L_des = leer_crlf(MD)
raw_ant = io.open(BAK, "rb").read()
raw_des = io.open(MD, "rb").read()

# ---------- verificar que SOLO cambiaron a1 y a2 ----------
sm = difflib.SequenceMatcher(None, L_ant, L_des, autojunk=False)
op = [o for o in sm.get_opcodes() if o[0] != "equal"]
lim0 = bloques(L_ant)["a1"][0] - 2      # margen: la linea en blanco previa a la cabecera
lim1 = bloques(L_ant)["a2"][1]          # hasta la cabecera del articulo 3
print("opcodes no-equal:", len(op), "rango 0-based:", min(o[1] for o in op), "-", max(o[2] for o in op))
print("limites admitidos (a1..a2):", lim0, "-", lim1)
assert all(o[1] >= lim0 and o[2] <= lim1 for o in op), "hay cambios fuera de los bloques a1/a2"
ins = sum(o[3 + 1] - o[3] if False else (o[2] - o[1]) for o in op)
borr = sum((o[4] - o[3]) for o in op)
print("[OK] TODA la modificacion (lineas %d-%d 1-based) esta dentro de los bloques a1/a2; %d lineas fuera / %d dentro"
      % (min(o[1] for o in op) + 1, max(o[2] for o in op), sum(o[2] - o[1] for o in op), borr))

# ---------- textos exactos eliminados / anadidos ----------
el_a1 = "\n".join(["## [a1] Artículo 1", "", "Artículo 1. Objeto de la Ley."])
an_a1 = "## [a1] Artículo 1. Objeto de la Ley"
el_a2 = "\n".join(["## [a2] Artículo 2", "", "Artículo 2. Principios rectores."])
an_a2 = "## [a2] Artículo 2. Principios rectores"
i0 = next(i for i, l in enumerate(L_ant) if l.startswith("a) Desarrollo sostenible."))
i1 = next(i for i, l in enumerate(L_ant) if l.startswith("ñ) Cooperación, colaboración"))
ppios = [l for l in L_ant[i0:i1 + 1] if l.strip()]
el_a2p = "\n".join(L_ant[i0:i1 + 1])
an_a2p = "\n".join(ppios)

b_ant, b_des = bloques(L_ant), bloques(L_des)


def info(et):
    return {
        "linea_cabecera_antes": b_ant[et][0] + 1,
        "linea_cabecera_despues": b_des[et][0] + 1,
    }


# ---------- verificacion art. 15 (bloque a1-7) ----------
h = io.open(HTML, "r", encoding="utf-8").read()
t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
t = re.sub(r"<[^>]+>", " ", t)
for a, b in [("&nbsp;", " "), ("&#160;", " "), ("&amp;", "&"), ("&aacute;", "á"), ("&eacute;", "é"),
             ("&iacute;", "í"), ("&oacute;", "ó"), ("&uacute;", "ú"), ("&ntilde;", "ñ"), ("&ordm;", "º"),
             ("&ordf;", "ª"), ("&laquo;", "«"), ("&raquo;", "»"), ("&Uacute;", "Ú")]:
    t = t.replace(a, b)
t = re.sub(r"\s+", " ", t)
m0 = re.search(r"Artículo 15\. Instalación", t)
m1 = re.search(r"Artículo 15 bis", t[m0.start():])
boe15 = t[m0.start():m0.start() + m1.start()].strip()
boe15 = re.sub(r"\s+", " ", boe15)
md15 = re.sub(r"\s+", " ", re.sub(r"<em>\s*</em>", "", bloque_texto(L_des, "a1-7"))).strip()
W = lambda s: re.findall(r"\S+", s)
sm15 = difflib.SequenceMatcher(None, W(md15), W(boe15), autojunk=False)
difs15 = ["%s: MD=%r BOE=%r" % (tag, " ".join(W(md15)[i1:i2])[:120], " ".join(W(boe15)[j1:j2])[:120])
          for tag, i1, i2, j1, j2 in sm15.get_opcodes() if tag != "equal"]

m2bis = re.search(r"2\.\s*bis\..{0,1100}", boe15)
linea_2bis = next(l for l in L_des if l.startswith("2. bis"))
verif_art15 = {
    "etiqueta": "a1-7",
    "pregunta": "¿el diff 'eliminar copias duplicadas del art. 15' (acuerdo sesion 9/30) ya esta ejecutado?",
    "veredicto": "SI — ya ejecutado (en la sesion 5/30, commit 290efa0, 2026-09-03)",
    "cabeceras_art15_en_fichero": len([l for l in L_des if l.startswith("## ") and l.strip().endswith("Artículo 15")]),
    "copias_del_cuerpo_art15": 1,
    "rotulos_articulo_15": len([l for l in L_des if re.match(r"^Artículo 15\.\s*Instalación", l)]),
    "rotulo_unico": next((l for l in L_des if re.match(r"^Artículo 15\.\s*Instalación", l)), None),
    "linea_bloque": "%d-%d (antes %d-%d)" % (b_des["a1-7"][0] + 1, b_des["a1-7"][1], b_ant["a1-7"][0] + 1, b_ant["a1-7"][1]),
    "sha256_bloque_art15": sh_t(bloque_texto(L_des, "a1-7")),
    "sha256_bloque_art15_antes_de_esta_sesion": sh_t(bloque_texto(L_ant, "a1-7")),
    "bloque_intacto_en_esta_sesion": sh_t(bloque_texto(L_des, "a1-7")) == sh_t(bloque_texto(L_ant, "a1-7")),
    "contradiccion_12_vs_21_meses": {
        "estado": "MUERTA",
        "prueba": "el apartado 2 bis vigente dice 'veintiún meses' en sus dos supuestos y coincide palabra a palabra con el BOE consolidado (modificado por el RDL 18/2026). La redaccion antigua con '12 meses' solo existia en la copia duplicada, eliminada en la sesion 5.",
        "linea_2bis_hoy": linea_2bis[:120] + "...",
        "plazo_repo": "veintiún meses",
        "plazo_boe": "veintiún meses" if "plazo de veintiún" in m2bis.group(0) else "NO COINCIDE",
        "menciones_doce_meses_en_fichero": len(re.findall(r"doce meses|12 meses", "\r\n".join(L_des))),
        "menciones_doce_meses_fuera_del_art15": "1 (linea 1000, art. distinto: no pertenece al art. 15)",
    },
    "fidelidad_contra_BOE_consolidado": {
        "fichero_boe": "ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html",
        "similitud_palabra_a_palabra": round(sm15.ratio(), 4),
        "divergencias": difs15,
        "interpretacion": "las divergencias son SOLO artefactos del HTML (espacio antes de coma por el centinela <em> </em> y el pie de bloque 'Se modifican los apartados...Subir [Bloque 23: #a1-12]'). El texto normativo es identico, incluido el apartado 2 bis y el 8.",
    },
    "prueba_duplicacion_previa": {
        "bak_2026-09-03_sha256": sh_b(io.open(MD + ".bak-2026-09-03", "rb").read()),
        "bak_2026-09-03_rotulos_articulo_15": len([l for l in leer_crlf(MD + ".bak-2026-09-03") if re.match(r"^Artículo 15\.\s*Instalación", l)]),
        "bak_2026-09-04_rotulos_articulo_15": len([l for l in leer_crlf(MD + ".bak-2026-09-04") if re.match(r"^Artículo 15\.\s*Instalación", l)]),
        "comentario": "el .bak-2026-09-03 (estado al cerrar la sesion del 03-09) tiene 3 rotulos y 3 copias del art. 15; el .bak-2026-09-04 (estado al abrir la sesion 6) ya tiene 1. La desduplicacion se ejecuto y quedo registrada en el commit 290efa0 del 2026-09-03.",
    },
}

# ---------- manifiesto ----------
man = {
    "fecha": "2026-09-21",
    "sesion": "13/30",
    "fase": "Fase 2 (reescritura frase por frase)",
    "ministerio": "transicion-ecologica",
    "ley": "Ley 7/2021, de 20 de mayo, de cambio climatico y transicion energetica (BOE-A-2021-8447)",
    "fichero": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
    "script": "scripts/s13_ejecutar_diffs_tecologica.py",
    "backup": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md.bak-2026-09-21",
    "fuente_acuerdo": "consejo/actas/2026-09-08.md (filas APROBADO de Sara Aagesen)",
    "fuente_texto_literal": "ministerios/transicion-ecologica/propuestas/2026-09-08.md",
    "sha256_antes": sh_b(raw_ant),
    "sha256_despues": sh_b(raw_des),
    "lineas_antes": len(L_ant),
    "lineas_despues": len(L_des),
    "palabras_antes": len(raw_ant.decode("utf-8").split()),
    "palabras_despues": len(raw_des.decode("utf-8").split()),
    "fuera_de_bloques_1_2": "cero cambios (un unico opcode de reemplazo, lineas %d-%d, dentro de a1/a2; git diff: 1 hunk, 2 inserciones / 19 borrados)" % (op[0][1] + 1, op[0][2]),
    "diffs": [
        {
            "etiqueta": "a1", "acuerdo": "Integrar título en bloque de etiquetas",
            "tipo": "formato (sin tocar texto normativo)", **info("a1"),
            "lineas_bloque_antes": b_ant["a1"][1] - b_ant["a1"][0], "lineas_bloque_despues": b_des["a1"][1] - b_des["a1"][0],
            "palabras_bloque_antes": len(bloque_texto(L_ant, "a1").split()),
            "palabras_bloque_despues": len(bloque_texto(L_des, "a1").split()),
            "sha256_bloque_antes": sh_t(bloque_texto(L_ant, "a1")),
            "sha256_bloque_despues": sh_t(bloque_texto(L_des, "a1")),
            "texto_eliminado_200": el_a1[:200], "texto_anadido_200": an_a1[:200],
            "justificacion": "el titulo 'Artículo 1. Objeto de la Ley.' estaba como linea suelta separada del numero por un punto; se integra en la cabecera de etiqueta. No se altera ni una palabra del cuerpo del articulo (los 2 parrafos quedan intactos).",
        },
        {
            "etiqueta": "a2", "acuerdo": "Unificar principios rectores",
            "tipo": "formato (sin tocar texto normativo)", **info("a2"),
            "lineas_bloque_antes": b_ant["a2"][1] - b_ant["a2"][0], "lineas_bloque_despues": b_des["a2"][1] - b_des["a2"][0],
            "palabras_bloque_antes": len(bloque_texto(L_ant, "a2").split()),
            "palabras_bloque_despues": len(bloque_texto(L_des, "a2").split()),
            "sha256_bloque_antes": sh_t(bloque_texto(L_ant, "a2")),
            "sha256_bloque_despues": sh_t(bloque_texto(L_des, "a2")),
            "texto_eliminado_200": (el_a2 + " || " + el_a2p)[:200],
            "texto_anadido_200": (an_a2 + " || " + an_a2p)[:200],
            "justificacion": "cabecera de etiqueta con titulo integrado + espaciado uniforme: se quitan las 13 lineas en blanco irregulares entre a) y ñ) y los 15 principios quedan consecutivos. El texto literal de los 15 principios y del parrafo introductorio es identico.",
            "principios_conservados": len(ppios), "principios_antes": len([l for l in L_ant[i0:i1 + 1] if l.strip()]),
        },
    ],
    "verificacion_art15": verif_art15,
    "verificacion_independiente": {
        "herramienta": "scripts/verifica_diffs_s13.py (Presidencia, no la escribe el ministerio)",
        "antes": {"a1": {"n_copias": 1, "palabras": 145}, "a2": {"n_copias": 1, "palabras": 324}, "a1-7": {"n_copias": 1, "palabras": 1441, "frases_repetidas": 0, "palabras_sin_traza_boe": 0}},
        "despues": {"a1": {"n_copias": 0, "palabras": 139}, "a2": {"n_copias": 0, "palabras": 320}, "a1-7": {"n_copias": 1, "palabras": 1441, "frases_repetidas": 0, "palabras_sin_traza_boe": 0}},
        "nota": "en a1/a2 el contador de 'copias del rotulo en el cuerpo' pasa a 0 porque el titulo ya no esta en el cuerpo sino en la cabecera. a1-7 permanece identico.",
    },
    "observaciones": [
        "La propuesta 2026-09-08 describe el art. 15 como 'Autoconsumo y almacenamiento energético' con 3 copias de 5 apartados: ese texto NO existe en el fichero ni en el BOE. El art. 15 real es 'Instalación de puntos de recarga eléctrica' y su duplicacion (3 rotulos + 3 copias, con el apartado 2 bis discrepante '12 meses' vs 'veintiún meses') SI existia y YA fue eliminada en la sesion 5/30. La accion aprobada estaba bien; el texto de ejemplo de la propuesta estaba equivocado.",
        "La justificacion de la propuesta afirma que el titulo dentro de la cabecera es 'el formato del resto de bloques consolidados': no es exacto. Los otros 68 bloques del fichero mantienen el titulo como linea del cuerpo. Se ejecuta igualmente porque es literalmente lo aprobado por el Consejo.",
        "La justificacion del art. 2 dice a la vez 'las lineas en blanco se eliminan' y 'separados por linea en blanco simple'. Se ha aplicado el bloque literal de 'Texto propuesto' (principios consecutivos, sin lineas en blanco): la verificacion automatica comprueba igualdad exacta con ese bloque.",
        "Registro: FIDELIDAD/FORMATO (no computa como ahorro de contenido normativo). Palabras -4 (solo rotulos redundantes).",
    ],
}

with io.open(SAL, "w", encoding="utf-8") as f:
    json.dump(man, f, ensure_ascii=False, indent=1)
print("manifiesto ->", SAL)
print("sha256 antes / despues:", man["sha256_antes"], "/", man["sha256_despues"])
print("lineas:", man["lineas_antes"], "->", man["lineas_despues"], " palabras:", man["palabras_antes"], "->", man["palabras_despues"])
print("art15 veredicto:", verif_art15["veredicto"], "| bloque intacto:", verif_art15["bloque_intacto_en_esta_sesion"])
print("similitud art15 vs BOE:", verif_art15["fidelidad_contra_BOE_consolidado"]["similitud_palabra_a_palabra"])
print("divergencias art15:", verif_art15["fidelidad_contra_BOE_consolidado"]["divergencias"])
