#!/bin/bash
# usage: vobuild.sh <name_vo>  (run inside the film folder after narrate.py; reuses video.mp4)
set -e
N=$1
ffmpeg -v error -y -i video.mp4 -i mix.wav -c:v copy -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart $N.mp4
rm -f p-0*
ffmpeg -v error -y -i video.mp4 -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 1 -passlogfile p -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i video.mp4 -i mix.wav -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 2 -passlogfile p -pix_fmt yuv420p -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart web.mp4
echo "copy web.mp4 to the media clone as media/$N.mp4"
ls -la web.mp4 | awk '{print "web bytes:", $5}'
