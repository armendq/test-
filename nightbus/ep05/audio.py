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
e_in = env_seg([(0, 1), (14.05, 1), (14.2, 0), (21.1, 0), (21.3, 1), (30, 1)])
e_out = env_seg([(0, 0), (14.05, 0), (14.2, 0.8), (16.7, 0.8), (16.9, 0.55), (21.1, 0.45), (21.3, 0), (30, 0)])
buf[:NS] += rain_out * e_out * 0.05 + rain_in * e_in * 0.06
f_eng = env_seg([(0, 66), (1.55, 66), (1.95, 42), (14.1, 42), (14.3, 62), (16.5, 62), (16.9, 42), (21.1, 42), (21.3, 60), (25.3, 60), (25.6, 40), (30, 40)])
g_eng = env_seg([(0, 0.075), (1.55, 0.075), (1.95, 0.028), (3.6, 0.022), (14.1, 0.02), (14.3, 0.07), (16.5, 0.07), (16.9, 0.02), (17.4, 0.0), (21.1, 0.0), (21.3, 0.06),
                 (25.3, 0.06), (25.6, 0.0), (30, 0.0)])
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng

# ---------------------------------------------------------------- music: enters when the ghost appears, stops for the cliffhanger
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
M0 = 9.85; MUSIC_END = 25.6
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (14.1, 0.85), (14.3, 0.95), (18.7, 0.95), (18.9, 1.05), (21.2, 1.0), (24.3, 0.9), (25.2, 0.5),
                  (MUSIC_END - 0.03, 0.42), (MUSIC_END, 0.0), (30, 0)])
mus = np.zeros(NS + 2 * SR)
def madd(x, t0, g):
    i = int(t0 * SR); j = min(len(mus), i + len(x))
    if i >= 0 and j > i: mus[i:j] += g * x[:j - i]
for bar in range(6):
    ch = CH[bar % 4]; t0 = M0 + bar * 4 * beat
    madd(bass(mtof(ch[0] - 12)), t0, 0.20); madd(bass(mtof(ch[0] - 12), 0.9), t0 + 2.5 * beat, 0.11)
    for e, k in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
        madd(vibe(mtof(ch[k] + 12), 1.6, 3.2), t0 + e * beat / 2, 0.05 * (1.2 if e % 4 == 0 else 0.85))
    d = 4 * beat; t = tt(d); env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    pad = sum(np.sin(2 * np.pi * mtof(n) * t) + 0.25 * np.sin(2 * np.pi * mtof(n + 12) * t) for n in ch)
    madd(pad * env, t0, 0.022)
for rep in range(2):
    for (b, n) in MEL:
        tm = M0 + rep * 12 * beat + b * beat
        if tm < MUSIC_END: madd(vibe(mtof(n), 2.4, 2.0), tm, 0.085)
mus[int(MUSIC_END * SR):] = 0
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

# ---------------------------------------------------------------- scene A 0-3.6: who rang the bell
bell(0.0, 0.13); bell(0.42, 0.10); cap(0.05)
creep(0.0, 3.5, 0.05)
for t in (0.22, 0.95): heartbeat(t, 0.26)
for k in range(4): tick(0.12 + 0.3 * k, 900, 0.04)                                  # the strap swings
whoosh(0.6, 0.6, 0.08, 3)                                                           # the camera pulls back
add(sweep(2300, 1500, 0.35) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.35))), 1.5, 0.06); thunk(1.78, 0.16)   # Otto brakes
puff(2.1, 0.09, 1); thunk(2.12, 0.1); pop(2.14, 500, 900, 0.09)                     # a seat dents in the mirror
cap(2.4); heartbeat(2.5, 0.26)
bell(3.0, 0.11); bell(3.22, 0.09); pop(3.02, 600, 1000, 0.08)
# ---------------------------------------------------------------- scene B 3.6-8: nobody there, somebody there
creep(3.6, 4.4, 0.05); cap(3.8)
for k in range(5):
    step(3.68 + k * 0.22, 0.07, k); pizz(3.68 + k * 0.22, 50 if k % 2 == 0 else 53, 0.05)
