# Sesion 6 — plan de insercion: para cada k, buscar anclaje UNICO en el repo
import json, re
BASE = "ministerios/transicion-ecologica"
norm = lambda s: re.sub(r"\s+", " ", s).strip()

t = json.load(open(f"{BASE}/evidencia/textos_restitucion_532_2026-09-04.json", encoding="utf-8"))
lines = open(f"{BASE}/leyes/BOE-A-2021-8447.md", encoding="utf-8").read().split("\n")
nlines = [norm(x) for x in lines]

# contexto BOE extraido de la sonda (lineas vecinas, recortadas a su forma completa):
# para cada k doy la linea BOE que DEBE preceder y la que DEBE seguir (forma completa)
CTX = {
 0:(None,"Artículo 3."),            # tras cabecera bloque ti
 1:(None,"Artículo 7."),
 2:(None,"Artículo 9."),
 3:(None,"Artículo 14."),
 4:("i) Integrar los planes específicos de electrificación de última milla con las zonas de bajas emisiones.",
    "Real Decreto 102/2011, de 28 de enero"),
 5:("e) La elaboración de informes periódicos de seguimiento y evaluación del PNACC y sus programas y estrategias.","a) La identificación y evaluación de impactos previsibles y riesgos derivados del cambio climático"),
 6:("d) Los riesgos derivados de los impactos posibles del ascenso del nivel del mar sobre las costas y las zonas húmedas.","a) Anticiparse a los impactos previsibles del cambio climático"),
 7:("i) Realizar el seguimiento de los impactos asociados al cambio del clima para ajustar las medidas que se considere necesario.","Artículo 20."),
 8:(None,"Artículo 27."),
 9:("e) El marco de elaboración de los convenios de Transición Justa.","Artículo 28."),
 10:("4. A los efectos de lo previsto en el",", de Régimen Jurídico del Sector Público, la vigencia de los convenios de transición justa"),
 11:(None,"Artículo 37."),
 12:("artículo 62 de la Ley 34/1998, de 7 de octubre","2. Se añade un nuevo apartado 8.bis en el"),
 13:("2. Se añade un nuevo apartado 8.bis en el","artículo 14 de la Ley 24/2013, de 26 de diciembre"),
 14:("artículo 14 de la Ley 24/2013, de 26 de diciembre","«8.bis. Las metodologías de retribución"),
 15:("3. Se modifica el artículo 20.9 de la Ley 24/2013, de 26 de diciembre","«9. Las sociedades que realizan actividades reguladas"),
 16:("3. Se modifica el","«9. Las sociedades que realizan actividades reguladas"),
 17:("4. El apartado 1 del artículo 60 de la Ley 18/2014, de 15 de octubre","La metodología de retribución de las actividades de transporte, regasificación, almacenamiento"),
 18:("«1. En las Leyes de Presupuestos Generales del Estado de cada año se destinará a financiar","2. Las aportaciones señaladas en el apartado anterior"),
 19:("2. Las aportaciones señaladas en el apartado anterior se realizarán mediante libramientos","La aportación que haya de realizarse en función de la recaudación del mes de diciembre"),
 20:("«2. Las sociedades que realicen actividades incluidas en las letras a) y b) del apartado 1","artículo 42.1 del Código de Comercio"),
 21:("artículo 42.1 del Código de Comercio","En las mismas circunstancias señaladas en el párrafo anterior"),
}
def find_unique(s):
    hits=[i for i,l in enumerate(nlines) if s and s in l]
    return hits
for k in range(22):
    prev,nxt = CTX[k]
    ph = find_unique(prev) if prev else []
    nh = find_unique(nxt) if nxt else []
    print(f"k={k:2d} prev_hits={len(ph)}{ph[:3]} next_hits={len(nh)}{nh[:3]}")
