# S6 paso3 — dictamen definitivo por k: ¿está ya en el repo (substring), o falta de verdad?
import html, json, re
BASE = "ministerios/transicion-ecologica"
norm = lambda s: re.sub(r"\s+", " ", s).strip()
h = html.unescape(re.sub(r"<[^>]+>", "\n", open(f"{BASE}/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8").read()))
hl = [x for x in (norm(y) for y in h.split("\n")) if x and x != "Subir" and not x.startswith("[Bloque")]
t = json.load(open(f"{BASE}/evidencia/textos_restitucion_532_2026-09-04.json", encoding="utf-8"))
repo_raw = open(f"{BASE}/leyes/BOE-A-2021-8447.md", encoding="utf-8").read()
repo = repo_raw.split("\n")
rn = [norm(x) for x in repo]
repoN = norm(repo_raw)

for k in range(22):
    s = norm(t[str(k)])
    present = s in repoN
    L = [i for i, l in enumerate(hl) if l == s]
    i = L[0] if len(L) == 1 else None
    prev = hl[i-1] if i and hl[i-1] and not re.match(r"^T[IÍ]TULO", hl[i-1]) else None
    nxt = hl[i+1] if i and hl[i+1] and not re.match(r"^T[IÍ]TULO", hl[i+1]) else None
    ph = [j for j, l in enumerate(rn) if prev and norm(prev) == l]
    nh = [j for j, l in enumerate(rn) if nxt and norm(nxt) == l]
    # fallback: vecino como substring de linea repo
    phs = [j for j, l in enumerate(rn) if prev and norm(prev) in l] if not ph else ph
    nhs = [j for j, l in enumerate(rn) if nxt and norm(nxt) in l] if not nh else nh
    flag = "PRESENT" if present else "FALTA"
    print(f"k={k:2d} {flag:7s} boe={len(L)} prev_exact={ph[:2]}/sub={phs[:2]} next_exact={nh[:2]}/sub={nhs[:2]} | {s[:60]}")
    if not present:
        print(f"      PREVTXT: {(prev or '')[:110]}")
        print(f"      NEXTTXT: {(nxt or '')[:110]}")
