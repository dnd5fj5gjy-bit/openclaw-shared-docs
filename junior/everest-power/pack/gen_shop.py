#!/usr/bin/env python3
"""Everest Power in-shop imagery. Uses the actual concept sachet as a reference
image so the pack in the shop is OUR pack, not a generic sachet.

Usage: python3 gen_shop.py [job ...]
"""
import urllib.request, urllib.error, json, time, subprocess, sys, os, base64
import concurrent.futures as cf

KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE = "https://api.dev.runwayml.com"
H = {"Authorization": f"Bearer {KEY}", "X-Runway-Version": "2024-11-06",
     "Content-Type": "application/json"}
OUT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(OUT, "concepts", "c1-blue-nimbu-namak.jpg")


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def api(m, ep, b=None):
    data = json.dumps(b).encode() if b else None
    req = urllib.request.Request(BASE + ep, data=data, headers=H, method=m)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


JOBS = {
"shop-strip": ("1344:768",
 "Documentary photograph inside a small Indian kirana shop, shot from the customer side of the "
 "counter. A long vertical hanging strip of joined single-serve drink sachets dangles in the "
 "doorway among other hanging sachet strips, catching the light. The sachets on that strip carry "
 "the design in @pack exactly: same deep blue and orange artwork, same mountain, same lettering. "
 "Behind, wooden shelves of biscuits and jars, a steel counter, a shopkeeper out of focus. Warm "
 "afternoon light, dust in the air, honest and lived in. 35mm lens, natural light, shallow depth "
 "of field."),

"shop-handover": ("1344:768",
 "Documentary photograph at a roadside stall in India. A shopkeeper's hands passing a single "
 "drink sachet across a steel counter to a customer's hand. The sachet carries the design in "
 "@pack exactly: same deep blue and orange artwork, same mountain, same lettering. Close in on "
 "the exchange, the counter and hanging sachet strips soft behind. Hot bright daylight, real "
 "skin, real hands, no styling. 50mm lens, shallow depth of field."),

"shop-counter": ("1344:768",
 "Documentary photograph of a tea stall counter in an Indian market at midday. An open display "
 "carton on the counter packed upright with single-serve drink sachets, all carrying the design "
 "in @pack exactly: same deep blue and orange artwork, same mountain, same lettering. A steel "
 "kettle and glasses beside it, painted Hindi signage behind, a customer's arm reaching in. "
 "Strong sunlight and hard shadow, saturated street colour. 35mm lens, natural light."),
}


def go(name):
    ratio, prompt = JOBS[name]
    body = {"model": "gemini_image3_pro", "promptText": prompt[:995], "ratio": ratio,
            "referenceImages": [{"uri": data_uri(REF), "tag": "pack"}]}
    st, d = api("POST", "/v1/text_to_image", body)
    if st not in (200, 201):
        print(f"ERR  {name}  {st}  {json.dumps(d)[:300]}", flush=True)
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
            print(f"FAIL {name} {json.dumps(d)[:300]}", flush=True)
            return
        time.sleep(6)
    print(f"TIMEOUT {name}", flush=True)


if __name__ == "__main__":
    names = sys.argv[1:] or list(JOBS)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(go, names))
    print("DONE", flush=True)
