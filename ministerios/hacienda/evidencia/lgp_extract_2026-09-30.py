import re, html, io, sys, json

p = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/ley47-2003-general-presupuestaria-BOE-A-2003-21614-consolidado-2026-09-28.html"
raw = open(p, encoding="utf-8", errors="replace").read()
txt = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S | re.I)
# keep block boundaries
txt = re.sub(r"</(p|div|li|br|h[1-6]|tr)>", "\n", txt, flags=re.I)
txt = re.sub(r"<br\s*/?>", "\n", txt, flags=re.I)
txt = re.sub(r"<[^>]+>", " ", txt)
txt = html.unescape(txt)
lines = [re.sub(r"[ \t\u00a0]+", " ", l).strip() for l in txt.split("\n")]
lines = [l for l in lines if l]
with open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/lgp_texto_limpio_2026-09-30.txt", "w", encoding="utf-8", newline="\n") as f:
    for i, l in enumerate(lines, 1):
        f.write(f"{i}\t{l}\n")

# locate article headers
idx = {}
for i, l in enumerate(lines, 1):
    m = re.match(r"^Artículo (\d+)\.\s*(.*)$", l)
    if m:
        n = int(m.group(1))
        if n not in idx:
            idx[n] = (i, m.group(2)[:90])
print("HEADERS encontrados:", len(idx))
targets = [42, 46, 47, 52, 58, 59, 60, 61, 62, 63, 64]
for n in targets:
    print(n, idx.get(n))
json.dump({str(k): v for k, v in idx.items()}, open(r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia/lgp_indice_arts_2026-09-30.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def art(n, extra=0):
    start = idx[n][0]
    nxt = min([v[0] for k, v in idx.items() if v[0] > start] or [start + 200])
    end = nxt + extra
    print("\n" + "=" * 100)
    for i in range(start, min(end, start + 140)):
        print(lines[i - 1])

for n in (52, 58, 60, 61, 62, 63):
    art(n)
