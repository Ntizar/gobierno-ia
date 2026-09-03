# DA18 del BOE vivo: todos los divs entre anclas (sin marcador de corte) + sha256 por parrafo
import re, io, sys, json, html as H, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open("../evidencia/boe_vivo_LGT_2026-09-02.html", encoding="utf-8", errors="replace").read()
i = raw.find('id="dadecimoctava"')
j = raw.find('id="dadecimonovena"', i + 10)
sec = raw[i:j]
# quitar la barra lateral de "versiones/otras disposiciones" si existe: cortar en el primer div 'texto consolidado'
# estrategia: solo divs cuyo class sea de texto: 'paragraph' o sin class, ignorar nav/list
divs = re.findall(r"<div\b[^>]*>(.*?)</div>", sec, flags=re.S)
out = []
for d in divs:
    cls_m = re.match(r'<div\b[^>]*class="([^"]*)"', d)
    cls = cls_m.group(1) if cls_m else ""
    t = H.unescape(re.sub(r"<[^>]+>", "", d)).strip()
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        continue
    if cls and not re.search(r"parrafo|texto|content|normal", cls, re.I):
        # conserva igualmente si empieza por patron legal
        if not re.match(r"^(Disposición|\d\.|[a-d]\)|Las |Constituyen|También|A los|La sanción|Serán)", t):
            continue
    out.append({"class": cls, "sha256": hashlib.sha256(t.encode()).hexdigest(), "text": t})
print("parrafos:", len(out))
for k, p in enumerate(out):
    print(k, "|", p["class"], "|", p["sha256"][:10], "|", p["text"][:100])
json.dump(out, open("../evidencia/da18_boe_full_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
