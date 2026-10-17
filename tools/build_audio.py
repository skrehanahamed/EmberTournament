#!/usr/bin/env python3
"""Builds data/audio from the raw CC0 sources in Assets/audio_src (+ a few synthesised effects).
Needs: numpy, ffmpeg.   Run: .venv/bin/python tools/build_audio.py"""
import glob
import os
import shutil
import subprocess
import wave

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "Assets", "audio_src")
OUT = os.path.join(ROOT, "data", "audio")
SR = 44100
rng = np.random.default_rng(7)


def write_wav(path, x, gain=0.9):
    x = np.asarray(x, dtype=np.float64)
    x = x / (np.max(np.abs(x)) or 1.0) * gain
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def t_(sec):
    return np.arange(int(sec * SR)) / SR


def lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / (1.0 + (f / cutoff) ** 4), len(x))


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def noise(sec):
    return rng.standard_normal(int(sec * SR))


def reverb(x, sec=1.6, wet=0.25):
    n = int(sec * SR)
    ir = lowpass(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.2), 3500)
    size = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y / (np.max(np.abs(y)) + 1e-9) * np.max(np.abs(x)) * wet * 1.6


def punch(sec, f0, f1, noise_cut, body, snap, seed):
    """Soft body-impact thud: a falling low sine plus a short, dark noise slap. No ringing partials, so nothing metallic."""
    r = np.random.default_rng(seed)
    n = int(sec * SR)
    t = np.arange(n) / SR
    sweep = f1 + (f0 - f1) * np.exp(-t * 38)
    thump = np.sin(2 * np.pi * np.cumsum(sweep) / SR) * np.exp(-t * (16 if body < 1.2 else 11))
    slap = lowpass(r.standard_normal(n), noise_cut) * np.exp(-t * 70)
    slap = lowpass(slap, noise_cut * 0.8)
    click = lowpass(r.standard_normal(n), 900) * np.exp(-t * 300) * snap
    x = thump * body + slap * 0.9 + click
    x[:60] *= np.linspace(0, 1, 60)
    return lowpass(x, 5200)


def synth(sfx):
    for i in range(5):
        write_wav(f"{sfx}/hit_light_{i}.wav", punch(0.17, 190 + i * 14, 70, 2300 + i * 150, 1.0, 0.25, 20 + i), 0.85)
        write_wav(f"{sfx}/hit_heavy_{i}.wav", punch(0.30, 150 + i * 10, 48, 1700 + i * 120, 1.6, 0.35, 40 + i), 0.95)
        # block: a muffled, short "thwump" (padded forearm), clearly softer and lower than a hit
        write_wav(f"{sfx}/block_{i}.wav", punch(0.14, 130 + i * 8, 85, 1100 + i * 60, 0.8, 0.0, 60 + i), 0.6)
    def whoosh(sec, f0, f1):
        n = noise(sec)
        m = np.linspace(0, 1, len(n))
        out = highpass(lowpass(n, f0) * (1 - m) + lowpass(n, f1) * m, 220)
        return out * np.sin(np.pi * m) ** 1.5

    write_wav(f"{sfx}/whoosh_light.wav", whoosh(0.16, 900, 2600), 0.33)
    write_wav(f"{sfx}/whoosh_heavy.wav", whoosh(0.28, 600, 2200), 0.42)
    write_wav(f"{sfx}/jump.wav", whoosh(0.22, 600, 2400), 0.4)
    t = t_(0.9)
    m = np.linspace(0, 1, len(t))
    nz = noise(0.9)
    fire = (lowpass(nz, 900) * (1 - m) + lowpass(nz, 4000) * m) * np.sin(np.pi * m) ** 0.7
    fire += np.sin(2 * np.pi * (180 + 500 * t) * t) * 0.35 * np.exp(-t * 2)
    write_wav(f"{sfx}/fireball_cast.wav", fire, 0.7)
    t = t_(0.7)
    boom = np.sin(2 * np.pi * (90 * np.exp(-t * 3)) * t) * np.exp(-t * 6) + lowpass(noise(0.7), 2500) * np.exp(-t * 12)
    write_wav(f"{sfx}/fireball_hit.wav", boom)
    t = t_(0.25)
    write_wav(f"{sfx}/land.wav", np.sin(2 * np.pi * 70 * t) * np.exp(-t * 25) + lowpass(noise(0.25), 800) * np.exp(-t * 30), 0.6)
    t = t_(4.0)
    gong = sum(np.sin(2 * np.pi * f * t + p) * a * np.exp(-t * d) for f, a, d, p in
               [(98, 1, 1.0, 0), (147, .8, 1.3, 1), (196.8, .7, 1.6, 2), (271, .5, 2.0, 3), (392, .35, 2.6, 4), (577, .2, 3.4, 5)])
    gong = gong * np.minimum(1, t / 0.01) + lowpass(noise(4.0), 2000) * np.exp(-t * 14) * 0.4
    write_wav(f"{sfx}/gong.wav", reverb(gong, 2.0, 0.3))
    t = t_(0.12)
    write_wav(f"{sfx}/ui_move.wav", np.sin(2 * np.pi * 880 * t) * np.exp(-t * 35), 0.4)
    t = t_(0.25)
    write_wav(f"{sfx}/ui_select.wav", (np.sin(2 * np.pi * 660 * t) + np.sin(2 * np.pi * 990 * t) * 0.6) * np.exp(-t * 14), 0.5)


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *args], check=True)


