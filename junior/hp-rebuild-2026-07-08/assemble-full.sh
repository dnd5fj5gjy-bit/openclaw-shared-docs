#!/bin/bash
# Comprehensive HealthPilot walkthrough: white-label + health quiz + value narration.
set -e
cd "$(dirname "$0")"
python3 make_captions_full.py
mkdir -p scenes-full
SCENES=(01-frontdoor 12-studio 09-rebrand 13-quizflow 04-upsell 03-wearables 07-escalations 06-analytics 10-owner 11-close)
LAST=11-close
skip_for(){ case "$1" in 04-upsell) echo 4;; 06-analytics) echo 9;; 07-escalations) echo 9;; 10-owner) echo 6;; *) echo 0;; esac; }
> concat-full.txt
for id in "${SCENES[@]}"; do
  clip="clips/${id}.webm"; vo="audio-full/${id}.ogg"; cap="captions-full/${id}.png"; out="scenes-full/${id}.mp4"
  [ -f "$clip" ] || { echo "MISSING $clip"; continue; }
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  target=$(python3 -c "print(round(${vd}+0.75,2))")
  skip=$(skip_for "$id")
  fade=""
  [ "$id" = "01-frontdoor" ] && fade=",fade=t=in:st=0:d=0.5"
  [ "$id" = "$LAST" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.7,2))"):d=0.7"
  echo "-> $id vo=${vd}s target=${target}s skip=${skip}s"
  ffmpeg -y -loglevel error -ss "$skip" -i "$clip" -i "$vo" -i "$cap" -filter_complex \
    "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600[bg];[bg][2:v]overlay=0:0${fade},format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$target" -r 30 \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 "$out"
  echo "file '$(pwd)/$out'" >> concat-full.txt
done
echo "=== concat ==="
ffmpeg -y -loglevel error -f concat -safe 0 -i concat-full.txt -c copy -movflags +faststart healthpilot-full-walkthrough.mp4
echo "DONE $(ffprobe -v error -show_entries format=duration -of csv=p=0 healthpilot-full-walkthrough.mp4)s"
ls -lh healthpilot-full-walkthrough.mp4 | awk '{print $5}'
