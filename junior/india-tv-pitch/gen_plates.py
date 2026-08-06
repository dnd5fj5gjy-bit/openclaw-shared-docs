#!/usr/bin/env python3
"""Generate the location plates for the India TV pitch. Runway gemini_image3_pro (Nano Banana Pro)."""
import urllib.request, urllib.error, json, time, subprocess, sys, os
import concurrent.futures as cf

KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE = "https://api.dev.runwayml.com"
H = {"Authorization": f"Bearer {KEY}", "X-Runway-Version": "2024-11-06", "Content-Type": "application/json"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

# House look, appended to every prompt. Keeps the deck reading as one film.
LOOK = ("Cinematic documentary film still, anamorphic widescreen, shot on 35mm, natural available light, "
        "muted desaturated earth palette, deep shadows, fine film grain, no text, no logos, no watermark, "
        "no captions, no on-screen graphics.")

TINY = ("A single human figure, extremely small in the frame, seen from behind or in silhouette, face never "
        "visible or identifiable. ")

PLATES = {
  # --- openers and structural plates ---
  "cover": "A vast 6000-metre Himalayan snow summit ridge in Ladakh at first light. Deep blue pre-dawn shadow "
           "filling the valleys, only the highest snow catching cold orange sun. " + TINY +
           "standing on the ridgeline, dwarfed. Endless brown and white Zanskar ranges receding to the horizon. Very wide shot.",

  "vacancy": "An empty rocky summit cairn at dawn above a sea of cloud in the Indian Himalaya. Nobody there. "
             "Cold blue light, one shaft of low sun. Utterly still and unoccupied. Wide shot.",

  "why_now": "Rural northern India at dusk. Interior of a simple concrete house lit only by the screen of a "
             "large television, family silhouettes watching from behind, faces not visible. Warm screen glow "
             "against blue evening light through an open doorway. Quiet, ordinary, intimate.",

  "languages": "A dense Indian city street at night from above, shop signs and hoardings blurred into pure colour "
               "and light with no readable lettering, motorcycle headlights streaking. Long exposure, abstract, "
               "layered, many overlapping lights. No legible text anywhere.",

  # --- the nine legs ---
  "leg_kanyakumari": "The southernmost rock of India at Kanyakumari before sunrise. Black wet granite outcrops in a "
                     "dark ocean where three seas meet, long swell, pink and grey sky. " + TINY +
                     "swimming toward the rocks. Very wide.",

  "leg_ghats": "Deep monsoon jungle gorge in the Western Ghats. A high waterfall falling through thick green canopy "
               "into a black plunge pool, mist and spray, wet basalt walls. " + TINY +
               "abseiling on a thin rope beside the falling water, tiny against the wall.",

  "leg_badami": "Red and ochre sandstone cliffs at Badami, Karnataka, in hard late afternoon light. Steep overhanging "
                "rock, deep horizontal strata, an ancient stepped tank of green water below. " + TINY +
                "sport climbing high on the overhang.",

  "leg_hampi": "The granite boulder field of Hampi at golden hour. Enormous rounded orange boulders stacked to the "
               "horizon, ruined stone temple colonnades among them, palms. A single highline webbing strung between "
               "two boulder summits with " + TINY + "balanced halfway across, minute in the frame.",

  "leg_konkan": "Konkan Kada, the great curved vertical wall of the Sahyadri escarpment, Maharashtra, at dawn. A huge "
                "concave amphitheatre of black basalt dropping sheer into cloud filling the valley below. " + TINY +
                "standing right on the lip of the exit point. Vertiginous wide shot.",

  "leg_bir": "Paragliding above Bir Billing, Himachal Pradesh. One paraglider wing high over green terraced foothills "
             "with the snow line of the Dhauladhar range behind, layers of blue ridges, late morning haze. The wing "
             "small in a very large sky.",

  "leg_miyar": "Untouched big-wall alpine granite in the Miyar Valley, Himachal. Clean grey granite towers rising "
               "straight out of a green glacial meadow with a braided river, snow peaks behind, no sign of humans "
               "anywhere. Cold clear morning light. Very wide.",

  "leg_zanskar": "The Zanskar gorge in Ladakh. Two riders on horseback, extremely small, seen from far above and behind, "
                 "crossing a bare high-altitude desert plateau of ochre and violet rock above a turquoise river far "
                 "below. Enormous scale, thin air, hard shadow.",

  "leg_ladakh": "A steep snow and ice summit slope at 6000 metres in Ladakh in the last hour before the top. " + TINY +
                "climbing a bootpack up the ridge, rope trailing, brown Himalayan desert ranges laid out far below "
                "through thin cloud. Bitter cold blue-white light.",

  # --- payload plates ---
  "finale": "A paraglider wing launching off a snow summit at 6000 metres in the Ladakh Himalaya, wing just loading, "
            "pilot tiny and unidentifiable, a two-thousand-metre drop of brown desert valley opening beneath. Cold "
            "clear high-altitude light, curvature of enormous ranges to the horizon. The single most dramatic frame.",

  "closing": "Sunrise over the sea at Kanyakumari where three seas meet, seen from the shore rocks. Low sun cutting a "
             "path across dark water, fishing boats as small silhouettes, warm light on wet black rock. Calm, epic, wide.",
}

def api(m, ep, b=None):
    data = json.dumps(b).encode() if b else None
    req = urllib.request.Request(BASE + ep, data=data, headers=H, method=m)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def go(item):
    name, body_prompt = item
    dest = os.path.join(OUT, name + ".png")
    if os.path.exists(dest) and os.path.getsize(dest) > 40000:
        print("SKIP", name, flush=True)
        return name, True
    prompt = (body_prompt + " " + LOOK)[:995]
    st, d = api("POST", "/v1/text_to_image",
                {"model": "gemini_image3_pro", "promptText": prompt, "ratio": "1344:768"})
    if st not in (200, 201):
        print("ERR", name, st, json.dumps(d)[:200], flush=True)
        return name, False
    tid = d["id"]
    for _ in range(100):
        time.sleep(6)
        st, d = api("GET", f"/v1/tasks/{tid}")
        s = d.get("status")
        if s == "SUCCEEDED":
            subprocess.run(["curl", "-s", "-o", dest, d["output"][0]], check=True)
            print("OK", name, flush=True)
            return name, True
        if s in ("FAILED", "CANCELLED"):
            print("FAIL", name, json.dumps(d)[:200], flush=True)
            return name, False
    print("TIMEOUT", name, flush=True)
    return name, False

if __name__ == "__main__":
    want = sys.argv[1:] or list(PLATES)
    items = [(k, PLATES[k]) for k in want if k in PLATES]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(go, items))
    bad = [n for n, ok in res if not ok]
    print("DONE. failed:", bad if bad else "none", flush=True)
