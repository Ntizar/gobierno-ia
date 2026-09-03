# -*- coding: utf-8 -*-
# DIFFS FASE 1 — 2026-09-03: deduplicacion [aveinticinco] y [asetentaynueve]
# Criterio (acuerdo 17 + método Fase 1): conservar UNA sola copia, la redaccion
# VIGENTE coincidente con el BOE consolidado (hash parrafo); suprimir capas
# apiladas obsoletas y copias parciales. En art. 79 la copia conservada se
# COMPLETA con "e) Tributos estatales cedidos." (Ley 21/2001 art. 68.1, segun
# nota oficial del BOE) integrada tras d). En art. 25 la copia vigente intercala
# 3. y 4. que precedian fisicamente a la capa nueva -> se reordena segun BOE.
import re, json, hashlib, unicodedata, io, sys, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
LEY = BASE + "/leyes/BOE-A-1986-10499.md"
PLANO = BASE + "/evidencia/boe_texto_plano.txt"
ANTES = r"C:/Users/d_ant/AppData/Local/Temp/ley_ANTES_2026-09-03.md"
shutil.copyfile(LEY, ANTES)

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())
def h12(s):
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()[:12]

plano_lines = open(PLANO, encoding="utf-8").read().splitlines()
boe = {h12(l) for l in plano_lines if norm(l)}
boe_order = {}
for n, l in enumerate(plano_lines):
    t = norm(l)
    if t and h12(t) not in boe_order:
        boe_order[h12(t)] = n + 1

lines = open(LEY, encoding="utf-8").read().splitlines()

def heads_of(ls):
    return [(i, m.group(1)) for i, l in enumerate(ls) for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]

report = {"fecha": "2026-09-03"}

# ============ [aveinticinco] ============
heads = heads_of(lines)
k = next(i for i, (n, b) in enumerate(heads) if b == "aveinticinco")
s, e = heads[k][0], (heads[k+1][0] if k+1 < len(heads) else len(lines))
paras = {}
for n in range(s+1, e):
    if norm(lines[n]):
        paras.setdefault(h12(lines[n]), []).append(lines[n].rstrip())

def P(pref, must=None):
    for h, v in paras.items():
        t = norm(v[0])
        if t.startswith(pref) and (must is None or must in t):
            return v[0]
    raise SystemExit("NO ENCONTRADO: " + pref)

cur1 = P("1. La exigencia", "Ley General de Salud Pública")
assert h12(cur1) in boe
head = "Artículo veinticinco."
new = [head, "", cur1, "",
       P("2. Las autorizaciones"), "",
       P("a) No resultarán"), "", P("b) Deberán estar justificados"), "",
       P("c) Se cuidará"), "", P("d) Los procedimientos"), "",
       P("3. Deberán establecerse"), "", P("4. Cuando la actividad"), ""]
removed25 = [norm(l) for l in lines[s+1:e] if norm(l)]
words_removed25 = sum(len(t.split()) for t in removed25) - sum(len(norm(x).split()) for x in new if norm(x))
report["aveinticinco"] = {
    "lineas_antes": e - s - 1, "lineas_despues": len(new) + 0,
    "palabras_suprimidas": words_removed25,
    "suprimido_detalle": [t[:80] for t in removed25 if norm(t) not in [norm(x) for x in new if norm(x)]][:1] if False else "ver diff",
}
lines[s+1:e] = new + [""]

# ============ [asetentaynueve] ============
heads = heads_of(lines)
k = next(i for i, (n, b) in enumerate(heads) if b == "asetentaynueve")
s, e = heads[k][0], (heads[k+1][0] if k+1 < len(heads) else len(lines))
body = [l.rstrip() for l in lines[s+1:e] if l.strip()]
c1_start = next(i for i, l in enumerate(body) if norm(l) == "Artículo setenta y nueve")
sec_head = next(i for i, l in enumerate(body) if i > c1_start and norm(l) == "Artículo setenta y nueve")
i_num1 = next(i for i, l in enumerate(body) if norm(l).startswith("1. La financiación"))
i_second = next(i for i, l in enumerate(body) if i > i_num1 and norm(l).startswith("1. La financiación"))
e_line = next(i for i, l in enumerate(body) if i >= i_second and norm(l).startswith("e) Tributos"))
e_txt = body[e_line].rstrip()
words_removed79 = sum(len(norm(l).split()) for i, l in enumerate(body) if i >= i_second and i != e_line)
copyA = [l for i, l in enumerate(body[:i_second]) if not (i > c1_start and norm(l) == "Artículo setenta y nueve")]
out = []
for l in copyA:
    out.append(l)
    if norm(l).startswith("d) Por aportaciones"):
        out.append(e_txt)
new79 = sum([[x, ""] for x in out], [])
report["asetentaynueve"] = {
    "lineas_antes": e - s - 1, "lineas_despues": len(new79),
    "palabras_suprimidas": words_removed79,
    "nota": "copia A conservada y COMPLETADA con e) tras d) (Ley 21/2001 art. 68.1)" if "e)" not in [norm(x) for x in copyA] else "",
}
lines[s+1:e] = new79 + [""]

open(LEY, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

# ============ VERIFICACION ============
lines2 = open(LEY, encoding="utf-8").read().splitlines()
out_blocks, cur = {}, None
for l in lines2:
    m = re.match(r'^## \[(a\w+)\] (.*)$', l)
    if m: cur = m.group(1); out_blocks[cur] = []
    elif cur: out_blocks[cur].append(l)

def dupcount(paras):
    seen = {}
    for p in paras:
        seen.setdefault(h12(p), [0, p])[0] += 1
    return sum((c-1) * len(norm(p).split()) for c, p in seen.values())

res = {}
for bid in ("aveinticinco", "asetentaynueve"):
    pr = [norm(l) for l in out_blocks[bid] if norm(l)]
    res[bid] = {"parrafos": len(pr), "dup_rest": dupcount(pr),
                "fuera_BOE": [p[:90] for p in pr if h12(p) not in boe]}
res["orden_25_ok"] = [n for n, l in enumerate([norm(x) for x in out_blocks["aveinticinco"] if norm(x)]) if l[:2] in ("1.","2.","3.","4.")]
res["a_25_unica"] = sum(1 for p in out_blocks["aveinticinco"] if norm(p).startswith("a) No resultarán"))
res["a_79_unica"] = sum(1 for p in out_blocks["asetentaynueve"] if norm(p) == "a) Cotizaciones sociales.")
res["e_79_tras_d"] = [norm(x)[:4] for x in out_blocks["asetentaynueve"] if norm(x) and re.match(r'^[a-e]\)', norm(x))]
total = {b: dupcount([norm(l) for l in ls if norm(l)]) for b, ls in out_blocks.items()}
res["total_ley_dup"] = sum(total.values())
res["bloques_con_dup"] = sum(1 for v in total.values() if v > 0)
res["suprimido"] = report
json.dump(res, open(BASE + "/evidencia/dedup_25_79_2026-09-03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
