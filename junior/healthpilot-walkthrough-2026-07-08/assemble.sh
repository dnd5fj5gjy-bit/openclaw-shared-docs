#!/bin/bash
# Assemble the HealthPilot white-label walkthrough: per-scene video fitted to its
# voiceover, PNG lower-third caption overlay, then concatenated into one mp4.
set -e
cd "$(dirname "$0")"

python3 make_captions.py
mkdir -p scenes

SCENES=(01-landing 02-intake 03-whitelabel 04-owner 05-close)

> concat.txt
for id in "${SCENES[@]}"; do
  clip="clips/${id}.webm"; vo="audio/${id}.ogg"; cap="captions/${id}.png"; out="scenes/${id}.mp4"

  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  target=$(python3 -c "print(round(${vd}+0.8,2))")

  # fade in on first scene, fade out on last
  fade=""
  [ "$id" = "01-landing" ] && fade=",fade=t=in:st=0:d=0.5"
  [ "$id" = "05-close" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.7,2))"):d=0.7"

  echo "-> $id  vo=${vd}s target=${target}s"
  ffmpeg -y -loglevel error -i "$clip" -i "$vo" -i "$cap" -filter_complex \
    "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600[bg];[bg][2:v]overlay=0:0${fade},format=yuv420p[v]" \
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
