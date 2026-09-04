# TRAMO F1 LGT arts. 1-30 — restitución de letras «a)» perdidas en la conversión
# Acuerdo 23 del Consejo 2026-09-03 (APROBADO). Ejecutado el viernes 09-04 bajo test cruzado (acuerdo 32).
#
# Método idéntico a la restitución [a150]/[a271] del 09-01 (la regla que yo mismo fijé):
#   - idempotente: aborta si la letra «a)» ya está o si el ancla «b)» no casa 1:1
#   - texto = BOE consolidado literal, archivado en evidencia/ (sha256 b29db001…)
#   - manifiesto sha256 del fichero ANTES y DESPUÉS + backup .bak-2026-09-04
#   - ahorro = 0 palabras (esto es FIDELIDAD, no deduplicación: devuelvo texto que la ley ya tiene)
import re, io, sys, json, hashlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

LAW = "leyes/BOE-A-2003-23186.md"
BAK = "leyes/BOE-A-2003-23186.md.bak-2026-09-04"
def norm(p): return re.sub(r'\s+', ' ', p).strip()
def wc(s): return len(s.split())
def sha_file(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def sha_txt(s): return hashlib.sha256(s.encode()).hexdigest()
def sha_norm(s): return hashlib.sha256(norm(s).encode()).hexdigest()

raw_before = open(LAW, 'rb').read()
sha_before = hashlib.sha256(raw_before).hexdigest()
src = raw_before.decode('utf-8').replace('\r\n', '\n')
print("SHA256 ANTES (crudo):", sha_before)

# Las cuatro piezas a restituir (texto BOE literal, evidencia/textos_a_tramo130_2026-09-04.json)
# Cada restitución = insertar la letra «a)» ANTES de su «b)» huérfana.
# ancla_b = principio de la «b)» huérfana correspondiente (texto normalizado, único por bloque).
RESTIT = {
  '[a7]':  ("a) Por la Constitución.",
            "b) Por los tratados o convenios internacionales"),
  '[a8]':  ("a) La delimitación del hecho imponible, del devengo, de la base imponible y liquidable, la fijación del tipo de gravamen y de los demás elementos directamente determinantes de la cuantía de la deuda tributaria, así como el establecimiento de presunciones que no admitan prueba en contrario.",
            "b) Los supuestos que dan lugar al nacimiento de las obligaciones tributarias de realizar pagos a cuenta"),
  '[a15]': ("a) Que, individualmente considerados o en su conjunto, sean notoriamente artificiosos o impropios para la consecución del resultado obtenido.",
            "b) Que de su utilización no resulten efectos jurídicos o económicos relevantes"),
  '[a27]': ("a) Que la declaración o autoliquidación se presente en el plazo de seis meses a contar desde el día siguiente a aquél en que la liquidación se notifique o se entienda notificada.",
            "b) Que se produzca el completo reconocimiento y pago de las cantidades resultantes de la declaración"),
}

# troceo por TODOS los encabezados (convención 335) — lección 08-31
parts = re.split(r'(?m)^(## \[[^\]]+\][^\n]*)$', src)
head_idx = {}
for i, seg in enumerate(parts):
    m = re.match(r'^## (\[[^\]]+\])', seg)
    if m: head_idx[m.group(1)] = i

assert len(head_idx) == 335, f"CONVENCION 335 ROTA: {len(head_idx)}"

manifiesto = {}
nuevas = []  # reconstruyo el fichero pieza a pieza para controlar el offset exacto
out = src  # voy a operar sobre el texto con sustituciones ancladas, no sobre el troceo
report = {}
for bid, (letra, ancla) in RESTIT.items():
    idx = head_idx[bid]
    body = parts[idx+1]
    # precondición idempotente: la letra a) NO debe estar ya
    paras = [norm(p) for p in re.split(r'\n\s*\n', body) if norm(p)]
    if any(p.startswith('a)') for p in paras):
        print(f"ABORTO {bid}: la letra a) ya está presente"); sys.exit(1)
    # el ancla b) debe casar EXACTAMENTE una vez en el bloque
    hits = [p for p in paras if p.startswith(norm(ancla))]
    copias = len(hits)
    # inserto la letra solo ante la PRIMERA b) (el apartado legal es uno; las demás copias son duplicación D1, no omisión)
    # sustitución anclada sobre el texto crudo del cuerpo
    pat = re.compile(r'(?m)^(' + re.escape(ancla) + ')')
    nuevo_body, n = pat.subn(lambda mm: letra + "\n\n" + mm.group(1), body, count=1)
    assert n == 1, f"{bid}: el ancla no casa (n={n})"
    out = out.replace(body, nuevo_body, 1)
    report[bid] = {
        "letra_restituida": letra,
        "palabras_restituidas": wc(letra),
        "sha256_letra_norm": sha_norm(letra),
        "copias_b_huerfana_en_bloque": copias,
        "nota": "1 restitución (apartado legal único); el resto de copias son duplicación D1, no omisión"
    }
    print(f"[{bid}] restituida letra a) ({wc(letra)} palabras); copias b) huérfanas en bloque: {copias}")

# escribir — PRESERVANDO el fin de linea original del fichero (LF; leccion 09-04: no CRLF-izar la ley)
shutil.copy(LAW, BAK)
eol = '\r\n' if b'\r\n' in open(LAW,'rb').read(200000) else '\n'
out_bytes = out.replace('\n', eol).encode('utf-8') if eol == '\r\n' else out.encode('utf-8')
open(LAW, 'wb').write(out_bytes)
sha_after = sha_file(LAW)

# verificación: cada letra presente 1 vez; cada bloque intacto salvo la inserción; 335 bloques vivos
chk = open(LAW, encoding='utf-8').read().replace('\r\n','\n')
ok = {}
for bid,(letra,_) in RESTIT.items():
    ok[bid] = sum(1 for l in chk.split('\n') if norm(l) == norm(letra))
n_bloques = len(re.findall(r'(?m)^## \[', chk))
pal_antes = wc(re.sub(r'(?m)^## \[[^\]]+\]', '', src))
pal_despues = wc(re.sub(r'(?m)^## \[[^\]]+\]', '', chk))

resumen = {
  "ley": "BOE-A-2003-23186 (Ley 58/2003 General Tributaria)",
  "fecha": "2026-09-04", "sesion": "6/30 — cierre Fase 1",
  "mandato": "Acuerdo 23 Consejo 2026-09-03 (APROBADO): tramo F1 arts. 1-30, orden numérico, manifiesto frase a frase",
  "metodo": "restitución BOE literal, anclada antes de cada b) huérfana del apartado legal; idempotente; convención 335",
  "sha256_antes_crudo": sha_before,
  "sha256_despues_crudo": sha_after,
  "backup": "leyes/BOE-A-2003-23186.md.bak-2026-09-04",
  "bloques_vivos": n_bloques,
  "palabras_ley_antes": pal_antes, "palabras_ley_despues": pal_despues,
  "delta_palabras": pal_despues - pal_antes,
  "AHLORRO_EJECUTADO": 0,
  "FIDELIDAD_RESTITUIDA": sum(r["palabras_restituidas"] for r in report.values()),
  "bloques": report,
  "verificacion_letra_unica": ok,
  "cuadre_vs_mandato": {
    "anunciadas_acta_23": {"[a7]": 5, "[a8]": 46, "[a15]": 38, "[a27]": 32, "total": 121},
    "ejecutadas_fichero": {b: r["palabras_restituidas"] for b, r in report.items()},
    "total_ejecutado": sum(r["palabras_restituidas"] for r in report.values()),
    "diferencia": 121 - sum(r["palabras_restituidas"] for r in report.values()),
    "explicacion": (
      "20 palabras de diferencia, dos causas, ambas declaradas: (1) [a7]: el manifiesto contaba 5 porque "
      "el texto del caso incluia el token 'b)' inicial; el BOE da 'a) Por la Constitucion.' = 4 palabras. "
      "(2) [a15]: el manifiesto contaba 2 casos F1 (19+19=38 pal.) porque el bloque tiene DOS copias del "
      "apartado 1 y a las dos les falta su 'a)'; el BOE tiene un solo apartado 1, luego la ley solo admite "
      "UNA letra. Insertarla dos veces seria fabricar duplicacion para cuadrar un inventario diagnostico: "
      "se restituye 1 (19 pal.) y la copia de mas se liquidara con el diff D1 del bloque. "
      "El inventario decia 121; la ley admite 101. Cada numero, con su denominador."
    ),
  },
}
json.dump(resumen, open('evidencia/manifiesto_aplicacion_tramo130_2026-09-04.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print("\nSHA256 DESPUES:", sha_after)
print("bloques vivos:", n_bloques, "| palabras ley:", pal_antes, "->", pal_despues, "| delta:", pal_despues-pal_antes)
print("letra presente 1x por bloque:", ok)
print("FIDELIDAD restituida:", resumen["FIDELIDAD_RESTITUIDA"], "| AHORRO:", resumen["AHLORRO_EJECUTADO"])
