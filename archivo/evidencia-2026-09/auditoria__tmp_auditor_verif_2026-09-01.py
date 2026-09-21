# Verificacion forense independiente del Auditor - 2026-09-01 (sesion 4/30)
# Solo stdlib. Crea auditoria/tmp_auditor_verif_2026-09-01.json
import re, hashlib, json, collections, os, sys

REPO = r"C:/Users/d_ant/Projects/gobierno-ia"

def norm(p):
    p = p.replace("**", "").replace("&nbsp;", " ").replace("\u00a0", " ").replace("\ufeff", "")
    return re.sub(r"\s+", " ", p).strip().lower()

def wc(t):
    return len(t.split())

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def dup_stats(path):
    """sha256 por parrafo normalizado, por bloque ## [x]; devuelve totales y detalle."""
    txt = read(path)
    lines = txt.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("## [")]
    idx.append(len(lines))
    tb, tw = 0, 0
    per = {}
    for a, b in zip(idx, idx[1:]):
        body = "\n".join(lines[a+1:b])
        paras = [norm(p) for p in body.split("\n\n") if norm(p)]
        c = collections.Counter(paras)
        d = sum(n-1 for n in c.values() if n > 1)
        if d:
            tb += 1
            w = sum(wc(p)*(c[p]-1) for p in c if c[p] > 1)
            tw += w
            per[lines[a][:60]] = {"dup_paras": d, "dup_words": w}
    heads = [l for l in lines if l.startswith("## [")]
    num = [h for h in heads if re.match(r"## \[a\d+\]", h)]
    return {"headers_total": len(heads), "headers_numeric": len(num),
            "dup_blocks": tb, "dup_words": tw, "total_words": wc(txt), "per_block": per}

out = {}

# ---------- LGT (Hacienda) ----------
lgt = os.path.join(REPO, r"ministerios/hacienda/leyes/BOE-A-2003-23186.md")
cur = dup_stats(lgt)
out["LGT_current"] = {k: v for k, v in cur.items() if k != "per_block"}
bak = lgt + ".bak-2026-09-01"
if os.path.exists(bak):
    b = dup_stats(bak)
    out["LGT_backup"] = {k: v for k, v in b.items() if k != "per_block"}
    out["LGT_words_removed_by_diffs"] = b["total_words"] - cur["total_words"]
    # DA blocks in backup: dup words per DA vs claimed (841,1089,303,534,349,1504,853,151)
    das = ["[daquinta]", "[dasexta]", "[daundecima]", "[dadecimoctava]", "[davigesima]",
           "[davigesimosegunda]", "[da]", "[da-2]"]
    out["LGT_backup_DA_detail"] = {d: b["per_block"].get(d, "sin dup") for d in das}
txt = read(lgt)
out["LGT_art150_label_count_current"] = len(re.findall(r"(?m)^Art[íi]culo 150\.", txt))
out["LGT_art150_label_count_backup"] = len(re.findall(r"(?m)^Art[íi]culo 150\.", read(bak)))
# check restored letter a) 18 meses in current LGT
out["LGT_a150_has_18meses_general"] = bool(re.search(r"18 meses, con carácter general", txt))
out["LGT_a150_has_18meses_backup"] = bool(re.search(r"18 meses, con carácter general", read(bak)))
# 139 huerfanas: heuristico propio - listas que arrancan en "b)" sin "a) " previa en el bloque
def orphan_b(path):
    t = read(path)
    lines = t.splitlines()
    idx = [i for i, l in enumerate(lines) if l.startswith("## [")]
    idx.append(len(lines))
    n = 0
    blocks = set()
    for a, b2 in zip(idx, idx[1:]):
        body = lines[a+1:b2]
        seen_a = False
        for l in body:
            s = norm(l)
            if re.match(r"^a\)", s): seen_a = True
            if re.match(r"^b\)", s) and not seen_a:
                n += 1; blocks.add(lines[a][:40]); seen_a = False
    return {"orphan_b_lines": n, "blocks_affected": len(blocks)}
out["LGT_orphan_b_heuristic"] = orphan_b(lgt)

# ---------- LGS (Sanidad) ----------
lgs = os.path.join(REPO, r"ministerios/sanidad/leyes/BOE-A-1986-10499.md")
s = dup_stats(lgs)
out["LGS_current"] = {k: v for k, v in s.items() if k != "per_block"}
t = read(lgs)
out["LGS_art18_header_count"] = len(re.findall(r"(?m)^Art[íi]culo dieciocho\.", t))
out["LGS_art35_header_count"] = len(re.findall(r"(?m)^Art[íi]culo treinta y cinco\.", t))
out["LGS_colab_voluntaria_present"] = ("colaboración voluntaria" in t)
out["LGS_registro_estatal_count"] = t.count("Registro Estatal de Profesionales Sanitarios")
out["LGS_orphan_b_heuristic"] = orphan_b(lgs)
# memento: line 287/289/291 area
lines = t.splitlines()
out["LGS_lines_285_292"] = lines[284:292]

# ---------- L7 (Ecologia) ----------
l7 = os.path.join(REPO, r"ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md")
e = dup_stats(l7)
out["L7_current"] = {k: v for k, v in e.items() if k != "per_block"}
t7 = read(l7)
lines7 = t7.splitlines()
out["L7_art15_label_count"] = len(re.findall(r"(?m)^Art[íi]culo 15\.", t7))
out["L7_df4_terminates_in_preamble"] = bool(re.search(r"en los siguientes términos:\s*\n+## \[", t7))
out["L7_embates_marinos_present"] = ("embates marinos" in t7)
out["L7_directiva_2014_94_present"] = ("2014/94/UE" in t7)
out["L7_v3_marker_21_meses_count"] = t7.count("veintiún meses")
out["L7_v2_marker_12_meses_art15"] = len(re.findall(r"plazo de doce meses|plazo de 12 meses", t7))
# lines of block [a1-7]
m = [i for i, l in enumerate(lines7) if l.startswith("## [a1-7]")]
if m:
    a = m[0]
    nxt = next((i for i in range(a+1, len(lines7)) if lines7[i].startswith("## [")), len(lines7))
    out["L7_a1_7_lines_range"] = (a+1, nxt)  # 1-indexed start,end of block
    out["L7_a1_7_word_count"] = wc("\n".join(lines7[a:nxt]))

# ---------- hashes evidencia ----------
man = json.loads(read(os.path.join(REPO, r"ministerios/hacienda/evidencia/manifiesto_aplicacion_2026-09-01.json")))
out["LGT_manifest_keys"] = list(man.keys())[:10] if isinstance(man, dict) else type(man).__name__

with open(os.path.join(REPO, "auditoria/tmp_auditor_verif_2026-09-01.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
