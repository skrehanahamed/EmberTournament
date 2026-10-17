"""A fighter: state machine, frame data, hit/hurt boxes, blocking, combos and drawing."""
import enum
import math
import random
from collections import deque

import pygame

from .constants import CHARS, GROUND, K, WALL_L, WALL_R


class State(enum.Enum):
    INTRO = 0
    IDLE = 1
    WALK = 2
    CROUCH = 3
    JUMP_START = 4
    JUMP = 5
    LAND = 6
    ATTACK = 7
    HITSTUN = 8
    BLOCKSTUN = 9
    KNOCKDOWN = 10
    GETUP = 11
    KO = 12
    WIN = 13
    STUNNED = 14
    DASH = 15


# Frame data at 60 ticks per second. "dur" is how many ticks each animation frame lasts, "active" the
# animation frames whose pose can hit (taken from where the art shows the limb extended).
MOVES = {
    "light": dict(anim="punch_light", dur=[2, 2, 3, 3, 4], active=[2, 3], dmg=45, hitstun=17, blockstun=11,
                  push=11, knock=False, reach=(170, 130), stop=5, shake=0),
    "heavy": dict(anim="punch_heavy", dur=[3, 4, 4, 3, 4, 5, 6], active=[4, 5], dmg=95, hitstun=26, blockstun=17,
                  push=22, knock=True, reach=(210, 150), stop=9, shake=7, lunge=7),
    "kick": dict(anim="kick", dur=[2, 3, 3, 4, 4, 3, 3], active=[3, 4], dmg=75, hitstun=21, blockstun=14,
                 push=18, knock=False, reach=(250, 170), stop=7, shake=4),
    "special": dict(anim="special", dur=[3, 4, 4, 3, 5, 5, 6, 6], spawn=4, dmg=90, hitstun=24, blockstun=16,
                    push=18, knock=True, reach=(0, 0), stop=8, shake=6),
}
MOVES["super"] = dict(anim="special", dur=[4, 6, 6, 5, 8, 8, 9, 9], spawn=4, dmg=230, hitstun=32, blockstun=22,
                      push=30, knock=True, reach=(0, 0), stop=14, shake=16, chip=0.2)
CANCELS = {"light": ("heavy", "kick", "special", "super"), "heavy": ("special", "super"), "kick": ("special", "super"),
           "special": ("super",), "super": ()}
SUPER_MAX = 100.0
DASH_TICKS = 13
DASH_SPEED = 17.0       # px per tick (before K) forward
BACKDASH_SPEED = 13.0

GRAVITY = 1.6 * K
JUMP_V = 32.0 * K
BUFFER = 7
ENERGY_MAX = 100.0
ENERGY_COST = 34.0       # three fireballs from a full meter
ENERGY_REGEN = 0.30      # per tick: an empty meter refills in about 5.5 seconds


