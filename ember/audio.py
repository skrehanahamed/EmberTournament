"""Music, sound effects, announcer and fighter grunts."""
import glob
import os
import random

import pygame

from .constants import DATA

MUSIC = {"menu": "menu.ogg", "fight": "fight.mp3", "final": "final.ogg"}


class AudioManager:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.groups = {}
        self.sounds = {}
        self.track = None
        self.volume_music = 0.45
        self.volume_sfx = 0.8
        self.story_on = True
        self.ducked = False
        self.vol_music = self.vol_sfx = self.vol_voice = 1.0   # user settings (0..1)
        if not enabled:
            return
        pygame.mixer.set_num_channels(24)
        self.announcer_ch = pygame.mixer.Channel(0)
        self.story_ch = pygame.mixer.Channel(3)
        self.story_on = True
        self.ducked = False
        self.effort_ch = [pygame.mixer.Channel(1), pygame.mixer.Channel(2)]
        for sub in ("sfx", "voice"):
            for path in sorted(glob.glob(os.path.join(DATA, "audio", sub, "*"))):
                name = os.path.splitext(os.path.basename(path))[0]
                group = name
                if not name.startswith("announcer") and name.rsplit("_", 1)[-1].isdigit():
                    group = name.rsplit("_", 1)[0]
                self.groups.setdefault(f"{sub}/{group}", []).append(path)

    def _sound(self, path):
        s = self.sounds.get(path)
        if s is None:
            s = pygame.mixer.Sound(path)
            self.sounds[path] = s
        return s

    def sfx(self, name, volume=1.0):
        if not self.enabled:
            return
        paths = self.groups.get("sfx/" + name)
        if paths:
            s = self._sound(random.choice(paths))
            s.set_volume(min(1.0, volume * self.volume_sfx * self.vol_sfx))
            s.play()

    def announce(self, line, volume=1.0):
        if not self.enabled:
            return
        paths = self.groups.get("voice/announcer_" + line)
        if paths:
            s = self._sound(random.choice(paths))
            s.set_volume(min(1.0, volume * self.vol_voice))
            self.announcer_ch.play(s)

    def effort(self, slot, kind, volume=0.8, style="effort"):
        """Grunt / shout. kind: 'm' (normal), 'h' (deep), 'f' (high). style 'win' = long victory shout."""
        if not self.enabled:
            return
        paths = self.groups.get(f"voice/{style}_{kind}") or self.groups.get(f"voice/effort_{kind}")
        if paths:
            s = self._sound(random.choice(paths))
            s.set_volume(min(1.0, volume * self.vol_voice))
            self.effort_ch[slot].play(s)

    def music(self, track, fade_ms=600):
        if not self.enabled or track == self.track:
            return
        self.track = track
        try:
            pygame.mixer.music.fadeout(300)
            pygame.mixer.music.load(os.path.join(DATA, "audio", "music", MUSIC[track]))
            pygame.mixer.music.set_volume(self.volume_music * self.vol_music)
            pygame.mixer.music.play(-1, fade_ms=fade_ms)
        except pygame.error:
            pass

    def apply_settings(self, st):
        self.vol_music, self.vol_sfx, self.vol_voice = st.music / 10, st.sfx / 10, st.voice / 10
        self.story_on = getattr(st, "story_voice", True)
        if self.enabled:
            pygame.mixer.music.set_volume(self.volume_music * self.vol_music)

    def story(self, line_id):
        """Play one spoken story line (narration or a character). Music is turned down while it plays."""
        if not self.enabled or not self.story_on:
            return False
        path = os.path.join(DATA, "audio", "story", line_id + ".mp3")
        if not os.path.exists(path):
            return False
        s = self._sound(path)
        s.set_volume(min(1.0, 1.0 * self.vol_voice))
        self.story_ch.play(s)
        self._duck(True)
        return True

    def stop_story(self):
        if self.enabled:
            self.story_ch.stop()
            self._duck(False)

    def story_busy(self):
        return self.enabled and self.story_ch.get_busy()

    def _duck(self, on):
        if self.enabled and on != self.ducked:
            self.ducked = on
            pygame.mixer.music.set_volume(self.volume_music * self.vol_music * (0.35 if on else 1.0))

    def tick_duck(self):
        """Call every frame from story scenes: bring the music back up when the voice has finished."""
        if self.ducked and not self.story_busy():
            self._duck(False)

    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.fadeout(500)
            self.track = None
