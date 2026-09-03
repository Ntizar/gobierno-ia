# Volcado con indices de los parrafos de [dadecimoctava] para diseñar la reparacion
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open("../leyes/BOE-A-2003-23186.md", encoding="utf-8").read().replace("\r\n", "\n")
blocks = re.split(r"\n(?=## \[)", src)
b = next(x for x in blocks if x.startswith("## [dadecimoctava]"))
for i, l in enumerate(b.split("\n")):
    if l.strip():
        print(f"{i:02d}|{l[:165]}")
