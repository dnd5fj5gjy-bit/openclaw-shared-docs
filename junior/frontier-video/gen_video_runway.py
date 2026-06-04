#!/usr/bin/env python3
"""
Generate all Wildernests Frontier video clips via Runway Veo3.
Queues all tasks, then polls until done and downloads.
"""
import requests, json, time, os, sys

RUNWAY_KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE_URL = "https://api.dev.runwayml.com"
HEADERS = {
    "Authorization": f"Bearer {RUNWAY_KEY}",
    "X-Runway-Version": "2024-11-06",
    "Content-Type": "application/json"
}
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")
os.makedirs(OUT_DIR, exist_ok=True)

# Scene definitions: (id, duration_s, prompt)
# Photorealistic, cinematic, no text, anamorphic lens style
STYLE = "cinematic photorealistic 4k, anamorphic lens, film grain, no text, no watermarks, ultra detailed"

SCENES = [
    ("s01", 8,  f"Aerial drone shot at pre-dawn over vast untouched American wilderness. Lone horseman barely visible in tall golden grass far below, moving slowly through the landscape. Indigo pre-dawn sky with first amber light breaking on distant mountain horizon. {STYLE}"),
    ("s02", 8,  f"Low tracking shot following a lone rider on horseback through tall prairie grass, camera skimming the earth, grass blurring in foreground. Cold early morning light, golden rolling grasslands, wild open frontier landscape stretching to distant hills. {STYLE}"),
    ("s04", 8,  f"Ancient Mesopotamia 5000 BC. Eye-level perspective among early farmers at the fertile banks of the Euphrates. Dark rich earth, reed structures in distance, workers planting in the fields, warm golden ancient light, hazy sky, date palms. {STYLE}"),
    ("s05", 8,  f"Medieval hilltop stone settlement on a rolling hillside. Practical stone walls, terraced agricultural fields cascading below, trade roads converging from multiple directions, smoke from hearths, horses in the distance, overcast European sky. {STYLE}"),
    ("s06", 8,  f"Cold industrial modern landscape. Row of massive electricity pylons stretching across grey flat terrain into the distance. Motorway interchange below, water treatment towers, all grey and dehumanizing scale, flat winter light, mist. {STYLE}"),
    ("s07", 8,  f"Dense urban compression at night. High-rise tower blocks crowding the sky, neon light reflections on wet tarmac below, crowds blurred in motion, traffic light trails, overwhelming claustrophobic modern city. {STYLE}"),
    ("s07b", 4, f"Single black frame, pitch darkness, complete emptiness. Very faint distant horizon light. Absolute silence represented visually."),
    ("s08", 8,  f"First dramatic reveal of a stunning modern off-grid architectural home in a vast remote mountain valley. Wide aerial approach shot, the structure small and perfect against ancient landscape, golden hour dawn light, no roads no power lines visible. {STYLE}"),
    ("s09", 6,  f"Close architectural detail of the off-grid home exterior at golden dawn. Low sun raking dramatically across integrated solar cladding panels. Warm amber light spreading across the structure surface, dew glistening. {STYLE}"),
    ("s10", 6,  f"Wide aerial shot at night. A single modern home glowing warm amber from within in a vast ocean of pitch-black wilderness. No roads, no other lights, no neighbours for miles in any direction. Star field above. {STYLE}"),
    ("s11", 6,  f"Beautiful interior shot of an atmospheric water generation machine. Treated with architectural reverence almost like sculpture. Brushed metal, blue LED glow, water condensing on surfaces, precision engineering. {STYLE}"),
    ("s12", 6,  f"Extreme close-up detail of the atmospheric water generator in operation. Viewing port showing condensation collecting and flowing, intricate mechanism, engineering precision, macro photography style. {STYLE}"),
    ("s13", 6,  f"Crystal clear water pouring from a tap into a glass held by a weathered strong hand. Through the window behind: vast untouched wilderness in soft golden focus. Warm interior light, slow motion quality. {STYLE}"),
    ("s14", 6,  f"Exterior of the off-grid home. Sky darkening rapidly, storm approaching, wind rising and bending grass. Armoured steel shutters sliding silently and automatically into place across the windows. Ominous dark sky. {STYLE}"),
    ("s15", 8,  f"Violent storm at full force. Rain sheeting horizontally against the sealed steel shutters of the home. Lightning strikes illuminating dark clouds behind. The home completely unmoved and solid. {STYLE}"),
    ("s16", 6,  f"Wall of wildfire burning in a valley below. Massive orange inferno, towering smoke column rising. The off-grid home in the foreground on the hillside, shutters closed, completely protected, fire will not reach it. {STYLE}"),
    ("s17", 6,  f"Ground earthquake tremor. Cracked earth in the foreground, dust clouds rising from the ground. The off-grid home on solid bedrock foundation, completely intact and standing firm, undamaged. {STYLE}"),
    ("s18", 6,  f"Flash flood waters rushing through a valley below. The off-grid home elevated on the hillside completely untouched above the flood. Dramatic aerial perspective, churning muddy water through the valley. {STYLE}"),
    ("s19", 8,  f"The off-grid home in a remote wild valley at dusk. No road leading to it. No power line. No fence. No other structure visible in any direction. Complete wilderness self-sufficiency. Golden dusk light. {STYLE}"),
    ("s20", 8,  f"Time-lapse construction sequence. Skilled team of workers assembling the off-grid home structure, motion blur suggesting rapid progress. Three days of building condensed. Raw materials arriving, structure rising. {STYLE}"),
    ("s21", 10, f"Hero shot at golden hour. The architecturally stunning off-grid home perfectly framed in a sweeping epic mountain landscape. A single figure stands outside looking at the mountains they chose as home. Wide, vast, aspirational. {STYLE}"),
    ("s22", 8,  f"Slow aerial retreat. Camera pulling back and rising, the off-grid home growing smaller and smaller as the vast untouched wilderness expands to fill the frame in every direction. Final scale reveal. {STYLE}"),
    ("s23", 6,  f"Extreme slow pullback aerial shot, the home now a tiny point of light in an infinite dark landscape, stars appearing above, pure wilderness, pure freedom. End frame. {STYLE}"),
]

