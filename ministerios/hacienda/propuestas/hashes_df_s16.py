# Hashes definitivos s16: bloques VIVOS dfquinta/dfsexta/dfoctava (convención Auditor)
# + canon limpio de basura AEBOE + bloque propuesto (cabecera + LF + canon).
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
lg = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8", newline="").read()
crlf = lg.count("\r\n")
lg = lg.replace("\r\n", "\n")
h = open(BASE + r"/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
import html as H
txt = re.sub(r"<(script|style).*?</\1>", " ", h, flags=re.S | re.I)
txt = H.unescape(re.sub(r"<[^>]+>", "\n", txt)).replace("\xa0", " ")
flat = "\n".join(l.strip() for l in txt.split("\n") if l.strip())
flat = "\n".join(l for l in flat.split("\n") if l != "Subir" and not re.match(r"^\[Bloque \d+:\s*#", l))

def deacc(s):
    return s.replace("é","e").replace("á","a").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").lower()

allhits = [(m.start(), deacc(m.group(1))) for m in re.finditer(r"Disposición final (quinta|sexta|octava)\b", flat)]
WS = re.compile(r"\S+")

def auditor(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n","\n").encode("utf-8")).hexdigest()

def canon_de(order, nextmarks):
    hits = [p for p, w in allhits if w == order]
    start = hits[1] if len(hits) > 1 else hits[0]
    ends = [p for p, _ in ((m.start(), m.group(0)) for m in re.finditer(nextmarks, flat)) if p > start]
    c = flat[start:(ends[0] if ends else len(flat))]
    # cortar pies AEBOE: desde cualquier línea que sea pie típico
    for foot in ["Jurisprudencia", "Legislación", "Notas", "Información", "Índice", "Relación de disposiciones",
                 "Agencia Estatal Boletín", "Avda.", "Tutoriales", "Empleo en la AEBOE", "Ver texto", "Compartir"]:
        idx = c.find("\n" + foot + "\n")
        if idx != -1:
            c = c[:idx]
    return c.strip()

def nextmark(order):
    return {"quinta": r"Disposición final sexta", "sexta": r"Disposición final séptima|Disposición final septima",
            "octava": r"Disposición final novena"}[order]

for slug, order in [("dfquinta","quinta"), ("dfsexta","sexta"), ("dfoctava","octava")]:
    lm = re.search(r"(?ms)^## \[" + slug + r"\][^\n]*\n.*?(?=^## \[|\Z)", lg)
    live = lm.group(0).strip("\n")
    c = canon_de(order, nextmark(order))
    prop = "## [" + slug + "] " + c.split(".")[0].replace("Modificación", "Modificación").split("\n")[0]
    # cabecera viva exacta reutilizada + canon
    head = live.split("\n")[0]
    prop = head + "\n\n" + c
    print("###", slug)
    print("  VIVO  pal", len(WS.findall(live)), "hash", auditor(live))
    print("  CANON pal", len(WS.findall(c)), "hash-cuerpo", auditor(c))
    print("  PROP  pal", len(WS.findall(prop)), "hash", auditor(prop))
    print("  canon inicio:", c[:90].replace("\n"," ⏎ "))
    print("  canon final :", c[-90:].replace("\n"," ⏎ "))
    open(BASE + rf"/ministerios/hacienda/evidencia/bloque_vivo_{slug}_2026-09-24.txt","w",encoding="utf-8",newline="\n").write(live)
    open(BASE + rf"/ministerios/hacienda/evidencia/bloque_propuesto_{slug}_2026-09-24.txt","w",encoding="utf-8",newline="\n").write(prop)
print("CRLF en fichero ley:", crlf)
