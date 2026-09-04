# Sesion 6 — sonda de ancorajes: localiza las 22 lineas del JSON 532 en el BOE
# archivado y devuelve contexto (lineas previas/siguientes) para anclar en el repo.
import html, json, re

BASE = "ministerios/transicion-ecologica"
BOE = f"{BASE}/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html"
TXT = f"{BASE}/evidencia/textos_restitucion_532_2026-09-04.json"

norm = lambda s: re.sub(r"\s+", " ", s).strip()
h = html.unescape(re.sub(r"<[^>]+>", "\n", open(BOE, encoding="utf-8").read()))
hl = [norm(x) for x in h.split("\n")]
hl = [x for x in hl if x]
hidx = {}
for i, l in enumerate(hl):
    hidx.setdefault(l, []).append(i)

t = json.load(open(TXT, encoding="utf-8"))
repo = open(f"{BASE}/leyes/BOE-A-2021-8447.md", encoding="utf-8").read().split("\n")
repo_set = {norm(x) for x in repo if x.strip()}

out = []
for k in range(22):
    s = norm(t[str(k)])
    locs = hidx.get(s, [])
    if not locs:
        # substring search
        locs = [i for i, l in enumerate(hl) if s in l]
    entry = {"k": k, "n_locs": len(locs), "hits": []}
    for i in locs[:3]:
        prev = [l[:90] for l in hl[max(0, i - 3):i]]
        nxt = [l[:90] for l in hl[i + 1:i + 4]]
        entry["hits"].append({"boe_idx": i, "prev": prev, "next": nxt,
                              "line_len": len(hl[i])})
    out.append(entry)

print(json.dumps(out, ensure_ascii=False, indent=1))
# ademas: donde caen los TITULO y que articulo les sigue
print("=== TITULOS EN BOE ===")
for i, l in enumerate(hl):
    if re.match(r"^T[IÍ]TULO\b", l):
        print(i, "|", l[:70], "|->", " / ".join(x[:40] for x in hl[i+1:i+4]))
print("=== TITULO en repo? ===")
print(sum(1 for r in repo if "TÍTULO" in r or "TITULO" in r))
