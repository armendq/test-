#!/bin/bash
# usage: lfbuild.sh <name> [video_kbps]
# Run inside a long-form folder after make.py (STUDIO_W=1920 STUDIO_H=1080) and narrate.py: needs video.mp4 and mix.wav.
# Writes <name>.mp4: 16:9 YouTube long-form, two-pass x264 veryfast, AAC 96k, -15 LUFS.
# Fails if the file reaches 95 MB, the limit for the media branch. Rerun with a lower video_kbps.
set -e
N=$1; VB=${2:-800}
rm -f lf-0*
ffmpeg -v error -y -i video.mp4 -c:v libx264 -preset veryfast -tune animation -b:v ${VB}k -maxrate $((VB * 2))k -bufsize $((VB * 4))k -pass 1 -passlogfile lf -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i video.mp4 -i mix.wav -c:v libx264 -preset veryfast -tune animation -b:v ${VB}k -maxrate $((VB * 2))k -bufsize $((VB * 4))k -pass 2 -passlogfile lf -pix_fmt yuv420p -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 96k -ar 44100 -shortest -movflags +faststart "$N.mp4"
rm -f lf-0*
B=$(stat -c %s "$N.mp4")
echo "bytes: $B"
if [ "$B" -ge 99614720 ]; then echo "OVER 95 MB: rerun with a lower video_kbps"; exit 1; fi
echo "copy $N.mp4 to the media clone as media/$N.mp4"
