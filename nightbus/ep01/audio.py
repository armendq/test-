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
e_out = env_seg([(0, 1), (3.85, 1), (4.1, 0.0), (15.9, 0.0), (16.15, 1), (25.35, 1), (25.6, 0), (30, 0)])
e_in = env_seg([(0, 0), (3.85, 0), (4.1, 1), (15.9, 1), (16.15, 0), (25.35, 0), (25.6, 1), (30, 1)])
buf[:NS] += rain_out * e_out * 0.055 + rain_in * e_in * 0.07

# engine: idle in A, rolling in D, cruising in F
f_eng = env_seg([(0, 46), (4, 46), (16.4, 46), (16.9, 78), (17.6, 70), (17.95, 44), (20, 44), (25.5, 62), (30, 64)])
g_eng = env_seg([(0, 0.05), (3.9, 0.05), (4.1, 0.018), (15.9, 0.018), (16.4, 0.05), (16.9, 0.085), (17.9, 0.06), (18.3, 0.035),
                 (25.4, 0.03), (25.6, 0.085), (30, 0.085)])
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng

# ---------------------------------------------------------------- music: 80 bpm, bar = 3 s, F  Dm  Bb  C
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
MUSIC_END = 27.35
m_gain = env_seg([(0, 0.85), (3.9, 0.85), (4.1, 0.7), (10.9, 0.7), (11.0, 0.85), (20, 0.9), (22, 1.1), (25.4, 1.0), (25.6, 0.55),
                  (MUSIC_END - 0.02, 0.55), (MUSIC_END, 0.0), (30, 0)])
mus = np.zeros(NS + 2 * SR)


def madd(x, t0, g):
    i = int(t0 * SR); j = min(len(mus), i + len(x))
    if j > i: mus[i:j] += g * x[:j - i]


for bar in range(10):
    ch = CH[bar % 4]; t0 = bar * 4 * beat
    madd(bass(mtof(ch[0] - 12)), t0, 0.20); madd(bass(mtof(ch[0] - 12), 0.9), t0 + 2.5 * beat, 0.11)
    for e, k in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
        madd(vibe(mtof(ch[k] + 12), 1.6, 3.2), t0 + e * beat / 2, 0.05 * (1.2 if e % 4 == 0 else 0.85))
    d = 4 * beat; t = tt(d); env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    pad = sum(np.sin(2 * np.pi * mtof(n) * t) + 0.25 * np.sin(2 * np.pi * mtof(n + 12) * t) for n in ch)
    madd(pad * env, t0, 0.022)
for rep in range(3):
    for (b, n) in MEL:
        tm = rep * 12 * beat + b * beat
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
def snore(t, g=0.20, seed=9):
    d = 0.75; x = bnoise(d, 90, 420, seed) * hann(int(SR * d)) * (1 + 0.6 * np.sin(2 * np.pi * 27 * tt(d)))
    add(x, t, g)                                                       # in
    add(sweep(640, 980, 0.5) * 0.5 + bnoise(0.5, 900, 2600, seed + 1) * hann(int(SR * 0.5)) * 0.3, t + 0.85, g * 0.42)   # out, whistling
def boing(t, g=0.22):
    d = 0.5; q = tt(d); f = 240 + 260 * q / d + 70 * np.sin(2 * np.pi * 17 * q) * np.exp(-q * 5)
    add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-q * 5) * np.minimum(1, q / 0.004), t, g)
def heartbeat(t, g=0.5):
    for dt, k in ((0, 1.0), (0.2, 0.7)):
        add(sweep(74, 38, 0.14, 12), t + dt, g * k); add(sweep(170, 95, 0.10, 16), t + dt, g * k * 0.45)


# ---------------------------------------------------------------- scene A 0-4: hook
add(bnoise(0.5, 500, 5000, 3) * hann(int(SR * 0.5)), 0.0, 0.12)                       # air brake as the bus waits
for k, t in enumerate([0.25, 0.75, 1.25]): add(sweep(300, 240, 0.09), t, 0.06)        # tiny snail steps
cap(0.05); cap(2.5)
add(sweep(700, 1000, 0.12), 1.0, 0.05)                                              # camera pull out
# ---------------------------------------------------------------- scene B 4-11: time lapse
pop(4.25, 500, 880, 0.10); pop(4.45, 620, 990, 0.10)                                # Otto waves hello
for k in range(4): tick(4.7 + k * 0.22, 2100 if k % 2 == 0 else 1500, 0.07)
for T in (5.6, 7.3, 9.0):                                                           # time jumps
    for k in range(8): tick(T - 0.30 + k * 0.036, 1500 + k * 160, 0.075)
    add(bnoise(0.22, 800, 8000, int(T * 10)) * hann(int(SR * 0.22)), T - 0.16, 0.12)
    chime(T, 86, 0.10); cap(T + 0.06)
