#!/bin/bash
# Fully-updated comprehensive walkthrough: white-label + quiz (slow) + results +
# supplements + prescribing value + the rest, with value narration.
set -e
cd "$(dirname "$0")"
python3 make_captions_v2.py
mkdir -p scenes-v2
SCENES=(01-frontdoor 12-studio 09-rebrand 16-quizslow 14-results 15-supplements clinicalvalue 04-upsell 03-wearables 07-escalations 06-analytics 10-owner 11-close)
LAST=11-close
QUIZDUR=52
skip_for(){ case "$1" in 04-upsell) echo 4;; 06-analytics) echo 9;; 07-escalations) echo 9;; 10-owner) echo 6;; *) echo 0;; esac; }
> concat-v2.txt
for id in "${SCENES[@]}"; do
  clip="clips/${id}.webm"; vo="audio-v2/${id}.ogg"; cap="captions-v2/${id}.png"; out="scenes-v2/${id}.mp4"
  [ -f "$clip" ] || { echo "MISSING $clip"; continue; }
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  if [ "$id" = "16-quizslow" ]; then target=$QUIZDUR; else target=$(python3 -c "print(round(${vd}+0.75,2))"); fi
  skip=$(skip_for "$id")
  fade=""
  [ "$id" = "01-frontdoor" ] && fade=",fade=t=in:st=0:d=0.5"
  [ "$id" = "$LAST" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.7,2))"):d=0.7"
  echo "-> $id vo=${vd}s target=${target}s skip=${skip}s cap=$([ -f "$cap" ] && echo y || echo n)"
  if [ -f "$cap" ]; then
    ffmpeg -y -loglevel error -ss "$skip" -i "$clip" -i "$vo" -i "$cap" -filter_complex \
      "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600[bg];[bg][2:v]overlay=0:0${fade},format=yuv420p[v]" \
      -map "[v]" -map 1:a -t "$target" -r 30 -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 "$out"
  else
    ffmpeg -y -loglevel error -ss "$skip" -i "$clip" -i "$vo" -filter_complex \
      "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600${fade},format=yuv420p[v]" \
      -map "[v]" -map 1:a -t "$target" -r 30 -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 "$out"
  fi
  echo "file '$(pwd)/$out'" >> concat-v2.txt
done
echo "=== concat ==="
ffmpeg -y -loglevel error -f concat -safe 0 -i concat-v2.txt -c copy -movflags +faststart healthpilot-full-walkthrough-v2.mp4
echo "DONE $(ffprobe -v error -show_entries format=duration -of csv=p=0 healthpilot-full-walkthrough-v2.mp4)s"
ls -lh healthpilot-full-walkthrough-v2.mp4 | awk '{print $5}'
