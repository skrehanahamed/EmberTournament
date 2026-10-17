#!/usr/bin/env python3
"""Generates the spoken narration and character voices for the Arcade Story from data/story.json.
Uses free neural voices (edge-tts, needs internet once). Output: data/audio/story/<id>.mp3

Line ids:  prologue_<i>   epilogue_<i>   ch<chapter>_before_<i>   ch<chapter>_after_<i>
Run:  .venv/bin/python tools/make_story_voice.py          (re-run after editing the story text; unchanged lines are skipped)
      .venv/bin/python tools/make_story_voice.py --force  (regenerate everything)
"""
import asyncio
import hashlib
import json
import os
import subprocess
import sys

import edge_tts

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "Assets", "audio_src", "story")
OUT = os.path.join(ROOT, "data", "audio", "story")

# speaker -> (voice, rate, pitch, ffmpeg effects). Natural multilingual neural voices at their default
# rate/pitch; only the Emperor and the Voice get a light room reverb.
VOICES = {
    "narrator": ("en-AU-WilliamMultilingualNeural", "+0%", "+0Hz", ""),
    "reno": ("en-US-AndrewMultilingualNeural", "+0%", "+0Hz", ""),
    "kaito": ("en-US-BrianMultilingualNeural", "+0%", "+0Hz", ""),
    "valeria": ("en-US-AvaMultilingualNeural", "+0%", "+0Hz", ""),
    "mira": ("en-US-EmmaMultilingualNeural", "+0%", "+0Hz", ""),
    "brutus": ("en-US-RogerNeural", "+0%", "+0Hz", ""),
    "rudra": ("en-IN-PrabhatNeural", "+0%", "+0Hz", ""),
    "emperor": ("en-GB-RyanNeural", "-4%", "+0Hz", "aecho=0.8:0.9:60:0.2"),
    "voice": ("en-GB-ThomasNeural", "-4%", "+0Hz", "aecho=0.8:0.88:90|180:0.25|0.15"),
}


def collect():
    st = json.load(open(os.path.join(ROOT, "data", "story.json"), encoding="utf-8"))
    items = []
    for i, text in enumerate(st["prologue"]):
        items.append((f"prologue_{i}", "narrator", text))
    for ch in st["chapters"]:
        for part in ("before", "after"):
            for i, ln in enumerate(ch[part]):
                items.append((f"ch{ch['id']}_{part}_{i}", ln["who"], ln["text"]))
    for i, text in enumerate(st["epilogue"]):
        if text.strip().upper() == "THE END":
            continue
        items.append((f"epilogue_{i}", "narrator", text))
    return items


def spoken(text):
    return " ".join(text.replace("\"", "").split())


async def main(force):
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    sig_path = os.path.join(RAW, "signatures.json")
    sigs = json.load(open(sig_path)) if os.path.exists(sig_path) else {}
    done = 0
    for lid, who, text in collect():
        voice, rate, pitch, fx = VOICES.get(who, VOICES["narrator"])
        sig = hashlib.md5(f"{who}|{voice}|{rate}|{pitch}|{fx}|{text}".encode()).hexdigest()
        out = os.path.join(OUT, lid + ".mp3")
        if not force and sigs.get(lid) == sig and os.path.exists(out):
            continue
        raw = os.path.join(RAW, lid + ".mp3")
        for attempt in range(4):
            try:
                await edge_tts.Communicate(spoken(text), voice, rate=rate, pitch=pitch).save(raw)
                break
            except edge_tts.exceptions.NoAudioReceived:
                if attempt == 3:
                    raise
                await asyncio.sleep(1.5)
        flt = ("highpass=f=70,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,"
               "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse")
        if fx:
            flt += "," + fx
        flt += ",loudnorm=I=-16:TP=-1.5,apad=pad_dur=0.25"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-af", flt, "-ar", "44100", "-ac", "1",
                        "-c:a", "libmp3lame", "-q:a", "4", out], check=True)
        sigs[lid] = sig
        done += 1
        print("made", lid, f"[{who}]")
    json.dump(sigs, open(sig_path, "w"), indent=1)
    print(f"done: {done} new / {len(collect())} total lines")


if __name__ == "__main__":
    asyncio.run(main("--force" in sys.argv))
