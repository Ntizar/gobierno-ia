# -*- coding: utf-8 -*-
"""Cuadre del sha256 del fichero de ley en disco vs git HEAD (líneas EOL)."""
import hashlib, io, sys, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
raw = open("ministerios/hacienda/leyes/BOE-A-2003-23186.md", "rb").read()
print("disk bytes:", len(raw), "sha256:", hashlib.sha256(raw).hexdigest())
crlf = raw.count(b"\r\n"); lf = raw.count(b"\n")
print("CRLF:", crlf, "LF total:", lf, "solo-LF:", lf - crlf)
lf_only = raw.replace(b"\r\n", b"\n")
print("sha256 normalizado a LF:", hashlib.sha256(lf_only).hexdigest())
h = subprocess.run(["git", "show", "HEAD:ministerios/hacienda/leyes/BOE-A-2003-23186.md"],
                   capture_output=True)
print("sha256 blob git HEAD:", hashlib.sha256(h.stdout).hexdigest(), "bytes:", len(h.stdout))
c = subprocess.run(["git", "show", "HEAD", "--format=%H %ci %s", "--no-patch"],
                   capture_output=True, text=True)
print("HEAD:", c.stdout.strip())
d = subprocess.run(["git", "diff", "--stat", "79ecfc2", "HEAD", "--",
                    "ministerios/hacienda/leyes/BOE-A-2003-23186.md"],
                   capture_output=True, text=True)
print("diff 79ecfc2..HEAD en ley:", d.stdout.strip() or "ninguno")
