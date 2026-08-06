#!/usr/bin/env python3
"""Everest Power imagery via Runway gemini_image3_pro (Nano Banana Pro).
Usage: python3 gen.py <job1> <job2> ...   (no args = all)
"""
import urllib.request, urllib.error, json, time, subprocess, sys, os
import concurrent.futures as cf

KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE = "https://api.dev.runwayml.com"
H = {"Authorization": f"Bearer {KEY}", "X-Runway-Version": "2024-11-06",
     "Content-Type": "application/json"}
OUT = os.path.dirname(os.path.abspath(__file__))


def api(m, ep, b=None):
    data = json.dumps(b).encode() if b else None
    req = urllib.request.Request(BASE + ep, data=data, headers=H, method=m)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


# Runway ratios are model-specific. 1080:1920 portrait, 1920:1080 landscape.
JOBS = {
# ---------------------------------------------------------------- THE PACK
"pack-hero": ("1080:1920",
 "Photorealistic product packaging mockup. A vertical single-serve foil drink sachet "
 "standing upright, flat pouch with serrated zigzag tear edges top and bottom, soft foil "
 "sheen, gentle studio shadow, plain pale grey background. "
 "DESIGN ON THE PACK: deep midnight blue to black vertical gradient, one burnt orange accent. "
 "A cold blue world with a single warm element. Very high contrast, bold and simple, readable "
 "from two metres. Upper area shows a snow-lit Himalayan summit pyramid with a wind plume off "
 "the ridge against a deep cobalt sky, and small Tibetan prayer flags strung across one corner. "
 "TYPOGRAPHY centred: a small white line at top reading BEAR GRYLLS in condensed capitals with "
 "wide letter spacing; below it very large heavy condensed capitals reading EVEREST on one line "
 "and POWER on the next, EVEREST in white, POWER in burnt orange, subtle rough texture. "
 "Below that a slim orange band. Lower left a short vertical list of five small white bullet "
 "items. Lower right a bright cut lemon with a citrus and water splash, the one saturated warm "
 "moment. Across the very bottom a clean solid white-on-dark information strip containing the "
 "text 12 g at the left, a small green dot inside a green square outline, a small circular logo, "
 "and the words MADE IN INDIA at the right. Crisp commercial packaging photography, sharp focus, "
 "clean accurate lettering, no clutter."),

# ---------------------------------------------------------------- DECK ART
"deck-street": ("1920:1080",
 "Documentary photograph, early morning golden light in a small Indian market town. A row of "
 "tiny open-fronted shops and a roadside stall, hanging vertical strips of colourful single-serve "
 "sachets swinging in the doorway, steel counter, glass jars, a scooter parked at the kerb, dusty "
 "street, hand-painted Hindi signage on the walls. Warm dust in the air, long shadows, lived-in "
 "and real. Shot on a 35mm lens, natural light, rich colour, shallow depth of field. No text "
 "overlay."),

"deck-everest": ("1920:1080",
 "Photograph of the Everest massif at first light, the summit pyramid catching gold while the "
 "valley below stays in cold blue shadow, a long plume of spindrift streaming off the ridge line, "
 "deep clear high-altitude sky, layers of dark foreground ridges receding into haze. Vast, still "
 "and cold. Large format landscape photography, extremely sharp, natural colour."),

"deck-vendor": ("1920:1080",
 "Documentary portrait photograph. An Indian cycle rickshaw rider in his forties resting in the "
 "shade at the side of a hot city street in the afternoon, sweat on his face and forearms, "
 "drinking from a steel tumbler, eyes closed for a second. Heat haze, saturated street colour "
 "behind him thrown out of focus. Honest, warm, dignified, not staged. 50mm lens, natural light."),

"deck-himalaya-trail": ("1920:1080",
 "Photograph of a lone trekker with a heavy pack on a high Himalayan trail in Ladakh, small in "
 "the frame against enormous ochre and grey mountain walls, a thin ribbon of trail, prayer flags "
 "on a cairn in the foreground, brilliant thin blue sky. Scale and solitude. Landscape "
 "photography, sharp, natural colour, no text."),
}


def go(name):
    ratio, prompt = JOBS[name]
    body = {"model": "gemini_image3_pro", "promptText": prompt[:995], "ratio": ratio}
    st, d = api("POST", "/v1/text_to_image", body)
    if st not in (200, 201):
        print(f"ERR  {name}  {st}  {json.dumps(d)[:220]}", flush=True)
        return
    tid = d["id"]
    print(f"queued {name}", flush=True)
    t0 = time.time()
    while time.time() - t0 < 420:
        st, d = api("GET", f"/v1/tasks/{tid}")
        s = d.get("status")
        if s == "SUCCEEDED":
            dest = os.path.join(OUT, f"{name}.png")
            subprocess.run(["curl", "-s", "-o", dest, d["output"][0]], check=True)
            print(f"OK   {name} -> {dest}", flush=True)
            return
        if s in ("FAILED", "CANCELLED"):
            print(f"FAIL {name} {json.dumps(d)[:220]}", flush=True)
            return
        time.sleep(6)
    print(f"TIMEOUT {name}", flush=True)


if __name__ == "__main__":
    names = sys.argv[1:] or list(JOBS)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(go, names))
    print("DONE", flush=True)
