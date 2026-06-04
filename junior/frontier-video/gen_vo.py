#!/usr/bin/env python3
"""Generate VO audio for each Wildernests Frontier scene."""
import subprocess, os, sys

VOICE = "bm_george"  # British male - right for Wildernests brand

SCENES = [
    ("s01", 8,  "For two hundred thousand years..."),
    ("s02", 10, "...we've built our lives around what we could not live without."),
    ("s04", 10, "We shaped our first cities from mud and silt."),
    ("s05", 10, "We built where the soil was fertile and the ground held firm."),
    ("s06", 10, "We hung our lives off wires and roads and pipes. We handed our water to the reservoir. Our power to the grid. Our planning to a committee. We lived where the system allowed us to."),
    ("s07", 10, "Every home we have ever built has been built by necessity. We have lived where the river ran and the land was rich and the roads ran through, never where we longed to."),
    ("s08", 7,  "The real renegades aren't building cities anymore. We're walking back out into the land. Taking everything we need with us."),
    ("s09", 4,  "The sun is our power."),
    ("s11", 4,  "The water comes from the air itself,"),
    ("s12", 4,  "drawn down by an atmospheric water generator."),
    ("s15", 4,  "Our walls hold when the wind comes,"),
    ("s16", 3,  "when fires burn,"),
    ("s17", 3,  "when the ground itself moves under us,"),
    ("s18", 3,  "when the rivers rise."),
    ("s19", 5,  "No councils to ask, no grid to wait on, no permission to need."),
    ("s20", 5,  "Raised in three days. On any land we choose."),
    ("s21", 10, "Wherever we choose to stand."),
]

OUT_DIR = os.path.join(os.path.dirname(__file__), "audio")
TOOL = os.path.expanduser("~/agents/shared/tools/generate_voice_local.py")

for scene_id, duration, text in SCENES:
    out_file = os.path.join(OUT_DIR, f"{scene_id}.ogg")
    if os.path.exists(out_file):
        print(f"  [skip] {scene_id} already exists")
        continue
    print(f"  [gen]  {scene_id}: {text[:60]}...")
    result = subprocess.run(
        ["python3", TOOL, "--text", text, "--output", out_file, "--voice", VOICE],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  [err]  {scene_id}: {result.stderr[:200]}")
    else:
        print(f"  [ok]   {scene_id}")

print("VO generation complete.")
