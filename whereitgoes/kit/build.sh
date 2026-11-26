#!/bin/bash
# usage: build.sh <name>   (run inside the film folder; needs scenes.py and audio.py)
set -e
N=$1
python3 audio.py
python3 make.py render > render.log 2>&1 || { tail -5 render.log; exit 1; }
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v copy -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart $N.mp4
ffprobe -v error -show_entries format=duration:stream=nb_frames -of csv=p=0 $N.mp4 | tr '\n' ' '
ffmpeg -v info -i $N.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:" | tail -1
echo "black: $(ffmpeg -v info -i $N.mp4 -vf "blackdetect=d=0.1:pix_th=0.06" -an -f null - 2>&1 | grep -c black_start)"
ffmpeg -v error -y -i $N.mp4 -vf "fps=1,scale=180:320,tile=10x3" -frames:v 1 -q:v 3 sheet_all.jpg
rm -f p-0*
ffmpeg -v error -y -i video.mp4 -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 1 -passlogfile p -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 2 -passlogfile p -pix_fmt yuv420p -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart web.mp4
cp web.mp4 /home/claude/test-/media/$N.mp4; cp $N.mp4 /mnt/user-data/outputs/$N.mp4
ls -la web.mp4 | awk '{print "web bytes:", $5}'
