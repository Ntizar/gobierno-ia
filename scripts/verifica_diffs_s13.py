#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificacion independiente de los diffs de Fase 2 (sesion 13/30).

Herramienta de Presidencia (Mastermind): NO la escribe el ministerio que ejecuta.
Para cada ley y cada bloque objetivo calcula:
  - n de copias del cuerpo del articulo dentro del bloque (duplicacion)
  - palabras del bloque
  - fidelidad de vocabulario contra el BOE consolidado archivado en el repo
  - palabras del bloque SIN TRAZA en el BOE (proxy de texto inventado)
  - frases repetidas dentro del bloque (duplicacion literal)

Uso:
  python scripts/verifica_diffs_s13.py                # estado actual (working tree)
  python scripts/verifica_diffs_s13.py --fuente head  # estado en el ultimo commit
"""
import re, os, sys, json, io, html as htmlmod, hashlib, subprocess, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERIF = {
    "hacienda": {
        "ley": "ministerios/hacienda/leyes/BOE-A-2003-23186.md",
        "boe": "ministerios/hacienda/evidencia/boe_consolidado_BOE-A-2003-23186.html",
        "objetivo": ["a12", "a43", "a62", "a95"],
    },
    "sanidad": {
        "ley": "ministerios/sanidad/leyes/BOE-A-1986-10499.md",
        "boe": "ministerios/sanidad/evidencia/boe_consolidado_BOE-A-1986-10499.html",
        "objetivo": ["atres", "aseis", "adieciseis", "aveinte"],
    },
    "transicion-ecologica": {
        "ley": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
        "boe": "ministerios/transicion-ecologica/evidencia/BOE-A-2021-8447_consolidado_2026-08-31.html",
        "objetivo": ["a1", "a2", "a1-7"],
    },
}


def leer(path):
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def leer_git(rel):
    out = subprocess.run(["git", "show", "HEAD:" + rel], cwd=RAIZ,
                         capture_output=True)
    if out.returncode != 0:
        raise SystemExit("git show fallo para %s: %s" % (rel, out.stderr.decode("utf-8", "replace")))
    return out.stdout.decode("utf-8", "replace")


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return set(re.findall(r"[a-z0-9]{2,}", texto.lower()))


def html_a_texto(raw):
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)</(p|div|li|tr|h[1-6]|br)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return htmlmod.unescape(raw)


def trozo_ancla(raw_html, ancla):
    """Devuelve el HTML del articulo con id=ancla hasta el siguiente id='a...'."""
    m = re.search(r'id="%s"' % re.escape(ancla), raw_html)
    if not m:
        return None
    resto = raw_html[m.end():]
    fin = re.search(r'id="a[0-9a-z\-]*"', resto)
    if fin:
        resto = resto[:fin.start()]
    return resto[:60000]


def bloque_repo(texto, label):
    m = re.search(r"^## \[%s\][^\n]*\n" % re.escape(label), texto, re.M)
    if not m:
        return None, None, None
    ini = m.end()
    sig = re.search(r"^## \[", texto[ini:], re.M)
    fin = ini + sig.start() if sig else len(texto)
    return texto[m.start():ini], texto[ini:fin], texto[:m.start()].count("\n") + 1


def cabeceras_cuerpo(cuerpo):
    return [l.strip() for l in cuerpo.splitlines()
            if re.match(r"^\**Art[íi]culo\b", l.strip())]


def frases_repetidas(cuerpo):
    frases = [f.strip().lower() for f in re.split(r"(?<=[.;])\s+", cuerpo) if len(f.split()) >= 8]
    vistos, repes = {}, []
    for fr in frases:
        k = re.sub(r"\W+", " ", fr)
        if k in vistos:
            repes.append(fr[:110])
        vistos[k] = 1
    return repes


def analiza(ley_txt, boe_raw, objetivos):
    res = {}
    for lab in objetivos:
        cab, cuerpo, linea = bloque_repo(ley_txt, lab)
        if cuerpo is None:
            res[lab] = {"estado": "BLOQUE NO ENCONTRADO"}
            continue
        html_art = trozo_ancla(boe_raw, lab)
        if html_art:
            art_txt = html_a_texto(html_art)
            w_boe = normalizar(art_txt)
            w_repo = normalizar(cuerpo)
            inter = w_repo & w_boe
            fidelidad = round(100.0 * len(inter) / max(1, len(w_boe)), 2)
            sin_traza = len(w_repo - w_boe)
            boe_ok = True
        else:
            fidelidad, sin_traza, boe_ok = None, None, False
        repes = frases_repetidas(cuerpo)
        res[lab] = {
            "linea_cabecera": linea,
            "cabeceras_cuerpo": cabeceras_cuerpo(cuerpo),
            "n_copias": len(cabeceras_cuerpo(cuerpo)),
            "palabras_bloque": len(cuerpo.split()),
            "frases_repetidas": len(repes),
            "muestra_repetida": repes[:2],
            "fidelidad_vocab_pct": fidelidad,
            "palabras_sin_traza_boe": sin_traza,
            "ancla_boe_encontrada": boe_ok,
        }
    return res


def main():
    fuente = "worktree"
    if "--fuente" in sys.argv:
        fuente = sys.argv[sys.argv.index("--fuente") + 1]

    salida = {"fuente": fuente, "leyes": {}}
    for min_, cfg in VERIF.items():
        ley_txt = leer_git(cfg["ley"]) if fuente == "head" else leer(os.path.join(RAIZ, cfg["ley"]))
        boe_raw = leer(os.path.join(RAIZ, cfg["boe"]))
        info = {
            "fichero": cfg["ley"],
            "palabras_fichero": len(ley_txt.split()),
            "sha256": hashlib.sha256(ley_txt.encode("utf-8")).hexdigest()[:16],
            "bloques": analiza(ley_txt, boe_raw, cfg["objetivo"]),
        }
        salida["leyes"][min_] = info

    print(json.dumps(salida, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
