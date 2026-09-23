# -*- coding: utf-8 -*-
"""Escaneo F1 del CUERPO NORMATIVO LGT contra el canon BOE (sesion 15/30, 23-09-2023).
Metodo: texto unido del consolidado archivado (apparato filtrado, igual que el script
de canon del 22-09), partido por encabezados 'Articulo N.' / 'Disposicion ...'. Cada
parrafo de cada precepto se testea como subsecuencia normalizada del fichero vivo.
Excluye: encabezado/sancion/preambulo (el repo no los incluye por diseno, commit
eb965f4) y la letra de disposicion derogada (no es deber de fidelidad).
Convencion Auditor (dictamen 22-09): hash = sha256(bloque completo desde '## [tag]'
hasta antes de la siguiente cabecera, LF normalizado, sin saltos finales)."""
import re, html, hashlib, unicodedata, json, collections
REPO="C:/Users/d_ant/Projects/gobierno-ia"
SRC=REPO+"/data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html"
LAW=REPO+"/ministerios/hacienda/leyes/BOE-A-2003-23186.md"
def strip_acc(s): return "".join(c for c in unicodedata.normalize("NFD",s) if unicodedata.category(c)!="Mn")
def norm(s): return re.sub(r"[^a-z0-9]","",strip_acc(s.lower()))
raw=open(SRC,encoding="utf-8",errors="replace").read()
txt=re.sub(r"<[^>]+>","\n",raw); txt=html.unescape(txt); txt=re.sub(r"[ \t]+"," ",txt)
lines=[l.strip() for l in txt.splitlines() if l.strip()]
BAD=("Ref. BOE","Seleccionar redacci","Ultima actualizaci","Última actualizaci","Texto original, publicado","Subir","[Bloque","Se deroga","Se añade","Añadido","Redaccion anterior","Redacción anterior","Volver","Se modifica","Modificación publicada","Jurisprudencia","Boletín Oficial","Segundo.-","Primero.-")
J="\n".join(l for l in lines if not any(l.startswith(b) for b in BAD))
# recorte al cuerpo normativo: del primer "Artículo 1." tras la sanción
i1=J.find("Artículo 1.\n")
if i1<0: i1=J.find("Artículo 1.")
cuerpo=J[i1:]
# partir por precepto
heads=list(re.finditer(r"(?m)^(Artículo \d+[^\n]{0,90}|Disposición adicional \w+\.|Disposición transitoria \w+\.|Disposición final \w+\.|Disposición derogatoria \w+\.?$)",cuerpo))
live=open(LAW,encoding="utf-8").read()
ln=norm(live)
# etiqueta de bloque por numero de articulo
def tag_de(h):
    m=re.match(r"Artículo (\d+)",h)
    if m: return "[a%s]"%m.group(1)
    ordinales={"primera":"primera","segunda":"segunda","tercera":"tercera","cuarta":"cuarta","quinta":"quinta","sexta":"sexta","séptima":"septima","sima":"sima"}
    m2=re.match(r"Disposición (adicional|transitoria|final|derogatoria) (\w+)",h)
    if not m2: return None
    mapnum={"única":"unica","unica":"unica","primera":"primera","segunda":"segunda","tercera":"tercera","cuarta":"cuarta","quinta":"quinta","sexta":"sexta","séptima":"septima","septima":"septima","octava":"octava","novena":"novena","décima":"decima","decima":"decima","undécima":"undecima","undecima":"undecima","duodécima":"duodecima","duodecima":"duodecima","decimotercera":"decimotercera","decimocuarta":"decimocuarta","decimoquinta":"decimoquinta","decimosexta":"decimosexta","decimoséptima":"decimoseptima","decimoséptima".replace("é","e"):"decimosptima","decimoctava":"decimoctava","decimonovena":"decimonovena","vigésima":"vigesima","vigesima":"vigesima","vigésimo primera":"vigesimaprimera","vigésimo segunda":"vigesimasegunda","vigésimo tercera":"vigesimatercera"}
    key=mapnum.get(m2.group(2))
    if not key: return None
    pre={"adicional":"da","transitoria":"dt","final":"df","derogatoria":"dd"}[m2.group(1)]
    return "[%s%s]"%(pre,key)
res=collections.OrderedDict()
tot_p=tot_w=0
for k,h in enumerate(heads):
    seg=cuerpo[h.start():heads[k+1].start() if k+1<len(heads) else len(cuerpo)]
    tag=tag_de(h.group(1))
    paras=[p.strip() for p in seg.splitlines() if p.strip()]
    miss=[]
    for p in paras[1:]:
        if norm(p) and norm(p) not in ln: miss.append(p)
    if miss:
        w=sum(len(m.split()) for m in miss)
        tot_p+=len(miss); tot_w+=w
        res[tag or h.group(1)]= {"casos":len(miss),"palabras":w,"ejemplos":[m[:90] for m in miss[:3]]}
print("preceptos con parrafos ausentes:",len(res))
print("TOTAL casos:",tot_p,"palabras:",tot_w)
json.dump({"fuente":"canon data/raw 2026-08-31 vs fichero vivo 2026-09-23 (solo cuerpo normativo; preambulo excluido por diseno del repo)",
"metodo":"subsecuencia normalizada por parrafo; convencion hash del Auditor 22-09 para bloques",
"preceptos_afectados":res},open(REPO+"/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
