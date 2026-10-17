"""In-fight HUD drawn with pygame primitives plus the generated portraits."""
import math

import pygame

from .constants import GOLD, H, W, CHARS

BAR_W, BAR_H, SKEW = 700, 68, 28
BAR_Y = 40
P1_X, P2_X = 230, W - 230 - BAR_W


def _shift(y, top, h, skew):
    return skew * (1.0 - (y - top) / h)


def para(x0, x1, ya, yb, top, h, skew, lean):
    """Parallelogram strip between x0..x1 (at the bottom edge) from ya to yb. lean=+1 is '/', -1 is '\\'."""
    sa, sb = _shift(ya, top, h, skew), _shift(yb, top, h, skew)
    if lean < 0:
        sa, sb = skew - sa, skew - sb
    return [(x0 + sa, ya), (x1 + sa, ya), (x1 + sb, yb), (x0 + sb, yb)]


def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Hud:
    def __init__(self, assets, fighters):
        self.a = assets
        self.f = fighters
        self.lag = [f.spec["hp"] for f in fighters]
        self.hold = [0, 0]
        self.last = [f.spec["hp"] for f in fighters]
        self.t = 0
        self.portraits = [self._portrait(f.cid, tint=getattr(f, "tint", None)) for f in fighters]
        self.vignette = self._strip()

    def _strip(self):
        s = pygame.Surface((W, 200), pygame.SRCALPHA)
        for y in range(200):
            pygame.draw.line(s, (0, 0, 0, int(190 * (1 - y / 200) ** 1.4)), (0, y), (W, y))
        return s

    def _portrait(self, cid, size=124, tint=None):
        img = self.a.image(f"portrait_{cid}")
        w, h = img.get_size()
        side = min(w, h)
        crop = img.subsurface(pygame.Rect((w - side) // 2, 0, side, side))
        crop = pygame.transform.smoothscale(crop, (size, size))
        if tint:
            crop.fill(tint + (255,), special_flags=pygame.BLEND_RGBA_MULT)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
        out = pygame.Surface((size, size), pygame.SRCALPHA)
        out.blit(crop, (0, 0))
        out.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return out

    # ------------------------------------------------------------------
    def update(self):
        self.t += 1
        for i, f in enumerate(self.f):
            if f.hp < self.last[i]:
                self.hold[i] = 28
            self.last[i] = f.hp
            if self.hold[i] > 0:
                self.hold[i] -= 1
            elif self.lag[i] > f.hp:
                self.lag[i] = max(f.hp, self.lag[i] - f.spec["hp"] * 0.006)
            if self.lag[i] < f.hp:
                self.lag[i] = f.hp

    # ---- pixel-art health bar: drawn at half resolution, then scaled 2x with hard pixels -------------
    HW, HH, HSK = 350, 34, 14   # half-res width, height, skew

    def _bar_surface(self, slot, f):
        w, h, sk = self.HW, self.HH, self.HSK
        pad_top = 4
        surf = pygame.Surface((w + sk + 8, h + 30), pygame.SRCALPHA)
        flip = False   # every bar is built left-handed; player 2's is mirrored when drawn
        lean = 1

        def P(x0, x1, y0, y1):
            """Slanted strip between two heights (half-res coords), mirrored for player 2."""
            def sh(y):
                t = (y - pad_top) / h
                v = sk * (1 - t)
                return v if lean > 0 else sk - v
            pts = [(x0 + sh(y0), y0), (x1 + sh(y0), y0), (x1 + sh(y1), y1), (x0 + sh(y1), y1)]
            return [(x + 4, y) for x, y in pts]

        # drop shadow, outer dark rim, gold frame (3 tones), inner dark rim
        pygame.draw.polygon(surf, (0, 0, 0, 150), [(x + 2, y + 3) for x, y in P(0, w, pad_top, pad_top + h)])
        pygame.draw.polygon(surf, (24, 12, 14), P(0, w, pad_top, pad_top + h))
        pygame.draw.polygon(surf, (255, 236, 160), P(1, w - 1, pad_top + 1, pad_top + 7))
        pygame.draw.polygon(surf, (222, 160, 52), P(1, w - 1, pad_top + 7, pad_top + h // 2 + 3))
        pygame.draw.polygon(surf, (150, 92, 26), P(1, w - 1, pad_top + h // 2 + 3, pad_top + h - 1))
        ix0, ix1, iy0, iy1 = 5, w - 5, pad_top + 6, pad_top + h - 6
        ih = iy1 - iy0
        pygame.draw.polygon(surf, (20, 4, 8), P(ix0 - 1, ix1 + 1, iy0 - 1, iy1 + 1))
        pygame.draw.polygon(surf, (62, 10, 16), P(ix0, ix1, iy0, iy1))
        iw = ix1 - ix0
        ratio = max(0.0, f.hp / f.spec["hp"])
        lag = max(0.0, self.lag[slot] / f.spec["hp"])

        def seg(r0, r1):
            return (ix1 - iw * r1, ix1 - iw * r0) if flip else (ix0 + iw * r0, ix0 + iw * r1)

        if lag > ratio:
            a0, b0 = seg(ratio, lag)
            pygame.draw.polygon(surf, (255, 250, 205), P(a0, b0, iy0, iy0 + ih // 2))
            pygame.draw.polygon(surf, (236, 118, 30), P(a0, b0, iy0 + ih // 2, iy1))
        if ratio > 0:
            a0, b0 = seg(0, ratio)
            if ratio > 0.5:
                base = lerp_color((255, 220, 40), (60, 220, 70), (ratio - 0.5) * 2)
            elif ratio > 0.25:
                base = lerp_color((255, 70, 40), (255, 220, 40), (ratio - 0.25) * 4)
            else:
                base = tuple(int(c * (0.7 + 0.3 * math.sin(self.t * 0.35))) for c in (255, 50, 36))
            bands = [(0.00, 0.22, 0.62), (0.22, 0.45, 0.30), (0.45, 0.75, 0.0), (0.75, 1.0, -0.38)]
            for f0, f1, lighten in bands:
                col = tuple(max(0, min(255, int(c + (255 - c) * lighten) if lighten > 0 else int(c * (1 + lighten)))) for c in base)
                pygame.draw.polygon(surf, col, P(a0, b0, iy0 + ih * f0, iy0 + ih * f1 + (1 if f1 < 1 else 0)))
            # top gloss line
            pygame.draw.polygon(surf, (255, 255, 255), P(a0, b0, iy0, iy0 + 1))
            # leading edge glow
            ex = a0 if flip else b0
            pygame.draw.polygon(surf, (255, 255, 230), P(ex - (0 if flip else 2), ex + (2 if flip else 0), iy0, iy1))
        # tick marks
        for i in range(1, 10):
            xx = ix0 + iw * i / 10
            pygame.draw.polygon(surf, (30, 8, 10), P(xx, xx + 1, iy0, iy1))
        # rivets and end caps
        for rx in (3, w - 4):
            c = P(rx - 1, rx + 1, pad_top + h // 2 - 2, pad_top + h // 2 + 1)
            pygame.draw.polygon(surf, (255, 240, 190), c)
        return surf, ratio

    def draw_plate(self, screen, slot, f):
        """Name plate (static, so it is drawn once into a cached image)."""
        key = (slot, f.cid)
        cache = self.__dict__.setdefault("_plates", {})
        img = cache.get(key)
        w, h = 400, 44
        y = BAR_Y + BAR_H + 6
        x = P1_X + 6 if slot == 0 else P2_X + BAR_W - 6 - w
        if img is None:
            img = pygame.Surface((w + 30, h + 30), pygame.SRCALPHA)
            self._plate_raw(img, slot, f, 10, 10)
            cache[key] = img
        screen.blit(img, (x - 10, y - 10))

    def _plate_raw(self, screen, slot, f, x, y):
        """Name plate: slanted gold-edged panel, accent gradient, big name, role tag."""
        acc = tuple(f.spec["accent"])
        w, h, sk = 400, 44, 20

        def quad(x0, y0, ww, hh, dx=0, dy=0):
            if slot == 0:   # leans "/" like the bar
                return [(x0 + sk + dx, y0 + dy), (x0 + ww + dx, y0 + dy), (x0 + ww - sk + dx, y0 + hh + dy), (x0 + dx, y0 + hh + dy)]
            return [(x0 + dx, y0 + dy), (x0 + ww - sk + dx, y0 + dy), (x0 + ww + dx, y0 + hh + dy), (x0 + sk + dx, y0 + hh + dy)]

        pygame.draw.polygon(screen, (0, 0, 0), quad(x, y, w, h, 5, 6))
        pygame.draw.polygon(screen, (255, 236, 160), quad(x, y, w, h))
        pygame.draw.polygon(screen, (150, 92, 26), quad(x + 3, y + 3, w - 6, h - 6))
        pygame.draw.polygon(screen, (20, 8, 12), quad(x + 5, y + 5, w - 10, h - 10))
        # accent gradient sweeping in from the outer edge
        inner = w - 10
        bands = 14
        for i in range(bands):
            t = i / bands
            col = tuple(int(c * (0.9 - 0.8 * t) + 12) for c in acc)
            bw = inner / bands
            bx = x + 5 + (i * bw if slot == 0 else inner - (i + 1) * bw)
            q = quad(bx, y + 5, bw + 1, h - 10)
            pygame.draw.polygon(screen, col, q)
        # bright accent stripe along the top inside edge
        pygame.draw.polygon(screen, tuple(min(255, c + 70) for c in acc), quad(x + 5, y + 5, w - 10, 3))
        # name
        name = self.a.text(f.spec["name"], 28, (255, 255, 255), thick=4)
        nx = x + 40 if slot == 0 else x + w - 40 - name.get_width()
        screen.blit(name, (nx, y + (h - name.get_height()) // 2 + 1))
        # role tag on the far side
        role = self.a.text(f.spec["role"], 12, (255, 220, 150), thick=2, shadow=False)
        rx = x + w - 30 - role.get_width() if slot == 0 else x + 30
        screen.blit(role, (rx, y + (h - role.get_height()) // 2 + 1))

    def draw_bar(self, screen, slot, f):
        ratio = max(0.0, f.hp / f.spec["hp"])
        lag = max(0.0, self.lag[slot] / f.spec["hp"])
        key = (slot, f.cid, int(ratio * 350), int(lag * 350), (self.t // 3) % 6 if ratio <= 0.25 else 0)
        cache = self.__dict__.setdefault("_bars", {})
        big = cache.get(key)
        if big is None:
            surf, _ = self._bar_surface(slot, f)
            big = pygame.transform.scale(surf, (surf.get_width() * 2, surf.get_height() * 2))
            if slot == 1:
                big = pygame.transform.flip(big, True, False)
            if len(cache) > 400:
                cache.clear()
            cache[key] = big
        x = P1_X - 8 if slot == 0 else W - (P1_X - 8) - big.get_width()
        y = BAR_Y - 8
        screen.blit(big, (x, y))
        self.draw_plate(screen, slot, f)
        # ember sparks drifting off the edge of the fill
        if ratio > 0.02:
            iw = (self.HW - 10) * 2
            base0 = (P1_X - 8) + 8 + 8 * 2 + iw * ratio
            base_x = base0 if slot == 0 else W - base0
            for i in range(3):
                ph = (self.t * 0.07 + i * 0.37) % 1.0
                ex = base_x + math.sin(self.t * 0.2 + i * 2) * 8 + (14 if slot == 0 else -14) * ph
                ey = y + 30 - ph * 38
                col = (255, int(190 - 110 * ph), int(60 - 40 * ph))
                pygame.draw.rect(screen, col, (int(ex), int(ey), 4, 4))
        # portrait medallion
        r = 70
        cx = P1_X - 76 if slot == 0 else P2_X + BAR_W + 76
        cy = BAR_Y + 38
        pygame.draw.circle(screen, (0, 0, 0), (cx + 4, cy + 6), r + 8)
        pygame.draw.circle(screen, (24, 12, 14), (cx, cy), r + 8)
        pygame.draw.circle(screen, (150, 92, 26), (cx, cy), r + 6)
        pygame.draw.circle(screen, (255, 236, 160), (cx, cy), r + 3)
        pygame.draw.circle(screen, (222, 160, 52), (cx, cy), r - 2)
        pygame.draw.circle(screen, tuple(f.spec["accent"]), (cx, cy), r - 6)
        por = self.portraits[slot]
        if slot == 1:
            por = pygame.transform.flip(por, True, False)
        por = pygame.transform.smoothscale(por, (r * 2 - 14, r * 2 - 14))
        screen.blit(por, (cx - por.get_width() // 2, cy - por.get_height() // 2))
        # who controls this fighter: P1 / P2 / CPU badge under the portrait
        from .input import AIController
        is_cpu = isinstance(f.controller, AIController)
        both_cpu = isinstance(self.f[0].controller, AIController) and isinstance(self.f[1].controller, AIController)
        if is_cpu:
            label, col = (f"CPU {slot + 1}" if both_cpu else "CPU"), (232, 70, 54)
        else:
            label, col = f"P{slot + 1}", (70, 165, 255) if slot == 0 else (255, 160, 50)
        tag = self.a.text(label, 20, (255, 255, 255), thick=3, shadow=False)
        bw, bh = tag.get_width() + 26, 32
        bx, by = cx - bw // 2, cy + r + 10
        pygame.draw.rect(screen, (0, 0, 0), (bx + 3, by + 4, bw, bh), border_radius=8)
        pygame.draw.rect(screen, (255, 236, 160), (bx - 3, by - 3, bw + 6, bh + 6), border_radius=10)
        pygame.draw.rect(screen, col, (bx, by, bw, bh), border_radius=8)
        screen.blit(tag, (bx + (bw - tag.get_width()) // 2, by + 3))
        for ang in (45, 135, 225, 315):  # rivets on the ring
            rx = cx + int((r + 1) * math.cos(math.radians(ang)))
            ry = cy + int((r + 1) * math.sin(math.radians(ang)))
            pygame.draw.circle(screen, (255, 245, 200), (rx, ry), 3)

    def draw_energy(self, screen, slot, f):
        """Fireball limiter: three slanted cells that fill with ember energy; a cell flashes red if you try to fire while empty."""
        from .fighter import ENERGY_COST
        cells, cw, ch, gap, sk = 3, 104, 20, 10, 12
        total_w = cells * cw + (cells - 1) * gap
        x0 = P1_X + 40 if slot == 0 else P2_X + BAR_W - 40 - total_w
        y0 = BAR_Y + BAR_H + 62
        label = self.a.text("EMBER", 13, (255, 200, 120), thick=2, shadow=False)
        screen.blit(label, (x0 - 4, y0 + ch + 8) if slot == 0 else (x0 + total_w - label.get_width() + 4, y0 + ch + 8))
        frac = f.energy / ENERGY_COST
        for i in range(cells):
            pos = i if slot == 0 else cells - 1 - i      # mirrored: player 2's first cell sits on the outer edge
            cx = x0 + pos * (cw + gap)
            def quad(x, w, y, h):
                a, b = (sk, 0) if slot == 0 else (0, sk)
                return [(x + a, y), (x + w + a, y), (x + w + b, y + h), (x + b, y + h)]
            pygame.draw.polygon(screen, (0, 0, 0), [(px + 3, py + 4) for px, py in quad(cx, cw, y0, ch)])
            pygame.draw.polygon(screen, (222, 160, 52), quad(cx - 2, cw + 4, y0 - 2, ch + 4))
            pygame.draw.polygon(screen, (30, 10, 12), quad(cx, cw, y0, ch))
            fill = max(0.0, min(1.0, frac - i))
            if fill > 0:
                fw = int(cw * fill)
                full = fill >= 0.999
                top = (255, 235, 140) if full else (255, 170, 60)
                bot = (255, 120, 20) if full else (200, 80, 20)
                if slot == 0:
                    fx = cx
                else:
                    fx = cx + cw - fw
                pygame.draw.polygon(screen, bot, quad(fx, fw, y0, ch))
                pygame.draw.polygon(screen, top, quad(fx, fw, y0, ch // 2))
                if full:
                    glow = 0.5 + 0.5 * math.sin(self.t * 0.2 + i)
                    pygame.draw.polygon(screen, (255, int(200 + 55 * glow), int(120 + 80 * glow)), quad(cx + 2, cw - 4, y0 + 1, 3))
            if f.no_energy and (f.no_energy // 4) % 2 == 0:
                pygame.draw.polygon(screen, (255, 40, 40), quad(cx, cw, y0, ch), 3)

    def draw_super(self, screen, slot, f):
        """Super meter along the bottom of the screen; fills from the outside in, pulses gold when ready."""
        w, h, sk = 560, 24, 20
        x = 130 if slot == 0 else W - 130 - w
        y = H - 62
        full = f.super >= 100
        ratio = max(0.0, min(1.0, f.super / 100))
        pulse = 0.5 + 0.5 * math.sin(self.t * 0.25)
        def quad(x0, ww, pad=0):
            a, b = (sk, 0) if slot == 0 else (0, sk)
            return [(x0 + a, y + pad), (x0 + ww + a, y + pad), (x0 + ww + b, y + h - pad), (x0 + b, y + h - pad)]
        pygame.draw.polygon(screen, (0, 0, 0), [(px + 4, py + 5) for px, py in quad(x, w)])
        pygame.draw.polygon(screen, (255, 236, 160) if full else (170, 115, 35), quad(x - 3, w + 6, -3))
        pygame.draw.polygon(screen, (28, 10, 14), quad(x, w))
        fw = int(w * ratio)
        if fw > 0:
            fx = x if slot == 0 else x + w - fw
            top = (255, 245, 170) if full else (120, 210, 255)
            bot = (255, 170, 40) if full else (40, 120, 230)
            pygame.draw.polygon(screen, bot, quad(fx, fw))
            pygame.draw.polygon(screen, top, [(px, py) for px, py in quad(fx, fw)][:2] + [(quad(fx, fw)[2][0], y + h // 2), (quad(fx, fw)[3][0], y + h // 2)])
        if full:
            pygame.draw.polygon(screen, (255, int(200 + 55 * pulse), 120), quad(x - 3, w + 6, -3), 3)
        for i in range(1, 4):
            tx = x + w * i / 4
            pygame.draw.line(screen, (0, 0, 0), (tx + (sk if slot == 0 else 0), y), (tx + (0 if slot == 0 else sk), y + h), 2)
        label = "SUPER READY!" if full else "SUPER"
        t = self.a.text(label, 16, (255, 235, 140) if full else (190, 215, 255), thick=3)
        ty = y - 24
        screen.blit(t, (x + (24 if slot == 0 else w - t.get_width() - 4), ty))

    def draw_timer(self, screen, seconds, urgent, unlimited=False):
        cx, cy = W // 2, BAR_Y + 54
        pulse = 1.0 + (0.06 * math.sin(self.t * 0.5) if urgent else 0)
        r = int(70 * pulse)
        pygame.draw.circle(screen, (0, 0, 0), (cx + 4, cy + 6), r + 6)
        pygame.draw.circle(screen, (170, 115, 35), (cx, cy), r + 4)
        pygame.draw.circle(screen, (255, 232, 150), (cx, cy), r - 2)
        pygame.draw.circle(screen, (28, 8, 14), (cx, cy), r - 9)
        pygame.draw.circle(screen, (110, 60, 25), (cx, cy), r - 16, 2)
        col = (255, 90, 70) if urgent else (255, 244, 220)
        txt = self.a.text("INF" if unlimited else f"{seconds:02d}", 44 if unlimited else 56, col, thick=5)
        screen.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2 + 2))

    def draw_gems(self, screen, wins, needed):
        for slot in (0, 1):
            for i in range(needed):
                if slot == 0:
                    cx = P1_X + 18 + i * 44
                else:
                    cx = P2_X + BAR_W - 18 - i * 44
                cy = BAR_Y + BAR_H + 138
                on = i < wins[slot]
                pts = [(cx, cy - 17), (cx + 15, cy), (cx, cy + 17), (cx - 15, cy)]
                pygame.draw.polygon(screen, (255, 200, 60) if on else (30, 12, 16), pts)
                pygame.draw.polygon(screen, (255, 235, 160) if on else (140, 100, 50), pts, 3)
                if on:
                    pygame.draw.polygon(screen, (255, 255, 230), [(cx, cy - 11), (cx + 6, cy - 2), (cx - 3, cy - 2)])

    def draw(self, screen, scene):
        screen.blit(self.vignette, (0, 0))
        for slot, f in enumerate(self.f):
            self.draw_bar(screen, slot, f)
            self.draw_energy(screen, slot, f)
            self.draw_super(screen, slot, f)
        secs = max(0, math.ceil(scene.timer / 60))
        unlimited = not scene.round_seconds
        self.draw_timer(screen, secs, secs <= 10 and scene.phase == "fight" and not unlimited, unlimited)
        self.draw_gems(screen, scene.wins, scene.wins_needed)
        # combos
        for slot, f in enumerate(self.f):
            atk = self.f[1 - slot]
            if f.combo_taken >= 2 and f.state.name in ("HITSTUN", "KNOCKDOWN"):
                txt = self.a.text(f"{f.combo_taken} HITS", 54, GOLD, thick=7)
                sh = int(3 * math.sin(self.t * 1.3))
                if slot == 1:
                    screen.blit(txt, (90 + sh, 330))
                else:
                    screen.blit(txt, (W - 90 - txt.get_width() + sh, 330))
