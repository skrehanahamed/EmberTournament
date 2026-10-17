<div align="center">

  <img src="docs/images/logo.png" alt="Ember Tournament Logo" width="620" />

  <h3>A 1080p Pixel-Art Fighting Game in Python & Pygame-CE</h3>

  <p>
    <strong>Six legendary combatants. Three animated arenas. Cinematic supers and finishers.</strong>
  </p>

  <p>
    <a href="#-quick-download-windows-exe"><img src="https://img.shields.io/badge/Platform-Windows%20x64%20|%20macOS%20|%20Linux-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform Support" /></a>
    <a href="https://github.com"><img src="https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" /></a>
    <a href="https://pyga.me"><img src="https://img.shields.io/badge/Engine-pygame--ce-ED2939?style=for-the-badge" alt="Pygame-CE" /></a>
    <a href=".github/workflows/windows-exe.yml"><img src="https://img.shields.io/badge/CI%2FCD-Automated%20EXE%20Build-2ea44f?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" /></a>
    <img src="https://img.shields.io/badge/Display-1080p%20%40%2060%20FPS-FF8C00?style=for-the-badge" alt="Resolution" />
  </p>

  <p>
    <a href="#-quick-download-windows-exe"><b>Download Game (.exe)</b></a> •
    <a href="#-game-screenshots"><b>Screenshots</b></a> •
    <a href="#-fighter-roster"><b>Fighter Roster</b></a> •
    <a href="#-game-modes"><b>Modes</b></a> •
    <a href="#-controls--combos"><b>Controls</b></a> •
    <a href="#-run-from-source"><b>Run from Source</b></a> •
    <a href="#-github-actions--automated-exe-build"><b>GitHub Actions CI/CD</b></a>
  </p>

</div>

---

## 📸 Game Screenshots

<div align="center">
  <table border="0">
    <tr>
      <td width="50%">
        <img src="docs/images/fight_volcano.jpg" alt="Volcanic Ruins Battle" width="100%"/>
        <p align="center"><em>Reno vs Brutus — Volcanic Ruins</em></p>
      </td>
      <td width="50%">
        <img src="docs/images/fight_temple.jpg" alt="Sunset Shrine Battle" width="100%"/>
        <p align="center"><em>Valeria vs Kaito — Sunset Shrine</em></p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <img src="docs/images/fight_neon.jpg" alt="Neon City Battle" width="100%"/>
        <p align="center"><em>Mira vs Rudra — Neon City</em></p>
      </td>
      <td width="50%">
        <img src="docs/images/select.jpg" alt="Character Select Screen" width="100%"/>
        <p align="center"><em>Character Selection & Fighter Archetypes</em></p>
      </td>
    </tr>
    <tr>
      <td width="50%">
        <img src="docs/images/title.jpg" alt="Title Screen" width="100%"/>
        <p align="center"><em>Title Screen & Ambient Embers</em></p>
      </td>
      <td width="50%">
        <img src="docs/images/story_preview.jpg" alt="Arcade Story Cutscene" width="100%"/>
        <p align="center"><em>Arcade Story Mode Illustrated Cutscenes</em></p>
      </td>
    </tr>
  </table>
</div>

---

## ⚡ Game Features

* **Authentic 2D Fighting Engine**: Fixed-timestep 60 FPS physics, block-stun, hit-stun, corner pushback, jump arcs, and attack priority.
* **Combo & Cancel System**: Cancel normal attacks into heavy strikes, kicks, and devastating fireball specials on hit-confirm.
* **Cinematic Supers & Finishers**: Charge your Ember Meter through combat to trigger screen-shattering Super Moves and match-winning cinematic Finishers.
* **Full Controller Support**: Plug-and-play support for PlayStation DualSense (PS5), Xbox Wireless Controllers, and standard PC gamepads with custom vibration/rumble feedback and on-screen button prompts.
* **Hardware GPU Scaling**: Native 1920×1080 internal resolution smoothly presented in resizable windowed or borderless fullscreen modes.
* **Full Audio & Voice Acting**: Custom sound effects, dynamic punch/kick impacts, stage music, and voice-acted story narration.

---

## 👥 Fighter Roster

Six unique martial artists with distinct archetypes, hitboxes, frame data, and special moves:

