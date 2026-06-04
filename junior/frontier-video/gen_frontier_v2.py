#!/usr/bin/env python3
"""
Frontier Video — v2 rebuild with correct visual concept.
Rider + dog as constant protagonist, always from behind, along a river.
Civilizations appear in the landscape around them.
First 4 scenes only — for Jesse approval before full rebuild.
"""

import requests
import time
import os
import json

RUNWAY_KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE_URL = "https://api.dev.runwayml.com"
HEADERS = {
    "Authorization": f"Bearer {RUNWAY_KEY}",
    "X-Runway-Version": "2024-11-06",
    "Content-Type": "application/json",
}
MODEL = "veo3.1_fast"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips_v2")
STATE_FILE = os.path.join(OUT_DIR, "state.json")

os.makedirs(OUT_DIR, exist_ok=True)

# Core visual lock — never changes across scenes
BASE = (
    "Cinematic landscape 16:9. "
    "Close tracking shot from directly behind a lone rider on horseback — "
    "rider wears a dark weathered frontier duster coat and wide-brim hat, never showing face. "
    "A black and white border collie trots alongside on the right of the horse. "
    "They move slowly forward along the muddy bank of a wide river. "
    "Desaturated muted color grade, overcast moody sky, prestige Western cinematic aesthetic. "
    "Photorealistic, anamorphic lens, film grain, deep shadows, no CGI, no text, no watermarks. "
    "Camera stays low and close behind the rider throughout."
)

# First 4 scenes — for Jesse approval
# VO context given for reference only, not included in prompt
SCENES = [
    (
        "s01",
        8,
        BASE + " "
        "The wilderness is completely untouched — no structures, no roads, no signs of settlement. "
        "Ancient primordial river valley, mountains in the distance, tall wild grass and reeds on the banks. "
        "Pre-dawn blue-grey light, mist rising from the water. The landscape vast and empty.",
    ),
    (
        "s02",
        8,
        BASE + " "
        "Very faint first traces of human presence along the far riverbank — "
        "a few simple reed and stick shelters in the distance, a thin wisp of smoke rising. "
        "Stone Age encampment barely visible, the river wide and slow, flat ancient plains stretching away. "
        "Cool grey morning light, timeless and sparse.",
    ),
    (
        "s04",
        8,
        BASE + " "
        "Ancient mud-brick ruins line both banks of the river — "
        "low domed Mesopotamian-style structures, some crumbling into the water, some partially submerged. "
        "A once-great river civilization, now quiet and dissolving back into earth. "
        "The rider passes through without stopping. Overcast sky, pale flat light, dust and silence.",
    ),
    (
        "s05",
        8,
        BASE + " "
        "Medieval stone walls and field terraces step up the hillsides flanking the river valley. "
        "Ruins of a stone mill on the far bank, collapsed timber bridge, overgrown cobbled path beside the water. "
        "Fertile land, green hills, grey sky. An agricultural world that was — now quieter, emptier. "
        "The rider and dog are the only moving things in the frame.",
    ),
]


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def submit(scene_id, duration, prompt):
    payload = {
        "model": MODEL,
        "promptText": prompt,
        "ratio": "1280:720",
        "duration": min(duration, 8),
    }
    resp = requests.post(
        f"{BASE_URL}/v1/text_to_video", headers=HEADERS, json=payload, timeout=30
    )
    if resp.status_code in (200, 201):
        task_id = resp.json().get("id")
        print(f"  [queued] {scene_id} -> {task_id}")
        return task_id
    else:
        print(f"  [ERROR] {scene_id}: {resp.status_code} {resp.text[:200]}")
        return None


def poll(task_id, timeout=600):
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(f"{BASE_URL}/v1/tasks/{task_id}", headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            time.sleep(10)
            continue
        data = resp.json()
        status = data.get("status", "")
        progress = data.get("progress", 0)
        if status == "SUCCEEDED":
            url = data.get("output", [None])[0]
            return url
        elif status in ("FAILED", "CANCELLED"):
            print(f"  [FAILED] task {task_id}: {data}")
            return None
        print(f"  ... {status} {int(progress * 100)}%")
        time.sleep(15)
    print(f"  [TIMEOUT] task {task_id}")
    return None


def download(url, path):
    r = requests.get(url, timeout=120)
    with open(path, "wb") as f:
        f.write(r.content)


def main():
    state = load_state()

    for scene_id, duration, prompt in SCENES:
        out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")

        if os.path.exists(out_path):
            print(f"[skip] {scene_id} already done")
            continue

        print(f"\n=== {scene_id} ({duration}s) ===")

        # Submit if not already queued
        task_id = state.get(scene_id, {}).get("task_id")
        if not task_id:
            task_id = submit(scene_id, duration, prompt)
            if not task_id:
                continue
            state[scene_id] = {"task_id": task_id, "status": "RUNNING"}
            save_state(state)

        # Poll
        print(f"  polling {task_id}...")
        url = poll(task_id)

        if url:
            print(f"  [done] downloading {scene_id}...")
            download(url, out_path)
            state[scene_id]["status"] = "DONE"
            save_state(state)
            print(f"  saved -> {out_path}")
        else:
            state[scene_id]["status"] = "FAILED"
            save_state(state)

    # Summary
    done = [s for s, _, _ in SCENES if os.path.exists(os.path.join(OUT_DIR, f"{s}.mp4"))]
    print(f"\nDone: {done} / {[s for s, _, _ in SCENES]}")


if __name__ == "__main__":
    main()
