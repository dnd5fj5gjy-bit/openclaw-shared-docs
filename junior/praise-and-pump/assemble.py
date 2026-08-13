#!/usr/bin/env python3
"""
Praise and Pump - 40:00 master assembly.

Takes Suno exports and builds Bear's spec exactly (verified at source, WhatsApp
`papa` 12 Aug 2026, three messages 12:42 / 12:46+17:15 / 17:33):

  - 10 songs of exactly 3:00, one per exercise block
  - inside each working track: 30s song, 15s drums-and-beat only, repeated x4
  - 1:00 of standardised drum beat between each set
  - the whole thing bounced as ONE 40:00 track  ("3x10, 1x10")

Arithmetic: 10 x 3:00 = 30:00, plus 9 bridges x 1:00 + 1:00 reprise = 10:00. Total 40:00.

Everything is cut on the bar line at 128 BPM, so joins are inaudible:
  1 bar = 1.875s | 30s = 16 bars | 15s = 8 bars | 60s = 32 bars | 3:00 = 96 bars

INPUT  (put files in ./raw, any of wav/mp3/flac)
  01_praise_and_pump.wav        07_by_my_right_hand.wav
  02_seven_times_rising.wav     08_out_of_the_pit.wav
  03_all_things.wav             09_clean_heart.wav
  04_draw_near.wav              10_still_waters.wav
  05_wherever_you_go.wav        11_bridge.wav
  06_easy_yoke.wav              12_reprise.wav

  For tracks 2-9 also drop the Suno stems (Auto Split -> download):
  02_seven_times_rising_drums.wav, 02_seven_times_rising_bass.wav, etc.
  If a stem pair is missing the track is left continuous and a warning is printed.

OUTPUT ./out/praise-and-pump-master.wav   (40:00, -9 LUFS)
       ./out/praise-and-pump-master.mp3   (320kbps, for instructors' phones)

Usage:  python3 assemble.py [--raw ./raw] [--out ./out] [--bpm 128]
"""

import argparse, json, os, subprocess, sys, tempfile

BAR = 60.0 / 128 * 4          # 1.875s at 128 BPM 4/4
SONG_LEN = 180.0              # 3:00 = 96 bars
PLAY = 30.0                   # 16 bars of full mix
REST = 15.0                   # 8 bars of drums+bass only
BRIDGE_LEN = 60.0             # 32 bars
TARGET_LUFS = -9.0

# (index, slug, continuous?) - tracks 1 and 10 stay whole per the prompt pack:
# the warm-up needs unbroken flow and the warm-down an unbroken stretch.
TRACKS = [
    (1,  "praise_and_pump",   True),
    (2,  "seven_times_rising", False),
    (3,  "all_things",         False),
    (4,  "draw_near",          False),
    (5,  "wherever_you_go",    False),
    (6,  "easy_yoke",          False),
    (7,  "by_my_right_hand",   False),
    (8,  "out_of_the_pit",     False),
    (9,  "clean_heart",        False),
    (10, "still_waters",      True),
]


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed:\n" + " ".join(cmd[:6]) + "\n" + p.stderr[-1500:])
    return p


def find(raw, n, slug, suffix=""):
    stem = f"{n:02d}_{slug}{suffix}"
    for ext in (".wav", ".flac", ".mp3", ".m4a"):
        p = os.path.join(raw, stem + ext)
        if os.path.exists(p):
            return p
    return None