thunk(4.85, 0.16); puff(4.86, 0.1, 2); add(sweep(240, 420, 0.12), 4.9, 0.08); add(sweep(420, 300, 0.16), 5.02, 0.06)   # the cushion dents
pop(4.9, 700, 1200, 0.10); heartbeat(5.1, 0.28)
for k in range(4): glass(5.55 + k * 0.35, 0.1, 880 - 40 * k, 760 - 40 * k, 0.05 * (1 - 0.2 * k))                     # the strap creaks
pizz(5.6, 57, 0.05); pizz(6.1, 56, 0.05)
cap(5.87); hiss(5.9, 0.55, 0.06, 6)                                                 # the window fogs
glass(6.5, 0.1, 1500, 1750); glass(6.7, 0.1, 1600, 1850)                            # two eyes
glass(6.9, 0.5, 1250, 1700, 0.065); glass(7.3, 0.12, 1700, 1300, 0.05)              # the mouth
heartbeat(6.3, 0.26)
tick(7.56, 2400, 0.08); add(sweep(1400, 700, 0.12), 7.6, 0.07); pizz(7.6, 62, 0.06)  # a tear
# ---------------------------------------------------------------- scene C 8-12.4: one spare sheet
chime(8.12, 96, 0.06); cap(8.17)
pop(8.42, 500, 950, 0.11)                                                           # the cloth
add(sweep(300, 220, 0.2), 8.72, 0.05); whoosh(8.92, 0.3, 0.13, 12, 700, 6000)       # wind up and throw
rustle(9.05, 0.5, 0.09, 1)
puff(9.55, 0.13, 3); thunk(9.57, 0.1)                                               # it lands on somebody
pop(9.85, 600, 1000, 0.11); pop(9.93, 700, 1150, 0.11)                              # two eye holes
tick(9.83, 1700, 0.10)
for k, n in enumerate((65, 69, 72, 77)): add(vibe(mtof(n), 2.4, 1.8), 9.86 + 0.05 * k, 0.09)
cap(9.97)
woo(10.25, 430, 520, 0.4, 0.07)                                                     # shy
woo(10.68, 560, 760, 0.26, 0.07); woo(11.0, 600, 820, 0.26, 0.07)                   # happy
pop(10.66, 500, 900, 0.08); pop(10.99, 500, 900, 0.08)
add(sweep(600, 900, 0.07), 10.66, 0.09)                                             # Otto salutes
clack(11.42); clack(11.5, 0.08, 1300); chime(11.72, 91, 0.09)                       # a clothes peg
add(sweep(520, 760, 0.09), 11.68, 0.07)
# ---------------------------------------------------------------- scene D 12.4-16.8: the fare, then the road
cap(12.57)
clack(12.82, 0.12); pop(12.84, 700, 1150, 0.08)                                     # the peg changes paws
woo(13.02, 600, 840, 0.26, 0.07); woo(13.45, 620, 860, 0.24, 0.06)
chime(13.33, 93, 0.10); add(sweep(600, 900, 0.07), 13.52, 0.09)
whoosh(14.05, 0.3, 0.10, 14); cap(14.29); cap(14.87)
rustle(14.45, 0.2, 0.10, 4); pop(14.47, 500, 1000, 0.10)                            # the picture
puff(14.6, 0.06, 4); puff(15.65, 0.06, 5); puff(16.5, 0.06, 6)                      # bushes go by
add(sweep(300, 1100, 0.22), 15.33, 0.12); pop(15.5, 700, 1200, 0.10)                # up through the roof
woo(15.6, 640, 900, 0.4, 0.08); woo(16.25, 700, 940, 0.3, 0.06)
d = 1.4; q = tt(d); add(bnoise(d, 900, 5000, 15) * np.minimum(1, q / 0.2) * np.minimum(1, (d - q) / 0.2) * (1 + 0.3 * np.sin(2 * np.pi * 5 * q)), 15.4, 0.06)   # wind
# ---------------------------------------------------------------- scene E 16.8-21.2: home, and washing day
add(sweep(2300, 1500, 0.3) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.3))), 16.62, 0.05); hiss(16.85, 0.4, 0.09, 8); cap(17.02)
woo(17.12, 560, 900, 0.3, 0.08); pop(17.1, 600, 1100, 0.07)                         # it sees its sheet
rustle(17.3, 0.3, 0.06, 5); rustle(17.75, 0.3, 0.06, 6)                             # the sheet flaps
add(sweep(400, 1000, 0.3), 17.68, 0.09)                                             # up it goes
whoosh(18.0, 0.3, 0.12, 16, 900, 7000)
for k, n in enumerate((72, 76, 79, 84)): add(vibe(mtof(n), 1.8, 2.4), 18.02 + 0.05 * k, 0.08)
pop(18.1, 600, 1000, 0.09); pop(18.17, 700, 1150, 0.09)
rustle(18.1, 0.45, 0.07, 7)                                                         # Otto's cloth flies back
clack(18.42, 0.12); clack(18.5, 0.10, 1300); pop(18.44, 500, 950, 0.09)             # the pegs pop off
puff(18.57, 0.08, 7)
woo(18.6, 660, 960, 0.4, 0.08); cap(18.87)
d = 0.45; q = tt(d); add(np.sin(2 * np.pi * np.cumsum(300 + 160 * q / d) / SR) * (1 + 0.5 * np.sin(2 * np.pi * 28 * q)) * hann(len(q)), 19.1, 0.05)   # the door
pop(19.3, 800, 1300, 0.08); woo(19.34, 820, 1100, 0.2, 0.05)                        # small ghosts at the windows
pop(19.6, 900, 1400, 0.08); woo(19.64, 900, 1200, 0.2, 0.05)
for k in range(3): chime(19.05 + k * 0.4, 84 + k * 4, 0.05)
add(sweep(600, 900, 0.07), 19.92, 0.09)                                             # salute
pop(20.5, 1000, 1600, 0.10); woo(20.55, 1000, 1400, 0.22, 0.06); chime(20.52, 96, 0.07)   # one more in the chimney
# ---------------------------------------------------------------- scene F 21.2-25.6: the peg joins the collection
add(sweep(320, 520, 0.5), 21.3, 0.04)                                               # the paw goes up
cap(22.22)
tick(22.6, 2300, 0.12); clack(22.61, 0.12); chime(22.64, 91, 0.10)                  # pinned
for k, n in enumerate((84, 86, 88, 91, 96)): chime(23.3 + 0.3 * k, n, 0.06)         # the collection
for k, (dt, n) in enumerate(((0.0, 65), (0.3, 69), (0.6, 67), (0.9, 72))): add(hum(mtof(n - 12), 0.24), 23.2 + dt, 0.03)
fiddle(24.42, 86, 0.16, 0.03); fiddle(24.62, 91, 0.16, 0.035); fiddle(24.82, 93, 0.22, 0.04)   # something small plays far away
pop(24.92, 600, 1000, 0.09); cap(24.96)
fiddle(25.2, 91, 0.16, 0.04); fiddle(25.4, 88, 0.16, 0.045)
# ---------------------------------------------------------------- scene G 25.6-30: seat 7. no music, only the small fiddle
for k in range(4): step(25.7 + k * 0.22, 0.06, k)
PH = [(0.0, 86, .18), (0.2, 91, .18), (0.4, 93, .18), (0.6, 91, .18), (0.8, 88, .18), (1.0, 90, .18), (1.2, 91, .34), (1.7, 86, .18), (1.9, 88, .18), (2.1, 90, .18),
      (2.3, 93, .18), (2.5, 95, .18), (2.7, 93, .26)]
for (dt, n, d) in PH: fiddle(25.75 + dt, n, d, 0.15)
for (dt, n) in ((0.0, 62), (0.8, 59), (1.7, 62), (2.5, 57)): pizz(25.75 + dt, n, 0.06)
rustle(26.6, 0.35, 0.05, 8); add(sweep(420, 300, 0.25), 26.62, 0.04)                # Otto bends down
cap(26.87); cap(27.62)
for t in (27.0, 27.95): heartbeat(t, 0.34)
tick(28.75, 1100, 0.10); add(sweep(700, 380, 0.14), 28.77, 0.06)                    # the light goes out
heartbeat(28.82, 0.42)
pop(29.1, 500, 1000, 0.12)                                                          # and comes back
for k, (dt, n, d) in enumerate(((0.0, 91, .11), (0.12, 93, .11), (0.24, 95, .11), (0.36, 98, .34))): fiddle(29.1 + dt, n, d, 0.17)
chime(29.12, 98, 0.07); pop(29.14, 700, 1200, 0.08)
add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), 29.5, 0.16)

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)
