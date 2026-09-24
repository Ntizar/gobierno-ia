# scan dedup 24-09 + verificacion fuentes art.16/21 + colas agenda/kpis
import hashlib, re, io, sys
BASE = "C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad/"
raw = open(BASE+"leyes/BOE-A-1986-10499.md","rb").read().decode("utf-8")
text = raw.replace("\r\n","\n")
lines = text.split("\n")
# trocear bloques
starts = [i for i,l in enumerate(lines) if re.match(r"^## \[", l)]
blocks = {}
for k,s in enumerate(starts):
    e = starts[k+1] if k+1 < len(starts) else len(lines)
    m = re.match(r"^## \[([^\]]+)\]", lines[s])
    if not m: continue
    tag = m.group(1)
    body = [l for l in lines[s:e] if l.strip()]
    blocks[tag] = "\n".join(lines[s:e]).rstrip("\n")

# scan: lineas duplicadas DENTRO de cada bloque (cuerpo, excluyendo el rotulo ## [..])
total_words = 0; dirty = []
for tag, b in blocks.items():
    bl = [l.strip() for l in b.split("\n")[1:] if l.strip() and not l.strip().startswith("<strong>")]
    seen = {}
    for l in bl:
        seen[l] = seen.get(l,0)+1
    dup = {l:c for l,c in seen.items() if c>1 and len(l.split())>3}
    if dup:
        w = sum((c-1)*len(l.split()) for l,c in dup.items())
        total_words += w
        dirty.append((tag, sum(c-1 for c in dup.values()), w, list(dup.keys())[:2]))
print("BLOQUES TOTALES:", len(blocks))
print("PALABRAS DUPLICADAS HOY:", total_words, "EN", len(dirty), "BLOQUES")
for t,d,w,ex in dirty:
    print(f"  [{t}] extra={d} words_extra={w} ej={ex[0][:60]!r}")

def sha(tag):
    return hashlib.sha256(blocks[tag].encode("utf-8")).hexdigest()
for t in ["adieciseis","aveintiuno","atreintayseis","aochentaycuatro"]:
    if t in blocks:
        bl = blocks[t].split("\n")
        l0 = lines.index(bl[0])
        print(f"HASH [{t}] bloque l.{l0+1}-{l0+len(bl)}: {sha(t)} (pal={len(' '.join(bl).split())})")
        if t=="adieciseis":
            print("----BLOQUE adieciseis----"); print(blocks[t][:1800])

plan = open(BASE+"evidencia/boe_texto_plano.txt","rb").read().decode("utf-8",errors="replace")
i = plan.find("Artículo dieciséis")
print("----PLANO art16----")
print(plan[i:i+1500].replace("\r",""))
print("Cartilla en plano:", plan.lower().count("cartilla"))
html = open(BASE+"evidencia/boe_consolidado_BOE-A-1986-10499.html","rb").read().decode("utf-8",errors="replace")
print("Cartilla en html:", html.lower().count("cartilla"), "| 'sistema de información de las listas' html:", html.lower().count("sistema de informaci\u00f3n de las listas"))
j = html.find("Artículo dieciséis")
print("----HTML art16 (texto plano)----")
seg = re.sub(r"<[^>]+>"," ",html[j:j+2200])
print(re.sub(r"\s+"," ",seg)[:900])
k = text.find("Sanidad y Consumo")
occ = [i+1 for i,l in enumerate(lines) if "Sanidad y Consumo" in l]
print("Ocur. 'Sanidad y Consumo' en ley (lineas):", occ[:30])
print("Ocur. plano 1986 'Sanidad y Consumo':", plan.count("Sanidad y Consumo"), "| html consolidado:", html.count("Sanidad y Consumo"))
ag = open(BASE+"agenda.md","rb").read().decode("utf-8")
print("----AGENDA TAIL----"); print(ag[-900:])
kp = open(BASE+"kpis.md","rb").read().decode("utf-8")
print("----KPIS TAIL----"); print(kp[-1000:])
