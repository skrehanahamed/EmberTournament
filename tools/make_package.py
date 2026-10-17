#!/usr/bin/env python3
"""Builds dist/EmberTournament.zip - just what is needed to play (no Assets/, no .venv). Copy it to another PC and unzip.
Run:  .venv/bin/python tools/make_package.py
"""
import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "dist", "EmberTournament.zip")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
files = ["main.py", "requirements.txt", "run_windows.bat", "build_windows.bat", "README.md", "Makefile"]
n = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(os.path.join(ROOT, f), "EmberTournament/" + f)
    for top in ("ember", "data"):
        for dp, dn, fn in os.walk(os.path.join(ROOT, top)):
            dn[:] = [d for d in dn if d != "__pycache__"]
            for f in fn:
                if f.startswith(".") or f.endswith(".pyc"):
                    continue
                p = os.path.join(dp, f)
                z.write(p, "EmberTournament/" + os.path.relpath(p, ROOT))
                n += 1
print(f"{OUT}  ({os.path.getsize(OUT) / 1e6:.0f} MB, {n} files)")
