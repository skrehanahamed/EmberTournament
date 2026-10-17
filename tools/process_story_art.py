#!/usr/bin/env python3
"""Converts the cutscene illustrations in Assets/story/<key>.png into data/story/<key>.jpg (1920x1080, centre-cropped 16:9).
Keys are listed in story/ART_PROMPTS.md (prologue_0, ch2_before, ch2_after, epilogue_3 ...). Missing keys fall back to the stage picture.
Run:  .venv/bin/python tools/process_story_art.py
"""
import os

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC, OUT = os.path.join(ROOT, "Assets", "story"), os.path.join(ROOT, "data", "story")
os.makedirs(OUT, exist_ok=True)
n = 0
for name in sorted(os.listdir(SRC)):
    base, ext = os.path.splitext(name)
    if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
        continue
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    w, h = im.size
    tw = int(h * 16 / 9)
    if tw <= w:
        box = ((w - tw) // 2, 0, (w - tw) // 2 + tw, h)
    else:
        th = int(w * 9 / 16)
        box = (0, (h - th) // 2, w, (h - th) // 2 + th)
    im.crop(box).resize((1920, 1080), Image.LANCZOS).save(os.path.join(OUT, base + ".jpg"), quality=90)
    n += 1
    print("story art", base)
print(n, "pictures ->", OUT)
