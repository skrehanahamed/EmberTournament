"""Controllers: keyboard and a simple CPU opponent. Both produce an InputFrame every tick."""
import random

import pygame

from .gamepad import PADS


class InputFrame:
    __slots__ = ("left", "right", "up", "down", "press", "dash")

    def __init__(self):
        self.left = self.right = self.up = self.down = False
        self.press = set()
        self.dash = 0        # -1 / +1: dash left / right (world direction)


BUTTONS = ("light", "heavy", "kick", "special", "super")


class KeyboardController:
    def __init__(self, keymap, slot=0):
        self.slot = slot            # which game controller (PADS) also drives this player
        self.keys = {name: pygame.key.key_code(k) for name, k in keymap.items()}
        self.prev = set()
        self.prev_dx = 0
        self.pad_dash_prev = False
        self.tick = 0
        self.last_tap = {-1: -99, 1: -99}

    def poll(self, fighter, opp):
        pressed = pygame.key.get_pressed()
        f = InputFrame()
        f.left = pressed[self.keys["left"]]
        f.right = pressed[self.keys["right"]]
        f.up = pressed[self.keys["up"]]
        f.down = pressed[self.keys["down"]]
        held = {b for b in BUTTONS if pressed[self.keys[b]]}
        pad = PADS.get(self.slot)
        pad_dash = False
        if pad:
            l, r, u, d = pad.direction()
            f.left, f.right, f.up, f.down = f.left or l, f.right or r, f.up or u, f.down or d
            held |= pad.fight_buttons()
            pad_dash = pad.dash_held()
        f.press = held - self.prev
        self.prev = held
        # double-tap left/right = dash
        self.tick += 1
        dx = int(f.right) - int(f.left)
        if dx != 0 and dx != self.prev_dx:
            if self.tick - self.last_tap[dx] <= 14:
                f.dash = dx
                self.last_tap[dx] = -99
            else:
                self.last_tap[dx] = self.tick
        self.prev_dx = dx
        if pad_dash and not self.pad_dash_prev:
            f.dash = dx or (1 if (fighter.facing > 0) else -1)
        self.pad_dash_prev = pad_dash
        return f


class IdleController:
    """Used while the match is not live (intro, round end)."""

    def poll(self, fighter, opp):
        return InputFrame()


class AIController:
    """Picks a plan, holds it for a short time. Not a genius, but it blocks, zones and punishes."""

    def __init__(self, level=0.6, rng=None):
        self.level = level
        self.rng = rng or random.Random()
        self.plan = "idle"
        self.t = 0
        self.fired = False

    def poll(self, f, opp):
        from .fighter import State
        r = self.rng
        inp = InputFrame()
        dx = opp.x - f.x
        dist = abs(dx)
        toward = 1 if dx > 0 else -1
        self.t -= 1
        threat = opp.state == State.ATTACK and dist < 420
        if self.t <= 0 or (threat and self.plan not in ("block",) and r.random() < 0.08 * self.level):
            self.t = r.randint(int(14 - 8 * self.level), int(40 - 22 * self.level))
            p = r.random()
            if threat and p < 0.55 * self.level + 0.1:
                self.plan, self.t = "block", r.randint(14, 30)
            elif opp.state in (State.KNOCKDOWN, State.GETUP) and dist < 340:
                self.plan = "light" if p < 0.5 else "heavy"
            elif dist > 750:
                self.plan = "fireball" if p < 0.35 else ("dash" if p < 0.55 else ("approach" if p < 0.9 else "jump"))
            elif dist > 330:
                self.plan = ("approach" if p < 0.5 else ("dash" if p < 0.65 else ("fireball" if p < 0.72 else ("jump" if p < 0.82 else "idle"))))
            else:
                self.plan = ("light" if p < 0.28 else "heavy" if p < 0.45 else "kick" if p < 0.62
                             else "block" if p < 0.78 else "retreat" if p < 0.9 else "crouch")
            self.fired = False
        plan = self.plan
        if plan == "approach":
            inp.right, inp.left = (toward > 0), (toward < 0)
        elif plan in ("retreat", "block"):
            inp.right, inp.left = (toward < 0), (toward > 0)
        elif plan == "crouch":
            inp.down = True
        elif plan == "jump" and not self.fired:
            inp.up = True
            inp.right, inp.left = (toward > 0), (toward < 0)
            self.fired = True
        elif plan in ("light", "heavy", "kick") and not self.fired:
            inp.press.add(plan)
            self.fired = True
        elif plan == "fireball" and not self.fired:
            if f.can_fire():
                inp.press.add("special")
            self.fired = True
        elif plan == "dash" and not self.fired:
            inp.dash = toward if r.random() < 0.7 else -toward
            self.fired = True
        if f.super >= 100 and dist < 1100 and r.random() < 0.02 * self.level and f.state.name in ("IDLE", "WALK"):
            inp.press.add("super")
        return inp
