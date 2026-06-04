#!/usr/bin/env python3
"""
Assemble Wildernests Frontier video.
Kinetic typography: VO text on dark backgrounds, VO audio narration.
Output: frontier-video.mp4 (1920x1080, ~2:40)
"""
import subprocess, os, sys, json, textwrap

BASE = os.path.dirname(__file__)
AUDIO_DIR = os.path.join(BASE, "audio")
TMP_DIR   = os.path.join(BASE, "tmp")
OUT_FILE  = os.path.join(BASE, "wildernests-frontier-video.mp4")

FONT_SERIF  = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
FONT_SANS   = "/System/Library/Fonts/HelveticaNeue.ttc"
W, H = 1920, 1080
GOLD = "0xc8a84a"
CREAM = "0xf2ede4"
MUTED = "0x8a847a"

# Scene definitions
# (id, duration_s, bg_hex, label, vo_text, act_label)
SCENES = [
    # Title
    ("title", 6, "#020202", None, None, None),
    # ACT ONE
    ("s01",  8,  "#0a0a10", "ACT ONE", "For two hundred thousand years...", None),
    ("s02", 10,  "#0a0c14", None, "...we've built our lives around\nwhat we could not live without.", None),
    ("s04", 10,  "#080c14", None, "We shaped our first cities\nfrom mud and silt.", None),
    ("s05", 10,  "#0f1007", None, "We built where the soil was fertile\nand the ground held firm.", None),
    ("s06", 14,  "#0d0c0a", None, "We hung our lives off wires\nand roads and pipes.\nWe handed our water to the reservoir.\nOur power to the grid.\nOur planning to a committee.\nWe lived where the system allowed us to.", None),
    ("s07", 12,  "#080808", None, "Every home we have ever built\nhas been built by necessity.\nWe have lived where the river ran\nand the land was rich and the roads ran through,\nnever where we longed to.", None),
    # Pivot - silence
    ("s07b", 4, "#020202", None, None, None),
    # ACT THREE
    ("s08", 10, "#0a0c10", "THE RENEGADES", "The real renegades aren't\nbuilding cities anymore.\nWe're walking back out into the land.\nTaking everything we need with us.", None),
    ("s09",  5, "#0a0e1a", None, "The sun is our power.", None),
    ("s10",  4, "#020202", None, None, None),  # silent - night glow
    ("s11",  5, "#060c14", None, "The water comes\nfrom the air itself,", None),
    ("s12",  6, "#060c14", None, "drawn down by an\natmospheric water generator.", None),
    ("s13",  4, "#060c14", None, None, None),  # silent - water tap
    # ACT FOUR
    ("s14",  5, "#080808", "AND WE WILL HOLD.", None, None),  # shutters
    ("s15",  5, "#060606", None, "Our walls hold\nwhen the wind comes,", None),
    ("s16",  4, "#140804", None, "when fires burn,", None),
    ("s17",  4, "#080808", None, "when the ground itself\nmoves under us,", None),
    ("s18",  4, "#060a12", None, "when the rivers rise.", None),
    ("s19",  7, "#0a0c08", None, "No councils to ask,\nno grid to wait on,\nno permission to need.", None),
    ("s20",  6, "#1c1606", None, "Raised in three days.\nOn any land we choose.", None),
    ("s21", 10, "#1e1606", None, "Wherever we choose to stand.", None),
    # Aerial retreat - silence
    ("s22",  8, "#020202", None, None, None),
    # End title
    ("s23",  8, "#000000", "WILDERNESTS", None, "The world is yours.\nLive in it."),
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

def hex_to_ffmpeg(h):
    h = h.lstrip("#")
    return f"0x{h}"

def escape_text(t):
    """Escape text for ffmpeg drawtext."""
    return t.replace("'", "\\'").replace(":", "\\:").replace("\\n", "\n")

def make_drawtext(text, y_frac, font_path, size, color, duration, fade_in=1.0, fade_out=1.0, x_offset=0):
    """Build ffmpeg drawtext filter for a single line."""
    d = duration
    fi = fade_in
    fo = fade_out
    alpha_expr = f"if(lt(t\\,{fi})\\,t/{fi}\\,if(lt(t\\,{d-fo})\\,1\\,max(0\\,({d}-t)/{fo})))"
    # Escape colons in font path for ffmpeg filter syntax
    fp = font_path.replace(":", "\\:")
    txt = escape_text(text)
    x = f"(W-text_w)/2+{x_offset}"
    y = f"H*{y_frac}-text_h/2"
    return (f"drawtext=fontfile='{fp}'"
            f":text='{txt}'"
            f":fontsize={size}:fontcolor={color}"
            f":x={x}:y={y}"
            f":alpha='{alpha_expr}'")

def build_scene_clip(scene_id, duration, bg_hex, label, vo_text, end_tag, index):
    """Generate one scene video clip (no audio)."""
    out = os.path.join(TMP_DIR, f"{index:02d}_{scene_id}_vid.mp4")
    if os.path.exists(out):
        print(f"  [skip vid] {scene_id}")
        return out

    bg_color = bg_hex.lstrip("#")
    vf_parts = []

    # Background: color + subtle vignette
    bg_filter = f"color=c=#{bg_color}:size={W}x{H}:duration={duration},format=yuv420p"

    # ---- ACT LABEL ----
    if label:
        vf_parts.append(make_drawtext(
            label, 0.42,
            FONT_SANS, 18, GOLD, duration, fade_in=1.5, fade_out=1.5
        ).replace("y=H*0.42-text_h/2", "y=H*0.42-text_h/2"))

    # ---- VO TEXT ----
    if vo_text:
        lines = vo_text.split("\n")
        n = len(lines)
        fs = 52 if n <= 2 else (42 if n <= 4 else 32)
        line_h = fs * 1.55
        total_h = n * line_h
        for i, line in enumerate(lines):
            y_px = f"(H-{total_h:.0f})/2+{i * line_h:.0f}"
            fp = FONT_SERIF.replace(":", "\\:")
            txt = escape_text(line)
            fi = 1.2
            fo = 1.0
            d = duration
            alpha_expr = f"if(lt(t\\,{fi})\\,t/{fi}\\,if(lt(t\\,{d-fo})\\,1\\,max(0\\,({d}-t)/{fo})))"
            vf_parts.append(
                f"drawtext=fontfile='{fp}'"
                f":text='{txt}'"
                f":fontsize={fs}:fontcolor={CREAM}"
                f":x=(W-text_w)/2:y={y_px}"
                f":alpha='{alpha_expr}'"
            )

    # ---- END TAG (final title card) ----
    if end_tag:
        tag_lines = end_tag.split("\n")
        for i, tl in enumerate(tag_lines):
            fp = FONT_SERIF.replace(":", "\\:")
            txt = escape_text(tl)
            fi = 2.0
            fo = 1.0
            d = duration
            alpha_expr = f"if(lt(t\\,{fi})\\,t/{fi}\\,if(lt(t\\,{d-fo})\\,1\\,max(0\\,({d}-t)/{fo})))"
            y_px = f"H*0.56+{i * 52 * 1.5:.0f}"
            vf_parts.append(
                f"drawtext=fontfile='{fp}'"
                f":text='{txt}'"
                f":fontsize=40:fontcolor={MUTED}"
                f":x=(W-text_w)/2:y={y_px}"
                f":alpha='{alpha_expr}'"
            )

    # Special title scene
    if scene_id == "title":
        # WILDERNESTS
        fp = FONT_SANS.replace(":", "\\:")
        fi, fo, d = 1.5, 1.0, duration
        alpha_expr = f"if(lt(t\\,{fi})\\,t/{fi}\\,if(lt(t\\,{d-fo})\\,1\\,max(0\\,({d}-t)/{fo})))"
        vf_parts.append(
            f"drawtext=fontfile='{fp}'"
            f":text='WILDERNESTS'"
            f":fontsize=90:fontcolor={CREAM}"
            f":x=(W-text_w)/2:y=H*0.40-text_h/2"
            f":alpha='{alpha_expr}'"
        )
        vf_parts.append(
            f"drawtext=fontfile='{fp}'"
            f":text='THE FRONTIER'"
            f":fontsize=24:fontcolor={GOLD}"
            f":x=(W-text_w)/2:y=H*0.54-text_h/2"
            f":alpha='{alpha_expr}'"
        )

    if scene_id == "s23":
        fp = FONT_SANS.replace(":", "\\:")
        fi, fo, d = 2.0, 2.0, duration
        alpha_expr = f"if(lt(t\\,{fi})\\,t/{fi}\\,if(lt(t\\,{d-fo})\\,1\\,max(0\\,({d}-t)/{fo})))"
        vf_parts.append(
            f"drawtext=fontfile='{fp}'"
            f":text='WILDERNESTS'"
            f":fontsize=110:fontcolor={CREAM}"
            f":x=(W-text_w)/2:y=H*0.38-text_h/2"
            f":alpha='{alpha_expr}'"
        )

    vf = bg_filter
    if vf_parts:
        vf += "," + ",".join(vf_parts)

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=c=#{bg_color}:size={W}x{H}:duration={duration}",
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        out
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERR vid] {scene_id}: {result.stderr[-500:]}")
        return None
    print(f"  [ok  vid] {scene_id}")
    return out


