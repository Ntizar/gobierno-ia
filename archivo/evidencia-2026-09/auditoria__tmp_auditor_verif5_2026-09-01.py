import json, os
REPO = r"C:/Users/d_ant/Projects/gobierno-ia"
om = json.load(open(os.path.join(REPO, "ministerios/transicion-ecologica/evidencia/omisiones_repositorio_2026-09-01.json"), encoding="utf-8"))
tot_o = sum(int(x.get("palabras", 0)) for x in om["omisiones"])
tot_p = sum(int(x.get("palabras", 0)) for x in om["parciales"])
print("omisiones:", len(om["omisiones"]), "palabras:", tot_o)
print("parciales:", len(om["parciales"]), "palabras:", tot_p)
# desglose de omisiones: cuales son notas/errores vs texto normativo
notas = [x for x in om["omisiones"] if "BOE núm" in str(x) or "Errata" in str(x) or "corrección" in str(x)]
print("omisiones_q_parecen_notas:", len(notas), "palabras:", sum(int(x.get("palabras",0)) for x in notas))
la = json.load(open(os.path.join(REPO, "ministerios/transicion-ecologica/evidencia/lineas_ausentes_BOE_vs_repo_2026-09-01.json"), encoding="utf-8"))
L = la if isinstance(la, list) else la.get("lineas", [])
print("lineas_ausentes JSON:", len(L), "palabras:", sum(int(x.get("palabras",0)) for x in L))
d97 = json.load(open(os.path.join(REPO, "ministerios/sanidad/evidencia/diff_arts18_y_35_2026-08-31.json"), encoding="utf-8"))
print("san diff JSON keys:", list(d97)[:8] if isinstance(d97, dict) else len(d97))
