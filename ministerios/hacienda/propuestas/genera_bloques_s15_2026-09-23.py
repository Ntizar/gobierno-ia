# -*- coding: utf-8 -*-
"""Genera los bloques propuestos [a82] y [a104] desde el canon BOE archivado
(texto byte a byte; las lineas partidas por enlaces HTML inline se vuelven a unir;
la nota de aparato «Vease la D.A. undecima de la Ley 16/2022» del art. 82 pasa al
pie, etiquetada, y no al cuerpo). Mide el diff antes/despues con la convencion de
hash dictada por el Auditor el 22-09: sha256 del bloque completo con cabecera, LF
normalizado, sin saltos finales."""
import re, html, hashlib
REPO="C:/Users/d_ant/Projects/gobierno-ia"
SRC=REPO+"/data/raw/boe/BOE-A-2003-23186/2026-08-31/source.html"
LAW=REPO+"/ministerios/hacienda/leyes/BOE-A-2003-23186.md"
raw=open(SRC,encoding="utf-8",errors="replace").read()
txt=re.sub(r"<[^>]+>","\n",raw); txt=html.unescape(txt); txt=re.sub(r"[ \t]+"," ",txt)
lines=[l.strip() for l in txt.splitlines() if l.strip()]
BAD=("Ref. BOE","Seleccionar redacci","Última actualizaci","Texto original, publicado","Subir","[Bloque","Se deroga","Se añade","Añadido","Redacción anterior","Volver","Se modifica","Modificación publicada","Jurisprudencia",".", "..")
def keep(l): return not any(l.startswith(b) for b in BAD)
J="\n".join(l for l in lines if keep(l))
def grab(ini,fin):
    i=J.find(ini); j=J.find(fin,i+len(ini)); return J[i:j].strip()
def unir(canon):
    """nuevo parrafo solo si el anterior cierra norma (. o ':' o ')' de letra):
    las lineas partidas por enlaces HTML inline se pegan al anterior."""
    out=[]
    for l in canon.splitlines():
        l=l.strip()
        if not l: continue
        if not out: out.append(l); continue
        prev=out[-1]
        starts_par=re.match(r"^(\d\.\s|[a-z]\)\s|Véase |Queda excluido|El plazo se contará)",l)
        if starts_par or re.search(r"[.:]$",prev):
            out.append(l)
        else:
            out[-1]=prev+" "+l
    return out
def sha_bloque(texto):
    return hashlib.sha256(texto.replace("\r\n","\n").rstrip("\r\n").encode("utf-8")).hexdigest()
c82=grab("Artículo 82.","Véase la disposición adicional undécima")  # cuerpo sin la nota de aparato
c104=grab("Artículo 104.","Artículo 105.")
pie82="> Consolidación 2026-09-23 (Ministerio de Hacienda): texto íntegro del BOE consolidado vigente, en una sola copia. El bloque del repo conservaba tres copias del precepto y ninguna con la letra a) del apartado 2 (la dispensa por cuantía); solo la primera copia recogía además la remisión anterior a la reforma del apartado 1 por el art. único.15 de la Ley 34/2015, de 21 de septiembre (en vigor 12/10/2015) — «apartado 5» del artículo anterior —, superada por la vigente («apartado 6») que ya portaban las otras dos. La nota de aparato del BOE consolidado —«Véase la disposición adicional undécima de la Ley 16/2022, de 5 de septiembre, de reforma del texto refundido de la Ley Concursal, en cuanto a aplazamientos y fraccionamientos de deudas tributarias por la Agencia Estatal de Administración Tributaria, que produce efectos desde el 1 de enero de 2023» (Ref. BOE-A-2022-14580)— se reproduce aquí y no en el cuerpo: es aparato, no precepto (en el fichero vivo venía además con una etiqueta HTML colada: «<a class=\"refPost\">»). Las remisiones «reglamentariamente» (apartados 1 y 2.b)) no fijan plazo propio en la ley: no se inventa ninguno. Órgano de aplicación: la Administración tributaria (AEAT, Departamento de Recaudación)."
pie104="> Consolidación 2026-09-23 (Ministerio de Hacienda): texto íntegro del BOE consolidado vigente, en una sola copia. El bloque del repo conservaba dos copias del precepto: ninguna con la letra a) del apartado 1 («El plazo se contará:» seguido directamente por la b)), ninguna con la letra a) del apartado 4, y ninguna con el párrafo primero del apartado 5 (declaración de oficio o a instancia del interesado y archivo de las actuaciones). Además, la primera copia conserva el apartado 2 en su redacción anterior a la reforma por el art. único.20 de la Ley 34/2015, de 21 de septiembre (en vigor 12/10/2015): le faltan el párrafo de los sujetos obligados o acogidos voluntariamente a recibir notificaciones electrónicas y los períodos de suspensión del plazo, ambos vigentes. El plazo máximo de seis meses es legal; las interrupciones justificadas, dilaciones y suspensiones del apartado 2 remiten a desarrollo reglamentario: la ley no fija plazo propio, no se inventa ninguno. Órgano de aplicación: la Administración tributaria actuante en cada procedimiento de aplicación de los tributos."
def bloque(tag_tit,canon,pie):
    return "## "+tag_tit+"\n\n"+"\n\n".join(unir(canon))+"\n\n"+pie+"\n"
b82=bloque("[a82] Artículo 82",c82,pie82)
b104=bloque("[a104] Artículo 104",c104,pie104)
open(REPO+"/ministerios/hacienda/evidencia/bloque_propuesto_a82_2026-09-23.txt","w",encoding="utf-8").write(b82)
open(REPO+"/ministerios/hacienda/evidencia/bloque_propuesto_a104_2026-09-23.txt","w",encoding="utf-8").write(b104)
law=open(LAW,encoding="utf-8").read()
def w(s): return len(s.split())
for tag,ini,fin,b,cn in (("[a82]","## [a82]","## [a83]",b82,c82),("[a104]","## [a104]","## [a105]",b104,c104)):
    i=law.find(ini); j=law.find(fin,i+1); vivo=law[i:j]
    print(tag,"VIVO:",w(vivo),"pal | sha:",sha_bloque(vivo)[:16])
    print(tag,"PROP:",w(b),"pal | sha:",sha_bloque(b)[:16],"| Δ neto:",w(b)-w(vivo))
    Js=re.sub(r"\s+"," ",J)  # huecos normalizados: los enlaces HTML inline del archivado partían líneas; unir() las pega y la comparación debe ser con el canon compactado
    for p in unir(cn):
        assert re.sub(r"\s+"," ",p) in Js, ("no literal del canon:",p[:70])
    # etiquetas de letra unicas en el propuesto
    for letra in ("a)","b)","c)"):
        n=len(re.findall(r"(?m)^%s"%re.escape(letra),"\n".join(unir(cn))))
        print(tag,"letra",letra,"en cuerpo:",n)
print("OK: test de literalidad canon + hashes con convencion del Auditor")
