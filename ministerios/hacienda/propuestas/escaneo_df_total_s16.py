# Escaneo total DF s16: vivo vs canon BOE archivado (limpio de basura AEBOE),
# hashes convención Auditor (sha256 del bloque completo con cabecera, LF, sin saltos finales).
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
lg = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
h = open(BASE + r"/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
import html as H
txt = re.sub(r"<(script|style).*?</\1>", " ", h, flags=re.S | re.I)
txt = H.unescape(re.sub(r"<[^>]+>", "\n", txt)).replace("\xa0", " ")
flat = "\n".join(l.strip() for l in txt.split("\n") if l.strip())
flat = "\n".join(l for l in flat.split("\n") if l != "Subir" and not re.match(r"^\[Bloque \d+:\s*#", l))

def deacc(s):
    return s.replace("é", "e").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n").lower()

allhits = [(m.start(), deacc(m.group(1))) for m in re.finditer(r"Disposición final (primera|segunda|tercera|cuarta|quinta|sexta|séptima|septima|octava|novena|décima|decima|undécima|undecima|duodécima|duodecima)\b", flat)]
WS = re.compile(r"\S+")
JUNK = {"jurisprudencia", "legislación", "legislacion", "nota", "notas", "información", "informacion",
        "índice", "indice", "relación de disposiciones", "sumario"}

def auditor(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n", "\n").encode("utf-8")).hexdigest()

def canon_de(order):
    hits = [p for p, w in allhits if w == order]
    if not hits:
        return None
    start = hits[1] if len(hits) > 1 else hits[0]
    after = [p for p, _ in allhits if p > start]
    c = flat[start:(after[0] if after else len(flat))].strip()
    lines = c.split("\n")
    while lines and deacc(lines[-1]) in JUNK:
        lines.pop()
    return "\n".join(lines).strip()

slug_order = [("dfprimera","primera"),("dfsegunda","segunda"),("dftercera","tercera"),
              ("dfcuarta","cuarta"),("dfquinta","quinta"),("dfsexta","sexta"),
              ("dfseptima","septima"),("dfoctava","octava"),("dfnovena","novena"),
              ("dfdecima","decima"),("dfundecima","undecima"),("dfduodecima","duodecima")]
evid = []
for slug, order in slug_order:
    lm = re.search(r"(?ms)^## \[" + slug + r"\].*?(?=^## \[|\Z)", lg)
    c = canon_de(order)
    if not lm and not c:
        continue
    live = lm.group(0).rstrip("\n") if lm else "(sin bloque vivo)"
    lp = [l for l in live.split("\n") if l.strip() and not l.startswith("#")]
    cw = len(WS.findall(c)) if c else 0
    lw = len(WS.findall("\n".join(lp)))
    print("=" * 70)
    print(slug, "| vivo", lw, "pal | canon", cw, "pal | gap", cw - lw)
    print("  cabecera vivo:", (live.split("\n")[0])[:90])
    if c:
        print("  canon inicio:", c[:110].replace("\n", " ⏎ "))
        print("  canon FINAL :", c[-110:].replace("\n", " ⏎ "))
    evid.append({"slug": slug, "canon": c})

with open(BASE + r"/ministerios/hacienda/evidencia/df_canon_limpio_s16_2026-09-24.txt", "w", encoding="utf-8", newline="\n") as f:
    for e in evid:
        if e["canon"]:
            f.write("#### CANON " + e["slug"] + " (sha256 cuerpo limpio " + auditor(e["canon"])[:12] + ")\n")
            f.write(e["canon"] + "\n\n##----##\n\n")
print("\nevidencia escrita: df_canon_limpio_s16_2026-09-24.txt")
