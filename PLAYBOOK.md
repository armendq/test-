# Studio playbook

How to build and post one concise vertical film for each series. A fresh session follows this file from top to bottom. Read `STATE.md` first. It says which episode is next.

## The two series

| | Where It Goes | The Night Bus |
|---|---|---|
| Brand | CutSignal HQ (`cutsignalhq`) | Talewend (`tale.wend`) |
| Metricool blogId | `6535620` | `8346815` |
| Premise | Second person. "You did X. Here is where it went." One hero object with a face rides through the real system behind an everyday act. Ends on a human payoff and a question. | Wordless night bus. Otto the badger driver takes one odd passenger home per episode. Ends on a cliffhanger and a three-option vote for the next passenger. |
| Facts | Every number on screen comes from a named source found in this run. Sources go on screen and in the caption. | None. Pure story. |
| Look | Bright, bold caption blocks (`caption()` in `engine/lib.py`), cream and gold on ink. | Navy night palette, serif captions (`cap2()` in `nightbus/base.py`). |
| Catchphrase | Opening block: the specific surprising destination or problem, visible from frame 0. | "Every passenger gets home." near the end. |

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

1. Make an isolated work folder. For an existing episode use `python engine/prepare.py <whereitgoes|nightbus> <episode-number> <work-folder>`. This copies the matching dependencies, including `engine/edit.py`. For a new episode create its source folder first. Never render in or overwrite another run's folder.
2. Where It Goes only: research. Two or three web searches. At least two named sources. Every number in the film must appear in a source. Prefer the newest report.
3. Write `scenes.py`. Use the latest episode of the same series as the model for structure and helper use. Export `SCENES` and `draw(c, g, f)`.
4. Review stills: `python3 make.py still 0,2.5,5,8,11,14,17,20,23,26,29 4 sheet.jpg`, then read the image. Fix and repeat. At least two rounds.
5. Write `audio.py`. Copy the latest `audio.py` of the same series. Keep the helpers and the music. Rewrite the sound effect timeline to match the new scene times.
6. Render and mux:

```bash
python3 audio.py && python3 make.py render
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v copy -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 192k -ar 44100 -shortest -movflags +faststart final.mp4
```

7. Check the result. Duration matches `scenes.DURATION` (30 s if absent), exactly `round(duration * 30)` video frames, matching audio, loudness near -15 LUFS, no black frames, then one full contact sheet:

```bash
ffprobe -v error -show_entries format=duration:stream=nb_frames -of default=nw=1 final.mp4
ffmpeg -v info -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
ffmpeg -v info -i final.mp4 -vf "blackdetect=d=0.1:pix_th=0.06" -an -f null - 2>&1 | grep -c black_start
ffmpeg -v error -y -i final.mp4 -vf "fps=2,scale=180:320,tile=10x6" -frames:v 1 -q:v 3 sheet_all.jpg
```

8. Web copy for hosting (inspect the encoded copy for compression damage):

```bash
ffmpeg -v error -y -i video.mp4 -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 1 -passlogfile p -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v libx264 -preset veryslow -tune animation -b:v 1000k -maxrate 2200k -bufsize 5000k -pass 2 -passlogfile p -pix_fmt yuv420p -af "loudnorm=I=-15:TP=-1.5:LRA=11" -c:a aac -b:a 128k -ar 44100 -shortest -movflags +faststart web.mp4
```

If any check fails and you cannot fix it, do not post. Report what failed.

## Film rules

- 1080 x 1920, 30 fps. Start with the established 30-second format, then cut repeated setup and empty holds. The November 27 revisions run 22.6 to 25 seconds. Length serves the story; it is not an algorithm requirement. Declare `DURATION` for a shorter cut and check picture and audio against it.
- The first frame carries the hook: the hero in close-up plus the opening caption. No title card.
- Keep faces, action and labels inside x 60 to 960 and y 250 to 1500. The apps cover the rest.
- Captions sit near y 215 to 300. Nothing else may sit under them. One idea per caption. Six words or fewer when possible.
- Wordless apart from captions. No voice.
- Give every beat motion: a walk, a pop, a count, a camera push. No frame should hold still for more than a second.
- Deliver the promised answer or completed passenger story before the final prompt. Use one specific question if it fits. Keep the closing prompt brief; do not withhold the answer for comments.
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

Notes: TikTok needs `title`. Where It Goes uses category `ENTERTAINMENT` and tags like `#whereitgoes`. The Night Bus uses `FILM_ANIMATION` and `#nightbus #animation #cozy`. The Night Bus caption invites a choice for a future ride. Do not promise a vote will decide an episode already built or scheduled. Record actual votes before claiming a winner.

4. Send the finished file to the user with a one-line caption.
5. Update `STATE.md`: episode log line, the vote options, any numbers you read. Commit and push the `studio` branch together with the new `scenes.py` and `audio.py` in `series/epNN/`.

## Opening and pacing rules (revised 2026-11-26)

Read `audit/2026-11-26-retention-review.md` for qualified conclusions and official sources. Observed values live in the private Posting project, never in this repository. A plateau near 1,000 views is not evidence of a fixed view cap. Opening choice, continued watching and satisfaction all matter. The averages do not reveal the exact drop-off second. These edits are hypotheses, not proven causes.

