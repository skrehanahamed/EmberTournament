#!/usr/bin/env python3
"""Generates the one-line victory quotes (spoken after a match win) into data/audio/quotes/<id>.mp3.
Run:  .venv/bin/python tools/make_win_quotes.py     (needs internet once, and ffmpeg)
Edit QUOTES to change the lines (also used by the game: ember/constants.py WIN_QUOTES must match, run with --write-json).
"""
import asyncio
import json
import os
import subprocess
import sys

import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_story_voice import VOICES  # noqa: E402

ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "data", "audio", "quotes")
RAW = os.path.join(ROOT, "Assets", "audio_src", "quotes")
QUOTES = {
    "kaito": ("kaito", "The fire teaches humility."),
    "brutus": ("brutus", "The crowd is mine!"),
    "valeria": ("valeria", "Too slow. Always too slow."),
    "mira": ("mira", "The storm chose me."),
    "rudra": ("rudra", "For my river. For my people."),
    "reno": ("reno", "Okay. That actually worked!"),
    "emperor": ("emperor", "Hollow. Forever."),
}


async def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(RAW, exist_ok=True)
    for cid, (who, text) in QUOTES.items():
        voice, rate, pitch, fx = VOICES[who]
        raw = os.path.join(RAW, cid + ".mp3")
        for attempt in range(4):
            try:
                await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(raw)
                break
            except edge_tts.exceptions.NoAudioReceived:
                await asyncio.sleep(1.5)
        flt = ("highpass=f=70,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,"
               "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse")
        if fx:
            flt += "," + fx
        flt += ",loudnorm=I=-16:TP=-1.5,apad=pad_dur=0.2"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", flt, "-ar", "44100", "-ac", "1",
                        "-c:a", "libmp3lame", "-q:a", "4", os.path.join(OUT, cid + ".mp3")], check=True)
        print("made", cid, "-", text)
    json.dump({k: v[1] for k, v in QUOTES.items()}, open(os.path.join(ROOT, "data", "quotes.json"), "w"), indent=1)


asyncio.run(main())
