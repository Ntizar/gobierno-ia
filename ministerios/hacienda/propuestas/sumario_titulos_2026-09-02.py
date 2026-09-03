# Titulos completos de BOE-A-2026-18437 y 18456 (Hacienda) en el sumario del 02-09
import re, io, sys, html as H
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
raw = open(r"C:\Users\d_ant\AppData\Local\Temp\boe_0902.html", encoding="utf-8", errors="replace").read()
for pid in ("BOE-A-2026-18437", "BOE-A-2026-18456"):
    for m in re.finditer(r'<a[^>]*href="[^"]*' + pid + r'\.pdf"[^>]*>(.*?)</a>', raw, flags=re.S):
        t = H.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
        t = re.sub(r"\s+", " ", t).strip()
        print(pid, "::", t[:260])
# y el heading H3 cerca
i = raw.find(pid := "BOE-A-2026-18437")
seg = raw[max(0,i-3000):i+200]
for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", seg, flags=re.S):
    print("H3:", H.unescape(re.sub(r"<[^>]+>"," ",m.group(1))).strip()[:200])
