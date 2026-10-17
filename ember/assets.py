"""Loads and caches all game art. Frames are stored right-facing; a mirrored copy is made for left-facing."""
import json
import os

import pygame

from .constants import DATA, W, H


class Frame:
    __slots__ = ("img", "flip", "w", "h", "ox", "oy", "tip")

    def __init__(self, img, meta):
        self.img = img
        self.flip = pygame.transform.flip(img, True, False)
        self.w, self.h = img.get_size()
        self.ox, self.oy = meta["ox"], meta["oy"]
        self.tip = tuple(meta.get("tip", (self.w + self.ox, self.oy + self.h / 2)))


class Anim:
    def __init__(self, frames):
        self.frames = frames

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, i):
        return self.frames[min(i, len(self.frames) - 1)]


def _load_anim_dir(root, name, metas):
    frames = []
    for i, m in enumerate(metas):
        img = pygame.image.load(os.path.join(root, name, f"{i}.png")).convert_alpha()
        frames.append(Frame(img, m))
    return Anim(frames)


class Assets:
    def __init__(self):
        self.chars = {}
        self.fx = {}
        self.stages = {}
        self.ui = {}
        self._fonts = {}
        self._text_cache = {}

    # -- loading -------------------------------------------------------
    def load_character(self, cid):
        if cid not in self.chars:
            root = os.path.join(DATA, "characters", cid)
            meta = json.load(open(os.path.join(root, "meta.json")))
            anims = {name: _load_anim_dir(root, name, metas) for name, metas in meta["anims"].items()}
            self.chars[cid] = {"anims": anims, "stance_h": meta["stance_h"]}
        return self.chars[cid]

    def load_fx(self):
        if not self.fx:
            root = os.path.join(DATA, "fx")
            meta = json.load(open(os.path.join(root, "meta.json")))
            for name, metas in meta.items():
                self.fx[name] = _load_anim_dir(root, name, metas)
        return self.fx

    def stage(self, sid):
        if sid not in self.stages:
            self.stages[sid] = pygame.image.load(os.path.join(DATA, "stages", f"{sid}.png")).convert()
        return self.stages[sid]

    def image(self, name, alpha=True):
        if name not in self.ui:
            img = pygame.image.load(os.path.join(DATA, "ui", name + ".png"))
            self.ui[name] = img.convert_alpha() if alpha else img.convert()
        return self.ui[name]

    # -- fonts / text --------------------------------------------------
    def font(self, size):
        if size not in self._fonts:
            self._fonts[size] = pygame.font.Font(os.path.join(DATA, "fonts", "PressStart2P.ttf"), size)
        return self._fonts[size]

    def text(self, s, size, color=(255, 255, 255), outline=(0, 0, 0), thick=None, shadow=True):
        """Pixel-font text with an outline, cached."""
        key = (s, size, color, outline, thick, shadow)
        surf = self._text_cache.get(key)
        if surf is None:
            f = self.font(size)
            thick = thick if thick is not None else max(2, size // 10)
            thick = min(thick, size // 14 + 1)       # a thicker outline would fuse the letters into a black slab
            base = f.render(s, False, color)
            ol = f.render(s, False, outline)
            w, h = base.get_size()
            surf = pygame.Surface((w + thick * 2 + 4, h + thick * 2 + (6 if shadow else 0)), pygame.SRCALPHA)
            for dx in range(-thick, thick + 1):
                for dy in range(-thick, thick + 1):
                    if dx * dx + dy * dy <= thick * thick + 1:
                        surf.blit(ol, (thick + dx + 2, thick + dy))
            if shadow:
                surf.blit(ol, (thick + 2, thick + 6))
            surf.blit(base, (thick + 2, thick))
            if len(self._text_cache) > 600:
                self._text_cache.clear()
            self._text_cache[key] = surf
        return surf
