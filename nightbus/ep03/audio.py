import numpy as np, wave
SR = 44100; DUR = 30.0; NS = int(SR * DUR)
buf = np.zeros(NS + 2 * SR)


def add(x, t0, g=1.0):
    i = int(t0 * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(len(buf), i + len(x))
    if j > i: buf[i:j] += g * x[:j - i]


def tt(d): return np.arange(int(SR * d)) / SR
def hann(n): return np.hanning(n)
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)


def bnoise(d, lo, hi, seed):
    n = int(SR * d); r = np.random.default_rng(seed).standard_normal(n); F = np.fft.rfft(r); fr = np.fft.rfftfreq(n, 1 / SR)
    F[(fr < lo) | (fr > hi)] = 0; x = np.fft.irfft(F, n); return x / (np.max(np.abs(x)) + 1e-9)


def sweep(f0, f1, d, dec=0):
    t = tt(d); f = f0 + (f1 - f0) * t / d; ph = 2 * np.pi * np.cumsum(f) / SR; s = np.sin(ph) * hann(len(t))
    return s * np.exp(-t * dec) if dec else s


def vibe(freq, d=2.2, dec=2.4):
    t = tt(d); trem = 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)
    s = np.sin(2 * np.pi * freq * t) + 0.28 * np.sin(2 * np.pi * 4 * freq * t) * np.exp(-t * 9) + 0.12 * np.sin(2 * np.pi * 2 * freq * t)
    return s * trem * np.exp(-t * dec) * np.minimum(1, t / 0.006)


def bass(freq, d=1.3):
    t = tt(d); s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 5)
    return s * np.exp(-t * 2.2) * np.minimum(1, t / 0.012)


def hum(freq, d):
    t = tt(d); vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t); ph = 2 * np.pi * np.cumsum(freq * vib) / SR
    s = np.sin(ph) + 0.42 * np.sin(2 * ph) + 0.16 * np.sin(3 * ph)
    return s * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.06)


def env_seg(points):
    """piecewise-linear envelope over the whole clip from (time, gain) points"""
    ts = np.arange(NS) / SR
    return np.interp(ts, [p[0] for p in points], [p[1] for p in points])


# ---------------------------------------------------------------- beds
ts = np.arange(NS) / SR
rain_out = bnoise(DUR, 1800, 9500, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.23 * ts))
rain_in = bnoise(DUR, 250, 2600, 2) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.31 * ts + 1))
e_in = env_seg([(0, 1), (3.25, 1), (3.5, 0), (9.25, 0), (9.5, 1), (14.45, 1), (14.7, 0), (30, 0)])
e_out = env_seg([(0, 0), (3.25, 0), (3.5, 1), (9.25, 1), (9.5, 0), (14.45, 0), (14.7, 0.6), (20.9, 0.4), (21.1, 0.25), (25.9, 0.25), (26.1, 1), (30, 1)])
buf[:NS] += rain_out * e_out * 0.05 + rain_in * e_in * 0.065
f_eng = env_seg([(0, 62), (2.2, 62), (2.6, 42), (26.3, 42), (26.9, 60), (30, 74)])
g_eng = env_seg([(0, 0.08), (2.2, 0.08), (2.7, 0.03), (9.3, 0.03), (9.5, 0.02), (14.5, 0.02), (14.8, 0.0), (26.2, 0.0), (26.6, 0.07), (30, 0.09)])
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng

# ---------------------------------------------------------------- music: enters at the reveal
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
M0 = 6.3; MUSIC_END = 26.68
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (14.5, 0.8), (14.7, 0.9), (21, 0.95), (22.3, 1.1), (25.9, 1.0), (26.1, 0.6),
                  (MUSIC_END - 0.02, 0.6), (MUSIC_END, 0.0), (30, 0)])
mus = np.zeros(NS + 2 * SR)
def madd(x, t0, g):
    i = int(t0 * SR); j = min(len(mus), i + len(x))
    if i >= 0 and j > i: mus[i:j] += g * x[:j - i]
