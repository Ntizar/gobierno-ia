# Cuenta palabras de cada párrafo del canon frente al bloque actual de la ley,
# para la justificación medida de las propuestas da11/da20 (sesión 15/30).
import re

canon = open("ministerios/hacienda/evidencia/boe_canonico_da11_da20_2026-09-22.txt", encoding="utf-8").read()
law = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", encoding="utf-8", newline="").read().replace("\r\n", "\n")

def seg(a, b):
    i = canon.find(a); j = canon.find(b, i + 1)
    return canon[i:j].strip()

c11 = seg("### da11:", "### da20:")
c20 = seg("### da20:", "\Z") if False else canon[canon.find("### da20:"):].split("\n", 1)[1].strip()
c20 = "\n".join(l for l in c20.splitlines() if l.strip() and not l.startswith((".", "Modificación", "Texto añadido")))

da11_act = law[law.find("## [daundecima]"):law.find("## [daduodecima]")]
da20_act = law[law.find("## [davigesima]"):law.find("## [davigesimoprimera]")]

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def parrafos(canon_block):
    return [p for p in canon_block.splitlines() if norm(p)]

print("== DA11: párrafos del canon y su presencia literal en el bloque actual ==")
miss11 = 0
for p in parrafos(c11):
    ok = norm(p) in norm(da11_act)
    w = len(p.split())
    if not ok: miss11 += w
    print(("OK " if ok else "FALTA "), w, "|", p[:70])
extra11 = [p for p in da11_act.splitlines() if p.strip() and p.strip() not in ("## [daundecima] Disposición adicional undécima","") and norm(p) not in norm(c11)]
print("-- en el actual y NO en el canon (derogado/residuo):")
for p in extra11:
    print("  SOBRA", len(p.split()), "|", p[:70])

print()
print("== DA20: párrafos del canon y su presencia literal en el bloque actual ==")
miss20 = 0
for p in parrafos(c20):
    ok = norm(p) in norm(da20_act)
    w = len(p.split())
    if not ok: miss20 += w
    print(("OK " if ok else "FALTA "), w, "|", p[:70])
extra20 = [p for p in da20_act.splitlines() if p.strip() and norm(p) not in norm(c20)]
print("-- en el actual y NO en el canon:")
for p in extra20:
    print("  SOBRA", len(p.split()), "|", p[:70])
print()
print("MISSING PALABRAS da11:", miss11, "| da20:", miss20)
