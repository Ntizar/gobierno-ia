# -*- coding: utf-8 -*-
"""Genera docs/index.html del Gobierno IA con las novedades de cada día.
Lee actas del Consejo, auditorías, informes presidenciales y KPIs del repo
y renderiza un boletín estático. Todo en castellano."""
import re, os, json, html, subprocess, datetime

REPO = "C:/Users/d_ant/Projects/gobierno-ia"

def esc(s): return html.escape(str(s))

def fecha_humana(d):
    MESES = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"

def listar(carpeta, sufijo=".md"):
    p = os.path.join(REPO, carpeta)
    if not os.path.isdir(p): return []
    return sorted(f for f in os.listdir(p) if f.endswith(sufijo))

def leer(path):
    try:
        return open(path, encoding="utf-8").read()
    except Exception:
        return ""

def celdas(linea):
    """Celdas de una fila de tabla markdown, sin los pipes exteriores."""
    return [c.strip() for c in linea.strip().strip("|").split("|")]

VEREDICTOS = r"(APROBADO CON CONDICI[ÓO]N|APROBADO|APLAZADAS?|APLAZADO|RECHAZADO(?:S)?|VALIDADA CON OBSERVACIONES|VALIDADA|RECHAZADA)"

def _descripcion(cs, idx, veredicto):
    """La celda más informativa de la fila: la de antes del veredicto si la hay,
    si no las dos primeras de después (se descartan números de columna y guiones)."""
    def util(c):
        t = c.replace("*", "").strip()
        return len(t) > 8 and not re.fullmatch(r"[-–\d.\s]+", t)
    antes = [c for c in cs[:idx] if util(c)]
    if antes:
        return max(antes, key=len)
    despues = [c for c in cs[idx + 1:] if util(c)]
    return " · ".join(despues[:2])

def filas_veredicto(texto, patron):
    """Filas de tabla que contienen un veredicto: (descripción, veredicto literal).

    Busca el veredicto por prioridad: celda que ES el veredicto, celda que EMPIEZA por
    él, y por último celda que lo CONTIENE. La prioridad importa: en la tabla de una
    auditoría la celda del acuerdo puede contener «APROBADO CON CONDICIÓN (cumplida)»
    mientras el veredicto real («VALIDADA») vive en la columna siguiente."""
    out = []
    for linea in texto.splitlines():
        if not linea.strip().startswith("|") or "---" in linea:
            continue
        cs = celdas(linea)
        idx = ver = None
        for modo in (re.fullmatch, re.match, re.search):
            for i, c in enumerate(cs):
                t = c.replace("*", "").strip()
                m = modo(patron, t, re.I)
                if m:
                    idx, ver = i, (m.group(1) if m.groups() else t)
                    break
            if idx is not None:
                break
        if idx is None:
            continue
        d = _descripcion(cs, idx, ver)
        if d:
            out.append((d, ver))
    return out

BADGE = {"aplazadas": "aplazado", "aplazada": "aplazado", "rechazadas": "rechazado",
         "validada con observaciones": "observaciones", "validada": "validada", "rechazada": "rechazado"}

def clase_badge(ver):
    return BADGE.get(ver.lower().strip(), ver.lower().split()[0])

def extraer_acuerdos(acta):
    """Extrae acuerdos del acta: filas de tabla con veredicto o líneas 'Nombre: APROBADO'."""
    filas = []
    for desc, ver in filas_veredicto(acta, VEREDICTOS):
        filas.append(f'<li><span class="badge {clase_badge(ver)}">{esc(ver)}</span> {esc(desc[:160])}</li>')
    for linea in acta.splitlines():
        m2 = re.match(r"\s*[-*]\s*(.+?):\s*\*?\*?(APROBADO|APLAZADO|RECHAZADO)", linea, re.I)
        if m2:
            filas.append(f'<li><span class="badge {clase_badge(m2.group(2))}">{m2.group(2)}</span> {esc(m2.group(1)[:160])}</li>')
    return "".join(filas)

def extraer_seccion(texto, titulo):
    """Extrae el contenido de '## <titulo>' hasta el siguiente '## '."""
    m = re.search(rf"#+\s*{re.escape(titulo)}.*?\n(.*?)(?=\n#|\Z)", texto, re.S | re.I)
    return m.group(1).strip() if m else ""

def bullets(texto, limite=5):
    out = []
    for l in texto.splitlines():
        m = re.match(r"\s*[-*]\s*(.+)", l)
        if m and m.group(1).strip():
            out.append(f"<li>{esc(m.group(1).strip()[:220])}</li>")
        if len(out) >= limite: break
    return "".join(out)

def tabla_veredictos(aud):
    filas = []
    for desc, ver in filas_veredicto(aud, VEREDICTOS):
        filas.append(f'<tr><td>{esc(desc[:140])}</td><td><span class="badge {clase_badge(ver)}">{esc(ver)}</span></td></tr>')
    if not filas: return ""
    return "<table><tr><th>Acuerdo</th><th>Veredicto del Auditor</th></tr>" + "".join(filas) + "</table>"

def kpis_ministro(kpi_txt):
    """Última fila del histórico diario."""
    m = re.findall(r"^\|\s*-?\s*(\d{4}-\d{2}-\d{2}.*?)\|\s*$", kpi_txt, re.M)
    return m[-1].strip() if m else "sin datos"

