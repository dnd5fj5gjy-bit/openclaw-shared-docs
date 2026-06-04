#!/usr/bin/env python3
"""Generate all VO with Bill voice - deep, slow, wise American narrator."""
import os, time, requests

API_KEY = "sk_1b22744129f73cf892c424001c48ec0d2ce2b5600e1f3a5d"
VOICE_ID = "pqHfZKP75CvOlQylNhV4"  # Bill - Wise, Mature, Balanced
MODEL = "eleven_multilingual_v2"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio-el")
os.makedirs(OUT_DIR, exist_ok=True)

VOICE_SETTINGS = {
    "stability": 0.22,           # Lower = more character/gravelly
    "similarity_boost": 0.92,    # High = stays true to Bill's voice
    "style": 0.68,               # Higher = more dramatic/emotive
    "use_speaker_boost": True,
    "speed": 0.82                # Slower delivery
}

SCENES = [
    ("s01", "For two hundred thousand years..."),
    ("s02", "...we've built our lives around what we could not live without."),
    ("s04", "We shaped our first cities from mud and silt."),
    ("s05", "We built where the soil was fertile and the ground held firm."),
    ("s06", "We hung our lives off wires and roads and pipes. We handed our water to the reservoir. Our power to the grid. Our planning to a committee. We lived where the system allowed us to."),
    ("s07", "Every home we have ever built has been built by necessity. We have lived where the river ran and the land was rich and the roads ran through... never where we longed to."),
    ("s08", "The real renegades aren't building cities anymore. We're walking back out into the land. Taking everything we need with us."),
    ("s09", "The sun is our power."),
    ("s11", "The water comes from the air itself,"),
    ("s12", "drawn down by an atmospheric water generator."),
    ("s15", "Our walls hold when the wind comes,"),
    ("s16", "when fires burn,"),
    ("s17", "when the ground itself moves under us,"),
    ("s18", "when the rivers rise."),
    ("s19", "No councils to ask. No grid to wait on. No permission to need."),
    ("s20", "Raised in three days. On any land we choose."),
    ("s21", "Wherever we choose to stand."),
]

URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
HEADERS = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

print(f"Generating {len(SCENES)} VO scenes with Bill (slow, gravelly)...")

for scene_id, text in SCENES:
    out_file = os.path.join(OUT_DIR, f"{scene_id}.mp3")
    # Force regenerate all with new settings
    print(f"  [gen]  {scene_id}: {text[:60]}...")
    payload = {"text": text, "model_id": MODEL, "voice_settings": VOICE_SETTINGS}
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    if resp.status_code == 200:
        with open(out_file, "wb") as f:
            f.write(resp.content)
        print(f"  [ok]   {scene_id} ({len(resp.content)/1024:.0f}KB)")
    else:
        print(f"  [err]  {scene_id}: {resp.status_code} {resp.text[:200]}")
    time.sleep(0.5)

print("\nAll VO generated with Bill voice.")
