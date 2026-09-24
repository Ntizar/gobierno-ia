# Canon BOE s16: extraer del boe_consolidado archivado el texto COMPLETO de las
# DF 1ª-6ª de la LGT (truncadas en el repo) y volcarlo a evidencia con sha256.
import re, sys, io, html, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
h = open(BASE + r"/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()

txt = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S | re.I)
txt = re.sub(r"<[^>]+>", "\n", txt)
txt = html.unescape(txt).replace("\xa0", " ")
lines = [l.strip() for l in txt.split("\n") if l.strip()]
flat = "\n".join(lines)

WS = re.compile(r"\S+")
ordenes = ["primera", "segunda", "tercera", "cuarta", "quinta", "sexta"]

# todas las cabeceras "Disposición final X" del plano (índice + cuerpo)
allhits = [(m.start(), m.group(1).lower()) for m in re.finditer(r"Disposición final (\w+)\b", flat)]
print("hits totales 'Disposición final ...':", len(allhits))

out = []
for i, o in enumerate(ordenes):
    hits = [p for p, word in allhits if word == o]
    if not hits:
        print("SIN HIT:", o)
        continue
    start = hits[1] if len(hits) > 1 else hits[0]
    after = [p for p, _ in allhits if p > start]
    end = after[0] if after else len(flat)
    c = flat[start:end].strip()
    out.append((o, c))
    print("=" * 70)
    nw = len(WS.findall(c))
    print("[DF " + o + "] " + str(len(c)) + " chars, " + str(nw) + " palabras")
    print(c[:400])

with open(BASE + r"/ministerios/hacienda/evidencia/boe_canonico_df_2026-09-24.txt", "w", encoding="utf-8", newline="\n") as f:
    for o, c in out:
        f.write("#### BOE consolidado — Disposición final " + o + " (Ley 58/2003, BOE-A-2003-23186)\n" + c + "\n\n")
    f.write("#### Fuente: ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html (archivado 2026-09-02), volcado 2026-09-24.\n")
b = open(BASE + r"/ministerios/hacienda/evidencia/boe_canonico_df_2026-09-24.txt", "rb").read()
print("canon guardado, sha256:", hashlib.sha256(b).hexdigest())
