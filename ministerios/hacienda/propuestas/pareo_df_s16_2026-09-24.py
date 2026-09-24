# Pareo s16: bloques DF 1ª-6ª vivos vs canon BOE extraído hoy.
# Hash convención Auditor: sha256 del bloque completo con su cabecera, LF, sin saltos finales.
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
raw = open(BASE + r"/ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")

def auditor_hash(block_text):
    b = block_text.strip("\n").replace("\r\n", "\n").encode("utf-8")
    return hashlib.sha256(b).hexdigest()

# partir en bloques ## [slug]
parts = re.split(r"(?m)^(?=## \[)", raw)
blocks = {}
for p in parts:
    m = re.match(r"## \[([a-z0-9\-]+)\]", p)
    if m:
        blocks.setdefault(m.group(1), []).append(p.rstrip("\n"))

# canon
canon_raw = open(BASE + r"/ministerios/hacienda/evidencia/boe_canonico_df_2026-09-24.txt", encoding="utf-8").read()
canon = {}
for m in re.finditer(r"#### BOE consolidado — Disposición final (\w+) \(Ley 58/2003[^)]*\)\n(.*?)(?=\n\n####|\Z)", canon_raw, re.S):
    canon[m.group(1)] = m.group(2).strip()

WS = re.compile(r"\S+")
for slug, orden in [("dfprimera", "primera"), ("dfsegunda", "segunda"), ("dftercera", "tercera"),
                    ("dfcuarta", "cuarta"), ("dfquinta", "quinta"), ("dfsexta", "sexta")]:
    bs = blocks.get(slug, [])
    print("=" * 78)
    print("BLOQUE [" + slug + "] — copias en vivo:", len(bs))
    for i, b in enumerate(bs):
        print("  copia", i, "| palabras:", len(WS.findall(b)), "| hash Auditor:", auditor_hash(b))
    c = canon.get(orden, "")
    print("  CANON palabras:", len(WS.findall(c)), "| hash Auditor del canon:", auditor_hash(c))
    if bs:
        b0 = bs[0]
        # ¿cada línea del canon está en el bloque vivo? (comparación por fragmentos de 60 chars normalizados)
        def norm(s):
            return re.sub(r"\s+", " ", s)
        live_norm = norm(b0)
        canon_norm = norm(c)
        # piezas del canon ausentes en vivo: trocear canon en frases de ~80 chars en límite de palabra
        ausentes = []
        for k in range(0, max(0, len(canon_norm) - 80 + 1), 80):
            frag = canon_norm[k:k + 80]
            if frag not in live_norm:
                ausentes.append(frag)
        print("  fragmentos canon (80c) NO presentes en bloque vivo:", len(ausentes), "de", (len(canon_norm) + 79) // 80)
        for a in ausentes[:6]:
            print("    FALTA:", a[:80])
