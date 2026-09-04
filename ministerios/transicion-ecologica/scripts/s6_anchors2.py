# S6 paso2 — para cada k: vecinos BOE exactos + posiciones en repo de esos vecinos
import html, json, re
BASE = "ministerios/transicion-ecologica"
norm = lambda s: re.sub(r"\s+", " ", s).strip()

h = html.unescape(re.sub(r"<[^>]+>", "\n", open(f"{BASE}/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8").read()))
hl = [x for x in (norm(y) for y in h.split("\n")) if x]
# limpio marcadores de navegación BOE
SKIP = {"Subir"}
t = json.load(open(f"{BASE}/evidencia/textos_restitucion_532_2026-09-04.json", encoding="utf-8"))
repo = open(f"{BASE}/leyes/BOE-A-2021-8447.md", encoding="utf-8").read().split("\n")
rn = [norm(x) for x in repo]

def loc(s):
    return [i for i, l in enumerate(hl) if l == s]

def rep(s):
    return [i for i, l in enumerate(rn) if l == s]

for k in range(22):
    s = norm(t[str(k)])
    L = loc(s)
    print(f"--- k={k} len={len(s.split())}w boe_hits={len(L)} repo_exact={len(rep(s))}")
    if len(L) != 1:
        print("   !! boe ambiguo", L[:4]); continue
    i = L[0]
    # vecinos no vacios y no 'Subir'
    prv = None
    j = i - 1
    while j >= 0:
        if hl[j] not in SKIP and not hl[j].startswith("[Bloque") and not re.match(r"^T[IÍ]TULO", hl[j]):
            prv = hl[j]; break
        j -= 1
    nxt = None
    j = i + 1
    while j < len(hl):
        if hl[j] not in SKIP and not hl[j].startswith("[Bloque") and not re.match(r"^T[IÍ]TULO", hl[j]):
            nxt = hl[j]; break
        j += 1
    pr = rep(prv) if prv else []
    nr = rep(nxt) if nxt else []
    print(f"   PREV[{len(pr)}] {pr[:3]} :: {(prv or '')[:95]}")
    print(f"   NEXT[{len(nr)}] {nr[:3]} :: {(nxt or '')[:95]}")
