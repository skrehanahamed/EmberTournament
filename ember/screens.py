"""Screens: title, controls, character select, VS splash, the fight itself and the result menu."""
import json
import math
import os
import random

import pygame

from .constants import (DATA, CHARS, CHAR_ORDER, FINISHERS, SUPERS, GOLD, GROUND, H, K, STAGES, W,
                        WALL_L, WALL_R)
from .settings import ACTIONS, ACTION_LABELS, RESERVED, ROUND_TIMES, WIN_COUNTS
from .effects import FX, Ambient, Fireball, warm
from .fighter import ENERGY_MAX, MOVES, Fighter, State
from .hud import Hud
from .gamepad import PADS
from .input import AIController, IdleController, KeyboardController


class Scene:
    def __init__(self, app):
        self.app = app
        self.a = app.assets
        self.audio = app.audio

    def handle(self, ev):
        pass

    def pad_menu(self):
        """True when a game controller may drive the menu (False while a fight is live: the buttons are the moves)."""
        return True

    def update(self):
        pass

    def draw(self, screen):
        pass


def draw_dim(screen, alpha):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    s.fill((0, 0, 0, max(0, min(255, int(alpha)))))
    screen.blit(s, (0, 0))


def gradient_band(h, top_alpha, bottom_alpha):
    s = pygame.Surface((W, h), pygame.SRCALPHA)
    for y in range(h):
        t = y / max(1, h - 1)
        pygame.draw.line(s, (0, 0, 0, int(top_alpha + (bottom_alpha - top_alpha) * t)), (0, y), (W, y))
    return s


