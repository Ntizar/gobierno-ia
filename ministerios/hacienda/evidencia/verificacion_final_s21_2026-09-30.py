# -*- coding: utf-8 -*-
"""VERIFICACION FINAL de la sesion 21/30 (2026-09-30). Comprueba, byte a byte, que en los tres
ficheros tocados (agenda, kpis, diario) lo unico anadido es lo mio y que nada previo se ha
perdido, ademas de que la ley insignia sigue intacta."""
import io, hashlib, subprocess, os

W = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda"
ok_all = True

def sha(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()

def integridad(nombre, path, bak, quitar):
    """quitar(lineas) -> lista sin mis lineas; debe devolver el fichero previo exacto."""
    global ok_all
    cur = io.open(path, encoding="utf-8", newline="").read()
    prev = io.open(bak, encoding="utf-8", newline="").read()
    rest = quitar(cur)
    ok = (rest == prev)
    ok_all = ok_all and ok
    print("%-8s %s | previo %s | reconstruido %s" % (
        nombre, "OK" if ok else "FALLO",
        hashlib.sha256(prev.encode("utf-8")).hexdigest()[:16],
        hashlib.sha256(rest.encode("utf-8")).hexdigest()[:16]))
    return ok

# --- KPIs: quitar mis dos filas ---
integridad("KPIs", W + "/kpis.md", W + "/kpis.md.bak-2026-09-30",
           lambda s: "\n".join(l for l in s.split("\n") if not l.startswith("| - 2026-09-30")))

# --- AGENDA: quitar mi entrada. OJO: el contenido original empieza por "|# Agenda — 2026-10-13"
#     (artefacto del fichero heredado), asi que el corte debe buscar "|# Agenda" o "\n# Agenda".
def quita_agenda(s):
    i = s.find("# Agenda — 2026-09-30 — Hacienda\n")
    assert i == 0, "mi entrada no esta al principio"
    j = s.find("\n|# Agenda")
    if j < 0:
        j = s.find("\n# Agenda")
    return s[j + 1:]
integridad("AGENDA", W + "/agenda.md", W + "/agenda.md.bak-2026-09-30", quita_agenda)

# --- DIARIO: quitar mi entrada de hoy (cabecera con parentesis hasta la siguiente) ---
def quita_diario(s):
    i = s.find("## 2026-09-30 (noche, al cerrar la jornada")
    j = s.find("\n## ", i + 10)
    return s[:i] + s[j + 1:]
integridad("DIARIO", W + "/diario.md", W + "/diario.md.bak-2026-09-30", quita_diario)

# --- LEY INSIGNIA ---
ley = W + "/leyes/BOE-A-2003-23186.md"
raw = io.open(ley, "rb").read().decode("utf-8")
h = sha(ley)
bloques = raw.count("\n## [")
print("\nLEY  sha256 %s | %d palabras | %d bloques | coincide con d0b7ef22: %s" % (
    h[:16], len(raw.split()), bloques, h.startswith("d0b7ef22")))
ok_all = ok_all and h.startswith("d0b7ef22") and len(raw.split()) == 131823 and bloques == 335

# --- ficheros que NO son mios y deben seguir como estaban ---
print("\nFicheros ajenos (no borrados ni sobrescritos):")
for f, esperado in [(W + "/propuestas/2026-09-30.proceso-automatico-0104.md",
                     "964e3a8f01b7726f1dbf45263bab6d62bcbcc664f93bb2afe68652175e90e37a")]:
    got = sha(f)
    ok = got == esperado
    ok_all = ok_all and ok
    print("  %s  %s" % ("OK " if ok else "FALLO", os.path.basename(f)))

# --- git: que leyes no aparezcan en el diff ---
r = subprocess.run(["git", "-C", r"C:/Users/d_ant/Projects/gobierno-ia", "status", "--porcelain",
                    "--", "ministerios/"], capture_output=True, text=True)
leyes_tocadas = [l for l in r.stdout.splitlines() if "/leyes/" in l]
rangos = [l for l in r.stdout.splitlines() if "propuestas/" in l and "leyes/" not in l]
print("\nGIT: leyes modificadas ->", leyes_tocadas if leyes_tocadas else "NINGUNA (correcto)")
ok_all = ok_all and not leyes_tocadas
# comprobacion de que el respaldo historico existe
assert os.path.exists(W + "/agenda.md.duplicado-2026-09-30"), "falta el estado defectuoso guardado"

print("\n=== RESULTADO GLOBAL:", "TODO VERIFICADO" if ok_all else "HAY UN FALLO", "===")
