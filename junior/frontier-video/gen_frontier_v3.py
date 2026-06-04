#!/usr/bin/env python3
"""
Frontier Video — v3 rebuild with Jesse's corrections:
- Smaller, narrower river
- Civilizations rise and fall from mud organically
- NO CGI, NO video game aesthetic — photographic film realism only
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
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips_v3")
STATE_FILE = os.path.join(OUT_DIR, "state.json")

os.makedirs(OUT_DIR, exist_ok=True)

# Core visual lock — never changes
BASE = (
    "Cinematic landscape 16:9. "
    "Close tracking shot from directly behind a lone rider on horseback — "
    "rider wears a dark weathered frontier duster coat and wide-brim hat, never showing face. "
    "A black and white border collie trots alongside on the right of the horse. "
    "They move slowly forward along the muddy bank of a narrow winding river. "
    "Shot on 35mm film, Kodak Vision3 stock, real outdoor location, natural available light only. "
    "Desaturated muted color grade, overcast sky, prestige feature film aesthetic. "
    "Photorealistic documentary footage — NOT CGI, NOT animation, NOT video game, NOT digital art, "
    "NOT rendered, NOT Unreal Engine. Real textures, real mud, real water, real light. "
    "Organic film grain, anamorphic lens distortion, deep practical shadows. "
    "Camera stays low and close behind the rider throughout."
)

SCENES = [
    (
        "s01",
        8,
        BASE + " "
        "Completely untouched wilderness, no structures, no human presence. "
        "Narrow winding river through ancient plains, tall reeds and wild grass on the muddy banks. "
        "Mountains far in the distance. Pre-dawn blue-grey mist lifting off the water.",
    ),
    (
        "s02",
        8,
        BASE + " "
        "First faint signs of human presence — crude reed shelters barely visible on the far bank, "
        "a thin wisp of smoke. Narrow muddy river, flat ancient plains stretching away. "
        "The mud banks show faint traces of early settlement. Cool grey dawn light.",
    ),
    (
        "s04",
        8,
        BASE + " "
        "Ancient mud-brick structures rise organically from the muddy riverbanks — "
        "low domed forms and crumbling arched walls made of the same mud as the earth itself, "
        "indistinguishable from the ground they emerge from, some half-dissolved into the shallow river. "
        "Real weathered mud-brick, real erosion, real decay. Flat overcast light. Dust and silence.",
    ),
    (
        "s05",
        8,
        BASE + " "
        "Crumbling stone walls and overgrown cobbled paths on the narrow riverbanks — "
        "a collapsed mill foundation dissolving into the mud, terraced hillsides eroding. "
        "Real moss, real weathered stone, real decay returning to earth. "
        "Grey overcast sky. The rider and dog the only living things moving in the frame.",
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

        task_id = state.get(scene_id, {}).get("task_id")
        if not task_id:
            task_id = submit(scene_id, duration, prompt)
            if not task_id:
                continue
            state[scene_id] = {"task_id": task_id, "status": "RUNNING"}
            save_state(state)

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

    done = [s for s, _, _ in SCENES if os.path.exists(os.path.join(OUT_DIR, f"{s}.mp4"))]
    print(f"\nDone: {done} / {[s for s, _, _ in SCENES]}")


if __name__ == "__main__":
    main()
