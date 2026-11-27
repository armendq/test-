import numpy as np, wave
SR = 44100; DUR = 25.0; NS = int(SR * DUR)
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



IN = [(0.0, 10.4), (17.8, 21.6)]
ENG = [(0, 0.03), (6.5, 0.03), (6.7, 0.02), (10.3, 0.02), (10.5, 0.08), (13.5, 0.08), (13.7, 0.0), (17.7, 0.0), (17.9, 0.06), (21.5, 0.06), (21.7, 0.08), (22.35, 0.08), (22.5, 0.0), (25, 0.0)]
M0 = 3.6; MEND = 21.6

ts = np.arange(NS) / SR
def spans_env(spans, r=0.12):
    pts = [(0, 0)]
    for a, b in spans: pts += [(max(a - r, 0.001), 0), (a + r, 1), (b - r, 1), (min(b + r, 29.999), 0)]
    pts.append((30, 0)); return env_seg(pts)
e_in = spans_env(IN); e_out = 1 - e_in
rain_out = bnoise(DUR, 1800, 9500, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.23 * ts))
rain_in = bnoise(DUR, 250, 2600, 2) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.31 * ts + 1))
buf[:NS] += rain_out * e_out * 0.045 + rain_in * e_in * 0.06
g_eng = env_seg(ENG)
f_eng = 42 + 300 * g_eng
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (16.7, 0.8), (17.0, 0.95), (19.0, 1.1), (MEND - 0.5, 1.0), (MEND - 0.02, 0.6), (MEND, 0.0), (30, 0)])
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
        if tm < MEND: madd(vibe(mtof(n), 2.4, 2.0), tm, 0.085)
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

def squeak(t, g=0.07, f0=1500):
    for dt in (0, 0.09): add(sweep(f0, f0 * 1.35, 0.06), t + dt, g)
def rustle(t, d=0.35, g=0.10, seed=7): add(bnoise(d, 2200, 9000, 300 + seed) * hann(int(SR * d)), t, g)
def bell(t, g=0.2):
    add(vibe(mtof(88), 2.2, 2.0) + 0.6 * vibe(mtof(95), 2.2, 2.6) + 0.3 * vibe(mtof(100), 2.2, 4.0), t, g); tick(t, 2600, 0.08)
def buzz(t, g=0.07):
    for dt in (0, 0.17):
        d = 0.13; q = tt(d); add(np.sign(np.sin(2 * np.pi * 150 * q)) * hann(len(q)), t + dt, g)

def woo(t, f0=520, f1=640, d=0.32, g=0.07):
    """the ghost's small voice"""
    q = tt(d); fq = f0 + (f1 - f0) * np.sin(np.pi * q / d); vib = 1 + 0.02 * np.sin(2 * np.pi * 7 * q)
    p = 2 * np.pi * np.cumsum(fq * vib) / SR
    add((np.sin(p) + 0.25 * np.sin(2 * p)) * hann(len(q)), t, g)
def clack(t, g=0.11, f0=1500):
    add(sweep(f0, f0 * 0.7, 0.03, 60), t, g); add(bnoise(0.02, 1200, 6000, int(t * 1000) % 997) * np.exp(-tt(0.02) * 160), t, g * 0.6)
def glass(t, d=0.14, f0=1500, f1=1900, g=0.06):
    q = tt(d); fq = f0 + (f1 - f0) * q / d; p = 2 * np.pi * np.cumsum(fq * (1 + 0.012 * np.sin(2 * np.pi * 31 * q))) / SR
    add((np.sin(p) + 0.4 * np.sin(2 * p)) * hann(len(q)), t, g)
def fiddle(t, n, d=0.18, g=0.07):
    """a very small fiddle: bowed saw with a quick vibrato"""
    q = tt(d); vib = 1 + 0.008 * np.sin(2 * np.pi * 6.5 * q) * np.minimum(1, q / 0.08)
    p = 2 * np.pi * np.cumsum(mtof(n) * vib) / SR
    x = sum(np.sin(k * p) / k for k in range(1, 6)) * np.minimum(1, q / 0.022) * np.minimum(1, (d - q) / 0.04)
    add(x, t, g * 0.5)
def whoosh(t, d=0.35, g=0.10, seed=11, lo=500, hi=5000): add(bnoise(d, lo, hi, seed) * hann(int(SR * d)), t, g)
def pizz(t, n, g=0.05): add(vibe(mtof(n), 0.5, 9.0), t, g)

