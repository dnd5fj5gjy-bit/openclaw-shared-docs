#!/usr/bin/env python3
"""Monitor and download s05-s07b as they complete."""
import requests, time, os

KEY = "key_91a58fa80debc1cc9981f00972dcc49e6ab272614e8795cfcf9f642b5ed17de8c4b816ba0bc63337bf097281e10039b30d13d8b38e098992378501ab6f0023a4"
BASE = "https://api.dev.runwayml.com"
HEADERS = {"Authorization": f"Bearer {KEY}", "X-Runway-Version": "2024-11-06"}
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clips")

TASKS = {
    "s05": "6d14d009-6ba5-432e-8648-82935766c0bf",
    "s06": "e312e8ef-a579-4dc4-9ae3-69b6426a3511",
    "s07": "143a5515-96a5-4007-b865-69fb21072abc",
    "s07b": "9fe964c1-6693-4ca7-b746-3d258e2fa801",
}

pending = {k: v for k, v in TASKS.items()
           if not os.path.exists(os.path.join(OUT_DIR, f"{k}.mp4"))}

print(f"Monitoring {len(pending)} scenes: {list(pending.keys())}")

while pending:
    for sid, tid in list(pending.items()):
        r = requests.get(f"{BASE}/v1/tasks/{tid}", headers=HEADERS, timeout=15)
        if r.status_code != 200:
            continue
        d = r.json()
        status = d.get("status", "")
        if status == "SUCCEEDED":
            output = d.get("output", [])
            url = output[0] if isinstance(output, list) else output
            resp = requests.get(url, timeout=180, stream=True)
            if resp.status_code == 200:
                out_path = os.path.join(OUT_DIR, f"{sid}.mp4")
                with open(out_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        f.write(chunk)
                size_mb = os.path.getsize(out_path) / 1024 / 1024
                print(f"  [done] {sid} ({size_mb:.1f}MB)")
                del pending[sid]
        elif status in ("FAILED", "CANCELLED"):
            print(f"  [fail] {sid}: {d.get('failure', '?')}")
            del pending[sid]
        else:
            print(f"  {sid}: {status} {d.get('progress', 0):.0%}")
    if pending:
        time.sleep(30)

print("All early scenes done.")
