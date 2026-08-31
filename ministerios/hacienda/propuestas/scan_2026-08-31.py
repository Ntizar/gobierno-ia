# Escaneo sha256 por bloque de la LGT (sesion 3, 2026-08-31)
import hashlib, json, re
src = open("leyes/BOE-A-2003-23186.md", encoding="utf-8").read()
blocks = re.split(r'\n(?=## \[a\d+\])', src)
done = {"a2", "a27", "a95", "a43", "a112"}
results = []
for b in blocks:
    m = re.match(r'## \[a(\d+)\]', b)
    if not m:
        continue
    aid = m.group(1)
    paras = [l.strip() for l in b.split('\n') if l.strip() and len(l.strip()) > 40 and not l.strip().startswith('## [')]
    seen, dup_words, dups = {}, 0, []
    for p in paras:
        key = hashlib.sha256(re.sub(r'\s+', ' ', p).encode()).hexdigest()
        if key in seen:
            seen[key] += 1
            dup_words += len(p.split())
            dups.append(p[:130])
        else:
            seen[key] = 1
    tw = sum(len(p.split()) for p in paras)
    if dup_words > 0 and aid not in done:
        results.append((dup_words, tw, aid, len(paras), dups))
results.sort(reverse=True)
for dw, tw, aid, np_, dups in results[:15]:
    print(f"[a{aid}] dup={dw} total={tw} ratio={dw/tw*100:.0f}% paras={np_} | {dups[0][:95] if dups else ''}")
json.dump([[f"a{r[2]}", r[0], r[1]] for r in results], open("propuestas/.dups_2026-08-31.json", "w"), ensure_ascii=False, indent=1)
print(f"\nRESTANTES con duplicados: {len(results)} | palabras dup restantes: {sum(r[0] for r in results)}")
