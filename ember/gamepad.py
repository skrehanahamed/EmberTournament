"""Game controllers (PS5 DualSense, Xbox, ...) through SDL's controller layer.
Menus: pads are turned into the same key presses the keyboard makes, so every screen works unchanged.
Fights: KeyboardController merges its pad (slot 0 = P1, slot 1 = P2) with the keyboard.

PlayStation layout:  D-pad / left stick  move        Square  light     Triangle  heavy
                     Cross  kick                      Circle  fireball  R1 / R2   SUPER
                     L1 / L2  dash                    Options  pause / back
Menus:               D-pad / stick  move   Cross  select   Circle  back   Options  back / pause
"""
import pygame
from pygame._sdl2 import controller as sdl

CB = pygame
BTN_MAP = {"light": pygame.CONTROLLER_BUTTON_X, "heavy": pygame.CONTROLLER_BUTTON_Y,
           "kick": pygame.CONTROLLER_BUTTON_A, "special": pygame.CONTROLLER_BUTTON_B,
           "super": pygame.CONTROLLER_BUTTON_RIGHTSHOULDER}
DEAD = 0.5 * 32767
FIRST, REPEAT = 22, 7        # menu auto-repeat (frames)


PS_LABELS = ("SQUARE", "TRIANGLE", "CROSS", "CIRCLE", "R1 / R2", "L1 / L2", "OPTIONS")
XB_LABELS = ("X", "Y", "A", "B", "RB / RT", "LB / LT", "MENU")


def is_playstation(name):
    n = name.lower()
    return any(k in n for k in ("dualsense", "dualshock", "playstation", "ps4", "ps5", "wireless controller"))


# name -> envelope: list of (heavy motor, light motor, milliseconds) steps played one after another,
# scaled by the VIBRATION setting. Sharp attack + decay is what makes a hit feel like a hit.
PRESETS = {
    "tap": [(0.0, 0.35, 35)], "dash": [(0.0, 0.3, 50), (0.0, 0.1, 40)], "cast": [(0.3, 0.4, 70), (0.15, 0.2, 90)],
    "hit_light_a": [(0.1, 0.5, 40), (0.0, 0.15, 40)],
    "hit_light": [(0.55, 0.8, 50), (0.3, 0.4, 60), (0.1, 0.1, 50)],
    "hit_heavy_a": [(0.5, 0.5, 70), (0.2, 0.2, 80)],
    "hit_heavy": [(1.0, 0.9, 80), (0.8, 0.6, 90), (0.45, 0.3, 110), (0.15, 0.1, 100)],
    "block": [(0.45, 0.25, 50), (0.15, 0.1, 50)],
    "fire_hit": [(0.9, 0.8, 90), (0.6, 0.5, 120), (0.3, 0.2, 140)],
    "super_start": [(0.15, 0.15, 90), (0.3, 0.3, 90), (0.5, 0.5, 90), (0.7, 0.7, 90), (0.9, 0.9, 120), (1.0, 1.0, 260), (0.4, 0.3, 200)],
    "super_hit": [(1.0, 1.0, 200), (0.85, 0.75, 220), (0.55, 0.45, 260), (0.25, 0.2, 260)],
    "super_land": [(0.7, 0.6, 100), (0.3, 0.2, 160)],
    "fin_start": [(0.9, 0.5, 120), (0.3, 0.2, 100), (0.8, 0.5, 120), (0.2, 0.1, 100)],
    "heartbeat": [(0.7, 0.0, 70), (0.0, 0.0, 70), (0.45, 0.0, 70)],
    "charge": [(0.5, 0.5, 90), (0.35, 0.35, 60)],
    "fin_boom": [(1.0, 1.0, 280), (0.95, 0.85, 260), (0.7, 0.6, 300), (0.4, 0.3, 300), (0.15, 0.1, 300)],
    "ko": [(1.0, 0.8, 140), (0.7, 0.5, 160), (0.35, 0.25, 200)], "round": [(0.4, 0.4, 100), (0.15, 0.1, 100)],
    "test": [(0.8, 0.7, 120), (0.0, 0.0, 80), (0.8, 0.7, 120), (0.3, 0.3, 120)],
}
LEVELS = (0.0, 0.5, 1.0, 1.35)      # off, low, normal, strong
LED_DEFAULT = (0, 70, 220)


