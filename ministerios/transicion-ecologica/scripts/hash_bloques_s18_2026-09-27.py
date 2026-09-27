"""Sesión 18 (2026-09-27): medición reproducible de hashes por bloque para los manifiestos.

Convención UNICA y declarada:
  - fichero leído en modo texto UTF-8 (Python normaliza CRLF -> LF, como en todas las sesiones);
  - bloque = desde la línea del rótulo «## [nombre]» hasta la línea anterior al siguiente
    rótulo «## [», con los saltos de línea finales eliminados;
  - hash = sha256 hex de ese texto, unido con LF, codificado UTF-8;
  - palabras = len(texto.split()) (equivale a wc -w).

Uso:  python hash_bloques_s18_2026-09-27.py [ruta_fichero]
      (por defecto, la ley 8447 del ministerio)
"""
import hashlib
import sys

P = sys.argv[1] if len(sys.argv) > 1 else "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"


def blocks_from(raw: str):
    lines = raw.split("\n")
    marks = [i for i, l in enumerate(lines) if l.startswith("## [")]
    out = {}
    for k, i in enumerate(marks):
        j = marks[k + 1] if k + 1 < len(marks) else len(lines)
        name = lines[i].split("]")[0][4:]
        body = "\n".join(lines[i:j]).rstrip("\n")
        out[name] = body
    return out


for path in [P, P + ".bak-2026-09-27"]:
    raw = open(path, encoding="utf-8").read()
    bs = blocks_from(raw)
    print(f"\n== {path} | bloques={len(bs)} | palabras={len(raw.split())}")
    for name in ["a1-6", "a1-7", "da-2"]:
        if name in bs:
            h = hashlib.sha256(bs[name].encode("utf-8")).hexdigest()
            print(f"  {name}: sha256={h} palabras={len(bs[name].split())}")
