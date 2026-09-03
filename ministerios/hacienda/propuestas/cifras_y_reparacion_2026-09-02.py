# Cifras cuadradas para la taxonomia firmada + proyecto de reparacion DA18 (hash por parrafo)
import re, io, sys, json, hashlib, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def norm(p): return re.sub(r"\s+", " ", p).strip()
def wc(s): return len(s.split())
def shaci(s): return hashlib.sha256(norm(s).casefold().encode()).hexdigest()

manif = json.load(open("../evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
fidel = manif["casos_fidelidad"]
# bloques distintos por categoria
for v in ("contenido_perdido", "no_localizable_en_bloque_BOE", "solo_marca_perdida", "BOE_sin_a_legitimo"):
    cs = [r for r in fidel if r["v"] == v]
    bl = sorted(set(r["bloque"] for r in cs))
    print(v, "| casos:", len(cs), "| bloques distintos:", len(bl), "| palabras:", sum(int(r.get("palabras") or 0) for r in cs))
    if v == "contenido_perdido":
        print("   bloques:", bl[:20], "..." if len(bl) > 20 else "")
# palabras aun ausentes hoy: casos cuyo sha256_texto no esta en el bloque hoy
bloques = manif["bloques"]
aun = [r for r in fidel if r["v"] == "contenido_perdido" and r["sha256_texto"] not in bloques.get(r["bloque"], {}).get("hashes_parrafo", [])]
ya = [r for r in fidel if r["v"] == "contenido_perdido"]
print("contenido_perdido aun ausente hoy:", len(aun), "casos | palabras:", sum(int(r.get("palabras") or 0) for r in aun))
print("recuperadas desde el test (ejecutadas 09-01):", len(ya) - len(aun))
print("TOTAL casos:", len(fidel), "| bloques con cualquier defecto:", len(set(r["bloque"] for r in fidel)))
# letras_a json: 139 registros, para cuadrar el titular del acta
la = json.load(open("../evidencia/fidelidad_letras_a_2026-09-01.json", encoding="utf-8"))
print("letras_a registros:", len(la), "| bloques:", len(set(r["bloque"] for r in la)), "| en repo hoy:", sum(1 for r in la if r["contenido_en_repo"]))

# ---- reparacion DA18: bloque nuevo segun BOE consolidado ----
boe = json.load(open("../evidencia/da18_boe_full_2026-09-02.json", encoding="utf-8"))
legales = [p["text"] for p in boe if p["class"] in ("parrafo", "parrafo_2")]
notas = [p["text"] for p in boe if p["class"] in ("nota_pie", "p", "pie_unico")]
titulo = "Disposición adicional decimoctava. Obligación de información sobre bienes y derechos situados en el extranjero."
nuevo_body = "\n\n".join(legales + notas)
print("\nDA18 BOE: legales", len(legales), "| notas", len(notas), "| palabras legales:", sum(wc(t) for t in legales), "| palabras notas:", sum(wc(t) for t in notas))
txt = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"^## \[dadecimoctava\][^\n]*\n(.*?)(?=^## \[)", txt, flags=re.S | re.M)
body_old = m.group(1)
print("DA18 repo hoy: palabras:", wc(body_old), "| parrafos:", len([p for p in re.split(r"\n\s*\n", body_old) if norm(p)]))
# parrafo a) que falta en el repo
falta = [t for t in legales if t.startswith("a)")]
print("parrafo a) a restituir:", len(falta), "| palabras:", sum(wc(t) for t in falta))
# huellas
print("\nSHA-256 del bloque reparado (norm):", hashlib.sha256(norm(nuevo_body).encode()).hexdigest())
for i, t in enumerate(legales + notas):
    print(i, hashlib.sha256(norm(t).encode()).hexdigest()[:16], wc(t), "|", t[:70])
