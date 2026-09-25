# Manifiesto de evidencia de la sesión 17 (25-09-2026) — no se ejecuta NINGÚN diff en la ley
import hashlib, json, os

ev = r"C:/Users/d_ant/Projects/gobierno-ia/ministerios/hacienda/evidencia"
ley = os.path.join(os.path.dirname(ev), "leyes", "BOE-A-2003-23186.md")

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

files = ["bloque_vivo_a229_2026-09-25.txt", "bloque_propuesto_a229_2026-09-25.txt",
         "bloque_vivo_a203_2026-09-25.txt", "bloque_propuesto_a203_2026-09-25.txt",
         "bloque_vivo_a188_2026-09-25.txt", "bloque_propuesto_a188_2026-09-25.txt",
         "bloque_vivo_a82_2026-09-25.txt", "bloque_propuesto_a82_2026-09-25.txt",
         "pareo_frases_total_s17_2026-09-25.json", "canon_a229_s17_2026-09-25.txt"]

man = {
  "fecha": "2026-09-25", "sesion": "17/30", "ministerio": "Hacienda",
  "ejecucion_en_ley": False,
  "motivo": "Deuda propia 0. sha256 de la ley idéntico a la apertura (7e66b466…). Ningún diff aprobado pendiente sobre LGT. No se crea .bak porque no se toca el fichero.",
  "sha256_ley_apertura": sha(ley),
  "sha256_ley_esperada_referencia": "7e66b466990e0b87ceafe5263552643046d452e2d97faa27f3ea02aa748f93dd",
  "coincide": sha(ley) == "7e66b466990e0b87ceafe5263552643046d452e2d97faa27f3ea02aa748f93dd",
  "bloques_propuestos_pendientes_de_votacion": {},
  "ficheros": {f: {"sha256": sha(os.path.join(ev, f)), "palabras": len(open(os.path.join(ev, f), encoding="utf-8").read().split())} for f in files if os.path.exists(os.path.join(ev, f))},
}
for b in ("a229", "a203", "a188"):
    v = man["ficheros"].get(f"bloque_vivo_{b}_2026-09-25.txt", {}).get("palabras")
    p = man["ficheros"].get(f"bloque_propuesto_{b}_2026-09-25.txt", {}).get("palabras")
    man["bloques_propuestos_pendientes_de_votacion"][b] = {"vivo": v, "propuesto": p, "delta": (p - v) if (v and p) else None}

out = os.path.join(ev, "manifiesto_s17_2026-09-25.json")
json.dump(man, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(man, ensure_ascii=False, indent=1))
