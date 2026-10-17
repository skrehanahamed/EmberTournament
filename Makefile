# EMBER TOURNAMENT -   make run
PY := .venv/bin/python

.PHONY: run demo dev dev-boss setup assets audio story-art package clean help

help:
	@echo "make setup   - create the Python environment (first time only)"
	@echo "make run     - play the game"
	@echo "make demo    - watch CPU vs CPU"
	@echo "make dev     - developer mode (test hotkeys + debug overlay), starts in a Reno vs Brutus fight"
	@echo "make dev-boss - developer mode, straight into the Hollow Emperor fight (key 2 = FINAL FORM)"
	@echo "make assets  - re-cut the AI sprite sheets in Assets/ into data/ (needs a setup first)"
	@echo "make story-art - convert Assets/story/*.png cutscene pictures into data/story"
	@echo "make audio   - rebuild data/audio from Assets/audio_src (needs ffmpeg)"

setup:
	python3 -m venv .venv
	.venv/bin/pip install -q pygame-ce pillow numpy scipy

run:
	@test -d .venv || $(MAKE) setup
	$(PY) main.py

demo:
	$(PY) main.py --demo --p1 brutus --p2 valeria --stage volcano

dev:
	$(PY) main.py --dev --screen fight --p1 reno --p2 brutus --stage volcano

package:
	$(PY) tools/make_package.py

story-art:
	$(PY) tools/process_story_art.py

dev-boss:
	$(PY) main.py --dev --screen fight --p1 reno --boss

assets:
	$(PY) tools/process_assets.py

audio:
	$(PY) tools/build_audio.py

clean:
	rm -rf .venv __pycache__ ember/__pycache__