# ====================================================================== title
class TitleScene(Scene):
    LEVELS = [("EASY", (110, 255, 140)), ("NORMAL", (255, 220, 90)), ("HARD", (255, 90, 70))]
    # menu name -> (heading, [(label, key, description)])
    MENUS = {
        "main": ("", [
            ("ARCADE STORY", "arcade", "PLAY RENO'S STORY: SIX FIGHTS AND THE HOLLOW EMPEROR"),
            ("VERSUS", "versus", "FIGHT THE CPU, A FRIEND, OR WATCH CPU VS CPU"),
            ("TRAINING", "training", "FULL GUIDE: LEARN EVERY MOVE STEP BY STEP, THEN FREE PRACTICE"),
            ("OPTIONS", "options", "SETTINGS, CONTROLS AND KEY BINDINGS"),
            ("QUIT", "quit", "LEAVE THE GAME"),
        ]),
        "versus": ("VERSUS", [
            ("VS CPU", "vs_cpu", "YOU AGAINST THE COMPUTER"),
            ("2 PLAYERS", "vs_2p", "TWO PLAYERS ON ONE KEYBOARD"),
            ("CPU VS CPU", "cvc", "WATCH TWO COMPUTER FIGHTERS"),
            ("CPU LEVEL", "level", "HOW SMART THE COMPUTER IS   (LEFT / RIGHT TO CHANGE)"),
            ("BACK", "back", ""),
        ]),
        "options": ("OPTIONS", [
            ("SETTINGS", "settings", "VOLUME, SCREEN, ROUND TIME, FINISHER, KEY BINDINGS"),
            ("CONTROLS", "controls", "SHOW THE BUTTON LAYOUT"),
            ("BACK", "back", ""),
        ]),
    }

    def __init__(self, app):
        super().__init__(app)
        self.menu = "main"
        self.pos = {"main": 0, "versus": 0, "options": 0}
        self.switch_t = 99
        self.t = 0
        self.bg = self.a.image("menu_bg", alpha=False)
        logo = self.a.image("logo")
        s = 1040 / logo.get_width()
        self.logo = pygame.transform.smoothscale(logo, (1040, int(logo.get_height() * s)))
        self.embers = Ambient("embers")
        self.shade = pygame.Surface((W, H), pygame.SRCALPHA)
        for y in range(H):
            a = 0
            if y > 480:
                a = int(185 * min(1, (y - 480) / 260))
            pygame.draw.line(self.shade, (0, 0, 0, a), (0, y), (W, y))
        self.show_controls = False
        self.audio.music("menu")

    @property
    def items(self):
        return self.MENUS[self.menu][1]

    @property
    def idx(self):
        return self.pos[self.menu]

    @idx.setter
    def idx(self, v):
        self.pos[self.menu] = v

    def open_menu(self, name):
        self.menu = name
        self.switch_t = 0

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if self.show_controls:
            if ev.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.show_controls = False
            return
        k = ev.key
        key = self.items[self.idx][1]
        if k in (pygame.K_UP, pygame.K_w):
            self.idx = (self.idx - 1) % len(self.items)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_DOWN, pygame.K_s):
            self.idx = (self.idx + 1) % len(self.items)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d) and key == "level":
            self.app.difficulty = (self.app.difficulty + (1 if k in (pygame.K_RIGHT, pygame.K_d) else -1)) % 3
            self.audio.sfx("ui_move")
        elif k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f):
            self.audio.sfx("ui_select")
            if key == "arcade":
                from .story import ArcadeRun
                ArcadeRun(self.app).start()
            elif key in ("versus", "options"):
                self.open_menu(key)
            elif key == "back":
                self.open_menu("main")
            elif key == "vs_cpu":
                self.app.goto(SelectScene(self.app, cpu=True))
            elif key == "training":
                self.app.goto(SelectScene(self.app, cpu=True, training=True))
            elif key == "vs_2p":
                self.app.goto(SelectScene(self.app, cpu=False))
            elif key == "cvc":
                self.app.goto(SelectScene(self.app, cpu=True, cvc=True))
            elif key == "level":
                self.app.difficulty = (self.app.difficulty + 1) % 3
            elif key == "settings":
                self.app.goto(SettingsScene(self.app, TitleScene(self.app)))
            elif key == "controls":
                self.show_controls = True
            elif key == "quit":
                self.app.running = False
        elif k == pygame.K_ESCAPE:
            if self.menu == "main":
                self.app.running = False
            else:
                self.audio.sfx("ui_move")
                self.open_menu("main")

    def update(self):
        self.t += 1
        self.switch_t += 1
        self.embers.update()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.shade, (0, 0))
        self.embers.draw(screen)
        bob = int(6 * math.sin(self.t * 0.04))
        screen.blit(self.logo, (W // 2 - self.logo.get_width() // 2, 50 + bob))
        heading, items = self.MENUS[self.menu]
        k = min(1.0, self.switch_t / 10)
        slide = int((1 - (1 - k) ** 3) * 0 + (1 - k) ** 2 * 70)          # sub-menus slide in from the right
        top = 500
        sub = self.menu != "main"
        if sub:
            n = len(items)
            panel = pygame.Rect(W // 2 - 520 + slide, top - 8, 1040, 70 + n * 76)
            pygame.draw.rect(screen, (0, 0, 0), panel.move(6, 8), border_radius=14)
            pygame.draw.rect(screen, (16, 7, 11), panel, border_radius=14)
            pygame.draw.rect(screen, (222, 160, 52), panel, 4, border_radius=14)
            hd = self.a.text(heading, 26, (255, 190, 90), thick=3)
            screen.blit(hd, (panel.centerx - hd.get_width() // 2, panel.y + 18))
            y0, gap = panel.y + 78, 76
        else:
            y0, gap = top + 4, 82
        for i, (label, key, desc) in enumerate(items):
            on = i == self.idx
            col = GOLD if on else (225, 220, 215)
            size = (46 if on else 40) if sub else (62 if on else 50)
            cx = W // 2 + slide
            y = y0 + i * gap
            if key == "level":
                nm, lc = self.LEVELS[self.app.difficulty]
                lab = self.a.text(label + ":  ", size, col, thick=5)
                val = self.a.text(("< " + nm + " >") if on else nm, size, lc, thick=5)
                x = cx - (lab.get_width() + val.get_width()) // 2
                screen.blit(lab, (x, y))
                screen.blit(val, (x + lab.get_width(), y))
            else:
                txt = self.a.text(label, size, col, thick=5)
                screen.blit(txt, (cx - txt.get_width() // 2, y))
                if on:                                                    # arrow markers either side of the highlighted entry
                    bob2 = int(5 * math.sin(self.t * 0.3))
                    for sx, d in ((cx - txt.get_width() // 2 - 54 - bob2, 1), (cx + txt.get_width() // 2 + 30 + bob2, -1)):
                        pts = [(sx, y + size // 2 - 14), (sx + 24 * d, y + size // 2), (sx, y + size // 2 + 14)]
                        pygame.draw.polygon(screen, GOLD, pts)
        desc = items[self.idx][2]
        if desc:
            d = self.a.text(desc, 20, (255, 225, 170), thick=3)
            screen.blit(d, (W // 2 - d.get_width() // 2, H - 118))
        blit_hint(screen, self.app, [("W/S", "dpad", "MOVE"), ("ENTER", "kick", "SELECT"), ("ESC", "special", "BACK" if sub else "QUIT"),
                                     ("F11", None, "FULLSCREEN")], H - 48)
        if self.show_controls:
            draw_controls(screen, self.a, self.app.settings.keys, self.app)


def hint_surf(app, items, size=16, color=(200, 195, 190), gap=44):
    """One row of control hints. items = (keyboard text, controller icon or None, action).
    With a controller connected the keys turn into its button symbols (items without an icon are dropped)."""
    a = app.assets
    pad = bool(PADS.pads)
    pre = "ps_" if PADS.is_ps() else "xb_"
    parts = []
    for key, icon, act in items:
        if pad:
            if not icon:
                continue
            segs = [app.pad_icon(pre + n, int(size * 2.1)) for n in ([icon] if isinstance(icon, str) else icon)]
            if act:
                segs.append(a.text(act, size, color, thick=2))
        else:
            segs = [a.text((key + " " + act).strip(), size, color, thick=2)]
        parts.append(segs)
    widths = [sum(sg.get_width() for sg in segs) + 8 * (len(segs) - 1) for segs in parts]
    h = max(sg.get_height() for segs in parts for sg in segs)
    out = pygame.Surface((sum(widths) + gap * (len(parts) - 1), h), pygame.SRCALPHA)
    x = 0
    for segs, w in zip(parts, widths):
        for sg in segs:
            out.blit(sg, (x, (h - sg.get_height()) // 2))
            x += sg.get_width() + 8
        x += gap - 8
    return out


def blit_hint(screen, app, items, y, size=16, color=(200, 195, 190), gap=44):
    img = hint_surf(app, items, size, color, gap)
    screen.blit(img, (W // 2 - img.get_width() // 2, y - img.get_height() // 2))


def key_label(name):
    return {"return": "ENTER", "space": "SPACE", "left": "LEFT", "right": "RIGHT", "up": "UP", "down": "DOWN"}.get(name, name.upper())


def draw_controls(screen, a, keys, app=None):
    if app is not None and PADS.pads:
        draw_dim(screen, 215)
        panel = app.pad_panel("CONTROLS")
        screen.blit(panel, (W // 2 - panel.get_width() // 2, H // 2 - panel.get_height() // 2))
        blit_hint(screen, app, [("", "kick", "CLOSE")], H - 50, 20, (200, 200, 200))
        return
    draw_dim(screen, 215)
    t = a.text("CONTROLS", 70, GOLD, thick=8)
    screen.blit(t, (W // 2 - t.get_width() // 2, 90))
    k1, k2 = keys
    def pair(*acts):
        return " / ".join(key_label(k1[x]) for x in acts), " / ".join(key_label(k2[x]) for x in acts)
    rows = [("", "PLAYER 1", "PLAYER 2"), ("MOVE", *pair("left", "right")), ("JUMP / CROUCH", *pair("up", "down")),
            ("BLOCK", "HOLD BACK", "HOLD BACK"), ("LIGHT PUNCH", *pair("light")), ("HEAVY PUNCH", *pair("heavy")),
            ("KICK", *pair("kick")), ("FIREBALL (USES EMBER METER)", *pair("special"))]
    y = 230
    for r in rows:
        for j, (txt, x) in enumerate(zip(r, (260, 1200, 1560))):
            if txt:
                col = GOLD if y == 230 or j == 0 else (255, 255, 255)
                s_ = a.text(txt, 24, col, thick=3)
                screen.blit(s_, (x if j == 0 else x - s_.get_width() // 2 + 60, y))
        y += 62
    tips = ["FIREBALL ALSO WITH:  DOWN, DOWN+FORWARD, FORWARD + PUNCH", "COMBO:  LIGHT > HEAVY / KICK > FIREBALL (CANCEL AFTER A HIT)",
            "FINISHER:  THE MATCH-WINNING BLOW TRIGGERS THE EMBER FINISHER (SETTINGS: OFF / EVERY KO)"]
    for i, tip in enumerate(tips):
        s = a.text(tip, 22, (255, 220, 160), thick=3)
        screen.blit(s, (W // 2 - s.get_width() // 2, 780 + i * 46))
    s = a.text("ESC / ENTER TO CLOSE", 24, (200, 200, 200), thick=3)
    screen.blit(s, (W // 2 - s.get_width() // 2, 960))


# ====================================================================== settings
class SettingsScene(Scene):
    def __init__(self, app, back):
        super().__init__(app)
        self.back = back
        self.st = app.settings
        self.idx = 0
        self.mode = "list"           # "list" or "keys"
        self.kp = 0                  # which player's keys
        self.ki = 0                  # selected action
        self.waiting = False
        self.msg = ""
        self.t = 0
        self.bg = self.a.image("select_bg", alpha=False)
        self.rows = [
            ("AUDIO", "MUSIC VOLUME", "slider", "music"), ("AUDIO", "SOUND EFFECTS", "slider", "sfx"), ("AUDIO", "VOICES", "slider", "voice"),
            ("VIDEO", "FULLSCREEN", "toggle", "fullscreen"), ("VIDEO", "SCREEN SHAKE", "choice", "shake"),
            ("VIDEO", "FLASH EFFECTS", "choice", "flash"), ("AUDIO", "STORY VOICES", "choice", "story_voice"),
            ("CONTROLLER", "VIBRATION", "choice", "rumble"),
            ("GAME", "DIFFICULTY", "choice", "difficulty"), ("GAME", "ROUND TIME", "choice", "round_time"),
            ("GAME", "ROUNDS TO WIN", "choice", "wins_needed"), ("GAME", "EMBER FINISHER", "choice", "finisher"),
            ("KEYS", "PLAYER 1 CONTROLS", "action", "keys0"), ("KEYS", "PLAYER 2 CONTROLS", "action", "keys1"),
            ("KEYS", "RESET CONTROLS", "action", "reset_keys"), ("", "RESET ALL SETTINGS", "action", "reset_all"),
            ("", "BACK", "action", "back"),
        ]
        self.audio.music("menu") if self.audio.track is None else None

    # -- value helpers -----------------------------------------------------
    def value_text(self, key):
        st = self.st
        if key == "shake":
            return ("OFF", "LOW", "NORMAL")[st.shake]
        if key == "flash":
            return "FULL" if st.flash else "REDUCED"
        if key == "rumble":
            return ("OFF", "LOW", "NORMAL", "STRONG")[st.rumble]
        if key == "story_voice":
            return "ON" if st.story_voice else "OFF"
        if key == "difficulty":
            return ("EASY", "NORMAL", "HARD")[st.difficulty]
        if key == "round_time":
            return "NO LIMIT" if st.round_time == 0 else f"{st.round_time} SEC"
        if key == "wins_needed":
            return f"BEST OF {st.wins_needed * 2 - 1}"
        if key == "finisher":
            return ("OFF", "MATCH POINT KO", "EVERY KO")[st.finisher]
        if key == "fullscreen":
            return "ON" if st.fullscreen else "OFF"
        return ""

    def change(self, d):
        _, _, kind, key = self.rows[self.idx]
        st = self.st
        if kind == "slider":
            setattr(st, key, max(0, min(10, getattr(st, key) + d)))
            self.audio.apply_settings(st)
            if key == "sfx":
                self.audio.sfx("hit_light")
            elif key == "voice":
                self.audio.effort(0, "m", 0.9)
        elif kind == "toggle":
            if key == "fullscreen":
                self.app.toggle_fullscreen()
        elif kind == "choice":
            if key == "shake":
                st.shake = (st.shake + d) % 3
            elif key == "flash":
                st.flash = not st.flash
            elif key == "rumble":
                st.rumble = (st.rumble + d) % 4
                PADS.level = st.rumble
                PADS.buzz(0, "test")
            elif key == "story_voice":
                st.story_voice = not st.story_voice
                self.audio.apply_settings(st)
            elif key == "difficulty":
                st.difficulty = (st.difficulty + d) % 3
            elif key == "round_time":
                st.round_time = ROUND_TIMES[(ROUND_TIMES.index(st.round_time) + d) % len(ROUND_TIMES)] if st.round_time in ROUND_TIMES else 99
            elif key == "finisher":
                st.finisher = (st.finisher + d) % 3
            elif key == "wins_needed":
                st.wins_needed = WIN_COUNTS[(WIN_COUNTS.index(st.wins_needed) + d) % len(WIN_COUNTS)] if st.wins_needed in WIN_COUNTS else 2
            self.audio.sfx("ui_move")
        st.save()

    def activate(self):
        _, _, kind, key = self.rows[self.idx]
        if kind in ("choice", "toggle"):
            self.change(1)
        elif key.startswith("keys"):
            self.mode, self.kp, self.ki, self.waiting = "keys", int(key[-1]), 0, False
            self.audio.sfx("ui_select")
        elif key == "reset_keys":
            self.st.reset_keys()
            self.st.save()
            self.msg = "CONTROLS RESET"
            self.audio.sfx("ui_select")
        elif key == "reset_all":
            was_full = self.st.fullscreen
            self.st.reset_all()
            if was_full:
                self.app.toggle_fullscreen()
            self.audio.apply_settings(self.st)
            self.st.save()
            self.msg = "ALL SETTINGS RESET"
            self.audio.sfx("ui_select")
        elif key == "back":
            self.leave()

    def leave(self):
        self.st.save()
        self.app.goto(self.back)

    # -- input -------------------------------------------------------------------
    def pad_menu(self):
        return not self.waiting

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        k = ev.key
        self.msg = ""
        if self.mode == "keys":
            self.handle_keys(ev)
            return
        if k == pygame.K_ESCAPE:
            self.leave()
        elif k in (pygame.K_UP, pygame.K_w):
            self.idx = (self.idx - 1) % len(self.rows)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_DOWN, pygame.K_s):
            self.idx = (self.idx + 1) % len(self.rows)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_LEFT, pygame.K_a):
            self.change(-1)
        elif k in (pygame.K_RIGHT, pygame.K_d):
            self.change(1)
        elif k in (pygame.K_RETURN, pygame.K_SPACE):
            self.activate()

    def handle_keys(self, ev):
        k = ev.key
        keys = self.st.keys[self.kp]
        if self.waiting:
            name = pygame.key.name(k)
            if k == pygame.K_ESCAPE:
                self.waiting = False
            elif name in RESERVED or not name:
                self.msg = "THAT KEY IS RESERVED"
            else:
                act = ACTIONS[self.ki]
                for other, v in keys.items():          # swap if the key is already used by this player
                    if v == name and other != act:
                        keys[other] = keys[act]
                keys[act] = name
                self.waiting = False
                self.st.save()
                self.audio.sfx("ui_select")
            return
        if k == pygame.K_ESCAPE:
            self.mode = "list"
        elif k in (pygame.K_UP, pygame.K_w):
            self.ki = (self.ki - 1) % (len(ACTIONS) + 1)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_DOWN, pygame.K_s):
            self.ki = (self.ki + 1) % (len(ACTIONS) + 1)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_RETURN, pygame.K_SPACE):
            if self.ki == len(ACTIONS):
                self.mode = "list"
            else:
                self.waiting = True
                self.audio.sfx("ui_select")

    def update(self):
        self.t += 1

    # -- drawing -------------------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 190)
        t = self.a.text("SETTINGS" if self.mode == "list" else f"PLAYER {self.kp + 1} CONTROLS", 52, GOLD, thick=6)
        screen.blit(t, (W // 2 - t.get_width() // 2, 36))
        panel = pygame.Rect(W // 2 - 560, 120, 1120, 880)
        pygame.draw.rect(screen, (0, 0, 0), panel.move(6, 8), border_radius=16)
        pygame.draw.rect(screen, (18, 8, 12), panel, border_radius=16)
        pygame.draw.rect(screen, (222, 160, 52), panel, 4, border_radius=16)
        if self.mode == "list":
            self.draw_list(screen, panel)
        else:
            self.draw_keys(screen, panel)
        if self.msg:
            m = self.a.text(self.msg, 20, (255, 140, 110), thick=3)
            screen.blit(m, (W // 2 - m.get_width() // 2, 1010))
        if self.mode == "list":
            blit_hint(screen, self.app, [("W/S", "dpad", "MOVE / CHANGE"), ("ENTER", "kick", "SELECT"), ("ESC", "special", "BACK")], 1050, color=(210, 205, 200))
        elif self.waiting:
            blit_hint(screen, self.app, [("PRESS THE NEW KEY  (ESC CANCEL)", "menu", "CANCEL")], 1050, color=(210, 205, 200))
        else:
            blit_hint(screen, self.app, [("W/S", "dpad", "MOVE"), ("ENTER", "kick", "REBIND"), ("ESC", "special", "BACK")], 1050, color=(210, 205, 200))

    def draw_list(self, screen, panel):
        y = panel.y + 22
        last = ""
        for i, (sect, label, kind, key) in enumerate(self.rows):
            on = i == self.idx
            gap = 14 if sect and sect != last and i else 0
            y += gap
            if sect and sect != last:
                last = sect
            row = pygame.Rect(panel.x + 24, y, panel.w - 48, 54)
            if on:
                pygame.draw.rect(screen, (60, 24, 24), row, border_radius=8)
                pygame.draw.rect(screen, GOLD, row, 3, border_radius=8)
            if sect:
                tag = self.a.text(sect, 12, (150, 110, 70), thick=1, shadow=False)
                screen.blit(tag, (row.x + 14, row.y + 8))
            lab = self.a.text(label, 24, GOLD if on else (235, 230, 225), thick=3)
            screen.blit(lab, (row.x + 140, row.y + 10))
            vx = row.x + 640
            if kind == "slider":
                v = getattr(self.st, key)
                for n in range(10):
                    c = (255, 160, 50) if n < v else (58, 34, 36)
                    pygame.draw.rect(screen, c, (vx + n * 34, row.y + 14, 26, 26))
                num = self.a.text(f"{v * 10}%", 16, (230, 225, 220), thick=2)
                screen.blit(num, (vx + 350, row.y + 17))
            elif kind in ("choice", "toggle"):
                vt = self.value_text(key)
                col = (255, 220, 120) if on else (210, 205, 200)
                if key == "difficulty":
                    col = TitleScene.LEVELS[self.st.difficulty][1]
                txt = self.a.text(("<  " + vt + "  >") if on else vt, 24, col, thick=3)
                screen.blit(txt, (vx, row.y + 10))
            elif key.startswith("keys"):
                txt = self.a.text("OPEN  >", 22, (180, 200, 255) if on else (150, 160, 190), thick=3)
                screen.blit(txt, (vx, row.y + 11))
            y += 56

    def draw_keys(self, screen, panel):
        keys = self.st.keys[self.kp]
        y = panel.y + 40
        for i, act in enumerate(ACTIONS + ["back"]):
            on = i == self.ki
            row = pygame.Rect(panel.x + 120, y, panel.w - 240, 64)
            if on:
                pygame.draw.rect(screen, (60, 24, 24), row, border_radius=8)
                pygame.draw.rect(screen, GOLD, row, 3, border_radius=8)
            if act == "back":
                txt = self.a.text("DONE", 26, GOLD if on else (235, 230, 225), thick=3)
                screen.blit(txt, (row.centerx - txt.get_width() // 2, row.y + 16))
            else:
                lab = self.a.text(ACTION_LABELS[act], 26, GOLD if on else (235, 230, 225), thick=3)
                screen.blit(lab, (row.x + 30, row.y + 16))
                waiting = on and self.waiting
                kt = "PRESS A KEY..." if waiting else key_label(keys[act])
                box = self.a.text(kt, 24, (255, 140, 110) if waiting else (255, 255, 255), thick=3)
                bx = row.right - 330
                pygame.draw.rect(screen, (40, 18, 22), (bx, row.y + 8, 300, 48), border_radius=8)
                pygame.draw.rect(screen, (222, 160, 52) if on else (120, 90, 50), (bx, row.y + 8, 300, 48), 3, border_radius=8)
                screen.blit(box, (bx + 150 - box.get_width() // 2, row.y + 15))
            y += 76


# ====================================================================== select
class SelectScene(Scene):
    """Classic roster screen: portrait grid in the middle, big fighters on both sides, name banners at the bottom."""
    GRID = ["kaito", "brutus", "valeria", "mira", "rudra", "reno", "random", "soon"]
    COLS = 4
    TILE, GAP = 164, 30
    BLUE, RED = (70, 165, 255), (255, 80, 64)
    STATS = {"kaito": (7, 7, 7, 6), "brutus": (10, 4, 10, 5), "valeria": (6, 10, 5, 7), "mira": (6, 6, 5, 10),
             "rudra": (8, 6, 8, 6), "reno": (7, 7, 7, 7)}
    STAT_NAMES = ("POWER", "SPEED", "HEALTH", "RANGE")

    def __init__(self, app, cpu, cvc=False, training=False):
        super().__init__(app)
        self.cpu = cpu or cvc
        self.cvc = cvc
        self.training = training                      # one human picks both: first the fighter, then the dummy
        self.cpu_auto = self.cpu and not self.cvc and not training      # versus the CPU: it picks its own fighter once P1 has chosen
        self.cpu_t = 0
        self.cur = [0, 3]               # grid cell of each cursor
        self.ready = [False, False]
        self.pick = [None, None]        # final fighter id once confirmed
        self.t = 0
        self.go_t = None
        self.change_t = [0, 0]
        self.ready_t = [0, 0]
        self.bg = self.a.image("select_bg", alpha=False)
        self.por = {cid: self.a.image(f"portrait_{cid}") for cid in CHAR_ORDER}
        for cid in CHAR_ORDER:
            self.a.load_character(cid)
        self.embers = Ambient("embers")
        self.audio.music("menu")
        self.audio.announce("choose_your_character")
        self.tiles = {cid: self._tile(cid) for cid in CHAR_ORDER}
        self.side = [self._side_glow(self.BLUE), self._side_glow(self.RED)]
        self.big_cache = {}

    # ---- art ----------------------------------------------------------------
    def _tile(self, cid):
        n = self.TILE
        s = pygame.Surface((n, n), pygame.SRCALPHA)
        img = self.por[cid]
        iw, ih = img.get_size()
        side = min(iw, ih)
        crop = img.subsurface(pygame.Rect((iw - side) // 2, 0, side, side))
        s.fill((18, 8, 12, 255))
        s.blit(pygame.transform.smoothscale(crop, (n - 12, n - 12)), (6, 6))
        # bottom name strip
        strip = pygame.Surface((n - 12, 34), pygame.SRCALPHA)
        strip.fill((0, 0, 0, 170))
        s.blit(strip, (6, n - 40))
        name = self.a.text(CHARS[cid]["name"], 16, (255, 255, 255), thick=2, shadow=False)
        s.blit(name, ((n - name.get_width()) // 2, n - 36))
        return s

    def _side_glow(self, color):
        s = pygame.Surface((W // 2, H), pygame.SRCALPHA)
        for x in range(W // 2):
            a = int(120 * (1 - x / (W // 2)) ** 1.6)
            pygame.draw.line(s, (*color, a), (x, 0), (x, H))
        for i in range(-4, 14):  # diagonal stripes
            pygame.draw.line(s, (*color, 26), (i * 140, H), (i * 140 + 520, 0), 38)
        return s

    def cell_pos(self, i):
        c, r = i % self.COLS, i // self.COLS
        w = self.COLS * self.TILE + (self.COLS - 1) * self.GAP
        x = W // 2 - w // 2 + c * (self.TILE + self.GAP)
        y = 330 + r * (self.TILE + self.GAP)
        return x, y

    # ---- logic ----------------------------------------------------------------
    def shown_id(self, slot):
        """Fighter currently shown big for this cursor (the roulette for RANDOM)."""
        if self.pick[slot]:
            return self.pick[slot]
        if slot == 1 and self.cpu_auto:                 # the CPU shuffles through the roster until it locks in
            return CHAR_ORDER[(self.t // 4 + 2) % len(CHAR_ORDER)] if self.ready[0] else None
        cell = self.GRID[self.cur[slot]]
        if cell == "random":
            return CHAR_ORDER[(self.t // 4) % len(CHAR_ORDER)]
        if cell == "soon":
            return None
        return cell

    def move_cursor(self, slot, dx, dy):
        i = self.cur[slot]
        c, r = i % self.COLS, i // self.COLS
        rows = len(self.GRID) // self.COLS
        c = (c + dx) % self.COLS
        r = (r + dy) % rows
        self.cur[slot] = r * self.COLS + c
        self.change_t[slot] = self.t
        self.audio.sfx("ui_move")

    def confirm(self, slot):
        if self.ready[slot]:
            self.ready[slot] = False
            self.pick[slot] = None
            self.audio.sfx("ui_move")
            return
        cell = self.GRID[self.cur[slot]]
        if cell == "soon":
            return
        self.pick[slot] = random.choice(CHAR_ORDER) if cell == "random" else cell
        self.ready[slot] = True
        self.ready_t[slot] = self.t
        self.audio.sfx("ui_select")
        self.audio.effort(slot, CHARS[self.pick[slot]]["voice"], 0.9)
        if all(self.ready):
            self.go_t = 0
            self.audio.announce("prepare_yourself")

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN or self.go_t is not None:
            return
        k = ev.key
        if k == pygame.K_ESCAPE:
            if self.training and self.ready[0] and not self.ready[1]:
                self.confirm(0)                       # step back to choosing your own fighter
                return
            self.app.goto(TitleScene(self.app))
            return
        pad_no = getattr(ev, "pad", None)
        if self.cpu_auto or self.training or pad_no is not None:
            # one human: every key (and any pad) drives P1 (and the dummy in training).  Two humans: pad 0 = P1, pad 1 = P2.
            slot = (0 if not self.ready[0] else 1) if self.training else (0 if self.cpu_auto else min(1, pad_no or 0))
            dirs = {pygame.K_a: (-1, 0), pygame.K_d: (1, 0), pygame.K_w: (0, -1), pygame.K_s: (0, 1),
                    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1)}
            if pad_no is not None or self.cpu_auto or self.training:
                if k in dirs:
                    if not self.ready[slot]:
                        self.move_cursor(slot, *dirs[k])
                elif k in (pygame.K_RETURN, pygame.K_f, pygame.K_j, pygame.K_SPACE):
                    self.confirm(slot)
                return
        mv = {pygame.K_a: (0, -1, 0), pygame.K_d: (0, 1, 0), pygame.K_w: (0, 0, -1), pygame.K_s: (0, 0, 1),
              pygame.K_LEFT: (1, -1, 0), pygame.K_RIGHT: (1, 1, 0), pygame.K_UP: (1, 0, -1), pygame.K_DOWN: (1, 0, 1)}
        if k in mv:
            slot, dx, dy = mv[k]
            if not self.ready[slot]:
                self.move_cursor(slot, dx, dy)
        elif k == pygame.K_f:
            self.confirm(0)
        elif k in (pygame.K_RETURN, pygame.K_j):
            self.confirm(1)
        elif k == pygame.K_r and self.cpu and not self.cvc and not self.ready[1]:
            self.cur[1] = random.choice([0, 1, 2, 3, 4, 5])
            self.change_t[1] = self.t
            self.audio.sfx("ui_move")

    def cpu_pick(self):
        """The CPU takes a little while to 'think', then locks in a fighter that is not P1's."""
        self.cpu_t += 1
        if self.cpu_t < 50:
            return
        cid = random.choice([c for c in CHAR_ORDER if c != self.pick[0]])
        self.pick[1], self.ready[1], self.ready_t[1] = cid, True, self.t
        self.cur[1] = self.GRID.index(cid)
        self.change_t[1] = self.t
        self.audio.sfx("ui_select")
        self.audio.effort(1, CHARS[cid]["voice"], 0.9)
        self.go_t = 0
        self.audio.announce("prepare_yourself")

    def update(self):
        self.t += 1
        self.embers.update()
        if self.cpu_auto and self.go_t is None:
            if self.ready[0] and not self.ready[1]:
                self.cpu_pick()
            else:
                self.cpu_t = 0
        if self.go_t is not None:
            self.go_t += 1
            if self.go_t > 60:
                self.app.goto(StageScene(self.app, list(self.pick), self.cpu, self.cvc, self.training))

    # ---- drawing -----------------------------------------------------------------
    def big_sprite(self, cid, slot, ready):
        anims = self.a.chars[cid]["anims"]
        if ready:
            anim = anims["win"]
            idx = min(len(anim) - 1, (self.t - self.ready_t[slot]) // 7)
        else:
            anim = anims["idle"]
            idx = (self.t // 9) % len(anim)
        fr = anim[idx]
        key = (cid, "win" if ready else "idle", idx, slot)
        img = self.big_cache.get(key)
        scale = 540 / self.a.chars[cid]["stance_h"]
        if img is None:
            src = fr.img if slot == 0 else fr.flip
            img = pygame.transform.scale(src, (int(fr.w * scale), int(fr.h * scale)))
            self.big_cache[key] = img
        return img, fr, scale

    @staticmethod
    def SIDE_X(slot):
        return 330 if slot == 0 else W - 330

    def draw_fighter(self, screen, slot):
        cid = self.shown_id(slot)
        tint = self.BLUE if slot == 0 else self.RED
        screen.blit(self.side[slot] if slot == 0 else pygame.transform.flip(self.side[slot], True, False),
                    (0, 0) if slot == 0 else (W // 2, 0))
        cx = self.SIDE_X(slot)
        gy = 770
        # glowing floor ring
        pygame.draw.ellipse(screen, (*tint,), (cx - 210, gy - 24, 420, 48), 4)
        pygame.draw.ellipse(screen, (255, 255, 255), (cx - 198, gy - 18, 396, 36), 2)
        if cid is None:
            q = self.a.text("?", 280, (90, 80, 86), thick=12)
            screen.blit(q, (cx - q.get_width() // 2, gy - 520))
            return
        img, fr, scale = self.big_sprite(cid, slot, self.ready[slot])
        k = min(1.0, (self.t - self.change_t[slot]) / 10)
        slide = (1 - k) ** 2 * (-220 if slot == 0 else 220)
        left = cx + slide + (fr.ox * scale if slot == 0 else -(fr.w + fr.ox) * scale)
        top = gy + fr.oy * scale
        screen.blit(img, (int(left), int(top)))
        if self.pick[slot] is None and self.GRID[self.cur[slot]] == "random":
            pass

    def draw_banner(self, screen, slot):
        """Player panel: portrait, player tag, big name, title/role chips and four stat bars."""
        cid = self.shown_id(slot)
        tint = self.BLUE if slot == 0 else self.RED
        w, h = 700, 190
        y0 = 800
        x0 = 36 if slot == 0 else W - 36 - w
        sk = 34
        if slot == 0:
            pts = [(x0 + sk, y0), (x0 + w, y0), (x0 + w - sk, y0 + h), (x0, y0 + h)]
        else:
            pts = [(x0, y0), (x0 + w - sk, y0), (x0 + w, y0 + h), (x0 + sk, y0 + h)]
        pygame.draw.polygon(screen, (0, 0, 0), [(x + 6, y + 7) for x, y in pts])
        pygame.draw.polygon(screen, (22, 10, 14), pts)
        pygame.draw.polygon(screen, tint, pts, 5)
        pygame.draw.line(screen, tint, pts[0], pts[1], 12)
        tag = ("CPU 1" if self.cvc else "PLAYER 1") if slot == 0 else ("CPU 2" if self.cvc else ("DUMMY" if self.training else "CPU" if self.cpu else "PLAYER 2"))
        random_cell = self.GRID[self.cur[slot]] == "random" and not self.pick[slot]
        # portrait medallion on the outer side
        r = 66
        px = x0 + 100 if slot == 0 else x0 + w - 100
        py = y0 + h // 2 + 8
        pygame.draw.circle(screen, (0, 0, 0), (px + 4, py + 5), r + 7)
        pygame.draw.circle(screen, tint, (px, py), r + 6)
        pygame.draw.circle(screen, (22, 10, 14), (px, py), r + 1)
        if cid and not random_cell:
            img = self.por[cid]
            iw, ih = img.get_size()
            side = min(iw, ih)
            crop = pygame.transform.smoothscale(img.subsurface(pygame.Rect((iw - side) // 2, 0, side, side)), (r * 2 - 4, r * 2 - 4))
            mask = pygame.Surface(crop.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (r - 2, r - 2), r - 2)
            crop.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(crop, (px - r + 2, py - r + 2))
        else:
            q = self.a.text("?", 70, GOLD, thick=6)
            screen.blit(q, (px - q.get_width() // 2, py - q.get_height() // 2))
        # text column
        tx0 = x0 + 190 if slot == 0 else x0 + 40
        tx1 = x0 + w - 40 if slot == 0 else x0 + w - 190
        def put(surf, y):
            screen.blit(surf, (tx0 if slot == 0 else tx1 - surf.get_width(), y))
        put(self.a.text(tag, 16, tint, thick=2), y0 + 18)
        if random_cell:
            nm, sub = "RANDOM", "LET FATE DECIDE"
        elif cid is None:
            nm, sub = "COMING SOON", ""
        else:
            spec = CHARS[cid]
            nm, sub = spec["name"], f"{spec['title'].upper()}"
        put(self.a.text(nm, 40, (255, 255, 255), thick=5), y0 + 40)
        if cid and not random_cell:
            put(self.a.text(sub, 13, GOLD, thick=2), y0 + 92)
            role = CHARS[cid]["role"]
            chip = self.a.text(role, 13, (255, 255, 255), thick=2, shadow=False)
            cw = chip.get_width() + 22
            cx_ = tx0 if slot == 0 else tx1 - cw
            pygame.draw.rect(screen, tint, (cx_, y0 + 112, cw, 24), border_radius=5)
            screen.blit(chip, (cx_ + 11, y0 + 114))
            # stat bars (two columns of two)
            for i, (nm_, v) in enumerate(zip(self.STAT_NAMES, self.STATS[cid])):
                col, row = i % 2, i // 2
                sx = (tx0 if slot == 0 else tx1 - 220) + col * 232 if slot == 0 else tx1 - 220 - col * 0
                if slot == 1:
                    sx = tx1 - 440 + col * 232
                sy = y0 + 146 + row * 20 if False else y0 + 142 + row * 22
                lab = self.a.text(nm_, 10, (225, 220, 215), thick=1, shadow=False)
                screen.blit(lab, (sx, sy + 1))
                for k in range(10):
                    bx = sx + 76 + k * 14
                    c = CHARS[cid]["accent"] if k < v else (52, 30, 34)
                    pygame.draw.rect(screen, c, (bx, sy, 11, 12))
        if self.ready[slot]:
            r2 = self.a.text("READY!", 50, (110, 255, 140), thick=7)
            screen.blit(r2, (self.SIDE_X(slot) - r2.get_width() // 2, 150))

    def draw_cursor(self, screen, slot):
        i = self.cur[slot]
        x, y = self.cell_pos(i)
        col = self.BLUE if slot == 0 else self.RED
        n = self.TILE
        pad = 5 if slot == 0 else 11
        pulse = 0 if self.ready[slot] else int(3 * math.sin(self.t * 0.25))
        rect = pygame.Rect(x - pad - pulse, y - pad - pulse, n + 2 * (pad + pulse), n + 2 * (pad + pulse))
        width = 10 if self.ready[slot] else 6
        pygame.draw.rect(screen, col, rect, width)
        # corner brackets
        L = 34
        for cx_, cy_, dx, dy in ((rect.left, rect.top, 1, 1), (rect.right, rect.top, -1, 1),
                                 (rect.left, rect.bottom, 1, -1), (rect.right, rect.bottom, -1, -1)):
            pygame.draw.line(screen, (255, 255, 255), (cx_, cy_), (cx_ + dx * L, cy_), 4)
            pygame.draw.line(screen, (255, 255, 255), (cx_, cy_), (cx_, cy_ + dy * L), 4)
        tag = self.a.text(("C1" if self.cvc else "1P") if slot == 0 else ("C2" if self.cvc else ("CPU" if self.cpu else "2P")), 22, (255, 255, 255), thick=3)
        flag = pygame.Rect(x + 4 if slot == 0 else x + self.TILE - tag.get_width() - 24, y + 4, tag.get_width() + 20, 30)
        pygame.draw.rect(screen, col, flag)
        screen.blit(tag, (flag.x + 10, flag.y))

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 150)
        self.embers.draw(screen)
        self.draw_fighter(screen, 0)
        self.draw_fighter(screen, 1)
        # title and VS
        t = self.a.text("SELECT YOUR FIGHTER", 44, GOLD, thick=6)
        screen.blit(t, (W // 2 - t.get_width() // 2, 70))
        sub = self.a.text("CPU VS CPU" if self.cvc else ("VERSUS CPU" if self.cpu else "VERSUS 2 PLAYERS"), 20, (230, 225, 220), thick=3)
        screen.blit(sub, (W // 2 - sub.get_width() // 2, 140))
        # grid panel
        gx, gy = self.cell_pos(0)
        gw = self.COLS * self.TILE + (self.COLS - 1) * self.GAP
        gh = 2 * self.TILE + self.GAP
        panel = pygame.Rect(gx - 22, gy - 22, gw + 44, gh + 44)
        pygame.draw.rect(screen, (0, 0, 0), panel.move(5, 6), border_radius=10)
        pygame.draw.rect(screen, (20, 9, 13), panel, border_radius=10)
        pygame.draw.rect(screen, (222, 160, 52), panel, 4, border_radius=10)
        for i, cell in enumerate(self.GRID):
            x, y = self.cell_pos(i)
            if cell in CHAR_ORDER:
                dim = not any(self.cur[s] == i for s in (0, 1))
                tile = self.tiles[cell]
                if dim:
                    tile = tile.copy()
                    tile.fill((175, 175, 175, 255), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tile, (x, y))
            else:
                pygame.draw.rect(screen, (28, 14, 18), (x, y, self.TILE, self.TILE))
                label = "?" if cell == "random" else "SOON"
                col = GOLD if cell == "random" else (90, 78, 80)
                q = self.a.text(label, 90 if cell == "random" else 30, col, thick=7 if cell == "random" else 3)
                screen.blit(q, (x + (self.TILE - q.get_width()) // 2, y + (self.TILE - q.get_height()) // 2 - 12))
                if cell == "random":
                    r = self.a.text("RANDOM", 18, (255, 255, 255), thick=2, shadow=False)
                    screen.blit(r, (x + (self.TILE - r.get_width()) // 2, y + self.TILE - 34))
            pygame.draw.rect(screen, (222, 160, 52), (x, y, self.TILE, self.TILE), 3)
        self.draw_cursor(screen, 0)
        if not self.cpu_auto or self.ready[1]:
            self.draw_cursor(screen, 1)
        self.draw_banner(screen, 0)
        self.draw_banner(screen, 1)
        if PADS.pads:
            blit_hint(screen, self.app, [("", "dpad", "MOVE"), ("", "kick", "CONFIRM"), ("", "special", "BACK")], H - 40, 15, (205, 200, 195))
        else:
            hint = self.a.text(("CPU 1: A/D/W/S + F        CPU 2: ARROWS + ENTER" if self.cvc else "YOU: WASD OR ARROWS + ENTER / F        " + ("CHOOSE YOUR FIGHTER, THEN THE DUMMY" if self.training else "THE CPU PICKS ITS OWN FIGHTER" if self.cpu else "P2: ARROWS + ENTER")), 15, (205, 200, 195), thick=2)
            screen.blit(hint, (W // 2 - hint.get_width() // 2, H - 36))
        if self.go_t is not None:
            draw_dim(screen, min(230, self.go_t * 5))


# ====================================================================== stage select
class StageScene(Scene):
    OPTIONS = STAGES + [{"id": "random", "name": "RANDOM", "fx": ""}]

    def __init__(self, app, ids, cpu, cvc, training=False):
        super().__init__(app)
        self.ids, self.cpu, self.cvc, self.training = ids, cpu, cvc, training
        self.idx = 0
        self.t = 0
        self.go = None
        self.thumbs = {}
        for st in STAGES:
            img = self.a.stage(st["id"])
            self.thumbs[st["id"]] = pygame.transform.smoothscale(img, (520, 292))
        self.audio.music("menu")

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN or self.go is not None:
            return
        k = ev.key
        if k == pygame.K_ESCAPE:
            self.app.goto(SelectScene(self.app, self.cpu and not self.cvc, self.cvc, self.training))
        elif k in (pygame.K_LEFT, pygame.K_a):
            self.idx = (self.idx - 1) % len(self.OPTIONS)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_RIGHT, pygame.K_d):
            self.idx = (self.idx + 1) % len(self.OPTIONS)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f, pygame.K_j):
            self.audio.sfx("ui_select")
            self.go = 0

    def update(self):
        self.t += 1
        if self.go is not None:
            self.go += 1
            if self.go > 30:
                opt = self.OPTIONS[self.idx]
                stage = random.choice(STAGES) if opt["id"] == "random" else opt
                self.app.goto(VsScene(self.app, self.ids, self.cpu, stage, cvc=self.cvc, training=self.training))

    def draw(self, screen):
        screen.blit(self.a.image("select_bg", alpha=False), (0, 0))
        draw_dim(screen, 170)
        t = self.a.text("CHOOSE YOUR ARENA", 48, GOLD, thick=6)
        screen.blit(t, (W // 2 - t.get_width() // 2, 70))
        if self.cpu and not self.cvc:
            nm, lc = TitleScene.LEVELS[self.app.difficulty]
            d = self.a.text(f"CPU LEVEL: {nm}", 22, lc, thick=3)
            screen.blit(d, (W // 2 - d.get_width() // 2, 150))
        w, h, gap = 520, 292, 50
        x0 = W // 2 - (3 * w + 2 * gap) // 2
        for i, st in enumerate(STAGES):
            x, y = x0 + i * (w + gap), 330
            on = i == self.idx
            lift = int(8 * math.sin(self.t * 0.15)) if on else 0
            rect = pygame.Rect(x, y - lift, w, h)
            pygame.draw.rect(screen, (0, 0, 0), rect.move(6, 8))
            img = self.thumbs[st["id"]]
            if not on:
                img = img.copy()
                img.fill((120, 120, 120, 255), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(img, rect.topleft)
            pygame.draw.rect(screen, GOLD if on else (120, 90, 50), rect.inflate(10, 10), 6 if on else 3)
            n = self.a.text(st["name"], 24, (255, 255, 255) if on else (190, 190, 190), thick=3)
            screen.blit(n, (rect.centerx - n.get_width() // 2, rect.bottom + 20))
        # random option
        on = self.idx == 3
        r = self.a.text((">  RANDOM  <") if on else "RANDOM", 34 if on else 28, GOLD if on else (200, 200, 200), thick=4)
        screen.blit(r, (W // 2 - r.get_width() // 2, 760))
        blit_hint(screen, self.app, [("A/D OR ARROWS", "dpad", "CHOOSE"), ("ENTER", "kick", "FIGHT"), ("ESC", "special", "BACK")], H - 52, 17, (210, 210, 210))
        if self.go is not None:
            draw_dim(screen, min(230, self.go * 8))


# ====================================================================== versus splash
class VsScene(Scene):
    def __init__(self, app, ids, cpu, stage, cvc=False, arcade=None, boss=False, training=False):
        super().__init__(app)
        self.training = training
        self.ids, self.cpu, self.stage, self.cvc = ids, cpu, stage, cvc
        self.arcade, self.boss = arcade, boss
        self.t = 0
        self.bg = self.a.stage(stage["id"])
        self.por = [self.a.image(f"portrait_{cid}") for cid in ids]
        for cid in ids:
            self.a.load_character(cid)
        self.embers = Ambient("embers")

    def handle(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE) and self.t > 30:
            self.t = max(self.t, 150)

    def update(self):
        self.t += 1
        self.embers.update()
        if self.t == 20:
            self.audio.sfx("gong", 0.5)
        if self.t > 155 or (self.training and self.t > 40):
            if self.training:
                from .training import TrainingScene
                self.app.goto(TrainingScene(self.app, self.ids, self.stage))
                return
            self.app.goto(FightScene(self.app, self.ids, self.cpu, self.stage, cvc=self.cvc, arcade=self.arcade, boss=self.boss))

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 170)
        self.embers.draw(screen)
        k = min(1.0, self.t / 24)
        ease = 1 - (1 - k) ** 3
        for slot in (0, 1):
            img = self.por[slot]
            scale = 620 / img.get_height()
            img = pygame.transform.smoothscale(img, (int(img.get_width() * scale), 620))
            if slot == 1:
                img = pygame.transform.flip(img, True, False)
            final = 160 if slot == 0 else W - 160 - img.get_width()
            start = -img.get_width() if slot == 0 else W
            x = start + (final - start) * ease
            screen.blit(img, (int(x), 230))
            nm = "THE HOLLOW EMPEROR" if (self.boss and slot == 1) else CHARS[self.ids[slot]]["name"]
            name = self.a.text(nm, 64 if len(nm) < 12 else 38, (255, 255, 255), thick=8)
            nx = (final + img.get_width() // 2 - name.get_width() // 2)
            screen.blit(name, (int(nx - (final - x)), 870))
        if self.t > 14:
            s = 1.0 + max(0, 18 - self.t) * 0.15
            vs = self.a.text("VS", int(150 * s), (255, 90, 40), thick=14)
            screen.blit(vs, (W // 2 - vs.get_width() // 2, 400))
        st = self.a.text(self.stage["name"], 34, GOLD, thick=4)
        screen.blit(st, (W // 2 - st.get_width() // 2, 960))
        if self.arcade:
            n = self.arcade.fight_idx + 1
            hd = "FINAL FIGHT" if self.boss else f"FIGHT {n} OF {self.arcade.total_fights}"
            t = self.a.text(hd, 40, (255, 120, 90), thick=5)
            screen.blit(t, (W // 2 - t.get_width() // 2, 90))
        if self.t > 135:
            draw_dim(screen, int(255 * (self.t - 135) / 20))


# ====================================================================== the fight
class FightScene(Scene):
    def __init__(self, app, ids, cpu, stage, demo=False, cvc=False, arcade=None, boss=False):
        super().__init__(app)
        self.ids, self.cpu, self.stage, self.demo, self.cvc = ids, cpu, stage, demo, cvc
        self.arcade, self.boss = arcade, boss
        self.stats = {"time": 0, "perfect": 0, "finisher": 0}
        self.bg = self.a.stage(stage["id"])
        self.fxa = self.a.load_fx()
        self._prewarm(ids)
        self._aura = [pygame.transform.smoothscale(fr.img, (int(fr.w * 1.3), int(fr.h * 1.3))) for fr in self.fxa["super_aura"].frames]
        self.ambient = Ambient(stage["fx"])
        self.cfg = app.settings
        self.wins_needed = self.cfg.wins_needed
        self.round_seconds = self.cfg.round_time
        lvl = arcade.ai_level() if arcade else (0.25, 0.65, 1.0)[app.difficulty]
        c1 = AIController(lvl) if (demo or cvc) else KeyboardController(self.cfg.keys[0], 0)
        c2 = AIController(lvl) if (cpu or demo or cvc) else KeyboardController(self.cfg.keys[1], 1)
        self.f = [Fighter(ids[0], 0, self.a, c1, self), Fighter(ids[1], 1, self.a, c2, self)]
        for f_, c_ in zip(self.f, (c1, c2)):
            f_.pad_slot = c_.slot if isinstance(c_, KeyboardController) else None      # which controller shakes for this fighter
        PADS.level = self.cfg.rumble
        self.led_flash = {}
        for f_ in self.f:
            f_.prewarm_dance()
        try:
            self.win_quotes = json.load(open(os.path.join(DATA, "quotes.json")))
        except (OSError, ValueError):
            self.win_quotes = {}
        self.match_hold = 330 if arcade else 230          # how long the victory moment lasts before an arcade fight moves on
        self.victory_t = 0
        self.focus_off = 0
        self.phase2, self.p2_seq = False, 0                # the boss' second form (see begin_phase2)
        self._aura_v = []
        if boss:
            for fr in self.fxa["super_aura"].frames:
                im = pygame.transform.smoothscale(fr.img, (int(fr.w * 1.5), int(fr.h * 1.5)))
                im.fill((170, 70, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
                self._aura_v.append(im)
        self.hud = Hud(self.a, self.f)
        self.wins = [0, 0]
        self.round = 1
        self.fx_list, self.fireballs = [], []
        self.hitstop = 0
        self.shake_t = 0
        self.shake_amp = 0
        self.slow = 0
        self.flash = 0
        self.paused = False
        self.pause_idx = 0
        self.result_idx = 0
        self.show_hint = 420
        self.last_combo_voice = [0, 0]
        self.dev = bool(getattr(app.args, "dev", False))
        self.dev_on = True          # overlay visible
        self.dev_boxes = True
        self.dev_freeze = False
        self.dev_step = 0
        self.dev_msg = ("", 0)
        self.dev_dummy = False
        self.super_dark = 0
        self.fin = None
        self.fin_pair = None
        self.fin_title = None
        self.rings = []
        self.zoom = 1.0
        self.zoom_target = 1.0
        self.focus_x = W / 2
        self.dark = 0
        self.world = pygame.Surface((W, H), 0, self.app.screen)
        self.start_round()

    def _prewarm(self, ids):
        """Scale every big effect (and render the big banners) before the fight, so the finisher / super never stalls."""
        for cid in ids:
            col = CHARS[cid]["fireball"]
            warm(self.fxa[f"fireball_{col}"], 1.9 * K)                       # finisher projectile
            warm(self.fxa[f"fireball_{col}"], 0.85 * K)
            for sc_ in (2.8, 1.7, 2.0, 1.4):                                 # finisher explosion pieces
                warm(self.fxa[f"fireball_hit_{col}"], sc_)
            warm(self.fxa["hit_spark"], 2.4)
            sp = self.fxa[f"super_{cid}_proj"]
            warm(sp, 560 / (sum(fr.w for fr in sp.frames) / len(sp.frames)))
            sh = self.fxa[f"super_{cid}_hit"]
            warm(sh, 700 / (sum(fr.w for fr in sh.frames) / len(sh.frames)))
            self.a.text(FINISHERS[cid], 56, (255, 255, 255), thick=8)
            self.a.text(SUPERS[cid], 56, (255, 255, 255), thick=8)
        warm(self.fxa["super_burst"], 3.0)
        warm(self.fxa["dust"], 0.5)
        warm(self.fxa["dust"], K)
        for txt, size, colr in (("FINISH HIM!", 110, (255, 70, 50)), ("FINISHER!", 110, (255, 190, 60)), ("K.O.", 150, (255, 70, 50)),
                                ("FIGHT!", 150, (255, 190, 60))):
            self.a.text(txt, size, colr, thick=14)
        self.a.text("EMBER FINISHER", 20, (255, 220, 150), thick=3)
        self.a.text("SUPER MOVE", 20, (255, 220, 150), thick=3)

    # ---- services used by fighters ----------------------------------------
    def sfx(self, name, vol=1.0):
        self.audio.sfx(name, vol)

    def fx(self, name, x, y, scale=1.0, rate=3, flip=False):
        e = FX(self.fxa[name], x, y, rate=rate, scale=scale * (K if name == "dust" else 1.0), flip=flip)
        e.behind = name == "dust"
        self.fx_list.append(e)

    def update_led(self):
        """The pad's light bar shows the player's colour, flashes white on a hit, throbs red at low health, gold in a finisher."""
        for f in self.f:
            slot = getattr(f, "pad_slot", None)
            if slot is None:
                continue
            col = tuple(f.spec["accent"])
            ratio = f.hp / max(1, f.spec["hp"])
            if self.fin:
                k = 0.55 + 0.45 * math.sin(self.hud.t * 0.35)
                col = (int(255 * k), int(140 * k), 20)
            elif self.led_flash.get(slot, 0) > 0:
                self.led_flash[slot] -= 1
                col = (255, 255, 255)
            elif 0 < ratio < 0.3:
                k = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(self.hud.t * 0.28))
                col = (int(255 * k), 0, 0)
            PADS.led(slot, col)

    def buzz(self, f, name, scale=1.0):
        PADS.buzz(getattr(f, "pad_slot", None), name, scale)
        if name.startswith(("hit_", "fire_hit", "super_hit")) and not name.endswith("_a") and getattr(f, "pad_slot", None) is not None:
            self.led_flash[f.pad_slot] = 5

    def shake(self, amp):
        self.shake_t = 10
        self.shake_amp = max(self.shake_amp, int(amp * (0, 0.5, 1.0)[self.cfg.shake]))

    def on_move_start(self, f, name):
        if name == "super":
            self.buzz(f, "super_start")
            self.audio.effort(f.slot, f.spec["voice"], 1.0, "win")
            self.audio.sfx("gong", 0.7)
            self.audio.sfx("fireball_cast", 0.9)
            self.hitstop = 38
            self.super_dark = 70
            self.flash = 5
            self.fin_title = (f.spec.get("super_name", SUPERS[f.cid]), 0, f.spec["accent"], "SUPER MOVE")
            burst = FX(self.fxa["super_burst"], f.x, GROUND - f.stance_h * 0.5, rate=5, scale=3.0)
            burst.ignore_hitstop = True
            self.fx_list.append(burst)
        elif name == "special":
            self.buzz(f, "cast")
            self.audio.effort(f.slot, f.spec["voice"], 0.95)
        else:
            self.audio.sfx("whoosh_heavy" if name != "light" else "whoosh_light", 0.5)
            if random.random() < 0.4:
                self.audio.effort(f.slot, f.spec["voice"], 0.7)

    def spawn_fireball(self, f):
        tx, ty = f.tip_world()
        anim = self.fxa[f"fireball_{f.spec['fireball']}"]
        x = f.x + f.facing * 150 * K
        fb = Fireball(f, x, ty, f.facing, f.spec["fb_speed"], anim, scale=0.85 * K)
        fb.move = f.move if f.move in ("special", "super") else "special"
        if fb.move == "super":
            sanim = self.fxa[f"super_{f.cid}_proj"]
            sc = 560 / (sum(fr.w for fr in sanim.frames) / len(sanim.frames))
            fb = Fireball(f, f.x + f.facing * 260, ty - 10, f.facing, f.spec["fb_speed"] * 0.9, sanim, scale=sc)
            fb.move, fb.rscale = "super", 2.4
        if self.fin and self.fin["state"] == "cast" and f is self.fin["w"]:
            fb = Fireball(f, f.x + f.facing * 210, ty - 20, f.facing, f.spec["fb_speed"] * 0.62, anim, scale=1.9 * K)
            fb.finisher, fb.rscale = True, 2.1
        self.fireballs.append(fb)
        self.audio.sfx("fireball_cast", 1.0 if fb.finisher else 0.8)

    # ---- round flow ---------------------------------------------------------
    def start_round(self):
        self.f[0].reset(W // 2 - 330)
        self.f[1].reset(W // 2 + 330)
        self.f[0].facing, self.f[1].facing = 1, -1
        self.f[0].state = self.f[1].state = State.INTRO
        self.fireballs.clear()
        self.fin = None
        self.rings = []
        self.zoom_target = 1.0
        self.timer = (self.round_seconds or 999) * 60
        self.phase = "intro"
        self.pt = 0
        self.banner = ("", 0)
        final = self.wins[0] == 1 and self.wins[1] == 1
        self.audio.music("final" if final else "fight")

    def end_round(self, winner, text):
        self.phase, self.pt = "end", 0
        self.round_text = text
        self.winner = winner
        if winner >= 0:
            self.wins[winner] += 1
        if winner == 0:                                  # numbers for the arcade score
            self.stats["time"] += max(0, self.timer // 60) if self.round_seconds else 0
            self.stats["perfect"] += 1 if self.f[0].hp >= self.f[0].spec["hp"] else 0
            self.stats["finisher"] += 1 if text == "FINISHER!" else 0
        if text == "K.O." and 0 <= winner <= 1:
            self.buzz(self.f[1 - winner], "ko")
            self.buzz(self.f[winner], "round")
        if text in ("K.O.", "FINISHER!"):
            self.audio.sfx("gong", 0.8)
            self.audio.sfx("hit_heavy", 1.0)
            self.slow = 44
            self.flash = 10
            loser = self.f[1 - winner]
            self.audio.effort(loser.slot, loser.spec["voice"], 1.0)
            if self.f[winner].hp >= self.f[winner].spec["hp"]:
                self.pending_flawless = True
        elif text.startswith("TIME"):
            self.audio.announce("time")
        else:
            self.audio.announce("tie")

    def phase_logic(self):
        self.pt += 1
        if self.phase == "intro":
            if self.pt == 10:
                n = min(self.round, 3)
                final = self.wins[0] == 1 and self.wins[1] == 1
                self.audio.announce("final_round" if final else f"round_{n}")
            if self.pt == 10:
                lead = max(self.wins) == self.wins_needed - 1 and self.wins_needed > 1 and self.cfg.finisher == 1
                self.banner = ("FINAL ROUND" if self.wins == [1, 1] else ("MATCH POINT" if lead else f"ROUND {self.round}"), 0)
            if self.pt == 78:
                self.banner = ("FIGHT!", 0)
                self.audio.announce("fight")
                self.audio.sfx("gong", 0.45)
            if self.pt >= 140:
                self.phase, self.pt = "fight", 0
                self.banner = ("", 0)
                for f in self.f:
                    f.state, f.timer = State.IDLE, 0
        elif self.phase == "end":
            if self.pt == 2:
                self.banner = (self.round_text, 0)
            if self.pt == 40:
                self.zoom_target = 1.0
            if self.pt == 95 and self.winner >= 0 and max(self.wins) < self.wins_needed:
                self.banner = (f"{CHARS[self.ids[self.winner]]['name']} WINS!", 0)
            if self.pt == 50 and self.winner >= 0:
                w = self.f[self.winner]
                w.win()
                self.audio.effort(w.slot, w.spec["voice"], 1.0, "win")
            if self.pt == 80 and getattr(self, "pending_flawless", False):
                self.pending_flawless = False
                self.audio.announce("flawless_victory")
            if self.pt >= 230:
                if max(self.wins) >= self.wins_needed:
                    self.phase, self.pt = "match", 0
                    w = 0 if self.wins[0] >= self.wins_needed else 1
                    self.match_winner = w
                    self.victory_t = 0
                    self.f[w].dancing = True
                    self.f[w].win()
                    self.zoom_target = 1.32
                    self.focus_off = 0 if self.arcade else 270        # versus: the winner stands left of centre, the menu goes on the right
                    self.focus_x = self.f[w].x + self.focus_off
                    self.banner = (f"{self.f[w].spec['name']} WINS!", 0)
                    self.audio.announce("winner" if (self.boss and w == 1) else f"win_{self.ids[w]}", 1.2)
                    self.pending_cheer = 70
                else:
                    self.round += 1
                    self.start_round()
        elif self.phase == "match":
            self.victory_t += 1
            self.audio.tick_duck()
            self.focus_x += (self.f[self.match_winner].x + self.focus_off - self.focus_x) * 0.1
            if self.victory_t == 150 and not self.arcade:
                self.banner = ("", 0)
            if self.victory_t == 100:
                self.audio.quote(self.f[self.match_winner].cid)
                self.buzz(self.f[self.match_winner], "round")
            if getattr(self, "pending_cheer", 0):
                self.pending_cheer -= 1
                if self.pending_cheer == 0:
                    wf = self.f[self.match_winner]
                    self.audio.effort(wf.slot, wf.spec["voice"], 1.0, "win")

    # ---- input -----------------------------------------------------------------
    def pad_menu(self):
        return self.paused or self.phase == "match" or self.demo

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        k = ev.key
        if self.arcade and self.phase == "match" and k in (pygame.K_RETURN, pygame.K_SPACE):
            self.pt = max(self.pt, self.match_hold + 1)
            return
        if self.phase == "match" and self.pt > 150 and not self.arcade:
            if k in (pygame.K_w, pygame.K_UP):
                self.result_idx = (self.result_idx - 1) % 3
                self.audio.sfx("ui_move")
            elif k in (pygame.K_s, pygame.K_DOWN):
                self.result_idx = (self.result_idx + 1) % 3
                self.audio.sfx("ui_move")
            elif k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f):
                self.audio.sfx("ui_select")
                if self.result_idx == 0:
                    self.app.goto(FightScene(self.app, self.ids, self.cpu, self.stage, cvc=self.cvc))
                elif self.result_idx == 1:
                    self.app.goto(SelectScene(self.app, self.cpu, self.cvc))
                else:
                    self.app.goto(TitleScene(self.app))
            return
        if self.paused:
            if k in (pygame.K_w, pygame.K_UP):
                self.pause_idx = (self.pause_idx - 1) % 4
            elif k in (pygame.K_s, pygame.K_DOWN):
                self.pause_idx = (self.pause_idx + 1) % 4
            elif k == pygame.K_ESCAPE:
                self.paused = False
            elif k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f):
                if self.pause_idx == 0:
                    self.paused = False
                elif self.pause_idx == 1:
                    self.app.goto(SettingsScene(self.app, self))
                elif self.pause_idx == 2 and not self.arcade:
                    self.app.goto(SelectScene(self.app, self.cpu, self.cvc))
                else:
                    self.app.goto(TitleScene(self.app))
            return
        if k == pygame.K_ESCAPE and not self.demo:
            self.paused = True
            self.pause_idx = 0
            PADS.stop()
        elif self.dev and self.dev_key(k):
            return
        elif k == pygame.K_F1 and not self.demo and not self.cvc:
            f2 = self.f[1]
            f2.controller = KeyboardController(self.cfg.keys[1], 1) if isinstance(f2.controller, AIController) else AIController((0.25, 0.65, 1.0)[self.app.difficulty])

    # ---- developer mode ------------------------------------------------------------
    DEV_KEYS = [
        ("F2", "overlay on/off"), ("F3", "hit/hurt boxes on/off"), ("F4", "fill SUPER + EMBER (both)"),
        ("F5", "P2 down to 5 HP (one hit)"), ("F6", "heal both"), ("F7", "match point (P1 needs 1 win)"),
        ("F8", "P2 = dummy / CPU"), ("F9", "FINISHER now"), ("F10", "freeze;  . = one tick"),
        ("[ / ]", "P1 wins -/+  (round gems)"), ("F12", "instant KO P2 (real rules)"),
        ("1", "new fight vs the HOLLOW EMPEROR (boss)"), ("2", "boss: trigger FINAL FORM now"),
    ]

    def dev_say(self, text):
        self.dev_msg = (text, 150)

    def dev_key(self, k):
        p1, p2 = self.f
        if k == pygame.K_F2:
            self.dev_on = not self.dev_on
        elif k == pygame.K_F3:
            self.dev_boxes = not self.dev_boxes
        elif k == pygame.K_F4:
            for f in self.f:
                f.super, f.energy = 100.0, 100.0
            self.dev_say("SUPER + EMBER FULL")
        elif k == pygame.K_F5:
            p2.hp = 5
            self.dev_say("P2 HP = 5")
        elif k == pygame.K_F6:
            for f in self.f:
                f.hp = f.spec["hp"]
            self.dev_say("HEALED")
        elif k == pygame.K_F7:
            self.wins = [self.wins_needed - 1, 0]
            self.dev_say("MATCH POINT FOR P1")
        elif k == pygame.K_F8:
            from .input import IdleController
            self.dev_dummy = not self.dev_dummy
            p2.controller = IdleController() if self.dev_dummy else AIController((0.25, 0.65, 1.0)[self.app.difficulty])
            self.dev_say("P2 IS A DUMMY" if self.dev_dummy else "P2 IS CPU")
        elif k == pygame.K_F9:
            if self.phase == "fight" and self.fin is None:
                p2.hp = 1
                self.begin_finisher(p1, p2, 1 if p2.x >= p1.x else -1)
                self.dev_say("FINISHER FORCED")
        elif k == pygame.K_F10:
            self.dev_freeze = not self.dev_freeze
            self.dev_say("FROZEN  (. = step)" if self.dev_freeze else "RUNNING")
        elif k == pygame.K_PERIOD:
            self.dev_step += 1
        elif k == pygame.K_LEFTBRACKET:
            self.wins[0] = max(0, self.wins[0] - 1)
        elif k == pygame.K_RIGHTBRACKET:
            self.wins[0] = min(self.wins_needed, self.wins[0] + 1)
        elif k in (pygame.K_1, pygame.K_END):
            self.app.goto(FightScene(self.app, [p1.cid, "emperor"], True, self.stage, boss=True))
            return True
        elif k in (pygame.K_2, pygame.K_HOME):
            if self.boss and not self.phase2 and self.phase == "fight" and self.fin is None:
                self.begin_phase2()
                self.dev_say("FINAL FORM")
            else:
                self.dev_say("NOT A BOSS FIGHT  (press 1)" if not self.boss else "ALREADY IN FINAL FORM")
        elif k == pygame.K_F12:
            if self.phase == "fight" and self.fin is None:
                p2.hp = 1
                p2.state, p2.timer = State.IDLE, 0
                p2.back_ticks = 0
                self.hit_event(p1, p2, MOVES["heavy"], (p2.x, GROUND - 200))
                self.dev_say("KO BLOW DELIVERED")
        else:
            return False
        return True

    def draw_dev(self, world, screen):
        """Hit / hurt boxes are drawn in world space (before the camera); the info panel is drawn on the final screen."""
        if world is not None:
            for f in self.f:
                hu = f.hurtbox()
                if hu:
                    pygame.draw.rect(world, (60, 255, 90), hu, 2)
                hb = f.hitbox()
                if hb:
                    pygame.draw.rect(world, (255, 60, 60), hb, 3)
                pygame.draw.line(world, (255, 255, 0), (f.x, GROUND), (f.x, GROUND - 30), 3)
            for fb in self.fireballs:
                pygame.draw.rect(world, (255, 160, 40), fb.rect(), 2)
            return
        font = self.a.font(14)
        lines = [f"DEV MODE   {self.app.clock.get_fps():4.0f} fps   phase {self.phase}   t {self.timer // 60}s   wins {self.wins}   zoom {self.zoom:.2f}"]
        for f in self.f:
            lines.append(f"P{f.slot + 1} {f.fighter_name if hasattr(f, 'fighter_name') else f.spec['name']:8s} hp {f.hp:4d}  super {f.super:5.1f}  ember {f.energy:5.1f}  x {f.x:6.1f} y {f.y:5.1f}")
            lines.append(f"   {f.state.name:10s} move {str(f.move):8s} t {f.move_t:3d} stun {f.stun:2d} combo {f.combo_taken}")
        lines.append("")
        lines += [f"{k:7s} {v}" for k, v in self.DEV_KEYS]
        w, h = max(font.size(ln)[0] for ln in lines) + 24, 20 * len(lines) + 20
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 170))
        for i, ln in enumerate(lines):
            col = (255, 230, 120) if i == 0 else ((190, 255, 190) if ln.startswith("P") else (230, 230, 230))
            panel.blit(font.render(ln, False, col), (10, 10 + i * 20))
        screen.blit(panel, (14, 255))
        if self.dev_msg[1] > 0:
            m = self.a.text(self.dev_msg[0], 30, (255, 230, 90), thick=4)
            screen.blit(m, (W // 2 - m.get_width() // 2, 190))
            self.dev_msg = (self.dev_msg[0], self.dev_msg[1] - 1)

    # ---- update ------------------------------------------------------------------
    def update(self):
        if self.dev and self.dev_freeze:
            if self.dev_step > 0:
                self.dev_step -= 1
            else:
                return
        if self.paused:
            return
        self.update_led()
        self.ambient.update()
        for r in self.rings:
            r[2] += 1
        self.rings = [r for r in self.rings if r[2] < 26]
        self.hud.update()
        if self.fin_pair and self.phase == "end" and self.zoom_target > 1.0:
            self.zoom_target = self.fin_frame(*self.fin_pair, 1.25)       # keep both fighters framed as the loser flies back
        self.zoom += (self.zoom_target - self.zoom) * 0.07
        self.super_dark = max(0, self.super_dark - 1)
        want_dark = 150 if self.fin else (110 if self.super_dark else (70 if self.phase2 else 0))
        if self.p2_seq > 0:
            want_dark = 160
        self.dark += max(-6, min(6, want_dark - self.dark))
        self.show_hint = max(0, self.show_hint - 1)
        self.flash = max(0, self.flash - 1)
        if self.shake_t > 0:
            self.shake_t -= 1
            if self.shake_t == 0:
                self.shake_amp = 0
        if self.p2_seq > 0:                           # the boss' transformation: everything freezes, the effects play
            self.p2_seq -= 1
            if self.p2_seq in (150, 120, 90):
                self.rings.append([self.f[1].x, GROUND - 200, 0, (170, 80, 255)])
                self.shake(14)
                self.buzz(self.f[0], "hit_heavy")
                self.buzz(self.f[1], "hit_heavy")
            for e in self.fx_list:
                e.update()
            self.fx_list = [e for e in self.fx_list if not e.dead]
            return
        if self.hitstop > 0:
            self.hitstop -= 1
            for e in self.fx_list:                    # the super's opening burst keeps animating during the freeze
                if e.ignore_hitstop:
                    e.update()
            self.fx_list = [e for e in self.fx_list if not e.dead]
            return
        if self.slow > 0:
            self.slow -= 1
            if self.slow % 2:
                return
        live = self.phase == "fight"
        p1, p2 = self.f
        p1.update(p2, live)
        p2.update(p1, live)
        for f in self.f:
            if f.state in (State.IDLE, State.WALK, State.CROUCH) and f.timer > 14:
                f.combo_taken = 0
        self.separate()
        self.resolve_hits()
        self.update_finisher()
        for fb in self.fireballs:
            fb.update()
            tgt = self.f[1 - fb.owner.slot]
            hu = tgt.hurtbox()
            if hu and fb.rect().colliderect(hu) and not fb.dead:
                fb.dead = True
                if fb.finisher:
                    self.finale()
                else:
                    self.hit_event(fb.owner, tgt, MOVES[fb.move], (fb.x, fb.y), projectile=True)
        self.fireballs = [fb for fb in self.fireballs if not fb.dead]
        # fireballs cancel each other
        if len(self.fireballs) == 2 and self.fireballs[0].dir != self.fireballs[1].dir:
            if self.fireballs[0].rect().colliderect(self.fireballs[1].rect()):
                for fb in self.fireballs:
                    fb.dead = True
                    self.fx(f"fireball_hit_{fb.owner.spec['fireball']}", fb.x, fb.y, scale=0.7 * K)
                self.audio.sfx("fireball_hit", 0.6)
        for e in self.fx_list:
            e.update()
        self.fx_list = [e for e in self.fx_list if not e.dead]
        if live:
            if self.boss and not self.phase2 and self.fin is None and p2.hp <= p2.spec["hp"] * 0.5:
                self.begin_phase2()
                return
            if self.phase2:
                p2.energy = 100.0
                if self.hud.t % 480 == 0:
                    p2.super = 100.0
            if self.round_seconds:
                self.timer -= 1
            if p1.hp <= 0 and p2.hp <= 0:
                self.end_round(-1, "DRAW")
            elif p2.hp <= 0:
                self.end_round(0, "K.O.")
            elif p1.hp <= 0:
                self.end_round(1, "K.O.")
            elif self.timer <= 0:
                if p1.hp == p2.hp:
                    self.end_round(-1, "TIME UP - DRAW")
                else:
                    self.end_round(0 if p1.hp > p2.hp else 1, "TIME UP")
        self.phase_logic()
        if self.arcade and self.phase == "match" and self.pt > self.match_hold and not getattr(self, "_arc_done", False):
            self._arc_done = True
            self.arcade.fight_done(self)
            return
        if self.phase == "match" and self.demo and self.pt > 200:
            self.app.running = False
        if self.banner[0]:
            self.banner = (self.banner[0], self.banner[1] + 1)

    def separate(self):
        a, b = self.f
        if a.y > 120 or b.y > 120:
            return
        need = a.body_w + b.body_w - 14
        d = b.x - a.x
        if abs(d) < need:
            push = (need - abs(d)) / 2
            s = 1 if d >= 0 else -1
            a.x -= push * s
            b.x += push * s
            for f in (a, b):
                if f.x <= WALL_L or f.x >= WALL_R:
                    other = b if f is a else a
                    other.x += (WALL_L - f.x) * -1 if f.x <= WALL_L else (WALL_R - f.x)
            a.x = max(WALL_L, min(WALL_R, a.x))
            b.x = max(WALL_L, min(WALL_R, b.x))

    def resolve_hits(self):
        pairs = []
        for a, d in ((self.f[0], self.f[1]), (self.f[1], self.f[0])):
            hb, hu = a.hitbox(), d.hurtbox()
            if hb and hu and hb.colliderect(hu):
                pairs.append((a, d, hu, a.move, a.tip_world()))
        for a, d, hu, move, (tx, ty) in pairs:  # both lists were built first, so trades work
            self.hit_event(a, d, MOVES[move], (min(max(tx, hu.left), hu.right), ty))
            a.hit_done = True
            a.connected = True

    def hit_event(self, a, d, mv, pos, projectile=False):
        direction = 1 if d.x >= a.x else -1
        res = d.take_hit(a, mv, direction)
        if res == "none":
            return
        # super meter: attacker earns from damage dealt, defender from damage taken, both a little from blocks
        if mv is not MOVES["super"]:
            if res == "block":
                a.gain_super(3)
                d.gain_super(4)
            else:
                a.gain_super(mv["dmg"] * 0.13)
                d.gain_super(mv["dmg"] * 0.09)
        big = mv["knock"]
        if res == "block":
            self.buzz(d, "block")
            self.fx("block_spark", pos[0], pos[1], scale=0.7 * K)
            self.audio.sfx("block", 0.9)
            self.hitstop = 4
            if not projectile and (d.x <= WALL_L + 70 or d.x >= WALL_R - 70):
                a.x -= direction * mv["push"] * 0.8
        else:
            self.fx("hit_spark", pos[0], pos[1], scale=(0.62 if not big else 0.85) * K * (1.5 if mv is MOVES["super"] else 1), rate=2)
            if projectile:
                if mv is MOVES["super"]:
                    han = self.fxa[f"super_{a.cid}_hit"]
                    hs = 700 / (sum(fr.w for fr in han.frames) / len(han.frames))
                    self.fx(f"super_{a.cid}_hit", pos[0], pos[1], scale=hs, rate=4)
                    self.rings.append([pos[0], pos[1], 0, tuple(a.spec["accent"])])
                else:
                    self.fx(f"fireball_hit_{a.spec['fireball']}", pos[0], pos[1], scale=0.75 * K, rate=3)
                self.audio.sfx("fireball_hit", 0.9)
            self.audio.sfx("hit_heavy" if big else "hit_light", 1.0)
            if projectile:
                sup = mv is MOVES["super"]
                self.buzz(d, "super_hit" if sup else "fire_hit")
                self.buzz(a, "super_land" if sup else "tap")
            else:
                self.buzz(d, "hit_heavy" if big else "hit_light")
                self.buzz(a, "hit_heavy_a" if big else "hit_light_a")
            self.hitstop = mv["stop"]
            self.shake(mv["shake"])
            if random.random() < 0.55:
                self.audio.effort(d.slot, d.spec["voice"], 0.6)
            if not projectile and (d.x <= WALL_L + 70 or d.x >= WALL_R - 70):
                a.x -= direction * mv["push"] * 0.9
            if d.combo_taken == 3 and self.last_combo_voice[a.slot] < self.hud.t - 120:
                self.audio.announce("combo", 0.8)
                self.last_combo_voice[a.slot] = self.hud.t
            # the blow that would win the whole match becomes an Ember Finisher opportunity
            if (d.hp <= 0 and a.hp > 0 and self.fin is None and self.phase == "fight"
                    and (self.cfg.finisher == 2 or (self.cfg.finisher == 1 and self.wins[a.slot] + 1 >= self.wins_needed))
            and self.cfg.finisher != 0):
                self.begin_finisher(a, d, direction)

    # ---- boss second form -----------------------------------------------------------
    BOSS_LINE = "I WILL NOT BE HOLLOW AGAIN!"

    def begin_phase2(self):
        """At half health the Hollow Emperor gets a second wind: a transformation, then faster, harder, more aggressive."""
        e = self.f[1]
        self.phase2, self.p2_seq = True, 190
        self.f[0].combo_taken = 0
        e.hp = int(e.spec["hp"] * 0.6)
        e.state, e.timer, e.move = State.IDLE, 0, None
        e.vx = e.vy = 0.0
        e.y = 0.0
        e.spec["walk"] *= 1.25
        e.spec["back"] *= 1.25
        e.spec["dmg"] *= 1.2
        e.super = 100.0
        e.tint = (255, 150, 175)                                   # hotter, redder than the first form
        e.spec.update(role="FINAL FORM", accent=(255, 50, 90))
        self.hud.set_form2(1, e)
        if isinstance(e.controller, AIController):
            e.controller.level = 1.2
        self.fireballs.clear()
        self.rings.append([e.x, GROUND - 200, 0, (170, 80, 255)])
        self.rings.append([e.x, GROUND - 200, -8, (255, 255, 255)])
        burst = FX(self.fxa["super_burst"], e.x, GROUND - e.stance_h * 0.5, rate=5, scale=3.4)
        burst.ignore_hitstop = True
        self.fx_list.append(burst)
        self.flash = 8
        self.shake_t, self.shake_amp = 60, int(18 * (0, 0.5, 1.0)[self.cfg.shake])
        self.zoom_target = 1.0
        self.audio.sfx("gong", 1.0)
        self.audio.sfx("hit_heavy", 1.0)
        self.audio.effort(e.slot, e.spec["voice"], 1.0, "win")
        self.audio.music("final")
        for f in self.f:
            self.buzz(f, "fin_boom", 0.7)

    def draw_phase2(self, screen):
        if self.p2_seq <= 0:
            return
        t = 190 - self.p2_seq
        k = min(1.0, t / 14)
        title = self.a.text("FINAL FORM", 120, (200, 110, 255), thick=14)
        scale = 1.0 + (1 - k) * 1.8
        title = pygame.transform.smoothscale(title, (int(title.get_width() * scale), int(title.get_height() * scale)))
        title.set_alpha(int(255 * min(1, t / 6) * min(1, self.p2_seq / 20)))
        screen.blit(title, (W // 2 - title.get_width() // 2, 330 - title.get_height() // 2))
        if t > 50:
            line = self.a.text(self.BOSS_LINE, 36, (255, 255, 255), thick=5)
            line.set_alpha(int(255 * min(1, (t - 50) / 14) * min(1, self.p2_seq / 20)))
            screen.blit(line, (W // 2 - line.get_width() // 2, 470))

    # ---- Ember Finisher ----------------------------------------------------------
    FIN_WINDOW = 270           # ticks (4.5 s) the winner has to enter the command
    FIN_SEQ = (6, 2, 3)        # forward, down, down-forward  (+ heavy punch)

    def fin_frame(self, w, l, cap=1.32):
        """Zoom that keeps BOTH fighters (and a margin) fully on screen, and the point to centre on."""
        dist = abs(w.x - l.x)
        zoom = max(1.0, min(cap, (W * 0.80) / (dist + 560)))
        self.focus_x = (w.x + l.x) / 2
        return zoom

    def begin_finisher(self, w, l, direction):
        self.fin = dict(w=w, l=l, state="wait", t=0, prog=0, hist=[], dir=direction, armed=False,
                        auto=True, ct=0)
        self.phase, self.pt = "finisher", 0
        l.hp = 1
        l.state, l.timer, l.move = State.STUNNED, 0, None
        l.vx = l.vy = 0.0
        l.y = 0.0
        l.kd_phase = 0
        self.fireballs.clear()
        self.hitstop = 14
        self.zoom_target = self.fin_frame(w, l, 1.18)
        self.banner = ("FINISH HIM!", 0)
        self.buzz(w, "fin_start")
        self.buzz(l, "fin_start")
        self.audio.announce("kill_her" if l.cid in ("valeria", "mira") else "kill_him")
        self.audio.sfx("gong", 0.7)

    def update_finisher(self):
        fin = self.fin
        if not fin:
            return
        fin["t"] += 1
        w, l = fin["w"], fin["l"]
        self.focus_x = (w.x + l.x) / 2
        if fin["state"] == "wait" and self.cfg.shake:
            self.shake_t, self.shake_amp = 2, max(self.shake_amp, 2 + int(fin["t"] / 14) * self.cfg.shake // 2)
        if fin["state"] == "wait":
            if fin["t"] % 14 == 0:
                l.flash = 3
                self.buzz(w, "heartbeat", 0.6 + min(0.8, fin["t"] / 120))
                self.buzz(l, "heartbeat", 0.6 + min(0.8, fin["t"] / 120))
            ready = w.state in (State.IDLE, State.WALK, State.CROUCH) and w.grounded()
            trigger = False
            if fin["auto"]:
                trigger = fin["t"] >= 38 and ready
                if fin["t"] >= 80 and not ready:          # never leave the finisher hanging: take control of the winner
                    w.state, w.timer, w.move = State.IDLE, 0, None
                    w.y = w.vy = 0.0
                    trigger = True
            else:
                inp = w.controller.poll(w, l)
                fwd = (int(inp.right) - int(inp.left)) * w.facing
                d = Fighter._numpad(fwd, inp.up, inp.down)
                if not fin["hist"] or fin["hist"][-1][1] != d:
                    fin["hist"].append((fin["t"], d))
                fin["hist"] = [h for h in fin["hist"] if h[0] >= fin["t"] - 40]
                i = 0
                for _, x in fin["hist"]:
                    if i < 3 and x == self.FIN_SEQ[i]:
                        i += 1
                if i > fin["prog"]:
                    self.audio.sfx("ui_move", 0.7)
                fin["prog"] = i
                if i == 3 and "heavy" in inp.press:
                    fin["armed"] = True          # remembered until the winner is free to act
                if fin.get("armed") and ready:
                    trigger = True
            if trigger:
                self.start_cast()
            elif fin["t"] >= self.FIN_WINDOW:
                self.fin_timeout()
        elif fin["state"] == "cast":
            fin["ct"] += 1
            if fin["ct"] % 9 == 0:                       # a rumble that swells while the giant fireball flies
                self.buzz(w, "charge", min(1.6, 0.4 + fin["ct"] / 90))
                self.buzz(l, "charge", min(1.6, 0.4 + fin["ct"] / 90))
            if fin["ct"] < 60 and "slide" in fin:        # glide to the casting distance instead of jumping
                tw, tl = fin["slide"]
                w.x += (tw - w.x) * 0.16
                l.x += (tl - l.x) * 0.16
            self.zoom_target = self.fin_frame(w, l, 1.3)
            if fin["ct"] > 260:
                self.finale()

    def start_cast(self):
        fin = self.fin
        w = fin["w"]
        fin["state"], fin["ct"] = "cast", 0
        self.fin_title = (w.spec.get("finisher", FINISHERS[w.cid]), 0, w.spec["accent"])
        w.energy, w.fb_cooldown = ENERGY_MAX, 0
        w.hit_done = False
        # open the gap to ~760 px so the giant projectile is visible for a second or so before it lands
        l = fin["l"]
        want = 930
        d = 1 if l.x > w.x else -1
        tw = max(WALL_L, min(WALL_R, l.x - d * want))
        tl = l.x
        if abs(tl - tw) < want - 4:
            tl = max(WALL_L, min(WALL_R, tw + d * want))
        fin["slide"] = (tw, tl)
        w._start_move("special")
        self.banner = ("", 0)
        self.slow = 0
        self.audio.sfx("gong", 0.9)
        self.audio.sfx("fireball_cast", 0.7)

    def fin_timeout(self):
        fin = self.fin
        w, l = fin["w"], fin["l"]
        l.hp = 0
        l._go_down(State.KO, fin["dir"], 12 * K, 14 * K)
        self.fin = None
        self.zoom_target = 1.0
        self.end_round(w.slot, "K.O.")

    def finale(self):
        fin = self.fin
        if not fin:
            return
        w, l = fin["w"], fin["l"]
        cx, cy = l.x, GROUND - l.y - l.stance_h * 0.5
        color = w.spec["fireball"]
        self.fx(f"fireball_hit_{color}", cx, cy, scale=2.8, rate=4)
        self.fx("hit_spark", cx, cy, scale=2.4, rate=3)
        for dx, dy, sc in ((-150, 30, 1.7), (150, 40, 1.7), (0, -120, 1.4)):
            self.fx(f"fireball_hit_{color}", cx + dx, cy + dy, scale=sc, rate=3)
        self.rings.append([cx, cy, 0, tuple(w.spec["accent"])])
        self.rings.append([cx, cy, -8, (255, 255, 255)])
        for name, vol in (("hit_heavy", 1.0), ("fireball_hit", 1.0), ("gong", 1.0)):
            self.audio.sfx(name, vol)
        self.buzz(w, "fin_boom", 0.8)
        self.buzz(l, "fin_boom")
        l.hp = 0
        l._go_down(State.KO, fin["dir"], 15 * K, 14 * K)
        l.flash = 8
        self.fin = None
        self.fireballs.clear()
        self.fin_pair = (w, l)
        self.zoom_target = self.fin_frame(w, l, 1.25)
        self.end_round(w.slot, "FINISHER!")
        self.hitstop = 9
        self.flash = 7
        self.shake_t, self.shake_amp = 34, int(20 * (0, 0.5, 1.0)[self.cfg.shake])

    def draw_rings(self, dest, ox=0, oy=0):
        """Expanding shockwave rings from the explosion."""
        for r in self.rings:
            if r[2] < 0:
                continue
            k = r[2] / 26
            rad = int(40 + 520 * (1 - (1 - k) ** 2))
            a = int(230 * (1 - k))
            surf = pygame.Surface((rad * 2 + 8, rad * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(r[3]) + (a,), (rad + 4, rad + 4), rad, max(2, int(16 * (1 - k))))
            dest.blit(surf, (int(r[0] - rad - 4 + ox), int(r[1] - rad - 4 + oy)))

    def draw_charge(self, dest, ox=0, oy=0):
        """Glow gathering around the winner's hands while the finisher charges, and behind the giant projectile."""
        fin = self.fin
        if fin and fin["state"] == "wait":
            w = fin["w"]
            tt = fin["t"]
            cx, cy = w.x + w.facing * 40, GROUND - w.stance_h * 0.55
            for i in range(4):
                rad = int(40 + tt * 2.4 + i * 22 + 7 * math.sin(tt * 0.45 + i))
                surf = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, tuple(w.spec["accent"]) + (max(0, min(70, 14 + tt) - i * 10),), (rad, rad), rad)
                dest.blit(surf, (int(cx - rad + ox), int(cy - rad + oy)))
        if fin and fin["state"] == "cast":
            w = fin["w"]
            if w.state == State.ATTACK and w.move == "special" and w.move_frame() < MOVES["special"]["spawn"] + 1:
                tx, ty = w.tip_world()
                t = w.move_t
                for i in range(4):
                    rad = int(30 + t * 3.2 + i * 18 + 6 * math.sin(t * 0.5 + i))
                    surf = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surf, tuple(w.spec["accent"]) + (46 - i * 9,), (rad, rad), rad)
                    dest.blit(surf, (int(tx - rad + ox), int(ty - rad + oy)))
        for fb in self.fireballs:
            if fb.finisher:
                for i in range(3):
                    rad = int(90 + i * 40)
                    surf = pygame.Surface((rad * 2, rad * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surf, tuple(fb.owner.spec["accent"]) + (50 - i * 14,), (rad, rad), rad)
                    dest.blit(surf, (int(fb.x - rad + ox), int(fb.y - rad + oy)))

    def draw_finisher_title(self, screen):
        """Name card shown while a fighter performs their finisher: slides in from the side, holds, fades."""
        ft = self.fin_title
        if not ft:
            return
        name, t, col = ft[:3]
        label_txt = ft[3] if len(ft) > 3 else "EMBER FINISHER"
        total = 230 if label_txt == "EMBER FINISHER" else 90
        if t > total:
            self.fin_title = None
            return
        self.fin_title = (name, t + 1, col, label_txt)
        k = min(1.0, t / 14)
        ease = 1 - (1 - k) ** 3
        alpha = 255 if t < total - 25 else int(255 * (total - t) / 25)
        h = 104
        y = 262
        label = self.a.text(label_txt, 20, (255, 220, 150), thick=3)
        txt = self.a.text(name, 56, (255, 255, 255), thick=8)
        w = max(txt.get_width(), label.get_width()) + 150
        panel = pygame.Surface((w + 40, h + 20), pygame.SRCALPHA)
        sk = 34
        pts = [(sk, 6), (w, 6), (w - sk, h + 6), (0, h + 6)]
        pygame.draw.polygon(panel, (0, 0, 0, 170), [(x + 7, yy + 8) for x, yy in pts])
        pygame.draw.polygon(panel, (22, 8, 12, 235), pts)
        pygame.draw.polygon(panel, tuple(col) + (255,), pts, 5)
        pygame.draw.polygon(panel, tuple(col) + (255,), [(sk, 6), (w, 6), (w - 6, 24), (sk - 6, 24)])
        panel.blit(label, (80, 30))
        panel.blit(txt, (75, 52))
        panel.set_alpha(alpha)
        x = -panel.get_width() + (W // 2 - w // 2 + panel.get_width()) * ease
        screen.blit(panel, (int(x), y))

    def draw_cap(self, screen, cx, cy, kind, on, facing):
        size = 78
        rect = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
        pygame.draw.rect(screen, (0, 0, 0), rect.move(4, 5), border_radius=12)
        pygame.draw.rect(screen, (255, 236, 160) if on else (150, 110, 60), rect.inflate(6, 6), border_radius=14)
        pygame.draw.rect(screen, (255, 190, 60) if on else (34, 16, 20), rect, border_radius=12)
        if kind == "heavy":
            t = self.a.text("HVY", 22, (30, 10, 10) if on else (210, 200, 190), thick=0 if on else 2, shadow=False)
            screen.blit(t, (cx - t.get_width() // 2, cy - t.get_height() // 2))
            return
        ang = {"fwd": 0 if facing > 0 else 180, "down": 90, "df": 45 if facing > 0 else 135}[kind]
        pts = [(-20, -8), (4, -8), (4, -19), (24, 0), (4, 19), (4, 8), (-20, 8)]
        c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        poly = [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in pts]
        pygame.draw.polygon(screen, (30, 10, 10) if on else (220, 210, 200), poly)

    def draw_finisher_prompt(self, screen):
        fin = self.fin
        if not fin or fin["state"] != "wait":
            return
        w = fin["w"]
        left = max(0.0, 1 - fin["t"] / self.FIN_WINDOW)
        if not fin["auto"]:
            panel = pygame.Rect(W // 2 - 420, 205, 840, 196)
            pygame.draw.rect(screen, (0, 0, 0), panel.move(6, 7), border_radius=18)
            pygame.draw.rect(screen, (18, 8, 12), panel, border_radius=18)
            pygame.draw.rect(screen, (222, 160, 52), panel, 5, border_radius=18)
            who = "PLAYER 1" if w.slot == 0 else "PLAYER 2"
            t = self.a.text(f"{who}: ENTER THE EMBER FINISHER", 24, GOLD, thick=3)
            screen.blit(t, (W // 2 - t.get_width() // 2, panel.y + 18))
            seq = ["fwd", "down", "df", "heavy"]
            xs = [W // 2 - 240 + i * 160 for i in range(4)]
            for i, (kind, x) in enumerate(zip(seq, xs)):
                on = (i < fin["prog"]) if kind != "heavy" else bool(fin.get("armed"))
                self.draw_cap(screen, x, panel.y + 88, kind, on, w.facing)
                if i < 3:
                    pygame.draw.line(screen, (150, 110, 60), (x + 48, panel.y + 88), (x + 112, panel.y + 88), 4)
            keys = w.controller.keys if hasattr(w.controller, "keys") else {}
            def kn(n):
                return pygame.key.name(keys[n]).upper() if n in keys else "?"
            f = kn("right" if w.facing > 0 else "left")
            d = kn("down")
            hint = self.a.text(f"{f}   {d}   {d}+{f}   +   {kn('heavy')}", 20, (230, 225, 220), thick=2)
            screen.blit(hint, (W // 2 - hint.get_width() // 2, panel.y + 138))
            bar = pygame.Rect(panel.x + 40, panel.bottom - 24, panel.w - 80, 12)
            pygame.draw.rect(screen, (50, 20, 22), bar, border_radius=7)
            pygame.draw.rect(screen, (255, 120, 30) if left > 0.3 else (255, 50, 40), (bar.x, bar.y, int(bar.w * left), bar.h), border_radius=7)

    # ---- draw -------------------------------------------------------------------
    def draw(self, screen):
        ox = oy = 0
        if self.shake_t > 0 and self.shake_amp:
            ox = random.randint(-self.shake_amp, self.shake_amp)
            oy = random.randint(-self.shake_amp, self.shake_amp) // 2
        zoomed = self.zoom > 1.01
        world = self.world if zoomed else screen           # unzoomed frames are drawn straight onto the screen (one full-screen copy fewer)
        world.blit(self.bg, (ox // 2, oy // 2))
        self.ambient.draw(world)
        if self.dark > 0:
            k = max(0, 255 - int(self.dark))                # darken with one multiply instead of a full-screen alpha overlay
            world.fill((k, k, k), special_flags=pygame.BLEND_RGB_MULT)
        order = sorted(self.f, key=lambda f: (f.state in (State.ATTACK,), f.slot))
        for f in self.f:
            f.draw_shadow(world, ox, oy)
            if self.phase2 and f is self.f[1] and f.state not in (State.KO,):
                a = self._aura_v[(self.hud.t // 3) % len(self._aura_v)]
                world.blit(a, (int(f.x - a.get_width() / 2 + ox), int(GROUND - f.y - a.get_height() + 40 + oy)))
            elif f.super >= 100 and f.state not in (State.KO, State.KNOCKDOWN, State.GETUP):
                a = self._aura[(self.hud.t // 4) % len(self._aura)]
                world.blit(a, (int(f.x - a.get_width() / 2 + ox), int(GROUND - f.y - a.get_height() + 20 + oy)))
        if self.phase == "match" and self.victory_t:
            self.draw_spotlight(world, self.f[self.match_winner], ox, oy)
        for e in self.fx_list:
            if e.behind:
                e.draw(world, ox, oy)
        for f in order:
            f.draw(world, ox, oy)
        self.draw_charge(world, ox, oy)
        for fb in self.fireballs:
            fb.draw(world, ox, oy)
        for e in self.fx_list:
            if not e.behind:
                e.draw(world, ox, oy)
        self.draw_rings(world, ox, oy)
        if (self.dev and self.dev_on and self.dev_boxes) or getattr(self, "train_boxes", False):
            self.draw_dev(world, None)
        if zoomed:
            cw, ch = int(W / self.zoom), int(H / self.zoom)
            fx_ = self.focus_x if (self.fin or self.zoom_target > 1.0 or self.zoom > 1.05) else W / 2
            cx = int(max(0, min(W - cw, fx_ - cw / 2)))
            cy = int(max(0, min(H - ch, GROUND - ch * 0.66)))
            try:
                pygame.transform.scale(world.subsurface((cx, cy, cw, ch)), (W, H), screen)     # straight into the screen, no temporary copy
            except (ValueError, pygame.error):
                screen.blit(pygame.transform.scale(world.subsurface((cx, cy, cw, ch)), (W, H)), (0, 0))
        self.draw_finisher_prompt(screen)
        self.draw_finisher_title(screen)
        self.hud.draw(screen, self)
        if self.dev and self.dev_on:
            self.draw_dev(None, screen)
        self.draw_banner(screen)
        self.draw_phase2(screen)
        if self.flash:
            s = pygame.Surface((W, H))
            s.fill((255, 255, 255))
            s.set_alpha(int(220 * self.flash / 10 * (1.0 if self.cfg.flash else 0.25)))
            screen.blit(s, (0, 0))
        if self.show_hint and not self.demo and not self.fin and not self.paused:
            a = min(255, self.show_hint * 3)
            k = self.cfg.keys[0]
            kn = lambda n: key_label(k[n])
            hint = hint_surf(self.app, [(f"{kn('left')}/{kn('right')}", "dpad", "MOVE"), (f"{kn('up')}", None, "JUMP"), (f"{kn('down')}", None, "CROUCH"),
                                        (f"{kn('light')}", "light", "PUNCH"), (f"{kn('heavy')}", "heavy", "HEAVY"), (f"{kn('kick')}", "kick", "KICK"),
                                        (f"{kn('special')}", "special", "FIREBALL"), (f"{kn('super')}", ["r1", "r2"], "SUPER"),
                                        ("DOUBLE-TAP DIR", ["l1", "l2"], "DASH"), ("HOLD BACK TO", "stick", "BLOCK")], 15, (255, 255, 255), 26)
            hint.set_alpha(a)
            screen.blit(hint, (W // 2 - hint.get_width() // 2, H - 18 - hint.get_height()))
        if self.phase == "match":
            self.draw_winner_card(screen)
            self.draw_quote(screen)
        if self.phase == "match" and self.pt > 150 and not self.arcade:
            self.draw_result(screen)
        if self.paused:
            self.draw_pause(screen)

    def draw_banner(self, screen):
        text, t = self.banner
        if not text:
            return
        size = 150 if text in ("K.O.", "FIGHT!") else 110
        if len(text) > 12:
            size = 78
        k = min(1.0, t / 10)
        scale = 1.0 + (1 - k) * 1.6
        col = (255, 255, 255)
        if text == "FIGHT!":
            col = (255, 190, 60)
        elif text == "K.O." or text.startswith("TIME") or text.startswith("FINISH HIM"):
            col = (255, 70, 50)
        elif text == "FINISHER!":
            col = (255, 190, 60)
        elif "WINS" in text:
            col = GOLD
        surf = self.a.text(text, size, col, thick=14)
        scale = min(scale, (W * 0.96) / surf.get_width())
        if scale != 1.0:
            surf = pygame.transform.smoothscale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
        surf.set_alpha(int(255 * min(1, t / 6)))
        by = 470 if text.startswith("FINISH HIM") else (590 if "WINS" in text and self.phase == "match" else (540 if text == "FINISHER!" else 400))
        screen.blit(surf, (W // 2 - surf.get_width() // 2, by - surf.get_height() // 2))

    def draw_spotlight(self, world, w, ox, oy):
        """A soft coloured beam behind the winner while they celebrate."""
        k = min(1.0, self.victory_t / 30)
        cache = self.__dict__.setdefault("_spot", {})
        key = tuple(w.spec["accent"])
        beam = cache.get(key)
        if beam is None:
            beam = pygame.Surface((760, 1000), pygame.SRCALPHA)
            for y in range(1000):
                half = int(70 + 290 * y / 1000)
                a = int(95 * (1 - y / 1000) ** 0.5 * 0.9)
                pygame.draw.line(beam, key + (max(0, min(255, a)),), (380 - half, y), (380 + half, y))
            pygame.draw.ellipse(beam, key + (110,), (60, 930, 640, 70))
            cache[key] = beam
        beam.set_alpha(int(255 * k))
        world.blit(beam, (int(w.x - 380 + ox), GROUND - 980 + oy), special_flags=pygame.BLEND_RGBA_ADD if False else 0)

    def draw_quote(self, screen):
        if self.victory_t < 100:
            return
        w = self.f[self.match_winner]
        text = self.win_quotes.get(w.cid)
        if not text:
            return
        # versus: on the right under the menu (the winner stands on the left); arcade: centred, low
        cx, y0 = (W // 2, 800) if self.arcade else (1430, 740)
        size = 36 if self.arcade else 28
        n = int((self.victory_t - 100) * 0.9)
        k = min(1.0, (self.victory_t - 100) / 14)
        full = self.a.text('"' + text + '"', size, (255, 255, 255), thick=5)
        img = self.a.text('"' + text[:n] + ('"' if n >= len(text) else ""), size, (255, 255, 255), thick=5) if n > 0 else None
        name = self.a.text(w.spec["name"] if w.cid != "emperor" else "THE HOLLOW EMPEROR", 18, tuple(w.spec["accent"]), thick=3)
        bw = max(full.get_width(), name.get_width()) + 80
        band = pygame.Surface((bw, 120), pygame.SRCALPHA)
        pygame.draw.rect(band, (10, 5, 10, int(210 * k)), band.get_rect(), border_radius=16)
        pygame.draw.rect(band, tuple(w.spec["accent"]) + (int(255 * k),), band.get_rect(), 4, border_radius=16)
        screen.blit(band, (cx - bw // 2, y0))
        screen.blit(name, (cx - name.get_width() // 2, y0 + 16))
        if img:
            screen.blit(img, (cx - full.get_width() // 2, y0 + 56))

    def draw_winner_card(self, screen):
        """Match end: the winner's portrait in a ring above a gold 'NAME WINS!' plate."""
        w = self.match_winner
        f = self.f[w]
        k = min(1.0, self.pt / 18)
        ease = 1 - (1 - k) ** 3
        cx, cy = W // 2, 330
        r = int(92 * (0.6 + 0.4 * ease))
        glow = pygame.Surface((r * 5, r * 5), pygame.SRCALPHA)
        for i in range(6, 0, -1):
            pygame.draw.circle(glow, tuple(f.spec["accent"]) + (22,), (r * 5 // 2, r * 5 // 2), r + i * 16)
        screen.blit(glow, (cx - r * 5 // 2, cy - r * 5 // 2))
        pygame.draw.circle(screen, (0, 0, 0), (cx + 5, cy + 6), r + 12)
        pygame.draw.circle(screen, (255, 232, 150), (cx, cy), r + 10)
        pygame.draw.circle(screen, (170, 115, 35), (cx, cy), r + 4)
        pygame.draw.circle(screen, tuple(f.spec["accent"]), (cx, cy), r)
        por = self.a.image(f"portrait_{f.cid}")
        pw, ph = por.get_size()
        side = min(pw, ph)
        img = pygame.transform.smoothscale(por.subsurface(pygame.Rect((pw - side) // 2, 0, side, side)), (r * 2 - 8, r * 2 - 8))
        mask = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (r - 4, r - 4), r - 4)
        img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(img, (cx - r + 4, cy - r + 4))

    def draw_result(self, screen):
        draw_dim(screen, 120)
        items = ["REMATCH", "CHARACTER SELECT", "MAIN MENU"]
        for i, it in enumerate(items):
            on = i == self.result_idx
            t = self.a.text((">  " + it + "  <") if on else it, 36 if on else 30, GOLD if on else (225, 225, 225), thick=5)
            screen.blit(t, (1430 - t.get_width() // 2, 500 + i * 80))

    def draw_pause(self, screen):
        draw_dim(screen, 170)
        t = self.a.text("PAUSED", 90, GOLD, thick=10)
        screen.blit(t, (W // 2 - t.get_width() // 2, 260))
        for i, it in enumerate(["RESUME", "SETTINGS", "QUIT ARCADE" if self.arcade else "CHARACTER SELECT", "MAIN MENU"]):
            on = i == self.pause_idx
            s = self.a.text((">  " + it + "  <") if on else it, 40 if on else 34, GOLD if on else (225, 225, 225), thick=5)
            screen.blit(s, (W // 2 - s.get_width() // 2, 460 + i * 76))
        k = self.cfg.keys[0]
        kn = lambda n: key_label(k[n])
        blit_hint(screen, self.app, [(f"{kn('left')}/{kn('right')}/{kn('up')}/{kn('down')}", "dpad", "MOVE"), (kn("light"), "light", "LIGHT"),
                                     (kn("heavy"), "heavy", "HEAVY"), (kn("kick"), "kick", "KICK"), (kn("special"), "special", "FIREBALL"),
                                     (kn("super"), ["r1", "r2"], "SUPER"), ("DOUBLE-TAP", ["l1", "l2"], "DASH")], 880, 20, (225, 220, 215), 40)
        blit_hint(screen, self.app, [("W/S", "dpad", "MOVE"), ("ENTER", "kick", "SELECT"), ("ESC", "menu", "RESUME")], 960, 18, (180, 175, 170))
