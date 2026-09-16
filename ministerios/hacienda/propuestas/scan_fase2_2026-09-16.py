# Escaneo Fase 2 2026-09-16: bloques de la LGT con rotulo repetido, numeracion repetida
# o parrafos literales duplicados, ordenados por palabras duplicadas. Solo lectura.
import re, json
from collections import Counter

SRC = "../leyes/BOE-A-2003-23186.md"
txt = open(SRC, encoding="utf-8").read()
lines = txt.splitlines(keepends=True)

hdr = [(i, m.group(1)) for i, l in enumerate(lines) if (m := re.match(r"^## \[([^\]]+)\]", l))]
hdr.append((len(lines), "EOF"))

def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()

rows = []
for k in range(len(hdr) - 1):
    i0, key = hdr[k]
    i1 = hdr[k + 1][0]
    body = "".join(lines[i0:i1])
    heads = [norm(l) for l in body.splitlines() if re.match(r"^(Art[íi]culo|Disposici[oó]n|Cap[íi]tulo|T[íi]tulo)\b", l)]
    dup_heads = len(heads) - len(set(heads))
    nums = [re.match(r"^(\d+)\.", l).group(1) for l in body.splitlines() if re.match(r"^\d+\. ", l)]
    cn = Counter(nums)
    dup_nums = sum(v - 1 for v in cn.values() if v > 1)
    paras = [norm(x) for x in re.split(r"\n\s*\n", body) if len(x.strip()) > 40]
    cp = Counter(paras)
    dup_words = sum(len(x.split()) * (v - 1) for x, v in cp.items() if v > 1)
    total_words = len(re.findall(r"\S+", body))
    if dup_heads or dup_nums or dup_words:
        rows.append(dict(bloque=key, lineas=f"{i0+1}-{i1}", palabras=total_words,
                         rot_dup=dup_heads, num_dup=dup_nums, palabras_dup=dup_words,
                         ratio=round(dup_words / max(total_words, 1), 3)))

rows.sort(key=lambda r: -r["palabras_dup"])
out = dict(fichero="BOE-A-2003-23186.md", fecha="2026-09-16",
           total_bloques_defecto=len(rows),
           sum_dup=sum(r["palabras_dup"] for r in rows),
           top=rows[:45])
json.dump(out, open("scan_fase2_2026-09-16.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows[:45]:
    print(f"{r['bloque']:>16} {r['lineas']:>12} pal={r['palabras']:>5} rotdup={r['rot_dup']:>2} numdup={r['num_dup']:>3} dup={r['palabras_dup']:>5} ratio={r['ratio']}")