| Fighter | Archetype | Style & Lore | Super Move & Finisher |
| :---: | :---: | :--- | :--- |
| <img src="docs/images/portraits/reno.png" width="90" height="90" alt="Reno"/> <br/> **RENO** | **All-Rounder** | An ordinary brawler with an extraordinary temper. Signs every fireball and strike with a blazing neon "R". | **Super**: *R-Sign Blast*<br/>**Finisher**: *R-Sign Annihilation* |
| <img src="docs/images/portraits/kaito.png" width="90" height="90" alt="Kaito"/> <br/> **KAITO** | **All-Rounder** | A young monk who lost his master and his sacred blade. Fights with disciplined dragon-flame fists. | **Super**: *Dragon Breath*<br/>**Finisher**: *Dragon Fist of Embers* |
| <img src="docs/images/portraits/brutus.png" width="90" height="90" alt="Brutus"/> <br/> **BRUTUS** | **Grappler** | Exiled coliseum powerhouse with heavy armor and crushing high-damage strikes that dominate close range. | **Super**: *Magma Crush*<br/>**Finisher**: *Molten Hammer* |
| <img src="docs/images/portraits/valeria.png" width="90" height="90" alt="Valeria"/> <br/> **VALERIA** | **Rushdown** | A desert assassin wielding crimson embers. Blistering walk speed and relentless offensive pressure. | **Super**: *Crimson Tempest*<br/>**Finisher**: *Crimson Desert Storm* |
| <img src="docs/images/portraits/rudra.png" width="90" height="90" alt="Rudra"/> <br/> **RUDRA** | **Brawler** | Bengal's Iron Fist. A delta wrestler whose sacred flames empower devastating close-combat barrages. | **Super**: *Tiger Roar*<br/>**Finisher**: *Bengal Tiger Flame* |
| <img src="docs/images/portraits/mira.png" width="90" height="90" alt="Mira"/> <br/> **MIRA** | **Zoner** | Storm mage controlling the battlefield from afar with high-velocity electric projectiles and long reach. | **Super**: *Storm Caller*<br/>**Finisher**: *Thunder Judgement* |

---

## 🏛️ Stages

| Neon City | Sunset Shrine | Volcanic Ruins |
| :---: | :---: | :---: |
| <img src="docs/images/stages/neon.png" width="280" alt="Neon City" /> | <img src="docs/images/stages/temple.png" width="280" alt="Sunset Shrine" /> | <img src="docs/images/stages/volcano.png" width="280" alt="Volcanic Ruins" /> |
| Cyberpunk metropolis drenched in torrential rain | Sacred mountain temple with drifting cherry petals | Molten arena surrounded by rising sparks and ash |

---

## 🎮 Game Modes

* **Arcade Story Mode**: Embark on a 7-chapter narrative journey as Reno. Battle through the tournament ranks, uncover the secret of the Dragon Cores, and defeat the Hollow Emperor in a climactic showdown. Features voiced dialogue and chapter art.
* **Versus CPU**: Test your skills against computer-controlled opponents across three selectable difficulty levels (*Easy*, *Normal*, *Hard*).
* **Versus 2-Player (Local)**: Challenge a friend locally on a shared keyboard or dual controllers.
* **CPU vs CPU**: Watch AI combatants battle it out in demonstration mode.
* **Developer Mode (`make dev`)**: Real-time hitboxes, frame data counters, hurtbox debugging, and quick-swap fight triggers.

---

## 🕹️ Controls & Combos

### Keyboard Controls

| Action | Player 1 | Player 2 |
| :--- | :---: | :---: |
| **Move Left / Right** | <kbd>A</kbd> / <kbd>D</kbd> | <kbd>←</kbd> / <kbd>→</kbd> |
| **Jump / Crouch** | <kbd>W</kbd> / <kbd>S</kbd> | <kbd>↑</kbd> / <kbd>↓</kbd> |
| **Block** | Hold away from opponent | Hold away from opponent |
| **Light Punch** | <kbd>F</kbd> | <kbd>J</kbd> |
| **Heavy Punch** | <kbd>G</kbd> | <kbd>K</kbd> |
| **Kick** | <kbd>H</kbd> | <kbd>L</kbd> |
| **Fireball (Special)** | <kbd>T</kbd> | <kbd>I</kbd> |
| **Super Move** | <kbd>Y</kbd> | <kbd>O</kbd> |
| **Pause / Back** | <kbd>Esc</kbd> | <kbd>Esc</kbd> |
| **Fullscreen** | <kbd>F11</kbd> | <kbd>F11</kbd> |
| **Toggle CPU / Player 2** | <kbd>F1</kbd> | <kbd>F1</kbd> |

### Game Controller (PS5 DualSense / Xbox / Standard Gamepads)

Gamepads are automatically recognized upon plugging in or pairing over Bluetooth:

| Button (PlayStation) | Button (Xbox) | Action |
| :--- | :--- | :--- |
| **D-Pad / Left Stick** | **D-Pad / Left Stick** | Move, Jump, Crouch (Double-tap left/right to Dash) |
| **Square (□)** | **X** | Light Attack |
| **Triangle (△)** | **Y** | Heavy Attack |
| **Cross (✕)** | **A** | Kick |
| **Circle (○)** | **B** | Fireball Special (Ember) |
| **R1 / R2** | **RB / RT** | Super Move |
| **L1 / L2** | **LB / LT** | Quick Dash |
| **Options / Start** | **Menu / Start** | Pause Match / Menu Back |

### Special Moves & Combo Execution

* **Quarter-Circle Fireball**: Tap <kbd>Down</kbd>, <kbd>Down+Forward</kbd>, <kbd>Forward</kbd> + <kbd>Punch</kbd> (or hit your assigned Special button).
* **Hit Cancels**: Connect with a **Light Attack**, then immediately input **Heavy**, **Kick**, or **Fireball** to cancel recovery frames into a fluid combo sequence.
* **Super Move**: When the bottom Ember meter is fully charged, activate your Super to execute an unblockable multi-hit surge.

