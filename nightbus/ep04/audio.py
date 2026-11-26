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
e_in = env_seg([(0, 0), (3.5, 0), (3.7, 1), (12.3, 1), (12.5, 0), (25.5, 0), (25.7, 1), (30, 1)])
e_out = env_seg([(0, 1), (3.5, 1), (3.7, 0), (12.3, 0), (12.5, 0.8), (16.7, 0.8), (16.9, 0.6), (21.2, 0.5), (25.5, 0.4), (25.7, 0), (30, 0)])
buf[:NS] += rain_out * e_out * 0.05 + rain_in * e_in * 0.065
f_eng = env_seg([(0, 66), (1.9, 66), (2.3, 42), (12.3, 42), (12.6, 62), (15.3, 62), (16.2, 42), (25.5, 42), (25.8, 60), (30, 60)])
g_eng = env_seg([(0, 0.08), (1.9, 0.08), (2.4, 0.03), (3.5, 0.03), (3.7, 0.02), (12.3, 0.02), (12.6, 0.07), (15.3, 0.07), (16.2, 0.025), (16.8, 0.0), (25.5, 0.0), (25.8, 0.06), (30, 0.06)])
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng

# ---------------------------------------------------------------- music: enters at the reveal
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
M0 = 4.85; MUSIC_END = 27.0
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (12.4, 0.8), (12.6, 0.9), (20.4, 0.9), (20.6, 0.6), (21.3, 0.9), (23.0, 1.1), (25.5, 1.0), (25.7, 0.7),
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

def squeak(t, g=0.07, f0=1500):
    for dt in (0, 0.09): add(sweep(f0, f0 * 1.35, 0.06), t + dt, g)
def rustle(t, d=0.35, g=0.10, seed=7): add(bnoise(d, 2200, 9000, 300 + seed) * hann(int(SR * d)), t, g)
def bell(t, g=0.2):
    add(vibe(mtof(88), 2.2, 2.0) + 0.6 * vibe(mtof(95), 2.2, 2.6) + 0.3 * vibe(mtof(100), 2.2, 4.0), t, g); tick(t, 2600, 0.08)
def buzz(t, g=0.07):
    for dt in (0, 0.17):
        d = 0.13; q = tt(d); add(np.sign(np.sin(2 * np.pi * 150 * q)) * hann(len(q)), t + dt, g)

# ---------------------------------------------------------------- scene A 0-3.6: the chase
creep(0.0, 2.3, 0.10); cap(0.05); add(sweep(900, 1500, 0.09), 0.04, 0.11)
for t in (0.25, 0.95, 1.65): heartbeat(t, 0.42)
k = 0; t = 0.1
while t < 2.95:
    step(t, 0.11, k); t += 0.19; k += 1
