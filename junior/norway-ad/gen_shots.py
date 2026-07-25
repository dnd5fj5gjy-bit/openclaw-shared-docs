#!/usr/bin/env python3
"""Queue the Norway ad shots on Runway. Rough cut for the OpenAI pitch.

Creative rule being applied: BEAR'S FACE IS NEVER GENERATED. Every shot below is framed so that
identity is not the point - from behind, wide, or on the water. A text-to-video model asked for
"Bear Grylls" returns a Bear-ish stranger, and the room this is being shown to would spot it
instantly. The one shot of his real face comes from real footage, held separately.

The ad's job is to show the model REASONING against a constraint, not to list activities. The
activities are the payoff; the weather window is the product.
"""
import json, os, time
import requests

KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE = "https://api.dev.runwayml.com"
H = {"Authorization": f"Bearer {KEY}", "X-Runway-Version": "2024-11-06", "Content-Type": "application/json"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")
os.makedirs(OUT, exist_ok=True)

STYLE = ("cinematic photorealistic, anamorphic lens, natural light, film grain, "
         "no text, no watermarks, no on-screen graphics, ultra detailed")

SHOTS = [
    ("s1_ferry", 8,
     "A man in a weathered outdoor jacket and beanie steps off a small passenger ferry onto a wooden "
     "dock in a Norwegian fjord village. Filmed from BEHIND and slightly to the side, his face not "
     "visible to camera. He raises a phone to his ear as he walks. Cold clear morning light, steep "
     "green mountains rising straight out of deep dark water, painted timber houses along the shore. "
     f"Handheld documentary feel. {STYLE}"),
    ("s2_kayak", 8,
     "Aerial drone shot descending toward a single sea kayak cutting a clean line across a perfectly "
     "glassy Norwegian fjord at first light. Mirror-still black water, sheer thousand-metre rock walls "
     f"on both sides, thin mist on the surface, tiny paddler for scale. {STYLE}"),
    ("s3_base", 8,
     "A BASE jumper in a wingsuit steps off a sheer cliff edge high above a Norwegian fjord and falls "
     "away from camera into the void. Filmed from behind and above at the moment of the step. Vast "
     f"drop to dark water far below, cloud shadow moving across the rock face. {STYLE}"),
    ("s4_sail", 8,
     "A small sailing yacht heeled over under full sail moving down a Norwegian fjord in low golden "
     "evening light. Filmed wide from the water, crew visible only as small silhouettes. Wind texture "
     f"on the water, mountains going blue with dusk behind. {STYLE}"),
    ("s5_bike", 8,
     "A mountain biker riding fast along a narrow gravel ridge trail high above a Norwegian fjord, "
     "filmed from behind and slightly above, rider silhouetted, dust kicking off the back wheel. "
     f"Late afternoon light, huge landscape falling away on both sides. {STYLE}"),
]


def queue(sid, dur, prompt):
    r = requests.post(f"{BASE}/v1/text_to_video", headers=H, timeout=30, json={
        "model": "veo3.1_fast", "promptText": prompt, "ratio": "1280:720", "duration": min(dur, 8)})
    if r.status_code in (200, 201):
        tid = r.json().get("id")
        print(f"  queued {sid} -> {tid}")
        return tid
    print(f"  ERROR {sid}: {r.status_code} {r.text[:200]}")
    return None


if __name__ == "__main__":
    tasks = {}
    for sid, dur, prompt in SHOTS:
        tid = queue(sid, dur, prompt)
        if tid:
            tasks[sid] = tid
        time.sleep(1)
    # checkpoint to disk immediately: if this process dies, the render is still running and paid for
    with open(os.path.join(OUT, "tasks.json"), "w") as f:
        json.dump(tasks, f, indent=2)
    print(f"\n{len(tasks)}/{len(SHOTS)} queued, ids written to clips/tasks.json")
