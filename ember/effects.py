"""Short-lived visual effects, projectiles and ambient particles."""
import random

import pygame

from .constants import GROUND, H, W


_SCALED = {}


def scaled(fr, flip, scale):
    """Scaled copy of an effect frame, shared by every effect (so a size is only ever scaled once)."""
    key = (id(fr), flip, round(scale, 3))
    img = _SCALED.get(key)
    if img is None:
        base = fr.flip if flip else fr.img
        img = base if abs(scale - 1.0) < 1e-3 else pygame.transform.smoothscale(
            base, (max(1, int(fr.w * scale)), max(1, int(fr.h * scale))))
        _SCALED[key] = img
    return img


def warm(anim, scale):
    """Pre-scale every frame of an animation (both facings) so nothing stalls the first time it shows."""
    for fr in anim.frames:
        scaled(fr, False, scale)
        scaled(fr, True, scale)


class FX:
    """A one-shot sprite animation (hit spark, explosion, dust ...)."""

    def __init__(self, anim, x, y, rate=3, scale=1.0, flip=False, loop=False):
        self.anim, self.x, self.y = anim, x, y
        self.rate, self.scale, self.flip, self.loop = rate, scale, flip, loop
        self.t = 0
        self.dead = False
        self.behind = False
        self.ignore_hitstop = False
        self._cache = {}

    def update(self):
        self.t += 1
        if self.t // self.rate >= len(self.anim.frames):
            if self.loop:
                self.t = 0
            else:
                self.dead = True

    def draw(self, screen, ox=0, oy=0):
        i = min(self.t // self.rate, len(self.anim.frames) - 1)
        fr = self.anim.frames[i]
        img = scaled(fr, self.flip, self.scale)
        if self.flip:
            left = self.x - (fr.w + fr.ox) * self.scale
        else:
            left = self.x + fr.ox * self.scale
        screen.blit(img, (int(left + ox), int(self.y + fr.oy * self.scale + oy)))


class Fireball:
    def __init__(self, owner, x, y, direction, speed, anim, scale=0.85):
        self.owner, self.x, self.y, self.dir, self.speed = owner, x, y, direction, speed
        self.anim, self.scale = anim, scale
        self.t = 0
        self.dead = False
        self.finisher = False
        self.move = "special"
        self.rscale = 1.0
        self._cache = {}

    def rect(self):
        return pygame.Rect(int(self.x - 66 * self.rscale), int(self.y - 50 * self.rscale), int(132 * self.rscale), int(100 * self.rscale))

    def update(self):
        self.t += 1
        self.x += self.dir * self.speed
        if self.x < -200 or self.x > W + 200:
            self.dead = True

    def draw(self, screen, ox=0, oy=0):
        i = (self.t // 4) % len(self.anim.frames)
        fr = self.anim.frames[i]
        flip = self.dir < 0
        img = scaled(fr, flip, self.scale)
        if flip:
            left = self.x - (fr.w + fr.ox) * self.scale
        else:
            left = self.x + fr.ox * self.scale
        screen.blit(img, (int(left + ox), int(self.y + fr.oy * self.scale + oy)))


class Ambient:
    """Background particles: rain, petals, embers."""

    def __init__(self, kind, rng=None):
        self.kind = kind
        self.rng = rng or random.Random(5)
        n = {"rain": 220, "petals": 55, "embers": 90}.get(kind, 0)
        self.p = [self._new(True) for _ in range(n)]

    def _new(self, anywhere=False):
        r = self.rng
        x = r.uniform(0, W)
        y = r.uniform(0, H) if anywhere else (-20 if self.kind != "embers" else H + 10)
        if self.kind == "rain":
            return [x, y, r.uniform(-4, -2), r.uniform(26, 38), r.uniform(0.5, 1)]
        if self.kind == "petals":
            return [x, y, r.uniform(-1.5, -0.2), r.uniform(1.2, 2.6), r.uniform(0, 6.28)]
        return [x, y, r.uniform(-0.8, 0.8), r.uniform(-2.8, -0.8), r.uniform(0.4, 1)]

    def update(self):
        for p in self.p:
            p[0] += p[2]
            p[1] += p[3]
            if self.kind == "petals":
                p[4] += 0.05
                p[0] += 0.9 * (1 if (p[4] % 6.28) < 3.14 else -1) * 0.5
            if self.kind == "embers":
                p[2] += self.rng.uniform(-0.12, 0.12)
            if p[1] > H + 40 or p[1] < -40 or p[0] < -50 or p[0] > W + 50:
                p[:] = self._new()

    def draw(self, screen):
        if self.kind == "rain":
            for x, y, vx, vy, a in self.p:
                pygame.draw.line(screen, (150 + int(60 * a), 180 + int(40 * a), 255), (x, y), (x + vx * 0.8, y + vy * 0.8), 2)
        elif self.kind == "petals":
            for x, y, vx, vy, ph in self.p:
                pygame.draw.rect(screen, (255, 170, 205), (int(x), int(y), 7, 5))
                pygame.draw.rect(screen, (255, 215, 230), (int(x), int(y), 3, 2))
        elif self.kind == "embers":
            for x, y, vx, vy, a in self.p:
                c = (255, int(120 + 90 * a), int(30 + 40 * a))
                s = 4 if a > 0.7 else 3
                pygame.draw.rect(screen, c, (int(x), int(y), s, s))