for k in range(5): tick(5.85 + k * 0.26, 2100 if k % 2 == 0 else 1500, 0.08)         # he checks the watch
add(sweep(330, 250, 0.35), 6.75, 0.09)                                              # sigh
snore(7.45); snore(9.15, 0.2, 11)
for k in range(3): chime(9.85 + k * 0.12, 91 + k * 4, 0.085)                         # the snail made it
# ---------------------------------------------------------------- scene C 11-16
boing(11.0); add(sweep(900, 1500, 0.09), 11.05, 0.12); cap(11.05)
for k, t in enumerate([11.56, 11.87, 12.19, 12.50]): step(t, 0.16, k)                # walk to the door
add(sweep(360, 780, 0.28), 12.72, 0.12)                                             # lift
for k, t in enumerate([13.36, 13.67, 13.99, 14.30]): step(t, 0.15, k + 4)           # walk back
add(sweep(520, 300, 0.22), 14.4, 0.10); add(sweep(200, 120, 0.1, 10), 14.8, 0.2)     # set down on the seat
add(sweep(600, 900, 0.07), 15.02, 0.11)                                             # salute
chime(15.12, 88, 0.12); chime(15.24, 93, 0.10)                                      # heart
hiss(15.08, 0.6, 0.13, 6); thunk(15.68, 0.3)                                        # door
# ---------------------------------------------------------------- scene D 16-20
cap(16.2)
add(vibe(mtof(88), 1.8, 2.2) + 0.7 * vibe(mtof(84), 1.8, 2.2), 17.05, 0.20)          # stop bell
add(vibe(mtof(84), 1.8, 2.2), 17.27, 0.16)
add(sweep(1900, 2500, 0.28) * (1 + 0.5 * np.sin(2 * np.pi * 40 * tt(0.28))), 17.78, 0.06)   # brake squeak
add(sweep(110, 60, 0.2, 10), 17.95, 0.22); cap(17.98)
hiss(18.5, 0.6, 0.13, 7)
# ---------------------------------------------------------------- scene E 20-25.5
for k, t in enumerate([20.12, 20.43, 20.75]): step(t, 0.10, k + 9)
add(sweep(560, 300, 0.5), 21.1, 0.08)                                               # gentle lowering
add(sweep(240, 330, 0.3) * (1 + 0.4 * np.sin(2 * np.pi * 30 * tt(0.3))), 21.82, 0.07)   # tiny door creak
for k in range(3): pop(22.27 + k * 0.22, 600 + 120 * k, 1200 + 200 * k, 0.13)       # three babies
for k in range(3): chime(22.6 + k * 0.35, 84 + k * 4, 0.085)                         # hearts
add(sweep(600, 900, 0.07), 23.4, 0.09); cap(23.34)                                  # hat tip
for k, n in enumerate((77, 81, 84, 89)): add(vibe(mtof(n), 2.6, 1.6), 23.32 + 0.06 * k, 0.085)   # everyone is home
add(sweep(600, 900, 0.07), 23.95, 0.10)                                             # salute
# ---------------------------------------------------------------- scene F 25.5-30
HUM = [(25.62, 65, 0.28), (25.92, 69, 0.28), (26.22, 72, 0.42), (26.68, 69, 0.26), (26.96, 67, 0.26), (27.24, 70, 0.11)]
for (t, n, d) in HUM: add(hum(mtof(n), d), t, 0.095)
d = 3.0; q = tt(d)
creep = (np.sin(2 * np.pi * 61.7 * q) + 0.8 * np.sin(2 * np.pi * 65.4 * q) + 0.4 * np.sin(2 * np.pi * 185 * q)) * np.minimum(1, q / 1.2) * np.minimum(1, (d - q) / 0.05)
add(creep, 27.0, 0.11)                                                              # something is back there
tick(27.36, 900, 0.10)                                                              # the hum stops
d = 2.4; q = tt(d)
sting = sum(np.sin(2 * np.pi * mtof(n) * q) * (1 + 0.35 * np.sin(2 * np.pi * (6 + i) * q)) for i, n in enumerate((49, 55, 60, 66, 73)))
add(sting * np.minimum(1, q / 0.02) * np.exp(-q * 1.1), 27.65, 0.06)
add(sweep(95, 40, 0.5, 6), 27.65, 0.5)
add(sweep(1200, 2400, 0.12), 27.66, 0.10); cap(27.82)
for t in (28.15, 28.75, 29.32): heartbeat(t, 0.5)
cap(28.52); tick(28.42, 2600, 0.06); tick(29.44, 2600, 0.06)
add(bnoise(0.55, 400, 6000, 60) * np.minimum(1, tt(0.55) / 0.5) ** 2 * np.minimum(1, (0.55 - tt(0.55)) / 0.03), 29.45, 0.2)   # into the loop

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)
