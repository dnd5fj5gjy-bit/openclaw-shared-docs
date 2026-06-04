#!/usr/bin/env python3
"""
Wildernests Frontier — image-chained video generation pipeline.
Generates home scenes (s08-s23) with image-to-video chaining for visual continuity.
Each clip uses the last frame of the previous clip as its visual seed.
"""
import requests, json, time, os, sys, subprocess

RUNWAY_KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE_URL = "https://api.dev.runwayml.com"
HEADERS = {
    "Authorization": f"Bearer {RUNWAY_KEY}",
    "X-Runway-Version": "2024-11-06",
    "Content-Type": "application/json"
}
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")
FRAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# Use fast model for throughput — quality comes from prompt engineering
MODEL = "veo3.1_fast"

# Roger Deakins-level cinematography prompt style
# Key: natural lighting, real materials, specific lens work, no CGI or synthetic look
STYLE = (
    "shot on ARRI Alexa Mini LF, 40mm Cooke S7i lens, f2.8, "
    "natural available light only, real outdoor location, "
    "photorealistic 4K, organic film grain, subtle lens distortion, "
    "Emmanuel Lubezki cinematography style, no CGI, no digital artifacts, "
    "no text, no watermarks, deep shadows with lifted blacks, "
    "high micro-contrast, real material textures — wood grain, rust, wet stone, dry grass"
)

# Home scenes — sequential chaining (s08 establishes the home, s09-s23 chain from previous)
# (scene_id, duration_sec, prompt, use_image_chain)
HOME_SCENES = [
    ("s08", 8, (
        "First dramatic wide aerial reveal of a remote modern off-grid architectural home — "
        "low-profile dark steel and glass structure nestled in a vast wild mountain valley. "
        "Camera approaching slowly from distance, home tiny against ancient landscape, "
        "golden hour dawn light, no roads no power lines no neighbours. " + STYLE
    ), False),  # text_to_video — establishes the home design

    ("s09", 6, (
        "Same off-grid home — close architectural detail of exterior at golden dawn. "
        "Integrated solar cladding panels on the roof catching first light. "
        "Low sun raking across the dark steel surface, dew glistening on glass. "
        "Camera low, tracking slowly across the structure. " + STYLE
    ), True),

    ("s10", 6, (
        "Same off-grid home — wide aerial shot at night, pitch-black wilderness. "
        "A single warm amber glow from within the home in the vast dark valley. "
        "No other lights in any direction for miles. Star field overhead. "
        "Camera floating slowly above, revealing the infinite darkness around it. " + STYLE
    ), True),

    ("s11", 6, (
        "Beautiful interior close shot — atmospheric water generation machine. "
        "Brushed metal cabinet, blue LED glow, water condensing on cool surfaces. "
        "Camera slowly pushing in, reverent and contemplative framing. "
        "Precision engineering, quiet hum of mechanism. " + STYLE
    ), True),

    ("s12", 6, (
        "Extreme close-up macro detail of atmospheric water generator in operation. "
        "Viewing port showing condensation collecting, tiny droplets flowing and merging. "
        "Shallow depth of field, rack focus from mechanism to water. "
        "Engineering precision, living machine. " + STYLE
    ), True),

    ("s13", 6, (
        "Interior of off-grid home — crystal clear water pouring from a brushed steel tap "
        "into a glass held by a weathered, strong male hand. "
        "Through the window behind: vast untouched mountain wilderness, soft golden bokeh. "
        "Warm interior light, slow motion, 120fps. " + STYLE
    ), True),

    ("s14", 6, (
        "Exterior of off-grid home — sky darkening rapidly, storm rolling in across the valley. "
        "Wind rising, bending the long mountain grass. "
        "Armoured steel shutters sliding automatically and silently into place across the windows. "
        "Ominous dark storm clouds building behind the structure. " + STYLE
    ), True),

    ("s15", 8, (
        "Same off-grid home — violent storm at full force. "
        "Rain sheeting horizontally against the sealed steel shutters. "
        "Lightning strike illuminating roiling dark clouds. "
        "The home completely solid and unmoved, a rock in the chaos. " + STYLE
    ), True),

    ("s16", 6, (
        "Wide valley aerial — wall of wildfire burning in the valley below. "
        "Massive orange inferno, towering smoke column rising into dark sky. "
        "Off-grid home visible on hillside in foreground, shutters closed, untouched. "
        "Fire will not reach it. Dramatic scale. " + STYLE
    ), True),

    ("s17", 6, (
        "Ground level tremor — cracked earth in the foreground, dust rising from the ground. "
        "Off-grid home on solid bedrock foundation behind, completely intact, standing firm. "
        "Camera shaking slightly with the tremor, handheld feel. " + STYLE
    ), True),

    ("s18", 6, (
        "Flash flood waters rushing through valley below. "
        "Off-grid home elevated on the hillside, completely untouched above the flood line. "
        "Dramatic aerial perspective, churning muddy water carving through the valley. "
        "The home safe, immovable, above it all. " + STYLE
    ), True),

    ("s19", 8, (
        "Off-grid home in remote wild valley at dusk. "
        "No road leading to it. No power line. No fence. No other structure visible. "
        "Camera slowly pulling back, revealing total wilderness in every direction. "
        "Golden dusk light fading to deep blue. Complete self-sufficiency. " + STYLE
    ), True),

    ("s20", 8, (
        "Time-lapse construction — skilled team assembling the off-grid home structure. "
        "Motion blur of rapid progress, three days condensed. "
        "Raw dark steel panels arriving, structure rising from bare earth. "
        "Beautiful craftsmanship, purposeful hands at work. " + STYLE
    ), True),

    ("s21", 10, (
        "Hero shot — architecturally stunning off-grid home perfectly framed "
        "in sweeping epic mountain landscape at golden hour. "
        "A single silhouetted figure stands outside looking at the vast mountains they chose as home. "
        "Camera wide, slow, aspirational. The widest and most beautiful shot of the film. " + STYLE
    ), True),

    ("s22", 8, (
        "Slow aerial retreat — camera pulling back and rising steadily. "
        "Off-grid home growing smaller as the vast untouched wilderness fills the frame. "
        "Mountain ranges appearing, scale of wilderness revealed in every direction. " + STYLE
    ), True),

    ("s23", 6, (
        "Extreme slow pullback aerial — the home now a tiny point of warm light "
        "in an infinite dark landscape. Stars emerging above. "
        "Pure wilderness, pure freedom. The smallest human light in an endless world. "
        "Final end frame, camera rising still. " + STYLE
    ), True),
]


