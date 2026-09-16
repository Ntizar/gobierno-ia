# Extrae del BOE consolidado archivado las secciones vigentes de los arts. 95 y 43
# para verificar contra ellas las propuestas de 2026-09-16.
import re, html, os

d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ministerios/hacienda
ev = os.path.join(d, "evidencia")
raw = open(os.path.join(ev, "boe_consolidado_BOE-A-2003-23186.html"),
           encoding="utf-8", errors="replace").read()
text = re.sub(r"<[^>]+>", "\n", raw)
text = html.unescape(text)
lines = [l.strip() for l in text.split("\n") if l.strip()]
full = "\n".join(lines)

i95 = full.find("Carácter reservado de los datos con trascendencia tributaria")
i96 = full.find("Artículo 96.", i95)
sec95 = full[i95:i96]
open(os.path.join(ev, "tmp_sec95.txt"), "w", encoding="utf-8").write(sec95)

i43 = full.find("Responsables subsidiarios")
i44 = full.find("Capacidad de obrar", i43)
sec43 = full[i43 - 60:i44]
open(os.path.join(ev, "tmp_sec43.txt"), "w", encoding="utf-8").write(sec43)

print("sec95 chars:", len(sec95), "words:", len(sec95.split()))
print("sec43 chars:", len(sec43), "words:", len(sec43.split()))
print("art56 mention in sec95:", "artículo 56" in sec95.lower())
print("149/150 in sec95:", "149" in sec95 and "150" in sec95)
print("representantes aduaneros in sec43:", "representantes aduaneros" in sec43)
print("agentes y comisionistas in sec43:", "agentes y comisionistas" in sec43)