for bar in range(8):
    ch = CH[bar % 4]; t0 = M0 + bar * 4 * beat
    madd(bass(mtof(ch[0] - 12)), t0, 0.20); madd(bass(mtof(ch[0] - 12), 0.9), t0 + 2.5 * beat, 0.11)
    for e, k in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
        madd(vibe(mtof(ch[k] + 12), 1.6, 3.2), t0 + e * beat / 2, 0.05 * (1.2 if e % 4 == 0 else 0.85))
    d = 4 * beat; t = tt(d); env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    pad = sum(np.sin(2 * np.pi * mtof(n) * t) + 0.25 * np.sin(2 * np.pi * mtof(n + 12) * t) for n in ch)
    madd(pad * env, t0, 0.022)
for rep in range(3):
    for (b, n) in MEL:
        tm = M0 + rep * 12 * beat + b * beat
        if tm < MUSIC_END: madd(vibe(mtof(n), 2.4, 2.0), tm, 0.085)
buf[:NS] += mus[:NS] * m_gain

# ---------------------------------------------------------------- sfx helpers
def tick(t, f=2100, g=0.10): add(np.sin(2 * np.pi * f * tt(0.014)) * hann(int(SR * 0.014)), t, g)
def pop(t, f0=420, f1=900, g=0.14): add(sweep(f0, f1, 0.07), t, g)
def cap(t): add(sweep(520, 760, 0.06), t, 0.07)
def chime(t, n, g=0.12): add(vibe(mtof(n), 1.6, 3.0) + 0.5 * vibe(mtof(n + 7), 1.6, 3.4), t, g)
def step(t, g=0.16, seed=0):
    add(sweep(170, 70, 0.09, 18), t, g); add(bnoise(0.05, 300, 2500, 100 + seed) * np.exp(-tt(0.05) * 70), t, g * 0.35)
def knock(t, g=0.12, f0=520): add(sweep(f0, f0 * 0.6, 0.05, 30), t, g); add(bnoise(0.03, 600, 3000, int(t * 100)) * np.exp(-tt(0.03) * 90), t, g * 0.4)
def hiss(t, d=0.6, g=0.14, seed=5): add(bnoise(d, 2500, 10000, seed) * hann(int(SR * d)), t, g)
def thunk(t, g=0.3): add(sweep(130, 48, 0.16, 14), t, g); add(bnoise(0.04, 200, 1800, 77) * np.exp(-tt(0.04) * 80), t, g * 0.4)
def heartbeat(t, g=0.5):
    for dt, k in ((0, 1.0), (0.2, 0.7)):
        add(sweep(74, 38, 0.14, 12), t + dt, g * k); add(sweep(170, 95, 0.10, 16), t + dt, g * k * 0.45)
def creep(t0, d, g=0.10):
    q = tt(d)
    x = (np.sin(2 * np.pi * 61.7 * q) + 0.8 * np.sin(2 * np.pi * 65.4 * q) + 0.4 * np.sin(2 * np.pi * 185 * q)) * np.minimum(1, q / 0.4) * np.minimum(1, (d - q) / 0.08)
    add(x, t0, g)
def hoot(t, g=0.12, f0=392):
    for dt, d in ((0, 0.22), (0.3, 0.42)):
        q = tt(d); vib = 1 + 0.01 * np.sin(2 * np.pi * 6 * q)
        add((np.sin(2 * np.pi * np.cumsum(f0 * vib) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f0 * vib) / SR)) * hann(len(q)), t + dt, g)
def beep(t, g=0.13):
    d = 0.2; q = tt(d)
    add((np.sign(np.sin(2 * np.pi * 349 * q)) + np.sign(np.sin(2 * np.pi * 440 * q))) * 0.5 * np.minimum(1, q / 0.01) * np.minimum(1, (d - q) / 0.02), t, g)
def puff(t, g=0.08, seed=0): add(bnoise(0.28, 700, 4000, 200 + seed) * hann(int(SR * 0.28)), t, g)

