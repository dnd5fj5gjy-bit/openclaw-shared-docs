#!/usr/bin/env python3
"""
Wildernests Frontier — Final video assembly.
Combines all video clips with VO audio, letterbox, and cinematic grade.
Run this once all clips in clips/ are ready.
"""
import subprocess, os, sys, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
CLIPS_DIR = BASE / "clips"
AUDIO_DIR = BASE / "audio-el"   # ElevenLabs VO (MP3 files)
TMP_DIR   = BASE / "tmp_final"
OUT_FILE  = BASE / "wildernests-frontier-FINAL.mp4"
MUSIC_FILE = BASE / "music.mp3"  # optional background score

TMP_DIR.mkdir(exist_ok=True)

# Scene order and durations (matches storyboard)
# (scene_id, duration_s, has_vo, title_text, title_position)
SCENES = [
    # Pre-title black lead-in
    ("black_in",  2, False, None, None),

    # Title card - overlaid on s01
    ("s01",  8, True,  "WILDERNESTS\nTHE FRONTIER", "title"),

    ("s02", 10, True,  None, None),

    # ACT ONE label
    ("s04",  8, True,  "ACT ONE", "act"),
    ("s05",  8, True,  None, None),
    ("s06", 14, True,  None, None),
    ("s07", 12, True,  None, None),

    # Black pause
    ("s07b", 4, False, None, None),

    # THE RENEGADES label
    ("s08", 10, True,  "THE RENEGADES", "act"),
    ("s09",  6, True,  None, None),
    ("s10",  6, False, None, None),
    ("s11",  6, True,  None, None),
    ("s12",  6, True,  None, None),
    ("s13",  6, False, None, None),

    # AND WE WILL HOLD label
    ("s14",  5, False, "AND WE WILL HOLD.", "act"),

    ("s15",  8, True,  None, None),
    ("s16",  6, True,  None, None),
    ("s17",  6, True,  None, None),
    ("s18",  6, True,  None, None),
    ("s19",  8, True,  None, None),
    ("s20",  8, True,  None, None),

    # Hero shot
    ("s21", 10, True,  None, None),
    ("s22",  8, False, None, None),

    # End title - overlaid on s23
    ("s23",  6, False, "WILDERNESTS", "end_title"),

    # Post-end black
    ("black_out", 3, False, None, None),
]

# VO scenes that have audio files
VO_MAP = {
    "s01": "s01.mp3", "s02": "s02.mp3", "s04": "s04.mp3",
    "s05": "s05.mp3", "s06": "s06.mp3", "s07": "s07.mp3",
    "s08": "s08.mp3", "s09": "s09.mp3",
    "s11": "s11.mp3", "s12": "s12.mp3",
    "s15": "s15.mp3", "s16": "s16.mp3", "s17": "s17.mp3",
    "s18": "s18.mp3", "s19": "s19.mp3", "s20": "s20.mp3",
    "s21": "s21.mp3",
}

W, H = 1280, 720
# 2.39:1 letterbox bars (92px top and bottom)
BAR_H = 92

def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("CMD FAILED:", " ".join(str(c) for c in cmd[:6]))
        print(r.stderr[-400:])
        sys.exit(1)
    return r


def make_black_clip(out_path, duration):
    """Generate a black video clip with silence."""
    run(["ffmpeg", "-y",
         "-f", "lavfi", "-i", f"color=c=black:size={W}x{H}:r=24",
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-t", str(duration),
         "-c:v", "libx264", "-preset", "fast", "-crf", "18",
         "-c:a", "aac", "-ar", "44100",
         "-pix_fmt", "yuv420p", out_path])


def letterbox_filter():
    """Add 2.39:1 black bars via drawbox."""
    return (
        f"drawbox=x=0:y=0:w=iw:h={BAR_H}:color=black:t=fill,"
        f"drawbox=x=0:y=ih-{BAR_H}:w=iw:h={BAR_H}:color=black:t=fill"
    )


