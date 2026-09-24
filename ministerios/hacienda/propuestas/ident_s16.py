# Prueba de identidad en palabras (ignora saltos de linea del canon HTML).
import os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
EVID = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"

raw = open(os.path.join(EVID, "boe_canonico_df_2026-09-24.txt"), encoding="utf-8").read()
parts = re.split(r"(?m)^#### BOE consolidado — Disposición final (\w+)[^\n]*\n", raw)
canon = {parts[i]: parts[i+1] for i in range(1, len(parts)-1, 2)}

def key(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = t.replace("\u00a0", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()

for nom, slug in [("quinta","dfquinta"),("sexta","dfsexta"),("octava","dfoctava")]:
    c = canon.get(nom)
    pr = open(os.path.join(EVID, "bloque_propuesto_"+slug+"_2026-09-24.txt"), encoding="utf-8").read()
    body = pr.split("\n", 2)[2] if len(pr.split("\n",2)) > 2 else ""
    if c is None:
        print(slug, "SIN CANON en este fichero")
        continue
    ck, bk = key(c), key(body)
    print(slug, "IDENTICO en palabras:", ck == bk, "| canon w=", len(ck.split()), "prop w=", len(bk.split()))
    if ck != bk:
        a, b = ck.split(" "), bk.split(" ")
        k = next((i for i in range(min(len(a),len(b))) if a[i]!=b[i]), min(len(a),len(b)))
        print("  primera palabra distinta @", k, "| canon:", " ".join(a[max(0,k-6):k+8]))
        print("                        | prop :", " ".join(b[max(0,k-6):k+8]))
