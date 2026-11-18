#!/usr/bin/env python3
"""
PurePlated Master Daily Autonomous Automation Pipeline
------------------------------------------------------
Runs once daily (or on manual trigger):
1. Ingests or synthesizes a fresh healthy daily meal.
2. Generates 1000x1500 high-converting Pinterest Pin graphic.
3. Compiles static site, Google Recipe JSON-LD schemas, sitemap, and RSS feeds.
4. Advances the Pinterest publishing queue.
"""

import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.engine.recipe_generator import generate_and_publish_daily_recipe
from src.pinterest.publish_pins import publish_daily_pin

LOG_PATH = os.path.join(BASE_DIR, "scripts", "daily_pipeline.log")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def run():
    log("=" * 60)
    log("Starting PurePlated Daily Autonomous Pipeline...")
    log("=" * 60)

    try:
        # Step 1 & 2: Generate recipe and Pin, recompile site
        log("[Step 1/3] Synthesizing fresh daily healthy recipe and generating Pin...")
        recipe = generate_and_publish_daily_recipe()
        log(f"[✓] Published new recipe: '{recipe['title']}' ({recipe['protein']}g protein)")

        # Step 3: Advance Pinterest queue
        log("[Step 2/3] Dispatching next pin in queue for syndication...")
        publish_daily_pin()
        log("[✓] Pinterest queue successfully rotated.")

        log("[Step 3/3] Master pipeline completed successfully.")
        log("=" * 60 + "\n")
        return True
    except Exception as e:
        log(f"[!] Pipeline Error: {str(e)}")
        return False

if __name__ == "__main__":
    run()
