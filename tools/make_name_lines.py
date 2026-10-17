#!/usr/bin/env python3
"""Generates the announcer's "<NAME> wins!" lines with a neural voice (edge-tts, needs internet once).
Run: .venv/bin/python tools/make_name_lines.py   then   make audio"""
import asyncio, os
import edge_tts
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Assets", "audio_src", "names")
VOICE = "en-US-GuyNeural"          # deep, announcer-like
NAMES = {"kaito": "Kaito", "brutus": "Brutus", "valeria": "Valeria", "mira": "Mira", "rudra": "Rudra", "reno": "Reno"}


async def main():
    os.makedirs(OUT, exist_ok=True)
    for cid, name in NAMES.items():
        await edge_tts.Communicate(f"{name} wins!", VOICE, rate="-6%", pitch="-8Hz", volume="+30%").save(os.path.join(OUT, f"win_{cid}.mp3"))
        print("saved", cid)

asyncio.run(main())
