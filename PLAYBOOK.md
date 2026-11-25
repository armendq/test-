# Studio playbook

How to build and post one 30 second vertical film for each series. A fresh session follows this file from top to bottom. Read `STATE.md` first. It says which episode is next.

## The two series

| | Where It Goes | The Night Bus |
|---|---|---|
| Brand | CutSignal HQ (`cutsignalhq`) | Talewend (`tale.wend`) |
| Metricool blogId | `6535620` | `8346815` |
| Premise | Second person. "You did X. Here is where it went." One hero object with a face rides through the real system behind an everyday act. Ends on a human payoff and a question. | Wordless night bus. Otto the badger driver takes one odd passenger home per episode. Ends on a cliffhanger and a three-option vote for the next passenger. |
| Facts | Every number on screen comes from a named source found in this run. Sources go on screen and in the caption. | None. Pure story. |
| Look | Bright, bold caption blocks (`caption()` in `engine/lib.py`), cream and gold on ink. | Navy night palette, serif captions (`cap2()` in `nightbus/base.py`). |
| Catchphrase | Opening block: "WHERE DOES YOUR <THING> GO?" | "Every passenger gets home." near the end. |

Never post the same video on both brands.

## Setup

```bash
python3 -c "import cairocffi" || pip install cairocffi --break-system-packages
fc-list | grep -c -E "Archivo Black|Comic Relief|Crimson Text|DM Sans"   # must be above 0
git clone --depth 1 --branch studio https://github.com/armendq/test- studio
git clone --depth 1 --branch media  https://github.com/armendq/test- media
```

The repository needs push access in the session (`armendq/test-`). Add it first if the session does not have it.

## Build one episode

1. Make a work folder. Copy `engine/lib.py` and `engine/make.py` into it. For The Night Bus also copy `nightbus/base.py`.
2. Where It Goes only: research. Two or three web searches. At least two named sources. Every number in the film must appear in a source. Prefer the newest report.
3. Write `scenes.py`. Use the latest episode of the same series as the model for structure and helper use. Export `SCENES` and `draw(c, g, f)`.
4. Review stills: `python3 make.py still 0,2.5,5,8,11,14,17,20,23,26,29 4 sheet.jpg`, then read the image. Fix and repeat. At least two rounds.
5. Write `audio.py`. Copy the latest `audio.py` of the same series. Keep the helpers and the music. Rewrite the sound effect timeline to match the new scene times.
6. Render and mux:

```bash
python3 audio.py && python3 make.py render
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v copy -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart final.mp4
```

7. Check the result. Duration 30.000 s, 900 frames, loudness near -15 LUFS, no black frames, then one full contact sheet:

```bash
ffprobe -v error -show_entries format=duration:stream=nb_frames -of default=nw=1 final.mp4
ffmpeg -v info -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
ffmpeg -v info -i final.mp4 -vf "blackdetect=d=0.1:pix_th=0.06" -an -f null - 2>&1 | grep -c black_start
ffmpeg -v error -y -i final.mp4 -vf "fps=2,scale=180:320,tile=10x6" -frames:v 1 -q:v 3 sheet_all.jpg
```

8. Web copy for hosting (about 4 MB, visually identical):

```bash
ffmpeg -v error -y -i video.mp4 -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 1 -passlogfile p -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 2 -passlogfile p -pix_fmt yuv420p -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart web.mp4
```

If any check fails and you cannot fix it, do not post. Report what failed.

## Film rules

- 1080 x 1920, 30 fps, exactly 30 s, six or seven scenes.
- The first frame carries the hook: the hero in close-up plus the opening caption. No title card.
- Keep faces, action and labels inside x 60 to 960 and y 250 to 1500. The apps cover the rest.
- Captions sit near y 215 to 300. Nothing else may sit under them. One idea per caption. Six words or fewer when possible.
- Wordless apart from captions. No voice.
- Give every beat motion: a walk, a pop, a count, a camera push. No frame should hold still for more than a second.
- End with a question the viewer wants to answer in a comment.
- Characters keep their look: Otto (badger, blue uniform, cap), the hero object of Where It Goes always has a simple face.
- No real people, no brand logos, no known characters, no song lyrics.
- Sound: every visible event gets a small sound. Music ducks or stops for the cliffhanger.

