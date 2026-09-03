# -*- coding: utf-8 -*-
# TEST DE REEJECUCION UNIVERSAL — cierre Fase 1 (acuerdo 18 Consejo 2026-09-01)
# 1) dedup_scan antes (copia /tmp/ley_ANTES) vs despues (fichero vivo): debe BAJAR
# 2) fidelidad hash: TODO parrafo de los bloques [adieciocho] y [atreintaycinco]
#    post-diff debe tener SHA-256 identica a un parrafo del BOE consolidado plano
# 3) contadores: 21 letras a) del BOE presentes; 6 lineas 1.ª art. 35; 3 cabeceras
import re, json, hashlib, unicodedata, subprocess, sys

BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
LEY = BASE + "/leyes/BOE-A-1986-10499.md"
PLANO = BASE + "/evidencia/boe_texto_plano.txt"
ANTES = r"C:/Users/d_ant/AppData/Local/Temp/ley_ANTES_2026-09-02.md"

def norm(s):
    return unicodedata.normalize("NFC", s.replace("\u00a0", " ").replace("\ufeff", "").strip())

def h12(s):
    return hashlib.sha256(norm(s).encode("utf-8")).hexdigest()[:12]

def blocks(text):
    heads = [(i, m.group(1)) for i, l in enumerate(text)
             for m in [re.match(r'^## \[(a\w+)\] (.*)$', l)] if m]
    out = {}
    for k, (i, bid) in enumerate(heads):
        j = heads[k+1][0] if k+1 < len(heads) else len(text)
        out.setdefault(bid, []).extend([l for l in text[i+1:j] if l.strip()])
    return out

ley = open(LEY, encoding="utf-8").read().splitlines()
antes = open(ANTES, encoding="utf-8").read().splitlines()
plano = open(PLANO, encoding="utf-8").read().splitlines()

# --- BOE: set de hashes de parrafos del plano (todas las lineas no vacias) ---
boe = {h12(l) for l in plano if norm(l)}
res = {"fecha": "2026-09-02", "test": "reejecucion universal Fase 1"}

# --- 1) dedup antes/despues por bloque ---
def dupcount(bl):
    seen = {}
    for p in bl:
        seen.setdefault(h12(p), [0, p])[0] += 1
    return sum((c-1) * len(norm(p).split()) for c, p in seen.values() if c > 1)

ba, bd = blocks(antes), blocks(ley)
res["dedup_18_35"] = {b: {"antes_palabras": dupcount(ba[b]), "despues_palabras": dupcount(bd[b])}
                      for b in ("adieciocho", "atreintaycinco")}
res["total_ley_antes"] = sum(dupcount(v) for v in ba.values())
res["total_ley_despues"] = sum(dupcount(v) for v in bd.values())

# --- 2) fidelidad: cada parrafo del bloque post-diff existe en el BOE ---
fid = {}
for b in ("adieciocho", "atreintaycinco"):
    paras = [p for p in bd[b] if not p.startswith("## ")]
    ok = [p for p in paras if h12(p) in boe]
    bad = [p for p in paras if h12(p) not in boe]
    fid[b] = {"parrafos": len(paras), "hash_en_BOE": len(ok), "no_coinciden": [p[:70] for p in bad]}
res["fidelidad_hash"] = fid

# --- 3) contadores ---
a_res = json.load(open(BASE + "/evidencia/a_restituir_completas_2026-09-01.json", encoding="utf-8"))
presentes = sum(1 for r in a_res if any(h12(l) == h12(r["letra_a_BOE"]) for l in ley))
txt = "\n".join(ley)
res["restituciones"] = {
    "letras_a_BOE_presentes": f"{presentes}/21",
    "lineas_1a_art35": sum(1 for p in bd["atreintaycinco"] if norm(p).startswith("1.ª")),
    "preferencia_colaboracion_art28": "Preferencia de la colaboración voluntaria con las autoridades sanitarias." in txt,
    "cabeceras_art18": sum(1 for l in ley if norm(l) == "Artículo dieciocho"),
    "cabeceras_art35": sum(1 for l in ley if norm(l) == "Artículo treinta y cinco"),
}
res["pasos"] = sum(1 for x in [
    res["fidelidad_hash"]["adieciocho"]["hash_en_BOE"] == res["fidelidad_hash"]["adieciocho"]["parrafos"],
    res["fidelidad_hash"]["atreintaycinco"]["hash_en_BOE"] == res["fidelidad_hash"]["atreintaycinco"]["parrafos"],
    presentes == 21,
    res["restituciones"]["lineas_1a_art35"] == 3,
    res["restituciones"]["preferencia_colaboracion_art28"],
    res["restituciones"]["cabeceras_art18"] == 1,
    res["restituciones"]["cabeceras_art35"] == 1,
    res["total_ley_despues"] < res["total_ley_antes"],
    res["dedup_18_35"]["adieciocho"]["despues_palabras"] == 0,
    res["dedup_18_35"]["atreintaycinco"]["despues_palabras"] <= 15,
])
res["nota_15pal"] = "Las 15 pal. restantes del art. 35 son el par 1.ª B)=1.ª C), idéntico por ley en el propio BOE — no es basura editorial, no se borra."
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(BASE + "/evidencia/test_reejecucion_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
