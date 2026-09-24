# Comprobaciones previas s16:
# 1) ¿el cuerpo del canon de DF 5ª/6ª aparece en OTRO bloque del vivo? (evitar restaurar donde ya está)
# 2) final limpio del canon (no cortado a media frase)
# 3) hashes convención Auditor del bloque vivo y del bloque propuesto (3 DF candidatas)
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
raw = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
canon_raw = open(BASE + r"/ministerios/hacienda/evidencia/boe_canonico_df_2026-09-24.txt", encoding="utf-8").read()

canon = {}
for m in re.finditer(r"#### BOE consolidado — Disposición final (\w+) \(Ley 58/2003[^)]*\)\n(.*?)(?=\n\n####|\Z)", canon_raw, re.S):
    canon[m.group(1)] = m.group(2).strip()

def auditor_hash(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n", "\n").encode("utf-8")).hexdigest()

# 1) ocurrencias del canon fuera del propio bloque df
for o in ["quinta", "sexta", "cuarta"]:
    body = canon[o]
    # frases ancla (saltamos la cabecera "Disposición final X...")
    anchors = [ln for ln in body.split("\n") if len(ln) > 60][1:4]
    print("== " + o + ": anclas fuera de su bloque ==")
    for a in anchors:
        cnt = raw.count(a)
        print("   " + str(cnt) + "x | " + a[:70])

# 2) finales
for o in canon:
    print("FINAL " + o + ": ..." + canon[o][-90:].replace("\n", " ⏎ "))

# 3) hashes
for o, slug in [("cuarta", "dfcuarta"), ("quinta", "dfquinta"), ("sexta", "dfsexta")]:
    m = re.search(r"(?ms)^## \[" + slug + r"\].*?(?=^## \[|\Z)", raw)
    live = m.group(0).rstrip("\n")
    prop = "## [" + slug + "] Disposición final " + o + "\n\n" + canon[o]
    # cabecera vivo
    print("== " + slug + " ==")
    print("ACTUAL  pal " + str(len(re.findall(r'\S+', live))) + " hash " + auditor_hash(live))
    print("PROP    pal " + str(len(re.findall(r'\S+', prop))) + " hash " + auditor_hash(prop))
    # volcar texto propuesto a evidencia para el manifiesto
    with open(BASE + r"/ministerios/hacienda/evidencia/bloque_propuesto_" + slug + "_2026-09-24.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(prop.strip("\n"))