add(bnoise(0.3, 600, 5000, 3) * hann(int(SR * 0.3)), 0.6, 0.09)                    # the camera pulls back
beep(1.4); beep(1.68)
add(sweep(2300, 1500, 0.4) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.4))), 1.9, 0.09); thunk(2.25, 0.26)   # brakes
cap(2.42); puff(2.6, 0.07, 1); puff(3.2, 0.07, 2)
hiss(3.0, 0.45, 0.12, 8)                                                           # the door
add(sweep(700, 380, 0.14), 3.22, 0.09)                                             # the driver ducks
# ---------------------------------------------------------------- scene B 3.6-8: two eyes at the wheel
cap(3.78); creep(3.6, 1.2, 0.08)
for k, t in enumerate((3.75, 4.05, 4.35)): step(t, 0.10, k)
tick(3.95, 1500, 0.12)                                                             # torch
heartbeat(4.2, 0.4)
tick(4.8, 1700, 0.10)                                                              # the light finds it
for k, n in enumerate((65, 69, 72, 77)): add(vibe(mtof(n), 2.4, 1.8), 4.82 + 0.05 * k, 0.09)
cap(4.92); add(bnoise(0.4, 500, 5000, 21) * hann(int(SR * 0.4)), 4.9, 0.08)         # push in
pop(5.55, 500, 950, 0.12); squeak(5.75)                                           # the cap goes up
pop(6.15, 700, 1100, 0.09); squeak(6.5, 0.05, 1700)
add(sweep(800, 320, 0.16), 7.15, 0.11); thunk(7.32, 0.16); squeak(7.5, 0.06, 1300)  # the cap comes down
# ---------------------------------------------------------------- scene C 8-12.4: wrong bus, and the fare
cap(8.22); pop(8.42, 600, 1000, 0.11)
buzz(9.42); add(sweep(420, 300, 0.2), 9.75, 0.07)
pop(10.05, 900, 500, 0.08); cap(10.37)
tick(10.52, 1900, 0.10); pop(10.9, 700, 1150, 0.10)                                # the tag changes hands
chime(11.72, 91, 0.10); add(sweep(600, 900, 0.07), 11.62, 0.10)
thunk(11.9, 0.22); rustle(11.95, 0.4, 0.13, 1); squeak(12.1, 0.05, 1400)            # something moves in the suitcase
# ---------------------------------------------------------------- scene D 12.4-16.8: to the end of the lane
cap(12.58); cap(13.27)
add(bnoise(0.22, 1500, 9000, 41) * hann(int(SR * 0.22)), 12.7, 0.12); pop(12.8, 500, 1000, 0.11)   # the picture
puff(12.95, 0.07, 3); puff(14.15, 0.07, 4)                                         # bushes go by
for t in (13.5, 14.3, 14.9): knock(t, 0.08, 300)                                   # the suitcase bumps on the roof
add(sweep(2300, 1500, 0.5) * (1 + 0.5 * np.sin(2 * np.pi * 45 * tt(0.5))), 15.35, 0.08); thunk(16.1, 0.2)
add(sweep(320, 200, 0.3), 15.9, 0.09); knock(16.5, 0.12, 280)                      # it slides
chime(16.12, 86, 0.10)
# ---------------------------------------------------------------- scene E 16.8-21.2: the door and the suitcase
cap(17.02)
d = 1.35; q = tt(d); add(bnoise(d, 150, 1100, 51) * (1 + 0.5 * np.sin(2 * np.pi * 9 * q)) * np.minimum(1, q / 0.1) * np.minimum(1, (d - q) / 0.1), 16.95, 0.10)   # pushing
for k in range(5): step(17.0 + k * 0.27, 0.08, k)
puff(17.5, 0.07, 5); puff(18.1, 0.07, 6)
cap(19.17)
knock(19.5, 0.2, 300); thunk(19.5, 0.2); add(sweep(500, 330, 0.18), 19.62, 0.08)    # too big for the door
for k in range(3): tick(19.85 + 0.1 * k, 1300, 0.07)                               # Otto scratches his head
pop(20.15, 500, 1000, 0.11); squeak(20.3)
tick(20.52, 2300, 0.11); tick(20.6, 2600, 0.11)                                    # the latches
add(sweep(180, 950, 0.14), 20.65, 0.2); thunk(20.65, 0.24)                         # pop
d = 1.6; q = tt(d); add(bnoise(d, 1500, 9000, 53) * np.minimum(1, q / 0.05) * np.exp(-q * 1.6), 20.66, 0.16)
for k, n in enumerate((72, 76, 79, 84)): add(vibe(mtof(n), 1.6, 2.6), 20.7 + 0.05 * k, 0.07)
# ---------------------------------------------------------------- scene F 21.2-25.6: the winter bed
cap(21.42)
rustle(21.5, 0.9, 0.08, 2); rustle(22.2, 0.8, 0.07, 3)
add(sweep(950, 380, 0.4), 21.55, 0.09)                                             # the dive
add(bnoise(0.35, 700, 6000, 55) * hann(int(SR * 0.35)), 21.95, 0.14); thunk(21.97, 0.12)
pop(22.58, 600, 1100, 0.11); squeak(22.7, 0.07, 1600)
cap(23.07)
for k, n in enumerate((77, 81, 84, 89)): add(vibe(mtof(n), 2.6, 1.6), 23.12 + 0.06 * k, 0.085)
for k in range(3): chime(23.25 + k * 0.3, 84 + k * 4, 0.06)
add(sweep(600, 900, 0.07), 24.02, 0.10)                                            # salute
tick(24.78, 1200, 0.08)                                                            # a leaf lands on the cap
for t in (24.5, 25.15): add(sweep(190, 120, 0.4), t, 0.06); rustle(t + 0.35, 0.3, 0.04, int(t))   # snoring
# ---------------------------------------------------------------- scene G 25.6-30: the bell
for k, (dt, n) in enumerate(((0.15, 65), (0.45, 69), (0.75, 67), (1.05, 72))): add(hum(mtof(n - 12), 0.24), 25.6 + dt, 0.035)
chime(25.85, 96, 0.05)
bell(27.0, 0.22); cap(27.04)
creep(27.15, 2.8, 0.09)
for t in (27.45, 28.15, 28.85): heartbeat(t, 0.4)
cap(27.52); cap(28.22)
bell(28.95, 0.18); bell(29.2, 0.18)
add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), 29.5, 0.18)

x = buf[:NS]
x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR)); x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
x = np.tanh(x * 1.6); x = x / np.max(np.abs(x)) * 0.89
st = np.stack([x, x], 1); pcm = (st * 32767).astype('<i2')
w = wave.open('audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x) / SR)