def dia_md(d):
    iso = d.isoformat()
    acta = leer(os.path.join(REPO, "consejo/actas", f"{iso}.md"))
    aud  = leer(os.path.join(REPO, "auditoria", f"{iso}.md"))
    inf  = leer(os.path.join(REPO, "presidencia/informes", f"{iso}.md"))
    props = {m: leer(os.path.join(REPO, f"ministerios/{m}/propuestas", f"{iso}.md"))
             for m in ["hacienda", "sanidad", "transicion-ecologica"]}
    kpis = {m: leer(os.path.join(REPO, f"ministerios/{m}/kpis.md")) for m in props}
    hay = acta or aud or any(props.values()) or inf
    if not hay: return ""

    bloques = [f'<div class="dia"><h2>{fecha_humana(d)}</h2>']

    # Propuestas de los ministros (solo si hay alguna: un día en blanco no debe salir con lista vacía)
    items = []
    for m, txt in props.items():
        n = txt.count("## Propuesta")
        if n:
            titulos = re.findall(r"## Propuesta \d+: (.+)", txt)
            for t in titulos[:2]:
                items.append(f"<li><b>{esc(m.capitalize())}</b> — {esc(t[:150])}</li>")
        if "## Reasignación presupuestaria" in txt or "Reasignación presupuestaria" in txt:
            items.append(f"<li><b>{esc(m)}</b>: 💶 reasignación presupuestaria propuesta</li>")
    if items:
        bloques.append('<div class="seccion"><h3>Propuestas de los ministros</h3><ul>' + "".join(items) + "</ul></div>")

    # Acuerdos del Consejo
    if acta:
        ac = extraer_acuerdos(acta)
        if ac:
            bloques.append(f'<div class="seccion"><h3>Acuerdos del Consejo</h3><ul>{ac}</ul></div>')

    # Veredictos del Auditor
    if aud:
        tv = tabla_veredictos(aud)
        if tv: bloques.append(f'<div class="seccion"><h3>Auditoría del Estado</h3>{tv}</div>')
        riesgos = bullets(extraer_seccion(aud, "Riesgos del Estado"), 3)
        if riesgos:
            bloques.append(f'<div class="seccion"><h3>Riesgos del Estado</h3><ul>{riesgos}</ul></div>')
        kpi_rows = ""
        for m in props:
            estado = kpis_ministro(kpis[m])
            kpi_rows += f"<tr><td>{esc(m)}</td><td>{esc(estado[:120])}</td></tr>"
        if kpi_rows:
            bloques.append("<div class='seccion'><h3>KPIs de los ministros</h3><table><tr><th>Ministerio</th><th>Último dato</th></tr>" + kpi_rows + "</table></div>")

    # Informe presidencial
    if inf:
        m_imp = re.search(r"^#+.*?Lo más importante.*?$(.*?)(?=^#|\Z)", inf, re.S | re.M | re.I)
        if m_imp:
            pts = [x.strip().replace("**", "").replace("`", "")
                   for x in re.findall(r"^\s*\d+\.\s+(.+)", m_imp.group(1), re.M)]
            if pts:
                bloques.append('<div class="seccion"><h3>Lo más importante del informe presidencial</h3><ul>' +
                    "".join(f"<li>{esc(p[:260])}</li>" for p in pts[:3]) + "</ul></div>")
        enlaces = [e.rstrip(")\"'>.,;") for e in re.findall(r"https?://\S+", inf)]
        if enlaces:
            bloques.append('<div class="seccion"><h3>Enlaces del informe</h3><ul>' +
                "".join(f'<li><a href="{esc(u)}">{esc(u[:90])}</a></li>' for u in enlaces[:3]) + "</ul></div>")

    bloques.append("</div>")
    return "".join(bloques)

def main():
    # días con actividad: unión de ficheros con fecha
    fechas = set()
    for carpeta in ["consejo/actas", "auditoria", "presidencia/informes"]:
        for f in listar(os.path.join(REPO, carpeta)):
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f)
            if m: fechas.add(m.group(1))
    # también días con propuestas de ministros (aunque no haya acta aún)
    for m_ in ["hacienda", "sanidad", "transicion-ecologica"]:
        for f in listar(os.path.join(REPO, f"ministerios/{m_}/propuestas")):
            fm = re.match(r"(\d{4}-\d{2}-\d{2})", f)
            if fm: fechas.add(fm.group(1))
    dias = sorted(fechas, reverse=True)[:14]  # últimos 14 días con actividad

    if dias:
        cuerpo = "".join(dia_md(datetime.date.fromisoformat(d)) for d in dias)
    else:
        cuerpo = '<div class="dia"><h2>Pendiente de la primera jornada</h2><div class="seccion"><ul><li>Primer pase de lista: mañana a las 10:00.</li></ul></div></div>'

    plantilla = leer(os.path.join(REPO, "docs/index.html"))
    nuevo = re.sub(r"<!-- GENERADO.*?-->[\s\S]*?(?=<footer>)", "<!-- GENERADO -->" + cuerpo + "\n  </div>\n  ", plantilla, flags=re.S)
    # actualizar el aviso "pendiente" solo si no hay días
    open(os.path.join(REPO, "docs/index.html"), "w", encoding="utf-8").write(nuevo)
    print("OK, días renderizados:", len(dias))

if __name__ == "__main__":
    main()
