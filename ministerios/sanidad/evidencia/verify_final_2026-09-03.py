# -*- coding: utf-8 -*-
# Verificacion final 2026-09-03: ANTES (snapshot 09-03) vs DESPUES (fichero vivo)
import re, json, hashlib, unicodedata, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/sanidad"
def norm(s): return unicodedata.normalize("NFC", s.replace("\u00a0"," ").replace("\ufeff","").strip())
def h12(s): return hashlib.sha256(norm(s).encode()).hexdigest()[:12]
def blocks(ls):
    hs=[(i,m.group(1)) for i,l in enumerate(ls) for m in [re.match(r'^## \[(a\w+)\] (.*)$',l)] if m]
    out={}
    for k,(i,b) in enumerate(hs):
        j=hs[k+1][0] if k+1<len(hs) else len(ls)
        out.setdefault(b,[]).extend([norm(l) for l in ls[i+1:j] if norm(l)])
    return out
def dupw(ps):
    seen={}
    for p in ps: seen.setdefault(h12(p),[0,p])[0]+=1
    return sum((c-1)*len(p.split()) for c,p in seen.values())
A=blocks(open(r"C:/Users/d_ant/AppData/Local/Temp/ley_ANTES_2026-09-03.md",encoding="utf-8").read().splitlines())
D=blocks(open(BASE+"/leyes/BOE-A-1986-10499.md",encoding="utf-8").read().splitlines())
print("bloques ANTES/DESPUES:",len(A),len(D))
tot_a=sum(dupw(v) for v in A.values()); tot_d=sum(dupw(v) for v in D.values())
print("dup total ANTES/DESPUES:",tot_a,tot_d,"delta",tot_a-tot_d)
for b in ("aveinticinco","asetentaynueve"):
    wa=sum(len(p.split()) for p in A[b]); wd=sum(len(p.split()) for p in D[b])
    print(f"[{b}] dup {dupw(A[b])}->{dupw(D[b])}  palabras {wa}->{wd} (-{wa-wd})")
# que bloques han cambiado (regresiones fuera de los 2 objetivos)
changed=[b for b in A if A[b]!=D[b]]
print("bloques modificados:",changed)
# letras a) de las 21 siguen todas presentes
items=json.load(open(BASE+"/evidencia/a_restituir_completas_2026-09-01.json",encoding="utf-8"))
allp=[p for v in D.values() for p in v]
print("letras a) presentes:",sum(1 for it in items if norm(it['letra_a_BOE']) in allp),"/",len(items))
# Fidelidad: cada parrafo de los 2 bloques post-diff existe en BOE plano
plano={h12(l) for l in open(BASE+"/evidencia/boe_texto_plano.txt",encoding="utf-8") if norm(l)}
for b in ("aveinticinco","asetentaynueve"):
    ok=sum(1 for p in D[b] if h12(p) in plano)
    print(f"fidelidad {b}: {ok}/{len(D[b])} en BOE")
