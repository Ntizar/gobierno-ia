import hashlib
raw = open("leyes/BOE-A-2021-8447.md", "rb").read()
print("SHA_BYTES_FINAL:", hashlib.sha256(raw).hexdigest())
import re
t = raw.decode("utf-8")
print("PALABRAS:", len(re.findall(r"\S+", t)), "| LINEAS:", t.count("\r\n") + 1, "| BYTES:", len(raw))
b = open("leyes/BOE-A-2021-8447.md.bak-2026-09-03", "rb").read()
print("SHA_BACKUP:", hashlib.sha256(b).hexdigest())
print("ROTULOS_art15:", len(re.findall(r"^Artículo 15\.", t, re.M)))