def duration(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", path], capture_output=True, text=True)
    return float(json.loads(p.stdout)["format"]["duration"])


def crop(src, dst, length):
    """Trim to exactly `length` from the start, padding with silence if short."""
    run(["ffmpeg", "-y", "-i", src, "-t", f"{length}",
         "-af", f"apad=whole_dur={length},aresample=48000",
         "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", dst])


def build_3015(mix, drums, bass, dst, tmp):
    """30s of full mix, then 15s of the song's own drums and bass. x4 = 3:00."""
    parts = []
    t = 0.0
    i = 0
    while t < SONG_LEN - 0.001:
        seg = os.path.join(tmp, f"seg_{os.path.basename(dst)}_{i}.wav")
        if i % 2 == 0:                                    # play block
            ln = min(PLAY, SONG_LEN - t)
            run(["ffmpeg", "-y", "-ss", f"{t}", "-t", f"{ln}", "-i", mix,
                 "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", seg])
        else:                                             # rest block: drums + bass
            ln = min(REST, SONG_LEN - t)
            run(["ffmpeg", "-y", "-ss", f"{t}", "-t", f"{ln}", "-i", drums,
                 "-ss", f"{t}", "-t", f"{ln}", "-i", bass,
                 "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0[a]",
                 "-map", "[a]", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", seg])
        parts.append(seg)
        t += ln
        i += 1
    return concat(parts, dst, tmp)


def concat(parts, dst, tmp):
    lst = os.path.join(tmp, "list_" + os.path.basename(dst) + ".txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c:a", "pcm_s24le", "-ac", "2", "-ar", "48000", dst])
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="./raw")
    ap.add_argument("--out", default="./out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="pnp_")
    warnings, timeline = [], []

    bridge_src = find(args.raw, 11, "bridge")
    reprise_src = find(args.raw, 12, "reprise")
    if not bridge_src:
        sys.exit("Missing 11_bridge.* - the 1-minute drum break between every set.")
    if not reprise_src:
        sys.exit("Missing 12_reprise.* - the closing minute under the prayer.")

    bridge = crop(bridge_src, os.path.join(tmp, "bridge.wav"), BRIDGE_LEN) or os.path.join(tmp, "bridge.wav")
    crop(bridge_src, os.path.join(tmp, "bridge.wav"), BRIDGE_LEN)
    crop(reprise_src, os.path.join(tmp, "reprise.wav"), BRIDGE_LEN)

    sequence = []
    for n, slug, continuous in TRACKS:
        src = find(args.raw, n, slug)
        if not src:
            sys.exit(f"Missing track {n}: {n:02d}_{slug}.* in {args.raw}")
        print(f"[{n:02d}] {slug:22s} source {duration(src):6.1f}s", end="")

        cropped = os.path.join(tmp, f"{n:02d}_cropped.wav")
        crop(src, cropped, SONG_LEN)

        if continuous:
            final = cropped
            print("  -> continuous 3:00")
        else:
            drums = find(args.raw, n, slug, "_drums")
            bass = find(args.raw, n, slug, "_bass")
            if drums and bass:
                dcrop = os.path.join(tmp, f"{n:02d}_drums.wav")
                bcrop = os.path.join(tmp, f"{n:02d}_bass.wav")
                crop(drums, dcrop, SONG_LEN)
                crop(bass, bcrop, SONG_LEN)
                final = build_3015(cropped, dcrop, bcrop,
                                   os.path.join(tmp, f"{n:02d}_final.wav"), tmp)
                print("  -> 30/15 x4")
            else:
                final = cropped
                warnings.append(f"track {n} ({slug}): no drums/bass stems, left continuous")
                print("  -> continuous (STEMS MISSING)")

        sequence.append(final)
        timeline.append((slug, SONG_LEN))
        if n != 10:                                  # 9 bridges, none after the warm-down
            sequence.append(os.path.join(tmp, "bridge.wav"))
            timeline.append(("bridge", BRIDGE_LEN))

    sequence.append(os.path.join(tmp, "reprise.wav"))
    timeline.append(("reprise", BRIDGE_LEN))

    joined = concat(sequence, os.path.join(tmp, "joined.wav"), tmp)
    total = sum(d for _, d in timeline)
    print(f"\nTimeline {total/60:.2f} min across {len(timeline)} segments")

    wav = os.path.join(args.out, "praise-and-pump-master.wav")
    mp3 = os.path.join(args.out, "praise-and-pump-master.mp3")
    print("Normalising to -9 LUFS (two-pass)...")
    run(["ffmpeg", "-y", "-i", joined,
         "-af", f"loudnorm=I={TARGET_LUFS}:TP=-1.0:LRA=11",
         "-ac", "2", "-ar", "48000", "-c:a", "pcm_s24le", wav])
    run(["ffmpeg", "-y", "-i", wav, "-b:a", "320k", mp3])

    print(f"\nWAV {wav}  ({duration(wav)/60:.2f} min)")
    print(f"MP3 {mp3}")
    if warnings:
        print("\nWARNINGS - these tracks did not get the 30/15 pattern Bear asked for:")
        for w in warnings:
            print("  -", w)


if __name__ == "__main__":
    main()
