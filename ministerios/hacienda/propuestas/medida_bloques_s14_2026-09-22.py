# Limpia aparato residual del canon da20, genera los dos bloques propuestos
# (encabezado + canon + pie de consolidación) y mide palabras/ hashes exactos.
import hashlib, re

C = "ministerios/hacienda/evidencia/boe_canonico_da11_da20_2026-09-22.txt"
txt = open(C, encoding="utf-8").read()

def block(tag):
    i = txt.find("### " + tag); j = txt.find("### ", i + 4)
    s = txt[i:j]
    body = s.split("\n", 1)[1].strip()
    # quitar líneas de aparato del BOE web
    BAD = ("Ref. BOE", "Seleccionar redacci", "Última actualizaci", "Texto original", "Subir",
           "[Bloque", "Se deroga", "Se añade", "Modificación publicada", "Texto añadido", ".")
    keep = [l for l in body.splitlines() if l.strip() and l.strip() not in BAD and not l.startswith(BAD)]
    return "\n".join(keep)

da11 = block("da11")
da20 = block("da20")

foot11 = ("> Consolidación 2026-09-22 (Hacienda): texto íntegro del BOE consolidado vigente. "
 "Última modificación aplicable: Ley 6/2018, de 3 de julio, cuya disposición derogatoria única suprimió la letra c) del apartado 1 "
 "(pensiones y derechos pasivos), que el fichero del repo aún conservaba; las remisiones «reglamentariamente» (apartados 5, 6 y 7) "
 "remiten al desarrollo por el Ministerio competente y la ley no fija plazo propio: no se inventa ninguno. "
 "Órganos de aplicación: los tribunales económico-administrativos, con legitimación de la Interventor General de la Administración del Estado conforme al apartado 3.")
foot20 = ("> Consolidación 2026-09-22 (Hacienda): texto íntegro del BOE consolidado vigente "
 "(añadida por la Ley 34/2015, de 21 de septiembre, art. único.63; letra d) del apartado 1 añadida por la Ley 11/2021, de 9 de julio, art. 13.27). "
 "Los plazos de notificación y caducidad del apartado 1.b) son los de la normativa de la Unión Europea: la ley no fija plazo propio, no se inventa ninguno. "
 "Órgano de aplicación: la Administración tributaria (AEAT, Departamento de Aduanas e Impuestos Especiales).")

def full(head_md, title_line, canon, foot):
    paras = [head_md, "", title_line, ""]
    for p in canon.split("\n")[1:]:
        paras += [p, ""]
    paras += [foot, ""]
    return "\n".join(paras)

h11 = "## [daundecima] Disposición adicional undécima"
t11 = da11.splitlines()[0]
h20 = "## [davigesima] Disposición adicional vigésima"
t20 = da20.splitlines()[0]
b11 = full(h11, t11, da11, foot11)
b20 = full(h20, t20, da20, foot20)

open("ministerios/hacienda/evidencia/bloque_propuesto_da11_2026-09-22.txt", "w", encoding="utf-8").write(b11)
open("ministerios/hacienda/evidencia/bloque_propuesto_da20_2026-09-22.txt", "w", encoding="utf-8").write(b20)

print("PROPUERTO da11:", len(b11.split()), "pal | sha256", hashlib.sha256(b11.encode()).hexdigest()[:16])
print("PROPUERTO da20:", len(b20.split()), "pal | sha256", hashlib.sha256(b20.encode()).hexdigest()[:16])
print("CANON da11:", len(da11.split()), "| CANON da20:", len(da20.split()))

law = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
print("SHA LEY:", hashlib.sha256(law.encode("utf-8")).hexdigest())
for ini, fin in (("## [daundecima]", "## [daduodecima]"), ("## [davigesima]", "## [davigesimoprimera]")):
    i = law.find(ini); j = law.find(fin, i+1)
    print(ini, "actual:", len(law[i:j].split()), "pal")
