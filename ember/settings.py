"""Player settings, saved to ~/.ember_tournament/settings.json."""
import json
import os

from .constants import P1_KEYS, P2_KEYS

PATH = os.path.join(os.path.expanduser("~"), ".ember_tournament", "settings.json")
ACTIONS = ["left", "right", "up", "down", "light", "heavy", "kick", "special", "super"]
ACTION_LABELS = {"left": "MOVE LEFT", "right": "MOVE RIGHT", "up": "JUMP", "down": "CROUCH",
                 "light": "LIGHT PUNCH", "heavy": "HEAVY PUNCH", "kick": "KICK", "special": "FIREBALL", "super": "SUPER MOVE"}
ROUND_TIMES = [30, 60, 99, 0]          # 0 = no limit
WIN_COUNTS = [1, 2, 3]                 # rounds needed: best of 1 / 3 / 5
RESERVED = {"escape", "return", "f11"}  # keys that menus / the game use


class Settings:
    def __init__(self):
        self.music = 5            # 0..10
        self.sfx = 8
        self.voice = 8
        self.fullscreen = False
        self.shake = 2            # 0 off, 1 low, 2 normal
        self.flash = True
        self.difficulty = 1       # 0 easy, 1 normal, 2 hard
        self.round_time = 99
        self.wins_needed = 2
        self.finisher = 1         # 0 off, 1 match-winning KO only, 2 every KO
        self.rumble = 2           # controller vibration: 0 off, 1 low, 2 normal, 3 strong
        self.story_voice = True   # spoken narration and character voices in Arcade Story
        self.keys = [dict(P1_KEYS), dict(P2_KEYS)]
        self.load()

    # ------------------------------------------------------------------
    def load(self):
        try:
            with open(PATH) as f:
                d = json.load(f)
        except (OSError, ValueError):
            return
        for k in ("music", "sfx", "voice", "shake", "difficulty", "round_time", "wins_needed", "finisher", "rumble"):
            if isinstance(d.get(k), int):
                setattr(self, k, d[k])
        for k in ("fullscreen", "flash", "story_voice"):
            if isinstance(d.get(k), bool):
                setattr(self, k, d[k])
        for i in (0, 1):
            ks = d.get("keys", [{}, {}])[i] if isinstance(d.get("keys"), list) and len(d["keys"]) > i else {}
            for a in ACTIONS:
                if isinstance(ks.get(a), str):
                    self.keys[i][a] = ks[a]
        self.rumble = max(0, min(3, self.rumble))
        self.music = max(0, min(10, self.music))
        self.sfx = max(0, min(10, self.sfx))
        self.voice = max(0, min(10, self.voice))

    def save(self):
        try:
            os.makedirs(os.path.dirname(PATH), exist_ok=True)
            with open(PATH, "w") as f:
                json.dump({k: getattr(self, k) for k in ("music", "sfx", "voice", "fullscreen", "shake", "flash", "difficulty",
                                                         "round_time", "wins_needed", "finisher", "rumble", "story_voice", "keys")}, f, indent=1)
        except OSError:
            pass

    def reset_keys(self):
        self.keys = [dict(P1_KEYS), dict(P2_KEYS)]

    def reset_all(self):
        self.__dict__.update(Settings._defaults())

    @staticmethod
    def _defaults():
        s = Settings.__new__(Settings)
        s.music, s.sfx, s.voice = 5, 8, 8
        s.fullscreen, s.shake, s.flash, s.story_voice = False, 2, True, True
        s.difficulty, s.round_time, s.wins_needed, s.finisher, s.rumble = 1, 99, 2, 1, 2
        s.keys = [dict(P1_KEYS), dict(P2_KEYS)]
        return s.__dict__
