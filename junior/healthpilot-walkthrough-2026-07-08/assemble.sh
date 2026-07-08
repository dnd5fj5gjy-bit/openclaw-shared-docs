#!/bin/bash
# Assemble the HealthPilot white-label walkthrough: per-scene video fitted to its
# voiceover, lower-third caption, then concatenated into one mp4.
set -e
cd "$(dirname "$0")"

FONT="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
[ -f "$FONT" ] || FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
[ -f "$FONT" ] || FONT="/System/Library/Fonts/Helvetica.ttc"
echo "font: $FONT"

mkdir -p scenes captions
# scene id | caption
SCENES=(
  "01-landing|HealthPilot  -  the white-label health platform"
  "02-intake|Guided patient intake  -  premium on every screen"
  "03-whitelabel|Live white-label theming  -  one platform, any brand"
  "04-owner|Clinic owner console  -  fully self-serve"
  "05-close|HealthPilot  x  Ted's Health"
)

> concat.txt
i=0
for entry in "${SCENES[@]}"; do
  id="${entry%%|*}"; cap="${entry#*|}"
  clip="clips/${id}.webm"; vo="audio/${id}.ogg"; out="scenes/${id}.mp4"
  capfile="captions/${id}.txt"; printf '%s' "$cap" > "$capfile"

  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  target=$(python3 -c "print(round(${vd}+0.8,2))")

  # fade in on first scene, fade out on last
  fade=""
  [ "$id" = "01-landing" ] && fade=",fade=t=in:st=0:d=0.5"
  [ "$id" = "05-close" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.7,2))"):d=0.7"

  echo "-> $id  vo=${vd}s target=${target}s"
  ffmpeg -y -loglevel error -i "$clip" -i "$vo" -filter_complex \
    "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600,drawtext=fontfile='${FONT}':textfile='${capfile}':fontcolor=white:fontsize=30:box=1:boxcolor=0x0f2a28@0.55:boxborderw=18:x=70:y=h-120${fade},format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$target" -r 30 \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
    -c:a aac -b:a 160k -ar 48000 "$out"
  echo "file '$(pwd)/$out'" >> concat.txt
done

echo "=== concat ==="
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy -movflags +faststart healthpilot-walkthrough.mp4
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 healthpilot-walkthrough.mp4)
echo "DONE: healthpilot-walkthrough.mp4  (${dur}s)"
ls -lh healthpilot-walkthrough.mp4
