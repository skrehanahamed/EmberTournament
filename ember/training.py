"""Training mode: a dummy to hit, infinite meters, an input display, damage / combo numbers and hit boxes."""
import pygame

from .constants import GOLD, GROUND, H, W
from .fighter import MOVES, Fighter, State
from .gamepad import PADS
from .input import AIController, IdleController, InputFrame
from .screens import FightScene, SelectScene, TitleScene, blit_hint, draw_dim, hint_surf

DUMMY_MODES = ("STAND", "CROUCH", "JUMP", "BLOCK", "ATTACK", "CPU")
BTN_COL = {"light": (255, 110, 200), "heavy": (80, 220, 150), "kick": (110, 120, 255), "special": (255, 90, 70), "super": (255, 200, 60)}
BTN_LETTER = {"light": "L", "heavy": "H", "kick": "K", "special": "F", "super": "S"}


class DummyController:
    """What the training dummy does. BLOCK holds back, so every hit you land is guarded."""

    def __init__(self, mode, level=0.6):
        self.mode, self.t = mode, 0
        self.ai = AIController(level) if mode == "CPU" else None

    def poll(self, f, opp):
        if self.ai:
            return self.ai.poll(f, opp)
        self.t += 1
        inp = InputFrame()
        toward = 1 if opp.x > f.x else -1
        if self.mode == "CROUCH":
            inp.down = True
        elif self.mode == "JUMP":
            inp.up = self.t % 100 == 1
        elif self.mode == "BLOCK":
            inp.left, inp.right = toward > 0, toward < 0
        elif self.mode == "ATTACK":                       # walks up and throws a punch or kick every ~1.3 s
            dist = abs(opp.x - f.x)
            if dist > 230:
                inp.left, inp.right = toward < 0, toward > 0
            elif self.t % 80 == 0 and f.state in (State.IDLE, State.WALK):
                inp.press.add("light" if (self.t // 80) % 2 else "kick")
        return inp


class Recorder:
    """Wraps the player's controller and remembers what was pressed, for the input display."""

    def __init__(self, inner, owner):
        self.inner, self.owner = inner, owner
        self.slot = getattr(inner, "slot", 0)

    def poll(self, f, opp):
        inp = self.inner.poll(f, opp)
        self.owner.record(f, inp)
        return inp


def build_lessons(keys):
    """The guided course. Every lesson says WHICH BUTTON to press (keyboard key, or the controller symbol when a pad is connected)."""
    from .screens import key_label
    k = lambda n: key_label(keys[n])
    MOVE = (f"{k('left')} / {k('right')}", "dpad", "WALK")
    return [
        dict(title="WELCOME", info=True, text=["This guide teaches you everything, step by step.",
             "Each lesson shows which button to press. Do what it says", "and the next lesson starts by itself.",
             "ESC (or the OPTIONS button) opens the menu to skip around."]),
        dict(title="WALKING", text=["Walk TOWARDS the dummy, then BACK away from it.", "Holding BACK is also how you block, you learn that soon."],
             prompt=[(f"{k('right')}", "dpad", "WALK FORWARD  (towards the enemy)"), (f"{k('left')}", "dpad", "WALK BACK")],
             need=[("walk_f", 6, "STEPS FORWARD"), ("walk_b", 6, "STEPS BACK")]),
        dict(title="JUMP AND CROUCH", text=["Jump over attacks. Crouch to make yourself smaller."],
             prompt=[(k("up"), "dpad", "JUMP  (press UP)"), (k("down"), "dpad", "CROUCH  (hold DOWN)")],
             need=[("jump", 2, "JUMPS"), ("crouch", 2, "SECONDS CROUCHING")]),
        dict(title="LIGHT PUNCH", text=["Fast and safe. Stand close to the dummy and press the button.", "Light punches are the start of every combo."],
             prompt=[(k("light"), "light", "LIGHT PUNCH")], need=[("light", 3, "LIGHT HITS")]),
        dict(title="HEAVY PUNCH", text=["Slower, but it hits hard and KNOCKS THE ENEMY DOWN."],
             prompt=[(k("heavy"), "heavy", "HEAVY PUNCH")], need=[("heavy", 3, "HEAVY HITS")]),
        dict(title="KICK", text=["The kick has the longest reach. Use it to hit from a distance."],
             prompt=[(k("kick"), "kick", "KICK")], need=[("kick", 3, "KICK HITS")]),
        dict(title="BLOCKING", text=["The dummy is going to attack you.", "HOLD the BACK direction (away from the enemy) BEFORE the hit lands.",
             "Blocking stops almost all of the damage."], mode="ATTACK",
             prompt=[(f"HOLD {k('left')}", "stick", "= BLOCK  (hold BACK)")], need=[("blocked", 3, "HITS BLOCKED")]),
        dict(title="DASHING", text=["Dash to close the gap fast or to escape.", "Keyboard: tap a direction TWICE quickly.  Controller: press the dash button."],
             prompt=[(f"{k('right')} {k('right')}", ["l1", "l2"], "DASH FORWARD"), (f"{k('left')} {k('left')}", ["l1", "l2"], "DASH BACK")],
             need=[("dash", 3, "DASHES")]),
        dict(title="EMBER FIREBALL", text=["Your orange EMBER meter lets you throw a fireball. It refills over time", "(it is unlimited here). Hit the dummy with one from far away.",
             "Motion version: DOWN, DOWN+FORWARD, FORWARD, then a punch."],
             prompt=[(k("special"), "special", "FIREBALL")], need=[("fireball", 2, "FIREBALLS THROWN"), ("fireball_hit", 1, "FIREBALL HITS")]),
        dict(title="COMBOS", text=["Chain attacks while the first one is still hitting:", "tap LIGHT PUNCH, and the INSTANT it connects tap KICK.",
             "Think of it as tap-tap, one right after the other."],
             prompt=[(k("light"), "light", "1. LIGHT PUNCH"), (k("kick"), "kick", "2. KICK  (right away)")],
             need=[("combo2", 2, "2-HIT COMBOS")]),
        dict(title="FIREBALL COMBO", text=["Add a fireball to the end of the chain for big damage:", "LIGHT, then KICK, then FIREBALL, in a quick tap-tap-tap rhythm",
             "(about a tenth of a second between presses). Land a 3-HIT combo."],
             prompt=[(k("light"), "light", "1. LIGHT"), (k("kick"), "kick", "2. KICK"), (k("special"), "special", "3. FIREBALL")],
             need=[("combo3", 1, "3-HIT COMBO")]),
        dict(title="SUPER MOVE", text=["The SUPER bar (bottom of the screen) fills as you fight.", "When it says SUPER READY, unleash it. It is your strongest attack.",
             "Meters are unlimited in training."],
             prompt=[(k("super"), ["r1", "r2"], "SUPER MOVE")], need=[("super_hit", 1, "SUPER HITS")]),
        dict(title="EMBER FINISHER", info=True, text=["When your blow wins the whole match, the enemy is stunned", "and your fighter AUTOMATICALLY launches the EMBER FINISHER.",
             "You do not press anything, just enjoy the show!", "(Turn it off or make it work on every KO in OPTIONS > SETTINGS.)"]),
        dict(title="YOU ARE READY", info=True, text=["Training complete! Now it is free practice:", "ESC / OPTIONS opens the menu: change what the dummy does,",
             "show hit boxes, restart any lesson, or pick another fighter."]),
    ]


class TrainingScene(FightScene):
    def __init__(self, app, ids, stage):
        self.hist = []                       # newest first: [direction 1-9, buttons, frames]
        self.last_dmg = self.combo_hits = self.combo_dmg = self.max_combo = 0
        self.idle_ticks = 0
        self.mode_idx = 0
        self.train_boxes = False
        self.infinite = True
        self.cnt = {}
        self.lesson_i = 0
        self.lesson_t = 0
        self.done_t = 0
        self.prev_state = None
        self.prev_x = None
        self.walk_acc = [0.0, 0.0]
        self.crouch_ticks = 0
        super().__init__(app, ids, True, stage)
        self.round_seconds = 0
        self.lessons = build_lessons(self.cfg.keys[0])
        self.f[0].controller = Recorder(self.f[0].controller, self)
        self.free_mode_idx = 0
        self.show_hint = 0
        self.start_lesson(0)

    # ---- lessons -------------------------------------------------------------------
    @property
    def lesson(self):
        return self.lessons[self.lesson_i] if self.lesson_i < len(self.lessons) else None

    def info_page(self):
        les = self.lesson
        return bool(les and les.get("info"))

    def start_lesson(self, i):
        self.lesson_i = max(0, min(len(self.lessons), i))
        self.cnt = {}
        self.walk_acc = [0.0, 0.0]
        self.crouch_ticks = 0
        self.lesson_t = 0
        self.done_t = 0
        self.reset_positions()
        les = self.lesson
        mode = les.get("mode", "STAND") if les else DUMMY_MODES[self.free_mode_idx]
        self.mode_idx = DUMMY_MODES.index(mode)
        self.set_dummy()

    def lesson_done(self):
        les = self.lesson
        if not les or les.get("info") or self.done_t:
            return False
        return all(self.cnt.get(ev, 0) >= goal for ev, goal, _ in les["need"])

    def next_lesson(self):
        self.audio.sfx("ui_select")
        self.start_lesson(self.lesson_i + 1)

    # ---- setup ----------------------------------------------------------------------
    def set_dummy(self):
        mode = DUMMY_MODES[self.mode_idx]
        self.f[1].controller = DummyController(mode, (0.25, 0.65, 1.0)[self.app.difficulty])

    def start_round(self):
        super().start_round()
        self.phase, self.pt = "fight", 0                 # no intro, no rounds: straight into practice
        self.banner = ("", 0)
        for f in self.f:
            f.state, f.timer = State.IDLE, 0
        self.audio.music("fight")

    def begin_finisher(self, w, l, direction):           # no finishers in practice
        pass

    def reset_positions(self):
        self.f[0].reset(W // 2 - 330)
        self.f[1].reset(W // 2 + 330)
        self.f[0].facing, self.f[1].facing = 1, -1
        for f in self.f:
            f.state, f.timer = State.IDLE, 0
        self.fireballs.clear()
        self.last_dmg = self.combo_hits = self.combo_dmg = 0
        self.prev_x = None

    # ---- recording / counting ---------------------------------------------------------
    def record(self, f, inp):
        if self.paused:
            return
        fwd = (int(inp.right) - int(inp.left)) * f.facing
        d = Fighter._numpad(fwd, inp.up, inp.down)
        held = {b for b in ("light", "heavy", "kick", "special", "super") if b in inp.press}
        if self.hist and self.hist[0][0] == d and not held and not self.hist[0][1]:
            self.hist[0][2] += 1
        elif self.hist and self.hist[0][0] == d and held and self.hist[0][1] == held:
            self.hist[0][2] += 1
        else:
            self.hist.insert(0, [d, held, 1])
            del self.hist[12:]

    def bump(self, ev, n=1):
        self.cnt[ev] = self.cnt.get(ev, 0) + n

    def on_move_start(self, f, name):
        super().on_move_start(f, name)
        if f is self.f[0]:
            if name == "special":
                self.bump("fireball")
            elif name == "super":
                self.bump("super_cast")

    def hit_event(self, a, d, mv, pos, projectile=False):
        p1, p2 = self.f
        if d is p2:
            before = d.hp
            d.hp += 100000                                # the dummy can never be knocked out
            super().hit_event(a, d, mv, pos, projectile)
            dealt = max(0, before + 100000 - d.hp)
            d.hp = max(1, before - dealt)
            name = next((k for k, v in MOVES.items() if v is mv), "")
            if a is p1 and d.state != State.BLOCKSTUN:
                if projectile:
                    self.bump("super_hit" if name == "super" else "fireball_hit")
                else:
                    self.bump(name)
                if dealt and d.combo_taken >= 2:
                    self.cnt["combo2"] = self.cnt.get("combo2", 0) + (1 if d.combo_taken == 2 else 0)
                if dealt and d.combo_taken >= 3:
                    self.cnt["combo3"] = 1
            if dealt:
                if d.combo_taken <= 1 or self.idle_ticks > 50:
                    self.combo_dmg = 0
                self.combo_dmg += dealt
                self.last_dmg = dealt
                self.combo_hits = d.combo_taken
                self.max_combo = max(self.max_combo, self.combo_hits)
            self.idle_ticks = 0
        else:
            super().hit_event(a, d, mv, pos, projectile)
            if d is p1 and d.state == State.BLOCKSTUN:
                self.bump("blocked")

    # ---- update ---------------------------------------------------------------------
    def update(self):
        if not self.paused:
            self.idle_ticks += 1
            self.lesson_t += 1
            p1, p2 = self.f
            p1.hp = p1.spec["hp"]
            if self.infinite:
                for f in self.f:
                    f.energy, f.super = 100.0, 100.0
                    f.fb_cooldown = 0
            if self.idle_ticks > 90 and p2.state in (State.IDLE, State.WALK, State.CROUCH, State.BLOCKSTUN):
                p2.hp = p2.spec["hp"]                     # heals a moment after the combo ends
            self.count_moves(p1)
            if self.lesson_done():
                self.done_t = 1
                self.audio.sfx("gong", 0.5)
                self.audio.sfx("ui_select")
            elif self.done_t:
                self.done_t += 1
                if self.done_t > 110:
                    self.next_lesson()
        super().update()

    def count_moves(self, p1):
        if self.prev_x is not None:
            dx = (p1.x - self.prev_x) * p1.facing
            if p1.state == State.WALK:
                self.walk_acc[0 if dx > 0 else 1] += abs(dx)
                self.cnt["walk_f"] = int(self.walk_acc[0] / 45)
                self.cnt["walk_b"] = int(self.walk_acc[1] / 45)
        self.prev_x = p1.x
        if p1.state != self.prev_state:
            if p1.state == State.JUMP_START:
                self.bump("jump")
            elif p1.state == State.DASH:
                self.bump("dash")
        self.prev_state = p1.state
        if p1.state == State.CROUCH:
            self.crouch_ticks += 1
            self.cnt["crouch"] = self.crouch_ticks // 60

    # ---- menus ----------------------------------------------------------------------
    def pad_menu(self):
        return self.paused or self.info_page()

    def pause_items(self):
        n = len(self.lessons)
        les = ("FREE PRACTICE" if self.lesson_i >= n else f"{self.lesson_i + 1}/{n}  {self.lessons[self.lesson_i]['title']}")
        return [("RESUME", None), ("LESSON:  " + les, "lesson"), ("DUMMY:  " + DUMMY_MODES[self.mode_idx], "dummy"),
                ("HIT BOXES:  " + ("ON" if self.train_boxes else "OFF"), "boxes"), ("INFINITE METERS:  " + ("ON" if self.infinite else "OFF"), "inf"),
                ("RESET POSITIONS", "reset"), ("CHARACTER SELECT", "select"), ("MAIN MENU", "menu")]

    def handle(self, ev):
        if ev.type != pygame.KEYDOWN:
            return
        k = ev.key
        if k == pygame.K_F1:
            return
        if not self.paused:
            if self.info_page() and k in (pygame.K_RETURN, pygame.K_SPACE):
                self.next_lesson()
                return
            if k == pygame.K_r:
                self.reset_positions()
                return
            if k == pygame.K_b:
                self.train_boxes = not self.train_boxes
                return
            return super().handle(ev)
        items = self.pause_items()
        key = items[self.pause_idx][1]
        if k in (pygame.K_w, pygame.K_UP):
            self.pause_idx = (self.pause_idx - 1) % len(items)
            self.audio.sfx("ui_move")
        elif k in (pygame.K_s, pygame.K_DOWN):
            self.pause_idx = (self.pause_idx + 1) % len(items)
            self.audio.sfx("ui_move")
        elif k == pygame.K_ESCAPE:
            self.paused = False
        elif k in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d, pygame.K_RETURN, pygame.K_SPACE, pygame.K_f):
            confirm = k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_f)
            step = -1 if k in (pygame.K_LEFT, pygame.K_a) else 1
            self.audio.sfx("ui_select" if confirm else "ui_move")
            if key is None and confirm:
                self.paused = False
            elif key == "lesson":
                self.start_lesson((self.lesson_i + step) % (len(self.lessons) + 1))
                if confirm:
                    self.paused = False
            elif key == "dummy":
                self.mode_idx = (self.mode_idx + step) % len(DUMMY_MODES)
                self.free_mode_idx = self.mode_idx
                self.set_dummy()
            elif key == "boxes":
                self.train_boxes = not self.train_boxes
            elif key == "inf":
                self.infinite = not self.infinite
            elif key == "reset" and confirm:
                self.reset_positions()
                self.paused = False
            elif key == "select" and confirm:
                self.app.goto(SelectScene(self.app, True, training=True))
            elif key == "menu" and confirm:
                self.app.goto(TitleScene(self.app))

    def draw_pause(self, screen):
        draw_dim(screen, 170)
        t = self.a.text("TRAINING", 80, GOLD, thick=9)
        screen.blit(t, (W // 2 - t.get_width() // 2, 150))
        for i, (label, _) in enumerate(self.pause_items()):
            on = i == self.pause_idx
            s = self.a.text(("> " + label + " <") if on else label, 34 if on else 28, GOLD if on else (225, 225, 225), thick=5)
            screen.blit(s, (W // 2 - s.get_width() // 2, 290 + i * 74))
        blit_hint(screen, self.app, [("W/S", "dpad", "MOVE / CHANGE"), ("ENTER", "kick", "SELECT"), ("ESC", "menu", "RESUME")], 950, 18, (190, 185, 180))

    # ---- drawing --------------------------------------------------------------------
    def draw(self, screen):
        super().draw(screen)
        if not self.paused:
            self.draw_training(screen)
            self.draw_guide(screen)

    def panel(self, w, h, border=(222, 160, 52)):
        p = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(p, (14, 8, 12, 232), p.get_rect(), border_radius=14)
        pygame.draw.rect(p, border, p.get_rect(), 4, border_radius=14)
        return p

    def draw_guide(self, screen):
        from .story import wrap
        a = self.a
        les = self.lesson
        n = len(self.lessons)
        if les is None:
            return
        done = self.done_t > 0
        border = (110, 255, 140) if done else (222, 160, 52)
        if les.get("info"):
            size, w = 21, 1150
            lines = wrap(" ".join(les["text"]), (w - 100) // size)
            h = 130 + len(lines) * 44 + 80
            p = self.panel(w, h, border)
            t = a.text(f"{self.lesson_i + 1}/{n}   {les['title']}", 34, GOLD, thick=5)
            p.blit(t, (w // 2 - t.get_width() // 2, 26))
            for i, ln in enumerate(lines):
                s = a.text(ln, size, (240, 235, 230), thick=3)
                p.blit(s, (w // 2 - s.get_width() // 2, 100 + i * 44))
            screen.blit(p, (W // 2 - w // 2, 250))
            blit_hint(screen, self.app, [("ENTER", "kick", "CONTINUE")], 250 + h - 40, 22, (255, 220, 150))
            return
        size, w = 17, 1150
        lines = wrap(" ".join(les["text"]), (w - 90) // size)
        needs = les["need"]
        h = 70 + len(lines) * 32 + 20 + 62 + len(needs) * 36 + 20
        p = self.panel(w, h, border)
        t = a.text(f"LESSON {self.lesson_i + 1}/{n}   {les['title']}", 28, GOLD, thick=4)
        p.blit(t, (w // 2 - t.get_width() // 2, 20))
        y = 72
        for ln in lines:
            s = a.text(ln, size, (240, 235, 230), thick=2)
            p.blit(s, (w // 2 - s.get_width() // 2, y))
            y += 32
        y += 14
        # which button to press: highlighted row with the button symbols
        prompt = hint_surf(self.app, les["prompt"], 20, (255, 225, 140), 46)
        scale = min(1.0, (w - 60) / prompt.get_width())
        if scale < 1.0:
            prompt = pygame.transform.smoothscale(prompt, (int(prompt.get_width() * scale), int(prompt.get_height() * scale)))
        p.blit(prompt, (w // 2 - prompt.get_width() // 2, y))
        y += 62
        for ev, goal, label in needs:
            cur = min(goal, self.cnt.get(ev, 0))
            lab = a.text(f"{label}   {cur}/{goal}", 15, (200, 220, 255) if cur < goal else (120, 255, 150), thick=2)
            p.blit(lab, (50, y))
            bx, bw = 560, w - 560 - 50
            pygame.draw.rect(p, (40, 30, 36), (bx, y + 2, bw, 20), border_radius=6)
            if cur:
                pygame.draw.rect(p, (110, 255, 140) if cur >= goal else (255, 190, 70), (bx, y + 2, int(bw * cur / goal), 20), border_radius=6)
            y += 36
        screen.blit(p, (W // 2 - w // 2, 222))
        if done:
            k = min(1.0, self.done_t / 10)
            msg = a.text("LESSON COMPLETE!", 64, (110, 255, 140), thick=8)
            msg.set_alpha(int(255 * k))
            screen.blit(msg, (W // 2 - msg.get_width() // 2, 222 + h + 24))

    def draw_arrow(self, screen, d, cx, cy, size=15):
        if d == 5:
            pygame.draw.circle(screen, (150, 150, 160), (cx, cy), 4)
            return
        dx = {1: -1, 4: -1, 7: -1, 3: 1, 6: 1, 9: 1}.get(d, 0)
        dy = {7: -1, 8: -1, 9: -1, 1: 1, 2: 1, 3: 1}.get(d, 0)
        n = (dx * 0.7071, dy * 0.7071) if dx and dy else (dx, dy)
        p = (-n[1], n[0])
        tip = (cx + n[0] * size, cy + n[1] * size)
        back = (cx - n[0] * size * 0.7, cy - n[1] * size * 0.7)
        pts = [tip, (back[0] + p[0] * size * 0.8, back[1] + p[1] * size * 0.8), (back[0] - p[0] * size * 0.8, back[1] - p[1] * size * 0.8)]
        pygame.draw.polygon(screen, (255, 255, 255), pts)

    def draw_training(self, screen):
        a = self.a
        # input history (left)
        x0, y0 = 22, 470
        panel = pygame.Surface((290, 12 * 40 + 56), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 110))
        screen.blit(panel, (x0 - 8, y0 - 40))
        screen.blit(a.text("INPUTS", 16, GOLD, thick=2), (x0, y0 - 30))
        pre = ("ps_" if PADS.is_ps() else "xb_") if PADS.pads else None
        for i, (d, held, n) in enumerate(self.hist[:12]):
            y = y0 + i * 40 + 14
            self.draw_arrow(screen, d, x0 + 20, y)
            x = x0 + 56
            for b in sorted(held):
                if pre and b != "super":
                    screen.blit(self.app.pad_icon(pre + b, 30), (x, y - 15))
                else:
                    pygame.draw.circle(screen, BTN_COL[b], (x + 14, y), 14)
                    screen.blit(a.text(BTN_LETTER[b], 16, (0, 0, 0), outline=(255, 255, 255), thick=1, shadow=False), (x + 6, y - 9))
                x += 36
            fr = a.text(str(n), 14, (150, 150, 165), thick=1, shadow=False)
            screen.blit(fr, (x0 + 262 - fr.get_width(), y - 8))
        # numbers (right)
        px = W - 360
        rows = [("DUMMY", DUMMY_MODES[self.mode_idx]), ("LAST HIT", f"{self.last_dmg}"), ("COMBO", f"{self.combo_hits} HITS"),
                ("COMBO DAMAGE", f"{self.combo_dmg}"), ("BEST COMBO", f"{self.max_combo} HITS")]
        panel = pygame.Surface((330, 60 + len(rows) * 52), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 110))
        screen.blit(panel, (px - 8, 262))
        screen.blit(a.text("TRAINING", 16, GOLD, thick=2), (px, 272))
        for i, (k, v) in enumerate(rows):
            screen.blit(a.text(k, 13, (190, 190, 205), thick=1, shadow=False), (px, 312 + i * 52))
            screen.blit(a.text(v, 22, (255, 255, 255), thick=3), (px, 332 + i * 52))
        blit_hint(screen, self.app, [("ESC", "menu", "TRAINING MENU"), ("R", None, "RESET"), ("B", None, "HIT BOXES")], H - 18, 14, (210, 205, 200))
