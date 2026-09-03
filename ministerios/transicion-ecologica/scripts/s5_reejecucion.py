# Sesion 5 — TEST DE REEJECUCION (metodo del Consejo: lo medido, no lo contado)
# 1) ocurrencias del rotulo 'Articulo 15.' en el fichero (antes: 3 -> despues: 1)
# 2) 'embates marinos' y 'desagregados por sexo' presentes (DF 4a)
# 3) letra h) DF 5a y parrafo Enresa DF 9a presentes
# 4) recuento de listas que arrancan en 'b)' sin su 'a)' (antes: 22 -> objetivo: 0)
# 5) contraste con el BOE archivado: el texto restituido coincide caracter a caracter (linea normalizada)
# 6) denominador de bloques '## [' de la L7 (acuerdo 10: declarar en sesion 5)
import hashlib, html, json, re

LEY = "leyes/BOE-A-2021-8447.md"
BOE = "evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html"

raw = open(LEY, "rb").read()
print("SHA256_FICHERO:", hashlib.sha256(raw).hexdigest())
t = raw.decode("utf-8")
lines = [l for l in t.split("\n")]
print("ROTULO_art15_x", len(re.findall(r"^Artículo 15\.", t, re.M)))
print("ROTULO_a1-7_x", len(re.findall(r"^## \[a1-7\]", t, re.M)))
for probe in ("embates marinos", "desagregados por sexo", "interfaz urbano-forestal",
              "Impacto por razón de cambio climático", "Empresas Nacional de Residuos Radiactivos",
              "Empresa Nacional de Residuos Radiactivos"):
    print(f"PROBE {probe!r}: {t.count(probe)}")

# listas que arrancan en b) sin a)
faltan = []
for i, l in enumerate(lines):
    if l.strip().startswith("b) "):
        prev = "\n".join(lines[max(0, i - 5):i])
        if not re.search(r"^a\) ", prev, re.M):
            faltan.append(i + 1)
print("LISTAS_SIN_A:", len(faltan), faltan)

# contraste contra el BOE archivado (normalizacion: colapsar espacios)
h = html.unescape(re.sub(r"<[^>]+>", "\n", open(BOE, encoding="utf-8").read()))
hl = [re.sub(r"\s+", " ", x).strip() for x in h.split("\n")]
hl = [x for x in hl if x]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
vf = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
ok = bad = 0
for r in [x for x in vf if x.get("repo")]:
    a = norm(r["texto_a"])
    if a in [norm(l) for l in lines]:
        ok += 1
    else:
        bad += 1
        print("  AUSENTE_POR_TEXTO:", r["repo"][:28], a[:60])
print(f"LETRAS_A_CONTRA_FICHERO: {ok} ok / {bad} ausentes (de 22)")

# DF 4a/5a/9a contra BOE: exactas
om = json.load(open("evidencia/omisiones_repositorio_2026-09-01.json", encoding="utf-8"))["omisiones"]
sel = [r for r in om if r["bloque"].startswith(("artículo 20.1", "artículo 26.3", "artículo 38 bis"))]
boe_set = set(hl)
exact = sum(1 for r in sel if norm(r["linea"]) in boe_set)
print(f"DF_BOE_EXACTAS: {exact}/9")

# denominador de bloques
heads = [l for l in lines if l.startswith("## [")]
print("DENOMINADOR_BLOQUES_L7:", len(heads))
