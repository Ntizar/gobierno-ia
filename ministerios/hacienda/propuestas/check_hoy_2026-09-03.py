# Comprobar precondicion DA18 y extraer tramo F1 pendiente del manifiesto masivo
import re, json, hashlib, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = "leyes/BOE-A-2003-23186.md"
txt = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")
def norm(p): return re.sub(r"\s+", " ", p).strip()

# 1) Precondicion del diff DA18
m = re.search(r"^(## \[dadecimoctava\][^\n]*\n)(.*?)(?=^## \[)", txt, flags=re.S | re.M)
assert m, "bloque [dadecimoctava] no encontrado"
body = m.group(2)
paras = [norm(p) for p in body.split("\n\n") if norm(p)]
cur = hashlib.sha256(norm(body).encode()).hexdigest()
print("== PRECONDICION DA18 ==")
print("sha256(norm) bloque actual:", cur)
print("esperado (verificado 09-02): 574ad589ebb449387923d02ebdc7f42d6c7a2d621c896af8cf6b9290da6f6bdc")
print("MATCH:", cur == "574ad589ebb449387923d02ebdc7f42d6c7a2d621c896af8cf6b9290da6f6bdc")
print("parrafos bloque actual:", len(paras), "palabras:", sum(len(p.split()) for p in paras))

# 2) Bloque propuesto: hash y conteo (lectura robusta: todo lo que sigue al encabezado hasta EOF)
prop = open("evidencia/reparacion_DA18_bloque_propuesto_2026-09-02.md", encoding="utf-8").read()
lines = prop.split("\n")
hidx = next(i for i, l in enumerate(lines) if l.startswith("## [dadecimoctava]"))
pbody = "\n".join(lines[hidx + 1:])
pparas = [norm(p) for p in pbody.split("\n\n") if norm(p)]
print("\n== BLOQUE PROPUESTO (evidencia) ==")
print("sha256(norm):", hashlib.sha256(norm(pbody).encode()).hexdigest())
print("esperado: 11c84ad13a5dc5f9b452456bc5fff1bca87e155ba8164ae18e414a03d6fab889")
print("parrafos:", len(pparas), "palabras:", sum(len(p.split()) for p in pparas))
for i, p in enumerate(pparas):
    print(f"  [{i+1}] {p[:90]}...")

# 3) Manifiesto: estructura y tramos F1 pendientes
d = json.load(open("evidencia/MANIFIESTO_MASIVO_LGT_2026-09-02.json", encoding="utf-8"))
print("\n== MANIFIESTO: claves de nivel 1 ==")
print(list(d.keys()))
# buscar lista de bloques con F1
def find_f1(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, list) and v and isinstance(v[0], dict) and any("f1" in str(x).lower() or "contenido_perdido" in str(x).lower() for x in v[:1]):
                hits.append((path + "/" + k, len(v)))
            elif isinstance(v, (dict, list)):
                hits += find_f1(v, path + "/" + k)
    elif isinstance(obj, list):
        for i, x in enumerate(obj[:3]):
            if isinstance(x, (dict, list)):
                hits += find_f1(x, f"{path}[{i}]")
    return hits
print("listas con pinta de F1:", find_f1(d))
if "bloques" in d:
    b = d["bloques"]
    print("tipo bloques:", type(b), len(b))
    if isinstance(b, dict):
        k0 = list(b.keys())[0]
        print("ejemplo clave:", k0, "->", json.dumps(b[k0], ensure_ascii=False)[:400])
    elif isinstance(b, list):
        print("ejemplo:", json.dumps(b[0], ensure_ascii=False)[:400])
