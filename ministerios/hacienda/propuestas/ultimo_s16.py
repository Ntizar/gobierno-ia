# Ultima comprobacion s16: octava vs df_canon_limpio (palabras normalizadas),
# unicidad de rotulos ^## [dfxx], y entradas F1 de las tres DF.
import os, sys, io, re, json, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
EVID = os.path.join(BASE, "ministerios/hacienda/evidencia")
LEY = os.path.join(BASE, "ministerios/hacienda/leyes/BOE-A-2003-23186.md")

def key(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = t.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t).strip()

# canon limpio
raw = open(os.path.join(EVID, "df_canon_limpio_s16_2026-09-24.txt"), encoding="utf-8").read()
idx = {}
for m in re.finditer(r"(?m)^Disposición final (quinta|sexta|octava)\.", raw):
    idx[m.group(1)] = m.start()
order = sorted(idx.items(), key=lambda kv: kv[1])
for i, (nom, st) in enumerate(order):
    en = len(raw)
    for _, st2 in order:
        if st2 > st and st2 < en:
            en = st2
    canon = key(raw[st:en])
    pr = open(os.path.join(EVID, "bloque_propuesto_df" + nom + "_2026-09-24.txt"), encoding="utf-8").read()
    body = key(pr.split("\n", 2)[2])
    same = canon.startswith(body[:80]) and body in (canon + " ") or (body and canon.find(body) >= 0)
    # comparacion directa de palabras
    a, b = canon.split(" "), body.split(" ")
    n = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
    print(nom, "| canon w=", len(a), "| prop cuerpo w=", len(b), "| pal dispares =", n, "| prop incluido en canon:", canon.find(body) >= 0 or body.find(canon) >= 0)

# unicidad de rotulos
ley = open(LEY, encoding="utf-8").read()
for s in ["dfquinta", "dfsexta", "dfoctava"]:
    print("rotulo", s, "en ley:", len(re.findall(r"(?m)^## \[" + s + r"\]", ley)))

# entradas F1
inv = json.load(open(os.path.join(EVID, "inventario_f1_vivo_s15_2026-09-23.json"), encoding="utf-8"))
def walk(o, path=""):
    if isinstance(o, dict):
        if any(re.search(r"df[_ ]?(quinta|sexta|octava)|final (quinta|sexta|octava)", json.dumps(o, ensure_ascii=False), re.I) for _ in [1]) and len(json.dumps(o)) < 800:
            yield json.dumps(o, ensure_ascii=False)
        else:
            for k, v in o.items():
                yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[%d]" % i)
n = 0
for hit in walk(inv):
    print("F1:", hit[:350]); n += 1
print("entradas F1 df*:", n)
