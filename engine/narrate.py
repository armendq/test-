"""Add a voice-over to a rendered film.
usage: python3 narrate.py <film folder> <voice> <speed> <duration>
setup: pip install kokoro-onnx soundfile scipy --break-system-packages (model files download from GitHub on first run)
reads <folder>/narr.json: [{"t": start_seconds, "text": "..."}]
writes <folder>/voice.wav (diagnostic) and <folder>/mix.wav (bed ducked under the voice)"""
import sys, json, numpy as np, soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro
D, voice, speed, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
import os, urllib.request
C = os.path.expanduser("~/.cache/kokoro"); os.makedirs(C, exist_ok=True)
for fn in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
    if not os.path.exists(f"{C}/{fn}"):
        urllib.request.urlretrieve(f"https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{fn}", f"{C}/{fn}")
k = Kokoro(f"{C}/kokoro-v1.0.onnx", f"{C}/voices-v1.0.bin")
lines = json.load(open(f"{D}/narr.json"))
bed, sr = sf.read(f"{D}/audio.wav")
if bed.ndim == 1: bed = np.stack([bed, bed], 1)
NS = len(bed); vo = np.zeros(NS)
lang = "en-us" if voice[0] == "a" else "en-gb"
for i, L in enumerate(lines):
    t0 = L["t"]; nxt = lines[i + 1]["t"] if i + 1 < len(lines) else DUR - 0.25
    room = nxt - t0 - 0.1; sp = speed
    while True:
        s, vsr = k.create(L["text"], voice=voice, speed=sp, lang=lang)
        nz = np.where(np.abs(s) > 0.01)[0]
        s = s[max(0, nz[0] - 240): nz[-1] + 2400] if len(nz) else s
        d = len(s) / vsr
        if d <= room or sp >= 1.35: break
        sp = round(sp + 0.05, 2)
    s = resample_poly(s, sr, vsr)
    a = int(t0 * sr); b = min(NS, a + len(s)); vo[a:b] += s[:b - a]
    flag = "" if d <= room else "  OVER by %.2f s" % (d - room)
    print("%5.2f  %.2fs/%.2fs  speed %.2f  %s%s" % (t0, d, room, sp, L["text"], flag))
win = int(0.03 * sr)
env = np.convolve(np.abs(vo), np.ones(win) / win, mode="same")
act = (env > 0.01).astype(float)
att, rel = int(0.08 * sr), int(0.3 * sr)
sm = np.convolve(act, np.ones(rel) / rel, mode="same")
gain = 1.0 - 0.68 * np.clip(sm * 3, 0, 1)
bed_d = bed * gain[:, None]
m = act > 0.5
rb = np.sqrt(np.mean(bed_d[m] ** 2)) if m.any() else 0.05
rv = np.sqrt(np.mean(vo[m] ** 2)) if m.any() else 0.05
vo *= (rb * 3.4) / max(rv, 1e-6)
mix = bed_d + vo[:, None]
mix *= 0.95 / max(1e-6, np.abs(mix).max())
sf.write(f"{D}/voice.wav", vo, sr); sf.write(f"{D}/mix.wav", mix, sr)
print("mix ok", round(NS / sr, 3), "s")
