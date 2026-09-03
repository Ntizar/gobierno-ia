# Sesion 5 — reparacion de la pasada 1: las 5 letras «a)» de SEGUNDA lista dentro
# del mismo bloque (la busqueda del primer 'b)' del bloque las dejo atras).
# Se anclan por matching de la linea 'b)' inmediatamente posterior en el BOE,
# como hacia tmp_verif_a.py de la sesion 3.
import hashlib, json, re, shutil, sys

LEY = "leyes/BOE-A-2021-8447.md"
raw = open(LEY, "rb").read()
sha_before = hashlib.sha256(raw).hexdigest()
NL = "\r\n" if "\r\n" in raw.decode("utf-8") else "\n"
lines = raw.decode("utf-8").split(NL)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
wc = lambda s: len(re.findall(r"\S+", s))

# BOE como lista de lineas normalizadas
import html
h = html.unescape(re.sub(r"<[^>]+>", "\n", open("evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html", encoding="utf-8").read()))
hl = [norm(x) for x in h.split("\n") if norm(x)]

vf = json.load(open("evidencia/verificacion_fidelidad_BOE_2026-09-01.json", encoding="utf-8"))
reposet = set(norm(l) for l in lines if l.strip())
pend = [r for r in vf if r.get("repo") and norm(r["texto_a"]) not in reposet]
print("pendientes:", len(pend))
hechas, pal = 0, 0
for r in pend:
    a = norm(r["texto_a"])
    # en el BOE: la linea 'a)' va seguida (en 1-3 lineas) por su 'b)' — localizar el par
    idx = [j for j, x in enumerate(hl) if x == a and (j + 1 < len(hl) and hl[j + 1].startswith("b) ")
           or j + 2 < len(hl) and hl[j + 2].startswith("b) "))]
    if not idx:
        print("SIN ANCLA:", a[:60]); continue
    # la b) siguiente en el BOE
    j = idx[0]
    b = next(hl[k] for k in range(j + 1, j + 4) if hl[k].startswith("b) "))
    cand = [i for i, l in enumerate(lines) if norm(l) == b]
    if len(cand) != 1:
        print("ANCLA b) ambigua/ausente:", b[:60], cand); continue
    i = cand[0]
    if lines[i - 1].strip().startswith("a)"):
        print("ya presente en segunda pasada:", a[:40]); continue
    lines.insert(i, a)
    hechas += 1; pal += wc(a)
print("INSERTADAS 2a pasada:", hechas, "palabras:", pal)
sha_after = hashlib.sha256(NL.join(lines).encode("utf-8")).hexdigest()
open(LEY, "wb").write(NL.join(lines).encode("utf-8"))
# re-test
lines2 = open(LEY, "rb").read().decode("utf-8").split(NL)
faltan = []
for i, l in enumerate(lines2):
    if l.strip().startswith("b) "):
        prev = "\n".join(lines2[max(0, i - 5):i])
        if not re.search(r"^a\) ", prev, re.M):
            faltan.append(i + 1)
print("LISTAS_SIN_A tras reparacion:", len(faltan), faltan)
print("SHA_ANTES:", sha_before); print("SHA_DESPUES:", hashlib.sha256(open(LEY,'rb').read()).hexdigest())
m = json.load(open("evidencia/manifiesto_ejecucion_2026-09-03.json", encoding="utf-8"))
m["reparacion_segunda_pasada"] = {"insertadas": hechas, "palabras": pal, "sha_antes": sha_before,
    "sha_despues": hashlib.sha256(open(LEY, 'rb').read()).hexdigest(),
    "listas_sin_a_restantes": len(faltan)}
m["sha256_despues"] = m["reparacion_segunda_pasada"]["sha_despues"]
json.dump(m, open("evidencia/manifiesto_ejecucion_2026-09-03.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
