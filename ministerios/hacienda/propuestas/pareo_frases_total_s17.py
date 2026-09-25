# Test por frases sobre LOS 292 preceptos — métrica oficial de cierre «preceptos con texto» (acuerdo 67)
import json, re, unicodedata

canon = json.load(open(r"C:/Users/d_ant/Projects/gobierno-ia/data/canonical/BOE-A-2003-23186/2026-08-31.json", encoding="utf-8"))
arts = canon["articulos"]
ley = open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()

def bloque(tag):
    m = re.search(r"^## \[" + re.escape(tag) + r"\].*?(?=^## \[|\Z)", ley, re.S | re.M)
    return m.group(0) if m else ""

def norm(s):
    s = unicodedata.normalize("NFC", s)
    s = s.replace("<sup>", "").replace("</sup>", "").replace("’", "'").replace("«", '"').replace("»", '"')
    return re.sub(r"\s+", " ", s).strip().lower()

out = {}
sin_texto = []
for a in arts:
    tag = a["id"]
    b = norm(bloque(tag))
    if not b:
        sin_texto.append((tag, "bloque inexistente", 0))
        continue
    frases = [f.strip() for f in re.split(r"(?<=[.;:])\s+", norm(a["texto"])) if len(f.strip()) >= 15]
    falt = [f for f in frases if f not in b]
    fw = sum(len(f.split()) for f in falt)
    out[tag] = {"frases": len(frases), "faltan": len(falt), "pal_faltan": fw, "ejemplos": falt[:2]}
    if fw:
        sin_texto.append((tag, "frases ausentes", fw))

con_texto = len(arts) - len(sin_texto)
resumen = {
    "fecha": "2026-09-25", "sesion": 17,
    "metodo": "test por frases literales (≥15 chars), canon data/canonical 2026-08-31 vs fichero vivo; NFC+espacios+puntuación normalizada",
    "preceptos_canon": len(arts),
    "preceptos_con_texto": con_texto,
    "preceptos_con_texto_pct": round(100 * con_texto / len(arts), 2),
    "preceptos_deficientes": sin_texto,
    "palabras_litualmente_ausentes": sum(s[2] for s in sin_texto),
}
json.dump({"resumen": resumen, "detalle": out}, open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/pareo_frases_total_s17_2026-09-25.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("PRECEPTOS CON TEXTO:", con_texto, "/", len(arts), "=", resumen["preceptos_con_texto_pct"], "%")
for s in sin_texto:
    print("  DEFICIENTE:", s)