class Fighter:
    def __init__(self, cid, slot, assets, controller, game):
        self.cid = cid
        self.spec = dict(CHARS[cid])
        for key in ("walk", "back", "body_w", "fb_speed"):
            self.spec[key] = self.spec[key] * K
        self.slot = slot
        self.A = assets.load_character(cid)["anims"]
        self.stance_h = assets.chars[cid]["stance_h"]
        self.controller = controller
        self.game = game
        self.tint = None
        self._tint_cache = {}
        self.facing = 1 if slot == 0 else -1
        self.super = 0.0
        self.dash_dir = 0
        self.reset(0)

    # ------------------------------------------------------------------ setup
    def reset(self, x):
        self.x = float(x)
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.hp = self.spec["hp"]
        self.state = State.IDLE
        self.timer = 0
        self.tick = 0
        self.move = None
        self.move_t = 0
        self.hit_done = False
        self.connected = False
        self.buffer = {}
        self.dirs = deque(maxlen=26)
        self.back_ticks = 0
        self.guarding = False
        self.combo_taken = 0
        self.kd_phase = 0
        self.jump_dir = 0
        self.fb_cooldown = 0
        self.flash = 0
        self.stun = 0
        self.moving_forward = False
        self.energy = ENERGY_MAX
        self.no_energy = 0

    @property
    def body_w(self):
        return self.spec["body_w"]

    # ------------------------------------------------------------------ queries
    def grounded(self):
        return self.y <= 0.01

    def hurtbox(self):
        if self.state in (State.KNOCKDOWN, State.GETUP, State.KO):
            return None
        if self.state == State.DASH and self.dash_dir != self.facing and self.timer < 8:
            return None             # the back dash dodges attacks at the start
        h = self.stance_h * (0.62 if self.state == State.CROUCH else 0.98)
        return pygame.Rect(int(self.x - self.body_w), int(GROUND - self.y - h), int(self.body_w * 2), int(h))

    def current(self):
        """(animation name, frame index) to show."""
        st, t = self.state, self.timer
        A = self.A
        if st in (State.IDLE, State.INTRO):
            return "idle", (self.tick // 9) % len(A["idle"])
        if st == State.WALK:
            name = "walk_forward" if self.moving_forward else "walk_back"
            if self.guarding:
                return "block", 1
            return name, (self.tick // 5) % len(A[name])
        if st == State.DASH:
            name = "walk_forward" if self.dash_dir == self.facing else "walk_back"
            return name, (t // 2) % len(A[name])
        if st == State.CROUCH:
            return ("block", 1) if self.guarding else ("crouch", 0 if t < 3 else 1)
        if st == State.JUMP_START:
            return "jump", 0
        if st == State.LAND:
            return "jump", 5
        if st == State.JUMP:
            if self.vy > 20:
                return "jump", 1
            if self.vy > 6:
                return "jump", 2
            if self.vy > -6:
                return "jump", 3
            return "jump", 4
        if st == State.ATTACK:
            return MOVES[self.move]["anim"], self.move_frame()
        if st == State.HITSTUN:
            n = len(A["hit"])
            total = max(1, self.stun)
            return "hit", min(n - 1, int(t / total * n * 1.4)) if t < total else n - 1
        if st == State.STUNNED:
            return "hit", min(1, len(A["hit"]) - 1)
        if st == State.BLOCKSTUN:
            return "block", 1
        if st in (State.KNOCKDOWN, State.KO):
            name = "knockdown" if st == State.KNOCKDOWN else "ko"
            n = len(A[name])
            if self.kd_phase == 0:
                return name, min(2 if n > 3 else n - 1, t // 6)
            if self.kd_phase == 1:
                return name, min(n - 1, 3 + t // 7)
            return name, n - 1
        if st == State.GETUP:
            return "getup", min(len(A["getup"]) - 1, t // 6)
        if st == State.WIN:
            return "win", min(len(A["win"]) - 1, t // 8)
        return "idle", 0

    def move_frame(self):
        dur = MOVES[self.move]["dur"]
        acc = 0
        for i, d in enumerate(dur):
            acc += d
            if self.move_t < acc:
                return i
        return len(dur) - 1

    def frame(self):
        name, idx = self.current()
        return self.A[name][idx]

    def tip_world(self):
        fr = self.frame()
        return (self.x + self.facing * fr.tip[0], GROUND - self.y + fr.tip[1])

    def hitbox(self):
        if self.state != State.ATTACK or self.hit_done:
            return None
        mv = MOVES[self.move]
        if "active" not in mv or self.move_frame() not in mv["active"]:
            return None
        bw, bh = mv["reach"][0] * K, mv["reach"][1] * K
        tx, ty = self.tip_world()
        x1 = tx + self.facing * 12 * K
        x0 = tx - self.facing * bw
        near = self.x + self.facing * 30 * K
        if self.facing > 0:
            x0 = min(x0, near)
        else:
            x0 = max(x0, near)
        left, right = min(x0, x1), max(x0, x1)
        return pygame.Rect(int(left), int(ty - bh / 2), int(right - left), int(bh))

    # ------------------------------------------------------------------ update
    def update(self, opp, live):
        self.tick += 1
        self.timer += 1
        self.flash = max(0, self.flash - 1)
        self.no_energy = max(0, self.no_energy - 1)
        if self.state not in (State.KO, State.INTRO):
            self.energy = min(ENERGY_MAX, self.energy + ENERGY_REGEN)
        self.fb_cooldown = max(0, self.fb_cooldown - 1)
        inp = self.controller.poll(self, opp) if live else _IDLE.poll(self, opp)
        dx = int(inp.right) - int(inp.left)
        fwd = dx * self.facing
        self.dirs.append(self._numpad(fwd, inp.up, inp.down))
        for b in inp.press:
            self.buffer[b] = BUFFER
            if b == "special" and not self.can_fire() and live:
                self.no_energy = 24
                self.game.sfx("ui_move", 0.5)
        for b in list(self.buffer):
            self.buffer[b] -= 1
            if self.buffer[b] <= 0:
                del self.buffer[b]
        self.back_ticks = self.back_ticks + 1 if (fwd < 0 and self.grounded()) else 0
        self.moving_forward = fwd > 0
        self.guarding = False

        st = self.state
        if st in (State.IDLE, State.WALK, State.CROUCH, State.INTRO):
            if st != State.INTRO:
                self._ground_control(inp, fwd, dx, opp)
        elif st == State.JUMP_START:
            if self.timer >= 4:
                self.state, self.timer = State.JUMP, 0
                self.vy = JUMP_V
                self.vx = self.jump_dir * self.spec["walk"] * 1.15
                self.game.sfx("jump", 0.6)
        elif st == State.JUMP:
            self.vy -= GRAVITY
            self.y += self.vy
            self.x += self.vx
            if self.y <= 0:
                self.y = 0.0
                self.vy = 0.0
                self.vx = 0.0
                self.state, self.timer = State.LAND, 0
                self.game.fx("dust", self.x, GROUND, scale=0.8)
                self.game.sfx("land", 0.7)
        elif st == State.LAND:
            if self.timer >= 4:
                self.state, self.timer = State.IDLE, 0
        elif st == State.ATTACK:
            self._attack_tick(opp)
        elif st in (State.HITSTUN, State.BLOCKSTUN):
            self.guarding = st == State.BLOCKSTUN
            self.x += self.vx
            self.vx *= 0.84
            if self.timer >= self.stun:
                self.state, self.timer = State.IDLE, 0
        elif st in (State.KNOCKDOWN, State.KO):
            self._down_tick(st)
        elif st == State.GETUP:
            if self.timer >= 30:
                self.state, self.timer = State.IDLE, 0
        elif st == State.DASH:
            speed = (DASH_SPEED if self.dash_dir == self.facing else BACKDASH_SPEED) * K
            self.x += self.dash_dir * speed * (1.0 - 0.6 * self.timer / DASH_TICKS)
            if self.timer % 4 == 1:
                self.game.fx("dust", self.x - self.dash_dir * 40, GROUND, scale=0.5)
            if self.timer >= DASH_TICKS:
                self.state, self.timer = State.IDLE, 0
        elif st in (State.WIN, State.STUNNED):
            pass
        self.x = max(WALL_L, min(WALL_R, self.x))
        if self.state not in (State.JUMP, State.ATTACK, State.JUMP_START, State.KNOCKDOWN, State.KO, State.GETUP, State.WIN, State.DASH):
            if abs(opp.x - self.x) > 4:
                self.facing = 1 if opp.x > self.x else -1

    # ---- helpers for update -------------------------------------------------
    @staticmethod
    def _numpad(fwd, up, down):
        if down:
            return 3 if fwd > 0 else (1 if fwd < 0 else 2)
        if up:
            return 9 if fwd > 0 else (7 if fwd < 0 else 8)
        return 6 if fwd > 0 else (4 if fwd < 0 else 5)

    def _qcf(self):
        seq = []
        for d in list(self.dirs)[-22:]:
            if not seq or seq[-1] != d:
                seq.append(d)
        want, i = (2, 3, 6), 0
        for d in seq:
            if d == want[i]:
                i += 1
                if i == 3:
                    return True
        return False

    def can_fire(self):
        return self.energy >= ENERGY_COST and self.fb_cooldown == 0

    def _wanted(self):
        if "super" in self.buffer:
            if self.super >= SUPER_MAX:
                return "super"
            self.buffer.pop("super", None)
        pressed = [b for b in ("heavy", "light", "kick", "special") if b in self.buffer]
        if not pressed:
            return None
        b = pressed[0]
        if b == "kick" and self._qcf() and self.super >= SUPER_MAX:
            return "super"
        if b in ("light", "heavy") and self._qcf() and self.can_fire():
            return "special"
        if b == "special" and not self.can_fire():
            others = [x for x in pressed if x != "special"]
            return others[0] if others else None
        return b

    def _ground_control(self, inp, fwd, dx, opp):
        want = self._wanted()
        if want:
            self._start_move(want)
            return
        if inp.dash and self.state in (State.IDLE, State.WALK):
            self.state, self.timer = State.DASH, 0
            self.dash_dir = inp.dash
            self.game.sfx("jump", 0.45)
            return
        if inp.up:
            self.state, self.timer = State.JUMP_START, 0
            self.jump_dir = dx
            return
        if inp.down:
            if self.state != State.CROUCH:
                self.state, self.timer = State.CROUCH, 0
            self.guarding = fwd < 0
            return
        if dx != 0:
            if self.state != State.WALK:
                self.state, self.timer = State.WALK, 0
            speed = self.spec["walk"] if fwd > 0 else self.spec["back"]
            self.x += dx * speed
            self.guarding = fwd < 0
        elif self.state != State.IDLE:
            self.state, self.timer = State.IDLE, 0

    def _start_move(self, name):
        self.state, self.timer = State.ATTACK, 0
        self.move, self.move_t = name, 0
        self.hit_done = False
        self.connected = False
        self.buffer.pop(name, None)
        if name == "special":
            self.buffer.pop("light", None)
            self.energy -= ENERGY_COST
        elif name == "super":
            self.super = 0.0
        self.game.on_move_start(self, name)

    def _attack_tick(self, opp):
        mv = MOVES[self.move]
        self.move_t += 1
        idx = self.move_frame()
        if self.move in ("special", "super") and idx == mv["spawn"] and not self.hit_done:
            self.hit_done = True
            self.fb_cooldown = 30
            self.game.spawn_fireball(self)
        if self.move == "heavy" and idx == 3:
            self.x += self.facing * mv["lunge"] * K
        # cancel into a stronger move once the attack has connected
        if self.connected and idx >= 1:
            nxt = self._wanted()
            if nxt in CANCELS[self.move]:
                self._start_move(nxt)
                return
        if self.move_t >= sum(mv["dur"]):
            self.state, self.timer = State.IDLE, 0
            self.move = None

    def _down_tick(self, st):
        if self.kd_phase == 0:  # airborne
            self.vy -= GRAVITY * 1.0
            self.y += self.vy
            self.x += self.vx
            if self.y <= 0:
                self.y = 0.0
                self.vy = 0.0
                self.kd_phase, self.timer = 1, 0
                self.game.fx("dust", self.x, GROUND, scale=1.2)
                self.game.sfx("land", 1.0)
                self.game.shake(8)
        else:
            self.x += self.vx
            self.vx *= 0.86
            if self.kd_phase == 1 and self.timer >= 14:
                self.kd_phase, self.timer = 2, 0
            if self.kd_phase == 2 and st == State.KNOCKDOWN and self.timer >= 26:
                self.state, self.timer = State.GETUP, 0

    # ------------------------------------------------------------------ being hit
    def can_block(self):
        if self.state == State.BLOCKSTUN:
            return True
        return self.grounded() and self.state in (State.IDLE, State.WALK, State.CROUCH) and self.back_ticks >= 1

    def take_hit(self, atk, mv, opp_dir):
        """Returns 'block' or 'hit'. opp_dir: +1 if the attacker is to our left (we get pushed right)."""
        if self.state == State.STUNNED:
            return "none"
        base = mv["dmg"] * atk.spec["dmg"]
        if self.can_block():
            chip = int(base * mv.get("chip", 0.07))
            self.hp = max(1, self.hp - chip)
            self.state, self.timer = State.BLOCKSTUN, 0
            self.stun = mv["blockstun"]
            self.vx = opp_dir * mv["push"] * 0.9 * K
            self.guarding = True
            return "block"
        scale = max(0.4, 1.0 - 0.1 * self.combo_taken)
        self.combo_taken += 1
        self.hp = max(0, self.hp - int(base * scale))
        self.flash = 6
        self.move = None
        if self.hp <= 0:
            self._go_down(State.KO, opp_dir, 9 * K, 12 * K)
        elif mv["knock"] or not self.grounded():
            self._go_down(State.KNOCKDOWN, opp_dir, 8 * K, 11 * K)
        else:
            self.state, self.timer = State.HITSTUN, 0
            self.stun = mv["hitstun"]
            self.vx = opp_dir * mv["push"] * K
        return "hit"

    def _go_down(self, st, opp_dir, vx, vy):
        self.state, self.timer = st, 0
        self.kd_phase = 0
        self.vx = opp_dir * vx
        self.vy = vy
        self.y = max(self.y, 1.0)

    def invulnerable(self):
        return self.hurtbox() is None

    def win(self):
        self.state, self.timer = State.WIN, 0
        self.move = None

    # ------------------------------------------------------------------ drawing
    def draw(self, screen, ox=0, oy=0):
        fr = self.frame()
        sy = GROUND - self.y
        foy = fr.oy
        if self.state in (State.KNOCKDOWN, State.KO) and self.kd_phase == 0:
            foy = -fr.h  # the physics already lifts the body; sit the sprite on it
        if self.facing > 0:
            pos = (self.x + fr.ox + ox, sy + foy + oy)
            img = fr.img
        else:
            pos = (self.x - fr.w - fr.ox + ox, sy + foy + oy)
            img = fr.flip
        if self.tint:
            key = (id(fr), self.facing > 0)
            timg = self._tint_cache.get(key)
            if timg is None:
                timg = img.copy()
                timg.fill(self.tint + (255,), special_flags=pygame.BLEND_RGBA_MULT)
                timg.fill((35, 0, 60, 0), special_flags=pygame.BLEND_RGB_ADD)
                self._tint_cache[key] = timg
            img = timg
        if self.state == State.STUNNED:                # the finisher's victim trembles
            pos = (pos[0] + random.randint(-5, 5), pos[1] + random.randint(-2, 2))
        if self.flash:
            img = img.copy()
            img.fill((90, 90, 90, 0), special_flags=pygame.BLEND_RGB_ADD)
        screen.blit(img, (int(pos[0]), int(pos[1])))

    def gain_super(self, amount):
        self.super = min(SUPER_MAX, self.super + amount)

    def draw_shadow(self, screen, ox=0, oy=0):
        w = int(self.stance_h * 0.62 * max(0.5, 1 - self.y / 800))
        surf = pygame.Surface((w, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, 110), surf.get_rect())
        screen.blit(surf, (int(self.x - w / 2 + ox), GROUND - 12 + oy))


class _IdleCtl:
    def poll(self, fighter, opp):
        from .input import InputFrame
        return InputFrame()


_IDLE = _IdleCtl()