def cinematic_grade_filter():
    """Subtle cinematic color grade: slightly cool shadows, warm highlights, mild desaturation."""
    return "curves=r='0/0 .5/.48 1/1':g='0/0 .5/.5 1/1':b='0/0.02 .5/.52 1/1'"


def title_overlay_filter(title_text, position, duration):
    """Generate ffmpeg drawtext filter for title overlays."""
    lines = title_text.split("\n")

    if position == "title":
        # WILDERNESTS large + THE FRONTIER smaller below
        if len(lines) == 2:
            return (
                f"drawtext=text='{lines[0]}':font=Helvetica:fontsize=90:fontcolor=white@0.92:"
                f"x=(w-text_w)/2:y=(h/2)-80:"
                f"enable='between(t,1,{duration-1})',"
                f"drawtext=text='{lines[1]}':font=Helvetica:fontsize=26:fontcolor=0xC8A84A@0.85:"
                f"x=(w-text_w)/2:y=(h/2)+40:"
                f"enable='between(t,1,{duration-1})'"
            )

    elif position == "act":
        # Small gold act label, centered, upper third
        text = title_text.replace("\n", " ")
        return (
            f"drawtext=text='{text}':font=Helvetica:fontsize=18:fontcolor=0xC8A84A@0.8:"
            f"x=(w-text_w)/2:y=h/3:"
            f"enable='between(t,0.5,{duration-1})'"
        )

    elif position == "end_title":
        # WILDERNESTS large, centered
        return (
            f"drawtext=text='{lines[0]}':font=Helvetica:fontsize=110:fontcolor=white@0.92:"
            f"x=(w-text_w)/2:y=(h-text_h)/2:"
            f"enable='between(t,1,{duration-1})'"
        )

    return None


def process_scene_clip(scene_id, duration, has_vo, title_text, title_pos, idx):
    """Process one scene: apply grade, letterbox, title overlay. Return (video_path, audio_path)."""
    out_v = str(TMP_DIR / f"{idx:02d}_{scene_id}_v.mp4")
    out_a = str(TMP_DIR / f"{idx:02d}_{scene_id}_a.aac")

    if os.path.exists(out_v) and os.path.exists(out_a):
        print(f"  [skip] {scene_id}")
        return out_v, out_a

    # Source video
    if scene_id in ("black_in", "black_out"):
        tmp_clip = str(TMP_DIR / f"black_{duration}s.mp4")
        if not os.path.exists(tmp_clip):
            make_black_clip(tmp_clip, duration)
        src_v = tmp_clip
    else:
        src_v = str(CLIPS_DIR / f"{scene_id}.mp4")
        if not os.path.exists(src_v):
            print(f"  [MISSING] {scene_id}.mp4 - skipping")
            return None, None

    # Build video filter chain
    vf_parts = []

    # 1. Scale to exact dimensions if needed
    vf_parts.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2")

    # 2. Cinematic color grade
    vf_parts.append(cinematic_grade_filter())

    # 3. Letterbox
    vf_parts.append(letterbox_filter())

    # 4. Fade in/out (0.5s)
    fi, fo = 0.5, 0.5
    fo_start = max(0, duration - fo)
    vf_parts.append(f"fade=t=in:st=0:d={fi}")
    vf_parts.append(f"fade=t=out:st={fo_start}:d={fo}")

    # 5. Title overlay
    if title_text and title_pos:
        title_filter = title_overlay_filter(title_text, title_pos, duration)
        if title_filter:
            vf_parts.append(title_filter)

    vf_str = ",".join(vf_parts)

    cmd = [
        "ffmpeg", "-y",
        "-i", src_v,
        "-t", str(duration),
        "-vf", vf_str,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-an", out_v
    ]
    r = run(cmd, check=False)
    if r.returncode != 0:
        print(f"  [vf err] {scene_id}: {r.stderr[-300:]}")
        return None, None

    # Build audio: VO padded to duration, or silence
    vo_file = VO_MAP.get(scene_id)
    if has_vo and vo_file:
        src_a = str(AUDIO_DIR / vo_file)
        if os.path.exists(src_a):
            cmd_a = [
                "ffmpeg", "-y", "-i", src_a,
                "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={max(0,duration-0.5)}:d=0.5,apad=pad_dur={duration}",
                "-t", str(duration), "-c:a", "aac", "-ar", "44100", out_a
            ]
        else:
            vo_file = None

    if not has_vo or not vo_file or not os.path.exists(str(AUDIO_DIR / vo_file)):
        # Silence
        cmd_a = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-t", str(duration), "-c:a", "aac", out_a
        ]

    r = run(cmd_a, check=False)
    if r.returncode != 0:
        print(f"  [aud err] {scene_id}: {r.stderr[-200:]}")
        return None, None

    size = os.path.getsize(out_v) / 1024 / 1024
    print(f"  [ok] {scene_id} ({duration}s, {size:.1f}MB)")
    return out_v, out_a


