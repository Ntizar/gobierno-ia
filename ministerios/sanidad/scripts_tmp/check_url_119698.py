# Verifico el titular real de la URL usada en la agenda (no vale un 200: vale el título)
import urllib.request, re
url = 'https://www.consalud.es/politica/2026-09-23/jefes-servicio-quirurgicos-ramon-cajal-criterio-clinico-listas-espera_119698_100.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126'})
html = urllib.request.urlopen(req, timeout=25).read().decode('utf-8', 'replace')
m = re.search(r'<title>(.*?)</title>', html, re.S)
print('TITLE:', m.group(1).strip()[:160] if m else 'sin título')
m2 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
print('H1:', re.sub(r'<[^>]+>', '', m2.group(1)).strip()[:160] if m2 else 'sin h1')
m3 = re.search(r'"datePublished"\s*content="([^"]+)"', html)
print('FECHA:', m3.group(1) if m3 else '?')