---

## 📦 Quick Download: Windows (.exe)

You do **not** need Python installed to play the pre-compiled Windows version:

1. Go to the **[Actions Tab](../../actions)** in this repository (or check the **Releases** section on the right).
2. Click the latest successful build under **"Build Windows EXE"**.
3. Under **Artifacts**, download **`EmberTournament-Windows-x64`**.
4. Unzip the downloaded file and double-click **`EmberTournament.exe`** to launch the game!

---

## 💻 Run from Source (macOS, Linux, Windows)

### Prerequisites

* Python **3.10** or higher
* `pip` package manager

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Set Up Virtual Environment

On **macOS / Linux**:
```bash
make setup
make run
```

Or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On **Windows**:
Double-click `run_windows.bat` or run:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Command Line Options

```bash
python main.py --help
  --demo                 # Launch directly into CPU vs CPU demonstration
  --screen fight         # Jump straight into battle
  --p1 reno --p2 brutus  # Choose starting fighters
  --stage volcano        # Choose stage: neon, temple, volcano
  --dev                  # Enable developer hotkeys and hitbox overlay
  --fullscreen           # Launch directly in fullscreen mode
```

---

## 🚀 GitHub Actions: Automated Windows EXE Build

This repository includes a pre-configured, production-ready continuous integration workflow in [`.github/workflows/windows-exe.yml`](.github/workflows/windows-exe.yml).

### How It Works:
1. **Automated Triggers**: Runs automatically whenever code is pushed to `main` or `master`, on pull requests, or when a release tag (`v*`) is created.
2. **Manual Trigger (`workflow_dispatch`)**: You can trigger a new Windows build at any time by navigating to **GitHub Actions** → **Build Windows EXE** → **Run workflow**.
3. **Artifact Packaging**: The runner installs dependencies on `windows-latest`, compiles a self-contained executable with PyInstaller (embedding custom window icons and assets), and packages it into `EmberTournament-Windows-x64.zip`.
4. **Automated Releases**: Pushing a git tag (e.g., `git tag v1.0.0 && git push origin v1.0.0`) automatically publishes a formal GitHub Release with the standalone ZIP attached!

### Building Locally on Windows

If you are on a Windows machine and want to create the `.exe` locally:
```cmd
build_windows.bat
```
The compiled game will be generated in `dist\EmberTournament\EmberTournament.exe`.

---

## 📤 Uploading This Game to GitHub (Step-by-Step)

To upload this repository to GitHub for the first time:

```bash
# 1. Initialize git in this directory (if not already initialized)
git init -b main

# 2. Stage all project files (ignoring build folders & caches automatically via .gitignore)
git add .

# 3. Create your initial commit
git commit -m "Initial commit: Ember Tournament 1080p fighting game"

# 4. Create a new repository on github.com, then connect your local repo
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/<YOUR-REPOSITORY-NAME>.git

# 5. Push code to GitHub
git push -u origin main
```

Once pushed, GitHub Actions will automatically start building the Windows `.exe` under the **Actions** tab!

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── windows-exe.yml     # Automated GitHub Actions workflow for Windows EXE
├── docs/images/            # High-resolution screenshots, portraits, stages, and logo
├── ember/                  # Core game engine & state modules
│   ├── app.py              # Main application loop, display & scaling
│   ├── assets.py           # Frame slicing, animation loader, font caching
│   ├── audio.py            # Sound manager, BGM streaming, SFX pooling
│   ├── constants.py        # Physics constants, palettes, character stats
│   ├── fighter.py          # State machine, collision boxes, combos, supers
│   ├── gamepad.py          # SDL controller abstraction, haptics & rumble
│   ├── hud.py              # Health gauges, timer, combo counter, supers
│   ├── input.py            # Input buffering, keyboard & AI controllers
│   ├── screens.py          # Title, Character Select, Fight, & Results scenes
│   ├── settings.py         # Persistent configuration (~/.ember_tournament)
│   └── story.py            # Arcade story runner & narrative cutscenes
├── data/                   # Bundled production game assets (audio, sprites, fonts)
├── Assets/                 # Raw sprite sheets & master audio sources
├── tools/                  # Asset pipeline tools (sprite slicers, voice tools)
├── icon.ico                # Official Windows application icon
├── build_windows.bat       # Local one-click Windows compiler script
├── run_windows.bat         # One-click Windows game runner
├── Makefile                # Cross-platform development commands
├── requirements.txt        # Runtime dependencies (pygame-ce)
└── main.py                 # Game entry point
```

---

## 📜 Credits & License

* **Engine**: Built with [pygame-ce](https://pyga.me/) (Community Edition).
* **Font**: *Press Start 2P* by CodeMan38 (SIL Open Font License).
* **Gamepad Icons**: Kenney *Input Prompts* (CC0 Public Domain).
* **Audio & Music**: CC0 Public Domain compositions by Kenney, Pompei2, Tozan, and CleytonRX (see `Assets/audio_src/CREDITS.md`).
* **Game Code**: Open source under the [MIT License](LICENSE).
