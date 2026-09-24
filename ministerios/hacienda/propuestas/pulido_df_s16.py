# Pulido final canon DF s16: unir líneas partidas por el HTML del BOE (continuations),
# reconstruir bloques propuestos legibles y RE-HASHEAR con la convención del Auditor.
import re, sys, io, hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"C:/Users/d_ant/Projects/gobierno-ia"
WS = re.compile(r"\S+")

def auditor(t):
    return hashlib.sha256(t.strip("\n").replace("\r\n","\n").encode("utf-8")).hexdigest()

def join_lines(text):
    # Une una línea con la siguiente si la segunda empieza por minúscula, coma, espacio o paréntesis
    out = []
    for ln in text.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if out:
            prev = out[-1]
            cont = (ln[0] in " ,);—" or ln[0].islower() or ln.startswith("de ") or ln.startswith("del ")
                    or prev.endswith(("de", "del", "la", "el", "los", "las", "un", "una", "y", "e", "o", "a", "en", "con", "por", "para", "según", "al", ",", "(", "-", "su", "se", "que", "no", "más")))
            if cont:
                out[-1] = prev if prev.endswith((" ", "—")) else prev + ("" if prev.endswith("-") else " ")
                out[-1] = (out[-1].rstrip() + ("-" if prev.endswith("-") else " ") + ln).strip()
                continue
        out.append(ln)
    return "\n".join(out)

for slug in ["dfquinta", "dfsexta", "dfoctava"]:
    p = BASE + rf"/ministerios/hacienda/evidencia/bloque_propuesto_{slug}_2026-09-24.txt"
    t = open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")
    lines = t.split("\n")
    head = lines[0]
    body = join_lines("\n".join(lines[1:]))
    prop = head + "\n\n" + body
    open(p, "w", encoding="utf-8", newline="\n").write(prop)
    print(slug, "-> pal", len(WS.findall(prop)), "| hash NUEVO", auditor(prop))
    # muestra un fragmento
    frag = body.split("\n")
    print("   1ª línea cuerpo:", frag[0][:110])
    print("   2ª línea cuerpo:", frag[1][:110] if len(frag) > 1 else "")
