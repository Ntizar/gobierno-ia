# DA18 del BOE vivo (09-02): todos los <p> entre anclas con sha256 + clases
import re, io, sys, json, html as H, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open("../evidencia/boe_vivo_LGT_2026-09-02.html", encoding="utf-8", errors="replace").read()
i = raw.find('id="dadecimoctava"')
j = raw.find('id="dadecimonovena"', i + 10)
sec = raw[i:j]
out = []
for m in re.finditer(r'<(p|blockquote)[^>]*>(.*?)</\1>', sec, flags=re.S):
    cls = re.search(r'class="([^"]*)"', m.group(0))
    cls = cls.group(1) if cls else m.group(1)
    t = H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
    t = re.sub(r"\s+", " ", t).strip()
    out.append({"class": cls, "sha256": hashlib.sha256(t.encode()).hexdigest(), "text": t})
print("parrafos:", len(out))
for k, p in enumerate(out):
    print(k, "|", p["class"], "|", p["sha256"][:12], "|", p["text"][:95])
json.dump(out, open("../evidencia/da18_boe_full_2026-09-02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
