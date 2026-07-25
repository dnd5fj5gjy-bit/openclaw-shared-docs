#!/usr/bin/env python3
"""Norway rough cut v2.

Jesse's note: shot of him walking off the boat, he stops, talks to his phone, then cut to a fast
10-second action montage to music.

So: one 7s opening that plays the whole beat (walk, stop, lift phone, talk), then five 2s cuts under
music, then the card. The spoken assistant lines from v1 are gone - music carries the montage now - but
the reasoning still appears on screen, one line per cut, because the reasoning is the product.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
W, H, FPS = 1280, 720, 24
MUSIC, MUSIC_IN = "../frontier-video/music.mp3", 44.0   # loudest sustained window in the track

OPEN_DUR = 7.0
MONT = [("clean/s2_kayak.mp4", "fjord glass at dawn"),
        ("clips/s6_climb.mp4", "granite dry by 09:00"),
        ("clean/s3_base.mp4",  "Kjerag · wind 4kt"),
        ("clean/s4_sail.mp4",  "evening tide 19:40"),
        ("clean/s5_bike.mp4",  "Rallarvegen before the front")]
CUT = 2.0
MONT_START = OPEN_DUR
END_START = MONT_START + CUT * len(MONT)
END_DUR = 3.0
TOTAL = END_START + END_DUR


def font(sz):
    for p in ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()


def trace_png(text, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = font(26); x, y = 58, H - 104
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - 20, y - 16, x + tw + 46, y + 44], radius=7, fill=(0, 0, 0, 125))
    d.text((x, y), text, font=f, fill=(255, 255, 255, 242))
    d.rectangle([x + tw + 10, y + 3, x + tw + 17, y + 33], fill=(120, 220, 170, 235))
    im.save(path)


def endcard(path):
    im = Image.new("RGB", (W, H), (8, 9, 11)); d = ImageDraw.Draw(im)
    b = os.path.expanduser("~/openclaw-shared-docs/junior/companions/heads/bear.png")
    if os.path.exists(b):
        img = Image.open(b).convert("RGBA").resize((240, 240), Image.LANCZOS)
        im.paste(img, (345, 200), img)
    d.text((640, 240), "BEAR GRYLLS", font=font(38), fill=(255, 255, 255))
    d.text((640, 298), "two days in Norway,", font=font(26), fill=(168, 172, 178))
    d.text((640, 334), "planned on the dock.", font=font(26), fill=(168, 172, 178))
    d.text((640, 404), "rough cut  ·  stand-in footage", font=font(18), fill=(96, 100, 106))
    im.save(path)


def run(a): subprocess.run(a, check=True, capture_output=True)


if __name__ == "__main__":
    os.makedirs("build2", exist_ok=True)
    endcard("build2/end.png")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", "build2/end.png", "-t", str(END_DUR),
         "-vf", f"scale={W}:{H},fade=t=in:st=0:d=0.35", "-r", str(FPS),
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "build2/end.mp4"])

    parts = []
    run(["ffmpeg", "-v", "error", "-y", "-i", "clips/s1b_ferry_stop.mp4", "-t", str(OPEN_DUR),
         "-vf", f"scale={W}:{H},fps={FPS}", "-c:v", "libx264", "-crf", "18",
         "-pix_fmt", "yuv420p", "-an", "build2/p_open.mp4"])
    parts.append("build2/p_open.mp4")

    for i, (clip, _) in enumerate(MONT):
        p = f"build2/p{i}.mp4"
        # take from 1.5s in: the model's first second is usually the weakest part of a generation
        run(["ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-i", clip, "-t", str(CUT),
             "-vf", f"scale={W}:{H},fps={FPS}", "-c:v", "libx264", "-crf", "18",
             "-pix_fmt", "yuv420p", "-an", p])
        parts.append(p)
    parts.append("build2/end.mp4")

    with open("build2/list.txt", "w") as f:
        for p in parts: f.write(f"file '{os.path.basename(p)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "build2/list.txt",
         "-c", "copy", "build2/video.mp4"])

    ins, filt, last = ["-i", "build2/video.mp4"], [], "0:v"
    for i, (_, text) in enumerate(MONT):
        trace_png(text, f"build2/t{i}.png")
        ins += ["-i", f"build2/t{i}.png"]
        st = MONT_START + i * CUT
        filt.append(f"[{last}][{i+1}:v]overlay=0:0:enable='between(t,{st+0.15},{st+CUT-0.1})'[v{i}]")
        last = f"v{i}"
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(filt),
         "-map", f"[{last}]", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         "build2/video_txt.mp4"])

    # audio: his line over the dock, music hitting on the first montage cut
    run(["ffmpeg", "-v", "error", "-y",
         "-i", "audio/bear_bg01.mp3", "-ss", str(MUSIC_IN), "-i", MUSIC,
         "-filter_complex",
         f"[0:a]adelay=5100|5100,volume=1.15[vo];"
         f"[1:a]atrim=0:{TOTAL - MONT_START + 0.4},asetpts=PTS-STARTPTS,"
         f"adelay={int((MONT_START-0.35)*1000)}|{int((MONT_START-0.35)*1000)},"
         f"afade=t=in:st={MONT_START-0.35}:d=0.3,afade=t=out:st={END_START+0.6}:d=1.6,volume=0.72[mu];"
         f"[vo][mu]amix=inputs=2:dropout_transition=0:normalize=0,apad[a]",
         "-map", "[a]", "-t", str(TOTAL), "-c:a", "aac", "-b:a", "192k", "build2/audio.m4a"])

    run(["ffmpeg", "-v", "error", "-y", "-i", "build2/video_txt.mp4", "-i", "build2/audio.m4a",
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "norway-rough-cut-v2.mp4"])
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", "norway-rough-cut-v2.mp4"], capture_output=True, text=True).stdout.strip()
    print(f"norway-rough-cut-v2.mp4  {os.path.getsize('norway-rough-cut-v2.mp4')/1e6:.1f} MB  {d}s "
          f"(expected {TOTAL})")
