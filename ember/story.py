"""Arcade story mode: dialogue scenes, cards, continue / results screens and the runner that links them to the fights."""
import json
import math
import os
from collections import deque

import pygame

from .constants import CHARS, DATA, GOLD, H, STAGES, W
from .effects import Ambient
from .screens import Scene, TitleScene, VsScene, blit_hint, draw_dim

PLAYER = "reno"
SPEAKER_NAMES = {"narrator": "", "voice": "VOICE OF THE EMPEROR", "emperor": "THE HOLLOW EMPEROR", "reno": "RENO",
                 "kaito": "KAITO", "brutus": "BRUTUS", "valeria": "VALERIA", "mira": "MIRA", "rudra": "RUDRA"}
BEST_PATH = os.path.join(os.path.expanduser("~"), ".ember_tournament", "arcade.json")


def load_story():
    with open(os.path.join(DATA, "story.json"), encoding="utf-8") as f:
        return json.load(f)


def best_score():
    try:
        with open(BEST_PATH) as f:
            return int(json.load(f).get("best", 0))
    except (OSError, ValueError):
        return 0


def save_best(v):
    try:
        os.makedirs(os.path.dirname(BEST_PATH), exist_ok=True)
        with open(BEST_PATH, "w") as f:
            json.dump({"best": int(v)}, f)
    except OSError:
        pass


def wrap(text, per_line):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > per_line:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        lines.append(cur)
    return lines


class Portraits:
    """Dialogue portraits, scaled and tinted once."""

    def __init__(self, assets):
        self.a = assets
        self.cache = {}

    def get(self, who, height, flip=False, dim=False):
        key = (who, height, flip, dim)
        img = self.cache.get(key)
        if img is None:
            pid = "reno" if who == "emperor" else who
            src = self.a.image(f"portrait_{pid}")
            k = height / src.get_height()
            img = pygame.transform.smoothscale(src, (max(1, int(src.get_width() * k)), height))
            if flip:
                img = pygame.transform.flip(img, True, False)
            if who == "emperor":
                img.fill((120, 60, 200, 255), special_flags=pygame.BLEND_RGBA_MULT)
                img.fill((40, 0, 70, 0), special_flags=pygame.BLEND_RGB_ADD)
            if dim:
                img.fill((105, 105, 120, 255), special_flags=pygame.BLEND_RGBA_MULT)
            self.cache[key] = img
        return img


class Shot:
    """A cutscene picture with a slow camera drift (Ken Burns pan), scaled once."""
    ZOOM = 1.14
    _cache = {}

    def __init__(self, img, seed=0):
        k = max(W * self.ZOOM / img.get_width(), H * self.ZOOM / img.get_height())
        self.img = pygame.transform.smoothscale(img, (int(img.get_width() * k), int(img.get_height() * k)))
        self.dx, self.dy = self.img.get_width() - W, self.img.get_height() - H
        self.route = seed % 4

    def draw(self, screen, t, dur=700):
        p = min(1.0, t / dur)
        p = p * p * (3 - 2 * p)
        fx, fy = ((p, 0.5), (1 - p, 0.5), (0.5, p), (0.5, 1 - p))[self.route]
        screen.blit(self.img, (0, 0), pygame.Rect(int(self.dx * fx), int(self.dy * fy), W, H))

    @classmethod
    def art(cls, *keys):
        """Cutscene illustration data/story/<key>.jpg|png for the first key that exists, else None."""
        for key in keys:
            if key in cls._cache:
                shot = cls._cache[key]
            else:
                shot = None
                for ext in ("jpg", "png"):
                    path = os.path.join(DATA, "story", f"{key}.{ext}")
                    if os.path.exists(path):
                        shot = cls(pygame.image.load(path).convert(), sum(map(ord, key)))
                        break
                cls._cache[key] = shot
            if shot:
                return shot
        return None


def bottom_shade(screen, h=520, peak=235):
    s = pygame.Surface((W, h), pygame.SRCALPHA)
    for y in range(h):
        pygame.draw.line(s, (0, 0, 0, int(peak * (y / h) ** 0.7)), (0, y), (W, y))
    screen.blit(s, (0, H - h))


