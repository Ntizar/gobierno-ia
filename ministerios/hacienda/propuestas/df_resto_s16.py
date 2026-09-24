# Volcado vivo DF septima/octava/undecima + canon y hashes propuestos (s16).
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
lg = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
h = open(BASE + r"/ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
import html as H
txt = re.sub(r"<(script|style).*?</\1>", " ", h, flags=re.S | re.I)
txt = H.unescape(re.sub(r"<[^>]+>", "\n", txt)).replace("\xa0", " ")
flat = "\n".join(l.strip() for l in txt.split("\n") if l.strip())
flat = "\n".join(l for l in flat.split("\n") if l not in ("Subir",) and not re.match(r"^\[Bloque \d+:\s*#", l))

allhits = [(m.start(), m.group(1).lower()) for m in re.finditer(r"Disposición final (\w+)\b", flat)]
WS = re.compile(r"\S+")

def auditor_hash(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n", "\n").encode("utf-8")).hexdigest()

def canon_de(o):
    hits = [p for p, w in allhits if w == o]
    if not hits:
        return None
    start = hits[1] if len(hits) > 1 else hits[0]
    after = [p for p, _ in allhits if p > start]
    return flat[start:(after[0] if after else len(flat))].strip()

for o, slug in [("septima", "dfseptima"), ("séptima", "dfseptima"), ("octava", "dfoctava"),
                ("undecima", "dfundecima"), ("undécima", "dfundecima")]:
    c = canon_de(o)
    if not c:
        continue
    m = re.search(r"(?ms)^## \[" + slug + r"\][^\n]*\n(.*?)(?=^## \[|\Z)", lg)
    live_head = re.search(r"(?m)^## \[" + slug + r"\].*$", lg)
    print("=" * 72)
    print("== " + slug + " | orden " + o)
    print(live_head.group(0))
    if m:
        live = m.group(0).rstrip("\n")
        print("   VIVO pal", len(WS.findall(live)), "hash", auditor_hash(live))
    print("   CANON pal", len(WS.findall(c)))
    print("   CANON inicia:", c[:150].replace("\n", " ⏎ "))
    print("   CANON final:", c[-120:].replace("\n", " ⏎ "))
    prop = (live_head.group(0) + "\n\n" + c).strip("\n") if m else None
    if prop:
        print("   PROP pal", len(WS.findall(prop)), "hash", auditor_hash(prop))
        open(BASE + r"/ministerios/hacienda/evidencia/bloque_propuesto_" + slug + "_2026-09-24.txt", "w", encoding="utf-8", newline="\n").write(auditor_hash_text := prop)
