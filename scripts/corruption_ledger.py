#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ledger de corrupción del corpus — Fase 7.

Compara el corpus canónico limpio (data/raw/boe/) contra los MDs mutados
(ministerios/*/leyes/*.md) y clasifica cada diferencia.

Clasificación:
- duplicacion: contenido repetido introducido por el pipeline
- omision: contenido del BOE ausente en el MD mutado
- restauracion: contenido restaurado tras haber sido borrado
- cambio_editorial: modificación intencional (propuesta simplificadora)
- formato: cambios de formato sin alteración de contenido
- desconocida: no se puede clasificar automáticamente

Uso: python scripts/corruption_ledger.py [--json] [--markdown]
"""
import os
import re
import sys
import json
import hashlib
import unicodedata
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LEYES = {
    "LGT": {
        "boe_id": "BOE-A-2003-23186",
        "canonical_json": "data/canonical/BOE-A-2003-23186/2026-08-31.json",
        "mutated_md": "ministerios/hacienda/leyes/BOE-A-2003-23186.md",
    },
    "LGS": {
        "boe_id": "BOE-A-1986-10499",
        "canonical_json": "data/canonical/BOE-A-1986-10499/2026-08-31.json",
        "mutated_md": "ministerios/sanidad/leyes/BOE-A-1986-10499.md",
    },
    "L7": {
        "boe_id": "BOE-A-2021-8447",
        "canonical_json": "data/canonical/BOE-A-2021-8447/2026-08-31.json",
        "mutated_md": "ministerios/transicion-ecologica/leyes/BOE-A-2021-8447.md",
    },
}


def normalize(s):
    """Normaliza texto para comparación."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s.lower()).strip()
    return s


def extract_blocks_from_md(md_path):
    """Extrae bloques de artículo de un MD mutado."""
    if not os.path.exists(md_path):
        return {}
    with open(md_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    blocks = {}
    for m in re.finditer(r"^## \[([^\]]+)\][^\n]*\n", text, re.M):
        label = m.group(1)
        ini = m.end()
        sig = re.search(r"^## \[", text[ini:], re.M)
        fin = ini + sig.start() if sig else len(text)
        body = text[ini:fin].strip()
        # Remove markdown headers within block
        body_clean = re.sub(r"^#+\s*.*$", "", body, flags=re.M).strip()
        blocks[label] = body_clean
    return blocks


def load_canonical(canonical_path):
    """Carga JSON canónico."""
    if not os.path.exists(canonical_path):
        return {}
    with open(canonical_path, encoding="utf-8") as f:
        data = json.load(f)
    return {a["id"]: a["texto"] for a in data.get("articulos", [])}


def classify_difference(canonical_text, md_text):
    """Clasifica la diferencia entre canonical y MD."""
    can_norm = normalize(canonical_text)
    md_norm = normalize(md_text)

    if can_norm == md_norm:
        return "sin_cambio"

    can_words = set(can_norm.split())
    md_words = set(md_norm.split())

    missing = can_words - md_words
    extra = md_words - can_words

    missing_pct = 100.0 * len(missing) / max(1, len(can_words))
    extra_pct = 100.0 * len(extra) / max(1, len(md_words))

    if missing_pct > 50 and extra_pct > 50:
        return "cambio_editorial"  # Mucho se quitó y mucho se añadió
    elif missing_pct > 20:
        return "omision"  # Mucho contenido ausente
    elif extra_pct > 20:
        return "duplicacion"  # Mucho contenido extra
    elif missing_pct > 5 or extra_pct > 5:
        return "formato"
    else:
        return "cambio_editorial"


def compute_word_count(s):
    return len(s.split())


def main():
    output_json = "--json" in sys.argv
    output_md = "--markdown" in sys.argv or not output_json

    ledger = {"fecha_generacion": "", "leyes": {}}

    total_canonical_words = 0
    total_md_words = 0
    total_corruption_removed = 0
    total_content_restored = 0
    total_editorial = 0

    for nombre, cfg in LEYES.items():
        canonical_path = os.path.join(BASE, cfg["canonical_json"])
        md_path = os.path.join(BASE, cfg["mutated_md"])

        canonical = load_canonical(canonical_path)
        md_blocks = extract_blocks_from_md(md_path)

        ley_data = {
            "boe_id": cfg["boe_id"],
            "canonical_path": cfg["canonical_json"],
            "mutated_path": cfg["mutated_md"],
            "canonical_hash": "",
            "mutated_hash": "",
            "total_canonical_articles": len(canonical),
            "total_md_blocks": len(md_blocks),
            "differences": [],
            "summary": {},
        }

        # Hashes
        if os.path.exists(canonical_path):
            with open(canonical_path, "rb") as f:
                ley_data["canonical_hash"] = hashlib.sha256(f.read()).hexdigest()[:16]
        if os.path.exists(md_path):
            with open(md_path, "rb") as f:
                ley_data["mutated_hash"] = hashlib.sha256(f.read()).hexdigest()[:16]

        counts = {"sin_cambio": 0, "duplicacion": 0, "omision": 0,
                  "cambio_editorial": 0, "formato": 0, "desconocida": 0}
        words_by_type = {"duplicacion": 0, "omision": 0, "cambio_editorial": 0, "formato": 0}

        # Map canonical article IDs to MD block labels
        id_map = {
            "auno": "atres", "ados": "ados", "atres": "atres",
            # This is approximate — the mapping depends on the specific MD format
        }

        for art_id, art_text in canonical.items():
            total_canonical_words += compute_word_count(art_text)

            # Try to find matching MD block
            md_text = md_blocks.get(art_id, "")
            if not md_text:
                # Try approximate match
                for label, text in md_blocks.items():
                    if normalize(art_text[:100]) in normalize(text) or normalize(text[:100]) in normalize(art_text):
                        md_text = text
                        break

            if not md_text:
                counts["omision"] += 1
                words_by_type["omision"] += compute_word_count(art_text)
                continue

            total_md_words += compute_word_count(md_text)
            diff_type = classify_difference(art_text, md_text)
            counts[diff_type] += 1

            if diff_type != "sin_cambio":
                can_wc = compute_word_count(art_text)
                md_wc = compute_word_count(md_text)
                if diff_type == "omision":
                    words_by_type["omision"] += max(0, can_wc - md_wc)
                elif diff_type == "duplicacion":
                    words_by_type["duplicacion"] += max(0, md_wc - can_wc)
                elif diff_type == "cambio_editorial":
                    words_by_type["cambio_editorial"] += abs(can_wc - md_wc)

                ley_data["differences"].append({
                    "article_id": art_id,
                    "type": diff_type,
                    "canonical_words": can_wc,
                    "md_words": md_wc,
                    "delta_words": md_wc - can_wc,
                })

        ley_data["summary"] = counts
        ley_data["words_by_type"] = words_by_type
        total_corruption_removed += words_by_type["duplicacion"]
        total_content_restored += words_by_type["omision"]
        total_editorial += words_by_type["cambio_editorial"]

        ledger["leyes"][nombre] = ley_data

    ledger["totals"] = {
        "canonical_words": total_canonical_words,
        "md_words": total_md_words,
        "corruption_removed": total_corruption_removed,
        "content_restored": total_content_restored,
        "editorial_changes": total_editorial,
    }

    import datetime
    ledger["fecha_generacion"] = datetime.datetime.now().isoformat()

    if output_json:
        out_path = os.path.join(BASE, "reports", "rescate", "corruption-ledger.json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)
        print(f"Ledger guardado en {out_path}")
    else:
        # Print summary
        print("=== LEDGER DE CORRUPCIÓN ===\n")
        for nombre, data in ledger["leyes"].items():
            s = data["summary"]
            w = data["words_by_type"]
            print(f"## {nombre} ({data['boe_id']})")
            print(f"  Canonical: {data['total_canonical_articles']} artículos")
            print(f"  MD mutado: {data['total_md_blocks']} bloques")
            print(f"  Sin cambio: {s['sin_cambio']}")
            print(f"  Duplicación: {s['duplicacion']} ({w['duplicacion']} palabras)")
            print(f"  Omisión: {s['omision']} ({w['omision']} palabras)")
            print(f"  Cambio editorial: {s['cambio_editorial']} ({w['cambio_editorial']} palabras)")
            print(f"  Formato: {s['formato']}")
            print()

        t = ledger["totals"]
        print("### TOTALES")
        print(f"  Corrupción eliminada: {t['corruption_removed']} palabras")
        print(f"  Contenido restaurado: {t['content_restored']} palabras")
        print(f"  Cambios editoriales: {t['editorial_changes']} palabras")
        print(f"  ⚠️ NINGUNA de estas cifras es 'ahorro normativo'")


if __name__ == "__main__":
    main()
