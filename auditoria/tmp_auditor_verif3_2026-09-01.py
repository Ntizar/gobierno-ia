# 3ª pasada - Auditor 2026-09-01: comprobaciones puntuales
import re, json, os, subprocess, collections

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"
def norm(p):
    p = p.replace("**", "").replace("&nbsp;", " ").replace("\u00a0", " ").replace("\ufeff", "")
    return re.sub(r"\s+", " ", p).strip().lower()
def wc(t): return len(t.split())
def read(p):
    with open(p, encoding="utf-8") as f: return f.read()
def sh(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout

out = {}

# A. La restitucion en HEAD del commit 8493826 (12:20) vs original a547104
for sha in ("a547104", "8493826"):
    t = sh("git", "show", f"{sha}:ministerios/hacienda/leyes/BOE-A-2003-23186.md")
    out[f"LGT_{sha[:7]}_has_a150_letter_a"] = bool(re.search(r"a\) 18 meses, con carácter general", t))
    out[f"LGT_{sha[:7]}_has_a271_letter_a"] = bool(re.search(r"a\) Acuerdo de modificación", t))
    out[f"LGT_{sha[:7]}_total_words"] = wc(t)
t_bak = read(os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md.bak-2026-09-01"))
out["LGT_backup_has_a150_letter_a"] = bool(re.search(r"a\) 18 meses, con carácter general", t_bak))
out["LGT_backup_has_a271_letter_a"] = bool(re.search(r"a\) Acuerdo de modificación", t_bak))

# B. Manifiesto: palabras_eliminadas por bloque
man = json.loads(read(os.path.join(REPO, r"ministerios/hacienda/evidencia/manifiesto_aplicacion_2026-09-01.json")))
out["manifest_per_block"] = {k: man["eliminaciones"][k].get("palabras_eliminadas") for k in man["eliminaciones"]}
out["manifest_total"] = sum(v.get("palabras_eliminadas", 0) for v in man["eliminaciones"].values())

# C. Estado ACTUAL: los 8 bloques DA y [a150] a 0 duplicados? (test de reejecucion del ministro)
cur = os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md")
lines = read(cur).splitlines()
idx = [i for i, l in enumerate(lines) if l.startswith("## [")] + [len(lines)]
watch = {"daquinta","dasexta","daundecima","dadecimoctava","davigesima","davigesimosegunda","da","da-2","a150","a271"}
det = {}
for a, b in zip(idx, idx[1:]):
    m = re.match(r"## \[([^\]]+)\]", lines[a])
    key = m.group(1)
    if key in watch:
        body = "\n".join(lines[a+1:b])
        paras = [norm(p) for p in body.split("\n\n") if norm(p)]
        c = collections.Counter(paras)
        det[key] = {"dup_paras": sum(n-1 for n in c.values() if n>1),
                    "dup_words": sum(wc(p)*(c[p]-1) for p in c if c[p]>1),
                    "n_paras": len(paras)}
out["current_DA150_271_dupcheck"] = det

# D. Fidelidad LGT total: clasificaciones
f = json.loads(read(os.path.join(REPO, r"ministerios/hacienda/evidencia/fidelidad_LGT_total_2026-09-01.json")))
entries = f if isinstance(f, list) else f.get("casos", f.get("entries", []))
cnt = collections.Counter(e.get("v") for e in entries)
out["fidelidad_LGT_n"] = len(entries)
out["fidelidad_LGT_by_v"] = dict(cnt)
out["fidelidad_LGT_words_contenido_perdido"] = sum(e.get("palabras", 0) for e in entries if e.get("v") == "contenido_perdido")
out["fidelidad_LGT_blocks_contenido_perdido"] = len(set(e.get("bloque") for e in entries if e.get("v") == "contenido_perdido"))

# E. Sanidad: 21 JSONs verificadas + sellos de actualizacion del HTML plano y nota LO 3/2007
san = json.loads(read(os.path.join(REPO, r"ministerios/sanidad/evidencia/fidelidad_21_huerfanas_2026-09-01.json")))
out["san_n"] = len(san)
out["san_all_verified"] = all(e.get("verificada") for e in san)
plano = read(os.path.join(REPO, r"ministerios/sanidad/evidencia/boe_texto_plano.txt"))
html = read(os.path.join(REPO, r"ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html"))
out["plano_has_LO3_2007_note"] = ("LO 3/2007" in plano) or ("Orgánica 3/2007" in plano) or ("orgánica 3/2007" in plano.lower())
out["plano_has_Ley26_2011_note"] = ("26/2011" in plano)
out["plano_has_Ley3_2014_note"] = ("3/2014" in plano)
out["plano_has_infracciones_leves_3005"] = ("3.005,06" in plano)
out["plano_has_colab_voluntaria"] = ("colaboración voluntaria" in plano)
out["html_actualizacion_stamp"] = re.findall(r"Última actualización[^<\n]{0,60}", html)[:3]
out["html_real_ultimo_dato"] = re.findall(r"Real Decreto[^<\n]{0,40}20\d\d[^<\n]{0,10}", html)[:3]
lgs_repo = read(os.path.join(REPO, r"ministerios/sanidad/leyes/BOE-A-1986-10499.md"))
out["lgs_repo_has_3005_06_line"] = ("3.005,06" in lgs_repo)
out["lgs_repo_has_a_infracciones_leves"] = bool(re.search(r"a\) Infracciones leves", lgs_repo))
out["lgs_repo_has_preferencia"] = ("Preferencia de la colaboración" in lgs_repo)

# F. Ecologia: palabras v1/v2 art 15 por lineas (claim 1.152 + 1.380 + 16 rotulos)
l7 = read(os.path.join(REPO, r"ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md")).splitlines()
out["L7_v1_387_413_words"] = wc("\n".join(l7[386:413]))
out["L7_v2_414_443_words"] = wc("\n".join(l7[413:443]))
out["L7_v3_445_473_words"] = wc("\n".join(l7[444:473]))
out["L7_lines_379_386"] = [(i+1, l7[i]) for i in range(378, 386)]
# df-4 block ending
i = next(i for i,l in enumerate(l7) if l.startswith("## [df-4]"))
j = next(i2 for i2 in range(i+1,len(l7)) if l7[i2].startswith("## ["))
out["L7_df4_last_content_line"] = [l for l in l7[i:j] if l.strip()][-1][:120]
out["L7_df4_words"] = wc("\n".join(l7[i:j]))
# evidencia sha vs README
rd = read(os.path.join(REPO, r"ministerios/transicion-ecologica/evidencia/README.md"))
out["L7_readme_sha_lines"] = re.findall(r"[0-9a-f]{64}", rd)[:3]
import hashlib
ev = os.path.join(REPO, r"ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html")
out["L7_evidence_sha_actual"] = hashlib.sha256(open(ev,'rb').read()).hexdigest()
# omisiones 55 lineas JSON
om = json.loads(read(os.path.join(REPO, r"ministerios/transicion-ecologica/evidencia/omisiones_repositorio_2026-09-01.json")))
out["L7_omisiones_type"] = type(om).__name__
if isinstance(om, dict):
    out["L7_omisiones_keys"] = list(om)[:10]
elif isinstance(om, list):
    out["L7_omisiones_n"] = len(om); out["L7_omisiones_sample"] = om[0]

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
