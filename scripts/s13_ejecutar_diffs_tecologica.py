# -*- coding: utf-8 -*-
"""Sesion 13/30 - Transicion Ecologica: ejecucion de los 2 diffs APROBADOS pendientes
(arts. 1 y 2 de la Ley 7/2021) sobre leyes/BOE-A-2021-8447.md.

Metodo del proyecto (sesiones 5-6):
 - anclajes unicos verificados
 - ABORTA sin escribir si el cambio YA estaba aplicado (idempotencia)
 - escribe con newline='' para PRESERVAR los CRLF del original
 - verifica el resultado contra el 'Texto propuesto' literal de propuestas/2026-09-08.md

Uso:  python scripts/s13_ejecutar_diffs_tecologica.py
"""

import io, re, json, hashlib, os, sys, difflib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md")
PROP = os.path.join(RAIZ, "ministerios/transicion-ecologica/propuestas/2026-09-08.md")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_texto(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def bloques(lines):
    """Devuelve {etiqueta: (s, e)} con s = indice del '## [' y e = indice del siguiente '## ['."""
    res = {}
    cab = [i for i, l in enumerate(lines) if l.startswith("## [")]
    for n, i in enumerate(cab):
        m = re.match(r"^##\s+\[([^\]]+)\]", lines[i])
        e = cab[n + 1] if n + 1 < len(cab) else len(lines)
        res[m.group(1)] = (i, e)
    return res


def bloque_texto(lines, etiqueta):
    s, e = bloques(lines)[etiqueta]
    return "\r\n".join(lines[s:e])


def extraer_propuesto(ruta, n_propuesta):
    """Extrae el fenced block de '### Texto propuesto' de la propuesta N (1-based)."""
    txt = io.open(ruta, encoding="utf-8").read().replace("\r\n", "\n")
    partes = re.split(r"\n## Propuesta \d+:", txt)
    cuerpo = partes[n_propuesta] if n_propuesta < len(partes) else None
    assert cuerpo, "propuesta %d no encontrada" % n_propuesta
    m = re.search(r"### Texto propuesto\s*\n+```(?:markdown)?\n(.*?)\n```", cuerpo, re.S)
    assert m, "texto propuesto %d no encontrado" % n_propuesta
    return m.group(1)


# ---------- 0. estado inicial ----------
raw0 = io.open(MD, "rb").read()
txt0 = raw0.decode("utf-8")
assert b"\r\n" in raw0, "se esperaba CRLF"
lines = txt0.split("\r\n")
sha_antes = sha256_bytes(raw0)
palabras_antes = len(txt0.split())
print("sha256 ANTES fichero :", sha_antes)
print("lineas ANTES         :", len(lines))
print("palabras ANTES       :", palabras_antes)

# ---------- 0.b idempotencia ----------
if "## [a1] Artículo 1. Objeto de la Ley" in txt0 or "## [a2] Artículo 2. Principios rectores" in txt0:
    print("ABORTA: el diff de formato de los arts. 1/2 YA estaba aplicado. No se escribe nada.")
    sys.exit(0)

# ---------- 1. anclajes ----------
i1 = lines.index("## [a1] Artículo 1")
assert lines[i1 + 1] == "" and lines[i1 + 2] == "Artículo 1. Objeto de la Ley.", "ancla a1 inesperada"
assert lines.count("## [a1] Artículo 1") == 1, "cabecera a1 no unica"

i2 = lines.index("## [a2] Artículo 2")
assert lines[i2 + 1] == "" and lines[i2 + 2] == "Artículo 2. Principios rectores.", "ancla a2 inesperada"
assert lines.count("## [a2] Artículo 2") == 1, "cabecera a2 no unica"

p0 = next(i for i, l in enumerate(lines) if l.startswith("a) Desarrollo sostenible."))
assert i2 < p0 < i2 + 40, "primer principio fuera del bloque a2"
p1 = next(i for i, l in enumerate(lines) if l.startswith("ñ) Cooperación, colaboración"))
principios = [l for l in lines[p0:p1 + 1] if l.strip()]
assert len(principios) == 15, "se esperaban 15 principios, hay %d" % len(principios)

# ---------- 2. textos eliminados / anadidos ----------
elim_a1 = "\n".join(["## [a1] Artículo 1", "", "Artículo 1. Objeto de la Ley."])
anad_a1 = "## [a1] Artículo 1. Objeto de la Ley"
elim_a2_cab = "\n".join(["## [a2] Artículo 2", "", "Artículo 2. Principios rectores."])
anad_a2_cab = "## [a2] Artículo 2. Principios rectores"
elim_a2_ppios = "\n".join(lines[p0:p1 + 1])
anad_a2_ppios = "\n".join(principios)

# ---------- 3. aplicar ----------
sha_bloque_antes = {}
txt_bloque_antes = {}
for et in ("a1", "a2", "a1-7"):
    bt = bloque_texto(lines, et)
    sha_bloque_antes[et] = sha256_texto(bt)
    txt_bloque_antes[et] = bt

# a2: los principios se colapsan primero (indices mayores) para no descolocar a1
nuevas = list(lines)
nuevas[p0:p1 + 1] = principios[:]
del nuevas[i2 + 1:i2 + 3]
nuevas[i2] = anad_a2_cab
del nuevas[i1 + 1:i1 + 3]
nuevas[i1] = anad_a1

txt1 = "\r\n".join(nuevas)

# ---------- 4. verificar el resultado contra el 'Texto propuesto' literal ----------
lines1 = nuevas
i1n, e1n = bloques(lines1)["a1"]
i2n, e2n = bloques(lines1)["a2"]

prop1 = extraer_propuesto(PROP, 2)   # Propuesta 2 -> art. 1
prop2 = extraer_propuesto(PROP, 3)   # Propuesta 3 -> art. 2

# el bloque a2 termina en 'ñ) Cooperación...' (las lineas TITULO I siguientes NO son del art. 2,
# porque TÍTULO I va sin prefijo '## [' y por eso el corte por cabeceras lo incluye)
_fin_a2 = next(i for i, l in enumerate(lines1[i2n:e2n], start=i2n)
               if l.startswith("ñ) Cooperación, colaboración"))
obtenido1 = "\r\n".join(lines1[i1n:e1n]).rstrip()
obtenido2 = "\r\n".join(lines1[i2n:_fin_a2 + 1]).rstrip()

def compara(et, propuesto, obtenido):
    a = propuesto.replace("\n", "\r\n").rstrip()
    b = obtenido
    if a == b:
        print("[OK] bloque %s == Texto propuesto literal de propuestas/2026-09-08.md" % et)
        return True
    print("[FALLO] bloque %s NO coincide con el texto propuesto:" % et)
    for l in difflib.unified_diff(a.split("\r\n"), b.split("\r\n"), "propuesto", "obtenido", lineterm="", n=1):
        print("   ", l)
    return False

ok1 = compara("a1", prop1, obtenido1)
ok2 = compara("a2", prop2, obtenido2)

# los demas bloques no deben cambiar: solo entran/salen lineas de a1/a2
sin_a = lambda L, et: [x for x in L if True]
resto_antes = {k: bloque_texto(lines, k) for k in ("a3", "a1-12")}
resto_desp = {k: bloque_texto(lines1, k) for k in ("a3", "a1-12")}
assert resto_antes == resto_desp, "otros bloques cambiaron"
print("[OK] bloques ajenos (a3, a1-12) intactos")

if not (ok1 and ok2):
    print("ABORTA: verificacion fallida, no se escribe el fichero.")
    sys.exit(1)

# ---------- 5. escribir ----------
with io.open(MD, "w", encoding="utf-8", newline="") as f:
    f.write(txt1)

raw1 = io.open(MD, "rb").read()
assert raw1.decode("utf-8") == txt1
assert raw1.count(b"\r\n") == len(nuevas) - 1, "conteo CRLF inesperado"
sha_despues = sha256_bytes(raw1)
lines_fin = raw1.decode("utf-8").split("\r\n")
print()
print("sha256 DESPUES fichero:", sha_despues)
print("lineas DESPUES        :", len(lines_fin))
print("palabras DESPUES      :", len(raw1.decode("utf-8").split()))

# ---------- 6. informe JSON ----------
informe = {
    "fecha": "2026-09-21",
    "sesion": "13/30",
    "ministerio": "transicion-ecologica",
    "ley": "Ley 7/2021 (BOE-A-2021-8447)",
    "fichero": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
    "script": "scripts/s13_ejecutar_diffs_tecologica.py",
    "fuente_acuerdo": "consejo/actas/2026-09-08.md (filas APROBADO de Sara Aagesen)",
    "fuente_texto_literal": "ministerios/transicion-ecologica/propuestas/2026-09-08.md",
    "sha256_antes": sha_antes,
    "sha256_despues": sha_despues,
    "palabras_antes": palabras_antes,
    "palabras_despues": len(raw1.decode("utf-8").split()),
    "lineas_antes": len(lines),
    "lineas_despues": len(lines_fin),
    "diffs": [
        {
            "etiqueta": "a1",
            "titulo": "Artículo 1. Objeto de la Ley",
            "acuerdo": "Integrar título en bloque de etiquetas",
            "tipo": "formato",
            "lineas_antes": [i1 + 1, i1 + 3],
            "lineas_despues": [i1n + 1, i1n + 1],
            "n_lineas_antes": 3,
            "n_lineas_despues": 1,
            "palabras_antes": len(elim_a1.split()),
            "palabras_despues": len(anad_a1.split()),
            "sha256_bloque_antes": sha_bloque_antes["a1"],
            "sha256_bloque_despues": sha256_texto(bloque_texto(lines_fin, "a1")),
            "texto_eliminado_200": elim_a1[:200],
            "texto_anadido_200": anad_a1[:200],
        },
        {
            "etiqueta": "a2",
            "titulo": "Artículo 2. Principios rectores",
            "acuerdo": "Unificar principios rectores",
            "tipo": "formato",
            "lineas_antes": [i2 + 1, p1 - p0 + 3],
            "lineas_despues": [i2n + 1, i2n + 18],
            "n_lineas_antes": 3 + (p1 - p0 + 1),
            "n_lineas_despues": 18,
            "palabras_antes": len(elim_a2_cab.split()) + len(elim_a2_ppios.split()),
            "palabras_despues": len(anad_a2_cab.split()) + len(anad_a2_ppios.split()),
            "sha256_bloque_antes": sha_bloque_antes["a2"],
            "sha256_bloque_despues": sha256_texto(bloque_texto(lines_fin, "a2")),
            "texto_eliminado_200": elim_a2_cab[:200] + " | " + elim_a2_ppios[:200],
            "texto_anadido_200": anad_a2_cab[:200] + " | " + anad_a2_ppios[:200],
            "detalle": "-2 lineas de titulo de bloque (fusionadas en la cabecera) y -13 lineas en blanco irregulares entre principios (a)-ñ)); texto normativo identico",
        },
    ],
}
with io.open(os.path.join(RAIZ, ".tmp/informe_s13_tecologica.json"), "w", encoding="utf-8") as f:
    json.dump(informe, f, ensure_ascii=False, indent=1)
print("informe provisional ->", ".tmp/informe_s13_tecologica.json")