def main():
    for sub in ("sfx", "voice", "music"):
        shutil.rmtree(os.path.join(OUT, sub), ignore_errors=True)
        os.makedirs(os.path.join(OUT, sub))
    sfx, voice, music = (os.path.join(OUT, s) for s in ("sfx", "voice", "music"))
    synth(sfx)
    for f in glob.glob(f"{SRC}/announcer/*.ogg"):
        shutil.copy(f, f"{voice}/announcer_{os.path.basename(f)}")
    for i, f in enumerate(sorted(glob.glob(f"{SRC}/grunts/*.flac")), 1):
        raw = f"{voice}/_raw.wav"
        ffmpeg("-i", f, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", raw)
        with wave.open(raw) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
        # three voices from one recording: normal, deep (slower/lower) and high (faster/higher)
        for kind, factor in (("m", 1.0), ("h", 0.8), ("f", 1.32), ("r", 0.97)):
            idx = np.arange(0, len(x) - 1, factor)
            y = np.interp(idx, np.arange(len(x)), x)
            write_wav(f"{voice}/effort_{kind}_{i:02d}.wav", y, 0.9)
        # keep the long ones for victory shouts
        if len(x) / SR > 0.55:
            for kind, factor in (("m", 0.95), ("h", 0.78), ("f", 1.25), ("r", 0.97)):
                idx = np.arange(0, len(x) - 1, factor)
                y = np.interp(idx, np.arange(len(x)), x)
                y = np.concatenate([y, np.zeros(int(0.5 * SR))])
                write_wav(f"{voice}/win_{kind}_{i:02d}.wav", reverb(y, 0.9, 0.3), 0.95)
        os.remove(raw)
    ffmpeg("-i", f"{SRC}/music/determined_pursuit_loop.wav", "-c:a", "libmp3lame", "-q:a", "3", f"{music}/fight.mp3")
    shutil.copy(f"{SRC}/music/epic_combat.ogg", f"{music}/menu.ogg")
    shutil.copy(f"{SRC}/music/battle_rpg_theme.ogg", f"{music}/final.ogg")
    # announcer "<name> wins!" lines: trimmed, deepened a little, with an arena echo so they match the other announcer lines
    for f in sorted(glob.glob(f"{SRC}/names/*.mp3")):
        cid = os.path.splitext(os.path.basename(f))[0]
        raw = f"{voice}/_n.wav"
        ffmpeg("-i", f, "-ar", str(SR), "-ac", "1",
               "-af", "highpass=f=70,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,"
                      "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
                      "acompressor=threshold=-22dB:ratio=3:makeup=3,loudnorm=I=-15:TP=-1.5", "-c:a", "pcm_s16le", raw)
        with wave.open(raw) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
        x = reverb(np.concatenate([x, np.zeros(int(0.5 * SR))]), 1.0, 0.18)
        write_wav(f"{voice}/announcer_{cid}.wav", x, 0.95)
        os.remove(raw)
    os.makedirs(os.path.join(ROOT, "data", "fonts"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "Assets", "fonts", "PressStart2P.ttf"), os.path.join(ROOT, "data", "fonts", "PressStart2P.ttf"))
    print("audio built:", sum(len(files) for _, _, files in os.walk(OUT)), "files")


if __name__ == "__main__":
    main()
