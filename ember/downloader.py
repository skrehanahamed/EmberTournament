"""Asset recovery and dependency check for Ember Tournament.
If required data assets or dependencies are missing (e.g. user moved .exe standalone
or cloned without assets), this module automatically recovers and downloads them.
"""
import os
import sys
import urllib.request
import zipfile
import tempfile


RELEASE_ZIP_URL = "https://github.com/skrehanahamed/EmberTournament/releases/download/latest/EmberTournament-Windows-x64.zip"
FALLBACK_REPO_ZIP = "https://github.com/skrehanahamed/EmberTournament/archive/refs/heads/main.zip"


def _notify_user(title, message):
    """Display native message box on Windows or print to terminal."""
    if sys.platform == "win32":
        try:
            import ctypes
            # MB_OKCANCEL | MB_ICONINFORMATION = 0x1 | 0x40
            return ctypes.windll.user32.MessageBoxW(0, message, title, 0x1 | 0x40) == 1
        except Exception:
            pass
    print(f"[{title}] {message}")
    return True


def ensure_dependencies():
    """Ensure runtime dependencies are installed if running from Python source."""
    try:
        import pygame
    except ImportError:
        print("[Ember Tournament] 'pygame-ce' is required but not installed.")
        print("[Ember Tournament] Attempting automatic installation via pip...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame-ce"])
            print("[Ember Tournament] Successfully installed pygame-ce!")
        except Exception as e:
            print(f"[Ember Tournament] Automatic installation failed: {e}")
            print("Please run: pip install pygame-ce")


def ensure_assets(data_dir):
    """Verify that the data directory and key assets exist. If not, auto-download them."""
    marker = os.path.join(data_dir, "story.json")
    if os.path.exists(data_dir) and os.path.exists(marker):
        return data_dir

    target_dir = os.path.dirname(data_dir)
    if not os.access(target_dir, os.W_OK):
        target_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()

    proceed = _notify_user(
        "Ember Tournament - Missing Assets",
        "Required game data assets were not found in this folder.\n\n"
        "Ember Tournament will now automatically download and extract the required assets from GitHub.\n\n"
        "Click OK to begin automatic download."
    )
    if not proceed:
        return data_dir

    print("[Ember Tournament] Downloading game assets from GitHub...")
    temp_zip = os.path.join(tempfile.gettempdir(), "ember_assets_temp.zip")

    urls = [RELEASE_ZIP_URL, FALLBACK_REPO_ZIP]
    download_success = False

    for url in urls:
        try:
            print(f"[Ember Tournament] Connecting to {url}...")
            urllib.request.urlretrieve(url, temp_zip)
            download_success = True
            break
        except Exception as err:
            print(f"[Ember Tournament] Download attempt failed from {url}: {err}")

    if not download_success or not os.path.exists(temp_zip):
        _notify_user("Ember Tournament - Download Error", "Failed to download assets automatically. Please verify your internet connection or download EmberTournament-Windows-x64.zip manually from GitHub.")
        return data_dir

    print("[Ember Tournament] Extracting assets...")
    try:
        with zipfile.ZipFile(temp_zip, "r") as zf:
            for member in zf.namelist():
                # Extract any data/ files into the target data directory
                if "data/" in member:
                    parts = member.split("data/")
                    rel_path = parts[-1]
                    if not rel_path:
                        continue
                    out_path = os.path.join(data_dir, rel_path)
                    if member.endswith("/"):
                        os.makedirs(out_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(out_path), exist_ok=True)
                        with open(out_path, "wb") as f_out, zf.open(member) as f_in:
                            f_out.write(f_in.read())
        print(f"[Ember Tournament] Assets successfully restored to {data_dir}!")
    except Exception as e:
        print(f"[Ember Tournament] Extraction error: {e}")
    finally:
        if os.path.exists(temp_zip):
            try:
                os.remove(temp_zip)
            except OSError:
                pass

    return data_dir