def submit_task(scene_id, duration, prompt):
    payload = {
        "model": "veo3.1_fast",
        "promptText": prompt,
        "ratio": "1280:720",
        "duration": min(duration, 8)
    }
    resp = requests.post(f"{BASE_URL}/v1/text_to_video",
                         headers=HEADERS, json=payload, timeout=30)
    if resp.status_code in (200, 201):
        data = resp.json()
        task_id = data.get("id")
        print(f"  [queued] {scene_id} -> task {task_id}")
        return task_id
    else:
        print(f"  [err]   {scene_id}: {resp.status_code} {resp.text[:200]}")
        return None

def poll_task(task_id, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{BASE_URL}/v1/tasks/{task_id}",
                            headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            time.sleep(10)
            continue
        data = resp.json()
        status = data.get("status", "")
        progress = data.get("progress", 0)
        if status == "SUCCEEDED":
            return data
        elif status in ("FAILED", "CANCELLED"):
            print(f"  [fail] Task {task_id}: {data.get('failure','')}")
            return None
        else:
            print(f"  [poll] {task_id[:8]}... {status} {progress:.0%}")
            time.sleep(15)
    print(f"  [timeout] {task_id}")
    return None

def download_clip(task_data, scene_id):
    out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")
    if os.path.exists(out_path):
        return out_path
    output = task_data.get("output", [])
    if not output:
        print(f"  [no output] {scene_id}")
        return None
    url = output[0] if isinstance(output, list) else output
    resp = requests.get(url, timeout=120, stream=True)
    if resp.status_code == 200:
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"  [saved] {scene_id} ({size_mb:.1f}MB)")
        return out_path
    else:
        print(f"  [dl err] {scene_id}: {resp.status_code}")
        return None

def save_state(tasks):
    with open(os.path.join(OUT_DIR, "task_state.json"), "w") as f:
        json.dump(tasks, f, indent=2)

def load_state():
    path = os.path.join(OUT_DIR, "task_state.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def main():
    print("=== WILDERNESTS FRONTIER — VIDEO GENERATION ===")
    print(f"Model: veo3.1_fast | Scenes: {len(SCENES)}")

    # Load existing task state
    task_state = load_state()

    # Submit new tasks for scenes not yet submitted
    print("\n--- Submitting tasks ---")
    for scene_id, duration, prompt in SCENES:
        out_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")
        if os.path.exists(out_path):
            print(f"  [done]   {scene_id} already downloaded")
            continue
        if scene_id in task_state and task_state[scene_id].get("task_id"):
            print(f"  [exists] {scene_id} -> {task_state[scene_id]['task_id'][:8]}...")
            continue
        task_id = submit_task(scene_id, duration, prompt)
        if task_id:
            task_state[scene_id] = {"task_id": task_id, "status": "RUNNING"}
        save_state(task_state)
        time.sleep(2)  # Rate limiting

    # Poll all pending tasks until done
    print("\n--- Polling tasks ---")
    pending = {sid: info for sid, info in task_state.items()
               if not os.path.exists(os.path.join(OUT_DIR, f"{sid}.mp4"))
               and info.get("task_id")}

    while pending:
        completed = []
        for scene_id, info in list(pending.items()):
            task_id = info["task_id"]
            resp = requests.get(f"{BASE_URL}/v1/tasks/{task_id}",
                                headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            status = data.get("status", "")
            progress = data.get("progress", 0)

            if status == "SUCCEEDED":
                path = download_clip(data, scene_id)
                if path:
                    completed.append(scene_id)
                    del pending[scene_id]
            elif status in ("FAILED", "CANCELLED"):
                print(f"  [fail] {scene_id}: {data.get('failure','unknown')}")
                del pending[scene_id]
            else:
                print(f"  {scene_id}: {status} {progress:.0%}")

        if pending:
            print(f"  Waiting... {len(pending)} clips still processing")
            time.sleep(20)

    print(f"\nDone. Clips in: {OUT_DIR}")
    completed_clips = [f for f in os.listdir(OUT_DIR) if f.endswith('.mp4')]
    print(f"Total clips downloaded: {len(completed_clips)}")

if __name__ == "__main__":
    main()