## Publish

1. Copy `web.mp4` into the `media` clone as `media/<series>_epNN_<slug>.mp4`, commit, `git push origin media`.
2. Public link: `https://raw.githubusercontent.com/armendq/test-/media/media/<file>.mp4`
3. Schedule with the Metricool connector, tool `createScheduledPost`. Date must lie in the future. Use the slot given in the task prompt. Timezone `Europe/Budapest`. The `date` argument takes the same time with its offset, for example `2026-11-26T13:00:00+01:00`.

`info` template (fill the capitals):

```json
{"autoPublish": true, "descendants": [], "draft": false, "firstCommentText": "", "hasNotReadNotes": false,
 "media": ["PUBLIC_LINK"], "mediaAltText": [],
 "providers": [{"network": "instagram"}, {"network": "tiktok"}, {"network": "youtube"}],
 "publicationDate": {"dateTime": "YYYY-MM-DDTHH:MM:00", "timezone": "Europe/Budapest"},
 "shortener": false, "smartLinkData": {"ids": []},
 "text": "CAPTION\n\nSOURCES_LINE_FOR_WHERE_IT_GOES\n\n#tag1 #tag2 #tag3",
 "instagramData": {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": false},
 "tiktokData": {"disableComment": false, "disableDuet": false, "disableStitch": false, "privacyOption": "PUBLIC_TO_EVERYONE",
                "commercialContentThirdParty": false, "commercialContentOwnBrand": false, "title": "SHORT_TITLE", "autoAddMusic": false, "isAigc": true},
 "youtubeData": {"title": "TITLE_UNDER_100_CHARS", "type": "short", "privacy": "public", "tags": ["a", "b", "c"],
                 "category": "ENTERTAINMENT_OR_FILM_ANIMATION", "madeForKids": false, "isAiGeneratedContent": false}}
```

Notes: TikTok needs `title`. Where It Goes uses category `ENTERTAINMENT` and tags like `#whereitgoes`. The Night Bus uses `FILM_ANIMATION` and `#nightbus #animation #cozy`. The Night Bus caption ends with the vote: "Vote in the comments. The winner rides soon."

4. Send the finished file to the user with a one-line caption.
5. Update `STATE.md`: episode log line, the vote options, any numbers you read. Commit and push the `studio` branch together with the new `scenes.py` and `audio.py` in `series/epNN/`.

## Known pitfalls

- `make.py` imports `scenes.draw`. Run it from the work folder.
- `caption()` shrinks long lines to fit. Keep lines short so they stay large.
- A world transform that shifts the scene leaves unpainted bands. Paint the full frame first.
- Things that pass under a caption or the source strip read as clutter. Move them.
- The Night Bus interior helpers live in `nightbus/base.py` (`bus_int_back`, `otto_full`, `bus_ext`, `snail`). Episode 2 adds `fox`, `rear`, `bench`, `kid_drawing`, `country`, `hill`, `road`, `driver`. Reuse them.
- Episode 3 scripts import earlier episodes. Where It Goes: copy `whereitgoes/ep02/scenes.py` into the work folder as `base2.py` (`bag`, `belt`, `boh`, `hall`, `tag_card`), and `whereitgoes/ep03/scenes.py` adds `env`, `street`, `mailbox`, `stream`, `monitor`, `granny`. The Night Bus: copy `nightbus/base.py` as `base.py` and `nightbus/ep02/scenes.py` as `ep2.py`, and `nightbus/ep03/scenes.py` adds `owl`, `feather`, `tree_card`, `souvenirs`, `ladder`, `tree`. A new episode starts with `from ep2 import *` or `from base2 import *` and copies the helpers it needs.
- Build time in the chat session: about 35 minutes per film, most of it scene writing and one round of contact-sheet fixes.
- TikTok `@cutsignalhq` gets almost no reach. Post there anyway. Do not spend time on it.