# ====================================================================== dialogue
class StoryScene(Scene):
    SIZE, PER_LINE = 28, 51

    def __init__(self, app, lines, bg, left, right, on_done, tag="", voice_prefix=None):
        super().__init__(app)
        self.lines, self.on_done, self.tag = lines, on_done, tag
        self.voice_prefix = voice_prefix
        self.voiced = False
        self.bg = bg
        self.stage_shot = Shot(bg, sum(map(ord, voice_prefix or "x")))
        self.shot, self.shot_t = None, 0
        self.left, self.right_default = left, right
        self.por = Portraits(self.a)
        self.i = 0
        self.n = 0.0
        self.t = 0
        self.embers = Ambient("embers")
        self.render_line()
        self.audio.music("menu")

    def cur(self):
        return self.lines[self.i]

    def render_line(self):
        ln = self.cur()
        self.wrapped = wrap(ln["text"], self.PER_LINE)
        col = (205, 205, 225) if ln["who"] in ("narrator",) else (255, 255, 255)
        self.surfs = [self.a.text(s, self.SIZE, col, thick=2, shadow=False) for s in self.wrapped]
        self.total = sum(len(s) for s in self.wrapped)
        self.n = 0.0
        key = self.voice_prefix or ""
        art = Shot.art(f"{key}_{self.i}", key) if key else None
        self.art = art is not None
        shot = art or self.stage_shot
        if shot is not self.shot:
            self.shot, self.shot_t = shot, 0
        self.audio.stop_story()
        self.voiced = bool(self.voice_prefix) and self.audio.story(f"{self.voice_prefix}_{self.i}")

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if ev.key == pygame.K_ESCAPE:
            self.audio.stop_story()
            self.on_done()
        elif ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f, pygame.K_j):
            if self.n < self.total:
                self.n = self.total
            else:
                self.i += 1
                if self.i >= len(self.lines):
                    self.audio.stop_story()
                    self.on_done()
                else:
                    self.render_line()
                    self.audio.sfx("ui_move", 0.4)

    def update(self):
        self.t += 1
        self.shot_t += 1
        self.embers.update()
        self.audio.tick_duck()
        if self.n < self.total:
            before = int(self.n)
            self.n = min(self.total, self.n + 1.1)
            if int(self.n) // 3 != before // 3 and not self.voiced:
                self.audio.sfx("ui_move", 0.18)

    def right_id(self):
        who = self.cur()["who"]
        if who in CHARS and who != self.left and who != "emperor":
            return who
        return self.right_default

    def draw(self, screen):
        self.shot.draw(screen, self.shot_t)
        if self.art:
            bottom_shade(screen)
        else:
            draw_dim(screen, 175)
        self.embers.draw(screen)
        ln = self.cur()
        who = ln["who"]
        right = self.right_id()
        # portraits (the illustrated scenes show the picture instead)
        ph = 640
        base_y = 700
        if self.left and not self.art:
            img = self.por.get(self.left, ph, False, dim=who not in (self.left,))
            screen.blit(img, (80, base_y - img.get_height()))
        if right and not self.art:
            rid = "emperor" if (right == "reno" or who == "emperor") else right
            img = self.por.get(rid, ph, True, dim=who not in (rid, right))
            screen.blit(img, (W - 80 - img.get_width(), base_y - img.get_height()))
        # box
        box = pygame.Rect(150, 725, W - 300, 270)
        pygame.draw.rect(screen, (0, 0, 0), box.move(6, 8), border_radius=14)
        pygame.draw.rect(screen, (18, 8, 12), box, border_radius=14)
        pygame.draw.rect(screen, (222, 160, 52), box, 4, border_radius=14)
        name = SPEAKER_NAMES.get(who, who.upper())
        if name:
            tag = self.a.text(name, 24, GOLD if who not in ("emperor", "voice") else (190, 130, 255), thick=3)
            plate = pygame.Rect(box.x + 40, box.y - 24, tag.get_width() + 50, 50)
            pygame.draw.rect(screen, (30, 12, 16), plate, border_radius=8)
            pygame.draw.rect(screen, (222, 160, 52), plate, 3, border_radius=8)
            screen.blit(tag, (plate.x + 24, plate.y + 6))
        # typed text
        shown = int(self.n)
        y = box.y + 52
        for s in self.surfs:
            take = min(len(s_ := self.wrapped[self.surfs.index(s)]), shown)
            if take > 0:
                w = min(s.get_width(), take * self.SIZE + 8)
                screen.blit(s, (box.x + 56, y), pygame.Rect(0, 0, w, s.get_height()))
            shown = max(0, shown - len(s_))
            y += 48
        if self.n >= self.total and (self.t // 24) % 2 == 0:
            tri = [(box.right - 70, box.bottom - 46), (box.right - 40, box.bottom - 46), (box.right - 55, box.bottom - 26)]
            pygame.draw.polygon(screen, GOLD, tri)
        if self.tag:
            t = self.a.text(self.tag, 18, (230, 225, 220), thick=2)
            screen.blit(t, (W // 2 - t.get_width() // 2, 40))
        blit_hint(screen, self.app, [("ENTER", "kick", "NEXT"), ("ESC", "special", "SKIP")], H - 36, 16)


# ====================================================================== cards
class CardScene(Scene):
    """Pages of centred text on a dark picture (prologue / epilogue)."""

    def __init__(self, app, pages, bg, on_done, big_last=False, voice_prefix=None):
        super().__init__(app)
        self.pages, self.bg, self.on_done, self.big_last = pages, bg, on_done, big_last
        self.voice_prefix = voice_prefix
        self.bg_shot = Shot(bg, 7)
        self.i, self.t = 0, 0
        self.embers = Ambient("embers")
        self.audio.music("menu")
        self.speak()

    def speak(self):
        self.audio.stop_story()
        if self.voice_prefix:
            self.audio.story(f"{self.voice_prefix}_{self.i}")

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if ev.key == pygame.K_ESCAPE:
            self.audio.stop_story()
            self.on_done()
        elif ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f, pygame.K_j):
            if self.t < 25:
                self.t = 25
                return
            self.i += 1
            self.t = 0
            if self.i >= len(self.pages):
                self.audio.stop_story()
                self.on_done()
            else:
                self.speak()

    def update(self):
        self.t += 1
        self.embers.update()
        self.audio.tick_duck()

    def draw(self, screen):
        text = self.pages[min(self.i, len(self.pages) - 1)]
        last = self.i == len(self.pages) - 1 and self.big_last
        art = Shot.art(f"{self.voice_prefix}_{self.i}") if self.voice_prefix else None
        (art or self.bg_shot).draw(screen, self.t)
        if art and not last:
            bottom_shade(screen, 620, 235)
        else:
            draw_dim(screen, 190 if art else 215)
        self.embers.draw(screen)
        size = 70 if last else 30
        lines = wrap(text, 12 if last else 58)
        total_h = len(lines) * (size + 26)
        y = H // 2 - total_h // 2
        if art and not last:
            y = H - 150 - total_h
        a = min(255, self.t * 12)
        for s in lines:
            img = self.a.text(s, size, GOLD if last else (240, 235, 230), thick=4 if last else 3)
            img.set_alpha(a)
            screen.blit(img, (W // 2 - img.get_width() // 2, y))
            y += size + 26
        if self.t > 40 and (self.t // 24) % 2 == 0:
            blit_hint(screen, self.app, [("ENTER", "kick", "")], H - 80, 16)
        pg = self.a.text(f"{self.i + 1} / {len(self.pages)}", 14, (150, 145, 140), thick=2)
        screen.blit(pg, (W - pg.get_width() - 40, H - 36))


class ChapterCard(Scene):
    def __init__(self, app, ch, bg, on_done, n_fights=6, fight_no=None):
        super().__init__(app)
        self.ch, self.bg, self.on_done = ch, bg, on_done
        self.fight_no, self.n_fights = fight_no, n_fights
        self.t = 0
        self.audio.sfx("gong", 0.45)

    def handle(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f, pygame.K_j, pygame.K_ESCAPE) and self.t > 20:
            self.on_done()

    def update(self):
        self.t += 1
        if self.t > 170:
            self.on_done()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 205)
        a = min(255, self.t * 10) if self.t < 150 else max(0, 255 - (self.t - 150) * 12)
        items = [(f"CHAPTER {self.ch['id']}", 40, (255, 190, 90), 330), (self.ch["title"].upper(), 84, GOLD, 410),
                 (self.ch["place"].upper(), 24, (225, 220, 215), 560)]
        if self.fight_no:
            items.append((f"FIGHT {self.fight_no} OF {self.n_fights}", 26, (255, 120, 90), 640))
        for text, size, col, y in items:
            img = self.a.text(text, size, col, thick=5)
            k = min(1.0, self.t / 14)
            if k < 1.0:
                img = pygame.transform.smoothscale(img, (int(img.get_width() * (1.3 - 0.3 * k)), int(img.get_height() * (1.3 - 0.3 * k))))
            img.set_alpha(a)
            screen.blit(img, (W // 2 - img.get_width() // 2, y))


# ====================================================================== continue / results
class ContinueScene(Scene):
    def __init__(self, app, arcade):
        super().__init__(app)
        self.arc, self.t, self.left = arcade, 0, 10
        self.bg = self.a.image("select_bg", alpha=False)
        self.audio.announce("game_over") if False else None
        self.audio.music("menu")

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        if ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f, pygame.K_j):
            self.audio.sfx("ui_select")
            self.arc.retry()
        elif ev.key in (pygame.K_ESCAPE, pygame.K_n):
            self.arc.quit()

    def update(self):
        self.t += 1
        if self.t % 60 == 0:
            self.left -= 1
            self.audio.sfx("ui_move", 0.7)
            if self.left < 0:
                self.arc.quit()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 190)
        t = self.a.text("CONTINUE?", 110, (255, 90, 70), thick=12)
        screen.blit(t, (W // 2 - t.get_width() // 2, 220))
        n = self.a.text(str(max(0, self.left)), 240, GOLD, thick=18)
        screen.blit(n, (W // 2 - n.get_width() // 2, 400))
        blit_hint(screen, self.app, [("ENTER", "kick", "CONTINUE"), ("ESC", "special", "GIVE UP")], 820, 24, (225, 220, 215), 80)
        c = self.a.text(f"CONTINUES USED: {self.arc.continues}   (EACH COSTS 500 POINTS)", 16, (200, 195, 190), thick=2)
        screen.blit(c, (W // 2 - c.get_width() // 2, 880))


class ResultScene(Scene):
    def __init__(self, app, arcade):
        super().__init__(app)
        self.arc, self.t = arcade, 0
        self.bg = self.a.image("menu_bg", alpha=False)
        self.best_before = best_score()
        self.total = max(0, arcade.score - 500 * arcade.continues)
        self.new_best = self.total > self.best_before
        if self.new_best:
            save_best(self.total)
        self.embers = Ambient("embers")
        self.audio.music("menu")
        self.audio.announce("flawless_victory") if arcade.continues == 0 else None

    def handle(self, ev):
        if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_f) and self.t > 40:
            self.app.goto(TitleScene(self.app))

    def update(self):
        self.t += 1
        self.embers.update()

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        draw_dim(screen, 190)
        self.embers.draw(screen)
        t = self.a.text("ARCADE COMPLETE", 74, GOLD, thick=9)
        screen.blit(t, (W // 2 - t.get_width() // 2, 130))
        rows = [("FIGHTS WON", f"{self.arc.fights_won}"), ("TIME BONUS", f"{self.arc.time_bonus}"),
                ("PERFECT ROUNDS", f"{self.arc.perfect}  x 500"), ("EMBER FINISHERS", f"{self.arc.finishers}  x 300"),
                ("CONTINUES", f"{self.arc.continues}  x -500")]
        y = 320
        for k, (a, b) in enumerate(rows):
            if self.t > 20 + k * 14:
                la = self.a.text(a, 26, (235, 230, 225), thick=3)
                lb = self.a.text(b, 26, (255, 220, 150), thick=3)
                screen.blit(la, (W // 2 - 520, y))
                screen.blit(lb, (W // 2 + 520 - lb.get_width(), y))
            y += 62
        if self.t > 100:
            s = self.a.text(f"SCORE  {self.total}", 56, (255, 255, 255), thick=7)
            screen.blit(s, (W // 2 - s.get_width() // 2, 700))
            b = self.a.text(("NEW BEST!" if self.new_best else f"BEST  {max(self.best_before, self.total)}"), 28,
                            (110, 255, 140) if self.new_best else (200, 195, 190), thick=4)
            screen.blit(b, (W // 2 - b.get_width() // 2, 790))
        if self.t > 140 and (self.t // 24) % 2 == 0:
            blit_hint(screen, self.app, [("ENTER", "kick", "")], H - 80, 16)


# ====================================================================== runner
class ArcadeRun:
    """Walks the story: prologue -> (chapter card, dialogue, fight, dialogue) x chapters -> epilogue -> results."""

    def __init__(self, app):
        self.app = app
        self.story = load_story()
        self.a = app.assets
        self.steps = deque()
        self.continues = 0
        self.score = 0
        self.fights_won = 0
        self.time_bonus = 0
        self.perfect = 0
        self.finishers = 0
        self.cur = None
        self.fight_idx = 0
        self.chapters = self.story["chapters"]
        self.total_fights = sum(1 for c in self.chapters if c["opponent"])
        self.steps.append(("cards", self.story["prologue"], False))
        for ch in self.chapters:
            self.steps.append(("chapter", ch))
            if ch["before"]:
                self.steps.append(("story", ch, "before"))
            if ch["opponent"]:
                self.steps.append(("fight", ch))
            if ch["after"]:
                self.steps.append(("story", ch, "after"))
        self.steps.append(("cards", self.story["epilogue"], True))
        self.steps.append(("results",))

    def start(self):
        for cid in (PLAYER, "kaito", "valeria", "mira", "brutus", "rudra"):
            self.a.load_character(cid)
        self.a.load_fx()
        self.advance()

    def stage_img(self, ch):
        return self.a.stage(ch["stage"])

    def ai_level(self):
        base = (0.25, 0.65, 1.0)[self.app.settings.difficulty]
        return min(1.15, base + 0.05 * self.fight_idx)

    def advance(self):
        if not self.steps:
            self.quit()
            return
        step = self.steps.popleft()
        kind = step[0]
        app = self.app
        if kind == "cards":
            app.goto(CardScene(app, step[1], self.a.image("menu_bg", alpha=False), self.advance, big_last=step[2],
                               voice_prefix="epilogue" if step[2] else "prologue"))
        elif kind == "chapter":
            ch = step[1]
            self.cur = ch
            fight_no = (self.fight_idx + 1) if ch["opponent"] else None
            app.goto(ChapterCard(app, ch, self.stage_img(ch), self.advance, self.total_fights, fight_no))
        elif kind == "story":
            ch = step[1]
            lines = ch[step[2]]
            right = ch["opponent"] if ch["opponent"] else None
            app.goto(StoryScene(app, lines, self.stage_img(ch), PLAYER, right, self.advance,
                                tag=f"CHAPTER {ch['id']}  -  {ch['title'].upper()}", voice_prefix=f"ch{ch['id']}_{step[2]}"))
        elif kind == "fight":
            ch = step[1]
            self.cur = ch
            stage = next(s for s in STAGES if s["id"] == ch["stage"])
            app.goto(VsScene(app, [PLAYER, ch["opponent"]], True, stage, arcade=self, boss=bool(ch.get("boss"))))
        elif kind == "results":
            app.goto(ResultScene(app, self))

    # called by the FightScene when a match is over
    def fight_done(self, fight):
        if fight.match_winner == 0:
            st = fight.stats
            self.fights_won += 1
            self.fight_idx += 1
            self.time_bonus += st["time"] * 10
            self.perfect += st["perfect"]
            self.finishers += st["finisher"]
            self.score += 1000 + st["time"] * 10 + st["perfect"] * 500 + st["finisher"] * 300
            self.advance()
        else:
            self.app.goto(ContinueScene(self.app, self))

    def retry(self):
        self.continues += 1
        self.steps.appendleft(("fight", self.cur))
        self.advance()

    def quit(self):
        self.app.goto(TitleScene(self.app))
