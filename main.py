#!/usr/bin/env python3
"""Ember Tournament - Main Entry Point.
Automatically verifies runtime dependencies and game assets, recovering missing files if needed.
"""
import sys

# 1. Verify runtime dependencies
try:
    import pygame
except ImportError:
    from ember.downloader import ensure_dependencies
    ensure_dependencies()

# 2. Verify game assets
from ember.constants import DATA
from ember.downloader import ensure_assets
ensure_assets(DATA)

# 3. Launch game
from ember.app import main

if __name__ == "__main__":
    main()
