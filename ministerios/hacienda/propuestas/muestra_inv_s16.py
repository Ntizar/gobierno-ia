# Muestra s16: entradas del inventario F1 para los tops + detalle DF.
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
inv = json.load(open(BASE + r"/ministerios/hacienda/evidencia/inventario_f1_vivo_s15_2026-09-23.json", encoding="utf-8"))
pa = inv["preceptos_afectados"]
for k in ["[dfsexta]", "[dfquinta]", "[dfoctava]", "[a249]", "[a229]", "[a203]", "[a150]", "[a188]", "[a81]", "[a95]", "[a48]", "[davigesima]"]:
    print("=" * 70)
    print(k, "->", json.dumps(pa.get(k), ensure_ascii=False)[:600])
