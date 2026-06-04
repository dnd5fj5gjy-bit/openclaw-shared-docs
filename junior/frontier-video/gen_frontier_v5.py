#!/usr/bin/env python3
"""
Frontier Video — v5.
Key fix: civilization scenes now describe emergence from mud + dissolution back.
Structures rise organically from the riverbank mud and dissolve back — not hard-cut appearances.
Full scene set (s01-s22). Image-to-video chaining for character continuity.
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
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips_v5")
STATE_FILE = os.path.join(OUT_DIR, "state.json")

os.makedirs(OUT_DIR, exist_ok=True)

# Core visual lock (kept tight — API limit 1000 chars per prompt)
BASE = (
    "Cinematic 16:9. Tracking shot from directly behind lone rider on horseback. "
    "Dark frontier duster coat, wide-brim hat, face never shown. "
    "Black and white border collie trots alongside right of horse. "
    "Narrow muddy winding river. Rider moves slowly forward. "
    "35mm film, Kodak Vision3, desaturated muted grade, overcast sky. "
    "Photorealistic — NOT CGI, NOT animation, NOT video game. "
    "Film grain, anamorphic lens. Low close behind-rider framing throughout. "
    "No text, no watermarks."
)

# (scene_id, duration, prompt)
# Key: civilization scenes describe emergence FROM mud and dissolution BACK TO mud — not static presence
SCENES = [
    # === HISTORY OF CIVILIZATION — rise from mud, disappear back ===
    (
        "s01",
        8,
        BASE + " "
        "Completely untouched ancient wilderness. Zero human presence, zero structures. "
        "Narrow river through primordial plains. Tall reeds and wild grass on raw muddy banks. "
        "Pre-dawn blue-grey mist on water. Earth unformed and empty.",
    ),
    (
        "s02",
        10,
        BASE + " "
        "The muddy far bank slowly cohering — crude shapes rising from the earth itself, "
        "reed and stick shelters emerging as if grown from the mud rather than built. "
        "Barely distinguishable from the riverbank. A thin wisp of smoke rising. "
        "At the far edge of frame the shapes already dissolve back. "
        "Cool grey dawn. Early Stone Age. Earth and shelter almost the same thing.",
    ),
    (
        "s04",
        8,
        BASE + " "
        "Mud-brick domes and low arched walls slowly cohering from the muddy riverbanks — "
        "the same colour and texture as the earth they rise from. "
        "As if the land itself is remembering the shape of cities. "
        "Some structures still half-dissolved into the shallow river. "
        "Some already crumbling back to silt. Dust and flat overcast light.",
    ),
    (
        "s05",
        8,
        BASE + " "
        "Stone walls and field terraces stepping up from the muddy river valley — "
        "rising from the earth like they grew there, already weathering, returning. "
        "Collapsed mill on far bank dissolving into the mud. "
        "Cobbled path overgrown and softening back to earth. "
        "Green hills, grey sky. A world that rose and is sinking.",
    ),
    (
        "s06",
        14,
        BASE + " "
        "Iron telegraph poles and factory chimney stacks rising from the far bank — "
        "industrial age, raw and angular. A low iron bridge over the river. "
        "Pipes and wires strung across the landscape. Smoke and grey overcast sky. "
        "But at the edges everything softens — the structures already streaked with rust, "
        "beginning their long slow return to mud.",
    ),
    (
        "s07",
        12,
        BASE + " "
        "Concrete apartment blocks and roads visible in the far distance — "
        "modern city rising from the flood plain, grey and dense. "
        "The rider small against it. The river hemmed and channelled. "
        "Everything built by necessity. The land no longer visible beneath.",
    ),

    # === THE RENEGADES — pivot away, back into the wild ===
    (
        "s08",
        10,
        BASE + " "
        "The city dissolves behind them. The rider and dog move forward "
        "into open wilderness — no structures, no roads, no wires. "
        "The river narrows again, the banks return to mud and reeds. "
        "Wide open sky. Mountains ahead. The land empty and waiting.",
    ),
    (
        "s09",
        6,
        BASE + " "
        "A Wildernests structure visible ahead on high ground above the river — "
        "clean geometric form against the landscape. Solar panels catching flat sky. "
        "The rider approaches slowly. No roads to it, no power lines. "
        "Just the structure, the land, and the river.",
    ),
    (
        "s10",
        6,
        BASE + " "
        "Closer now — the Wildernests structure on the rise above the muddy bank. "
        "Atmospheric water generator catching mist from the river valley below. "
        "Condensation on cool surfaces. Water drawn from air. "
        "The rider pauses. Overcast sky. River mist. Silence.",
    ),
    (
        "s11",
        6,
        BASE + " "
        "River mist rising from the valley. The air itself thick with moisture. "
        "The Wildernests structure sits above the mist line — dry, solid, self-contained. "
        "Water drawn from the air around it. No pipes. No reservoir. "
        "Rider and dog moving through the mist below.",
    ),
    (
        "s12",
        6,
        BASE + " "
        "Close on the Wildernests structure from behind rider. "
        "Atmospheric water generator on the roof catching the valley mist — "
        "clean water condensing on cool metal. No external infrastructure. "
        "Just the machine, the air, and the water it pulls from nothing.",
    ),
    (
        "s13",
        6,
        BASE + " "
        "The rider and dog arrive at the Wildernests structure. "
        "High on a ridge above the river valley. No roads. No grid. "
        "Solar panels angled to the sky. The river far below. "
        "A complete, sovereign place. The rider looks out.",
    ),

    # === AND WE WILL HOLD — resilience ===
    (
        "s15",
        8,
        BASE + " "
        "Wind howling across an open ridge. The Wildernests structure holds firm — "
        "walls unmoving while reeds and grass flatten around it. "
        "The rider and dog in the foreground, facing into the wind. "
        "Dramatic overcast sky. Clouds moving fast.",
    ),
    (
        "s16",
        6,
        BASE + " "
        "Fire burning on the far hillside — slow and orange in the grey light. "
        "The Wildernests structure on a cleared rise, intact, firebreak around it. "
        "Smoke drifting. The rider watches from a distance. "
        "Structure holds. Land burns. Structure holds.",
    ),
    (
        "s17",
        6,
        BASE + " "
        "The ground fractured and disturbed — deep cracks in the earth, "
        "tilted landscape after seismic movement. "
        "The Wildernests structure intact on its platform, undamaged. "
        "Rider and dog picking their way through broken terrain below. "
        "Overcast sky. Silence.",
    ),
    (
        "s18",
        6,
        BASE + " "
        "The river risen and flooding the valley floor — brown water spreading wide. "
        "The Wildernests structure elevated above the flood line, dry and intact. "
        "The rider and dog on high ground watching the water. "
        "Everything low is submerged. The structure stands.",
    ),
    (
        "s19",
        8,
        BASE + " "
        "Vast open wilderness. No roads, no wires, no other structures visible. "
        "The rider and dog moving forward across the empty landscape. "
        "The Wildernests structure behind them on a distant ridge — "
        "a sovereign point in a sovereign land. The only mark on the horizon.",
    ),
    (
        "s20",
        8,
        BASE + " "
        "A flat open site — any land, any terrain. "
        "A Wildernests structure being raised: walls and roof assembling, "
        "a modular form coming together in open air. "
        "The rider and dog watching from nearby. Three days. Any ground.",
    ),

    # === HERO SHOT ===
    (
        "s21",
        10,
        BASE + " "
        "The rider and dog cresting a high ridge. "
        "The Wildernests structure behind them — perfectly placed, perfectly self-sufficient. "
        "The river visible far below, winding through open country. "
        "No city, no grid, no road. Just the land, the structure, and the rider. "
        "Wide open sky. This is where they chose to stand.",
    ),
    (
        "s22",
        8,
        BASE + " "
        "The rider and dog silhouetted on the ridge. "
        "Wildernests structure behind. The river valley below. "
        "The landscape vast and still. Camera holds behind them. "
        "The rider does not move. The dog sits. "
        "Just the horizon and the choice they made.",
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
    subprocess.run([
        "ffmpeg", "-sseof", "-0.1", "-i", clip_path,
        "-vframes", "1", "-q:v", "2", frame_path, "-y"
    ], capture_output=True)
    return os.path.exists(frame_path)


def upload_image(image_path):
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
    prev_clip = None

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
                task_id = submit_text(scene_id, duration, prompt)
            else:
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
