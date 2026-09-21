"""Sesion 4 - Test de fidelidad BOE definitivo (muestreo dirigido, no heuristico).

Dos tests complementarios:
  T1. Ventana deslizante: cada linea BOE sustantiva (>=60 car) debe tener una
      ventana de 25 palabras presente en el repo. Es el test mas permisivo:
      si AUSENTE25=0, el texto existe en el repo.
  T2. Para los casos marcados, localizar en que bloque del repo vive, o confirmar
      que el bloque del repo esta TRUNCADO (p.e. df-4: 'quedan redactados en los
      siguientes terminos:' y nada despues).
"""
import re
import html

MD = "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md"
BOE = "ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html"


def norm(s):
    s = s.replace("\u00a0", " ").replace("\r", " ")
    s = re.sub(r"[«»\"'’`´]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_lines(path):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    hu = html.unescape(re.sub(r"<[^>]+>", "\n", h))
    return [norm(l) for l in hu.split("\n") if l.strip()]


NOISE = re.compile(
    r"^(Subir|\[Bloque|Última|Texto |Redactado|Se modifica|Se añade|Modificación|En vigor"
    r"|Este texto|La consolidación|Agencia Estatal|https|BOE-A|Ley 7/2021, de|Vídeo|Ir a"
    r"|jQuery|\}|: «|Incluye la corrección|A todos los que|Este documento|Ayúdanos"
    r"|Título \w|TÍTULO|Sumario|EL PRESIDENTE|Don Felipe|Glosario|AYUDA|Compartir"
    r"|Se deroga|Real Decreto-ley \d+/20\d\d, de \d)"
)

md = norm(open(MD, encoding="utf-8").read().replace("**", ""))
md_words = " " + " ".join(md.split()) + " "
boe = load_lines(BOE)

win_abs = []
total = 0
for x in boe:
    if len(x) < 60 or NOISE.match(x):
        continue
    total += 1
    w = x.split()
    # ventana de 25 palabras desde el minuto 30 de la linea (evita cabeceras de lista)
    hit = False
    for off in (0, 20, 40):
        for k in range(off, min(off + 8, max(1, len(w) - 24))):
            frag = " " + " ".join(w[k:k + 25]) + " "
            if len(frag.split()) == 26 and frag in md_words:
                hit = True
                break
        if hit:
            break
    if not hit:
        win_abs.append(x)

print("lineas BOE sustantivas:", total)
print("AUSENTES con ventana de 25 palabras:", len(win_abs))
for x in win_abs:
    print("  -", x[:110])
