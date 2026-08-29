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

def extraer_acuerdos(acta):
    """Extrae acuerdos del acta: filas de tabla con veredicto o líneas 'Nombre: APROBADO'."""
    filas = []
    # formato tabla: | Propuesta | **APROBADO**... | motivo |
    for linea in acta.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*\*?\*?(APROBADO(?: CON CONDICIÓN)?|APLAZADO(?:AS)?|RECHAZADO(?:AS)?)", linea, re.I)
        if m and "---" not in linea:
            ver = m.group(2).lower().split()[0]
            filas.append(f'<li><span class="badge {ver}">{m.group(2)}</span> {esc(m.group(1)[:160])}</li>')
            continue
        m2 = re.match(r"\s*[-*]\s*(.+?):\s*\*?\*?(APROBADO|APLAZADO|RECHAZADO)", linea, re.I)
        if m2:
            ver = m2.group(2).lower()
            filas.append(f'<li><span class="badge {ver}">{m2.group(2)}</span> {esc(m2.group(1)[:160])}</li>')
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
    for linea in aud.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*\*?\*?(VALIDADA CON OBSERVACIONES|VALIDADA|RECHAZADA)\*?\*?\s*\|", linea, re.I)
        if m and "---" not in linea:
            cls = "validada" if "OBSERVACIONES" in m.group(2).upper() else m.group(2).lower()
            cls = "observaciones" if "OBSERVACIONES" in m.group(2).upper() else cls
            filas.append(f'<tr><td>{esc(m.group(1)[:140])}</td><td><span class="badge {cls}">{m.group(2)}</span></td></tr>')
    if not filas: return ""
    return "<table><tr><th>Acuerdo</th><th>Veredicto del Auditor</th></tr>" + "".join(filas) + "</table>"

def kpis_ministro(kpi_txt):
    """Última fila del histórico diario."""
    m = re.findall(r"^\|(\s*\d{4}-\d{2}-\d{2}.*?)\|\s*$", kpi_txt, re.M)
    return m[-1].strip() if m else "sin datos"

def dia_md(d):
    iso = d.isoformat()
    acta = leer(os.path.join(REPO, "consejo/actas", f"{iso}.md"))
    aud  = leer(os.path.join(REPO, "auditoria", f"{iso}.md"))
    inf  = leer(os.path.join(REPO, "presidencia/informes", f"{iso}.md"))
    props = {m: leer(os.path.join(REPO, f"ministerios/{m}/propuestas", f"{iso}.md"))
             for m in ["hacienda", "sanidad", "transicion-ecologica"]}
    kpis = {m: leer(os.path.join(REPO, f"ministerios/{m}/kpis.md")) for m in props}
    hay = acta or aud or any(props.values())
    if not hay: return ""

    bloques = [f'<div class="dia"><h2>{fecha_humana(d)}</h2>']

    # Propuestas de los ministros
    bloques.append('<div class="seccion"><h3>Propuestas de los ministros</h3><ul>')
    for m, txt in props.items():
        n = txt.count("## Propuesta")
        if n:
            titulos = re.findall(r"## Propuesta \d+: (.+)", txt)
            for t in titulos[:2]:
                bloques.append(f"<li><b>{esc(m.capitalize())}</b> — {esc(t[:150])}</li>")
        if "## Reasignación presupuestaria" in txt or "Reasignación presupuestaria" in txt:
            bloques.append(f"<li><b>{esc(m)}</b>: 💶 reasignación presupuestaria propuesta</li>")
    bloques.append("</ul></div>")

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
        enlaces = re.findall(r"https?://\S+", inf)
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
    nuevo = re.sub(r"<!-- GENERADO.*?-->[\s\S]*?(?=<footer>)", "<!-- GENERADO -->" + cuerpo + "\n  ", plantilla, flags=re.S)
    # actualizar el aviso "pendiente" solo si no hay días
    open(os.path.join(REPO, "docs/index.html"), "w", encoding="utf-8").write(nuevo)
    print("OK, días renderizados:", len(dias))

if __name__ == "__main__":
    main()
