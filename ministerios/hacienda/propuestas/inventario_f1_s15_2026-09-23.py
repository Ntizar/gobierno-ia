# -*- coding: utf-8 -*-
"""
Inventario F1 vivo de la LGT — sesion 15/30 (2026-09-23).
Metodo: canon BOE archivado (data/raw/boe/.../source.html, div.parrafo) pareado
párrafo a parrafo contra el fichero vivo, con normalizacion agresiva
(lower, sin tildes, sin puntuacion, sin espacios) y test de subsecuencia.
Un parrafo del canon FALTA si su forma normalizada NO aparece como subsecuencia
de ningun bloque del repo. Se excluye el aparato del BOE (cabeceras, refs).
Convencion de bloques: 335 (split por '^## \\[...\\]' segun acuerdo 11).
"""
import json, re, hashlib, unicodedata, sys, html

REPO = "C:/Users/d_ant/Projects/gobierno-ia"
LIVE = REPO + "/ministerios/hacienda/leyes/BOE-A-2003-23186.md"
BOE_HTML = REPO + "/data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html"
OUT = REPO + "/ministerios/hacienda/evidencia/inventario_f1_s15_2026-09-23.json"

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def norm(s):
    s = strip_acc(s.lower())
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

def words(s):
    return len(s.split())

# --- canon: parrafos del BOE consolidado ---
raw = open(BOE_HTML, encoding="utf-8", errors="replace").read()
# todos los div/p con class parrafo* o articulo*, en orden de documento
paras = re.findall(r'<(?:div|p)[^>]*class="[^"]*(?:parrafo|articulo)[^"]*"[^>]*>(.*?)</(?:div|p)>', raw, re.S)
canon = []
aparat = re.compile(r"(Se (?:añade|añaden)|Ref\. BOE|Subir|^\[?Bloque|Volver|Boletín Oficial del Estado|© (?:Boletín|Agencia)|Ir a|Sumario|Get XML|Get PDF|histórico)", re.I)
for p in paras:
    t = re.sub(r"<[^>]+>", "", p)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    if not t or aparat.search(t):
        continue
    canon.append(t)

# --- vivo: fichero del repo, por bloques ---
live = open(LIVE, encoding="utf-8", errors="replace").read()
parts = re.split(r"(?m)^(## \[[a-z0-9\-]+\][^\n]*)$", live)
blocks = []  # (etiqueta, texto)
i = 1
while i < len(parts):
    head = parts[i]
    body = parts[i+1] if i+1 < len(parts) else ""
    m = re.match(r"## \[([a-z0-9\-]+)\]", head)
    blocks.append((m.group(1) if m else head, body))
    i += 2
live_norm = norm(live)
print("bloques del repo:", len(blocks))
print("parrafos canon:", len(canon))

missing = []
for t in canon:
    n = norm(t)
    if not n:
        continue
    if n not in live_norm:
        missing.append(t)

print("parrafos del canon AUSENTES del repo:", len(missing))
w = sum(words(t) for t in missing)
print("palabras ausentes:", w)

# localizar a que bloque pertenece cada parrafo ausente: el canon va en orden de
# articulos; usamos la etiqueta mas cercana ANTERIOR encontrable por cabeceras "Art."
def etiqueta_de(t):
    m = re.match(r"\s*(?:Art[íi]culo\s+\d+[^\s]*|Disposici[óo]n\s+\w+|\w+\.)", t)
    return t[:60]

json.dump({
    "fuente": "canon data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html vs fichero vivo 2026-09-23",
    "metodo": "subsecuencia normalizada (lower, sin tildes/puntuacion/espacios)",
    "canon_parrafos": len(canon),
    "casos_ausentes": len(missing),
    "palabras_ausentes": w,
    "hash_vivo_sha256": hashlib.sha256(open(LIVE,'rb').read()).hexdigest()[:8],
    "muestras": missing[:40],
}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", OUT)
