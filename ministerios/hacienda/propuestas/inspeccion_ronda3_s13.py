# -*- coding: utf-8 -*-
"""Sesion 13/30 - Ronda 3: inspeccion de estado de los bloques objetivo ANTES
de ejecutar (regla: prohibido re-aplicar un diff ya ejecutado)."""
import io, os, re, hashlib, json

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MD = os.path.join(RAIZ, "ministerios/hacienda/leyes/BOE-A-2003-23186.md")
CANON = os.path.join(RAIZ, "ministerios/hacienda/evidencia/boe_canonico_a93_a101_a187_2026-09-21.txt")

raw = io.open(MD, "rb").read()
print("file_bytes", len(raw), "has_CRLF", b"\r\n" in raw, "bare_LF", raw.replace(b"\r\n", b"").count(b"\n"))
text = raw.decode("utf-8")
lines = text.split("\r\n") if "\r\n" in text else text.split("\n")

def sha(b): return hashlib.sha256(b).hexdigest()

cab = [i for i, l in enumerate(lines) if l.startswith("## [")]
idx = {}
for n, i in enumerate(cab):
    m = re.match(r"^##\s+\[([^\]]+)\]", lines[i])
    idx[m.group(1)] = (i, cab[n+1] if n+1 < len(cab) else len(lines))

for slug in ("a12", "a93", "a101", "a187"):
    i, j = idx[slug]
    body = "\r\n".join(lines[i+1:j]) if "\r\n" in text else "\n".join(lines[i+1:j])
    words = len(re.findall(r"\S+", re.sub(r"^##.*$", "", "\n".join(lines[i:j]))))
    rot = len(re.findall(r"(?m)^Art[íi]culo\s+\d+\.", body))
    print("="*70)
    print(f"[{slug}] lineas {i+1}-{j} (cabecera en {i+1}), rotulos_articulo={rot}, palabras={words}")
    print("  sha_cuerpo=", sha(body.encode("utf-8")))
    print("  cabecera:", repr(lines[i]))
    # primeras 3 y ultimas 3 lineas no vacías
    nl = [l for l in body.split("\r\n" if "\r\n" in text else "\n") if l.strip()]
    print("  --- primeras 4:")
    for l in nl[:4]: print("   ", l[:160])
    print("  --- ultimas 4:")
    for l in nl[-4:]: print("   ", l[:160])

# canon: secciones y hashes
can = io.open(CANON, "r", encoding="utf-8").read().replace("\r\n", "\n")
secs = re.split(r"(?m)^=+\r?$", can)
print("="*70)
print("CANON secciones:")
for s in re.finditer(r"## \[(a\d+)\][^\n]*\npalabras: (\d+) \| sha256: ([0-9a-f]+)\n(.*?)(?=\n=+|\Z)", can, re.S):
    slug, w, h, body = s.group(1), int(s.group(2)), s.group(3), s.group(4).rstrip("\n")
    blines = body.split("\n")
    print(f"  [{slug}] palabras_declaradas={w} sha_declarado={h[:16]} sha_recalculado={sha(body.encode('utf-8'))[:16]} primera_linea={blines[0][:80]!r} ultima={blines[-1][:80]!r} n_parrafos={sum(1 for l in blines if l.strip())}")
