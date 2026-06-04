#!/usr/bin/env python3
"""
Frontier Video — v4 with image-to-video chaining for continuity.
s01 is text-to-video (establishes rider/horse/dog).
Every subsequent scene uses the last frame of the previous clip as seed.
This locks the character visually across the entire video — one-shot feel.
"""

import requests
import subprocess
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
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips_v4")
STATE_FILE = os.path.join(OUT_DIR, "state.json")

os.makedirs(OUT_DIR, exist_ok=True)

# Core visual lock — repeated in every prompt to maintain consistency
BASE = (
    "Cinematic landscape 16:9. "
    "Continuous tracking shot from directly behind the same lone rider on horseback — "
    "rider wears a dark weathered frontier duster coat and wide-brim hat, back to camera, never showing face. "
    "The same black and white border collie trots alongside on the right of the horse. "
    "They move slowly forward along the muddy bank of a narrow winding river. "
    "Shot on 35mm film, Kodak Vision3 stock, real outdoor location, natural available light. "
    "Desaturated muted color grade, overcast sky, prestige feature film aesthetic. "
    "Photorealistic — NOT CGI, NOT animation, NOT video game, NOT rendered. "
    "Real mud, real water, real weathered textures, organic film grain, anamorphic lens. "
    "Camera low and close behind the rider, maintaining identical framing to previous shot."
)

# (scene_id, duration, prompt)
SCENES = [
    (
        "s01",
        8,
        BASE + " "
        "Completely untouched wilderness, no structures, no human presence. "
        "Narrow winding river through ancient primordial plains, tall reeds and wild grass. "
        "Pre-dawn blue-grey mist lifting off the water. The earth completely unformed.",
    ),
    (
        "s02",
        8,
        BASE + " "
        "First faint signs of human presence — crude reed shelters barely visible on the far bank, "
        "a thin wisp of smoke rising. Narrow muddy river, flat ancient plains. "
        "The mud banks show faint traces of early settlement. Cool grey dawn.",
    ),
    (
        "s04",
        8,
        BASE + " "
        "Ancient mud-brick structures rise organically from the muddy riverbanks around the rider — "
        "low domed forms and crumbling arched walls made of the same mud as the earth itself, "
        "some half-dissolved into the shallow river, indistinguishable from the ground. "
        "Real weathered mud-brick, real erosion. Flat overcast light. Dust and silence.",
    ),
    (
        "s05",
        8,
        BASE + " "
        "Crumbling stone walls and overgrown cobbled paths on the muddy narrow riverbanks — "
        "a collapsed mill foundation dissolving back into the earth, terraced hillsides eroding. "
        "Real moss, real weathered stone returning to ground. Grey overcast sky. "
        "The rider and dog the only living things moving.",
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


def extract_last_frame(clip_path, frame_path):
    """Extract the last frame of a video clip."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", clip_path],
        capture_output=True, text=True
    )
    # Get last frame by seeking to near the end
    subprocess.run([
        "ffmpeg", "-sseof", "-0.1", "-i", clip_path,
        "-vframes", "1", "-q:v", "2", frame_path, "-y"
    ], capture_output=True)
    return os.path.exists(frame_path)


def upload_image(image_path):
    """Upload image to catbox.moe for temporary public hosting."""
    with open(image_path, "rb") as f:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            files={"fileToUpload": f},
            data={"reqtype": "fileupload"},
            timeout=30,
        )
    if resp.status_code == 200 and resp.text.startswith("https://"):
        return resp.text.strip()
    print(f"  [upload error] {resp.status_code} {resp.text[:100]}")
    return None


def submit_text(scene_id, duration, prompt):
    payload = {
        "model": MODEL,
        "promptText": prompt,
        "ratio": "1280:720",
        "duration": min(duration, 8),
    }
    resp = requests.post(f"{BASE_URL}/v1/text_to_video", headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        task_id = resp.json().get("id")
        print(f"  [text queued] {scene_id} -> {task_id}")
        return task_id
    print(f"  [ERROR] {scene_id}: {resp.status_code} {resp.text[:200]}")
    return None


def submit_image(scene_id, duration, prompt, image_url):
    payload = {
        "model": MODEL,
        "promptText": prompt,
        "promptImage": image_url,
        "ratio": "1280:720",
        "duration": min(duration, 8),
    }
    resp = requests.post(f"{BASE_URL}/v1/image_to_video", headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        task_id = resp.json().get("id")
        print(f"  [img queued]  {scene_id} -> {task_id}")
        return task_id
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
            return data.get("output", [None])[0]
        elif status in ("FAILED", "CANCELLED"):
            print(f"  [FAILED] {task_id}: {data}")
            return None
        print(f"  ... {status} {int(progress * 100)}%")
        time.sleep(15)
    print(f"  [TIMEOUT] {task_id}")
    return None


def download(url, path):
    r = requests.get(url, timeout=120)
    with open(path, "wb") as f:
        f.write(r.content)


def main():
    state = load_state()
    prev_clip = None  # Path to previous completed clip for chaining

    for i, (scene_id, duration, prompt) in enumerate(SCENES):
        out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")

        if os.path.exists(out_path):
            print(f"[skip] {scene_id} already done")
            prev_clip = out_path
            continue

        print(f"\n=== {scene_id} ({duration}s, chain={prev_clip is not None}) ===")

        task_id = state.get(scene_id, {}).get("task_id")

        if not task_id:
            if i == 0 or prev_clip is None:
                # First scene: text-to-video to establish the character
                task_id = submit_text(scene_id, duration, prompt)
            else:
                # Chain from last frame of previous clip
                frame_path = os.path.join(OUT_DIR, f"{scene_id}_seed.jpg")
                print(f"  extracting last frame from {os.path.basename(prev_clip)}...")
                if not extract_last_frame(prev_clip, frame_path):
                    print(f"  [frame extract failed] falling back to text-to-video")
                    task_id = submit_text(scene_id, duration, prompt)
                else:
                    print(f"  uploading seed frame...")
                    image_url = upload_image(frame_path)
                    if image_url:
                        print(f"  seed: {image_url}")
                        task_id = submit_image(scene_id, duration, prompt, image_url)
                    else:
                        print(f"  [upload failed] falling back to text-to-video")
                        task_id = submit_text(scene_id, duration, prompt)

            if not task_id:
                print(f"  [SKIP] {scene_id} - submission failed")
                continue

            state[scene_id] = {"task_id": task_id, "status": "RUNNING"}
            save_state(state)

        print(f"  polling {task_id}...")
        url = poll(task_id)

        if url:
            print(f"  [done] downloading...")
            download(url, out_path)
            state[scene_id]["status"] = "DONE"
            save_state(state)
            prev_clip = out_path
            print(f"  saved -> {out_path}")
        else:
            state[scene_id]["status"] = "FAILED"
            save_state(state)

    done = [s for s, _, _ in SCENES if os.path.exists(os.path.join(OUT_DIR, f"{s}.mp4"))]
    print(f"\nComplete: {len(done)}/{len(SCENES)} scenes")


if __name__ == "__main__":
    main()
