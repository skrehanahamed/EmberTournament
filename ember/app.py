"""Window, main loop and command-line options."""
import argparse
import time
import os
import sys

import pygame

from .assets import Assets
from .audio import AudioManager
from .gamepad import PADS
from .constants import CHAR_ORDER, DATA, FPS, H, STAGES, W
from .settings import Settings


class App:
    def __init__(self, args):
        self.args = args
        if args.headless:
            os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
            os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
        os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "linear")          # smooth when the GPU scales the picture
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        PADS.start()
        self._pad_icons = {}
        self.gpu = None
        pygame.display.set_caption("EMBER TOURNAMENT")
        # The game is always drawn on a fixed 1920x1080 canvas, then scaled to fit the real window (keeping the
        # 16:9 shape, with black bars if the window is a different shape). The window can be resized freely.
        if args.headless:
            self.window = pygame.display.set_mode((W, H))
        else:
            info = pygame.display.Info()
            dw, dh = info.current_w or 1280, info.current_h or 720
            fit = min(1.0, (dw * 0.92) / W, (dh * 0.86) / H)      # open at most 92% of the screen's width, 86% of its height
            self.windowed_size = (max(640, int(W * fit)), max(360, int(H * fit)))
            self.fullscreen = bool(args.fullscreen)
            if not getattr(args, "cpu_present", False):
                self._try_gpu()
            if self.gpu is None:
                self._set_mode()
        self.screen = pygame.Surface((W, H), 0, 32, (0xFF0000, 0xFF00, 0xFF, 0)).convert() if self.gpu is None else pygame.Surface((W, H)).convert()
        self.view = pygame.Rect(0, 0, W, H)
        self._scaled = None
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.assets = Assets()
        try:
            self.audio = AudioManager(enabled=not args.mute)
        except pygame.error:
            self.audio = AudioManager(enabled=False)
        self.scene = None
        self.running = True
        self.frame = 0
        self.settings = Settings()
        PADS.level = self.settings.rumble
        self.audio.apply_settings(self.settings)
        if self.settings.fullscreen and not args.headless and not self.fullscreen:
            self.toggle_fullscreen()

    def _try_gpu(self):
        """Let the graphics chip scale the 1080p picture to the window (about 1 ms instead of 7+ ms on the CPU)."""
        try:
            from pygame._sdl2 import video
            pygame.display.set_mode((1, 1), pygame.HIDDEN)           # only needed so images can be converted to a fast format
            win = video.Window("EMBER TOURNAMENT", size=self.windowed_size, resizable=True)
            ren = video.Renderer(win, vsync=False)
            ren.logical_size = (W, H)                                # keeps the 16:9 shape, black bars when the window differs
            tex = video.Texture(ren, (W, H), streaming=True)
            if self.fullscreen:
                win.set_fullscreen(desktop=True)
            self.gpu = (win, ren, tex)
            self.window = win
        except Exception as e:                                       # old systems: fall back to the CPU scaler
            print("GPU presenting unavailable (%s) - using the CPU scaler" % e)
            self.gpu = None

    def _set_mode(self):
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        size = (0, 0) if self.fullscreen else self.windowed_size
        self.window = pygame.display.set_mode(size, flags)

    def toggle_fullscreen(self):
        if getattr(self.args, "headless", False):
            return
        self.fullscreen = not self.fullscreen
        self.settings.fullscreen = self.fullscreen
        self.settings.save()
        if self.gpu:
            win = self.gpu[0]
            if self.fullscreen:
                self.windowed_size = tuple(win.size)
                win.set_fullscreen(desktop=True)
            else:
                win.set_windowed()
                win.size = self.windowed_size
            return
        if self.fullscreen:
            self.windowed_size = self.window.get_size()
        self._set_mode()

    def window_size(self):
        return tuple(self.gpu[0].size) if self.gpu else self.window.get_size()

    def present(self):
        """Scale the 1080p canvas into the window, centred, keeping its shape."""
        if self.gpu:
            _, ren, tex = self.gpu
            tex.update(self.screen)
            ren.clear()
            tex.draw()
            ren.present()
            return
        ww, wh = self.window.get_size()
        if (ww, wh) == (W, H):
            self.window.blit(self.screen, (0, 0))
        else:
            k = min(ww / W, wh / H)
            tw, th = max(1, int(W * k)), max(1, int(H * k))
            if self._scaled is None or self._scaled.get_size() != (tw, th):
                self._scaled = pygame.Surface((tw, th)).convert()
            # smooth when shrinking (keeps text readable), plain pixel scaling when enlarging
            if k < 1.0:
                pygame.transform.smoothscale(self.screen, (tw, th), self._scaled)
            else:
                pygame.transform.scale(self.screen, (tw, th), self._scaled)
            x, y = (ww - tw) // 2, (wh - th) // 2
            if self.view.size != (tw, th) or self.view.topleft != (x, y):
                self.window.fill((0, 0, 0))
                self.view = pygame.Rect(x, y, tw, th)
            self.window.blit(self._scaled, (x, y))
        pygame.display.flip()

    @property
    def difficulty(self):
        return self.settings.difficulty

    @difficulty.setter
    def difficulty(self, v):
        self.settings.difficulty = v
        self.settings.save()

    def _selftest(self, log, upd, drw, prs):
        """Scripted finisher in a real window. Records how long each frame took (update / draw / present)."""
        sc = self.scene
        n = len(log)
        phase = getattr(sc, "phase", "")
        if n == 200:                                  # after the intro, set up a match-deciding KO and deliver it
            from .fighter import State
            from .screens import MOVES
            from .input import IdleController
            sc.wins = [sc.wins_needed - 1, 0]
            w, l = sc.f
            w.x, l.x = 800, 1150
            for f in sc.f:
                f.state, f.timer, f.move, f.back_ticks, f.guarding = State.IDLE, 0, None, 0, False
            l.hp = 5
            l.controller = IdleController()
            w.controller = IdleController()
            sc.hit_event(w, l, MOVES["heavy"], (1000, 700))
        log.append((n, upd, drw, prs, phase, (sc.fin or {}).get("state") if getattr(sc, "fin", None) else ""))
        if phase == "end" and getattr(sc, "pt", 0) > 220 and n > 300:
            tot = [u + d + p for _, u, d, p, _, _ in log[200:]]
            tot_s = sorted(tot)
            lines = ["frames measured: %d (finisher part)" % len(tot),
                     "average frame work: %.1f ms   median %.1f   95th pct %.1f   worst %.1f" % (sum(tot) / len(tot), tot_s[len(tot) // 2], tot_s[int(len(tot) * .95)], tot_s[-1]),
                     "frames over 16.7 ms (would drop below 60 fps): %d" % sum(1 for x in tot if x > 16.7),
                     "window size: %s   presenter: %s" % (self.window_size(), "GPU" if self.gpu else "CPU"),
                     "", "10 slowest frames: tick  total  update  draw  present  phase  finisher-state"]
            for e in sorted(log[200:], key=lambda e: -(e[1] + e[2] + e[3]))[:10]:
                lines.append("  %4d  %5.1f  %5.1f  %5.1f  %5.1f  %s %s" % (e[0], e[1] + e[2] + e[3], e[1], e[2], e[3], e[4], e[5]))
            open("/tmp/ember_selftest.txt", "w").write("\n".join(lines))
            return True
        return n > 2500

    def draw_pad_toast(self):
        if getattr(self.args, "headless", False) or getattr(self.args, "shot", None):
            return
        msg, left = PADS.toast
        if left > 0:
            PADS.toast = (msg, left - 1)
            img = self.assets.text(msg, 18, (255, 255, 255), thick=3)
            bar = pygame.Surface((img.get_width() + 40, 44), pygame.SRCALPHA)
            bar.fill((0, 0, 0, 170))
            x = W - bar.get_width() - 30
            self.screen.blit(bar, (x, 24))
            self.screen.blit(img, (x + 20, 36))

    def pad_icon(self, name, h=58):
        key = (name, h)
        img = self._pad_icons.get(key)
        if img is None:
            src = pygame.image.load(os.path.join(DATA, "ui", "pad", name + ".png")).convert_alpha()
            img = pygame.transform.smoothscale(src, (int(src.get_width() * h / src.get_height()), h))
            self._pad_icons[key] = img
        return img

    def pad_panel(self, title):
        pre = "ps_" if PADS.is_ps() else "xb_"
        rows = [("MOVE  /  JUMP  /  CROUCH", ["dpad", "stick"]), ("LIGHT ATTACK", ["light"]), ("HEAVY ATTACK", ["heavy"]),
                ("KICK", ["kick"]), ("FIREBALL  (EMBER)", ["special"]), ("SUPER", ["r1", "r2"]), ("DASH", ["l1", "l2"]),
                ("PAUSE  /  BACK", ["menu"])]
        a = self.assets
        row_h = 70
        w, h = 1000, 140 + len(rows) * row_h + 70
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (14, 8, 12, 252), panel.get_rect(), border_radius=16)
        pygame.draw.rect(panel, (222, 160, 52, 255), panel.get_rect(), 4, border_radius=16)
        t = a.text(title, 30, (255, 220, 120), thick=4)
        panel.blit(t, (w // 2 - t.get_width() // 2, 24))
        sub = a.text(PADS.pads[0].name.upper() if PADS.pads else "", 14, (200, 195, 190), thick=2)
        panel.blit(sub, (w // 2 - sub.get_width() // 2, 76))
        y = 118
        for label, icons in rows:
            panel.blit(a.text(label, 20, (235, 230, 225), thick=2), (50, y + 18))
            x = w - 50
            for ic in reversed(icons):
                img = self.pad_icon(pre + ic)
                x -= img.get_width()
                panel.blit(img, (x, y))
                x -= 16
            y += row_h
        cross, circ = ("CROSS", "CIRCLE") if PADS.is_ps() else ("A", "B")
        foot = a.text(f"MENUS:  D-PAD MOVE     {cross} SELECT     {circ} BACK", 16, (200, 195, 190), thick=2)
        panel.blit(foot, (w // 2 - foot.get_width() // 2, h - 56))
        return panel

    def draw_pad_help(self):
        if getattr(self.args, "headless", False) or getattr(self.args, "shot", None):
            return
        if PADS.help <= 0:
            return
        PADS.help -= 1
        panel = self.pad_panel("CONTROLLER CONNECTED")
        panel.set_alpha(min(255, PADS.help * 12, (520 - PADS.help) * 20))
        self.screen.blit(panel, (W // 2 - panel.get_width() // 2, H // 2 - panel.get_height() // 2))

    def goto(self, scene):
        self.scene = scene
        PADS.reset_led()

    def run(self):
        from .screens import FightScene, SelectScene, TitleScene
        a = self.args
        if a.demo or a.screen == "fight":
            ids = [a.p1, a.p2]
            stage = next(s for s in STAGES if s["id"] == a.stage) if a.stage else STAGES[0]
            if getattr(a, "boss", False):                     # dev: straight into the final boss fight
                ids = [a.p1, "emperor"]
                stage = next(s for s in STAGES if s["id"] == "volcano")
            self.scene = FightScene(self, ids, True, stage, demo=a.demo, boss=getattr(a, "boss", False))
        elif a.screen == "select":
            self.scene = SelectScene(self, cpu=True)
        else:
            self.scene = TitleScene(self)
        shots = sorted(int(x) for x in a.shot.split(",")) if a.shot else []
        log = []
        while self.running:
            t_frame = time.perf_counter()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                elif ev.type == getattr(pygame, "WINDOWCLOSE", -1):
                    self.running = False
                elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif ev.type in (pygame.CONTROLLERDEVICEADDED, pygame.CONTROLLERDEVICEREMOVED):
                    PADS.event(ev)
                elif ev.type == pygame.VIDEORESIZE and not a.headless:
                    self.window.fill((0, 0, 0))
                    self.view = pygame.Rect(0, 0, 0, 0)
                else:
                    self.scene.handle(ev)
            for k, pad_no in PADS.menu_keys(self.scene.pad_menu()):
                self.scene.handle(pygame.event.Event(pygame.KEYDOWN, key=k, unicode="", mod=0, scancode=0, pad=pad_no))
            PADS.update()
            steps = max(1, a.speed)
            t_u = time.perf_counter()
            for _ in range(steps):
                self.scene.update()
                self.frame += 1
                if shots and self.frame == shots[0]:
                    break
            t_d = time.perf_counter()
            self.scene.draw(self.screen)
            self.draw_pad_toast()
            self.draw_pad_help()
            t_p = time.perf_counter()
            self.present()
            t_e = time.perf_counter()
            if a.selftest:
                if self._selftest(log, (t_d - t_u) * 1000, (t_p - t_d) * 1000, (t_e - t_p) * 1000):
                    break
            if shots and self.frame >= shots[0]:
                pygame.image.save(self.screen, f"/tmp/ember_shot_{shots[0]}.png")
                shots.pop(0)
                if not shots:
                    break
            if not a.headless:
                self.clock.tick(FPS)
        PADS.stop()
        pygame.quit()


def main(argv=None):
    p = argparse.ArgumentParser(description="EMBER TOURNAMENT")
    p.add_argument("--demo", action="store_true", help="CPU vs CPU")
    p.add_argument("--screen", default="title", choices=["title", "select", "fight"])
    p.add_argument("--p1", default="kaito", choices=CHAR_ORDER)
    p.add_argument("--p2", default="mira", choices=CHAR_ORDER)
    p.add_argument("--stage", default=None, choices=[s["id"] for s in STAGES])
    p.add_argument("--shot", default=None, help="save screenshots at these frame numbers, then quit")
    p.add_argument("--speed", type=int, default=1, help="logic ticks per drawn frame (testing)")
    p.add_argument("--headless", action="store_true")
    p.add_argument("--mute", action="store_true")
    p.add_argument("--selftest", action="store_true", help="play a scripted finisher in a REAL window and write frame timings to /tmp/ember_selftest.txt")
    p.add_argument("--cpu-present", action="store_true", help="scale the picture on the CPU instead of the graphics chip (fallback)")
    p.add_argument("--boss", action="store_true", help="start the fight against the Hollow Emperor (use with --screen fight, handy with --dev)")
    p.add_argument("--dev", action="store_true", help="developer mode: test hotkeys and a debug overlay in fights")
    p.add_argument("--fullscreen", action="store_true")
    args = p.parse_args(argv)
    App(args).run()
