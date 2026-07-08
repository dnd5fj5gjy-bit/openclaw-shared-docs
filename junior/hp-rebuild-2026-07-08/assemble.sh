#!/bin/bash
# Assemble the comprehensive HealthPilot x Ted's white-label walkthrough.
set -e
cd "$(dirname "$0")"
python3 make_captions.py
mkdir -p scenes
SCENES=(01-frontdoor 02-quiz 03-wearables 04-upsell 05-history 06-analytics 07-escalations 08-customise 09-rebrand 10-owner 11-close)
LAST=11-close
> concat.txt
for id in "${SCENES[@]}"; do
  clip="clips/${id}.webm"; vo="audio/${id}.ogg"; cap="captions/${id}.png"; out="scenes/${id}.mp4"
  [ -f "$clip" ] || { echo "MISSING clip $clip - skipping"; continue; }
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  target=$(python3 -c "print(round(${vd}+0.75,2))")
  fade=""
  [ "$id" = "01-frontdoor" ] && fade=",fade=t=in:st=0:d=0.5"
  [ "$id" = "$LAST" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.7,2))"):d=0.7"
  echo "-> $id vo=${vd}s target=${target}s"
  ffmpeg -y -loglevel error -i "$clip" -i "$vo" -i "$cap" -filter_complex \
    "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600[bg];[bg][2:v]overlay=0:0${fade},format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$target" -r 30 \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 "$out"
  echo "file '$(pwd)/$out'" >> concat.txt
done
echo "=== concat ==="
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy -movflags +faststart healthpilot-integrated-walkthrough.mp4
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 healthpilot-integrated-walkthrough.mp4)
echo "DONE ${dur}s"; ls -lh healthpilot-integrated-walkthrough.mp4
