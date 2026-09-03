# -*- coding: utf-8 -*-
# Aplicacion de los diffs APROBADOS por el Consejo 2026-09-01 (acuerdo 17) sobre
# el fichero de la Ley 14/1986. Todo el texto sale del BOE consolidado plano
# (evidencia/boe_texto_plano.txt) — cero tecleo manual de texto legal.
import re, json, hashlib, unicodedata, sys

BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
LEY = BASE + "/leyes/BOE-A-1986-10499.md"
PLANO = BASE + "/evidencia/boe_texto_plano.txt"

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

lines = open(LEY, encoding="utf-8").read().splitlines()
plano = open(PLANO, encoding="utf-8").read().splitlines()
heads = [(i, m.group(1)) for i, l in enumerate(lines)
         for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]

def block_range(bid):
    idxs = [i for i, b in enumerate(heads) if heads[b][1] == bid] if False else [i for i, b in heads if b == bid]
    assert len(idxs) == 1, (bid, idxs)
    s = idxs[0]
    nxt = [i for i, b in heads if i > s]
    return s, (nxt[0] if nxt else len(lines))

# ---- extraccion del BOE plano: consolidado art. 18 (intro + 18 pts) ----
i24 = next(i for i, l in enumerate(plano) if "Bloque 24: #adieciocho" in l)
j = next(i for i in range(i24, len(plano)) if norm(plano[i]) == "Artículo dieciocho")
buf18 = []
for l in plano[j+1:]:
    s = norm(l)
    if s.startswith("Se modifica"):
        break
    if s:
        buf18.append(s)
assert len(buf18) == 19, ("art18", len(buf18))
assert buf18[0].startswith("Las Administraciones Públicas"), buf18[0]
assert buf18[-1].startswith("18."), buf18[-1]

# ---- consolidado art. 35 (intro + A)/3 + B)/7 + C)/8) ----
i45 = next(i for i, l in enumerate(plano) if "Bloque 45: #atreintaycinco" in l)
j35 = next(i for i in range(i45, len(plano)) if norm(plano[i]).startswith("Se tipifican"))
buf35 = []
for l in plano[j35:]:
    s = norm(l)
    if s.startswith("Se modifica el apartado"):
        break
    if s:
        buf35.append(s)
assert len(buf35) == 22, ("art35", len(buf35), buf35[:2], buf35[-2:])

def rebuild(bid, title, body):
    out = [f"## [{bid}] {title}", "", title, ""]
    for p in body:
        out.append(p)
        out.append("")
    return out

res = {"aplicado_2026-09-02": True}

# ---- reemplazo art. 18 y 35 (de abajo arriba para no desplazar indices) ----
s, e = block_range("atreintaycinco")
old35 = [l for l in lines[s:e] if l.strip()]
lines[s:e] = rebuild("atreintaycinco", "Artículo treinta y cinco", buf35)
res["art35"] = {"lineas_antes": len(old35), "lineas_despues": len([l for l in rebuild("atreintaycinco", "x", buf35) if l.strip()])}

s, e = block_range("adieciocho")
old18 = [l for l in lines[s:e] if l.strip()]
lines[s:e] = rebuild("adieciocho", "Artículo dieciocho", buf18)
res["art18"] = {"lineas_antes": len(old18), "lineas_despues": len([l for l in rebuild("adieciocho", "x", buf18) if l.strip()])}

# ---- restitucion de las 21 letras «a)» (anclaje por contenido, no por linea) ----
fide = json.load(open(BASE + "/evidencia/fidelidad_21_huerfanas_2026-09-01.json", encoding="utf-8"))
a_res = json.load(open(BASE + "/evidencia/a_restituir_completas_2026-09-01.json", encoding="utf-8"))
pairs = []
for f, r in zip(fide, a_res):
    assert f["linea"] == r["linea_repo"], (f["linea"], r["linea_repo"])
    pairs.append((norm(f["b"]), r["letra_a_BOE"]))
aplicadas, ya_estaban, fallos = [], [], []
plano_norm = [norm(l) for l in plano]
for bpre, a_txt in pairs:
    cands = [i for i, l in enumerate(lines) if norm(l).startswith(bpre)]
    if len(cands) != 1:
        fallos.append((bpre[:60], len(cands)))
        continue
    i = cands[0]
    k = i - 1
    while k >= 0 and not lines[k].strip():
        k -= 1
    if norm(lines[k]) == norm(a_txt):
        ya_estaban.append(a_txt[:50])
        continue
    assert any(a_txt[:60] in pl for pl in plano_norm), ("a) no está en el BOE plano", a_txt[:50])
    lines[i:i] = [a_txt, ""]
    aplicadas.append(a_txt[:50])
res["restituciones_a"] = {"insertadas": len(aplicadas), "ya_estaban": len(ya_estaban), "fallos": fallos}

open(LEY, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
json.dump(res, open(BASE + "/evidencia/aplicacion_diffs_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