def build_scene_audio(scene_id, duration):
    """Generate padded/silent audio for one scene."""
    out = os.path.join(TMP_DIR, f"{scene_id}_aud.aac")
    if os.path.exists(out):
        return out

    vo_file = VO_AUDIO_MAP.get(scene_id)

    if vo_file:
        src = os.path.join(AUDIO_DIR, vo_file)
        # Get VO duration
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", src],
            capture_output=True, text=True
        )
        vo_dur = float(probe.stdout.strip())

        if vo_dur >= duration:
            # VO fills the scene
            cmd = ["ffmpeg", "-y", "-i", src,
                   "-af", f"apad=pad_dur={duration}",
                   "-t", str(duration), "-c:a", "aac", out]
        else:
            # VO + trailing silence
            pad = duration - vo_dur
            cmd = ["ffmpeg", "-y", "-i", src,
                   "-af", f"apad=pad_dur={pad}",
                   "-t", str(duration), "-c:a", "aac", out]
    else:
        # Silent scene
        cmd = ["ffmpeg", "-y",
               "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={duration}",
               "-t", str(duration), "-c:a", "aac", out]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERR aud] {scene_id}: {result.stderr[-300:]}")
        return None
    print(f"  [ok  aud] {scene_id}")
    return out


def main():
    os.makedirs(TMP_DIR, exist_ok=True)

    print("=== Generating scene clips ===")
    vid_files = []
    aud_files = []

    for i, (scene_id, duration, bg_hex, label, vo_text, end_tag) in enumerate(SCENES):
        print(f"Scene {i+1}/{len(SCENES)}: {scene_id} ({duration}s)")

        vid = build_scene_clip(scene_id, duration, bg_hex, label, vo_text, end_tag, i)
        aud = build_scene_audio(scene_id, duration)

        if vid and aud:
            vid_files.append(vid)
            aud_files.append(aud)
        else:
            print(f"  [SKIP] {scene_id} - missing video or audio")

    print(f"\n=== Concatenating {len(vid_files)} scenes ===")

    # Write concat lists
    vid_list = os.path.join(TMP_DIR, "vid_list.txt")
    aud_list = os.path.join(TMP_DIR, "aud_list.txt")

    with open(vid_list, "w") as f:
        for v in vid_files:
            f.write(f"file '{v}'\n")
    with open(aud_list, "w") as f:
        for a in aud_files:
            f.write(f"file '{a}'\n")

    # Concatenate video
    vid_concat = os.path.join(TMP_DIR, "video_concat.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", vid_list, "-c", "copy", vid_concat
    ], check=True, capture_output=True)
    print("Video concatenated.")

    # Concatenate audio
    aud_concat = os.path.join(TMP_DIR, "audio_concat.aac")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", aud_list, "-c", "copy", aud_concat
    ], check=True, capture_output=True)
    print("Audio concatenated.")

    # Combine video + audio
    print(f"\n=== Assembling final video ===")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", vid_concat,
        "-i", aud_concat,
        "-c:v", "copy", "-c:a", "aac",
        "-shortest",
        OUT_FILE
    ], check=True)
    print(f"\nDONE: {OUT_FILE}")

    # Get file size
    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
    print(f"File size: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
