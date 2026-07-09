#!/bin/bash
# Assemble the Harborview / Ted's Health white-label walkthrough.
set -e
cd "$(dirname "$0")"
mkdir -p scenes
SCENES=(01-intro 02-whitelabel 03-quiz 04-results 05-bloods 06-bloodreview 07-portal 08-close)
LAST=08-close
> concat.txt
for id in "${SCENES[@]}"; do
  clip="clips/${id}.webm"; vo="audio/${id}.ogg"; cap="captions/${id}.png"; out="scenes/${id}.mp4"
  [ -f "$clip" ] || { echo "MISSING $clip"; exit 1; }
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$vo")
  target=$(python3 -c "print(round(${vd}+0.7,2))")
  fade=""
  [ "$id" = "01-intro" ] && fade=",fade=t=in:st=0:d=0.6"
  [ "$id" = "$LAST" ] && fade=",fade=t=out:st=$(python3 -c "print(round(${target}-0.8,2))"):d=0.8"
  echo "-> $id  vo=${vd}s  target=${target}s"
  ffmpeg -y -loglevel error -ss 0.4 -i "$clip" -i "$vo" -i "$cap" -filter_complex \
    "[0:v]scale=1600:900:force_original_aspect_ratio=decrease,pad=1600:900:(ow-iw)/2:(oh-ih)/2:color=white,fps=30,tpad=stop_mode=clone:stop_duration=600[bg];[bg][2:v]overlay=0:0${fade},format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$target" -r 30 -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 "$out"
  echo "file '$(pwd)/$out'" >> concat.txt
done
echo "=== concat ==="
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy -movflags +faststart harborview-walkthrough.mp4
echo "DONE $(ffprobe -v error -show_entries format=duration -of csv=p=0 harborview-walkthrough.mp4)s"
ls -lh harborview-walkthrough.mp4 | awk '{print $5}'