def main():
    print("=== WILDERNESTS FRONTIER — FINAL ASSEMBLY ===")

    # Check which clips are ready
    missing = []
    for scene_id, duration, has_vo, _, _ in SCENES:
        if scene_id in ("black_in", "black_out"):
            continue
        clip = CLIPS_DIR / f"{scene_id}.mp4"
        if not clip.exists():
            missing.append(scene_id)

    if missing:
        print(f"\nMISSING CLIPS: {missing}")
        print("Run clip generation pipelines first. Proceeding with available clips.\n")

    vid_files = []
    aud_files = []

    for idx, (scene_id, duration, has_vo, title_text, title_pos) in enumerate(SCENES):
        print(f"\n[{idx+1}/{len(SCENES)}] {scene_id} ({duration}s)")
        v, a = process_scene_clip(scene_id, duration, has_vo, title_text, title_pos, idx)
        if v and a:
            vid_files.append(v)
            aud_files.append(a)
        else:
            print(f"  [SKIP] {scene_id}")

    if not vid_files:
        print("No clips to assemble!")
        sys.exit(1)

    print(f"\n=== Concatenating {len(vid_files)} clips ===")

    vlist = str(TMP_DIR / "vlist.txt")
    alist = str(TMP_DIR / "alist.txt")
    with open(vlist, "w") as f:
        for v in vid_files:
            f.write(f"file '{v}'\n")
    with open(alist, "w") as f:
        for a in aud_files:
            f.write(f"file '{a}'\n")

    vconcat = str(TMP_DIR / "vconcat.mp4")
    aconcat = str(TMP_DIR / "aconcat.aac")

    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", vlist, "-c", "copy", vconcat])
    print("Video concatenated.")

    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", alist, "-c", "copy", aconcat])
    print("Audio concatenated.")

    # Final assembly with optional background music
    print("\n=== Final mix ===")
    if MUSIC_FILE.exists():
        # Mix VO with background music (music at -18dB under VO)
        cmd = [
            "ffmpeg", "-y",
            "-i", vconcat,
            "-i", aconcat,
            "-i", str(MUSIC_FILE),
            "-filter_complex",
            "[1:a]volume=1.0[vo];[2:a]volume=0.15[music];[vo][music]amix=inputs=2:duration=first[audio]",
            "-map", "0:v", "-map", "[audio]",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(OUT_FILE)
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", vconcat, "-i", aconcat,
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            str(OUT_FILE)
        ]

    run(cmd)

    size_mb = os.path.getsize(str(OUT_FILE)) / 1024 / 1024
    dur_r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(OUT_FILE)],
        capture_output=True, text=True
    )
    dur = float(dur_r.stdout.strip() or 0)
    print(f"\nDONE: {OUT_FILE}")
    print(f"Size: {size_mb:.1f}MB | Duration: {dur:.0f}s ({dur/60:.1f} min)")


if __name__ == "__main__":
    main()
