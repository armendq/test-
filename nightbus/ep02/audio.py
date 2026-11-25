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
e_out = env_seg([(0, 0), (14.85, 0), (15.1, 1), (25.85, 1), (26.1, 0), (30, 0)])
e_in = 1 - e_out
buf[:NS] += rain_out * e_out * 0.05 + rain_in * e_in * 0.065
f_eng = env_seg([(0, 62), (15, 62), (15.3, 70), (19.3, 70), (20.0, 44), (26.0, 44), (26.2, 62), (30, 64)])
g_eng = env_seg([(0, 0.08), (3.4, 0.08), (3.6, 0.04), (14.9, 0.04), (15.1, 0.07), (19.3, 0.07), (20.1, 0.03), (25.9, 0.03), (26.1, 0.08), (30, 0.08)])
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng

# ---------------------------------------------------------------- music: enters when the light goes on
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
M0 = 7.0; MUSIC_END = 27.3
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (14.9, 0.8), (15.1, 0.9), (21, 0.95), (22.5, 1.1), (25.9, 1.0), (26.1, 0.55),
                  (MUSIC_END - 0.02, 0.55), (MUSIC_END, 0.0), (30, 0)])
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
def hiss(t, d=0.6, g=0.14, seed=5): add(bnoise(d, 2500, 10000, seed) * hann(int(SR * d)), t, g)
def thunk(t, g=0.3): add(sweep(130, 48, 0.16, 14), t, g); add(bnoise(0.04, 200, 1800, 77) * np.exp(-tt(0.04) * 80), t, g * 0.4)
def heartbeat(t, g=0.5):
    for dt, k in ((0, 1.0), (0.2, 0.7)):
        add(sweep(74, 38, 0.14, 12), t + dt, g * k); add(sweep(170, 95, 0.10, 16), t + dt, g * k * 0.45)
def buzz(t, g=0.12):
    for dt in (0, 0.17):
        d = 0.13; q = tt(d); add(np.sign(np.sin(2 * np.pi * 155 * q)) * hann(len(q)), t + dt, g * 0.5)
def creep(t0, d, g=0.10):
    q = tt(d)
    x = (np.sin(2 * np.pi * 61.7 * q) + 0.8 * np.sin(2 * np.pi * 65.4 * q) + 0.4 * np.sin(2 * np.pi * 185 * q)) * np.minimum(1, q / 0.6) * np.minimum(1, (d - q) / 0.08)
    add(x, t0, g)

# ---------------------------------------------------------------- scene A 0-3.5
creep(0.0, 3.5, 0.10); cap(0.05)
for t in (0.35, 1.05, 1.75, 2.75): heartbeat(t, 0.42)
tick(0.92, 2600, 0.06); tick(2.62, 2600, 0.06)
add(sweep(420, 260, 0.2), 2.0, 0.10); cap(2.15)                                   # gulp
# ---------------------------------------------------------------- scene B 3.5-9.5
tick(3.62, 1500, 0.12); add(sweep(900, 1300, 0.05), 3.64, 0.06)                  # torch on
for k, t in enumerate([3.85, 4.4, 4.95, 5.5, 6.0]): step(t, 0.10, k)
cap(3.75)
d = 2.3; q = tt(d)
growl = (np.sign(np.sin(2 * np.pi * np.cumsum(58 + 16 * q / d) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(58 + 16 * q / d) / SR)) * (1 + 0.5 * np.sin(2 * np.pi * 9 * q))
add(growl * np.minimum(1, q / 0.35) * np.minimum(1, (d - q) / 0.05), 4.3, 0.085)   # the shadow
add(sweep(180, 420, 2.0), 4.45, 0.05)
for t in (4.5, 5.2, 5.9): heartbeat(t, 0.36)
add(sweep(1300, 420, 0.28), 6.5, 0.13)                                           # the shadow shrinks
pop(6.52, 700, 1500, 0.15); add(sweep(1500, 1900, 0.09), 6.62, 0.09)             # a squeak
cap(6.62)
tick(7.0, 1700, 0.13)                                                            # light switch
for k, n in enumerate((65, 69, 72, 77)): add(vibe(mtof(n), 2.4, 1.8), 7.02 + 0.05 * k, 0.09)
pop(7.95, 700, 1100, 0.10); pop(8.1, 900, 1400, 0.10)                            # the cub waves
chime(8.15, 88, 0.10)
# ---------------------------------------------------------------- scene C 9.5-15
cap(9.7); pop(10.05, 500, 900, 0.12)
add(sweep(400, 620, 0.12), 10.75, 0.09); cap(11.02)
thunk(11.45, 0.22); tick(11.45, 2400, 0.14); chime(11.5, 91, 0.11)               # punched
add(sweep(620, 420, 0.14), 11.9, 0.08)
add(bnoise(0.22, 1500, 9000, 41) * hann(int(SR * 0.22)), 12.5, 0.13); pop(12.6, 500, 1000, 0.12); cap(12.52)   # the drawing
add(sweep(300, 250, 0.25), 13.0, 0.10); add(sweep(260, 300, 0.25), 13.4, 0.10)   # hmm
add(sweep(600, 900, 0.07), 14.02, 0.11); chime(14.1, 84, 0.08)                   # deal
# ---------------------------------------------------------------- scene D 15-21
cap(15.15); buzz(15.8); cap(17.0); buzz(17.6)
add(sweep(1900, 2500, 0.3) * (1 + 0.5 * np.sin(2 * np.pi * 40 * tt(0.3))), 19.4, 0.05)   # brakes
cap(19.6)
for k, n in enumerate((84, 88, 91, 96)): add(vibe(mtof(n), 2.2, 2.0), 19.92 + 0.06 * k, 0.10)   # that one
# ---------------------------------------------------------------- scene E 21-26
hiss(21.05, 0.5, 0.10, 8)
for k in range(4): pop(21.42 + k * 0.3, 520 + 90 * k, 900 + 140 * k, 0.11)       # running home
add(sweep(220, 130, 0.12, 10), 22.56, 0.18)                                      # hug
for k in range(3): chime(22.72 + k * 0.3, 84 + k * 4, 0.08)
for k, n in enumerate((77, 81, 84, 89)): add(vibe(mtof(n), 2.6, 1.6), 23.62 + 0.06 * k, 0.085)   # everyone is home
add(bnoise(0.5, 900, 7000, 43) * hann(int(SR * 0.5)), 24.02, 0.10); pop(24.6, 600, 1000, 0.11)   # the drawing flies
add(sweep(600, 900, 0.07), 24.92, 0.10)
# ---------------------------------------------------------------- scene F 26-30
HUM = [(26.1, 65, 0.28), (26.4, 69, 0.28), (26.7, 72, 0.4), (27.14, 69, 0.14)]
for (t, n, d) in HUM: add(hum(mtof(n), d), t, 0.095)
for k, t in enumerate((27.3, 27.85, 28.4)):
    add(sweep(120, 40, 0.3, 9), t, 0.55); add(bnoise(0.12, 150, 1500, 50 + k) * np.exp(-tt(0.12) * 30), t, 0.2); add(sweep(260, 150, 0.12, 14), t, 0.2)
creep(28.4, 1.6, 0.11)
add(sweep(300, 900, 0.4), 28.88, 0.07); tick(29.62, 2600, 0.06)
cap(28.6); cap(29.22)
for t in (29.0, 29.55): heartbeat(t, 0.42)
add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), 29.5, 0.18)

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)