1. Frame 0 shows a large, legible subject and the specific problem or surprising destination. A frightened face alone is not the hook. Use emotion appropriate to the scene, not mandatory fear on every object.
2. Put the opening words on frame 0, without a fade. Prefer one short sentence. Do not begin every CutSignal episode with the generic series question. Keep series branding and episode numbers after the title's specific promise.
3. Show meaningful action immediately. Frame the subject tightly enough to read on a phone without cropping the relevant threat, clue or destination. No mandatory zoom factor.
4. Cut repeated setup. Begin a useful explanation or causal story beat within the first few seconds. For The Night Bus, identify this episode's passenger and problem without requiring knowledge of the last cliffhanger.
5. Give each shot a purpose: new information, an action, a consequence or a payoff. Do not impose uniform 4.4-second shots. Hold long enough to read, then move on. A bobbing character is not a new story beat.
6. Review frame 0, 0.5 and 1 second at phone size, then every scene boundary and the full film. Confirm the title's promise resolves within the film. Keep Otto's continuity and the next cliffhanger intact.
7. For revisions using `EDIT`, each tuple is `(output_seconds, source_start, source_end)` and stays inside one source scene. `edited_draw` and `edited_audio` share this list. The sound is time-stretched with pitch preserved. Copy `edit.py` when preparing a film. Never trim picture while leaving the old audio timeline.
8. Research each quantitative claim with its year, geography, unit and denominator. Sales value is not order count. An estimate is not a measured result. A retailer's returns policy is not a universal grading system. Save primary-source URLs with the episode caption or audit.

## Keep the catalogue alive (added 2026-11-26)

- Lead the caption with the specific promise. Use a natural, relevant send line only where useful. Do not treat share requests, tags or posting times as distribution switches.
- The Night Bus: put the specific story hook first and the episode number at the end of the title. The caption carries the episode number. The caption names the previous episode in one short line ("Episode 2: the fox cub.").
- Never delete a stalled video. Never upload the same file twice.
- Chat check-ins with the server browser (CutSignal HQ only, the browser holds no Talewend login): after each CutSignal film goes live, post one question comment under it on YouTube with a sourced fact from the film, add it to the public playlist "Where It Goes", and reply to every viewer comment with a heart.
- Blocked on 2026-11-26: related-video links and pinned comments on CutSignal HQ YouTube need channel verification (selfie video or ID). The browser showed "Video verification in review" on November 26 evening. Check the actual status before adding related videos. Do not promise an unlock date or request another identity submission while review is pending.

## Voice and audience (owner decision, 2026-11-27)

The owner asked the chat session to decide the direction toward reach and profit. Decisions:

1. Every film carries a spoken voice-over from the first frame. Caption-only openings did not hold viewers.
2. Voice engine: Kokoro (open source, free), `engine/narrate.py`. Where It Goes uses voice `af_heart` at speed 1.1. The Night Bus uses `af_bella` at speed 0.95 (calm). Write `narr.json` in the film folder: a list of `{"t": seconds, "text": "..."}`. Lines start with the matching caption. Spell numbers as words ("a hundred and eight", "sixty-nine percent"). `narrate.py` speeds a line up to 1.35 to fit its slot and reports anything still over. Keep bedtime lines at or below speed 1.15 by shortening the text. Then `bash engine/vobuild.sh <name>_vo` inside the film folder: it reuses `video.mp4`, ducks the music and effects about 10 dB under the voice, normalizes to -15 LUFS and writes the two-pass `web.mp4`.
3. Where It Goes opens on the spoken surprise ("This bottle was at sea for a hundred and eight years."). Topics: famous places and useful seasonal stories first. Everyday objects come later.
4. The Night Bus is children's bedtime content. Set YouTube `madeForKids: true` on every Night Bus post (YouTube guidance: stories and animated characters aimed at children make content "made for kids", and the creator carries the legal duty). Comments are off on YouTube for these, so the guess invitation lives on Instagram and TikTok.
5. No new channels for now. A new channel restarts at the same first-test audience with no history.
6. No paid video tool yet. Decision point 2026-12-02: compare the narrated films' 48-hour retention with the best silent film (numbers live in the private Posting project, never in this repository). If they do not beat it, recommend the owner buy a Runway plan for realistic opening shots. Never buy anything from a run.
7. One film per brand per day from 2026-11-29: Where It Goes at 19:00, The Night Bus at 23:00 (Europe/Budapest). Each film changes one thing and gets judged at 48 hours.

## Known pitfalls

- `make.py` imports `scenes.draw` and uses `scenes.DURATION` when present. Run it from the work folder.
- `caption()` shrinks long lines to fit. Keep lines short so they stay large.
- A world transform that shifts the scene leaves unpainted bands. Paint the full frame first.
- Things that pass under a caption or the source strip read as clutter. Move them.
- The Night Bus interior helpers live in `nightbus/base.py` (`bus_int_back`, `otto_full`, `bus_ext`, `snail`). Episode 2 adds `fox`, `rear`, `bench`, `kid_drawing`, `country`, `hill`, `road`, `driver`. Reuse them.
- Episode 3 scripts import earlier episodes. Where It Goes: copy `whereitgoes/ep02/scenes.py` into the work folder as `base2.py` (`bag`, `belt`, `boh`, `hall`, `tag_card`), and `whereitgoes/ep03/scenes.py` adds `env`, `street`, `mailbox`, `stream`, `monitor`, `granny`. The Night Bus: copy `nightbus/base.py` as `base.py` and `nightbus/ep02/scenes.py` as `ep2.py`, and `nightbus/ep03/scenes.py` adds `owl`, `feather`, `tree_card`, `souvenirs`, `ladder`, `tree`. A new episode starts with `from ep2 import *` or `from base2 import *` and copies the helpers it needs.
- Build time in the chat session: about 35 minutes per film, most of it scene writing and one round of contact-sheet fixes.
- TikTok `@cutsignalhq` gets almost no plays. The owner removed TikTok from the CutSignal post for 2026-11-26 06:00. CutSignal HQ posts go to Instagram and YouTube only: providers `instagram` and `youtube`, no `tiktokData`. Talewend posts keep all three networks.
