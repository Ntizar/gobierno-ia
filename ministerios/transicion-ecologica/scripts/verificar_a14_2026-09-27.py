import hashlib

P = "C:/Users/d_ant/Projects/gobierno-ia/ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
raw = open(P, encoding="utf-8").read()
lines = raw.split("\n")
b = "\n".join(lines[361:398]).strip("\n")
print("sha256 [a14] vivo hoy:", hashlib.sha256(b.encode("utf-8")).hexdigest())
print("palabras:", len(b.split()))
