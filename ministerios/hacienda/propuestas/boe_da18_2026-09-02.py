# Extraer la DA18 real del BOE consolidado archivado (2ª tentativa: cuerpo por marcador de titulo)
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

boe = open("../evidencia/boe_consolidado_BOE-A-2003-23186.html", encoding="utf-8", errors="replace").read()
nb = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", boe.replace("\xa0", " ")))
oc = [m.start() for m in re.finditer("Disposición adicional decimoctava", nb)]
print("ocurrencias del rotulo DA18:", oc)
i = oc[-1] if oc else -1
j = nb.find("Disposición adicional decimonovena", i + 30)
print("inicio cuerpo:", i, "fin (DA19):", j)
seg = nb[i:j] if j > 0 else nb[i:i+20000]
print("palabras del bloque DA18 en BOE:", len(seg.split()))
print(seg[:12000])
