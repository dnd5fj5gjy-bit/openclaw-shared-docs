#!/usr/bin/env python3
"""
Wildernests Frontier — kinetic typography video.
Uses Pillow for text rendering + ffmpeg for video assembly.
Output: wildernests-frontier-video.mp4 (~2:40, 1920x1080)
"""
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE, "audio")
TMP_DIR   = os.path.join(BASE, "tmp")
OUT_FILE  = os.path.join(BASE, "wildernests-frontier-video.mp4")

os.makedirs(TMP_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_SERIF_IT  = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
FONT_SERIF     = "/System/Library/Fonts/Supplemental/Georgia.ttf"
FONT_SANS      = "/System/Library/Fonts/HelveticaNeue.ttc"

CREAM  = (242, 237, 228)
GOLD   = (200, 168, 74)
MUTED  = (138, 132, 122)
DIM    = (80, 76, 70)

# Scene definitions
# (id, duration_s, bg_rgb, act_label, vo_lines, bottom_lines)
SCENES = [
    ("title", 6,  (2,  2,  2),   None,             [],
     []),

    ("s01",   8,  (10, 10, 16),  "ACT ONE",
     ["For two hundred thousand years..."],
     []),

    ("s02",  10,  (10, 12, 20),  None,
     ["...we've built our lives around",
      "what we could not live without."],
     []),

    ("s04",  10,  (8,  12, 20),  None,
     ["We shaped our first cities",
      "from mud and silt."],
     []),

    ("s05",  10,  (14, 15, 8),   None,
     ["We built where the soil was fertile",
      "and the ground held firm."],
     []),

    ("s06",  14,  (13, 12, 10),  None,
     ["We hung our lives off wires",
      "and roads and pipes.",
      "We handed our water to the reservoir.",
      "Our power to the grid.",
      "Our planning to a committee.",
      "We lived where the system allowed us to."],
     []),

    ("s07",  12,  (8,  8,  8),   None,
     ["Every home we have ever built",
      "has been built by necessity.",
      "We have lived where the river ran",
      "and the land was rich and the roads ran through,",
      "never where we longed to."],
     []),

    ("s07b",  4,  (2,  2,  2),   None, [], []),

    ("s08",  10,  (10, 12, 16),  "THE RENEGADES",
     ["The real renegades aren't",
      "building cities anymore.",
      "We're walking back out into the land.",
      "Taking everything we need with us."],
     []),

    ("s09",   5,  (10, 14, 26),  None,
     ["The sun is our power."],
     []),

    ("s10",   4,  (2,  2,  2),   None, [], []),

    ("s11",   5,  (6,  12, 20),  None,
     ["The water comes",
      "from the air itself,"],
     []),

    ("s12",   6,  (6,  12, 20),  None,
     ["drawn down by an",
      "atmospheric water generator."],
     []),

    ("s13",   4,  (6,  12, 20),  None, [], []),

    ("s14",   5,  (8,  8,  8),   "AND WE WILL HOLD.", [], []),

    ("s15",   5,  (6,  6,  6),   None,
     ["Our walls hold",
      "when the wind comes,"],
     []),

    ("s16",   4,  (20, 8,  4),   None,
     ["when fires burn,"],
     []),

    ("s17",   4,  (8,  8,  8),   None,
     ["when the ground itself",
      "moves under us,"],
     []),

    ("s18",   4,  (6,  10, 18),  None,
     ["when the rivers rise."],
     []),

    ("s19",   7,  (10, 12, 8),   None,
     ["No councils to ask,",
      "no grid to wait on,",
      "no permission to need."],
     []),

    ("s20",   6,  (28, 22, 6),   None,
     ["Raised in three days.",
      "On any land we choose."],
     []),

    ("s21",  10,  (30, 22, 6),   None,
     ["Wherever we choose to stand."],
     []),

    ("s22",   8,  (2,  2,  2),   None, [], []),

    ("s23",   8,  (0,  0,  0),   None, [],
     ["The world is yours.", "Live in it."]),
]

VO_AUDIO_MAP = {
    "s01": "s01.ogg", "s02": "s02.ogg", "s04": "s04.ogg",
    "s05": "s05.ogg", "s06": "s06.ogg", "s07": "s07.ogg",
    "s08": "s08.ogg", "s09": "s09.ogg",
    "s11": "s11.ogg", "s12": "s12.ogg",
    "s15": "s15.ogg", "s16": "s16.ogg", "s17": "s17.ogg",
    "s18": "s18.ogg", "s19": "s19.ogg", "s20": "s20.ogg",
    "s21": "s21.ogg",
}

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def render_scene_png(scene_id, bg_rgb, act_label, vo_lines, bottom_lines, out_path):
    img = Image.new("RGB", (W, H), color=bg_rgb)
    draw = ImageDraw.Draw(img)

    # Subtle vignette
    vign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vign)
    for r in range(0, 500, 10):
        alpha = int(100 * (1 - r / 500))
        vd.ellipse([r, r, W-r, H-r], outline=(0, 0, 0, alpha), width=10)
    img.paste(Image.alpha_composite(img.convert("RGBA"), vign).convert("RGB"))
    draw = ImageDraw.Draw(img)

    if scene_id == "title":
        # WILDERNESTS title
        f_title = load_font(FONT_SANS, 100)
        f_sub   = load_font(FONT_SANS, 26)
        tw, th = text_width(draw, "WILDERNESTS", f_title)
        draw.text(((W - tw) // 2, H * 4 // 10 - th // 2), "WILDERNESTS", fill=CREAM, font=f_title)
        sw, sh = text_width(draw, "THE FRONTIER", f_sub)
        draw.text(((W - sw) // 2, H * 55 // 100 - sh // 2), "THE FRONTIER", fill=GOLD, font=f_sub)
        img.save(out_path)
        return

    if scene_id == "s23":
        # End title
        f_title = load_font(FONT_SANS, 120)
        tw, th = text_width(draw, "WILDERNESTS", f_title)
        draw.text(((W - tw) // 2, H * 36 // 100 - th // 2), "WILDERNESTS", fill=CREAM, font=f_title)
        if bottom_lines:
            f_tag = load_font(FONT_SERIF_IT, 44)
            total_h = len(bottom_lines) * 60
            y0 = H * 60 // 100 - total_h // 2
            for i, line in enumerate(bottom_lines):
                lw, lh = text_width(draw, line, f_tag)
                draw.text(((W - lw) // 2, y0 + i * 60), line, fill=MUTED, font=f_tag)
        img.save(out_path)
        return

    # Act label (small gold, above text block)
    if act_label:
        f_label = load_font(FONT_SANS, 18)
        lw, lh = text_width(draw, act_label, f_label)
        draw.text(((W - lw) // 2, H * 36 // 100 - lh // 2), act_label, fill=GOLD, font=f_label)

    # VO text
    if vo_lines:
        n = len(vo_lines)
        fs = 72 if n <= 1 else (58 if n <= 2 else (44 if n <= 4 else 34))
        f_vo = load_font(FONT_SERIF_IT, fs)
        line_gap = int(fs * 1.6)
        total_h = n * line_gap
        y_start = (H - total_h) // 2 + (20 if act_label else 0)
        for i, line in enumerate(vo_lines):
            lw, lh = text_width(draw, line, f_vo)
            x = (W - lw) // 2
            y = y_start + i * line_gap
            # Subtle text shadow
            draw.text((x + 2, y + 2), line, fill=(0, 0, 0, 100), font=f_vo)
            draw.text((x, y), line, fill=CREAM, font=f_vo)

    img.save(out_path)


def build_scene_video(scene_id, duration, bg_rgb, act_label, vo_lines, bottom_lines, idx):
    """Render PNG + create video clip with fade."""
    vid_out = os.path.join(TMP_DIR, f"{idx:02d}_{scene_id}.mp4")
    if os.path.exists(vid_out):
        print(f"  [skip] {scene_id}")
        return vid_out

    png_path = os.path.join(TMP_DIR, f"{idx:02d}_{scene_id}.png")

    # Render PNG
    render_scene_png(scene_id, bg_rgb, act_label, vo_lines, bottom_lines, png_path)

    fi = 0.8  # fade in duration
    fo = 0.8  # fade out duration
    fo_start = duration - fo

    # Convert to video with fades
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", png_path,
        "-t", str(duration),
        "-vf", f"fade=t=in:st=0:d={fi},fade=t=out:st={fo_start}:d={fo}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "25",
        vid_out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [ERR] {scene_id}: {r.stderr[-200:]}")
        return None
    print(f"  [ok]  {scene_id} ({duration}s)")
    return vid_out


def build_audio(scene_id, duration):
    """Pad VO audio or generate silence."""
    aud_out = os.path.join(TMP_DIR, f"{scene_id}_aud.aac")
    if os.path.exists(aud_out):
        return aud_out

    vo_file = VO_AUDIO_MAP.get(scene_id)
    if vo_file:
        src = os.path.join(AUDIO_DIR, vo_file)
        cmd = ["ffmpeg", "-y", "-i", src,
               "-af", f"apad=pad_dur={duration}",
               "-t", str(duration), "-c:a", "aac", "-ar", "44100", aud_out]
    else:
        cmd = ["ffmpeg", "-y",
               "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
               "-t", str(duration), "-c:a", "aac", aud_out]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [ERR aud] {scene_id}: {r.stderr[-200:]}")
        return None
    return aud_out


def main():
    print("=== WILDERNESTS — THE FRONTIER ===")
    print(f"Scenes: {len(SCENES)}")

    vid_files = []
    aud_files = []

    for idx, (scene_id, duration, bg_rgb, act_label, vo_lines, bottom_lines) in enumerate(SCENES):
        print(f"\n[{idx+1}/{len(SCENES)}] {scene_id} ({duration}s)")
        v = build_scene_video(scene_id, duration, bg_rgb, act_label, vo_lines, bottom_lines, idx)
        a = build_audio(scene_id, duration)
        if v and a:
            vid_files.append(v)
            aud_files.append(a)
        else:
            print(f"  [FAIL] {scene_id}")

    print(f"\n=== Concatenating {len(vid_files)} clips ===")

    # Write concat lists
    vlist = os.path.join(TMP_DIR, "vlist.txt")
    alist = os.path.join(TMP_DIR, "alist.txt")
    with open(vlist, "w") as f:
        for v in vid_files:
            f.write(f"file '{v}'\n")
    with open(alist, "w") as f:
        for a in aud_files:
            f.write(f"file '{a}'\n")

    vconcat = os.path.join(TMP_DIR, "vconcat.mp4")
    aconcat = os.path.join(TMP_DIR, "aconcat.aac")

    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                         "-i", vlist, "-c", "copy", vconcat],
                        capture_output=True, text=True)
    if r.returncode != 0:
        print("Video concat failed:", r.stderr[-300:])
        sys.exit(1)
    print("Video concatenated.")

    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                         "-i", alist, "-c", "copy", aconcat],
                        capture_output=True, text=True)
    if r.returncode != 0:
        print("Audio concat failed:", r.stderr[-300:])
        sys.exit(1)
    print("Audio concatenated.")

    print("\n=== Final assembly ===")
    r = subprocess.run([
        "ffmpeg", "-y",
        "-i", vconcat, "-i", aconcat,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest", OUT_FILE
    ], capture_output=True, text=True)

    if r.returncode != 0:
        print("Final assembly failed:", r.stderr[-300:])
        sys.exit(1)

    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
    dur = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries",
                          "format=duration", "-of", "csv=p=0", OUT_FILE],
                         capture_output=True, text=True).stdout.strip()
    print(f"\nDONE: {OUT_FILE}")
    print(f"Size: {size_mb:.1f} MB | Duration: {float(dur):.0f}s ({float(dur)/60:.1f} min)")


if __name__ == "__main__":
    main()
