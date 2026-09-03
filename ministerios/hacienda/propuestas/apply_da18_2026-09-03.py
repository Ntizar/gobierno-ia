# Reparar el DA18: revertir el intento fallido del 09-02 (regex truncaba el cuerpo)
# y aplicar el diff verificado con extraccion correcta (la del check_hoy, hashes OK).
import re, hashlib, shutil, io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = "leyes/BOE-A-2003-23186.md"
BAK = SRC + ".bak-2026-09-02-da18"          # copia intoca pre-diff (sha 598fbf2b...)
SHA_FILE_ANTES = "598fbf2b61e06ed2feaff48172b4b007429cfb02d054f3813912f14b454deb38"
SHA_BLOCK_ACTUAL = "574ad589ebb449387923d02ebdc7f42d6c7a2d621c896af8cf6b9290da6f6bdc"
SHA_BLOCK_PROPUESTO = "11c84ad13a5dc5f9b452456bc5fff1bca87e155ba8164ae18e414a03d6fab889"

def norm(p): return re.sub(r"\s+", " ", p).strip()
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

report = {}

# 0) evidencia del estado corrupto interino (intento 09-02 sin revertir)
txt_bad = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
mb = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt_bad, flags=re.S | re.M)
report["estado_interino_corrupto"] = {"palabras": len(norm(mb.group(2)).split()) if mb else -1,
                                      "sha_fichero": sha_file(SRC)}

# 1) revertir desde el .bak verificado
shutil.copy(BAK, SRC)
assert sha_file(SRC) == SHA_FILE_ANTES, "el .bak no coincide con el sha antes del diff"
txt = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt, flags=re.S | re.M)
assert m, "bloque no encontrado"
assert hashlib.sha256(norm(m.group(2)).encode()).hexdigest() == SHA_BLOCK_ACTUAL, "precondicion de bloque fallida"
report["revertido_ok"] = True
report["sha_fichero_antes"] = SHA_FILE_ANTES
report["palabras_antes"] = sum(len(norm(p).split()) for p in m.group(2).split("\n\n") if norm(p))

# 2) extraer cuerpo propuesto EXACTO (todo lo que sigue al encabezado hasta EOF)
prop = open("evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md", encoding="utf-8").read().replace("\r\n", "\n")
lines = prop.split("\n")
hidx = next(i for i, l in enumerate(lines) if l.startswith("## [dadecimoctava]"))
body = "\n".join(lines[hidx + 1:])
assert hashlib.sha256(norm(body).encode()).hexdigest() == SHA_BLOCK_PROPUESTO, "cuerpo propuesto no coincide con el hash verificado"

# 3) aplicar
shutil.copy(SRC, SRC + ".bak-2026-09-03-pre-da18")
out = txt[:m.start()] + m.group(1) + body + txt[m.end():]
open(SRC, "w", encoding="utf-8", newline="\n").write(out)

# 4) verificar post
txt2 = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
m2 = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt2, flags=re.S | re.M)
post_block = hashlib.sha256(norm(m2.group(2)).encode()).hexdigest()
report["sha_bloque_despues"] = post_block
report["sha_bloque_esperado"] = SHA_BLOCK_PROPUESTO
report["bloque_ok"] = post_block == SHA_BLOCK_PROPUESTO
report["sha_fichero_despues"] = sha_file(SRC)
report["palabras_despues"] = sum(len(norm(p).split()) for p in m2.group(2).split("\n\n") if norm(p))
report["delta_palabras"] = report["palabras_antes"] - report["palabras_despues"]
report["bloques_totales"] = len(re.findall(r"^## \[\w+\]", txt2, flags=re.M))
# intacto fuera del bloque: el resto del fichero no cambia
head_same = txt[:m.start()] == txt2[:m2.start()]
tail_same = txt[m.end():] == txt2[m2.end():]
report["resto_fichero_intacto"] = head_same and tail_same

print(json.dumps(report, indent=1, ensure_ascii=False))
