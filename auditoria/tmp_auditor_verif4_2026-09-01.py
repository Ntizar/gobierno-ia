# 4a pasada - detalles: DA18 residual, 21 lineas sanidad, omisiones L7, clima cafe
import re, json, os, collections
REPO = r"C:/Users/d_ant/Projects/gobierno-ia"
def norm(p):
    p = p.replace("**","").replace("&nbsp;"," ").replace("\u00a0"," ").replace("\ufeff","")
    return re.sub(r"\s+"," ",p).strip().lower()
def wc(t): return len(t.split())
def read(p):
    with open(p, encoding="utf-8") as f: return f.read()
out = {}

# 1. DA18: parrafos duplicados restantes en el fichero ACTUAL
cur = read(os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md")).splitlines()
idx = [i for i,l in enumerate(cur) if l.startswith("## [")]; idx.append(len(cur))
for a,b in zip(idx, idx[1:]):
    if cur[a].startswith("## [dadecimoctava]"):
        body = cur[a+1:b]
        paras = [norm(p) for p in "\n".join(body).split("\n\n") if norm(p)]
        c = collections.Counter(paras)
        out["DA18_residual_dups"] = [{"words": wc(p), "n": c[p], "head": p[:140]} for p in c if c[p]>1]
        # y en el backup, los mismos: cuantos eran
# 2. Tambien: ¿y si esos 4 parrafos son legitimos del BOE (repeticion interna)? mirar el backup
bak = read(os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-01")).splitlines()
idx = [i for i,l in enumerate(bak) if l.startswith("## [")]; idx.append(len(bak))
for a,b in zip(idx, idx[1:]):
    if bak[a].startswith("## [dadecimoctava]"):
        paras = [norm(p) for p in "\n".join(bak[a+1:b]).split("\n\n") if norm(p)]
        c = collections.Counter(paras)
        out["DA18_backup_dupgroups"] = {p[:60]: c[p] for p in c if c[p]>1}

# 3. Sanidad: verificar que la linea declarada de cada huerfana contiene la "b)" citada
san = json.loads(read(os.path.join(REPO, r"ministerios/sanidad/evidencia/fidelidad_21_huerfanas_2026-09-01.json")))
lgs = read(os.path.join(REPO, r"ministerios/sanidad/leyes/BOE-A-1986-10499.md")).splitlines()
ok = 0; bad = []
for e in san:
    ln = lgs[e["linea"]-1] if 0 < e["linea"] <= len(lgs) else ""
    if norm(ln).startswith("b)") and norm(e["b"])[:40] in norm(ln):
        ok += 1
    else:
        bad.append({"linea": e["linea"], "repo": ln[:80]})
out["san_line_check_ok"] = ok
out["san_line_check_bad"] = bad

# 4. Omisiones L7: conteo
om = json.loads(read(os.path.join(REPO, r"ministerios/transicion-ecologica/evidencia/omisiones_repositorio_2026-09-01.json")))
out["L7_omisiones_n"] = len(om["omisiones"]) if isinstance(om.get("omisiones"), list) else om.get("omisiones")
out["L7_parciales_n"] = len(om["parciales"]) if isinstance(om.get("parciales"), list) else om.get("parciales")
out["L7_omisiones_sample"] = json.dumps((om["omisiones"][0] if isinstance(om.get("omisiones"), list) else om["omisiones"]), ensure_ascii=False)[:300]

# 5. verificacion 297 palabras DF4/5/9: lineas ausentes JSON
la = json.loads(read(os.path.join(REPO, r"ministerios/transicion-ecologica/evidencia/lineas_ausentes_BOE_vs_repo_2026-09-01.json")))
if isinstance(la, list):
    out["L7_lineas_ausentes_n"] = len(la)
    tot = sum(wc(x.get("texto","" if isinstance(x,dict) else "")) if isinstance(x,dict) else 0 for x in la)
    out["L7_lineas_ausentes_words_sample_keys"] = list(la[0].keys()) if la and isinstance(la[0],dict) else None
    out["L7_lineas_ausentes_total_words"] = tot
else:
    out["L7_lineas_ausentes_keys"] = list(la)[:10]

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