def heartbeat(t, g=0.42):
    for dt, k in ((0, 1.0), (0.2, 0.7)):
        add(sweep(74, 38, 0.14, 12), t + dt, g * k); add(sweep(170, 95, 0.10, 16), t + dt, g * k * 0.45)
def creep(t0, d, g=0.09):
    q = tt(d)
    x = (np.sin(2 * np.pi * 61.7 * q) + 0.8 * np.sin(2 * np.pi * 65.4 * q) + 0.4 * np.sin(2 * np.pi * 185 * q)) * np.minimum(1, q / 0.4) * np.minimum(1, (d - q) / 0.08)
    add(x, t0, g)
def thunder(t, g=0.22):
    d = 1.6; add(bnoise(d, 40, 400, 91) * np.exp(-tt(d) * 2.2) * np.minimum(1, tt(d) / 0.02), t, g); add(bnoise(0.12, 1500, 9000, 92) * np.exp(-tt(0.12) * 30), t, g * 0.5)
def riser(t=29.45): add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), t, 0.16)
def steps(t0, n, gap=0.19, g=0.1):
    for k in range(n): step(t0 + k * gap, g, k)
def door(t): hiss(t, 0.5, 0.09, 8)


def gust(t, d=1.2, g=0.09, seed=1, lo=250, hi=1800):
    q = tt(d); add(bnoise(d, lo, hi, seed) * np.sin(np.pi * q / d) ** 2 * (1 + 0.3 * np.sin(2 * np.pi * 3 * q)), t, g)
def flap(t, n=6, gap=0.07, g=0.05, seed=50):
    for k in range(n): add(bnoise(0.04, 600, 4000, seed + k) * np.exp(-tt(0.04) * 90), t + k * gap, g)
gust(0.0, 1.6, 0.1, 1); gust(1.2, 1.8, 0.08, 2); gust(2.4, 1.2, 0.07, 3)
flap(0.2, 8); flap(1.0, 6); flap(2.2, 6)
add(sweep(900, 300, 0.12) * (1 + 0.7 * np.sin(2 * np.pi * 70 * tt(0.12))), 1.6, 0.06)
cap(0.05); cap(1.82)
for k in range(5): step(0.5 + k * 0.2, 0.08, k)
cap(3.6); whoosh(3.45, 0.5, 0.08, 21, 400, 3000); flap(3.6, 6); pop(4.1, 420, 900, 0.08)
for k in range(5): tick(4.4 + k * 0.09, 1800 + 120 * k, 0.04)
pop(5.6, 600, 1100, 0.1); chime(5.62, 88, 0.08); cap(5.62)

C0 = 6.6; D0 = 10.4; F0 = 17.8
cap(C0 + 0.2); pop(C0 + 0.35, 420, 800, 0.09); pop(C0 + 0.8, 460, 860, 0.09); pop(C0 + 1.5, 600, 1000, 0.1); cap(C0 + 2.02)
pop(C0 + 2.5, 700, 1100, 0.1); chime(C0 + 3.05, 88, 0.1)
for k in range(5): tick(C0 + 3.05 + k * 0.05, 2100 + 150 * k, 0.05)
cap(D0 + 0.2); pop(D0 + 0.52, 500, 1000, 0.1); cap(D0 + 0.8)
cap(13.8); whoosh(13.9, 1.4, 0.1, 31, 300, 2500); gust(13.8, 1.8, 0.06, 7); flap(14.2, 10, 0.12, 0.04, 70)
chime(15.5, 91, 0.1); cap(15.7)
for i in range(3): pop(15.9 + i * 0.3, 500 + 80 * i, 1000 + 80 * i, 0.08)
pop(F0 + 0.65, 500, 900, 0.09); cap(F0 + 1.0); chime(F0 + 1.4, 91, 0.1)
for k in range(8): tick(F0 + 1.85 + k * 0.2, 2400 + 100 * k, 0.045)
add(sweep(2300, 1500, 0.45) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.45))), 22.4, 0.1); thunk(22.75, 0.26)
cap(22.5); cap(23.4)
q = tt(2.2); add(bnoise(2.2, 150, 900, 88) * (0.5 + 0.5 * np.sin(2 * np.pi * 34 * q)) * np.minimum(1, q / 0.3), 22.8, 0.05)
for k in range(6): tick(23.0 + k * 0.28, 2600 + 200 * (k % 2), 0.05)
riser(24.45)

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)