def extract_last_frame(video_path, frame_path):
    cmd = [
        "ffmpeg", "-y",
        "-sseof", "-0.1",
        "-i", video_path,
        "-vframes", "1",
        "-update", "1",
        frame_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(frame_path)


def upload_image_catbox(image_path):
    """Upload image to catbox.moe for temporary public hosting."""
    with open(image_path, "rb") as f:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            files={"fileToUpload": f},
            data={"reqtype": "fileupload"},
            timeout=30
        )
    if resp.status_code == 200 and resp.text.startswith("https://"):
        return resp.text.strip()
    return None


def submit_text_to_video(scene_id, duration, prompt):
    payload = {
        "model": MODEL,
        "promptText": prompt,
        "ratio": "1280:720",
        "duration": min(duration, 8)
    }
    resp = requests.post(f"{BASE_URL}/v1/text_to_video",
                         headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        task_id = resp.json().get("id")
        print(f"  [queued text] {scene_id} -> {task_id}")
        return task_id
    else:
        print(f"  [err] {scene_id}: {resp.status_code} {resp.text[:200]}")
        return None


def submit_image_to_video(scene_id, duration, prompt, image_url):
    payload = {
        "model": MODEL,
        "promptText": prompt,
        "promptImage": image_url,
        "ratio": "1280:720",
        "duration": min(duration, 8)
    }
    resp = requests.post(f"{BASE_URL}/v1/image_to_video",
                         headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        task_id = resp.json().get("id")
        print(f"  [queued img]  {scene_id} -> {task_id}")
        return task_id
    else:
        print(f"  [err] {scene_id}: {resp.status_code} {resp.text[:300]}")
        return None


def poll_until_done(task_id, scene_id, timeout=1800):
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{BASE_URL}/v1/tasks/{task_id}",
                            headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            time.sleep(15)
            continue
        data = resp.json()
        status = data.get("status", "")
        progress = data.get("progress", 0)

        if status == "SUCCEEDED":
            return data
        elif status in ("FAILED", "CANCELLED"):
            print(f"  [fail] {scene_id}: {data.get('failure', 'unknown')}")
            return None
        else:
            elapsed = int(time.time() - start)
            print(f"  {scene_id}: {status} {progress:.0%} ({elapsed}s elapsed)")
            time.sleep(20)
    print(f"  [timeout] {scene_id}")
    return None


def download_clip(task_data, scene_id):
    out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")
    output = task_data.get("output", [])
    if not output:
        print(f"  [no output] {scene_id}")
        return None
    url = output[0] if isinstance(output, list) else output
    resp = requests.get(url, timeout=180, stream=True)
    if resp.status_code == 200:
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"  [saved] {scene_id} ({size_mb:.1f}MB) -> {out_path}")
        return out_path
    else:
        print(f"  [dl err] {scene_id}: {resp.status_code}")
        return None


def save_chain_state(state):
    path = os.path.join(OUT_DIR, "chain_state.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


def load_chain_state():
    path = os.path.join(OUT_DIR, "chain_state.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def main():
    print("=== WILDERNESTS FRONTIER — CHAINED VIDEO PIPELINE ===")
    print(f"Model: {MODEL} | Home scenes: {len(HOME_SCENES)}")
    print("Strategy: image-to-video chaining for visual continuity\n")

    chain_state = load_chain_state()
    prev_clip_path = None  # will track last completed clip

    for scene_id, duration, prompt, use_chain in HOME_SCENES:
        out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")

        # Already have this clip
        if os.path.exists(out_path):
            print(f"  [done] {scene_id} already exists")
            prev_clip_path = out_path
            continue

        print(f"\n--- {scene_id} ({duration}s, chain={use_chain}) ---")

        # Determine if we can chain from previous
        image_url = None
        if use_chain and prev_clip_path:
            frame_path = os.path.join(FRAMES_DIR, f"{scene_id}_seed.jpg")
            if extract_last_frame(prev_clip_path, frame_path):
                print(f"  [frame] Extracted last frame from {os.path.basename(prev_clip_path)}")
                image_url = upload_image_catbox(frame_path)
                if image_url:
                    print(f"  [upload] Seed frame: {image_url}")
                else:
                    print(f"  [warn] Upload failed, falling back to text_to_video")
            else:
                print(f"  [warn] Frame extract failed, falling back to text_to_video")

        # Submit the task
        task_id = None
        if image_url:
            task_id = submit_image_to_video(scene_id, duration, prompt, image_url)

        if not task_id:
            task_id = submit_text_to_video(scene_id, duration, prompt)

        if not task_id:
            print(f"  [SKIP] {scene_id} - submission failed")
            continue

        chain_state[scene_id] = {"task_id": task_id, "status": "RUNNING", "chained": bool(image_url)}
        save_chain_state(chain_state)

        # Wait for this clip to complete before proceeding to the next (chaining requirement)
        print(f"  Waiting for {scene_id}...")
        task_data = poll_until_done(task_id, scene_id)

        if task_data:
            path = download_clip(task_data, scene_id)
            if path:
                prev_clip_path = path
                chain_state[scene_id]["status"] = "DONE"
                save_chain_state(chain_state)
                print(f"  [complete] {scene_id} ready for chaining")
            else:
                print(f"  [err] Download failed for {scene_id}")
        else:
            print(f"  [err] {scene_id} generation failed")

        # Brief pause between submissions
        time.sleep(3)

    # Summary
    print("\n=== CHAINING PIPELINE COMPLETE ===")
    completed = [f for f in os.listdir(OUT_DIR) if f.endswith('.mp4')]
    print(f"Total clips: {len(completed)}")
    for f in sorted(completed):
        path = os.path.join(OUT_DIR, f)
        size_mb = os.path.getsize(path) / 1024 / 1024
        print(f"  {f} ({size_mb:.1f}MB)")


if __name__ == "__main__":
    main()