# ---------------------------------------------------------------- scene A 0-3.4
creep(0.0, 2.25, 0.10); cap(0.05)
for t in (0.3, 1.0, 1.7): heartbeat(t, 0.42)
add(bnoise(0.3, 600, 5000, 3) * hann(int(SR * 0.3)), 1.3, 0.10)                   # the eyes pull back
add(sweep(2300, 1500, 0.4) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.4))), 2.2, 0.09); thunk(2.55, 0.26); cap(2.22)   # brakes
# ---------------------------------------------------------------- scene B 3.4-9.4
hiss(3.45, 0.5, 0.10, 8)
for k, t in enumerate((3.6, 3.9, 4.2)): step(t, 0.10, k)
cap(3.62)
for k in range(6): knock(4.5 + k * 0.27, 0.11, 480 + 20 * k)                     # up the ladder
tick(5.78, 1500, 0.12)                                                            # torch
tick(6.3, 1700, 0.10)
for k, n in enumerate((65, 69, 72, 77)): add(vibe(mtof(n), 2.4, 1.8), 6.32 + 0.05 * k, 0.09)
cap(6.36); hoot(6.6, 0.11)
add(bnoise(0.35, 600, 6000, 31) * hann(int(SR * 0.35)), 7.6, 0.12); pop(8.2, 600, 1000, 0.12)   # hop on the cap
for k in range(4): knock(8.4 + k * 0.25, 0.10, 560 - 20 * k)                     # down again
# ---------------------------------------------------------------- scene C 9.4-14.6
cap(9.6); pop(9.95, 700, 1200, 0.11); hoot(10.05, 0.07, 440)
add(sweep(400, 620, 0.12), 10.5, 0.09)
pop(11.35, 800, 1300, 0.10); chime(11.45, 91, 0.09)                               # feather in the cap
add(bnoise(0.22, 1500, 9000, 41) * hann(int(SR * 0.22)), 12.0, 0.13); pop(12.1, 500, 1000, 0.12); cap(12.02)   # the picture
add(sweep(420, 240, 0.25), 12.8, 0.12); add(sweep(200, 150, 0.12), 13.1, 0.12)   # gulp
add(sweep(600, 900, 0.07), 13.82, 0.11)
# ---------------------------------------------------------------- scene D 14.6-21
cap(14.8)
for k in range(6): knock(14.9 + k * 0.28, 0.10, 500 + 15 * k)
for T in (16.5, 18.3):
    for k in range(8): tick(T - 0.30 + k * 0.036, 1500 + k * 160, 0.075)
    add(bnoise(0.22, 800, 8000, int(T * 10)) * hann(int(SR * 0.22)), T - 0.16, 0.12)
    chime(T, 86, 0.10); cap(T + 0.06)
for k in range(5): knock(16.7 + k * 0.3, 0.09, 520)
for k in range(4): knock(18.6 + k * 0.6, 0.09, 460); puff(18.85 + k * 0.6, 0.07, k)
hoot(19.9, 0.08, 440)
# ---------------------------------------------------------------- scene E 21-26
puff(21.1, 0.09, 9)
add(bnoise(0.7, 500, 5000, 43) * hann(int(SR * 0.7)), 21.5, 0.11)                # the last hop home
hoot(22.3, 0.10, 330); hoot(22.45, 0.09, 392); hoot(22.7, 0.07, 523)
for k in range(3): chime(22.5 + k * 0.3, 84 + k * 4, 0.08)
for k, n in enumerate((77, 81, 84, 89)): add(vibe(mtof(n), 2.6, 1.6), 23.42 + 0.06 * k, 0.085)
add(sweep(600, 900, 0.07), 24.62, 0.10)
# ---------------------------------------------------------------- scene F 26-30
thunk(26.25, 0.2)
beep(26.7); beep(27.15)
add(sweep(900, 1500, 0.09), 27.0, 0.12)                                          # !
k = 0; t = 27.6
while t < 29.9:
    step(t, 0.11, k); t += 0.19; k += 1
creep(27.6, 2.4, 0.09)
cap(28.22); cap(28.92)
for t in (28.6, 29.2): heartbeat(t, 0.4)
add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), 29.5, 0.18)

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)