class Pad:
    def __init__(self, index):
        self.c = sdl.Controller(index)
        self.id = self.c.as_joystick().get_instance_id()
        self.name = self.c.name
        self.menu_prev = set()
        self.menu_hold = {}
        self.seq = []               # rumble steps still to play: (low, high, frames)
        self.step = 0               # frames left of the current step
        self.peak = 0.0
        self.led = None

    def btn(self, b):
        return bool(self.c.get_button(b))

    def axis(self, a):
        return self.c.get_axis(a)

    def direction(self):
        L = self.axis(pygame.CONTROLLER_AXIS_LEFTX)
        U = self.axis(pygame.CONTROLLER_AXIS_LEFTY)
        left = self.btn(pygame.CONTROLLER_BUTTON_DPAD_LEFT) or L < -DEAD
        right = self.btn(pygame.CONTROLLER_BUTTON_DPAD_RIGHT) or L > DEAD
        up = self.btn(pygame.CONTROLLER_BUTTON_DPAD_UP) or U < -DEAD * 1.3
        down = self.btn(pygame.CONTROLLER_BUTTON_DPAD_DOWN) or U > DEAD
        return left, right, up, down

    def fight_buttons(self):
        held = {name for name, b in BTN_MAP.items() if self.btn(b)}
        if self.axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT) > 12000:
            held.add("super")
        return held

    def dash_held(self):
        return self.btn(pygame.CONTROLLER_BUTTON_LEFTSHOULDER) or self.axis(pygame.CONTROLLER_AXIS_TRIGGERLEFT) > 12000

    def rumble(self, low, high, ms):
        try:
            self.c.rumble(low, high, ms)
        except Exception:
            pass

    def set_led(self, rgb):
        if rgb != self.led:
            self.led = rgb
            try:
                self.c.set_led(tuple(int(v) for v in rgb))
            except Exception:
                pass

    def tick(self):
        """Advance the rumble envelope by one frame."""
        if self.step > 0:
            self.step -= 1
        if self.step <= 0:
            if self.seq:
                low, high, frames = self.seq.pop(0)
                self.peak = max(low, high)
                self.step = frames
                self.rumble(low, high, int(frames * 16.7) + 40)
            elif self.peak:
                self.peak = 0.0
                try:
                    self.c.stop_rumble()
                except Exception:
                    pass


class Pads:
    def __init__(self):
        self.pads = []
        self.toast = ("", 0)
        self.help = 0               # frames left to show the controls panel
        self.level = 2              # vibration setting 0..3

    def start(self):
        try:
            if not sdl.get_init():
                sdl.init()
            for i in range(sdl.get_count()):
                self.add(i, quiet=True)
        except Exception:
            pass

    def add(self, index, quiet=False):
        try:
            if not sdl.is_controller(index):
                return
            p = Pad(index)
        except Exception:
            return
        if any(q.id == p.id for q in self.pads):
            return
        self.pads.append(p)
        self.help = 520
        if not quiet:
            self.toast = (f"{p.name.upper()} CONNECTED", 200)

    def event(self, ev):
        if ev.type == pygame.CONTROLLERDEVICEADDED:
            self.add(ev.device_index)
        elif ev.type == pygame.CONTROLLERDEVICEREMOVED:
            gone = [p for p in self.pads if p.id == ev.instance_id]
            for p in gone:
                self.help = 0
                self.pads.remove(p)
                self.toast = (f"{p.name.upper()} DISCONNECTED", 200)

    def is_ps(self):
        return bool(self.pads) and is_playstation(self.pads[0].name)

    def get(self, slot):
        return self.pads[slot] if slot < len(self.pads) else None

    def buzz(self, slot, name, scale=1.0):
        """Vibrate the pad of this player with a named envelope (see PRESETS)."""
        k = LEVELS[max(0, min(3, self.level))] * scale
        p = self.get(slot) if k > 0 and slot is not None else None
        if not p:
            return
        steps = [(min(1.0, lo * k), min(1.0, hi * k), max(1, round(ms / 16.7))) for lo, hi, ms in PRESETS[name]]
        peak = max(max(lo, hi) for lo, hi, _ in steps)
        left = max([max(lo, hi) for lo, hi, _ in p.seq] + [p.peak if p.step > 0 else 0.0])
        if peak >= left * 0.6:                       # a weak buzz never cuts off a strong one that is still playing
            p.seq = steps
            p.step = 0

    def update(self):
        for p in self.pads:
            p.tick()

    def led(self, slot, rgb):
        p = self.get(slot)
        if p:
            p.set_led(rgb)

    def reset_led(self):
        for p in self.pads:
            p.set_led(LED_DEFAULT)

    def stop(self):
        for p in self.pads:
            p.seq, p.step = [], 0
            try:
                p.c.stop_rumble()
            except Exception:
                pass
            p.set_led(LED_DEFAULT)

    def menu_keys(self, full):
        """(key code, pad number) pairs to feed the current scene this frame. `full`: every control; otherwise only Options (pause)."""
        keys = []
        for idx, p in enumerate(self.pads):
            left, right, up, down = p.direction()
            now = set()
            if full:
                for on, key in ((left, pygame.K_LEFT), (right, pygame.K_RIGHT), (up, pygame.K_UP), (down, pygame.K_DOWN),
                                (p.btn(pygame.CONTROLLER_BUTTON_A), pygame.K_RETURN),
                                (p.btn(pygame.CONTROLLER_BUTTON_B), pygame.K_ESCAPE),
                                (p.btn(pygame.CONTROLLER_BUTTON_LEFTSHOULDER), pygame.K_q),
                                (p.btn(pygame.CONTROLLER_BUTTON_RIGHTSHOULDER), pygame.K_e)):
                    if on:
                        now.add(key)
            if p.btn(pygame.CONTROLLER_BUTTON_START):
                now.add(pygame.K_ESCAPE)
            for key in now:
                if key not in p.menu_prev:
                    keys.append((key, idx))
                    p.menu_hold[key] = FIRST
                elif key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    p.menu_hold[key] -= 1
                    if p.menu_hold[key] <= 0:
                        keys.append((key, idx))
                        p.menu_hold[key] = REPEAT
            p.menu_prev = now
            if self.help and self.help < 460 and (now or any(p.btn(b) for b in BTN_MAP.values())):
                self.help = min(self.help, 12)
        return keys


PADS = Pads()
