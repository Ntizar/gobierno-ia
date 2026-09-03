# DA18 completa: TODOS los divs de texto entre anclas del BOE vivo (09-02), con sha256
import re, io, sys, json, html as H, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open("../evidencia/boe_vivo_LGT_2026-09-02.html", encoding="utf-8", errors="replace").read()
i = raw.find('id="dadecimoctava"')
j = raw.find('id="dadecimonovena"', i + 10)
sec = raw[i:j]
divs = re.findall(r"<div\b[^>]*>(.*?)</div>", sec, flags=re.S)
pars = []
for d in divs:
    cls = ""
    t = re.sub(r"<[^>]+>", "", d).strip()
    t = H.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    if t:
        pars.append(t)
print("divs con texto:", len(pars))
for k, p in enumerate(pars):
    print(k, "|", hashlib.sha256(p.encode()).hexdigest()[:10], "|", p[:110])
json.dump(pars, open("../evidencia/da18_boe_full_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
