# Verificacion forense 2ª pasada - Auditor 2026-09-01
import re, json, os, hashlib, subprocess, collections

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"

def norm(p):
    p = p.replace("**", "").replace("&nbsp;", " ").replace("\u00a0", " ").replace("\ufeff", "")
    return re.sub(r"\s+", " ", p).strip().lower()

def wc(t): return len(t.split())
def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

out = {}

# 1. git status + working tree vs HEAD para la LGT
def sh(*args):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip()
out["git_status"] = sh("git", "status", "--porcelain")[:800]
out["git_diff_LGT_stat"] = sh("git", "diff", "--stat", "--", "ministerios/hacienda/leyes/BOE-A-2003-23186.md")
head_txt = sh("git", "show", "HEAD:ministerios/hacienda/leyes/BOE-A-2003-22186.md") or ""
try:
    head_lgt = subprocess.run(["git", "show", "HEAD:ministerios/hacienda/leyes/BOE-A-2003-23186.md"],
                              cwd=REPO, capture_output=True, text=True).stdout
    out["HEAD_LGT_has_18meses"] = bool(re.search(r"18 meses, con carácter general", head_lgt))
    out["HEAD_LGT_total_words"] = wc(head_lgt)
    out["HEAD_LGT_word_delta_vs_worktree"] = wc(read(os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md"))) - wc(head_lgt)
except Exception as e:
    out["head_err"] = str(e)

# 2. Detalle DA del backup (clave de cabecera = primer token entre corchetes)
bak = os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-01")
lines = read(bak).splitlines()
idx = [i for i, l in enumerate(lines) if l.startswith("## [")] + [len(lines)]
da_claim = {"daquinta":841,"dasexta":1089,"daundecima":303,"dadecimoctava":534,
            "davigesima":349,"davigesimosegunda":1504,"da":853,"da-2":151}
det = {}
for a,b in zip(idx, idx[1:]):
    m = re.match(r"## \[([^\]]+)\]", lines[a])
    key = m.group(1)
    body = "\n".join(lines[a+1:b])
    paras = [norm(p) for p in body.split("\n\n") if norm(p)]
    c = collections.Counter(paras)
    w = sum(wc(p)*(c[p]-1) for p in c if c[p] > 1)
    if key in da_claim:
        det[key] = w
out["DA_backup_audit"] = det
out["DA_audit_total"] = sum(det.values())
out["DA_claim_total"] = sum(da_claim.values())

# 3. Manifiesto aplicacion: total palabras eliminadas declarado
man = json.loads(read(os.path.join(REPO, r"ministerios/hacienda/evidencia/manifiesto_aplicacion_2026-09-01.json")))
els = man.get("eliminaciones", [])
tot_words = 0
per_blk = collections.Counter()
def getw(e):
    if isinstance(e, dict):
        return e.get("palabras", e.get("words", 0)) or 0
    return 0
if isinstance(els, dict):
    out["manifest_structure"] = {k: (len(v) if isinstance(v, list) else type(v).__name__) for k, v in list(els.items())[:12]}
    firstval = next(iter(els.values()), None)
    out["manifest_sample"] = json.dumps(firstval, ensure_ascii=False)[:500] if firstval is not None else None
    for blk, v in els.items():
        items = v if isinstance(v, list) else [v]
        for e in items:
            w = getw(e); tot_words += w; per_blk[blk] += w
else:
    out["manifest_structure"] = "list"
    out["manifest_sample"] = json.dumps(els[0], ensure_ascii=False)[:500] if els else None
    for e in els:
        w = getw(e); tot_words += w
        per_blk[e.get("bloque", "?") if isinstance(e, dict) else "?"] += w
out["manifest_n_entries"] = len(els)
out["manifest_total_words"] = tot_words
out["manifest_per_block_top"] = dict(per_blk.most_common(15))

# 4. Diff de restitucion: conteo de palabras del texto a insertar
d = read(os.path.join(REPO, r"ministerios/hacienda/evidencia/diff_restitucion_a150_2026-09-01.md"))
added = [l[1:].strip() for l in d.splitlines() if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
out["restitution_added_lines"] = len(added)
out["restitution_added_words"] = sum(wc(x) for x in added)

# 5. Fidelidad LGT: JSON del ministerio -> 139/135
f = json.loads(read(os.path.join(REPO, r"ministerios/hacienda/evidencia/fidelidad_LGT_total_2026-09-01.json")))
def count_cat(obj):
    s = json.dumps(obj)
    return s
out["fidelidad_LGT_keys"] = list(f.keys())[:15] if isinstance(f, dict) else f[:2]
# buscar categorias
txt_f = json.dumps(f, ensure_ascii=False)
for k in ["contenido_ausente","solo_marcador","boe_sin_a","fragmentado","135","139","3805","3.805"]:
    out.setdefault("fidelidad_mentions", {})[k] = txt_f.count(k)

# 6. Sanidad: contra-boqueo de las 21 huérfanas contra su propio texto plano del BOE
san_lines = [1593+1]
plano = read(os.path.join(REPO, r"ministerios/sanidad/evidencia/boe_texto_plano.txt"))
jsons = json.loads(read(os.path.join(REPO, r"ministerios/sanidad/evidencia/fidelidad_21_huerfanas_2026-09-01.json")))
out["san_json_type"] = type(jsons).__name__
out["san_json_keys"] = (list(jsons.keys())[:12] if isinstance(jsons, dict) else None)
if isinstance(jsons, list):
    out["san_n"] = len(jsons)
    out["san_sample"] = jsons[0]
elif isinstance(jsons, dict):
    for k in list(jsons)[:3]:
        out.setdefault("san_preview", {})[k] = jsons[k] if not isinstance(jsons[k], list) else jsons[k][:1]

# 7. SHA256SUMS de Hacienda: verificar
sp = os.path.join(REPO, r"ministerios/hacienda/evidencia/SHA256SUMS_2026-09-01.txt")
ok = {}
for l in read(sp).splitlines():
    l = l.strip()
    if not l: continue
    h, fn = l.split(None, 1)
    fn = fn.strip().replace("*", "")
    p = os.path.join(REPO, "ministerios/hacienda/evidencia", fn)
    if os.path.exists(p):
        ok[fn] = (hashlib.sha256(open(p,'rb').read()).hexdigest() == h.lower())
    else:
        ok[fn] = "FILE_NOT_FOUND"
out["SHA256SUMS_check"] = ok

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
