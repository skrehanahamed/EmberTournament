import os
import sys

# a PyInstaller build unpacks the game in _internal or sys._MEIPASS
if getattr(sys, "frozen", False):
    base = getattr(sys, "_MEIPASS", None)
    if base and os.path.exists(os.path.join(base, "data")):
        ROOT = base
    else:
        exe_dir = os.path.dirname(sys.executable)
        ROOT = exe_dir if os.path.exists(os.path.join(exe_dir, "data")) else (base or exe_dir)
else:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")

W, H = 1920, 1080
FPS = 60
K = 1.2                 # sprites are K times the size the frame data was tuned for
GROUND = 975            # screen y of the fighters' feet
WALL_L, WALL_R = 120, 1800
ROUND_SECONDS = 99
WINS_NEEDED = 2

GOLD = (255, 204, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EMBER = (255, 120, 30)

STAGES = [
    {"id": "neon", "name": "NEON CITY", "fx": "rain"},
    {"id": "temple", "name": "SUNSET SHRINE", "fx": "petals"},
    {"id": "volcano", "name": "VOLCANIC RUINS", "fx": "embers"},
]

# Character data. Frame data is shared (it comes from the shared animation layout); characters differ in
# speed, health, damage and fireball.
CHARS = {
    "kaito": dict(name="KAITO", title="The Swordless Monk", role="ALL-ROUNDER", hp=1000, walk=6.0, back=5.0,
                  dmg=1.0, body_w=72, fireball="orange", fb_speed=15, accent=(230, 50, 40), voice="m",
                  blurb=["A young monk who lost his master", "and his sword. He fights to learn the", "truth about the Dragon Cores."]),
    "brutus": dict(name="BRUTUS", title="Exiled Arena Champion", role="GRAPPLER", hp=1150, walk=4.8, back=4.0,
                   dmg=1.18, body_w=92, fireball="red", fb_speed=12, accent=(200, 40, 30), voice="h",
                   blurb=["Banished from the arena for", "winning too often. He wants the", "throne to bring the crowd back."]),
    "valeria": dict(name="VALERIA", title="Desert Assassin", role="RUSHDOWN", hp=950, walk=7.4, back=6.0,
                    dmg=0.92, body_w=62, fireball="crimson", fb_speed=16, accent=(240, 170, 40), voice="f",
                    blurb=["A fire-wielding killer from the", "burning sands. She hunts the", "Cores to free her kingdom."]),
    "rudra": dict(name="RUDRA", title="Bengal's Iron Fist", role="BRAWLER", hp=1050, walk=5.4, back=4.5,
                  dmg=1.1, body_w=70, fireball="crimson", fb_speed=15, accent=(225, 50, 40), voice="r",
                  blurb=["A wrestler from the river delta who", "fights for the honour of his village.", "His fists burn with the sacred flame."]),
    "reno": dict(name="RENO", title="The Challenger", role="ALL-ROUNDER", hp=1000, walk=5.8, back=4.8,
                 dmg=1.0, body_w=70, fireball="reno", fb_speed=17, accent=(90, 80, 255), voice="m",
                 blurb=["An ordinary guy with an extraordinary", "temper. He signs every move with a", "blazing letter R."]),
    "mira": dict(name="MIRA", title="Storm Mage", role="ZONER", hp=950, walk=5.6, back=4.8,
                 dmg=0.98, body_w=64, fireball="cyan", fb_speed=21, accent=(60, 190, 255), voice="f",
                 blurb=["She commands lightning from afar.", "The storm told her where the", "last Core sleeps."]),
}
SUPERS = {"kaito": "DRAGON BREATH", "brutus": "MAGMA CRUSH", "valeria": "CRIMSON TEMPEST", "mira": "STORM CALLER",
          "rudra": "TIGER ROAR", "reno": "R-SIGN BLAST"}
FINISHERS = {'kaito': 'DRAGON FIST OF EMBERS', 'brutus': 'MOLTEN HAMMER', 'valeria': 'CRIMSON DESERT STORM', 'mira': 'THUNDER JUDGEMENT', 'rudra': 'BENGAL TIGER FLAME', 'reno': 'R-SIGN ANNIHILATION'}
CHAR_ORDER = ["kaito", "brutus", "valeria", "mira", "rudra", "reno"]

P1_KEYS = dict(left="a", right="d", up="w", down="s", light="f", heavy="g", kick="h", special="t", super="y")
P2_KEYS = dict(left="left", right="right", up="up", down="down", light="j", heavy="k", kick="l", special="i", super="o")
