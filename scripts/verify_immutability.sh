#!/bin/bash
# verify_immutability.sh — Wrapper para CI que ejecuta la verificación de inmutabilidad.
set -uo pipefail
python scripts/verify_immutability.py
exit $?
